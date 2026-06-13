"""Content-production run routes."""
from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Query
from fastapi.responses import FileResponse, JSONResponse, Response

from ..contracts import (
    ContentProductionEvaluationDraftRequest,
    ContentProductionEvaluationRequest,
    ContentProductionReplayRequest,
    ContentProductionRunRequest,
    api_ok,
)


def build_content_production_runs_router(service: Any) -> APIRouter:
    router = APIRouter(tags=["content-production-runs"])

    @router.post("/workflows/content-production/runs", status_code=201, summary="Run content-production with uploaded assets")
    def run_content_production(request: ContentProductionRunRequest) -> JSONResponse:
        data = service.run_service.run_content_production(request)
        status_code = 202 if data.get("job_id") else 201
        return JSONResponse(status_code=status_code, content=api_ok(data))

    @router.post("/workflows/content-production/runs/preflight", summary="Preflight a content-production experiment run")
    def preflight_content_production_run(request: ContentProductionRunRequest) -> dict[str, Any]:
        return api_ok(service.run_service.preflight_content_production_run(request))

    @router.get("/workflows/content-production/runs", summary="List content-production experiment runs")
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
            service.console_service.list_runs(
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

    @router.get("/workflows/content-production/runs/compare", summary="Compare content-production experiment runs")
    def compare_content_production_runs_route(
        case_id: str = "",
        run_id: Optional[list[str]] = Query(default=None),
        run_ids: str = "",
    ) -> dict[str, Any]:
        ids = [*(run_id or []), *[item.strip() for item in run_ids.split(",") if item.strip()]]
        return api_ok(service.console_service.compare_runs(case_id=case_id, run_ids=ids))

    @router.get("/workflows/content-production/runs/{case_id}/{run_id}", summary="Inspect one content-production experiment run")
    def get_content_production_run(case_id: str, run_id: str) -> dict[str, Any]:
        return api_ok(service.console_service.get_run(case_id, run_id))

    @router.get("/workflows/content-production/runs/{case_id}/{run_id}/acceptance", summary="Inspect one run acceptance report")
    def get_content_production_run_acceptance_route(case_id: str, run_id: str) -> dict[str, Any]:
        return api_ok(service.console_service.get_run_acceptance(case_id, run_id))

    @router.get("/workflows/content-production/runs/{case_id}/{run_id}/evaluations", summary="List run evaluations")
    def list_content_production_run_evaluations_route(case_id: str, run_id: str) -> dict[str, Any]:
        return api_ok(service.console_service.list_run_evaluations(case_id, run_id))

    @router.post("/workflows/content-production/runs/{case_id}/{run_id}/evaluations/draft", summary="Build an automatic run evaluation draft")
    def build_content_production_run_evaluation_draft_route(
        case_id: str,
        run_id: str,
        request: ContentProductionEvaluationDraftRequest,
    ) -> dict[str, Any]:
        return api_ok(service.console_service.build_evaluation_draft(case_id, run_id, request))

    @router.post("/workflows/content-production/runs/{case_id}/{run_id}/evaluations", status_code=201, summary="Record a run evaluation")
    def record_content_production_run_evaluation_route(
        case_id: str,
        run_id: str,
        request: ContentProductionEvaluationRequest,
    ) -> dict[str, Any]:
        return api_ok(service.console_service.record_run_evaluation(case_id, run_id, request))

    @router.post("/workflows/content-production/runs/{case_id}/{run_id}/replay", status_code=201, summary="Replay one content-production experiment run")
    def replay_content_production_run(case_id: str, run_id: str, request: ContentProductionReplayRequest) -> JSONResponse:
        data = service.run_service.replay_content_production_run(case_id, run_id, request)
        status_code = 202 if data.get("job_id") else 201
        return JSONResponse(status_code=status_code, content=api_ok(data))

    @router.get("/workflows/content-production/runs/{case_id}/{run_id}/export", summary="Export one content-production run bundle")
    def export_content_production_run(case_id: str, run_id: str, include_inputs: bool = False) -> Response:
        data = service.console_service.get_run_export(case_id, run_id, include_inputs=include_inputs)
        return Response(
            content=data["content"],
            media_type=data["media_type"],
            headers={"Content-Disposition": f'attachment; filename="{data["filename"]}"'},
        )

    @router.get(
        "/workflows/content-production/runs/{case_id}/{run_id}/artifacts/inspect",
        summary="Inspect one run's artifacts for product review",
    )
    def inspect_content_production_run_artifacts_route(case_id: str, run_id: str) -> dict[str, Any]:
        return api_ok(service.console_service.inspect_run_artifacts(case_id, run_id))

    @router.get(
        "/workflows/content-production/runs/{case_id}/{run_id}/artifacts/{artifact_name:path}",
        summary="Download one run artifact",
    )
    def get_content_production_artifact_file(case_id: str, run_id: str, artifact_name: str) -> FileResponse:
        path = service.console_service.get_artifact_file(case_id, run_id, artifact_name)
        return FileResponse(path, filename=path.name)

    return router
