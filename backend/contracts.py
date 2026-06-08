"""Backend API contracts and response helpers."""
from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, Field


class ApiError(Exception):
    """Application error rendered through the shared API response shape."""

    def __init__(self, message: str, *, status_code: int = 400, data: Any = None) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.data = data


class SessionCreateRequest(BaseModel):
    user_id: str = ""
    profile_id: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)


class TurnCreateRequest(BaseModel):
    role: str = "user"
    content: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)


class TaskCreateRequest(BaseModel):
    goal: str
    workflow_name: str = ""
    acceptance: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class AssetReferencePublishRequest(BaseModel):
    asset_ids: list[str] = Field(default_factory=list)
    project: str = ""
    force: bool = False
    backend_public_base_url: str = ""
    public_url_map: dict[str, str] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)


class ReferencePublishCheckRequest(BaseModel):
    project: str = "diagnostics"
    session: str = "reference_publish_check"
    public_url_map: dict[str, str] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)


class ReferenceImageGenerationCheckRequest(BaseModel):
    prompt: str = "Generate a simple product image using the provided reference image."
    reference_images: list[str] = Field(default_factory=list)
    size: str = "1024x1024"
    metadata: dict[str, Any] = Field(default_factory=dict)


class SessionReferenceImageGenerationCheckRequest(BaseModel):
    asset_ids: list[str] = Field(default_factory=list)
    project: str = ""
    force_publish: bool = False
    backend_public_base_url: str = ""
    public_url_map: dict[str, str] = Field(default_factory=dict)
    verify_reference_urls: bool = False
    reference_url_probe_timeout: float = 3.0
    prompt: str = "Generate a simple product image using the selected session reference image."
    size: str = "1024x1024"
    metadata: dict[str, Any] = Field(default_factory=dict)


class ExperimentJobCancelRequest(BaseModel):
    reason: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)


class ContentGenerationPlanRequest(BaseModel):
    goal: str = ""
    platform: str = ""
    artifact_type: str = ""
    image_source: str = ""
    cover_strategy: str = ""
    human_gate_mode: str = ""
    entry_mode: str = ""
    workflow_id: str = ""
    action_id: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)


class WorkflowResolveRequest(BaseModel):
    goal: str = ""
    capability_id: str = ""
    workflow_id: str = ""
    action_id: str = ""
    prefer_direct_action: bool = False
    metadata: dict[str, Any] = Field(default_factory=dict)


class ContentProductionRunRequest(BaseModel):
    session_id: str
    task_id: str = ""
    goal: str = ""
    brief_text: str = ""
    case_id: str = ""
    case_title: str = ""
    platform: str = "xhs"
    asset_ids: list[str] = Field(default_factory=list)
    asset_paths: list[str] = Field(default_factory=list)
    backend_public_base_url: str = ""
    execution_mode: str = "sync"
    human_gate_mode: str = "skip"
    require_image_references: bool = False
    require_reference_image_generation_check: bool = False
    verify_reference_urls: bool = False
    reference_url_probe_timeout: float = 3.0
    market_evidence: dict[str, Any] = Field(default_factory=dict)
    config: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)


class ContentProductionRunTemplateRequest(BaseModel):
    session_id: str = ""
    task_id: str = ""
    goal: str = ""
    brief_text: str = ""
    case_id: str = ""
    case_title: str = ""
    platform: str = "xhs"
    asset_ids: list[str] = Field(default_factory=list)
    asset_paths: list[str] = Field(default_factory=list)
    backend_public_base_url: str = ""
    execution_mode: str = "sync"
    human_gate_mode: str = "skip"
    require_image_references: bool = False
    require_reference_image_generation_check: bool = False
    verify_reference_urls: bool = False
    reference_url_probe_timeout: float = 3.0
    market_evidence: dict[str, Any] = Field(default_factory=dict)
    config: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)


class ContentProductionReplayRequest(BaseModel):
    session_id: str = ""
    task_id: str = ""
    run_id: str = ""
    case_id: str = ""
    case_title: str = ""
    execution_mode: str = ""
    human_gate_mode: str = ""
    backend_public_base_url: str = ""
    require_image_references: Optional[bool] = None
    require_reference_image_generation_check: Optional[bool] = None
    verify_reference_urls: Optional[bool] = None
    reference_url_probe_timeout: Optional[float] = None
    overrides: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)


class ContentProductionEvaluationRequest(BaseModel):
    run_id: str = ""
    reviewer: str = ""
    source: str = "manual"
    status: str = "pending"
    score: Optional[int] = None
    notes: str = ""
    issues: list[dict[str, Any]] = Field(default_factory=list)
    metrics: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)


class ContentProductionEvaluationDraftRequest(BaseModel):
    run_id: str = ""
    reviewer: str = "auto_review_gate"
    persist: bool = False
    metadata: dict[str, Any] = Field(default_factory=dict)


class ContentProductionSelectionRequest(BaseModel):
    run_id: str
    decision: str = "selected"
    reviewer: str = "operator"
    reason: str = ""
    notes: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)


class ContentProductionPromotionRequest(BaseModel):
    run_id: str = ""
    reviewer: str = "operator"
    reason: str = ""
    notes: str = ""
    allow_unaccepted: bool = False
    metadata: dict[str, Any] = Field(default_factory=dict)


def api_ok(data: Any = None, *, message: str = "ok") -> dict[str, Any]:
    return {"code": 0, "message": message, "data": data}


def api_error(message: str, *, status_code: int, data: Any = None) -> dict[str, Any]:
    return {"code": status_code, "message": message, "data": data}
