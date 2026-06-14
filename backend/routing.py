"""FastAPI route composition for the Nori backend."""
from __future__ import annotations

from fastapi import FastAPI

from .routes import register_route_modules
from .routes.service_contracts import RouteServiceRegistryProtocol


def register_routes(app: FastAPI, route_services: RouteServiceRegistryProtocol) -> None:
    """Register all backend HTTP route modules."""

    register_route_modules(app, route_services)
