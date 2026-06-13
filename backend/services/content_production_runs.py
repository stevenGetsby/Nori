"""Content-production run orchestration service."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from nori.sessions import SessionEvent, SessionManager

from ..assets import select_assets
from ..contracts import ApiError, ContentProductionReplayRequest, ContentProductionRunRequest
from ..experiments import (
    ContentProductionRunFailed,
    experiment_readiness,
    get_content_production_case_selected_run,
    resolve_content_production_artifact_path,
)
from ..jobs import InProcessExperimentJobStore, enrich_content_run_result
from ..reference_urls import provider_fetchable_reference_url
from .session_assets import (
    assert_asset_paths_exist as _assert_asset_paths_exist,
    attach_public_reference_urls as _attach_public_reference_urls,
    backend_public_base_url as _backend_public_base_url,
    is_remote_url as _is_remote_url,
    latest_reference_image_generation_check as _latest_reference_image_generation_check,
    reference_image_generation_run_evidence as _reference_image_generation_run_evidence,
    reference_url_probe_summary as _reference_url_probe_summary,
    reference_url_probe_timeout as _reference_url_probe_timeout,
)


class BackendContentProductionRunService:
    """Owns content-production template, preflight, run, and replay orchestration."""

    def __init__(
        self,
        *,
        experiment_runner: Any,
        session_manager: SessionManager,
        job_store: InProcessExperimentJobStore,
        enforce_model_readiness: bool,
    ) -> None:
        self.experiment_runner = experiment_runner
        self.session_manager = session_manager
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
        session = self.session_manager.get_session(session_id) if session_id else None
        metadata = dict(getattr(session, "metadata", {}) or {}) if session is not None else {}
        task = None
        task_id = str(task_id or "").strip()
        if session is not None and task_id:
            task = next((item for item in session.task_goals if item.task_id == task_id), None)
        elif session is not None and session.task_goals:
            task = session.task_goals[-1]
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
            self.session_manager.save_session(session_id)
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
            session = self.session_manager.get_session(explicit_session_id)
            if session is None:
                raise ApiError(f"session not found: {explicit_session_id}", status_code=404)
            payload["session_id"] = explicit_session_id
        else:
            session = self.session_manager.create_session(
                metadata={
                    "source": "backend.replay_content_production_run",
                    "replay_of": {"case_id": case_id, "run_id": run_id},
                    "original_session_id": str(replay_payload.get("session_id") or ""),
                }
            )
            payload["session_id"] = session.session_id
            payload["asset_ids"] = []
            self.session_manager.save_session(session.session_id)

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
        session = self.session_manager.get_session(session_id)
        if session is None:
            raise ApiError(f"session not found: {session_id}", status_code=404)

        task_id = str(payload.get("task_id") or "").strip()
        task = None
        if task_id:
            task = next((item for item in session.task_goals if item.task_id == task_id), None)
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
            task = self.session_manager.start_task(
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
        session = self.session_manager.get_session(session_id)
        task = next((item for item in session.task_goals if item.task_id == task_id), None) if session else None
        if task is not None:
            task.status = "running"
            self.session_manager.save_session(session_id)
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
                self.session_manager.save_session(session_id)
            raise
        result = enrich_content_run_result(
            result,
            metadata={"case_id": str(payload.get("case_id") or session_id), "session_id": session_id},
        ) or result
        if task is not None:
            task.status = str(result.get("status") or task.status)
        if session is not None:
            session.events.append(SessionEvent(event_type="workflow_run_finished", payload=result))
            self.session_manager.save_session(session_id)
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


def _content_production_template_checks(
    payload: dict[str, Any],
    *,
    session_exists: bool,
    task_exists: bool,
    asset_error: str,
    selected_assets: list[dict[str, Any]],
    readiness: dict[str, Any],
    has_custom_market_collector: bool,
    enforce_model_readiness: bool,
) -> list[dict[str, str]]:
    has_goal = bool(str(payload.get("goal") or payload.get("brief_text") or "").strip())
    checks = [
        _preflight_check(
            "session",
            "passed" if session_exists else "failed",
            "session exists" if session_exists else "create or select a backend session",
        ),
        _preflight_check(
            "task",
            "passed" if task_exists else "failed",
            "task exists or will be created" if task_exists else "selected task_id does not exist in session",
        ),
        _preflight_check(
            "goal_or_brief_text",
            "passed" if has_goal else "failed",
            "goal or brief_text is ready" if has_goal else "goal or brief_text is required",
        ),
        _preflight_check(
            "asset_selection",
            "failed" if asset_error else "passed",
            asset_error or "asset selection is valid",
        ),
    ]
    checks.extend(
        _content_production_preflight_checks(
            payload,
            readiness=readiness,
            asset_rows=selected_assets,
            has_custom_market_collector=has_custom_market_collector,
        )
    )
    if not enforce_model_readiness:
        checks = [
            {
                **check,
                "status": "warning",
                "message": "model readiness is not enforced for this runner",
            }
            if check["name"] == "models_ready" and check["status"] == "failed"
            else check
            for check in checks
        ]
    return checks


def _content_production_template_actions(
    payload: dict[str, Any],
    *,
    checks: list[dict[str, str]],
    session_id: str,
    asset_summary: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    failed = {check["name"] for check in checks if check["status"] == "failed"}
    actions: list[dict[str, Any]] = []
    if "session" in failed:
        actions.append(
            {
                "action_id": "create_session",
                "severity": "blocking",
                "method": "POST",
                "href": "/sessions",
                "payload": {"metadata": _template_session_metadata(payload)},
                "message": "Create a backend session before uploading assets or running the experiment.",
            }
        )
    if "goal_or_brief_text" in failed:
        actions.append(
            {
                "action_id": "add_brief",
                "severity": "blocking",
                "method": "POST",
                "href": "/experiments/content-production/run-template",
                "payload": payload,
                "input_fields": ["goal", "brief_text"],
                "message": "Add goal or brief_text to the run request template.",
            }
        )
    if "asset_selection" in failed:
        actions.append(
            {
                "action_id": "fix_asset_selection",
                "severity": "blocking",
                "method": "POST",
                "href": f"/sessions/{session_id}/assets" if session_id else "/sessions/{session_id}/assets",
                "payload": {"usage": "reference"},
                "input_fields": ["asset_ids", "asset_paths", "files"],
                "message": "Remove missing asset_ids or upload the referenced assets into this session.",
            }
        )
    if "models_ready" in failed:
        actions.append(
            {
                "action_id": "configure_active_models",
                "severity": "blocking",
                "method": "GET",
                "href": "/experiments/readiness",
                "message": "Fix active LLM, vision, or image model configuration before running.",
            }
        )
    if "market_evidence" in failed:
        actions.append(
            {
                "action_id": "attach_market_evidence",
                "severity": "blocking",
                "method": "POST",
                "href": "/experiments/content-production/run-template",
                "payload": payload,
                "input_fields": ["market_evidence"],
                "message": "Attach market_evidence or configure a backend collector before running.",
            }
        )
    if "reference_assets_selected" in failed:
        actions.append(
            {
                "action_id": "upload_reference_assets",
                "severity": "blocking",
                "method": "POST",
                "href": f"/sessions/{session_id}/assets" if session_id else "/sessions/{session_id}/assets",
                "message": "Upload or select image assets for strict reference mode.",
            }
        )
    if "reference_transfer" in failed:
        actions.append(
            {
                "action_id": "publish_reference_assets",
                "severity": "blocking",
                "method": "POST",
                "href": (
                    f"/sessions/{session_id}/assets/publish-references"
                    if session_id
                    else "/sessions/{session_id}/assets/publish-references"
                ),
                "payload": _publish_reference_action_payload(payload),
                "message": "Publish selected assets or configure backend_public_base_url so the image provider can fetch references.",
            }
        )
    if "reference_image_generation_check" in failed:
        reference_check_action = _reference_image_generation_action(
            payload,
            session_id=session_id,
            asset_summary=asset_summary,
            required=True,
        )
        if reference_check_action:
            actions.append(reference_check_action)
    if not failed:
        actions.extend(
            [
                {
                    "action_id": "run_preflight",
                    "severity": "next_step",
                    "method": "POST",
                    "href": "/workflows/content-production/runs/preflight",
                    "payload": payload,
                    "message": "Run preflight with this request before live generation.",
                },
                {
                    "action_id": "run_experiment",
                    "severity": "next_step",
                    "method": "POST",
                    "href": "/workflows/content-production/runs",
                    "payload": payload,
                    "message": "Run the backend content-production experiment.",
                },
            ]
        )
        reference_check_action = _reference_image_generation_action(
            payload,
            session_id=session_id,
            asset_summary=asset_summary,
        )
        if reference_check_action:
            actions.append(reference_check_action)
    return actions


def _template_session_metadata(payload: dict[str, Any]) -> dict[str, Any]:
    metadata: dict[str, Any] = {}
    for key in ("case_id", "case_title", "goal", "brief_text", "platform", "backend_public_base_url"):
        value = payload.get(key)
        if value:
            metadata[key] = value
    for key in ("market_evidence", "config"):
        value = payload.get(key)
        if isinstance(value, dict) and value:
            metadata[key] = dict(value)
    return metadata


def _publish_reference_action_payload(payload: dict[str, Any]) -> dict[str, Any]:
    action_payload: dict[str, Any] = {"asset_ids": list(payload.get("asset_ids") or [])}
    backend_public_base_url = str(payload.get("backend_public_base_url") or "").strip()
    if backend_public_base_url:
        action_payload["backend_public_base_url"] = backend_public_base_url
    return action_payload


def _reference_image_generation_action(
    payload: dict[str, Any],
    *,
    session_id: str,
    asset_summary: dict[str, Any] | None,
    required: bool = False,
) -> dict[str, Any] | None:
    if not bool(payload.get("require_image_references")):
        return None
    urls = _provider_fetchable_urls_from_asset_summary(asset_summary)
    if not urls:
        return None
    asset_ids = [str(value) for value in payload.get("asset_ids") or [] if str(value)]
    if session_id and asset_ids:
        return {
            "action_id": "check_reference_image_generation",
            "severity": "blocking" if required else "optional",
            "method": "POST",
            "href": f"/sessions/{session_id}/assets/reference-image-generation-check",
            "payload": {
                "asset_ids": asset_ids,
                "backend_public_base_url": str(payload.get("backend_public_base_url") or ""),
                "verify_reference_urls": bool(payload.get("verify_reference_urls")),
                "reference_url_probe_timeout": _reference_url_probe_timeout(payload),
                "prompt": "Generate a simple product image using the selected session reference image.",
                "size": "1024x1024",
                "metadata": {
                    "source": "content_production_preflight",
                    "case_id": str(payload.get("case_id") or ""),
                },
            },
            "message": (
                "Publish selected session assets and verify that the active image provider accepts them as "
                "reference_images before this strict run."
                if required
                else "Optionally publish selected session assets and verify that the active image provider accepts them as reference_images before the full run."
            ),
        }
    return {
        "action_id": "check_reference_image_generation",
        "severity": "blocking" if required else "optional",
        "method": "POST",
        "href": "/experiments/content-production/reference-image-generation-check",
        "payload": {
            "prompt": "Generate a simple product image using the selected reference image.",
            "reference_images": urls,
            "size": "1024x1024",
            "metadata": {
                "source": "content_production_preflight",
                "case_id": str(payload.get("case_id") or ""),
            },
        },
        "message": (
            "Verify that the active image provider accepts these reference_images before this strict run."
            if required
            else "Optionally verify that the active image provider accepts these reference_images before the full run."
        ),
    }


def _provider_fetchable_urls_from_asset_summary(asset_summary: dict[str, Any] | None) -> list[str]:
    summary = asset_summary if isinstance(asset_summary, dict) else {}
    items = summary.get("items") if isinstance(summary.get("items"), list) else []
    urls: list[str] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        url = provider_fetchable_reference_url(str(item.get("provider_fetchable_url") or ""))
        if url:
            urls.append(url)
    return list(dict.fromkeys(urls))


def _content_production_preflight_actions(
    payload: dict[str, Any],
    *,
    checks: list[dict[str, str]],
    session_id: str,
    asset_summary: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    failed = {check["name"] for check in checks if check["status"] == "failed"}
    if not failed:
        actions = [
            {
                "action_id": "run_experiment",
                "severity": "next_step",
                "method": "POST",
                "href": "/workflows/content-production/runs",
                "payload": payload,
                "message": "Run the backend content-production experiment with the preflight-validated request.",
            }
        ]
        reference_check_action = _reference_image_generation_action(
            payload,
            session_id=session_id,
            asset_summary=asset_summary,
        )
        if reference_check_action:
            actions.append(reference_check_action)
        return actions

    actions: list[dict[str, Any]] = []
    if "models_ready" in failed:
        actions.append(
            {
                "action_id": "configure_active_models",
                "severity": "blocking",
                "method": "GET",
                "href": "/experiments/readiness",
                "message": "Fix active LLM, vision, or image model configuration before running.",
            }
        )
    if "market_evidence" in failed:
        actions.append(
            {
                "action_id": "attach_market_evidence",
                "severity": "blocking",
                "method": "POST",
                "href": "/experiments/content-production/run-template",
                "payload": payload,
                "input_fields": ["market_evidence"],
                "message": "Attach market_evidence or configure a backend collector before running.",
            }
        )
    if "reference_assets_selected" in failed:
        actions.append(
            {
                "action_id": "upload_reference_assets",
                "severity": "blocking",
                "method": "POST",
                "href": f"/sessions/{session_id}/assets" if session_id else "/sessions/{session_id}/assets",
                "payload": {"usage": "reference"},
                "input_fields": ["asset_ids", "asset_paths", "files"],
                "message": "Upload or select image assets for strict reference mode.",
            }
        )
    if "reference_transfer" in failed:
        actions.extend(
            [
                {
                    "action_id": "publish_reference_assets",
                    "severity": "blocking",
                    "method": "POST",
                    "href": (
                        f"/sessions/{session_id}/assets/publish-references"
                        if session_id
                        else "/sessions/{session_id}/assets/publish-references"
                    ),
                    "payload": _publish_reference_action_payload(payload),
                    "message": "Publish selected assets so the image provider can fetch reference images.",
                },
                {
                    "action_id": "set_backend_public_base_url",
                    "severity": "blocking",
                    "method": "POST",
                    "href": "/experiments/content-production/run-template",
                    "payload": payload,
                    "input_fields": ["backend_public_base_url"],
                    "message": "Provide a backend_public_base_url when local uploads should be served through the backend.",
                },
            ]
        )
    if "reference_url_reachability" in failed:
        actions.extend(
            [
                {
                    "action_id": "verify_reference_urls",
                    "severity": "blocking",
                    "method": "POST",
                    "href": "/workflows/content-production/runs/preflight",
                    "payload": {**payload, "verify_reference_urls": True},
                    "input_fields": ["backend_public_base_url", "verify_reference_urls"],
                    "message": "Verify that selected reference URLs can be reached before live strict-reference generation.",
                },
                {
                    "action_id": "set_backend_public_base_url",
                    "severity": "blocking",
                    "method": "POST",
                    "href": "/experiments/content-production/run-template",
                    "payload": payload,
                    "input_fields": ["backend_public_base_url"],
                    "message": "Provide a reachable public backend URL, HTTPS tunnel, or OSS reference URL.",
                },
            ]
        )
    if "reference_image_generation_check" in failed:
        reference_check_action = _reference_image_generation_action(
            payload,
            session_id=session_id,
            asset_summary=asset_summary,
            required=True,
        )
        if reference_check_action:
            actions.append(reference_check_action)
    return actions


def _content_production_preflight_links(payload: dict[str, Any], *, session_id: str) -> dict[str, str]:
    case_id = str(payload.get("case_id") or "")
    template = "/experiments/content-production/run-template"
    if case_id:
        template = f"{template}?case_id={case_id}"
    return {
        "run_template": template,
        "run": "/workflows/content-production/runs",
        "preflight": "/workflows/content-production/runs/preflight",
        "upload_assets": f"/sessions/{session_id}/assets" if session_id else "/sessions/{session_id}/assets",
        "publish_references": (
            f"/sessions/{session_id}/assets/publish-references"
            if session_id
            else "/sessions/{session_id}/assets/publish-references"
        ),
    }


def _content_production_preflight_checks(
    payload: dict[str, Any],
    *,
    readiness: dict[str, Any],
    asset_rows: list[dict[str, Any]],
    has_custom_market_collector: bool,
    reference_summary: dict[str, Any] | None = None,
) -> list[dict[str, str]]:
    reference = reference_summary or _reference_image_preflight_summary(payload, readiness=readiness, asset_rows=asset_rows)
    market = _market_evidence_preflight_summary(payload.get("market_evidence"))
    strict_references = bool(payload.get("require_image_references"))
    checks = [
        _preflight_check(
            "models_ready",
            "passed" if bool(readiness.get("ready")) else "failed",
            "active LLM, vision, and image model configuration is ready"
            if bool(readiness.get("ready"))
            else "one or more active model configurations are not ready",
        ),
        _preflight_check(
            "market_evidence",
            "passed" if market["provided"] or has_custom_market_collector else "failed",
            "market evidence is provided or a custom collector is configured"
            if market["provided"] or has_custom_market_collector
            else "market_evidence is required when the backend runner has no custom collector",
        ),
        _preflight_check(
            "reference_assets_selected",
            "passed" if asset_rows else ("failed" if strict_references else "warning"),
            "selected image references are available"
            if asset_rows
            else "no image reference assets are selected for this run",
        ),
    ]
    if asset_rows:
        status = "passed" if reference["can_send_selected_references"] else ("failed" if strict_references else "warning")
        checks.append(
            _preflight_check(
                "reference_transfer",
                status,
                "selected references can be sent to the image provider"
                if reference["can_send_selected_references"]
                else "selected local references need OSS or provider-fetchable HTTPS URLs before they can be sent",
            )
        )
        probe = reference.get("url_probe") if isinstance(reference.get("url_probe"), dict) else {}
        if probe.get("enabled"):
            probe_passed = bool(probe.get("passed"))
            checks.append(
                _preflight_check(
                    "reference_url_reachability",
                    "passed" if probe_passed else ("failed" if strict_references else "warning"),
                    "selected reference URLs are reachable from the backend"
                    if probe_passed
                    else "selected reference URLs could not be reached from the backend before live generation",
                )
            )
    generation_check = _reference_image_generation_gate_check(payload)
    if generation_check is not None:
        checks.append(generation_check)
    return checks


def _reference_image_generation_gate_check(payload: dict[str, Any]) -> dict[str, str] | None:
    if not bool(payload.get("require_reference_image_generation_check")):
        return None
    evidence = payload.get("reference_image_generation_check") if isinstance(
        payload.get("reference_image_generation_check"),
        dict,
    ) else {}
    ready = bool(evidence.get("ready"))
    covers_selected = bool(evidence.get("covers_selected_reference_images"))
    if ready and covers_selected:
        return _preflight_check(
            "reference_image_generation_check",
            "passed",
            "latest image-provider reference check covers the selected references",
        )
    if not evidence:
        message = "run requires a successful image-provider reference check before generation"
    elif not ready:
        reason = str(evidence.get("reason") or "not_ready")
        message = f"latest image-provider reference check is not ready: {reason}"
    else:
        missing = list(evidence.get("missing_selected_reference_images") or [])
        message = (
            "latest image-provider reference check does not cover all selected references"
            if not missing
            else f"latest image-provider reference check is missing selected references: {missing}"
        )
    return _preflight_check("reference_image_generation_check", "failed", message)


def _assert_content_production_run_gates(
    payload: dict[str, Any],
    *,
    readiness: dict[str, Any],
    asset_rows: list[dict[str, Any]],
    has_custom_market_collector: bool,
    enforce_model_readiness: bool = False,
) -> None:
    """Reject deterministic run blockers before task creation or model calls."""

    checked_names = {
        "market_evidence",
        "reference_assets_selected",
        "reference_transfer",
        "reference_url_reachability",
        "reference_image_generation_check",
    }
    if enforce_model_readiness:
        checked_names.add("models_ready")
    failures = [
        check
        for check in _content_production_preflight_checks(
            payload,
            readiness=readiness,
            asset_rows=asset_rows,
            has_custom_market_collector=has_custom_market_collector,
        )
        if check["name"] in checked_names and check["status"] == "failed"
    ]
    if not failures:
        return
    message = "; ".join(f"{check['name']}: {check['message']}" for check in failures)
    raise ApiError(
        f"content-production run preflight failed: {message}",
        status_code=400,
        data={
            "checks": failures,
            "actions": _content_production_preflight_actions(
                payload,
                checks=failures,
                session_id=str(payload.get("session_id") or ""),
                asset_summary=_asset_preflight_summary(asset_rows),
            ),
            "links": _content_production_preflight_links(payload, session_id=str(payload.get("session_id") or "")),
        },
    )


def _preflight_check(name: str, status: str, message: str) -> dict[str, str]:
    return {"name": name, "status": status, "message": message}


def _asset_preflight_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    fetchable = [_reference_fetchable_url(row) for row in rows]
    return {
        "selected_count": len(rows),
        "local_count": sum(1 for row in rows if not _is_remote_url(str(row.get("path") or ""))),
        "remote_count": sum(1 for row in rows if _is_remote_url(str(row.get("path") or ""))),
        "provider_fetchable_count": sum(1 for value in fetchable if value),
        "items": [
            {
                "asset_id": str(row.get("asset_id") or ""),
                "kind": str(row.get("kind") or ""),
                "filename": str(row.get("filename") or Path(str(row.get("path") or "")).name),
                "path": str(row.get("path") or ""),
                "public_reference_url": str(row.get("public_reference_url") or ""),
                "provider_fetchable_url": fetchable_url,
            }
            for row, fetchable_url in zip(rows, fetchable)
        ],
    }


def _market_evidence_preflight_summary(value: Any) -> dict[str, Any]:
    evidence = value if isinstance(value, dict) else {}
    return {
        "provided": bool(evidence),
        "queries": [str(item) for item in evidence.get("queries") or []],
        "hot_note_count": len(evidence.get("hot_notes") or []),
        "insufficient_count": len(evidence.get("insufficient") or []),
    }


def _reference_image_preflight_summary(
    payload: dict[str, Any],
    *,
    readiness: dict[str, Any],
    asset_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    reference_readiness = readiness.get("reference_images") if isinstance(readiness.get("reference_images"), dict) else {}
    fetchable = [_reference_fetchable_url(row) for row in asset_rows]
    probe = _reference_url_probe_summary(payload, fetchable)
    supports_reference = bool(reference_readiness.get("supports_reference_image"))
    provider_requires_public_urls = bool(reference_readiness.get("provider_requires_public_urls"))
    oss_configured = bool(reference_readiness.get("oss_configured"))
    can_send = supports_reference and bool(asset_rows)
    if can_send and provider_requires_public_urls:
        can_send = oss_configured or all(bool(value) for value in fetchable)
    if can_send and probe["enabled"]:
        can_send = bool(probe["passed"])
    return {
        "required": bool(payload.get("require_image_references")),
        "generation_check_required": bool(payload.get("require_reference_image_generation_check")),
        "supports_reference_image": supports_reference,
        "provider_requires_public_urls": provider_requires_public_urls,
        "oss_configured": oss_configured,
        "backend_public_base_url": _backend_public_base_url(str(payload.get("backend_public_base_url") or "")),
        "selected_count": len(asset_rows),
        "provider_fetchable_count": sum(1 for value in fetchable if value),
        "can_send_selected_references": can_send,
        "strict_reference_mode_ready": can_send if bool(payload.get("require_image_references")) else bool(
            reference_readiness.get("strict_reference_mode_ready")
        ),
        "url_probe": probe,
        "missing_oss_env": list(reference_readiness.get("missing_oss_env") or []),
    }


def _reference_fetchable_url(row: dict[str, Any]) -> str:
    public_url = str(row.get("public_reference_url") or "").strip()
    path = str(row.get("path") or "").strip()
    fetchable = provider_fetchable_reference_url(public_url)
    if fetchable:
        return fetchable
    return provider_fetchable_reference_url(path)


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
