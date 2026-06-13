"""System and capability routes."""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from ..contracts import api_ok


def build_system_router(service: Any) -> APIRouter:
    router = APIRouter(tags=["system"])

    @router.get("/health", summary="Service health")
    def health() -> dict[str, Any]:
        return api_ok(service.health())

    @router.get("/capabilities", summary="List product capability groups")
    def list_capabilities() -> dict[str, Any]:
        return api_ok(service.list_capabilities())

    return router
