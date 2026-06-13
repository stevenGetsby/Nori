"""Content-production run orchestration service."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from nori.sessions import SessionEvent

from ..assets import select_assets
from ..contracts import ApiError, ContentProductionReplayRequest, ContentProductionRunRequest
from ..experiments import (
    ContentProductionRunFailed,
    experiment_readiness,
    get_content_production_case_selected_run,
    resolve_content_production_artifact_path,
)
from ..jobs import InProcessExperimentJobStore, enrich_content_run_result
from .content_production_preflight_actions import (
    _content_production_preflight_actions,
    _content_production_preflight_links,
    _content_production_template_actions,
)
from .content_production_preflight_checks import (
    _assert_content_production_run_gates,
    _content_production_preflight_checks,
    _content_production_template_checks,
)
from .content_production_preflight_summaries import (
    _asset_preflight_summary,
    _market_evidence_preflight_summary,
    _reference_image_preflight_summary,
)
from .session_assets import (
    assert_asset_paths_exist as _assert_asset_paths_exist,
    attach_public_reference_urls as _attach_public_reference_urls,
    backend_public_base_url as _backend_public_base_url,
    latest_reference_image_generation_check as _latest_reference_image_generation_check,
    reference_image_generation_run_evidence as _reference_image_generation_run_evidence,
)
from .session_store import BackendSessionStore


class BackendContentProductionRunService:
    """Owns content-production template, preflight, run, and replay orchestration."""

    def __init__(
        self,
        *,
        experiment_runner: Any,
        session_store: BackendSessionStore,
        job_store: InProcessExperimentJobStore,
        enforce_model_readiness: bool,
    ) -> None:
        self.experiment_runner = experiment_runner
        self.session_store = session_store
        self.session_manager = session_store.session_manager
        self.job_store = job_store
        self.enforce_model_readiness = bool(enforce_model_readiness)

    def experiment_readiness(self) -> dict[str, Any]:
        return experiment_readiness(project_root=self.experiment_runner.project_root)

    def content_production_run_template(
        self,
        *,
        session_id: str = "",
        task_id: str = "",
        case_id: str = "",
        case_title: str = "",
        platform: str = "xhs",
        goal: str = "",
        brief_text: str = "",
        asset_ids: list[str] | None = None,
        asset_paths: list[str] | None = None,
        backend_public_base_url: str = "",
        execution_mode: str = "sync",
        human_gate_mode: str = "skip",
        require_image_references: bool = False,
        require_reference_image_generation_check: bool = False,
        verify_reference_urls: bool = False,
        reference_url_probe_timeout: float = 3.0,
        market_evidence: dict[str, Any] | None = None,
        config: dict[str, Any] | None = None,
        request_metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        session_id = str(session_id or "").strip()
        session = self.session_store.get_session(session_id) if session_id else None
        metadata = dict(getattr(session, "metadata", {}) or {}) if session is not None else {}
        task = None
        task_id = str(task_id or "").strip()
        if session is not None and task_id:
            task = self.session_store.find_task(session, task_id)
        elif session is not None:
            task = self.session_store.latest_task(session)
        if task is not None and not task_id:
            task_id = task.task_id

        resolved_goal = str(goal or getattr(task, "goal", "") or metadata.get("goal") or brief_text or "").strip()
        resolved_brief = str(brief_text or metadata.get("brief_text") or resolved_goal).strip()
        resolved_case_id = str(case_id or metadata.get("case_id") or metadata.get("project") or session_id or "").strip()
        resolved_case_title = str(case_title or metadata.get("case_title") or resolved_case_id).strip()
        resolved_base_url = str(
            backend_public_base_url
            or metadata.get("backend_public_base_url")
            or _backend_public_base_url()
        ).strip()
        resolved_market_evidence = (
            dict(market_evidence)
            if isinstance(market_evidence, dict) and market_evidence
            else dict(metadata.get("market_evidence") or {})
            if isinstance(metadata.get("market_evidence"), dict)
            else {}
        )
        resolved_config = (
            dict(config)
            if isinstance(config, dict) and config
            else dict(metadata.get("config") or {})
            if isinstance(metadata.get("config"), dict)
            else {}
        )
        selected_assets: list[dict[str, Any]] = []
        asset_error = ""
        if session is not None:
            try:
                selected_assets = select_assets(metadata.get("assets", []), asset_ids=list(asset_ids or []))
                for path in asset_paths or []:
                    selected_assets.append(
                        {"asset_id": "", "kind": "image", "path": str(path), "filename": Path(str(path)).name}
                    )
                selected_assets = _attach_public_reference_urls(
                    session_id,
                    selected_assets,
                    public_base_url=resolved_base_url,
                )
            except ValueError as exc:
                asset_error = str(exc)

        payload_metadata = dict(request_metadata or {})
        payload_metadata.setdefault("source", "backend.content_production_run_template")
        request_payload = {
            "session_id": session_id,
            "task_id": task_id,
            "goal": resolved_goal,
            "brief_text": resolved_brief,
            "case_id": resolved_case_id,
            "case_title": resolved_case_title,
            "platform": str(platform or metadata.get("platform") or "xhs"),
            "asset_ids": [str(row.get("asset_id") or "") for row in selected_assets if row.get("asset_id")],
            "asset_paths": [str(row.get("path") or "") for row in selected_assets if not row.get("asset_id")],
            "backend_public_base_url": resolved_base_url,
            "execution_mode": _execution_mode(execution_mode),
            "human_gate_mode": str(human_gate_mode or "skip"),
            "require_image_references": bool(require_image_references),
            "require_reference_image_generation_check": bool(require_reference_image_generation_check),
            "verify_reference_urls": bool(verify_reference_urls),
            "reference_url_probe_timeout": reference_url_probe_timeout,
            "market_evidence": resolved_market_evidence,
            "config": resolved_config,
            "metadata": payload_metadata,
        }
        latest_reference_check = _latest_reference_image_generation_check(session.events if session is not None else [])
        if latest_reference_check:
            request_payload["reference_image_generation_check"] = _reference_image_generation_run_evidence(
                latest_reference_check,
                selected_assets,
            )
        readiness = self.experiment_readiness()
        checks = _content_production_template_checks(
            request_payload,
            session_exists=session is not None,
            task_exists=(not task_id or task is not None),
            asset_error=asset_error,
            selected_assets=selected_assets,
            readiness=readiness,
            has_custom_market_collector=getattr(self.experiment_runner, "top_notes_collector", None) is not None,
            enforce_model_readiness=self.enforce_model_readiness,
        )
        missing_fields = [check["name"] for check in checks if check["status"] == "failed"]
        asset_summary = _asset_preflight_summary(selected_assets)
        reference_summary = _reference_image_preflight_summary(
            request_payload,
            readiness=readiness,
            asset_rows=selected_assets,
        )
        reference_summary["latest_check"] = latest_reference_check
        reference_summary["latest_check_for_selected_references"] = dict(
            request_payload.get("reference_image_generation_check") or {}
        )
        return {
            "schema_version": 1,
            "ready_for_preflight": not missing_fields,
            "ready_for_run": not missing_fields,
            "missing_fields": missing_fields,
            "checks": checks,
            "request": request_payload,
            "session": {
                "session_id": session_id,
                "exists": session is not None,
                "task_id": task_id,
                "task_exists": bool(not task_id or task is not None),
                "will_create_task": bool(session is not None and not task_id),
            },
            "assets": asset_summary,
            "market_evidence": _market_evidence_preflight_summary(resolved_market_evidence),
            "reference_images": reference_summary,
            "actions": _content_production_template_actions(
                request_payload,
                checks=checks,
                session_id=session_id,
                asset_summary=asset_summary,
            ),
            "links": {
                "create_session": "/sessions",
                "upload_assets": f"/sessions/{session_id}/assets" if session_id else "/sessions/{session_id}/assets",
                "publish_references": (
                    f"/sessions/{session_id}/assets/publish-references"
                    if session_id
                    else "/sessions/{session_id}/assets/publish-references"
                ),
                "preflight": "/workflows/content-production/runs/preflight",
                "run": "/workflows/content-production/runs",
            },
        }

    def run_content_production(self, request: ContentProductionRunRequest) -> dict[str, Any]:
        payload = _model_data(request)
        prepared = self._prepare_content_production_run(payload, create_task=True, enforce_strict_references=True)
        execution_mode = str(prepared["execution_mode"])
        session_id = str(prepared["session_id"])
        task_id = str(prepared["task_id"])
        task = prepared["task"]
        session = prepared["session"]
        selected_assets = list(prepared["asset_rows"])

        if execution_mode == "background":
            task.status = "queued"
            job = self.job_store.create(
                job_type="content_production",
                metadata={
                    "session_id": session_id,
                    "task_id": task_id,
                    "case_id": str(payload.get("case_id") or session_id),
                    "asset_count": len(selected_assets),
                },
            )
            session.events.append(SessionEvent(event_type="workflow_run_queued", payload={"job": job}))
            self.session_store.save_session(session_id)
            self.job_store.start(
                job["job_id"],
                target=lambda: self._execute_content_production_run(
                    payload,
                    session_id=session_id,
                    task_id=task_id,
                    asset_rows=selected_assets,
                ),
            )
            return job

        try:
            result = self._execute_content_production_run(
                payload,
                session_id=session_id,
                task_id=task_id,
                asset_rows=selected_assets,
            )
        except ContentProductionRunFailed as exc:
            raise ApiError(
                f"content-production run failed: {exc}",
                status_code=500,
                data={
                    "run": enrich_content_run_result(
                        exc.failure_result,
                        metadata={"case_id": str(payload.get("case_id") or session_id), "session_id": session_id},
                    )
                },
            ) from exc
        except Exception as exc:  # noqa: BLE001
            raise ApiError(f"content-production run failed: {type(exc).__name__}: {exc}", status_code=500) from exc

        return result

    def preflight_content_production_run(self, request: ContentProductionRunRequest) -> dict[str, Any]:
        payload = _model_data(request)
        prepared = self._prepare_content_production_run(payload, create_task=False, enforce_strict_references=False)
        readiness = self.experiment_readiness()
        selected_assets = list(prepared["asset_rows"])
        reference_summary = _reference_image_preflight_summary(
            payload,
            readiness=readiness,
            asset_rows=selected_assets,
        )
        reference_summary["latest_check"] = _latest_reference_image_generation_check(
            prepared["session"].events if prepared.get("session") is not None else []
        )
        reference_summary["latest_check_for_selected_references"] = dict(
            payload.get("reference_image_generation_check") or {}
        )
        checks = _content_production_preflight_checks(
            payload,
            readiness=readiness,
            asset_rows=selected_assets,
            has_custom_market_collector=getattr(self.experiment_runner, "top_notes_collector", None) is not None,
            reference_summary=reference_summary,
        )
        ready = not any(check["status"] == "failed" for check in checks)
        asset_summary = _asset_preflight_summary(selected_assets)
        return {
            "ready": ready,
            "checks": checks,
            "session": {
                "session_id": prepared["session_id"],
                "task_id": prepared["task_id"],
                "will_create_task": not bool(prepared["task_id"]),
            },
            "run_options": {
                "case_id": str(payload.get("case_id") or prepared["session_id"]),
                "execution_mode": prepared["execution_mode"],
                "human_gate_mode": str(payload.get("human_gate_mode") or "skip"),
                "require_image_references": bool(payload.get("require_image_references")),
                "require_reference_image_generation_check": bool(
                    payload.get("require_reference_image_generation_check")
                ),
            },
            "assets": asset_summary,
            "market_evidence": _market_evidence_preflight_summary(payload.get("market_evidence")),
            "reference_images": reference_summary,
            "readiness": readiness,
            "actions": _content_production_preflight_actions(
                payload,
                checks=checks,
                session_id=str(prepared["session_id"] or ""),
                asset_summary=asset_summary,
            ),
            "links": _content_production_preflight_links(payload, session_id=str(prepared["session_id"] or "")),
        }

    def replay_content_production_run(
        self,
        case_id: str,
        run_id: str,
        request: ContentProductionReplayRequest,
    ) -> dict[str, Any]:
        replay_payload = self._load_replay_request(case_id, run_id)
        replay_data = _model_data(request)
        payload = _replay_payload_with_overrides(
            replay_payload,
            replay_data,
            source_case_id=case_id,
            source_run_id=run_id,
        )

        explicit_session_id = str(payload.pop("_explicit_session_id", "") or "").strip()
        explicit_task_id = str(payload.pop("_explicit_task_id", "") or "").strip()
        if explicit_session_id:
            self.session_store.require_session(explicit_session_id)
            payload["session_id"] = explicit_session_id
        else:
            session = self.session_store.create_session(
                metadata={
                    "source": "backend.replay_content_production_run",
                    "replay_of": {"case_id": case_id, "run_id": run_id},
                    "original_session_id": str(replay_payload.get("session_id") or ""),
                }
            )
            payload["session_id"] = session.session_id
            payload["asset_ids"] = []
            self.session_store.save_session(session.session_id)

        payload["task_id"] = explicit_task_id
        return self.run_content_production(ContentProductionRunRequest(**payload))

    def replay_content_production_case(
        self,
        case_id: str,
        request: ContentProductionReplayRequest,
    ) -> dict[str, Any]:
        replay_data = _model_data(request)
        source_run_id = str(replay_data.get("run_id") or "").strip()
        source = "request"
        if not source_run_id:
            try:
                selected = get_content_production_case_selected_run(
                    project_root=self.experiment_runner.project_root,
                    case_id=case_id,
                    fallback_to_best=True,
                )
            except FileNotFoundError as exc:
                raise ApiError(str(exc), status_code=404) from exc
            except ValueError as exc:
                raise ApiError(str(exc), status_code=400) from exc
            source_run_id = str(selected.get("run_id") or "")
            source = str(selected.get("source") or "")
        if not source_run_id:
            raise ApiError(f"no replayable run found for case: {case_id}", status_code=404)
        data = self.replay_content_production_run(case_id, source_run_id, request)
        if isinstance(data, dict):
            data.setdefault("source", "case_replay")
            data.setdefault("source_case_id", case_id)
            data.setdefault("source_run_id", source_run_id)
            data.setdefault("source_run_selector", source)
        return data

    def _load_replay_request(self, case_id: str, run_id: str) -> dict[str, Any]:
        try:
            path = resolve_content_production_artifact_path(
                project_root=self.experiment_runner.project_root,
                case_id=case_id,
                run_id=run_id,
                artifact_name="replay_request.json",
            )
        except FileNotFoundError as exc:
            raise ApiError(f"replay_request.json not found for run: {case_id}/{run_id}", status_code=404) from exc
        except ValueError as exc:
            raise ApiError(str(exc), status_code=404) from exc
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ApiError(f"invalid replay_request.json: {exc.msg}", status_code=400) from exc
        if not isinstance(data, dict) or not data:
            raise ApiError("replay_request.json must be a non-empty JSON object", status_code=400)
        return data

    def _prepare_content_production_run(
        self,
        payload: dict[str, Any],
        *,
        create_task: bool,
        enforce_strict_references: bool,
    ) -> dict[str, Any]:
        execution_mode = _execution_mode(payload.get("execution_mode"))
        session_id = str(payload.get("session_id") or "").strip()
        session = self.session_store.require_session(session_id)

        task_id = str(payload.get("task_id") or "").strip()
        task = None
        if task_id:
            task = self.session_store.find_task(session, task_id)
            if task is None:
                raise ApiError(f"task not found in session: {task_id}", status_code=404)
        else:
            goal = str(payload.get("goal") or payload.get("brief_text") or "").strip()
            if not goal:
                raise ApiError("goal or brief_text is required", status_code=400)

        try:
            selected_assets = select_assets(session.metadata.get("assets", []), asset_ids=list(payload.get("asset_ids") or []))
            for path in payload.get("asset_paths") or []:
                selected_assets.append({"asset_id": "", "kind": "image", "path": str(path), "filename": Path(str(path)).name})
            selected_assets = _attach_public_reference_urls(
                session_id,
                selected_assets,
                public_base_url=str(payload.get("backend_public_base_url") or ""),
            )
            _assert_asset_paths_exist(selected_assets)
        except ValueError as exc:
            raise ApiError(str(exc), status_code=400) from exc

        latest_reference_check = _latest_reference_image_generation_check(session.events)
        if latest_reference_check:
            payload["reference_image_generation_check"] = _reference_image_generation_run_evidence(
                latest_reference_check,
                selected_assets,
            )

        if enforce_strict_references and bool(payload.get("require_image_references")) and not selected_assets:
            raise ApiError("require_image_references=true requires at least one selected image asset", status_code=400)
        if enforce_strict_references:
            readiness = self.experiment_readiness()
            _assert_content_production_run_gates(
                payload,
                readiness=readiness,
                asset_rows=selected_assets,
                has_custom_market_collector=getattr(self.experiment_runner, "top_notes_collector", None) is not None,
                enforce_model_readiness=self.enforce_model_readiness,
            )

        if create_task and not task_id:
            goal = str(payload.get("goal") or payload.get("brief_text") or "").strip()
            task = self.session_store.start_task(
                session_id,
                goal=goal,
                workflow_name="content-production",
                acceptance=["content_design_spec", "content_package", "cover image", "summary"],
                metadata={"source": "backend.run_content_production"},
            )
            task_id = task.task_id

        return {
            "payload": payload,
            "execution_mode": execution_mode,
            "session_id": session_id,
            "session": session,
            "task_id": task_id,
            "task": task,
            "asset_rows": selected_assets,
        }

    def _execute_content_production_run(
        self,
        payload: dict[str, Any],
        *,
        session_id: str,
        task_id: str,
        asset_rows: list[dict[str, Any]],
    ) -> dict[str, Any]:
        session = self.session_store.get_session(session_id)
        task = self.session_store.find_task(session, task_id) if session is not None else None
        if task is not None:
            task.status = "running"
            self.session_store.save_session(session_id)
        try:
            result = self.experiment_runner.run(payload, session_id=session_id, task_id=task_id, asset_rows=asset_rows)
        except Exception as exc:
            if task is not None:
                task.status = "failed"
            if session is not None:
                failure_result = getattr(exc, "failure_result", None)
                payload_data = dict(failure_result) if isinstance(failure_result, dict) else {"task_id": task_id}
                payload_data.setdefault("task_id", task_id)
                payload_data = enrich_content_run_result(
                    payload_data,
                    metadata={"case_id": str(payload.get("case_id") or session_id), "session_id": session_id},
                ) or payload_data
                if isinstance(failure_result, dict) and hasattr(exc, "failure_result"):
                    exc.failure_result = dict(payload_data)
                session.events.append(SessionEvent(event_type="workflow_run_failed", payload=payload_data))
                self.session_store.save_session(session_id)
            raise
        result = enrich_content_run_result(
            result,
            metadata={"case_id": str(payload.get("case_id") or session_id), "session_id": session_id},
        ) or result
        if task is not None:
            task.status = str(result.get("status") or task.status)
        if session is not None:
            session.events.append(SessionEvent(event_type="workflow_run_finished", payload=result))
            self.session_store.save_session(session_id)
        return result



def _model_data(model: Any) -> dict[str, Any]:
    if hasattr(model, "model_dump"):
        return model.model_dump()
    return model.dict()


def _execution_mode(value: Any) -> str:
    mode = str(value or "sync").strip().lower()
    if mode in {"sync", "synchronous"}:
        return "sync"
    if mode in {"background", "async"}:
        return "background"
    raise ApiError(f"unsupported execution_mode: {value}", status_code=400)


_REPLAY_OVERRIDE_FIELDS = {
    "session_id",
    "task_id",
    "goal",
    "brief_text",
    "case_id",
    "case_title",
    "platform",
    "asset_ids",
    "asset_paths",
    "backend_public_base_url",
    "execution_mode",
    "human_gate_mode",
    "require_image_references",
    "require_reference_image_generation_check",
    "verify_reference_urls",
    "reference_url_probe_timeout",
    "market_evidence",
    "config",
    "metadata",
}


def _content_run_request_fields() -> set[str]:
    fields = getattr(ContentProductionRunRequest, "model_fields", None) or getattr(ContentProductionRunRequest, "__fields__", {})
    return set(fields)


def _replay_payload_with_overrides(
    replay_payload: dict[str, Any],
    replay_data: dict[str, Any],
    *,
    source_case_id: str,
    source_run_id: str,
) -> dict[str, Any]:
    run_fields = _content_run_request_fields()
    payload = {key: value for key, value in replay_payload.items() if key in run_fields}
    overrides = dict(replay_data.get("overrides") or {})
    invalid = sorted(key for key in overrides if key not in _REPLAY_OVERRIDE_FIELDS)
    if invalid:
        raise ApiError(f"unsupported replay override fields: {invalid}", status_code=400)
    payload.update({key: value for key, value in overrides.items() if key in run_fields})

    for key in ("case_id", "case_title", "execution_mode", "human_gate_mode", "backend_public_base_url"):
        value = str(replay_data.get(key) or "").strip()
        if value:
            payload[key] = value
    if replay_data.get("require_image_references") is not None:
        payload["require_image_references"] = bool(replay_data["require_image_references"])
    if replay_data.get("require_reference_image_generation_check") is not None:
        payload["require_reference_image_generation_check"] = bool(
            replay_data["require_reference_image_generation_check"]
        )
    if replay_data.get("verify_reference_urls") is not None:
        payload["verify_reference_urls"] = bool(replay_data["verify_reference_urls"])
    if replay_data.get("reference_url_probe_timeout") is not None:
        payload["reference_url_probe_timeout"] = replay_data["reference_url_probe_timeout"]

    original_metadata = payload.get("metadata") if isinstance(payload.get("metadata"), dict) else {}
    metadata = dict(original_metadata)
    replay_metadata = replay_data.get("metadata") if isinstance(replay_data.get("metadata"), dict) else {}
    metadata.update(replay_metadata)
    metadata["replay_of"] = {"case_id": source_case_id, "run_id": source_run_id}
    metadata.setdefault("source", "backend.replay_content_production_run")
    payload["metadata"] = metadata

    payload["_explicit_session_id"] = str(replay_data.get("session_id") or overrides.get("session_id") or "").strip()
    payload["_explicit_task_id"] = str(replay_data.get("task_id") or overrides.get("task_id") or "").strip()
    payload.setdefault("execution_mode", "sync")
    payload.setdefault("human_gate_mode", "skip")
    payload.setdefault("asset_ids", [])
    payload.setdefault("asset_paths", [])
    return payload
