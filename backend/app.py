"""FastAPI product backend for Nori."""
from __future__ import annotations

import os
import json
import tempfile
from datetime import datetime, timezone
from typing import Any, Optional
from pathlib import Path

from fastapi import FastAPI, File, Form, Query, UploadFile
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse, Response
from starlette.exceptions import HTTPException as StarletteHTTPException

from nori.sessions import SessionEvent, SessionManager
from nori.core import llms
from nori.storage import ObjectStoreError, ReferenceImagePublisher

from .assets import append_session_assets, parse_metadata_json, save_uploaded_asset, select_assets
from .contracts import (
    ApiError,
    AssetReferencePublishRequest,
    ContentProductionReplayRequest,
    ContentProductionRunRequest,
    ContentProductionRunTemplateRequest,
    ContentProductionEvaluationDraftRequest,
    ContentProductionEvaluationRequest,
    ContentProductionPromotionRequest,
    ContentProductionSelectionRequest,
    ContentGenerationPlanRequest,
    ExperimentJobCancelRequest,
    ReferenceImageGenerationCheckRequest,
    ReferencePublishCheckRequest,
    SessionCreateRequest,
    SessionReferenceImageGenerationCheckRequest,
    TaskCreateRequest,
    TurnCreateRequest,
    WorkflowResolveRequest,
    api_error,
    api_ok,
)
from .content import ContentGenerationCatalog
from .experiments import (
    ContentProductionExperimentRunner,
    ContentProductionRunFailed,
    PROJECT_ROOT,
    build_content_production_case_delivery_export,
    build_content_production_case_export,
    build_content_production_evaluation_draft,
    build_content_production_run_export,
    compare_content_production_runs,
    content_production_case_compare,
    content_production_case_delivery,
    content_production_case_next_actions,
    content_production_case_timeline,
    content_production_diagnostics,
    content_production_experiment_overview,
    content_production_experiment_report,
    content_production_experiment_workbench,
    experiment_readiness,
    get_content_production_case_selection,
    get_content_production_case_selected_run,
    get_content_production_run_acceptance,
    inspect_content_production_run_artifacts,
    list_content_production_cases,
    list_content_production_run_evaluations,
    list_content_production_runs,
    promote_content_production_case_run,
    record_content_production_case_selection,
    record_content_production_run_evaluation,
    resolve_content_production_artifact_path,
    summarize_content_production_run,
)
from .jobs import InProcessExperimentJobStore, enrich_content_run_result
from .reference_urls import probe_reference_url, provider_fetchable_reference_url
from .workflows import WorkflowCatalog


class NoriBackend:
    """Service layer behind FastAPI routes."""

    def __init__(
        self,
        *,
        session_manager: SessionManager | None = None,
        workflow_catalog: WorkflowCatalog | None = None,
        content_catalog: ContentGenerationCatalog | None = None,
        experiment_runner: ContentProductionExperimentRunner | None = None,
        job_store: InProcessExperimentJobStore | None = None,
        reference_publisher: Any | None = None,
        upload_root: str | Path | None = None,
        enforce_model_readiness: bool | None = None,
    ) -> None:
        self.workflow_catalog = workflow_catalog or WorkflowCatalog()
        self.content_catalog = content_catalog or ContentGenerationCatalog()
        self.experiment_runner = experiment_runner or ContentProductionExperimentRunner()
        self.enforce_model_readiness = (
            isinstance(self.experiment_runner, ContentProductionExperimentRunner)
            if enforce_model_readiness is None
            else bool(enforce_model_readiness)
        )
        project_root = _experiment_project_root(self.experiment_runner)
        self.session_manager = session_manager or SessionManager(storage_root=project_root / "data" / "backend" / "sessions")
        self.reference_publisher = reference_publisher or ReferenceImagePublisher.from_env()
        self.job_store = job_store or InProcessExperimentJobStore(
            storage_root=project_root / "data" / "backend" / "jobs"
        )
        self.upload_root = Path(upload_root or PROJECT_ROOT / "data" / "backend" / "uploads")
        self._sync_interrupted_experiment_jobs()

    def health(self) -> dict[str, Any]:
        return {
            "status": "ok",
            "service": "nori-backend",
            "runtime": "fastapi",
        }

    def list_workflows(self) -> dict[str, Any]:
        return {"workflows": self.workflow_catalog.list_workflows()}

    def get_workflow(self, workflow_id: str) -> dict[str, Any]:
        workflow = self.workflow_catalog.get_workflow(workflow_id)
        if workflow is None:
            raise ApiError(f"workflow not found: {workflow_id}", status_code=404)
        return workflow

    def resolve_workflow(self, request: WorkflowResolveRequest) -> dict[str, Any]:
        return self.workflow_catalog.resolve(_model_data(request))

    def list_capabilities(self) -> dict[str, Any]:
        return {
            "capabilities": [
                {
                    "capability_id": "content_generation",
                    "label": "Content Generation",
                    "description": "Product-facing content generation controls, direct actions, and workflow entrypoints.",
                    "routes": {
                        "options": "/content/generation/options",
                        "actions": "/content/generation/actions",
                        "plan": "/content/generation/plan",
                        "readiness": "/experiments/readiness",
                        "upload_assets": "/sessions/{session_id}/assets",
                        "asset_file": "/sessions/{session_id}/assets/{asset_id}/file",
                        "publish_asset_references": "/sessions/{session_id}/assets/publish-references",
                        "session_reference_image_generation_check": "/sessions/{session_id}/assets/reference-image-generation-check",
                        "reference_publish_check": "/experiments/content-production/reference-publish-check",
                        "reference_image_generation_check": "/experiments/content-production/reference-image-generation-check",
                        "experiment_diagnostics": "/experiments/content-production/diagnostics",
                        "experiment_workbench": "/experiments/content-production/workbench",
                        "experiment_overview": "/experiments/content-production/overview",
                        "experiment_report": "/experiments/content-production/report",
                        "run_template": "/experiments/content-production/run-template",
                        "experiment_cases": "/experiments/content-production/cases",
                        "case_selection": "/experiments/content-production/cases/{case_id}/selection",
                        "case_selected_run": "/experiments/content-production/cases/{case_id}/selected-run",
                        "case_compare": "/experiments/content-production/cases/{case_id}/compare",
                        "case_next_actions": "/experiments/content-production/cases/{case_id}/next-actions",
                        "case_promotion": "/experiments/content-production/cases/{case_id}/promotion",
                        "case_replay": "/experiments/content-production/cases/{case_id}/replay",
                        "case_evaluation_draft": "/experiments/content-production/cases/{case_id}/evaluations/draft",
                        "case_evaluations": "/experiments/content-production/cases/{case_id}/evaluations",
                        "case_delivery": "/experiments/content-production/cases/{case_id}/delivery",
                        "case_delivery_export": "/experiments/content-production/cases/{case_id}/delivery/export",
                        "case_timeline": "/experiments/content-production/cases/{case_id}/timeline",
                        "case_export": "/experiments/content-production/cases/{case_id}/export",
                        "run_workflow": "/workflows/content-production/runs",
                        "preflight_run": "/workflows/content-production/runs/preflight",
                        "compare_runs": "/workflows/content-production/runs/compare",
                        "run_acceptance": "/workflows/content-production/runs/{case_id}/{run_id}/acceptance",
                        "run_evaluations": "/workflows/content-production/runs/{case_id}/{run_id}/evaluations",
                        "run_evaluation_draft": "/workflows/content-production/runs/{case_id}/{run_id}/evaluations/draft",
                        "replay_run": "/workflows/content-production/runs/{case_id}/{run_id}/replay",
                        "export_run": "/workflows/content-production/runs/{case_id}/{run_id}/export",
                        "inspect_run_artifacts": "/workflows/content-production/runs/{case_id}/{run_id}/artifacts/inspect",
                        "list_jobs": "/experiments/jobs",
                        "job_status": "/experiments/jobs/{job_id}",
                        "cancel_job": "/experiments/jobs/{job_id}/cancel",
                    },
                },
                {
                    "capability_id": "workflow_orchestration",
                    "label": "Workflow Orchestration",
                    "description": "End-to-end workflow catalog and resolver.",
                    "routes": {
                        "catalog": "/workflows",
                        "resolve": "/workflows/resolve",
                    },
                },
            ]
        }

    def content_options(self) -> dict[str, Any]:
        return {"option_groups": self.content_catalog.option_groups()}

    def content_option_group(self, group_id: str) -> dict[str, Any]:
        group = self.content_catalog.option_group(group_id)
        if group is None:
            raise ApiError(f"content option group not found: {group_id}", status_code=404)
        return {"group_id": group_id, "options": group}

    def content_actions(self) -> dict[str, Any]:
        return {"actions": self.content_catalog.actions()}

    def content_action(self, action_id: str) -> dict[str, Any]:
        action = self.content_catalog.action(action_id)
        if action is None:
            raise ApiError(f"content action not found: {action_id}", status_code=404)
        return action

    def plan_content_generation(self, request: ContentGenerationPlanRequest) -> dict[str, Any]:
        return self.content_catalog.plan(_model_data(request))

    def experiment_readiness(self) -> dict[str, Any]:
        return experiment_readiness(project_root=self.experiment_runner.project_root)

    def content_production_diagnostics(self) -> dict[str, Any]:
        data = content_production_diagnostics(project_root=self.experiment_runner.project_root)
        data["routes"]["reference_publish_check"] = "/experiments/content-production/reference-publish-check"
        data["routes"]["reference_image_generation_check"] = (
            "/experiments/content-production/reference-image-generation-check"
        )
        data["routes"]["session_reference_image_generation_check"] = (
            "/sessions/{session_id}/assets/reference-image-generation-check"
        )
        return data

    def content_production_experiment_workbench(
        self,
        *,
        case_id: str = "",
        limit: int = 20,
        include_diagnostics: bool = True,
    ) -> dict[str, Any]:
        return content_production_experiment_workbench(
            project_root=self.experiment_runner.project_root,
            case_id=case_id,
            limit=limit,
            include_diagnostics=include_diagnostics,
        )

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
        url_probe = _reference_url_probe_summary(
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
            or os.environ.get("NORI_BACKEND_PUBLIC_BASE_URL", "")
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

    def list_session_assets(self, session_id: str) -> dict[str, Any]:
        session = self.session_manager.get_session(session_id)
        if session is None:
            raise ApiError(f"session not found: {session_id}", status_code=404)
        return {
            "assets": [_asset_with_url(session_id, row) for row in session.metadata.get("assets", [])],
            "latest_reference_image_generation_check": _latest_reference_image_generation_check(session.events),
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
        if _is_remote_url(str(path)):
            raise ApiError(f"asset is remote and has no local file: {asset_id}", status_code=400)
        if not path.is_file():
            raise ApiError(f"asset file not found: {asset_id}", status_code=404)
        return path

    def publish_session_asset_references(self, session_id: str, request: AssetReferencePublishRequest) -> dict[str, Any]:
        session = self.session_manager.get_session(session_id)
        if session is None:
            raise ApiError(f"session not found: {session_id}", status_code=404)
        try:
            selected_assets = select_assets(session.metadata.get("assets", []), asset_ids=list(request.asset_ids or []))
            _assert_asset_paths_exist(selected_assets)
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
        if _is_remote_url(path):
            updated = {**row, "public_reference_url": path}
            return updated, _asset_publish_result(updated, public_reference_url=path, reason="remote")
        backend_asset_url = _backend_asset_public_reference_url(
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

    def get_experiment_job(self, job_id: str) -> dict[str, Any]:
        job = self.job_store.get(job_id)
        if job is None:
            raise ApiError(f"experiment job not found: {job_id}", status_code=404)
        return {"job": job}

    def cancel_experiment_job(self, job_id: str, request: ExperimentJobCancelRequest) -> dict[str, Any]:
        job = self.job_store.cancel(job_id, reason=str(request.reason or ""))
        if job is None:
            raise ApiError(f"experiment job not found: {job_id}", status_code=404)
        return {"job": job, "session": self._sync_cancelled_experiment_job(job)}

    def _sync_cancelled_experiment_job(self, job: dict[str, Any]) -> dict[str, Any]:
        metadata = job.get("metadata") if isinstance(job.get("metadata"), dict) else {}
        session_id = str(metadata.get("session_id") or "").strip()
        task_id = str(metadata.get("task_id") or "").strip()
        if not session_id or not task_id:
            return {}
        session = self.session_manager.get_session(session_id)
        if session is None:
            return {"session_id": session_id, "task_id": task_id, "task_found": False}
        task = next((item for item in session.task_goals if item.task_id == task_id), None)
        if task is None:
            return {"session_id": session_id, "task_id": task_id, "task_found": False}

        job_status = str(job.get("status") or "")
        if job_status == "cancelled":
            task_status = "cancelled"
            event_type = "workflow_run_cancelled"
        elif job_status == "cancelling":
            task_status = "cancelling"
            event_type = "workflow_run_cancel_requested"
        else:
            return {
                "session_id": session_id,
                "task_id": task_id,
                "task_found": True,
                "task_status": task.status,
                "event_type": "",
            }

        if task.status not in {"succeeded", "failed", "cancelled"}:
            task.status = task_status
        if not _session_has_job_event(session.events, event_type=event_type, job_id=str(job.get("job_id") or "")):
            cancel_request = metadata.get("cancel_request") if isinstance(metadata.get("cancel_request"), dict) else {}
            session.events.append(
                SessionEvent(
                    event_type=event_type,
                    payload={
                        "job_id": str(job.get("job_id") or ""),
                        "job_status": job_status,
                        "task_id": task_id,
                        "reason": str(cancel_request.get("reason") or ""),
                    },
                )
            )
        session.updated_at = _utc_now_iso()
        self.session_manager.save_session(session_id)
        return {
            "session_id": session_id,
            "task_id": task_id,
            "task_found": True,
            "task_status": task.status,
            "event_type": event_type,
        }

    def list_experiment_jobs(
        self,
        *,
        status: str = "",
        session_id: str = "",
        case_id: str = "",
        job_type: str = "",
    ) -> dict[str, Any]:
        return {
            "jobs": self.job_store.list_jobs(
                status=status,
                session_id=session_id,
                case_id=case_id,
                job_type=job_type,
            )
        }

    def _sync_interrupted_experiment_jobs(self) -> None:
        for job in self.job_store.list_jobs(status="interrupted"):
            metadata = job.get("metadata") if isinstance(job.get("metadata"), dict) else {}
            session_id = str(metadata.get("session_id") or "").strip()
            task_id = str(metadata.get("task_id") or "").strip()
            if not session_id or not task_id:
                continue
            session = self.session_manager.get_session(session_id)
            if session is None:
                continue
            task = next((item for item in session.task_goals if item.task_id == task_id), None)
            if task is None:
                continue
            if task.status not in {"succeeded", "failed", "cancelled", "interrupted"}:
                task.status = "interrupted"
            if not _session_has_job_event(
                session.events,
                event_type="workflow_run_interrupted",
                job_id=str(job.get("job_id") or ""),
            ):
                session.events.append(
                    SessionEvent(
                        event_type="workflow_run_interrupted",
                        payload={
                            "job_id": str(job.get("job_id") or ""),
                            "job_status": "interrupted",
                            "task_id": task_id,
                            "error": dict(job.get("error") or {}) if isinstance(job.get("error"), dict) else {},
                        },
                    )
                )
            session.updated_at = _utc_now_iso()
            self.session_manager.save_session(session_id)

    def content_production_experiment_overview(self, *, case_id: str = "", limit: int = 20) -> dict[str, Any]:
        return content_production_experiment_overview(
            project_root=self.experiment_runner.project_root,
            case_id=case_id,
            limit=limit,
        )

    def content_production_experiment_report(self, *, case_id: str = "", limit: int = 50) -> dict[str, Any]:
        return content_production_experiment_report(
            project_root=self.experiment_runner.project_root,
            case_id=case_id,
            limit=limit,
        )

    def list_content_production_cases(self) -> dict[str, Any]:
        return list_content_production_cases(project_root=self.experiment_runner.project_root)

    def get_content_production_case_selection(self, case_id: str) -> dict[str, Any]:
        try:
            return get_content_production_case_selection(
                project_root=self.experiment_runner.project_root,
                case_id=case_id,
            )
        except FileNotFoundError as exc:
            raise ApiError(str(exc), status_code=404) from exc
        except ValueError as exc:
            raise ApiError(str(exc), status_code=400) from exc

    def record_content_production_case_selection(
        self,
        case_id: str,
        request: ContentProductionSelectionRequest,
    ) -> dict[str, Any]:
        try:
            return record_content_production_case_selection(
                project_root=self.experiment_runner.project_root,
                case_id=case_id,
                selection=_model_data(request),
            )
        except FileNotFoundError as exc:
            raise ApiError(str(exc), status_code=404) from exc
        except ValueError as exc:
            raise ApiError(str(exc), status_code=400) from exc

    def promote_content_production_case_run(
        self,
        case_id: str,
        request: ContentProductionPromotionRequest,
    ) -> dict[str, Any]:
        try:
            return promote_content_production_case_run(
                project_root=self.experiment_runner.project_root,
                case_id=case_id,
                promotion=_model_data(request),
            )
        except FileNotFoundError as exc:
            raise ApiError(str(exc), status_code=404) from exc
        except ValueError as exc:
            raise ApiError(str(exc), status_code=400) from exc

    def get_content_production_case_selected_run(
        self,
        *,
        case_id: str,
        fallback_to_best: bool = True,
    ) -> dict[str, Any]:
        try:
            return get_content_production_case_selected_run(
                project_root=self.experiment_runner.project_root,
                case_id=case_id,
                fallback_to_best=fallback_to_best,
            )
        except FileNotFoundError as exc:
            raise ApiError(str(exc), status_code=404) from exc
        except ValueError as exc:
            raise ApiError(str(exc), status_code=400) from exc

    def content_production_case_compare(self, *, case_id: str, limit: int = 500) -> dict[str, Any]:
        try:
            return content_production_case_compare(
                project_root=self.experiment_runner.project_root,
                case_id=case_id,
                limit=limit,
            )
        except FileNotFoundError as exc:
            raise ApiError(str(exc), status_code=404) from exc
        except ValueError as exc:
            raise ApiError(str(exc), status_code=400) from exc

    def content_production_case_next_actions(self, *, case_id: str, limit: int = 500) -> dict[str, Any]:
        try:
            return content_production_case_next_actions(
                project_root=self.experiment_runner.project_root,
                case_id=case_id,
                limit=limit,
            )
        except FileNotFoundError as exc:
            raise ApiError(str(exc), status_code=404) from exc
        except ValueError as exc:
            raise ApiError(str(exc), status_code=400) from exc

    def content_production_case_delivery(self, *, case_id: str, allow_unpromoted: bool = False) -> dict[str, Any]:
        try:
            return content_production_case_delivery(
                project_root=self.experiment_runner.project_root,
                case_id=case_id,
                allow_unpromoted=allow_unpromoted,
            )
        except FileNotFoundError as exc:
            raise ApiError(str(exc), status_code=404) from exc
        except ValueError as exc:
            raise ApiError(str(exc), status_code=400) from exc

    def content_production_case_timeline(self, *, case_id: str, limit: int = 200) -> dict[str, Any]:
        try:
            return content_production_case_timeline(
                project_root=self.experiment_runner.project_root,
                case_id=case_id,
                limit=limit,
            )
        except FileNotFoundError as exc:
            raise ApiError(str(exc), status_code=404) from exc
        except ValueError as exc:
            raise ApiError(str(exc), status_code=400) from exc

    def get_content_production_case_export(self, case_id: str) -> dict[str, Any]:
        try:
            return build_content_production_case_export(
                project_root=self.experiment_runner.project_root,
                case_id=case_id,
            )
        except FileNotFoundError as exc:
            raise ApiError(str(exc), status_code=404) from exc
        except ValueError as exc:
            raise ApiError(str(exc), status_code=400) from exc

    def get_content_production_case_delivery_export(self, case_id: str, *, allow_unready: bool = False) -> dict[str, Any]:
        try:
            return build_content_production_case_delivery_export(
                project_root=self.experiment_runner.project_root,
                case_id=case_id,
                allow_unready=allow_unready,
            )
        except FileNotFoundError as exc:
            raise ApiError(str(exc), status_code=404) from exc
        except ValueError as exc:
            raise ApiError(str(exc), status_code=400) from exc

    def list_content_production_runs(
        self,
        *,
        case_id: str = "",
        status: str = "",
        proof_status: str = "",
        reference_status: str = "",
        evaluation_status: str = "",
        search: str = "",
        limit: int = 100,
        offset: int = 0,
    ) -> dict[str, Any]:
        return list_content_production_runs(
            project_root=self.experiment_runner.project_root,
            case_id=case_id,
            status=status,
            proof_status=proof_status,
            reference_status=reference_status,
            evaluation_status=evaluation_status,
            search=search,
            limit=limit,
            offset=offset,
        )

    def compare_content_production_runs(self, *, case_id: str, run_ids: list[str]) -> dict[str, Any]:
        try:
            return compare_content_production_runs(
                project_root=self.experiment_runner.project_root,
                case_id=case_id,
                run_ids=run_ids,
            )
        except FileNotFoundError as exc:
            raise ApiError(str(exc), status_code=404) from exc
        except ValueError as exc:
            raise ApiError(str(exc), status_code=400) from exc

    def list_content_production_run_evaluations(self, case_id: str, run_id: str) -> dict[str, Any]:
        try:
            return list_content_production_run_evaluations(
                project_root=self.experiment_runner.project_root,
                case_id=case_id,
                run_id=run_id,
            )
        except FileNotFoundError as exc:
            raise ApiError(str(exc), status_code=404) from exc

    def get_content_production_run_acceptance(self, case_id: str, run_id: str) -> dict[str, Any]:
        try:
            return get_content_production_run_acceptance(
                project_root=self.experiment_runner.project_root,
                case_id=case_id,
                run_id=run_id,
            )
        except FileNotFoundError as exc:
            raise ApiError(str(exc), status_code=404) from exc

    def inspect_content_production_run_artifacts(self, case_id: str, run_id: str) -> dict[str, Any]:
        try:
            return inspect_content_production_run_artifacts(
                project_root=self.experiment_runner.project_root,
                case_id=case_id,
                run_id=run_id,
            )
        except FileNotFoundError as exc:
            raise ApiError(str(exc), status_code=404) from exc
        except ValueError as exc:
            raise ApiError(str(exc), status_code=400) from exc

    def build_content_production_evaluation_draft(
        self,
        case_id: str,
        run_id: str,
        request: ContentProductionEvaluationDraftRequest,
    ) -> dict[str, Any]:
        try:
            return build_content_production_evaluation_draft(
                project_root=self.experiment_runner.project_root,
                case_id=case_id,
                run_id=run_id,
                reviewer=request.reviewer,
                persist=request.persist,
                metadata=dict(request.metadata),
            )
        except FileNotFoundError as exc:
            raise ApiError(str(exc), status_code=404) from exc
        except ValueError as exc:
            raise ApiError(str(exc), status_code=400) from exc

    def build_content_production_case_evaluation_draft(
        self,
        case_id: str,
        request: ContentProductionEvaluationDraftRequest,
    ) -> dict[str, Any]:
        run_id, source = self._resolve_content_production_case_run_id(case_id, run_id=request.run_id)
        data = self.build_content_production_evaluation_draft(case_id, run_id, request)
        data.setdefault("source", "case_evaluation_draft")
        data.setdefault("source_case_id", case_id)
        data.setdefault("source_run_id", run_id)
        data.setdefault("source_run_selector", source)
        return data

    def record_content_production_run_evaluation(
        self,
        case_id: str,
        run_id: str,
        request: ContentProductionEvaluationRequest,
    ) -> dict[str, Any]:
        try:
            return record_content_production_run_evaluation(
                project_root=self.experiment_runner.project_root,
                case_id=case_id,
                run_id=run_id,
                evaluation=_model_data(request),
            )
        except FileNotFoundError as exc:
            raise ApiError(str(exc), status_code=404) from exc
        except ValueError as exc:
            raise ApiError(str(exc), status_code=400) from exc

    def record_content_production_case_evaluation(
        self,
        case_id: str,
        request: ContentProductionEvaluationRequest,
    ) -> dict[str, Any]:
        run_id, source = self._resolve_content_production_case_run_id(case_id, run_id=request.run_id)
        data = self.record_content_production_run_evaluation(case_id, run_id, request)
        data.setdefault("source", "case_evaluation")
        data.setdefault("source_case_id", case_id)
        data.setdefault("source_run_id", run_id)
        data.setdefault("source_run_selector", source)
        return data

    def _resolve_content_production_case_run_id(self, case_id: str, *, run_id: str = "") -> tuple[str, str]:
        explicit_run_id = str(run_id or "").strip()
        if explicit_run_id:
            summary = summarize_content_production_run(
                project_root=self.experiment_runner.project_root,
                case_id=case_id,
                run_id=explicit_run_id,
            )
            if not summary:
                raise ApiError(f"content-production run not found: {case_id}/{explicit_run_id}", status_code=404)
            return explicit_run_id, "request"
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
        resolved_run_id = str(selected.get("run_id") or "")
        if not resolved_run_id:
            raise ApiError(f"no target run found for case: {case_id}", status_code=404)
        return resolved_run_id, str(selected.get("source") or "")

    def get_content_production_run(self, case_id: str, run_id: str) -> dict[str, Any]:
        result = summarize_content_production_run(
            project_root=self.experiment_runner.project_root,
            case_id=case_id,
            run_id=run_id,
        )
        if not result:
            raise ApiError(f"content-production run not found: {case_id}/{run_id}", status_code=404)
        return result

    def get_content_production_artifact_file(self, case_id: str, run_id: str, artifact_name: str) -> Path:
        try:
            return resolve_content_production_artifact_path(
                project_root=self.experiment_runner.project_root,
                case_id=case_id,
                run_id=run_id,
                artifact_name=artifact_name,
            )
        except FileNotFoundError as exc:
            raise ApiError(str(exc), status_code=404) from exc
        except ValueError as exc:
            raise ApiError(str(exc), status_code=400) from exc

    def get_content_production_run_export(self, case_id: str, run_id: str, *, include_inputs: bool = False) -> dict[str, Any]:
        try:
            return build_content_production_run_export(
                project_root=self.experiment_runner.project_root,
                case_id=case_id,
                run_id=run_id,
                include_inputs=include_inputs,
            )
        except FileNotFoundError as exc:
            raise ApiError(str(exc), status_code=404) from exc

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
        data["latest_reference_image_generation_check"] = _latest_reference_image_generation_check(session.events)
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


def _experiment_project_root(experiment_runner: Any) -> Path:
    return Path(getattr(experiment_runner, "project_root", PROJECT_ROOT))


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _session_has_job_event(events: list[SessionEvent], *, event_type: str, job_id: str) -> bool:
    return any(
        event.event_type == event_type and str((event.payload or {}).get("job_id") or "") == job_id
        for event in events
    )


def create_app(*, backend: NoriBackend | None = None) -> FastAPI:
    """Create the FastAPI application."""

    service = backend or NoriBackend()
    app = FastAPI(
        title="Nori Backend API",
        version="0.1.0",
        description="Product-service adapter for sessions and workflow catalog. Agent logic stays in nori/.",
    )
    app.state.backend = service

    @app.exception_handler(ApiError)
    async def api_error_handler(_request: Any, exc: ApiError) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content=api_error(exc.message, status_code=exc.status_code, data=exc.data))

    @app.exception_handler(StarletteHTTPException)
    async def http_error_handler(_request: Any, exc: StarletteHTTPException) -> JSONResponse:
        message = str(exc.detail)
        return JSONResponse(status_code=exc.status_code, content=api_error(message, status_code=exc.status_code))

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(_request: Any, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content=api_error("request validation failed", status_code=422, data={"errors": exc.errors()}),
        )

    @app.get("/health", summary="Service health")
    def health() -> dict[str, Any]:
        return api_ok(service.health())

    @app.get("/workflows", summary="List workflow catalog entries")
    def list_workflows() -> dict[str, Any]:
        return api_ok(service.list_workflows())

    @app.post("/workflows/resolve", summary="Resolve a workflow or direct action for a product request")
    def resolve_workflow(request: WorkflowResolveRequest) -> dict[str, Any]:
        return api_ok(service.resolve_workflow(request))

    @app.get("/workflows/{workflow_id}", summary="Inspect one workflow catalog entry")
    def get_workflow(workflow_id: str) -> dict[str, Any]:
        return api_ok(service.get_workflow(workflow_id))

    @app.get("/capabilities", summary="List product capability groups")
    def list_capabilities() -> dict[str, Any]:
        return api_ok(service.list_capabilities())

    @app.get("/experiments/readiness", summary="Inspect backend experiment readiness")
    def get_experiment_readiness() -> dict[str, Any]:
        return api_ok(service.experiment_readiness())

    @app.get("/experiments/content-production/diagnostics", summary="Diagnose content-production backend experiment readiness")
    def get_content_production_diagnostics() -> dict[str, Any]:
        return api_ok(service.content_production_diagnostics())

    @app.post(
        "/experiments/content-production/reference-publish-check",
        summary="Verify reference-image publishing with a backend-owned test image",
    )
    def check_reference_publish(request: ReferencePublishCheckRequest) -> dict[str, Any]:
        return api_ok(service.check_reference_publish(request))

    @app.post(
        "/experiments/content-production/reference-image-generation-check",
        summary="Verify reference-image generation with the active image model",
    )
    def check_reference_image_generation(request: ReferenceImageGenerationCheckRequest) -> dict[str, Any]:
        return api_ok(service.check_reference_image_generation(request))

    @app.post(
        "/sessions/{session_id}/assets/reference-image-generation-check",
        summary="Publish session image assets and verify active image-model reference support",
    )
    def check_session_reference_image_generation(
        session_id: str,
        request: SessionReferenceImageGenerationCheckRequest,
    ) -> dict[str, Any]:
        return api_ok(service.check_session_reference_image_generation(session_id, request))

    @app.get("/experiments/content-production/run-template", summary="Build a content-production run request template")
    def get_content_production_run_template(
        session_id: str = "",
        task_id: str = "",
        case_id: str = "",
        goal: str = "",
        brief_text: str = "",
        asset_ids: list[str] = Query(default=[]),
        backend_public_base_url: str = "",
        execution_mode: str = "sync",
        human_gate_mode: str = "skip",
        require_image_references: bool = False,
        require_reference_image_generation_check: bool = False,
        verify_reference_urls: bool = False,
        reference_url_probe_timeout: float = 3.0,
    ) -> dict[str, Any]:
        return api_ok(
            service.content_production_run_template(
                session_id=session_id,
                task_id=task_id,
                case_id=case_id,
                goal=goal,
                brief_text=brief_text,
                asset_ids=asset_ids,
                backend_public_base_url=backend_public_base_url,
                execution_mode=execution_mode,
                human_gate_mode=human_gate_mode,
                require_image_references=require_image_references,
                require_reference_image_generation_check=require_reference_image_generation_check,
                verify_reference_urls=verify_reference_urls,
                reference_url_probe_timeout=reference_url_probe_timeout,
            )
        )

    @app.post("/experiments/content-production/run-template", summary="Build a content-production run request template from a form draft")
    def post_content_production_run_template(request: ContentProductionRunTemplateRequest) -> dict[str, Any]:
        data = _model_data(request)
        return api_ok(
            service.content_production_run_template(
                session_id=str(data.get("session_id") or ""),
                task_id=str(data.get("task_id") or ""),
                case_id=str(data.get("case_id") or ""),
                case_title=str(data.get("case_title") or ""),
                platform=str(data.get("platform") or "xhs"),
                goal=str(data.get("goal") or ""),
                brief_text=str(data.get("brief_text") or ""),
                asset_ids=list(data.get("asset_ids") or []),
                asset_paths=list(data.get("asset_paths") or []),
                backend_public_base_url=str(data.get("backend_public_base_url") or ""),
                execution_mode=str(data.get("execution_mode") or "sync"),
                human_gate_mode=str(data.get("human_gate_mode") or "skip"),
                require_image_references=bool(data.get("require_image_references")),
                require_reference_image_generation_check=bool(data.get("require_reference_image_generation_check")),
                verify_reference_urls=bool(data.get("verify_reference_urls")),
                reference_url_probe_timeout=float(data.get("reference_url_probe_timeout") or 3.0),
                market_evidence=dict(data.get("market_evidence") or {}),
                config=dict(data.get("config") or {}),
                request_metadata=dict(data.get("metadata") or {}),
            )
        )

    @app.get("/experiments/jobs", summary="List background experiment jobs")
    def list_experiment_jobs(
        status: str = "",
        session_id: str = "",
        case_id: str = "",
        job_type: str = "",
    ) -> dict[str, Any]:
        return api_ok(
            service.list_experiment_jobs(
                status=status,
                session_id=session_id,
                case_id=case_id,
                job_type=job_type,
            )
        )

    @app.get("/content/generation/options", summary="List content generation option groups")
    def content_options() -> dict[str, Any]:
        return api_ok(service.content_options())

    @app.get("/content/generation/options/{group_id}", summary="Inspect one content generation option group")
    def content_option_group(group_id: str) -> dict[str, Any]:
        return api_ok(service.content_option_group(group_id))

    @app.get("/content/generation/actions", summary="List content generation sub-capabilities")
    def content_actions() -> dict[str, Any]:
        return api_ok(service.content_actions())

    @app.get("/content/generation/actions/{action_id}", summary="Inspect one content generation action")
    def content_action(action_id: str) -> dict[str, Any]:
        return api_ok(service.content_action(action_id))

    @app.post("/content/generation/plan", summary="Plan a content generation entrypoint")
    def plan_content_generation(request: ContentGenerationPlanRequest) -> dict[str, Any]:
        return api_ok(service.plan_content_generation(request))

    @app.get("/sessions/{session_id}/assets", summary="List uploaded assets for one session")
    def list_session_assets(session_id: str) -> dict[str, Any]:
        return api_ok(service.list_session_assets(session_id))

    @app.get("/sessions/{session_id}/assets/{asset_id}/file", summary="Download one uploaded session asset")
    def get_session_asset_file(session_id: str, asset_id: str) -> FileResponse:
        path = service.get_session_asset_file(session_id, asset_id)
        return FileResponse(path, filename=path.name)

    @app.post("/sessions/{session_id}/assets", status_code=201, summary="Upload image assets for a session")
    def upload_session_assets(
        session_id: str,
        files: list[UploadFile] = File(...),
        task_id: str = Form(""),
        usage: str = Form("reference"),
        metadata_json: str = Form(""),
    ) -> dict[str, Any]:
        return api_ok(
            service.upload_session_assets(
                session_id,
                files,
                task_id=task_id,
                usage=usage,
                metadata_json=metadata_json,
            )
        )

    @app.post("/sessions/{session_id}/assets/publish-references", summary="Publish session assets as model-fetchable references")
    def publish_session_asset_references(session_id: str, request: AssetReferencePublishRequest) -> dict[str, Any]:
        return api_ok(service.publish_session_asset_references(session_id, request))

    @app.post("/workflows/content-production/runs", status_code=201, summary="Run content-production with uploaded assets")
    def run_content_production(request: ContentProductionRunRequest) -> JSONResponse:
        data = service.run_content_production(request)
        status_code = 202 if data.get("job_id") else 201
        return JSONResponse(status_code=status_code, content=api_ok(data))

    @app.post("/workflows/content-production/runs/preflight", summary="Preflight a content-production experiment run")
    def preflight_content_production_run(request: ContentProductionRunRequest) -> dict[str, Any]:
        return api_ok(service.preflight_content_production_run(request))

    @app.get("/experiments/jobs/{job_id}", summary="Inspect one background experiment job")
    def get_experiment_job(job_id: str) -> dict[str, Any]:
        return api_ok(service.get_experiment_job(job_id))

    @app.post("/experiments/jobs/{job_id}/cancel", summary="Request cancellation for one background experiment job")
    def cancel_experiment_job(job_id: str, request: ExperimentJobCancelRequest) -> dict[str, Any]:
        return api_ok(service.cancel_experiment_job(job_id, request))

    @app.get("/experiments/content-production/overview", summary="Summarize content-production experiment health")
    def content_production_experiment_overview_route(case_id: str = "", limit: int = 20) -> dict[str, Any]:
        return api_ok(service.content_production_experiment_overview(case_id=case_id, limit=limit))

    @app.get("/experiments/content-production/workbench", summary="Build a content-production experiment workbench snapshot")
    def content_production_experiment_workbench_route(
        case_id: str = "",
        limit: int = 20,
        include_diagnostics: bool = True,
    ) -> dict[str, Any]:
        return api_ok(
            service.content_production_experiment_workbench(
                case_id=case_id,
                limit=limit,
                include_diagnostics=include_diagnostics,
            )
        )

    @app.get("/experiments/content-production/report", summary="Build a content-production experiment report")
    def content_production_experiment_report_route(case_id: str = "", limit: int = 50) -> dict[str, Any]:
        return api_ok(service.content_production_experiment_report(case_id=case_id, limit=limit))

    @app.get("/experiments/content-production/cases", summary="List content-production experiment cases")
    def list_content_production_cases_route() -> dict[str, Any]:
        return api_ok(service.list_content_production_cases())

    @app.get("/experiments/content-production/cases/{case_id}/selection", summary="Inspect a content-production case selection")
    def get_content_production_case_selection_route(case_id: str) -> dict[str, Any]:
        return api_ok(service.get_content_production_case_selection(case_id))

    @app.post("/experiments/content-production/cases/{case_id}/selection", status_code=201, summary="Record a content-production case selection")
    def record_content_production_case_selection_route(
        case_id: str,
        request: ContentProductionSelectionRequest,
    ) -> dict[str, Any]:
        return api_ok(service.record_content_production_case_selection(case_id, request))

    @app.post("/experiments/content-production/cases/{case_id}/promotion", status_code=201, summary="Promote an accepted content-production run")
    def promote_content_production_case_run_route(
        case_id: str,
        request: ContentProductionPromotionRequest,
    ) -> dict[str, Any]:
        return api_ok(service.promote_content_production_case_run(case_id, request))

    @app.post("/experiments/content-production/cases/{case_id}/replay", status_code=201, summary="Replay the selected or best run for a case")
    def replay_content_production_case_route(case_id: str, request: ContentProductionReplayRequest) -> JSONResponse:
        data = service.replay_content_production_case(case_id, request)
        status_code = 202 if data.get("job_id") else 201
        return JSONResponse(status_code=status_code, content=api_ok(data))

    @app.post("/experiments/content-production/cases/{case_id}/evaluations/draft", summary="Build an evaluation draft for a case target run")
    def build_content_production_case_evaluation_draft_route(
        case_id: str,
        request: ContentProductionEvaluationDraftRequest,
    ) -> dict[str, Any]:
        return api_ok(service.build_content_production_case_evaluation_draft(case_id, request))

    @app.post("/experiments/content-production/cases/{case_id}/evaluations", status_code=201, summary="Record an evaluation for a case target run")
    def record_content_production_case_evaluation_route(
        case_id: str,
        request: ContentProductionEvaluationRequest,
    ) -> dict[str, Any]:
        return api_ok(service.record_content_production_case_evaluation(case_id, request))

    @app.get("/experiments/content-production/cases/{case_id}/selected-run", summary="Resolve a content-production case selected run")
    def get_content_production_case_selected_run_route(
        case_id: str,
        fallback_to_best: bool = True,
    ) -> dict[str, Any]:
        return api_ok(service.get_content_production_case_selected_run(case_id=case_id, fallback_to_best=fallback_to_best))

    @app.get("/experiments/content-production/cases/{case_id}/compare", summary="Build a case-centered content-production comparison")
    def content_production_case_compare_route(case_id: str, limit: int = 500) -> dict[str, Any]:
        return api_ok(service.content_production_case_compare(case_id=case_id, limit=limit))

    @app.get("/experiments/content-production/cases/{case_id}/next-actions", summary="Plan next content-production case actions")
    def content_production_case_next_actions_route(case_id: str, limit: int = 500) -> dict[str, Any]:
        return api_ok(service.content_production_case_next_actions(case_id=case_id, limit=limit))

    @app.get("/experiments/content-production/cases/{case_id}/delivery", summary="Inspect case delivery readiness")
    def content_production_case_delivery_route(case_id: str, allow_unpromoted: bool = False) -> dict[str, Any]:
        return api_ok(service.content_production_case_delivery(case_id=case_id, allow_unpromoted=allow_unpromoted))

    @app.get("/experiments/content-production/cases/{case_id}/delivery/export", summary="Export one case delivery bundle")
    def export_content_production_case_delivery(case_id: str, allow_unready: bool = False) -> Response:
        data = service.get_content_production_case_delivery_export(case_id, allow_unready=allow_unready)
        return Response(
            content=data["content"],
            media_type=data["media_type"],
            headers={"Content-Disposition": f'attachment; filename="{data["filename"]}"'},
        )

    @app.get("/experiments/content-production/cases/{case_id}/timeline", summary="Inspect a content-production case timeline")
    def content_production_case_timeline_route(case_id: str, limit: int = 200) -> dict[str, Any]:
        return api_ok(service.content_production_case_timeline(case_id=case_id, limit=limit))

    @app.get("/experiments/content-production/cases/{case_id}/export", summary="Export one content-production case bundle")
    def export_content_production_case(case_id: str) -> Response:
        data = service.get_content_production_case_export(case_id)
        return Response(
            content=data["content"],
            media_type=data["media_type"],
            headers={"Content-Disposition": f'attachment; filename="{data["filename"]}"'},
        )

    @app.get("/workflows/content-production/runs", summary="List content-production experiment runs")
    def list_content_production_runs_route(
        case_id: str = "",
        status: str = "",
        proof_status: str = "",
        reference_status: str = "",
        evaluation_status: str = "",
        search: str = "",
        limit: int = 100,
        offset: int = 0,
    ) -> dict[str, Any]:
        return api_ok(
            service.list_content_production_runs(
                case_id=case_id,
                status=status,
                proof_status=proof_status,
                reference_status=reference_status,
                evaluation_status=evaluation_status,
                search=search,
                limit=limit,
                offset=offset,
            )
        )

    @app.get("/workflows/content-production/runs/compare", summary="Compare content-production experiment runs")
    def compare_content_production_runs_route(
        case_id: str = "",
        run_id: Optional[list[str]] = Query(default=None),
        run_ids: str = "",
    ) -> dict[str, Any]:
        ids = [*(run_id or []), *[item.strip() for item in run_ids.split(",") if item.strip()]]
        return api_ok(service.compare_content_production_runs(case_id=case_id, run_ids=ids))

    @app.get("/workflows/content-production/runs/{case_id}/{run_id}", summary="Inspect one content-production experiment run")
    def get_content_production_run(case_id: str, run_id: str) -> dict[str, Any]:
        return api_ok(service.get_content_production_run(case_id, run_id))

    @app.get("/workflows/content-production/runs/{case_id}/{run_id}/acceptance", summary="Inspect one run acceptance report")
    def get_content_production_run_acceptance_route(case_id: str, run_id: str) -> dict[str, Any]:
        return api_ok(service.get_content_production_run_acceptance(case_id, run_id))

    @app.get("/workflows/content-production/runs/{case_id}/{run_id}/evaluations", summary="List run evaluations")
    def list_content_production_run_evaluations_route(case_id: str, run_id: str) -> dict[str, Any]:
        return api_ok(service.list_content_production_run_evaluations(case_id, run_id))

    @app.post("/workflows/content-production/runs/{case_id}/{run_id}/evaluations/draft", summary="Build an automatic run evaluation draft")
    def build_content_production_run_evaluation_draft_route(
        case_id: str,
        run_id: str,
        request: ContentProductionEvaluationDraftRequest,
    ) -> dict[str, Any]:
        return api_ok(service.build_content_production_evaluation_draft(case_id, run_id, request))

    @app.post("/workflows/content-production/runs/{case_id}/{run_id}/evaluations", status_code=201, summary="Record a run evaluation")
    def record_content_production_run_evaluation_route(
        case_id: str,
        run_id: str,
        request: ContentProductionEvaluationRequest,
    ) -> dict[str, Any]:
        return api_ok(service.record_content_production_run_evaluation(case_id, run_id, request))

    @app.post("/workflows/content-production/runs/{case_id}/{run_id}/replay", status_code=201, summary="Replay one content-production experiment run")
    def replay_content_production_run(case_id: str, run_id: str, request: ContentProductionReplayRequest) -> JSONResponse:
        data = service.replay_content_production_run(case_id, run_id, request)
        status_code = 202 if data.get("job_id") else 201
        return JSONResponse(status_code=status_code, content=api_ok(data))

    @app.get("/workflows/content-production/runs/{case_id}/{run_id}/export", summary="Export one content-production run bundle")
    def export_content_production_run(case_id: str, run_id: str, include_inputs: bool = False) -> Response:
        data = service.get_content_production_run_export(case_id, run_id, include_inputs=include_inputs)
        return Response(
            content=data["content"],
            media_type=data["media_type"],
            headers={"Content-Disposition": f'attachment; filename="{data["filename"]}"'},
        )

    @app.get(
        "/workflows/content-production/runs/{case_id}/{run_id}/artifacts/inspect",
        summary="Inspect one run's artifacts for product review",
    )
    def inspect_content_production_run_artifacts_route(case_id: str, run_id: str) -> dict[str, Any]:
        return api_ok(service.inspect_content_production_run_artifacts(case_id, run_id))

    @app.get("/workflows/content-production/runs/{case_id}/{run_id}/artifacts/{artifact_name:path}", summary="Download one run artifact")
    def get_content_production_artifact_file(case_id: str, run_id: str, artifact_name: str) -> FileResponse:
        path = service.get_content_production_artifact_file(case_id, run_id, artifact_name)
        return FileResponse(path, filename=path.name)

    @app.get("/sessions", summary="List in-process sessions")
    def list_sessions() -> dict[str, Any]:
        return api_ok(service.list_sessions())

    @app.post("/sessions", status_code=201, summary="Create a session")
    def create_session(request: SessionCreateRequest) -> dict[str, Any]:
        return api_ok(service.create_session(request))

    @app.get("/sessions/{session_id}", summary="Inspect one session")
    def get_session(session_id: str) -> dict[str, Any]:
        return api_ok(service.get_session(session_id))

    @app.post("/sessions/{session_id}/turns", status_code=201, summary="Append a turn")
    def append_turn(session_id: str, request: TurnCreateRequest) -> dict[str, Any]:
        return api_ok(service.append_turn(session_id, request))

    @app.post("/sessions/{session_id}/tasks", status_code=201, summary="Start a task goal")
    def start_task(session_id: str, request: TaskCreateRequest) -> dict[str, Any]:
        return api_ok(service.start_task(session_id, request))

    return app


app = create_app()


def _model_data(model: Any) -> dict[str, Any]:
    if hasattr(model, "model_dump"):
        return model.model_dump()
    return model.dict()


def _assert_asset_paths_exist(rows: list[dict[str, Any]]) -> None:
    missing = [
        str(row.get("path") or "")
        for row in rows
        if not _is_remote_url(str(row.get("path") or "")) and not Path(str(row.get("path") or "")).is_file()
    ]
    if missing:
        raise ValueError(f"asset path not found: {missing}")


def _execution_mode(value: Any) -> str:
    mode = str(value or "sync").strip().lower()
    if mode in {"sync", "synchronous"}:
        return "sync"
    if mode in {"background", "async"}:
        return "background"
    raise ApiError(f"unsupported execution_mode: {value}", status_code=400)


def _is_remote_url(value: str) -> bool:
    return value.startswith(("http://", "https://"))


def _asset_with_url(session_id: str, row: dict[str, Any]) -> dict[str, Any]:
    data = dict(row)
    asset_id = str(data.get("asset_id") or "")
    if asset_id and not _is_remote_url(str(data.get("path") or "")):
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


def _latest_reference_image_generation_check(events: list[SessionEvent] | list[Any]) -> dict[str, Any]:
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


def _reference_image_generation_run_evidence(
    latest_check: dict[str, Any],
    asset_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    selected_refs = _provider_fetchable_refs_from_asset_rows(asset_rows)
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


def _provider_fetchable_refs_from_asset_rows(asset_rows: list[dict[str, Any]]) -> list[str]:
    urls: list[str] = []
    for row in asset_rows:
        for value in (row.get("public_reference_url"), row.get("path")):
            url = provider_fetchable_reference_url(str(value or ""))
            if url:
                urls.append(url)
                break
    return list(dict.fromkeys(urls))


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


def _attach_public_reference_urls(
    session_id: str,
    rows: list[dict[str, Any]],
    *,
    public_base_url: str = "",
) -> list[dict[str, Any]]:
    base_url = _backend_public_base_url(public_base_url)
    if not base_url:
        return [dict(row) for row in rows]
    out = []
    for row in rows:
        data = dict(row)
        asset_id = str(data.get("asset_id") or "")
        path = str(data.get("path") or "")
        backend_asset_url = _backend_asset_public_reference_url(
            session_id,
            asset_id=asset_id,
            path=path,
            public_base_url=base_url,
        )
        if backend_asset_url:
            data["public_reference_url"] = backend_asset_url
        out.append(data)
    return out


def _backend_asset_public_reference_url(
    session_id: str,
    *,
    asset_id: str,
    path: str,
    public_base_url: str = "",
) -> str:
    base_url = _backend_public_base_url(public_base_url)
    if not base_url or not asset_id or not path or _is_remote_url(path):
        return ""
    return f"{base_url}/sessions/{session_id}/assets/{asset_id}/file"


def _backend_public_base_url(value: str = "") -> str:
    raw = str(value or os.environ.get("NORI_BACKEND_PUBLIC_BASE_URL") or "").strip().rstrip("/")
    return provider_fetchable_reference_url(raw)


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


def _reference_url_probe_summary(payload: dict[str, Any], urls: list[str]) -> dict[str, Any]:
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
    timeout = _reference_url_probe_timeout(payload)
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


def _reference_url_probe_timeout(payload: dict[str, Any]) -> float:
    try:
        value = float(payload.get("reference_url_probe_timeout") or 3.0)
    except (TypeError, ValueError):
        return 3.0
    return min(max(value, 0.1), 30.0)


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
