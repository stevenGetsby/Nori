"""FastAPI application factory for the Nori product backend."""
from __future__ import annotations

from typing import Any

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from .contracts import ApiError, api_error
from .facade import NoriBackend
from .routing import register_routes


def create_app(*, backend: NoriBackend | None = None) -> FastAPI:
    """Create the FastAPI application."""

    service = backend or NoriBackend()
    app = FastAPI(
        title="Nori Backend API",
        version="0.1.0",
        description="Product-service adapter for sessions and workflow catalog. Agent logic stays in nori/.",
    )
    app.state.backend = service

    @app.exception_handler(ApiError)
    async def api_error_handler(_request: Any, exc: ApiError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=api_error(exc.message, status_code=exc.status_code, data=exc.data),
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_error_handler(_request: Any, exc: StarletteHTTPException) -> JSONResponse:
        message = str(exc.detail)
        return JSONResponse(status_code=exc.status_code, content=api_error(message, status_code=exc.status_code))

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(_request: Any, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content=api_error("request validation failed", status_code=422, data={"errors": exc.errors()}),
        )

    register_routes(app, service)

    return app


app = create_app()
