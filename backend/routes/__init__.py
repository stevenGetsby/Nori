"""Product-facing FastAPI route modules."""
from __future__ import annotations

from typing import Any, Callable

from fastapi import APIRouter, FastAPI

from .content_generation import build_content_generation_router
from .content_production_admin import build_content_production_admin_router
from .content_production_cases import build_content_production_cases_router
from .content_production_runs import build_content_production_runs_router
from .experiment_jobs import build_experiment_jobs_router
from .sessions import build_sessions_router
from .system import build_system_router
from .workflows import build_workflows_router

RouteBuilder = Callable[[Any], APIRouter]

ROUTE_BUILDERS: tuple[RouteBuilder, ...] = (
    build_system_router,
    build_workflows_router,
    build_content_production_admin_router,
    build_experiment_jobs_router,
    build_content_generation_router,
    build_sessions_router,
    build_content_production_runs_router,
    build_content_production_cases_router,
)


def register_route_modules(app: FastAPI, service: Any) -> None:
    """Attach all route modules to the FastAPI application."""

    for build_router in ROUTE_BUILDERS:
        app.include_router(build_router(service))
