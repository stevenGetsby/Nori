"""Session, asset upload, and reference-image service."""
from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import Any

from fastapi import UploadFile

from nori.core import llms
from nori.sessions import SessionEvent, SessionManager
from nori.storage import ObjectStoreError, ReferenceImagePublisher

from ..assets import append_session_assets, parse_metadata_json, save_uploaded_asset, select_assets
from ..contracts import (
    ApiError,
    AssetReferencePublishRequest,
    ReferenceImageGenerationCheckRequest,
    ReferencePublishCheckRequest,
    SessionCreateRequest,
    SessionReferenceImageGenerationCheckRequest,
    TaskCreateRequest,
    TurnCreateRequest,
)
from ..reference_urls import probe_reference_url, provider_fetchable_reference_url


class BackendSessionAssetService:
    """Owns backend session state, uploads, and reference-image publishing."""

    def __init__(
        self,
        *,
        session_manager: SessionManager,
        reference_publisher: Any | None = None,
        upload_root: str | Path,
    ) -> None:
        self.session_manager = session_manager
        self.reference_publisher = reference_publisher or ReferenceImagePublisher.from_env()
        self.upload_root = Path(upload_root)

    def check_reference_publish(self, request: ReferencePublishCheckRequest) -> dict[str, Any]:
        """Verify the configured reference publisher using a backend-owned tiny image."""

        with tempfile.TemporaryDirectory(prefix="nori_reference_publish_check_") as tmp_dir:
            path = Path(tmp_dir) / "reference_check.png"
            path.write_bytes(_TINY_REFERENCE_PNG)
            try:
                published = self.reference_publisher.publish_path(
                    str(path),
                    project=str(request.project or "diagnostics"),
                    session=str(request.session or "reference_publish_check"),
                    public_url_map=dict(request.public_url_map or {}),
                )
            except ObjectStoreError as exc:
                return _reference_publish_check_result(
                    ready=False,
                    path=path,
                    reason="object_store_error",
                    error_type=type(exc).__name__,
                    error=str(exc),
                    metadata=dict(request.metadata or {}),
                )
            except Exception as exc:  # noqa: BLE001
                return _reference_publish_check_result(
                    ready=False,
                    path=path,
                    reason="publish_error",
                    error_type=type(exc).__name__,
                    error=str(exc),
                    metadata=dict(request.metadata or {}),
                )
            public_url = str(getattr(published, "public_url", "") or getattr(published, "url", "") or "").strip()
            ready = bool(provider_fetchable_reference_url(public_url))
            return _reference_publish_check_result(
                ready=ready,
                path=path,
                reason=str(getattr(published, "reason", "") or ("public_url" if ready else "no_public_url")),
                public_reference_url=public_url,
                object_key=str(getattr(published, "key", "") or ""),
                uploaded=bool(getattr(published, "uploaded", False)),
                metadata=dict(request.metadata or {}),
            )

    def check_reference_image_generation(self, request: ReferenceImageGenerationCheckRequest) -> dict[str, Any]:
        """Verify that the active image provider accepts reference_images."""

        refs = [provider_fetchable_reference_url(str(item or "")) for item in request.reference_images]
        refs = [item for item in refs if item]
        if not refs:
            return _reference_image_generation_check_result(
                ready=False,
                reason="invalid_reference_images",
                prompt=str(request.prompt or ""),
                reference_images=list(request.reference_images or []),
                provider_fetchable_refs=[],
                size=str(request.size or ""),
                metadata=dict(request.metadata or {}),
            )
        prompt = str(request.prompt or "Generate a simple product image using the provided reference image.").strip()
        size = str(request.size or "1024x1024").strip() or "1024x1024"
        try:
            images = llms.image(prompt, usage="image", size=size, reference_images=refs)
        except Exception as exc:  # noqa: BLE001
            return _reference_image_generation_check_result(
                ready=False,
                reason="image_generation_error",
                prompt=prompt,
                reference_images=list(request.reference_images or []),
                provider_fetchable_refs=refs,
                size=size,
                error_type=type(exc).__name__,
                error=str(exc),
                metadata=dict(request.metadata or {}),
            )
        return _reference_image_generation_check_result(
            ready=bool(images),
            reason="image_generation_succeeded" if images else "empty_image_result",
            prompt=prompt,
            reference_images=list(request.reference_images or []),
            provider_fetchable_refs=refs,
            size=size,
            image_count=len(images or []),
            first_image_preview=str(images[0])[:80] if images else "",
            metadata=dict(request.metadata or {}),
        )

    def check_session_reference_image_generation(
        self,
        session_id: str,
        request: SessionReferenceImageGenerationCheckRequest,
    ) -> dict[str, Any]:
        """Publish selected session assets, then verify image-provider reference support."""

        publish_request = AssetReferencePublishRequest(
            asset_ids=list(request.asset_ids or []),
            project=str(request.project or ""),
            force=bool(request.force_publish),
            backend_public_base_url=str(request.backend_public_base_url or ""),
            public_url_map=dict(request.public_url_map or {}),
            metadata={**dict(request.metadata or {}), "source": "session_reference_image_generation_check"},
        )
        publish = self.publish_session_asset_references(session_id, publish_request)
        refs = _provider_fetchable_urls_from_publish_result(publish)
        url_probe = reference_url_probe_summary(
            {
                "verify_reference_urls": bool(request.verify_reference_urls),
                "reference_url_probe_timeout": request.reference_url_probe_timeout,
            },
            refs,
        )
        if not refs:
            result = _session_reference_image_generation_check_result(
                ready=False,
                reason="no_provider_fetchable_reference_images",
                publish=publish,
                generation=None,
                reference_images=[],
                url_probe=url_probe,
                metadata=dict(request.metadata or {}),
            )
            self._record_session_reference_image_generation_check(session_id, result)
            return result
        if bool(request.verify_reference_urls) and not bool(url_probe.get("passed")):
            result = _session_reference_image_generation_check_result(
                ready=False,
                reason="reference_url_probe_failed",
                publish=publish,
                generation=None,
                reference_images=refs,
                url_probe=url_probe,
                metadata=dict(request.metadata or {}),
            )
            self._record_session_reference_image_generation_check(session_id, result)
            return result
        generation = self.check_reference_image_generation(
            ReferenceImageGenerationCheckRequest(
                prompt=str(request.prompt or ""),
                reference_images=refs,
                size=str(request.size or ""),
                metadata={
                    **dict(request.metadata or {}),
                    "source": "session_reference_image_generation_check",
                    "session_id": session_id,
                },
            )
        )
        result = _session_reference_image_generation_check_result(
            ready=bool(generation.get("ready")),
            reason=str(generation.get("reason") or ""),
            publish=publish,
            generation=generation,
            reference_images=refs,
            url_probe=url_probe,
            metadata=dict(request.metadata or {}),
        )
        self._record_session_reference_image_generation_check(session_id, result)
        return result

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

    def publish_session_asset_references(
        self,
        session_id: str,
        request: AssetReferencePublishRequest,
    ) -> dict[str, Any]:
        session = self.session_manager.get_session(session_id)
        if session is None:
            raise ApiError(f"session not found: {session_id}", status_code=404)
        try:
            selected_assets = select_assets(session.metadata.get("assets", []), asset_ids=list(request.asset_ids or []))
            assert_asset_paths_exist(selected_assets)
        except ValueError as exc:
            raise ApiError(str(exc), status_code=400) from exc

        project = str(request.project or session.metadata.get("project") or session_id)
        results: list[dict[str, Any]] = []
        updated_rows: list[dict[str, Any]] = []
        for row in selected_assets:
            updated, result = self._publish_one_reference_asset(
                row,
                project=project,
                session_id=session_id,
                force=bool(request.force),
                backend_public_base_url=str(request.backend_public_base_url or ""),
                public_url_map=dict(request.public_url_map or {}),
            )
            results.append(result)
            if updated:
                updated_rows.append(updated)

        if updated_rows:
            session.metadata["assets"] = append_session_assets(session.metadata.get("assets"), updated_rows)
            session.events.append(
                SessionEvent(
                    event_type="asset_references_published",
                    payload={
                        "asset_ids": [row.get("asset_id") for row in updated_rows],
                        "metadata": dict(request.metadata or {}),
                    },
                )
            )
            self.session_manager.save_session(session_id)

        failed = [item for item in results if not item.get("public_reference_url")]
        return {
            "ready": not failed and bool(results),
            "selected_count": len(selected_assets),
            "published_count": len(results) - len(failed),
            "failed_count": len(failed),
            "assets": results,
        }

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

    def _record_session_reference_image_generation_check(self, session_id: str, result: dict[str, Any]) -> None:
        session = self.session_manager.get_session(session_id)
        if session is None:
            return
        session.events.append(
            SessionEvent(
                event_type="reference_image_generation_checked",
                payload=_session_reference_image_generation_event_payload(result),
            )
        )
        self.session_manager.save_session(session_id)

    def _publish_one_reference_asset(
        self,
        row: dict[str, Any],
        *,
        project: str,
        session_id: str,
        force: bool,
        backend_public_base_url: str,
        public_url_map: dict[str, str],
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        asset_id = str(row.get("asset_id") or "")
        path = str(row.get("path") or "")
        existing_url = str(row.get("public_reference_url") or "").strip()
        if provider_fetchable_reference_url(existing_url) and not force:
            result = _asset_publish_result(row, public_reference_url=existing_url, reason="existing_public_reference_url")
            return dict(row), result
        if is_remote_url(path):
            updated = {**row, "public_reference_url": path}
            return updated, _asset_publish_result(updated, public_reference_url=path, reason="remote")
        backend_asset_url = backend_asset_public_reference_url(
            session_id,
            asset_id=asset_id,
            path=path,
            public_base_url=backend_public_base_url,
        )
        if backend_asset_url:
            updated = {
                **row,
                "public_reference_url": backend_asset_url,
                "reference_publish_reason": "backend_public_base_url",
            }
            return updated, _asset_publish_result(
                updated,
                public_reference_url=backend_asset_url,
                reason="backend_public_base_url",
            )
        try:
            published = self.reference_publisher.publish_path(
                path,
                project=project,
                session=session_id,
                public_url_map=public_url_map,
            )
        except ObjectStoreError as exc:
            raise ApiError(f"reference asset publish failed: {exc}", status_code=502) from exc
        public_url = str(getattr(published, "public_url", "") or getattr(published, "url", "") or "").strip()
        updated = dict(row)
        if provider_fetchable_reference_url(public_url):
            updated["public_reference_url"] = public_url
            updated["reference_object_key"] = str(getattr(published, "key", "") or "")
            updated["reference_publish_reason"] = str(getattr(published, "reason", "") or "")
        return updated, {
            **_asset_publish_result(
                updated,
                public_reference_url=public_url,
                reason=str(getattr(published, "reason", "") or ""),
            ),
            "uploaded": bool(getattr(published, "uploaded", False)),
            "object_key": str(getattr(published, "key", "") or ""),
            "asset_id": asset_id,
        }


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


def _asset_publish_result(row: dict[str, Any], *, public_reference_url: str, reason: str) -> dict[str, Any]:
    path = str(row.get("path") or "")
    return {
        "asset_id": str(row.get("asset_id") or ""),
        "filename": str(row.get("filename") or Path(path).name),
        "path": path,
        "public_reference_url": public_reference_url,
        "reason": reason,
    }


_TINY_REFERENCE_PNG = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\xf8\x0f"
    b"\x00\x01\x01\x01\x00\x18\xdd\x8d\xb0\x00\x00\x00\x00IEND\xaeB`\x82"
)


def _reference_publish_check_result(
    *,
    ready: bool,
    path: Path,
    reason: str,
    public_reference_url: str = "",
    object_key: str = "",
    uploaded: bool = False,
    error_type: str = "",
    error: str = "",
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "ready": bool(ready),
        "reason": reason,
        "public_reference_url": public_reference_url,
        "provider_fetchable": bool(provider_fetchable_reference_url(public_reference_url)),
        "uploaded": bool(uploaded),
        "object_key": object_key,
        "test_image": {
            "filename": path.name,
            "size_bytes": path.stat().st_size if path.exists() else 0,
            "content_type": "image/png",
        },
        "error_type": error_type,
        "error": error,
        "metadata": dict(metadata or {}),
        "next_actions": _reference_publish_check_actions(ready=ready, reason=reason, error=error),
    }


def _reference_publish_check_actions(*, ready: bool, reason: str, error: str) -> list[dict[str, str]]:
    if ready:
        return [
            {
                "action_id": "run_strict_preflight",
                "severity": "next_step",
                "message": "Run content-production preflight with require_image_references=true.",
            }
        ]
    actions = [
        {
            "action_id": "configure_reference_publisher",
            "severity": "blocking",
            "message": "Configure OSS/TOS env vars or backend_public_base_url so reference images become HTTPS URLs.",
        }
    ]
    if reason == "object_store_error" or error:
        actions.append(
            {
                "action_id": "check_object_store_permissions",
                "severity": "blocking",
                "message": "Check object store credentials, bucket, endpoint, region, and write permissions.",
            }
        )
    return actions


def _reference_image_generation_check_result(
    *,
    ready: bool,
    reason: str,
    prompt: str,
    reference_images: list[str],
    provider_fetchable_refs: list[str],
    size: str,
    image_count: int = 0,
    first_image_preview: str = "",
    error_type: str = "",
    error: str = "",
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "ready": bool(ready),
        "reason": reason,
        "prompt": prompt,
        "size": size,
        "reference_count": len(reference_images),
        "provider_fetchable_count": len(provider_fetchable_refs),
        "reference_images": list(reference_images),
        "provider_fetchable_reference_images": list(provider_fetchable_refs),
        "image_count": int(image_count),
        "first_image_preview": first_image_preview,
        "error_type": error_type,
        "error": error,
        "metadata": dict(metadata or {}),
        "next_actions": _reference_image_generation_check_actions(ready=ready, reason=reason),
    }


def _reference_image_generation_check_actions(*, ready: bool, reason: str) -> list[dict[str, str]]:
    if ready:
        return [
            {
                "action_id": "run_strict_content_production",
                "severity": "next_step",
                "message": "Run the full content-production workflow with require_image_references=true.",
            }
        ]
    if reason == "invalid_reference_images":
        return [
            {
                "action_id": "publish_reference_assets",
                "severity": "blocking",
                "message": "Publish uploaded assets to provider-fetchable HTTPS URLs before checking image generation.",
            }
        ]
    return [
        {
            "action_id": "inspect_image_model_config",
            "severity": "blocking",
            "message": "Inspect active image model configuration and provider reference-image support.",
        }
    ]


def _provider_fetchable_urls_from_publish_result(publish: dict[str, Any]) -> list[str]:
    assets = publish.get("assets") if isinstance(publish.get("assets"), list) else []
    urls: list[str] = []
    for item in assets:
        if not isinstance(item, dict):
            continue
        url = provider_fetchable_reference_url(str(item.get("public_reference_url") or ""))
        if url:
            urls.append(url)
    return list(dict.fromkeys(urls))


def _session_reference_image_generation_check_result(
    *,
    ready: bool,
    reason: str,
    publish: dict[str, Any],
    generation: dict[str, Any] | None,
    reference_images: list[str],
    url_probe: dict[str, Any] | None,
    metadata: dict[str, Any],
) -> dict[str, Any]:
    failed_publish = int(publish.get("failed_count") or 0) if isinstance(publish, dict) else 0
    return {
        "ready": bool(ready),
        "reason": reason,
        "selected_count": int(publish.get("selected_count") or 0) if isinstance(publish, dict) else 0,
        "published_count": int(publish.get("published_count") or 0) if isinstance(publish, dict) else 0,
        "failed_count": failed_publish,
        "provider_fetchable_count": len(reference_images),
        "provider_fetchable_reference_images": list(reference_images),
        "publish": dict(publish or {}),
        "url_probe": dict(url_probe or {}),
        "generation": dict(generation or {}),
        "metadata": dict(metadata or {}),
        "next_actions": _session_reference_image_generation_check_actions(
            ready=bool(ready),
            reason=reason,
            failed_publish=failed_publish,
        ),
    }


def _session_reference_image_generation_event_payload(result: dict[str, Any]) -> dict[str, Any]:
    generation = result.get("generation") if isinstance(result.get("generation"), dict) else {}
    url_probe = result.get("url_probe") if isinstance(result.get("url_probe"), dict) else {}
    return {
        "ready": bool(result.get("ready")),
        "reason": str(result.get("reason") or ""),
        "selected_count": int(result.get("selected_count") or 0),
        "published_count": int(result.get("published_count") or 0),
        "failed_count": int(result.get("failed_count") or 0),
        "provider_fetchable_count": int(result.get("provider_fetchable_count") or 0),
        "provider_fetchable_reference_images": list(result.get("provider_fetchable_reference_images") or []),
        "url_probe": {
            "enabled": bool(url_probe.get("enabled")),
            "passed": bool(url_probe.get("passed")),
            "checked_count": int(url_probe.get("checked_count") or 0),
            "reachable_count": int(url_probe.get("reachable_count") or 0),
            "failed_count": int(url_probe.get("failed_count") or 0),
        },
        "generation": {
            "ready": bool(generation.get("ready")),
            "reason": str(generation.get("reason") or ""),
            "image_count": int(generation.get("image_count") or 0),
            "error_type": str(generation.get("error_type") or ""),
            "error": str(generation.get("error") or ""),
        },
        "metadata": dict(result.get("metadata") or {}),
    }


def _session_reference_image_generation_check_actions(
    *,
    ready: bool,
    reason: str,
    failed_publish: int,
) -> list[dict[str, str]]:
    if ready:
        return [
            {
                "action_id": "run_strict_preflight",
                "severity": "next_step",
                "message": "Run strict reference preflight or the full content-production experiment.",
            }
        ]
    if reason == "no_provider_fetchable_reference_images" or failed_publish:
        return [
            {
                "action_id": "set_backend_public_base_url_or_configure_oss",
                "severity": "blocking",
                "message": "Provide a real backend_public_base_url or configure OSS so session assets become public HTTPS references.",
            }
        ]
    if reason == "reference_url_probe_failed":
        return [
            {
                "action_id": "fix_reference_url_reachability",
                "severity": "blocking",
                "message": "Fix the backend public URL, HTTPS tunnel, CDN, or object-store public access before calling the image model.",
            }
        ]
    return [
        {
            "action_id": "inspect_image_model_config",
            "severity": "blocking",
            "message": "Inspect active image model configuration and provider reference-image support.",
        }
    ]
