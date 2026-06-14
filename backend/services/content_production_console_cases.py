"""Case-level content-production console service operations."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from ..contracts import (
    ApiError,
    ContentProductionEvaluationDraftRequest,
    ContentProductionEvaluationRequest,
    ContentProductionPromotionRequest,
    ContentProductionSelectionRequest,
)
from ..experiments import (
    build_content_production_case_delivery_export,
    build_content_production_case_export,
    content_production_case_compare,
    content_production_case_delivery,
    content_production_case_next_actions,
    content_production_case_timeline,
    content_production_experiment_overview,
    content_production_experiment_report,
    get_content_production_case_selection,
    get_content_production_case_selected_run,
    list_content_production_cases,
    promote_content_production_case_run,
    record_content_production_case_selection,
    summarize_content_production_run,
)
from .content_production_console_runs import BackendContentProductionRunConsoleService
from .service_errors import map_service_errors


class BackendContentProductionCaseConsoleService:
    """Owns case-level reporting, selection, review, delivery, and export operations."""

    def __init__(
        self,
        *,
        project_root: Path,
        run_console: BackendContentProductionRunConsoleService,
    ) -> None:
        self.project_root = Path(project_root)
        self.run_console = run_console

    def experiment_overview(self, *, case_id: str = "", limit: int = 20) -> dict[str, Any]:
        return content_production_experiment_overview(
            project_root=self.project_root,
            case_id=case_id,
            limit=limit,
        )

    def experiment_report(self, *, case_id: str = "", limit: int = 50) -> dict[str, Any]:
        return content_production_experiment_report(
            project_root=self.project_root,
            case_id=case_id,
            limit=limit,
        )

    def list_cases(self) -> dict[str, Any]:
        return list_content_production_cases(project_root=self.project_root)

    def get_case_selection(self, case_id: str) -> dict[str, Any]:
        with map_service_errors():
            return get_content_production_case_selection(project_root=self.project_root, case_id=case_id)

    def record_case_selection(
        self,
        case_id: str,
        request: ContentProductionSelectionRequest,
    ) -> dict[str, Any]:
        with map_service_errors():
            return record_content_production_case_selection(
                project_root=self.project_root,
                case_id=case_id,
                selection=_model_data(request),
            )

    def promote_case_run(
        self,
        case_id: str,
        request: ContentProductionPromotionRequest,
    ) -> dict[str, Any]:
        with map_service_errors():
            return promote_content_production_case_run(
                project_root=self.project_root,
                case_id=case_id,
                promotion=_model_data(request),
            )

    def get_case_selected_run(
        self,
        *,
        case_id: str,
        fallback_to_best: bool = True,
    ) -> dict[str, Any]:
        with map_service_errors():
            return get_content_production_case_selected_run(
                project_root=self.project_root,
                case_id=case_id,
                fallback_to_best=fallback_to_best,
            )

    def case_compare(self, *, case_id: str, limit: int = 500) -> dict[str, Any]:
        with map_service_errors():
            return content_production_case_compare(project_root=self.project_root, case_id=case_id, limit=limit)

    def case_next_actions(self, *, case_id: str, limit: int = 500) -> dict[str, Any]:
        with map_service_errors():
            return content_production_case_next_actions(project_root=self.project_root, case_id=case_id, limit=limit)

    def case_delivery(self, *, case_id: str, allow_unpromoted: bool = False) -> dict[str, Any]:
        with map_service_errors():
            return content_production_case_delivery(
                project_root=self.project_root,
                case_id=case_id,
                allow_unpromoted=allow_unpromoted,
            )

    def case_timeline(self, *, case_id: str, limit: int = 200) -> dict[str, Any]:
        with map_service_errors():
            return content_production_case_timeline(project_root=self.project_root, case_id=case_id, limit=limit)

    def get_case_export(self, case_id: str) -> dict[str, Any]:
        with map_service_errors():
            return build_content_production_case_export(project_root=self.project_root, case_id=case_id)

    def get_case_delivery_export(self, case_id: str, *, allow_unready: bool = False) -> dict[str, Any]:
        with map_service_errors():
            return build_content_production_case_delivery_export(
                project_root=self.project_root,
                case_id=case_id,
                allow_unready=allow_unready,
            )

    def build_case_evaluation_draft(
        self,
        case_id: str,
        request: ContentProductionEvaluationDraftRequest,
    ) -> dict[str, Any]:
        run_id, source = self._resolve_case_run_id(case_id, run_id=request.run_id)
        data = self.run_console.build_evaluation_draft(case_id, run_id, request)
        data.setdefault("source", "case_evaluation_draft")
        data.setdefault("source_case_id", case_id)
        data.setdefault("source_run_id", run_id)
        data.setdefault("source_run_selector", source)
        return data

    def record_case_evaluation(
        self,
        case_id: str,
        request: ContentProductionEvaluationRequest,
    ) -> dict[str, Any]:
        run_id, source = self._resolve_case_run_id(case_id, run_id=request.run_id)
        data = self.run_console.record_run_evaluation(case_id, run_id, request)
        data.setdefault("source", "case_evaluation")
        data.setdefault("source_case_id", case_id)
        data.setdefault("source_run_id", run_id)
        data.setdefault("source_run_selector", source)
        return data

    def _resolve_case_run_id(self, case_id: str, *, run_id: str = "") -> tuple[str, str]:
        explicit_run_id = str(run_id or "").strip()
        if explicit_run_id:
            summary = summarize_content_production_run(
                project_root=self.project_root,
                case_id=case_id,
                run_id=explicit_run_id,
            )
            if not summary:
                raise ApiError(f"content-production run not found: {case_id}/{explicit_run_id}", status_code=404)
            return explicit_run_id, "request"
        with map_service_errors():
            selected = get_content_production_case_selected_run(
                project_root=self.project_root,
                case_id=case_id,
                fallback_to_best=True,
            )
        resolved_run_id = str(selected.get("run_id") or "")
        if not resolved_run_id:
            raise ApiError(f"no target run found for case: {case_id}", status_code=404)
        return resolved_run_id, str(selected.get("source") or "")


def _model_data(model: Any) -> dict[str, Any]:
    if hasattr(model, "model_dump"):
        return model.model_dump()
    return model.dict()
