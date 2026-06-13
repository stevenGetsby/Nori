"""Session, task, and asset routes."""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import FileResponse

from ..contracts import (
    AssetReferencePublishRequest,
    SessionCreateRequest,
    SessionReferenceImageGenerationCheckRequest,
    TaskCreateRequest,
    TurnCreateRequest,
    api_ok,
)


def build_sessions_router(service: Any) -> APIRouter:
    router = APIRouter(tags=["sessions"])

    @router.get("/sessions/{session_id}/assets", summary="List uploaded assets for one session")
    def list_session_assets(session_id: str) -> dict[str, Any]:
        return api_ok(service.session_asset_service.list_session_assets(session_id))

    @router.get("/sessions/{session_id}/assets/{asset_id}/file", summary="Download one uploaded session asset")
    def get_session_asset_file(session_id: str, asset_id: str) -> FileResponse:
        path = service.session_asset_service.get_session_asset_file(session_id, asset_id)
        return FileResponse(path, filename=path.name)

    @router.post("/sessions/{session_id}/assets", status_code=201, summary="Upload image assets for a session")
    def upload_session_assets(
        session_id: str,
        files: list[UploadFile] = File(...),
        task_id: str = Form(""),
        usage: str = Form("reference"),
        metadata_json: str = Form(""),
    ) -> dict[str, Any]:
        return api_ok(
            service.session_asset_service.upload_session_assets(
                session_id,
                files,
                task_id=task_id,
                usage=usage,
                metadata_json=metadata_json,
            )
        )

    @router.post(
        "/sessions/{session_id}/assets/publish-references",
        summary="Publish session assets as model-fetchable references",
    )
    def publish_session_asset_references(session_id: str, request: AssetReferencePublishRequest) -> dict[str, Any]:
        return api_ok(service.reference_image_service.publish_session_asset_references(session_id, request))

    @router.post(
        "/sessions/{session_id}/assets/reference-image-generation-check",
        summary="Publish session image assets and verify active image-model reference support",
    )
    def check_session_reference_image_generation(
        session_id: str,
        request: SessionReferenceImageGenerationCheckRequest,
    ) -> dict[str, Any]:
        return api_ok(service.reference_image_service.check_session_reference_image_generation(session_id, request))

    @router.get("/sessions", summary="List in-process sessions")
    def list_sessions() -> dict[str, Any]:
        return api_ok(service.session_asset_service.list_sessions())

    @router.post("/sessions", status_code=201, summary="Create a session")
    def create_session(request: SessionCreateRequest) -> dict[str, Any]:
        return api_ok(service.session_asset_service.create_session(request))

    @router.get("/sessions/{session_id}", summary="Inspect one session")
    def get_session(session_id: str) -> dict[str, Any]:
        return api_ok(service.session_asset_service.get_session(session_id))

    @router.post("/sessions/{session_id}/turns", status_code=201, summary="Append a turn")
    def append_turn(session_id: str, request: TurnCreateRequest) -> dict[str, Any]:
        return api_ok(service.session_asset_service.append_turn(session_id, request))

    @router.post("/sessions/{session_id}/tasks", status_code=201, summary="Start a task goal")
    def start_task(session_id: str, request: TaskCreateRequest) -> dict[str, Any]:
        return api_ok(service.session_asset_service.start_task(session_id, request))

    return router
