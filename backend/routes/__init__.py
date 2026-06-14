"""Product-facing FastAPI route modules."""
from __future__ import annotations

from typing import Callable

from fastapi import APIRouter, FastAPI

from .content_generation import build_content_generation_router
from .content_production_admin import build_content_production_admin_router
from .content_production_cases import build_content_production_cases_router
from .content_production_runs import build_content_production_runs_router
from .experiment_jobs import build_experiment_jobs_router
from .service_contracts import RouteServiceRegistryProtocol
from .sessions import build_sessions_router
from .system import build_system_router
from .workflows import build_workflows_router

RouteBuilder = Callable[..., APIRouter]
RouteModule = tuple[str, RouteBuilder]

ROUTE_MODULES: tuple[RouteModule, ...] = (
    ("system", build_system_router),
    ("workflows", build_workflows_router),
    ("content_production_admin", build_content_production_admin_router),
    ("experiment_jobs", build_experiment_jobs_router),
    ("content_generation", build_content_generation_router),
    ("sessions", build_sessions_router),
    ("content_production_runs", build_content_production_runs_router),
    ("content_production_cases", build_content_production_cases_router),
)

ROUTE_BUILDERS: tuple[RouteBuilder, ...] = tuple(build_router for _name, build_router in ROUTE_MODULES)


def register_route_modules(app: FastAPI, route_services: RouteServiceRegistryProtocol) -> None:
    """Attach all route modules to the FastAPI application."""

    for service_name, build_router in ROUTE_MODULES:
        route_service = getattr(route_services, service_name)
        app.include_router(build_router(route_service))
