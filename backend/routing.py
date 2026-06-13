"""FastAPI route composition for the Nori backend."""
from __future__ import annotations

from typing import Any

from fastapi import FastAPI

from .routes import register_route_modules


def register_routes(app: FastAPI, service: Any) -> None:
    """Register all backend HTTP route modules."""

    register_route_modules(app, service)
