"""FastAPI product backend for Nori."""
from __future__ import annotations

from typing import Any
from pathlib import Path

from fastapi import FastAPI, UploadFile
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from nori.sessions import SessionManager

from .contracts import (
    ApiError,
    AssetReferencePublishRequest,
    ContentProductionReplayRequest,
    ContentProductionRunRequest,
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
)
from .content import ContentGenerationCatalog
from .experiments import (
    content_production_diagnostics,
    content_production_experiment_workbench,
    experiment_readiness,
)
from .jobs import InProcessExperimentJobStore
from .routing import register_routes
from .services import BackendServiceBundle
from .workflows import WorkflowCatalog


class NoriBackend:
    """Service layer behind FastAPI routes."""

    def __init__(
        self,
        *,
        session_manager: SessionManager | None = None,
        workflow_catalog: WorkflowCatalog | None = None,
        content_catalog: ContentGenerationCatalog | None = None,
        experiment_runner: Any | None = None,
        job_store: InProcessExperimentJobStore | None = None,
        reference_publisher: Any | None = None,
        upload_root: str | Path | None = None,
        enforce_model_readiness: bool | None = None,
        service_bundle: BackendServiceBundle | None = None,
    ) -> None:
        bundle = service_bundle or BackendServiceBundle.create(
            session_manager=session_manager,
            workflow_catalog=workflow_catalog,
            content_catalog=content_catalog,
            experiment_runner=experiment_runner,
            job_store=job_store,
            reference_publisher=reference_publisher,
            upload_root=upload_root,
            enforce_model_readiness=enforce_model_readiness,
        )
        self.service_bundle = bundle
        self.catalog_service = bundle.catalog_service
        self.experiment_runner = bundle.experiment_runner
        self.enforce_model_readiness = bundle.enforce_model_readiness
        self.content_production_console = bundle.content_production_console
        self.session_manager = bundle.session_manager
        self.session_store = bundle.session_store
        self.upload_root = bundle.upload_root
        self.session_asset_service = bundle.session_asset_service
        self.reference_image_service = bundle.reference_image_service
        self.reference_publisher = bundle.reference_publisher
        self.job_store = bundle.job_store
        self.experiment_job_service = bundle.experiment_job_service
        self.content_production_run_service = bundle.content_production_run_service

    def health(self) -> dict[str, Any]:
        return {
            "status": "ok",
            "service": "nori-backend",
            "runtime": "fastapi",
        }

    def list_workflows(self) -> dict[str, Any]:
        return self.catalog_service.list_workflows()

    def get_workflow(self, workflow_id: str) -> dict[str, Any]:
        return self.catalog_service.get_workflow(workflow_id)

    def resolve_workflow(self, request: WorkflowResolveRequest) -> dict[str, Any]:
        return self.catalog_service.resolve_workflow(request)

    def list_capabilities(self) -> dict[str, Any]:
        return self.catalog_service.list_capabilities()

    def content_options(self) -> dict[str, Any]:
        return self.catalog_service.content_options()

    def content_option_group(self, group_id: str) -> dict[str, Any]:
        return self.catalog_service.content_option_group(group_id)

    def content_actions(self) -> dict[str, Any]:
        return self.catalog_service.content_actions()

    def content_action(self, action_id: str) -> dict[str, Any]:
        return self.catalog_service.content_action(action_id)

    def plan_content_generation(self, request: ContentGenerationPlanRequest) -> dict[str, Any]:
        return self.catalog_service.plan_content_generation(request)

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
        return self.reference_image_service.check_reference_publish(request)

    def check_reference_image_generation(self, request: ReferenceImageGenerationCheckRequest) -> dict[str, Any]:
        return self.reference_image_service.check_reference_image_generation(request)

    def check_session_reference_image_generation(
        self,
        session_id: str,
        request: SessionReferenceImageGenerationCheckRequest,
    ) -> dict[str, Any]:
        return self.reference_image_service.check_session_reference_image_generation(session_id, request)

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
        return self.content_production_run_service.content_production_run_template(
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

    def list_session_assets(self, session_id: str) -> dict[str, Any]:
        return self.session_asset_service.list_session_assets(session_id)

    def upload_session_assets(
        self,
        session_id: str,
        files: list[UploadFile],
        *,
        task_id: str = "",
        usage: str = "reference",
        metadata_json: str = "",
    ) -> dict[str, Any]:
        return self.session_asset_service.upload_session_assets(
            session_id,
            files,
            task_id=task_id,
            usage=usage,
            metadata_json=metadata_json,
        )

    def get_session_asset_file(self, session_id: str, asset_id: str) -> Path:
        return self.session_asset_service.get_session_asset_file(session_id, asset_id)

    def publish_session_asset_references(self, session_id: str, request: AssetReferencePublishRequest) -> dict[str, Any]:
        return self.reference_image_service.publish_session_asset_references(session_id, request)

    def run_content_production(self, request: ContentProductionRunRequest) -> dict[str, Any]:
        return self.content_production_run_service.run_content_production(request)

    def preflight_content_production_run(self, request: ContentProductionRunRequest) -> dict[str, Any]:
        return self.content_production_run_service.preflight_content_production_run(request)

    def replay_content_production_run(
        self,
        case_id: str,
        run_id: str,
        request: ContentProductionReplayRequest,
    ) -> dict[str, Any]:
        return self.content_production_run_service.replay_content_production_run(case_id, run_id, request)

    def replay_content_production_case(
        self,
        case_id: str,
        request: ContentProductionReplayRequest,
    ) -> dict[str, Any]:
        return self.content_production_run_service.replay_content_production_case(case_id, request)

    def get_experiment_job(self, job_id: str) -> dict[str, Any]:
        return self.experiment_job_service.get_experiment_job(job_id)

    def cancel_experiment_job(self, job_id: str, request: ExperimentJobCancelRequest) -> dict[str, Any]:
        return self.experiment_job_service.cancel_experiment_job(job_id, request)

    def list_experiment_jobs(
        self,
        *,
        status: str = "",
        session_id: str = "",
        case_id: str = "",
        job_type: str = "",
    ) -> dict[str, Any]:
        return self.experiment_job_service.list_experiment_jobs(
            status=status,
            session_id=session_id,
            case_id=case_id,
            job_type=job_type,
        )

    def content_production_experiment_overview(self, *, case_id: str = "", limit: int = 20) -> dict[str, Any]:
        return self.content_production_console.experiment_overview(case_id=case_id, limit=limit)

    def content_production_experiment_report(self, *, case_id: str = "", limit: int = 50) -> dict[str, Any]:
        return self.content_production_console.experiment_report(case_id=case_id, limit=limit)

    def list_content_production_cases(self) -> dict[str, Any]:
        return self.content_production_console.list_cases()

    def get_content_production_case_selection(self, case_id: str) -> dict[str, Any]:
        return self.content_production_console.get_case_selection(case_id)

    def record_content_production_case_selection(
        self,
        case_id: str,
        request: ContentProductionSelectionRequest,
    ) -> dict[str, Any]:
        return self.content_production_console.record_case_selection(case_id, request)

    def promote_content_production_case_run(
        self,
        case_id: str,
        request: ContentProductionPromotionRequest,
    ) -> dict[str, Any]:
        return self.content_production_console.promote_case_run(case_id, request)

    def get_content_production_case_selected_run(
        self,
        *,
        case_id: str,
        fallback_to_best: bool = True,
    ) -> dict[str, Any]:
        return self.content_production_console.get_case_selected_run(
            case_id=case_id,
            fallback_to_best=fallback_to_best,
        )

    def content_production_case_compare(self, *, case_id: str, limit: int = 500) -> dict[str, Any]:
        return self.content_production_console.case_compare(case_id=case_id, limit=limit)

    def content_production_case_next_actions(self, *, case_id: str, limit: int = 500) -> dict[str, Any]:
        return self.content_production_console.case_next_actions(case_id=case_id, limit=limit)

    def content_production_case_delivery(self, *, case_id: str, allow_unpromoted: bool = False) -> dict[str, Any]:
        return self.content_production_console.case_delivery(
            case_id=case_id,
            allow_unpromoted=allow_unpromoted,
        )

    def content_production_case_timeline(self, *, case_id: str, limit: int = 200) -> dict[str, Any]:
        return self.content_production_console.case_timeline(case_id=case_id, limit=limit)

    def get_content_production_case_export(self, case_id: str) -> dict[str, Any]:
        return self.content_production_console.get_case_export(case_id)

    def get_content_production_case_delivery_export(self, case_id: str, *, allow_unready: bool = False) -> dict[str, Any]:
        return self.content_production_console.get_case_delivery_export(case_id, allow_unready=allow_unready)

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
        return self.content_production_console.list_runs(
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
        return self.content_production_console.compare_runs(case_id=case_id, run_ids=run_ids)

    def list_content_production_run_evaluations(self, case_id: str, run_id: str) -> dict[str, Any]:
        return self.content_production_console.list_run_evaluations(case_id, run_id)

    def get_content_production_run_acceptance(self, case_id: str, run_id: str) -> dict[str, Any]:
        return self.content_production_console.get_run_acceptance(case_id, run_id)

    def inspect_content_production_run_artifacts(self, case_id: str, run_id: str) -> dict[str, Any]:
        return self.content_production_console.inspect_run_artifacts(case_id, run_id)

    def build_content_production_evaluation_draft(
        self,
        case_id: str,
        run_id: str,
        request: ContentProductionEvaluationDraftRequest,
    ) -> dict[str, Any]:
        return self.content_production_console.build_evaluation_draft(case_id, run_id, request)

    def build_content_production_case_evaluation_draft(
        self,
        case_id: str,
        request: ContentProductionEvaluationDraftRequest,
    ) -> dict[str, Any]:
        return self.content_production_console.build_case_evaluation_draft(case_id, request)

    def record_content_production_run_evaluation(
        self,
        case_id: str,
        run_id: str,
        request: ContentProductionEvaluationRequest,
    ) -> dict[str, Any]:
        return self.content_production_console.record_run_evaluation(case_id, run_id, request)

    def record_content_production_case_evaluation(
        self,
        case_id: str,
        request: ContentProductionEvaluationRequest,
    ) -> dict[str, Any]:
        return self.content_production_console.record_case_evaluation(case_id, request)

    def get_content_production_run(self, case_id: str, run_id: str) -> dict[str, Any]:
        return self.content_production_console.get_run(case_id, run_id)

    def get_content_production_artifact_file(self, case_id: str, run_id: str, artifact_name: str) -> Path:
        return self.content_production_console.get_artifact_file(case_id, run_id, artifact_name)

    def get_content_production_run_export(self, case_id: str, run_id: str, *, include_inputs: bool = False) -> dict[str, Any]:
        return self.content_production_console.get_run_export(case_id, run_id, include_inputs=include_inputs)

    def list_sessions(self) -> dict[str, Any]:
        return self.session_asset_service.list_sessions()

    def create_session(self, request: SessionCreateRequest) -> dict[str, Any]:
        return self.session_asset_service.create_session(request)

    def get_session(self, session_id: str) -> dict[str, Any]:
        return self.session_asset_service.get_session(session_id)

    def append_turn(self, session_id: str, request: TurnCreateRequest) -> dict[str, Any]:
        return self.session_asset_service.append_turn(session_id, request)

    def start_task(self, session_id: str, request: TaskCreateRequest) -> dict[str, Any]:
        return self.session_asset_service.start_task(session_id, request)


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

    register_routes(app, service)

    return app


app = create_app()
