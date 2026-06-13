"""FastAPI route registration for the Nori backend."""
from __future__ import annotations

from typing import Any, Optional

from fastapi import FastAPI, File, Form, Query, UploadFile
from fastapi.responses import FileResponse, JSONResponse, Response

from .contracts import (
    AssetReferencePublishRequest,
    ContentGenerationPlanRequest,
    ContentProductionEvaluationDraftRequest,
    ContentProductionEvaluationRequest,
    ContentProductionPromotionRequest,
    ContentProductionReplayRequest,
    ContentProductionRunRequest,
    ContentProductionRunTemplateRequest,
    ContentProductionSelectionRequest,
    ExperimentJobCancelRequest,
    ReferenceImageGenerationCheckRequest,
    ReferencePublishCheckRequest,
    SessionCreateRequest,
    SessionReferenceImageGenerationCheckRequest,
    TaskCreateRequest,
    TurnCreateRequest,
    WorkflowResolveRequest,
    api_ok,
)


def register_routes(app: FastAPI, service: Any) -> None:
    """Register HTTP routes against a backend service facade."""

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



def _model_data(model: Any) -> dict[str, Any]:
    if hasattr(model, "model_dump"):
        return model.model_dump()
    return model.dict()
