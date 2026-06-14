"""Run-level content-production console service operations."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from ..contracts import ApiError, ContentProductionEvaluationDraftRequest, ContentProductionEvaluationRequest
from ..experiments import (
    build_content_production_evaluation_draft,
    build_content_production_run_export,
    compare_content_production_runs,
    get_content_production_run_acceptance,
    inspect_content_production_run_artifacts,
    list_content_production_run_evaluations,
    list_content_production_runs,
    record_content_production_run_evaluation,
    resolve_content_production_artifact_path,
    summarize_content_production_run,
)
from .service_errors import map_service_errors


class BackendContentProductionRunConsoleService:
    """Owns run-level reporting, evaluation, artifact, and export operations."""

    def __init__(self, *, project_root: Path) -> None:
        self.project_root = Path(project_root)

    def list_runs(
        self,
        *,
        case_id: str = "",
        status: str = "",
        proof_status: str = "",
        reference_status: str = "",
        evaluation_status: str = "",
        search: str = "",
        limit: int = 100,
        offset: int = 0,
    ) -> dict[str, Any]:
        return list_content_production_runs(
            project_root=self.project_root,
            case_id=case_id,
            status=status,
            proof_status=proof_status,
            reference_status=reference_status,
            evaluation_status=evaluation_status,
            search=search,
            limit=limit,
            offset=offset,
        )

    def compare_runs(self, *, case_id: str, run_ids: list[str]) -> dict[str, Any]:
        with map_service_errors():
            return compare_content_production_runs(
                project_root=self.project_root,
                case_id=case_id,
                run_ids=run_ids,
            )

    def list_run_evaluations(self, case_id: str, run_id: str) -> dict[str, Any]:
        with map_service_errors():
            return list_content_production_run_evaluations(
                project_root=self.project_root,
                case_id=case_id,
                run_id=run_id,
            )

    def get_run_acceptance(self, case_id: str, run_id: str) -> dict[str, Any]:
        with map_service_errors():
            return get_content_production_run_acceptance(
                project_root=self.project_root,
                case_id=case_id,
                run_id=run_id,
            )

    def inspect_run_artifacts(self, case_id: str, run_id: str) -> dict[str, Any]:
        with map_service_errors():
            return inspect_content_production_run_artifacts(
                project_root=self.project_root,
                case_id=case_id,
                run_id=run_id,
            )

    def build_evaluation_draft(
        self,
        case_id: str,
        run_id: str,
        request: ContentProductionEvaluationDraftRequest,
    ) -> dict[str, Any]:
        with map_service_errors():
            return build_content_production_evaluation_draft(
                project_root=self.project_root,
                case_id=case_id,
                run_id=run_id,
                reviewer=request.reviewer,
                persist=request.persist,
                metadata=dict(request.metadata),
            )

    def record_run_evaluation(
        self,
        case_id: str,
        run_id: str,
        request: ContentProductionEvaluationRequest,
    ) -> dict[str, Any]:
        with map_service_errors():
            return record_content_production_run_evaluation(
                project_root=self.project_root,
                case_id=case_id,
                run_id=run_id,
                evaluation=_model_data(request),
            )

    def get_run(self, case_id: str, run_id: str) -> dict[str, Any]:
        result = summarize_content_production_run(project_root=self.project_root, case_id=case_id, run_id=run_id)
        if not result:
            raise ApiError(f"content-production run not found: {case_id}/{run_id}", status_code=404)
        return result

    def get_artifact_file(self, case_id: str, run_id: str, artifact_name: str) -> Path:
        with map_service_errors():
            return resolve_content_production_artifact_path(
                project_root=self.project_root,
                case_id=case_id,
                run_id=run_id,
                artifact_name=artifact_name,
            )

    def get_run_export(self, case_id: str, run_id: str, *, include_inputs: bool = False) -> dict[str, Any]:
        with map_service_errors():
            return build_content_production_run_export(
                project_root=self.project_root,
                case_id=case_id,
                run_id=run_id,
                include_inputs=include_inputs,
            )


def _model_data(model: Any) -> dict[str, Any]:
    if hasattr(model, "model_dump"):
        return model.model_dump()
    return model.dict()
