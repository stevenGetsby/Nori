"""Workflow catalog routes."""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from ..contracts import WorkflowResolveRequest, api_ok
from .service_contracts import WorkflowRouteServiceProtocol


def build_workflows_router(service: WorkflowRouteServiceProtocol) -> APIRouter:
    router = APIRouter(tags=["workflows"])

    @router.get("/workflows", summary="List workflow catalog entries")
    def list_workflows() -> dict[str, Any]:
        return api_ok(service.catalog_service.list_workflows())

    @router.post("/workflows/resolve", summary="Resolve a workflow or direct action for a product request")
    def resolve_workflow(request: WorkflowResolveRequest) -> dict[str, Any]:
        return api_ok(service.catalog_service.resolve_workflow(request))

    @router.get("/workflows/{workflow_id}", summary="Inspect one workflow catalog entry")
    def get_workflow(workflow_id: str) -> dict[str, Any]:
        return api_ok(service.catalog_service.get_workflow(workflow_id))

    return router
