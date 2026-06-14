"""Structural service contracts consumed by FastAPI route modules."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Protocol


class CatalogServiceProtocol(Protocol):
    def list_capabilities(self) -> dict[str, Any]: ...

    def list_workflows(self) -> dict[str, Any]: ...

    def resolve_workflow(self, request: Any) -> dict[str, Any]: ...

    def get_workflow(self, workflow_id: str) -> dict[str, Any]: ...

    def content_options(self) -> dict[str, Any]: ...

    def content_option_group(self, group_id: str) -> dict[str, Any]: ...

    def content_actions(self) -> dict[str, Any]: ...

    def content_action(self, action_id: str) -> dict[str, Any]: ...

    def plan_content_generation(self, request: Any) -> dict[str, Any]: ...


class ContentProductionAdminServiceProtocol(Protocol):
    def experiment_readiness(self) -> dict[str, Any]: ...

    def content_production_diagnostics(self) -> dict[str, Any]: ...

    def content_production_experiment_workbench(
        self,
        *,
        case_id: str,
        limit: int,
        include_diagnostics: bool,
    ) -> dict[str, Any]: ...


class ContentProductionConsoleServiceProtocol(Protocol):
    def experiment_overview(self, *, case_id: str, limit: int) -> dict[str, Any]: ...

    def experiment_report(self, *, case_id: str, limit: int) -> dict[str, Any]: ...

    def list_cases(self) -> dict[str, Any]: ...

    def get_case_selection(self, case_id: str) -> dict[str, Any]: ...

    def record_case_selection(self, case_id: str, request: Any) -> dict[str, Any]: ...

    def promote_case_run(self, case_id: str, request: Any) -> dict[str, Any]: ...

    def build_case_evaluation_draft(self, case_id: str, request: Any) -> dict[str, Any]: ...

    def record_case_evaluation(self, case_id: str, request: Any) -> dict[str, Any]: ...

    def get_case_selected_run(self, *, case_id: str, fallback_to_best: bool) -> dict[str, Any]: ...

    def case_compare(self, *, case_id: str, limit: int) -> dict[str, Any]: ...

    def case_next_actions(self, *, case_id: str, limit: int) -> dict[str, Any]: ...

    def case_delivery(self, *, case_id: str, allow_unpromoted: bool) -> dict[str, Any]: ...

    def get_case_delivery_export(self, case_id: str, *, allow_unready: bool) -> dict[str, Any]: ...

    def case_timeline(self, *, case_id: str, limit: int) -> dict[str, Any]: ...

    def get_case_export(self, case_id: str) -> dict[str, Any]: ...

    def list_runs(
        self,
        *,
        case_id: str,
        status: str,
        proof_status: str,
        reference_status: str,
        evaluation_status: str,
        search: str,
        limit: int,
        offset: int,
    ) -> dict[str, Any]: ...

    def compare_runs(self, *, case_id: str, run_ids: list[str]) -> dict[str, Any]: ...

    def get_run(self, case_id: str, run_id: str) -> dict[str, Any]: ...

    def get_run_acceptance(self, case_id: str, run_id: str) -> dict[str, Any]: ...

    def list_run_evaluations(self, case_id: str, run_id: str) -> dict[str, Any]: ...

    def build_evaluation_draft(self, case_id: str, run_id: str, request: Any) -> dict[str, Any]: ...

    def record_run_evaluation(self, case_id: str, run_id: str, request: Any) -> dict[str, Any]: ...

    def get_run_export(self, case_id: str, run_id: str, *, include_inputs: bool) -> dict[str, Any]: ...

    def inspect_run_artifacts(self, case_id: str, run_id: str) -> dict[str, Any]: ...

    def get_artifact_file(self, case_id: str, run_id: str, artifact_name: str) -> Path: ...


class ContentProductionRunServiceProtocol(Protocol):
    def content_production_run_template(self, **kwargs: Any) -> dict[str, Any]: ...

    def run_content_production(self, request: Any) -> dict[str, Any]: ...

    def preflight_content_production_run(self, request: Any) -> dict[str, Any]: ...

    def replay_content_production_case(self, case_id: str, request: Any) -> dict[str, Any]: ...

    def replay_content_production_run(self, case_id: str, run_id: str, request: Any) -> dict[str, Any]: ...


class ExperimentJobServiceProtocol(Protocol):
    def list_experiment_jobs(
        self,
        *,
        status: str,
        session_id: str,
        case_id: str,
        job_type: str,
    ) -> dict[str, Any]: ...

    def get_experiment_job(self, job_id: str) -> dict[str, Any]: ...

    def cancel_experiment_job(self, job_id: str, request: Any) -> dict[str, Any]: ...


class ReferenceImageServiceProtocol(Protocol):
    def check_reference_publish(self, request: Any) -> dict[str, Any]: ...

    def check_reference_image_generation(self, request: Any) -> dict[str, Any]: ...

    def publish_session_asset_references(self, session_id: str, request: Any) -> dict[str, Any]: ...

    def check_session_reference_image_generation(self, session_id: str, request: Any) -> dict[str, Any]: ...


class SessionAssetServiceProtocol(Protocol):
    def list_session_assets(self, session_id: str) -> dict[str, Any]: ...

    def get_session_asset_file(self, session_id: str, asset_id: str) -> Path: ...

    def upload_session_assets(
        self,
        session_id: str,
        files: list[Any],
        *,
        task_id: str,
        usage: str,
        metadata_json: str,
    ) -> dict[str, Any]: ...

    def list_sessions(self) -> dict[str, Any]: ...

    def create_session(self, request: Any) -> dict[str, Any]: ...

    def get_session(self, session_id: str) -> dict[str, Any]: ...

    def append_turn(self, session_id: str, request: Any) -> dict[str, Any]: ...

    def start_task(self, session_id: str, request: Any) -> dict[str, Any]: ...


class SystemRouteServiceProtocol(Protocol):
    catalog_service: CatalogServiceProtocol

    def health(self) -> dict[str, str]: ...


class WorkflowRouteServiceProtocol(Protocol):
    catalog_service: CatalogServiceProtocol


class ContentGenerationRouteServiceProtocol(Protocol):
    catalog_service: CatalogServiceProtocol


class ContentProductionAdminRouteServiceProtocol(Protocol):
    admin_service: ContentProductionAdminServiceProtocol
    console_service: ContentProductionConsoleServiceProtocol
    reference_image_service: ReferenceImageServiceProtocol
    run_service: ContentProductionRunServiceProtocol


class ExperimentJobRouteServiceProtocol(Protocol):
    job_service: ExperimentJobServiceProtocol


class SessionRouteServiceProtocol(Protocol):
    session_asset_service: SessionAssetServiceProtocol
    reference_image_service: ReferenceImageServiceProtocol


class ContentProductionRunRouteServiceProtocol(Protocol):
    run_service: ContentProductionRunServiceProtocol
    console_service: ContentProductionConsoleServiceProtocol


class ContentProductionCaseRouteServiceProtocol(Protocol):
    run_service: ContentProductionRunServiceProtocol
    console_service: ContentProductionConsoleServiceProtocol


class RouteServiceRegistryProtocol(Protocol):
    system: SystemRouteServiceProtocol
    workflows: WorkflowRouteServiceProtocol
    content_generation: ContentGenerationRouteServiceProtocol
    content_production_admin: ContentProductionAdminRouteServiceProtocol
    experiment_jobs: ExperimentJobRouteServiceProtocol
    sessions: SessionRouteServiceProtocol
    content_production_runs: ContentProductionRunRouteServiceProtocol
    content_production_cases: ContentProductionCaseRouteServiceProtocol
