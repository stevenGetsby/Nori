"""Content-production experiment console service facade."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from ..contracts import (
    ContentProductionEvaluationDraftRequest,
    ContentProductionEvaluationRequest,
    ContentProductionPromotionRequest,
    ContentProductionSelectionRequest,
)
from .content_production_console_cases import BackendContentProductionCaseConsoleService
from .content_production_console_runs import BackendContentProductionRunConsoleService


class BackendContentProductionConsoleService:
    """Route-compatible facade over case-level and run-level console services."""

    def __init__(
        self,
        *,
        project_root: Path,
        case_console: BackendContentProductionCaseConsoleService | None = None,
        run_console: BackendContentProductionRunConsoleService | None = None,
    ) -> None:
        self.project_root = Path(project_root)
        self.run_console = run_console or BackendContentProductionRunConsoleService(project_root=self.project_root)
        self.case_console = case_console or BackendContentProductionCaseConsoleService(
            project_root=self.project_root,
            run_console=self.run_console,
        )

    def experiment_overview(self, *, case_id: str = "", limit: int = 20) -> dict[str, Any]:
        return self.case_console.experiment_overview(case_id=case_id, limit=limit)

    def experiment_report(self, *, case_id: str = "", limit: int = 50) -> dict[str, Any]:
        return self.case_console.experiment_report(case_id=case_id, limit=limit)

    def list_cases(self) -> dict[str, Any]:
        return self.case_console.list_cases()

    def get_case_selection(self, case_id: str) -> dict[str, Any]:
        return self.case_console.get_case_selection(case_id)

    def record_case_selection(
        self,
        case_id: str,
        request: ContentProductionSelectionRequest,
    ) -> dict[str, Any]:
        return self.case_console.record_case_selection(case_id, request)

    def promote_case_run(
        self,
        case_id: str,
        request: ContentProductionPromotionRequest,
    ) -> dict[str, Any]:
        return self.case_console.promote_case_run(case_id, request)

    def get_case_selected_run(
        self,
        *,
        case_id: str,
        fallback_to_best: bool = True,
    ) -> dict[str, Any]:
        return self.case_console.get_case_selected_run(case_id=case_id, fallback_to_best=fallback_to_best)

    def case_compare(self, *, case_id: str, limit: int = 500) -> dict[str, Any]:
        return self.case_console.case_compare(case_id=case_id, limit=limit)

    def case_next_actions(self, *, case_id: str, limit: int = 500) -> dict[str, Any]:
        return self.case_console.case_next_actions(case_id=case_id, limit=limit)

    def case_delivery(self, *, case_id: str, allow_unpromoted: bool = False) -> dict[str, Any]:
        return self.case_console.case_delivery(case_id=case_id, allow_unpromoted=allow_unpromoted)

    def case_timeline(self, *, case_id: str, limit: int = 200) -> dict[str, Any]:
        return self.case_console.case_timeline(case_id=case_id, limit=limit)

    def get_case_export(self, case_id: str) -> dict[str, Any]:
        return self.case_console.get_case_export(case_id)

    def get_case_delivery_export(self, case_id: str, *, allow_unready: bool = False) -> dict[str, Any]:
        return self.case_console.get_case_delivery_export(case_id, allow_unready=allow_unready)

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
        return self.run_console.list_runs(
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
        return self.run_console.compare_runs(case_id=case_id, run_ids=run_ids)

    def list_run_evaluations(self, case_id: str, run_id: str) -> dict[str, Any]:
        return self.run_console.list_run_evaluations(case_id, run_id)

    def get_run_acceptance(self, case_id: str, run_id: str) -> dict[str, Any]:
        return self.run_console.get_run_acceptance(case_id, run_id)

    def inspect_run_artifacts(self, case_id: str, run_id: str) -> dict[str, Any]:
        return self.run_console.inspect_run_artifacts(case_id, run_id)

    def build_evaluation_draft(
        self,
        case_id: str,
        run_id: str,
        request: ContentProductionEvaluationDraftRequest,
    ) -> dict[str, Any]:
        return self.run_console.build_evaluation_draft(case_id, run_id, request)

    def build_case_evaluation_draft(
        self,
        case_id: str,
        request: ContentProductionEvaluationDraftRequest,
    ) -> dict[str, Any]:
        return self.case_console.build_case_evaluation_draft(case_id, request)

    def record_run_evaluation(
        self,
        case_id: str,
        run_id: str,
        request: ContentProductionEvaluationRequest,
    ) -> dict[str, Any]:
        return self.run_console.record_run_evaluation(case_id, run_id, request)

    def record_case_evaluation(
        self,
        case_id: str,
        request: ContentProductionEvaluationRequest,
    ) -> dict[str, Any]:
        return self.case_console.record_case_evaluation(case_id, request)

    def get_run(self, case_id: str, run_id: str) -> dict[str, Any]:
        return self.run_console.get_run(case_id, run_id)

    def get_artifact_file(self, case_id: str, run_id: str, artifact_name: str) -> Path:
        return self.run_console.get_artifact_file(case_id, run_id, artifact_name)

    def get_run_export(self, case_id: str, run_id: str, *, include_inputs: bool = False) -> dict[str, Any]:
        return self.run_console.get_run_export(case_id, run_id, include_inputs=include_inputs)
