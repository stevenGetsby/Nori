"""Content-production run orchestration service."""
from __future__ import annotations

import json
from typing import Any

from nori.sessions import SessionEvent

from ..contracts import ApiError, ContentProductionReplayRequest, ContentProductionRunRequest
from ..experiments import (
    ContentProductionRunFailed,
    experiment_readiness,
    get_content_production_case_selected_run,
    resolve_content_production_artifact_path,
)
from ..job_presenters import enrich_content_run_result
from ..jobs import InProcessExperimentJobStore
from .content_production_run_preparation import ContentProductionRunPreparer
from .content_production_preflight_actions import (
    _content_production_preflight_actions,
    _content_production_preflight_links,
)
from .content_production_preflight_checks import (
    _content_production_preflight_checks,
)
from .content_production_preflight_summaries import (
    _asset_preflight_summary,
    _market_evidence_preflight_summary,
    _reference_image_preflight_summary,
)
from .content_production_run_payloads import _model_data, _replay_payload_with_overrides
from .content_production_run_templates import ContentProductionRunTemplateBuilder
from .session_assets import (
    latest_reference_image_generation_check as _latest_reference_image_generation_check,
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
        self.run_preparer = ContentProductionRunPreparer(
            experiment_runner=experiment_runner,
            session_store=session_store,
            enforce_model_readiness=self.enforce_model_readiness,
            readiness_provider=self.experiment_readiness,
        )
        self.template_builder = ContentProductionRunTemplateBuilder(
            experiment_runner=experiment_runner,
            session_store=session_store,
            enforce_model_readiness=self.enforce_model_readiness,
            readiness_provider=self.experiment_readiness,
        )

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
        return self.template_builder.build(
            session_id=session_id,
            task_id=task_id,
            case_id=case_id,
            case_title=case_title,
            platform=platform,
            goal=goal,
            brief_text=brief_text,
            asset_ids=asset_ids,
            asset_paths=asset_paths,
            backend_public_base_url=backend_public_base_url,
            execution_mode=execution_mode,
            human_gate_mode=human_gate_mode,
            require_image_references=require_image_references,
            require_reference_image_generation_check=require_reference_image_generation_check,
            verify_reference_urls=verify_reference_urls,
            reference_url_probe_timeout=reference_url_probe_timeout,
            market_evidence=market_evidence,
            config=config,
            request_metadata=request_metadata,
        )

    def run_content_production(self, request: ContentProductionRunRequest) -> dict[str, Any]:
        payload = _model_data(request)
        prepared = self.run_preparer.prepare(payload, create_task=True, enforce_strict_references=True)
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
        prepared = self.run_preparer.prepare(payload, create_task=False, enforce_strict_references=False)
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
