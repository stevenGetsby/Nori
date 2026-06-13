"""Content-production experiment console service."""
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
    build_content_production_evaluation_draft,
    build_content_production_run_export,
    compare_content_production_runs,
    content_production_case_compare,
    content_production_case_delivery,
    content_production_case_next_actions,
    content_production_case_timeline,
    content_production_experiment_overview,
    content_production_experiment_report,
    get_content_production_case_selection,
    get_content_production_case_selected_run,
    get_content_production_run_acceptance,
    inspect_content_production_run_artifacts,
    list_content_production_cases,
    list_content_production_run_evaluations,
    list_content_production_runs,
    promote_content_production_case_run,
    record_content_production_case_selection,
    record_content_production_run_evaluation,
    resolve_content_production_artifact_path,
    summarize_content_production_run,
)


class BackendContentProductionConsoleService:
    """Owns run/case review, reporting, artifact, and export operations."""

    def __init__(self, *, project_root: Path) -> None:
        self.project_root = Path(project_root)

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
        try:
            return get_content_production_case_selection(project_root=self.project_root, case_id=case_id)
        except FileNotFoundError as exc:
            raise ApiError(str(exc), status_code=404) from exc
        except ValueError as exc:
            raise ApiError(str(exc), status_code=400) from exc

    def record_case_selection(
        self,
        case_id: str,
        request: ContentProductionSelectionRequest,
    ) -> dict[str, Any]:
        try:
            return record_content_production_case_selection(
                project_root=self.project_root,
                case_id=case_id,
                selection=_model_data(request),
            )
        except FileNotFoundError as exc:
            raise ApiError(str(exc), status_code=404) from exc
        except ValueError as exc:
            raise ApiError(str(exc), status_code=400) from exc

    def promote_case_run(
        self,
        case_id: str,
        request: ContentProductionPromotionRequest,
    ) -> dict[str, Any]:
        try:
            return promote_content_production_case_run(
                project_root=self.project_root,
                case_id=case_id,
                promotion=_model_data(request),
            )
        except FileNotFoundError as exc:
            raise ApiError(str(exc), status_code=404) from exc
        except ValueError as exc:
            raise ApiError(str(exc), status_code=400) from exc

    def get_case_selected_run(
        self,
        *,
        case_id: str,
        fallback_to_best: bool = True,
    ) -> dict[str, Any]:
        try:
            return get_content_production_case_selected_run(
                project_root=self.project_root,
                case_id=case_id,
                fallback_to_best=fallback_to_best,
            )
        except FileNotFoundError as exc:
            raise ApiError(str(exc), status_code=404) from exc
        except ValueError as exc:
            raise ApiError(str(exc), status_code=400) from exc

    def case_compare(self, *, case_id: str, limit: int = 500) -> dict[str, Any]:
        try:
            return content_production_case_compare(project_root=self.project_root, case_id=case_id, limit=limit)
        except FileNotFoundError as exc:
            raise ApiError(str(exc), status_code=404) from exc
        except ValueError as exc:
            raise ApiError(str(exc), status_code=400) from exc

    def case_next_actions(self, *, case_id: str, limit: int = 500) -> dict[str, Any]:
        try:
            return content_production_case_next_actions(project_root=self.project_root, case_id=case_id, limit=limit)
        except FileNotFoundError as exc:
            raise ApiError(str(exc), status_code=404) from exc
        except ValueError as exc:
            raise ApiError(str(exc), status_code=400) from exc

    def case_delivery(self, *, case_id: str, allow_unpromoted: bool = False) -> dict[str, Any]:
        try:
            return content_production_case_delivery(
                project_root=self.project_root,
                case_id=case_id,
                allow_unpromoted=allow_unpromoted,
            )
        except FileNotFoundError as exc:
            raise ApiError(str(exc), status_code=404) from exc
        except ValueError as exc:
            raise ApiError(str(exc), status_code=400) from exc

    def case_timeline(self, *, case_id: str, limit: int = 200) -> dict[str, Any]:
        try:
            return content_production_case_timeline(project_root=self.project_root, case_id=case_id, limit=limit)
        except FileNotFoundError as exc:
            raise ApiError(str(exc), status_code=404) from exc
        except ValueError as exc:
            raise ApiError(str(exc), status_code=400) from exc

    def get_case_export(self, case_id: str) -> dict[str, Any]:
        try:
            return build_content_production_case_export(project_root=self.project_root, case_id=case_id)
        except FileNotFoundError as exc:
            raise ApiError(str(exc), status_code=404) from exc
        except ValueError as exc:
            raise ApiError(str(exc), status_code=400) from exc

    def get_case_delivery_export(self, case_id: str, *, allow_unready: bool = False) -> dict[str, Any]:
        try:
            return build_content_production_case_delivery_export(
                project_root=self.project_root,
                case_id=case_id,
                allow_unready=allow_unready,
            )
        except FileNotFoundError as exc:
            raise ApiError(str(exc), status_code=404) from exc
        except ValueError as exc:
            raise ApiError(str(exc), status_code=400) from exc

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
        try:
            return compare_content_production_runs(
                project_root=self.project_root,
                case_id=case_id,
                run_ids=run_ids,
            )
        except FileNotFoundError as exc:
            raise ApiError(str(exc), status_code=404) from exc
        except ValueError as exc:
            raise ApiError(str(exc), status_code=400) from exc

    def list_run_evaluations(self, case_id: str, run_id: str) -> dict[str, Any]:
        try:
            return list_content_production_run_evaluations(
                project_root=self.project_root,
                case_id=case_id,
                run_id=run_id,
            )
        except FileNotFoundError as exc:
            raise ApiError(str(exc), status_code=404) from exc

    def get_run_acceptance(self, case_id: str, run_id: str) -> dict[str, Any]:
        try:
            return get_content_production_run_acceptance(
                project_root=self.project_root,
                case_id=case_id,
                run_id=run_id,
            )
        except FileNotFoundError as exc:
            raise ApiError(str(exc), status_code=404) from exc

    def inspect_run_artifacts(self, case_id: str, run_id: str) -> dict[str, Any]:
        try:
            return inspect_content_production_run_artifacts(
                project_root=self.project_root,
                case_id=case_id,
                run_id=run_id,
            )
        except FileNotFoundError as exc:
            raise ApiError(str(exc), status_code=404) from exc
        except ValueError as exc:
            raise ApiError(str(exc), status_code=400) from exc

    def build_evaluation_draft(
        self,
        case_id: str,
        run_id: str,
        request: ContentProductionEvaluationDraftRequest,
    ) -> dict[str, Any]:
        try:
            return build_content_production_evaluation_draft(
                project_root=self.project_root,
                case_id=case_id,
                run_id=run_id,
                reviewer=request.reviewer,
                persist=request.persist,
                metadata=dict(request.metadata),
            )
        except FileNotFoundError as exc:
            raise ApiError(str(exc), status_code=404) from exc
        except ValueError as exc:
            raise ApiError(str(exc), status_code=400) from exc

    def build_case_evaluation_draft(
        self,
        case_id: str,
        request: ContentProductionEvaluationDraftRequest,
    ) -> dict[str, Any]:
        run_id, source = self._resolve_case_run_id(case_id, run_id=request.run_id)
        data = self.build_evaluation_draft(case_id, run_id, request)
        data.setdefault("source", "case_evaluation_draft")
        data.setdefault("source_case_id", case_id)
        data.setdefault("source_run_id", run_id)
        data.setdefault("source_run_selector", source)
        return data

    def record_run_evaluation(
        self,
        case_id: str,
        run_id: str,
        request: ContentProductionEvaluationRequest,
    ) -> dict[str, Any]:
        try:
            return record_content_production_run_evaluation(
                project_root=self.project_root,
                case_id=case_id,
                run_id=run_id,
                evaluation=_model_data(request),
            )
        except FileNotFoundError as exc:
            raise ApiError(str(exc), status_code=404) from exc
        except ValueError as exc:
            raise ApiError(str(exc), status_code=400) from exc

    def record_case_evaluation(
        self,
        case_id: str,
        request: ContentProductionEvaluationRequest,
    ) -> dict[str, Any]:
        run_id, source = self._resolve_case_run_id(case_id, run_id=request.run_id)
        data = self.record_run_evaluation(case_id, run_id, request)
        data.setdefault("source", "case_evaluation")
        data.setdefault("source_case_id", case_id)
        data.setdefault("source_run_id", run_id)
        data.setdefault("source_run_selector", source)
        return data

    def get_run(self, case_id: str, run_id: str) -> dict[str, Any]:
        result = summarize_content_production_run(project_root=self.project_root, case_id=case_id, run_id=run_id)
        if not result:
            raise ApiError(f"content-production run not found: {case_id}/{run_id}", status_code=404)
        return result

    def get_artifact_file(self, case_id: str, run_id: str, artifact_name: str) -> Path:
        try:
            return resolve_content_production_artifact_path(
                project_root=self.project_root,
                case_id=case_id,
                run_id=run_id,
                artifact_name=artifact_name,
            )
        except FileNotFoundError as exc:
            raise ApiError(str(exc), status_code=404) from exc
        except ValueError as exc:
            raise ApiError(str(exc), status_code=400) from exc

    def get_run_export(self, case_id: str, run_id: str, *, include_inputs: bool = False) -> dict[str, Any]:
        try:
            return build_content_production_run_export(
                project_root=self.project_root,
                case_id=case_id,
                run_id=run_id,
                include_inputs=include_inputs,
            )
        except FileNotFoundError as exc:
            raise ApiError(str(exc), status_code=404) from exc

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
        try:
            selected = get_content_production_case_selected_run(
                project_root=self.project_root,
                case_id=case_id,
                fallback_to_best=True,
            )
        except FileNotFoundError as exc:
            raise ApiError(str(exc), status_code=404) from exc
        except ValueError as exc:
            raise ApiError(str(exc), status_code=400) from exc
        resolved_run_id = str(selected.get("run_id") or "")
        if not resolved_run_id:
            raise ApiError(f"no target run found for case: {case_id}", status_code=404)
        return resolved_run_id, str(selected.get("source") or "")


def _model_data(model: Any) -> dict[str, Any]:
    if hasattr(model, "model_dump"):
        return model.model_dump()
    return model.dict()
