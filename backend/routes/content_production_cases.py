"""Content-production case routes."""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from fastapi.responses import JSONResponse, Response

from ..contracts import (
    ContentProductionEvaluationDraftRequest,
    ContentProductionEvaluationRequest,
    ContentProductionPromotionRequest,
    ContentProductionReplayRequest,
    ContentProductionSelectionRequest,
    api_ok,
)
from .service_contracts import ContentProductionCaseRouteServiceProtocol


def build_content_production_cases_router(service: ContentProductionCaseRouteServiceProtocol) -> APIRouter:
    router = APIRouter(tags=["content-production-cases"])

    @router.get("/experiments/content-production/cases", summary="List content-production experiment cases")
    def list_content_production_cases_route() -> dict[str, Any]:
        return api_ok(service.console_service.list_cases())

    @router.get("/experiments/content-production/cases/{case_id}/selection", summary="Inspect a content-production case selection")
    def get_content_production_case_selection_route(case_id: str) -> dict[str, Any]:
        return api_ok(service.console_service.get_case_selection(case_id))

    @router.post(
        "/experiments/content-production/cases/{case_id}/selection",
        status_code=201,
        summary="Record a content-production case selection",
    )
    def record_content_production_case_selection_route(
        case_id: str,
        request: ContentProductionSelectionRequest,
    ) -> dict[str, Any]:
        return api_ok(service.console_service.record_case_selection(case_id, request))

    @router.post(
        "/experiments/content-production/cases/{case_id}/promotion",
        status_code=201,
        summary="Promote an accepted content-production run",
    )
    def promote_content_production_case_run_route(
        case_id: str,
        request: ContentProductionPromotionRequest,
    ) -> dict[str, Any]:
        return api_ok(service.console_service.promote_case_run(case_id, request))

    @router.post(
        "/experiments/content-production/cases/{case_id}/replay",
        status_code=201,
        summary="Replay the selected or best run for a case",
    )
    def replay_content_production_case_route(case_id: str, request: ContentProductionReplayRequest) -> JSONResponse:
        data = service.run_service.replay_content_production_case(case_id, request)
        status_code = 202 if data.get("job_id") else 201
        return JSONResponse(status_code=status_code, content=api_ok(data))

    @router.post(
        "/experiments/content-production/cases/{case_id}/evaluations/draft",
        summary="Build an evaluation draft for a case target run",
    )
    def build_content_production_case_evaluation_draft_route(
        case_id: str,
        request: ContentProductionEvaluationDraftRequest,
    ) -> dict[str, Any]:
        return api_ok(service.console_service.build_case_evaluation_draft(case_id, request))

    @router.post(
        "/experiments/content-production/cases/{case_id}/evaluations",
        status_code=201,
        summary="Record an evaluation for a case target run",
    )
    def record_content_production_case_evaluation_route(
        case_id: str,
        request: ContentProductionEvaluationRequest,
    ) -> dict[str, Any]:
        return api_ok(service.console_service.record_case_evaluation(case_id, request))

    @router.get("/experiments/content-production/cases/{case_id}/selected-run", summary="Resolve a content-production case selected run")
    def get_content_production_case_selected_run_route(
        case_id: str,
        fallback_to_best: bool = True,
    ) -> dict[str, Any]:
        return api_ok(service.console_service.get_case_selected_run(case_id=case_id, fallback_to_best=fallback_to_best))

    @router.get("/experiments/content-production/cases/{case_id}/compare", summary="Build a case-centered content-production comparison")
    def content_production_case_compare_route(case_id: str, limit: int = 500) -> dict[str, Any]:
        return api_ok(service.console_service.case_compare(case_id=case_id, limit=limit))

    @router.get("/experiments/content-production/cases/{case_id}/next-actions", summary="Plan next content-production case actions")
    def content_production_case_next_actions_route(case_id: str, limit: int = 500) -> dict[str, Any]:
        return api_ok(service.console_service.case_next_actions(case_id=case_id, limit=limit))

    @router.get("/experiments/content-production/cases/{case_id}/delivery", summary="Inspect case delivery readiness")
    def content_production_case_delivery_route(case_id: str, allow_unpromoted: bool = False) -> dict[str, Any]:
        return api_ok(service.console_service.case_delivery(case_id=case_id, allow_unpromoted=allow_unpromoted))

    @router.get("/experiments/content-production/cases/{case_id}/delivery/export", summary="Export one case delivery bundle")
    def export_content_production_case_delivery(case_id: str, allow_unready: bool = False) -> Response:
        data = service.console_service.get_case_delivery_export(case_id, allow_unready=allow_unready)
        return Response(
            content=data["content"],
            media_type=data["media_type"],
            headers={"Content-Disposition": f'attachment; filename="{data["filename"]}"'},
        )

    @router.get("/experiments/content-production/cases/{case_id}/timeline", summary="Inspect a content-production case timeline")
    def content_production_case_timeline_route(case_id: str, limit: int = 200) -> dict[str, Any]:
        return api_ok(service.console_service.case_timeline(case_id=case_id, limit=limit))

    @router.get("/experiments/content-production/cases/{case_id}/export", summary="Export one content-production case bundle")
    def export_content_production_case(case_id: str) -> Response:
        data = service.console_service.get_case_export(case_id)
        return Response(
            content=data["content"],
            media_type=data["media_type"],
            headers={"Content-Disposition": f'attachment; filename="{data["filename"]}"'},
        )

    return router
