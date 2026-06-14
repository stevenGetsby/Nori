"""Content-production admin, readiness, diagnostics, and workbench service."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from ..experiments import (
    content_production_diagnostics,
    content_production_experiment_workbench,
    experiment_readiness,
)


class BackendContentProductionAdminService:
    """Owns content-production admin views exposed through FastAPI routes."""

    def __init__(self, *, project_root: str | Path) -> None:
        self.project_root = Path(project_root)

    def experiment_readiness(self) -> dict[str, Any]:
        return experiment_readiness(project_root=self.project_root)

    def content_production_diagnostics(self) -> dict[str, Any]:
        data = content_production_diagnostics(project_root=self.project_root)
        data["routes"]["reference_publish_check"] = "/experiments/content-production/reference-publish-check"
        data["routes"]["reference_image_generation_check"] = (
            "/experiments/content-production/reference-image-generation-check"
        )
        data["routes"]["session_reference_image_generation_check"] = (
            "/sessions/{session_id}/assets/reference-image-generation-check"
        )
        return data

    def content_production_experiment_workbench(
        self,
        *,
        case_id: str = "",
        limit: int = 20,
        include_diagnostics: bool = True,
    ) -> dict[str, Any]:
        return content_production_experiment_workbench(
            project_root=self.project_root,
            case_id=case_id,
            limit=limit,
            include_diagnostics=include_diagnostics,
        )
