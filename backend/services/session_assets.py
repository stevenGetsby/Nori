"""Session and uploaded-asset service."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from fastapi import UploadFile

from nori.sessions import SessionEvent, SessionManager

from ..assets import append_session_assets, parse_metadata_json, save_uploaded_asset
from ..contracts import (
    ApiError,
    SessionCreateRequest,
    TaskCreateRequest,
    TurnCreateRequest,
)
from ..reference_urls import probe_reference_url, provider_fetchable_reference_url


class BackendSessionAssetService:
    """Owns backend session state, uploads, and asset file access."""

    def __init__(
        self,
        *,
        session_manager: SessionManager,
        upload_root: str | Path,
    ) -> None:
        self.session_manager = session_manager
        self.upload_root = Path(upload_root)

    def list_session_assets(self, session_id: str) -> dict[str, Any]:
        session = self.session_manager.get_session(session_id)
        if session is None:
            raise ApiError(f"session not found: {session_id}", status_code=404)
        return {
            "assets": [_asset_with_url(session_id, row) for row in session.metadata.get("assets", [])],
            "latest_reference_image_generation_check": latest_reference_image_generation_check(session.events),
        }

    def upload_session_assets(
        self,
        session_id: str,
        files: list[UploadFile],
        *,
        task_id: str = "",
        usage: str = "reference",
        metadata_json: str = "",
    ) -> dict[str, Any]:
        session = self.session_manager.get_session(session_id)
        if session is None:
            raise ApiError(f"session not found: {session_id}", status_code=404)
        if not files:
            raise ApiError("at least one file is required", status_code=400)
        try:
            metadata = parse_metadata_json(metadata_json)
            rows = [
                save_uploaded_asset(
                    upload=file,
                    upload_root=self.upload_root,
                    session_id=session_id,
                    task_id=task_id,
                    usage=usage,
                    metadata=metadata,
                )
                for file in files
            ]
        except ValueError as exc:
            raise ApiError(str(exc), status_code=400) from exc
        except Exception as exc:  # noqa: BLE001
            raise ApiError(f"asset upload failed: {type(exc).__name__}: {exc}", status_code=500) from exc
        session.metadata["assets"] = append_session_assets(session.metadata.get("assets"), rows)
        session.events.append(SessionEvent(event_type="assets_uploaded", payload={"assets": rows}))
        self.session_manager.save_session(session_id)
        return {"assets": [_asset_with_url(session_id, row) for row in rows]}

    def get_session_asset_file(self, session_id: str, asset_id: str) -> Path:
        session = self.session_manager.get_session(session_id)
        if session is None:
            raise ApiError(f"session not found: {session_id}", status_code=404)
        row = next(
            (item for item in session.metadata.get("assets", []) if str(item.get("asset_id") or "") == asset_id),
            None,
        )
        if row is None:
            raise ApiError(f"asset not found in session: {asset_id}", status_code=404)
        path = Path(str(row.get("path") or ""))
        if is_remote_url(str(path)):
            raise ApiError(f"asset is remote and has no local file: {asset_id}", status_code=400)
        if not path.is_file():
            raise ApiError(f"asset file not found: {asset_id}", status_code=404)
        return path

    def list_sessions(self) -> dict[str, Any]:
        return {"sessions": [session.to_dict() for session in self.session_manager.sessions.values()]}

    def create_session(self, request: SessionCreateRequest) -> dict[str, Any]:
        session = self.session_manager.create_session(
            user_id=request.user_id,
            profile_id=request.profile_id,
            metadata=dict(request.metadata),
        )
        return session.to_dict()

    def get_session(self, session_id: str) -> dict[str, Any]:
        session = self.session_manager.get_session(session_id)
        if session is None:
            raise ApiError(f"session not found: {session_id}", status_code=404)
        data = session.to_dict()
        data["latest_reference_image_generation_check"] = latest_reference_image_generation_check(session.events)
        return data

    def append_turn(self, session_id: str, request: TurnCreateRequest) -> dict[str, Any]:
        try:
            turn = self.session_manager.append_turn(
                session_id,
                role=request.role,
                content=request.content,
                metadata=dict(request.metadata),
            )
        except KeyError as exc:
            raise ApiError(str(exc).strip("'"), status_code=404) from exc
        return turn.to_dict()

    def start_task(self, session_id: str, request: TaskCreateRequest) -> dict[str, Any]:
        goal = request.goal.strip()
        if not goal:
            raise ApiError("goal is required", status_code=400)
        try:
            task = self.session_manager.start_task(
                session_id,
                goal=goal,
                workflow_name=request.workflow_name,
                acceptance=list(request.acceptance),
                metadata=dict(request.metadata),
            )
        except KeyError as exc:
            raise ApiError(str(exc).strip("'"), status_code=404) from exc
        return task.to_dict()



def assert_asset_paths_exist(rows: list[dict[str, Any]]) -> None:
    missing = [
        str(row.get("path") or "")
        for row in rows
        if not is_remote_url(str(row.get("path") or "")) and not Path(str(row.get("path") or "")).is_file()
    ]
    if missing:
        raise ValueError(f"asset path not found: {missing}")


def is_remote_url(value: str) -> bool:
    return value.startswith(("http://", "https://"))


def attach_public_reference_urls(
    session_id: str,
    rows: list[dict[str, Any]],
    *,
    public_base_url: str = "",
) -> list[dict[str, Any]]:
    base_url = backend_public_base_url(public_base_url)
    if not base_url:
        return [dict(row) for row in rows]
    out = []
    for row in rows:
        data = dict(row)
        asset_id = str(data.get("asset_id") or "")
        path = str(data.get("path") or "")
        backend_asset_url = backend_asset_public_reference_url(
            session_id,
            asset_id=asset_id,
            path=path,
            public_base_url=base_url,
        )
        if backend_asset_url:
            data["public_reference_url"] = backend_asset_url
        out.append(data)
    return out


def backend_asset_public_reference_url(
    session_id: str,
    *,
    asset_id: str,
    path: str,
    public_base_url: str = "",
) -> str:
    base_url = backend_public_base_url(public_base_url)
    if not base_url or not asset_id or not path or is_remote_url(path):
        return ""
    return f"{base_url}/sessions/{session_id}/assets/{asset_id}/file"


def backend_public_base_url(value: str = "") -> str:
    raw = str(value or os.environ.get("NORI_BACKEND_PUBLIC_BASE_URL") or "").strip().rstrip("/")
    return provider_fetchable_reference_url(raw)


def latest_reference_image_generation_check(events: list[SessionEvent] | list[Any]) -> dict[str, Any]:
    for event in reversed(list(events or [])):
        if getattr(event, "event_type", "") != "reference_image_generation_checked":
            continue
        payload = getattr(event, "payload", {})
        if not isinstance(payload, dict):
            payload = {}
        return {
            "event_id": str(getattr(event, "event_id", "") or ""),
            "created_at": str(getattr(event, "created_at", "") or ""),
            **dict(payload),
        }
    return {}


def reference_image_generation_run_evidence(
    latest_check: dict[str, Any],
    asset_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    selected_refs = provider_fetchable_refs_from_asset_rows(asset_rows)
    checked_refs = [
        str(item)
        for item in latest_check.get("provider_fetchable_reference_images") or []
        if provider_fetchable_reference_url(str(item))
    ]
    checked_ref_set = set(checked_refs)
    covered_refs = [url for url in selected_refs if url in checked_ref_set]
    missing_refs = [url for url in selected_refs if url not in checked_ref_set]
    return {
        **dict(latest_check),
        "selected_provider_fetchable_reference_images": selected_refs,
        "covered_selected_reference_images": covered_refs,
        "missing_selected_reference_images": missing_refs,
        "covers_selected_reference_images": bool(selected_refs) and not missing_refs,
    }


def provider_fetchable_refs_from_asset_rows(asset_rows: list[dict[str, Any]]) -> list[str]:
    urls: list[str] = []
    for row in asset_rows:
        for value in (row.get("public_reference_url"), row.get("path")):
            url = provider_fetchable_reference_url(str(value or ""))
            if url:
                urls.append(url)
                break
    return list(dict.fromkeys(urls))


def reference_url_probe_summary(payload: dict[str, Any], urls: list[str]) -> dict[str, Any]:
    enabled = bool(payload.get("verify_reference_urls"))
    unique_urls = list(dict.fromkeys(url for url in urls if url))
    if not enabled:
        return {
            "enabled": False,
            "passed": False,
            "checked_count": 0,
            "reachable_count": 0,
            "failed_count": 0,
            "items": [],
        }
    timeout = reference_url_probe_timeout(payload)
    items = [probe_reference_url(url, timeout=timeout) for url in unique_urls]
    reachable_count = sum(1 for item in items if item.get("reachable"))
    return {
        "enabled": True,
        "passed": bool(items) and reachable_count == len(items),
        "checked_count": len(items),
        "reachable_count": reachable_count,
        "failed_count": len(items) - reachable_count,
        "timeout_seconds": timeout,
        "items": items,
    }


def reference_url_probe_timeout(payload: dict[str, Any]) -> float:
    try:
        value = float(payload.get("reference_url_probe_timeout") or 3.0)
    except (TypeError, ValueError):
        return 3.0
    return min(max(value, 0.1), 30.0)


def _asset_with_url(session_id: str, row: dict[str, Any]) -> dict[str, Any]:
    data = dict(row)
    asset_id = str(data.get("asset_id") or "")
    if asset_id and not is_remote_url(str(data.get("path") or "")):
        data["file_url"] = f"/sessions/{session_id}/assets/{asset_id}/file"
    return data
