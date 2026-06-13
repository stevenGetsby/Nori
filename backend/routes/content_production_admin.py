"""Content-production diagnostics, readiness, and launch routes."""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Query

from ..contracts import (
    ContentProductionRunTemplateRequest,
    ReferenceImageGenerationCheckRequest,
    ReferencePublishCheckRequest,
    api_ok,
)
from .shared import model_data


def build_content_production_admin_router(service: Any) -> APIRouter:
    router = APIRouter(tags=["content-production"])

    @router.get("/experiments/readiness", summary="Inspect backend experiment readiness")
    def get_experiment_readiness() -> dict[str, Any]:
        return api_ok(service.admin_service.experiment_readiness())

    @router.get(
        "/experiments/content-production/diagnostics",
        summary="Diagnose content-production backend experiment readiness",
    )
    def get_content_production_diagnostics() -> dict[str, Any]:
        return api_ok(service.admin_service.content_production_diagnostics())

    @router.post(
        "/experiments/content-production/reference-publish-check",
        summary="Verify reference-image publishing with a backend-owned test image",
    )
    def check_reference_publish(request: ReferencePublishCheckRequest) -> dict[str, Any]:
        return api_ok(service.reference_image_service.check_reference_publish(request))

    @router.post(
        "/experiments/content-production/reference-image-generation-check",
        summary="Verify reference-image generation with the active image model",
    )
    def check_reference_image_generation(request: ReferenceImageGenerationCheckRequest) -> dict[str, Any]:
        return api_ok(service.reference_image_service.check_reference_image_generation(request))

    @router.get("/experiments/content-production/run-template", summary="Build a content-production run request template")
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
            service.run_service.content_production_run_template(
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

    @router.post(
        "/experiments/content-production/run-template",
        summary="Build a content-production run request template from a form draft",
    )
    def post_content_production_run_template(request: ContentProductionRunTemplateRequest) -> dict[str, Any]:
        data = model_data(request)
        return api_ok(
            service.run_service.content_production_run_template(
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

    @router.get("/experiments/content-production/overview", summary="Summarize content-production experiment health")
    def content_production_experiment_overview_route(case_id: str = "", limit: int = 20) -> dict[str, Any]:
        return api_ok(service.console_service.experiment_overview(case_id=case_id, limit=limit))

    @router.get("/experiments/content-production/workbench", summary="Build a content-production experiment workbench snapshot")
    def content_production_experiment_workbench_route(
        case_id: str = "",
        limit: int = 20,
        include_diagnostics: bool = True,
    ) -> dict[str, Any]:
        return api_ok(
            service.admin_service.content_production_experiment_workbench(
                case_id=case_id,
                limit=limit,
                include_diagnostics=include_diagnostics,
            )
        )

    @router.get("/experiments/content-production/report", summary="Build a content-production experiment report")
    def content_production_experiment_report_route(case_id: str = "", limit: int = 50) -> dict[str, Any]:
        return api_ok(service.console_service.experiment_report(case_id=case_id, limit=limit))

    return router
