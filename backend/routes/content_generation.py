"""Content generation catalog and planning routes."""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from ..contracts import ContentGenerationPlanRequest, api_ok


def build_content_generation_router(service: Any) -> APIRouter:
    router = APIRouter(tags=["content-generation"])

    @router.get("/content/generation/options", summary="List content generation option groups")
    def content_options() -> dict[str, Any]:
        return api_ok(service.content_options())

    @router.get("/content/generation/options/{group_id}", summary="Inspect one content generation option group")
    def content_option_group(group_id: str) -> dict[str, Any]:
        return api_ok(service.content_option_group(group_id))

    @router.get("/content/generation/actions", summary="List content generation sub-capabilities")
    def content_actions() -> dict[str, Any]:
        return api_ok(service.content_actions())

    @router.get("/content/generation/actions/{action_id}", summary="Inspect one content generation action")
    def content_action(action_id: str) -> dict[str, Any]:
        return api_ok(service.content_action(action_id))

    @router.post("/content/generation/plan", summary="Plan a content generation entrypoint")
    def plan_content_generation(request: ContentGenerationPlanRequest) -> dict[str, Any]:
        return api_ok(service.plan_content_generation(request))

    return router
