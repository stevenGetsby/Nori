from __future__ import annotations

import ast
import hashlib
import io
import importlib
import json
import time
import zipfile
from pathlib import Path
from threading import Event
from types import SimpleNamespace

from fastapi.testclient import TestClient

from nori.sessions import SessionEvent

from backend.experiments import ContentProductionExperimentRunner, ContentProductionRunFailed
from backend.jobs import InProcessExperimentJobStore
from backend import NoriBackend, create_app


ROOT = Path(__file__).resolve().parents[1]
APP_MODULE = importlib.import_module("backend.app")
SESSION_ASSET_MODULE = importlib.import_module("backend.services.session_assets")
REFERENCE_IMAGE_MODULE = importlib.import_module("backend.services.reference_images")
CONTENT_RUN_MODULE = importlib.import_module("backend.services.content_production_runs")


def _file_sha256_for_test(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _json_sha256_for_test(value: object) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _fake_reference_readiness(*, oss_configured: bool) -> dict:
    return {
        "ready": True,
        "models": {
            "llm": {"ready": True},
            "vision": {"ready": True},
            "image": {"ready": True, "supports_reference_image": True, "provider_id": "relay"},
        },
        "reference_images": {
            "supports_reference_image": True,
            "provider_requires_public_urls": True,
            "oss_configured": oss_configured,
            "backend_public_url_configured": False,
            "backend_public_base_url": "",
            "local_upload_reference_ready": oss_configured,
            "strict_reference_mode_ready": oss_configured,
            "missing_oss_env": [] if oss_configured else ["NORI_OSS_BUCKET"],
        },
    }


def _fake_unready_model_readiness() -> dict:
    return {
        "ready": False,
        "models": {
            "llm": {"ready": True},
            "vision": {"ready": True},
            "image": {"ready": False, "error_type": "RuntimeError", "error": "missing image model"},
        },
        "reference_images": {
            "supports_reference_image": False,
            "provider_requires_public_urls": False,
            "oss_configured": False,
            "backend_public_url_configured": False,
            "backend_public_base_url": "",
            "local_upload_reference_ready": False,
            "strict_reference_mode_ready": False,
            "missing_oss_env": [],
        },
    }


def _project_runner(tmp_path: Path):
    return type("Runner", (), {"project_root": tmp_path, "top_notes_collector": None})()


def _failed_run_result(*, case_id: str, run_id: str, session_id: str, task_id: str) -> dict:
    return {
        "workflow_name": "content_production",
        "run_id": run_id,
        "run_dir": f"/tmp/{run_id}",
        "status": "failed",
        "session_id": session_id,
        "task_id": task_id,
        "asset_paths": [],
        "asset_ids": [],
        "artifact_paths": {"experiment_manifest.json": f"/tmp/{run_id}/experiment_manifest.json"},
        "cover_paths": [],
        "artifact_urls": {
            "experiment_manifest.json": (
                f"/workflows/content-production/runs/{case_id}/{run_id}/artifacts/experiment_manifest.json"
            )
        },
        "cover_urls": [],
        "input_manifest": {"case_id": case_id},
        "experiment_manifest": {
            "schema_version": 1,
            "experiment": {"case_id": case_id, "run_id": run_id, "status": "failed"},
            "error": {"type": "RuntimeError", "message": "image failed"},
        },
        "image_reference": {"status": "not_selected", "sent": False},
        "workflow_run": {"status": "failed", "session_id": session_id, "task_id": task_id},
    }


def test_backend_does_not_import_agent_implementation_modules():
    allowed_nori_import_roots = {
        "nori.core",
        "nori.core.llms",
        "nori.core.paths",
        "nori.sessions",
        "nori.storage",
        "nori.workflows.content_production",
    }
    for path in sorted((ROOT / "backend").rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        tree = ast.parse(path.read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("nori."):
                assert any(node.module == allowed for allowed in allowed_nori_import_roots), path
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.startswith("nori."):
                        assert any(alias.name == allowed for allowed in allowed_nori_import_roots), path


def test_fastapi_health_response_uses_shared_api_shape():
    client = TestClient(create_app())

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "code": 0,
        "message": "ok",
        "data": {
            "status": "ok",
            "service": "nori-backend",
            "runtime": "fastapi",
        },
    }


def test_fastapi_builtin_docs_and_openapi_are_served():
    client = TestClient(create_app())

    docs = client.get("/docs")
    spec = client.get("/openapi.json")

    assert docs.status_code == 200
    assert "text/html" in docs.headers["content-type"]
    assert "swagger-ui" in docs.text
    assert spec.status_code == 200
    data = spec.json()
    assert data["openapi"].startswith("3.")
    assert data["info"]["title"] == "Nori Backend API"
    assert "/sessions/{session_id}/tasks" in data["paths"]
    assert "/sessions/{session_id}/assets" in data["paths"]
    assert "/sessions/{session_id}/assets/publish-references" in data["paths"]
    assert "/sessions/{session_id}/assets/reference-image-generation-check" in data["paths"]
    assert "/experiments/readiness" in data["paths"]
    assert "/experiments/content-production/diagnostics" in data["paths"]
    assert "/experiments/content-production/reference-publish-check" in data["paths"]
    assert "/experiments/content-production/reference-image-generation-check" in data["paths"]
    assert "/experiments/jobs" in data["paths"]
    assert "/experiments/jobs/{job_id}" in data["paths"]
    assert "/experiments/jobs/{job_id}/cancel" in data["paths"]
    assert "/experiments/content-production/workbench" in data["paths"]
    assert "/experiments/content-production/run-template" in data["paths"]
    assert "get" in data["paths"]["/experiments/content-production/run-template"]
    assert "post" in data["paths"]["/experiments/content-production/run-template"]
    assert "/experiments/content-production/overview" in data["paths"]
    assert "/experiments/content-production/report" in data["paths"]
    assert "/experiments/content-production/cases" in data["paths"]
    assert "/experiments/content-production/cases/{case_id}/selection" in data["paths"]
    assert "/experiments/content-production/cases/{case_id}/promotion" in data["paths"]
    assert "/experiments/content-production/cases/{case_id}/replay" in data["paths"]
    assert "/experiments/content-production/cases/{case_id}/evaluations/draft" in data["paths"]
    assert "/experiments/content-production/cases/{case_id}/evaluations" in data["paths"]
    assert "/experiments/content-production/cases/{case_id}/delivery" in data["paths"]
    assert "/experiments/content-production/cases/{case_id}/delivery/export" in data["paths"]
    assert "/experiments/content-production/cases/{case_id}/selected-run" in data["paths"]
    assert "/experiments/content-production/cases/{case_id}/compare" in data["paths"]
    assert "/experiments/content-production/cases/{case_id}/next-actions" in data["paths"]
    assert "/experiments/content-production/cases/{case_id}/timeline" in data["paths"]
    assert "/experiments/content-production/cases/{case_id}/export" in data["paths"]
    assert "/content/generation/options" in data["paths"]
    assert "/workflows/resolve" in data["paths"]
    assert "/workflows/content-production/runs" in data["paths"]
    assert "/workflows/content-production/runs/preflight" in data["paths"]
    assert "/workflows/content-production/runs/compare" in data["paths"]
    assert "/workflows/content-production/runs/{case_id}/{run_id}" in data["paths"]
    assert "/workflows/content-production/runs/{case_id}/{run_id}/acceptance" in data["paths"]
    assert "/workflows/content-production/runs/{case_id}/{run_id}/evaluations" in data["paths"]
    assert "/workflows/content-production/runs/{case_id}/{run_id}/evaluations/draft" in data["paths"]
    assert "/workflows/content-production/runs/{case_id}/{run_id}/replay" in data["paths"]
    assert "/workflows/content-production/runs/{case_id}/{run_id}/export" in data["paths"]
    assert "/workflows/content-production/runs/{case_id}/{run_id}/artifacts/inspect" in data["paths"]


def test_fastapi_routes_are_registered_from_routing_module():
    routing = importlib.import_module("backend.routing")
    route_package = importlib.import_module("backend.routes")

    assert callable(routing.register_routes)
    assert callable(route_package.register_route_modules)
    assert [name for name, _builder in route_package.ROUTE_MODULES] == [
        "system",
        "workflows",
        "content_production_admin",
        "experiment_jobs",
        "content_generation",
        "sessions",
        "content_production_runs",
        "content_production_cases",
    ]
    builder_modules = {builder.__module__ for builder in route_package.ROUTE_BUILDERS}
    assert {
        "backend.routes.system",
        "backend.routes.workflows",
        "backend.routes.content_generation",
        "backend.routes.sessions",
        "backend.routes.experiment_jobs",
        "backend.routes.content_production_admin",
        "backend.routes.content_production_cases",
        "backend.routes.content_production_runs",
    } <= builder_modules

    routing_tree = ast.parse((ROOT / "backend" / "routing.py").read_text())
    route_decorator_calls = [
        node
        for node in ast.walk(routing_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr in {"delete", "get", "patch", "post", "put"}
    ]
    assert route_decorator_calls == []
    routing_source = (ROOT / "backend" / "routes" / "__init__.py").read_text(encoding="utf-8")
    assert 'getattr(service, "routes", service)' in routing_source
    assert "ROUTE_MODULES" in routing_source

    client = TestClient(create_app())

    paths = client.get("/openapi.json").json()["paths"]
    assert "/health" in paths
    assert "/sessions/{session_id}/assets" in paths
    assert "/workflows/content-production/runs" in paths


def test_backend_facade_composes_domain_services(tmp_path):
    services = importlib.import_module("backend.services")
    backend = NoriBackend(
        experiment_runner=_project_runner(tmp_path),
        reference_publisher=SimpleNamespace(),
    )

    assert isinstance(backend.service_bundle, services.BackendServiceBundle)
    assert backend.routes.system.catalog_service is backend.catalog_service
    assert backend.routes.workflows.catalog_service is backend.catalog_service
    assert backend.routes.content_generation.catalog_service is backend.catalog_service
    assert backend.routes.content_production_admin.admin_service is backend.content_production_admin
    assert backend.routes.content_production_admin.console_service is backend.content_production_console
    assert backend.routes.content_production_admin.reference_image_service is backend.reference_image_service
    assert backend.routes.content_production_admin.run_service is backend.content_production_run_service
    assert backend.routes.experiment_jobs.job_service is backend.experiment_job_service
    assert backend.routes.sessions.session_asset_service is backend.session_asset_service
    assert backend.routes.sessions.reference_image_service is backend.reference_image_service
    assert backend.routes.content_production_runs.run_service is backend.content_production_run_service
    assert backend.routes.content_production_runs.console_service is backend.content_production_console
    assert backend.routes.content_production_cases.run_service is backend.content_production_run_service
    assert backend.routes.content_production_cases.console_service is backend.content_production_console
    assert backend.service_bundle.project_root == tmp_path
    assert isinstance(backend.catalog_service, services.BackendCatalogService)
    assert isinstance(backend.content_production_admin, services.BackendContentProductionAdminService)
    assert isinstance(backend.content_production_console, services.BackendContentProductionConsoleService)
    assert isinstance(backend.content_production_run_service, services.BackendContentProductionRunService)
    assert isinstance(backend.experiment_job_service, services.BackendExperimentJobService)
    assert isinstance(backend.reference_image_service, services.BackendReferenceImageService)
    assert isinstance(backend.session_asset_service, services.BackendSessionAssetService)
    assert isinstance(backend.session_store, services.BackendSessionStore)
    assert backend.content_production_admin.project_root == tmp_path
    assert backend.content_production_console.project_root == tmp_path
    assert backend.session_store.session_manager is backend.session_manager
    assert backend.content_production_run_service.experiment_runner is backend.experiment_runner
    assert backend.content_production_run_service.job_store is backend.job_store
    assert backend.content_production_run_service.session_store is backend.session_store
    assert backend.content_production_run_service.session_manager is backend.session_manager
    assert backend.experiment_job_service.job_store is backend.job_store
    assert backend.experiment_job_service.session_store is backend.session_store
    assert backend.experiment_job_service.session_manager is backend.session_manager
    assert backend.reference_image_service.session_store is backend.session_store
    assert backend.reference_image_service.session_manager is backend.session_manager
    assert backend.reference_image_service.reference_publisher is backend.reference_publisher
    assert isinstance(
        backend.reference_image_service.publish_diagnostic,
        REFERENCE_IMAGE_MODULE.ReferencePublishDiagnostic,
    )
    assert isinstance(
        backend.reference_image_service.asset_publisher,
        REFERENCE_IMAGE_MODULE.SessionReferenceAssetPublisher,
    )
    assert isinstance(
        backend.reference_image_service.generation_checker,
        REFERENCE_IMAGE_MODULE.ReferenceImageGenerationChecker,
    )
    assert backend.reference_image_service.publish_diagnostic.reference_publisher is backend.reference_publisher
    assert backend.reference_image_service.asset_publisher.reference_publisher is backend.reference_publisher
    assert backend.session_asset_service.session_store is backend.session_store
    assert backend.session_asset_service.session_manager is backend.session_manager
    assert backend.session_asset_service.upload_root == tmp_path / "data" / "backend" / "uploads"

    app_source = (ROOT / "backend" / "app.py").read_text(encoding="utf-8")
    facade_source = (ROOT / "backend" / "facade.py").read_text(encoding="utf-8")
    route_services_source = (ROOT / "backend" / "route_services.py").read_text(encoding="utf-8")
    app_tree = ast.parse(app_source)
    experiment_imports = [
        alias.name
        for node in ast.walk(app_tree)
        if isinstance(node, ast.ImportFrom) and node.module == "experiments"
        for alias in node.names
    ]
    assert "class NoriBackend" not in app_source
    assert "class NoriBackend" in facade_source
    assert "BackendServiceBundle.create" in facade_source
    assert "BackendRouteServices.from_bundle" in facade_source
    assert "class ContentProductionRunRouteService" in route_services_source
    assert "class SessionRouteService" in route_services_source
    assert "def list_content_production_runs" not in facade_source
    assert "def upload_session_assets" not in facade_source
    assert "def list_content_production_runs" not in route_services_source
    assert "def upload_session_assets" not in route_services_source
    assert "BackendCatalogService" not in app_source
    assert "BackendCatalogService" not in facade_source
    assert "content_production_diagnostics" not in experiment_imports
    assert "content_production_experiment_workbench" not in experiment_imports
    assert "experiment_readiness" not in experiment_imports
    assert "BackendContentProductionRunService" not in app_source
    assert "BackendContentProductionRunService" not in facade_source
    assert "BackendReferenceImageService" not in app_source
    assert "BackendReferenceImageService" not in facade_source

    capability_ids = {row["capability_id"] for row in backend.list_capabilities()["capabilities"]}
    assert {"content_generation", "workflow_orchestration"} <= capability_ids


def test_content_production_preflight_policy_is_split_by_responsibility():
    run_source = (ROOT / "backend" / "services" / "content_production_runs.py").read_text(encoding="utf-8")
    compat_source = (ROOT / "backend" / "services" / "content_production_preflight.py").read_text(encoding="utf-8")
    checks_source = (ROOT / "backend" / "services" / "content_production_preflight_checks.py").read_text(encoding="utf-8")
    actions_source = (ROOT / "backend" / "services" / "content_production_preflight_actions.py").read_text(encoding="utf-8")
    summaries_source = (ROOT / "backend" / "services" / "content_production_preflight_summaries.py").read_text(encoding="utf-8")

    assert "from .content_production_preflight import" not in run_source
    assert "from .content_production_preflight_checks import" in run_source
    assert "from .content_production_preflight_actions import" in run_source
    assert "from .content_production_preflight_summaries import" in run_source
    assert "def _assert_content_production_run_gates" not in compat_source
    assert "def _content_production_preflight_actions" not in compat_source
    assert "def _asset_preflight_summary" not in compat_source
    assert "def _assert_content_production_run_gates" in checks_source
    assert "def _content_production_preflight_actions" in actions_source
    assert "def _asset_preflight_summary" in summaries_source


def test_content_production_run_service_delegates_template_payload_and_preparation_helpers():
    run_source = (ROOT / "backend" / "services" / "content_production_runs.py").read_text(encoding="utf-8")
    preparation_source = (
        ROOT / "backend" / "services" / "content_production_run_preparation.py"
    ).read_text(encoding="utf-8")
    template_source = (ROOT / "backend" / "services" / "content_production_run_templates.py").read_text(encoding="utf-8")
    payload_source = (ROOT / "backend" / "services" / "content_production_run_payloads.py").read_text(encoding="utf-8")

    assert "ContentProductionRunPreparer" in run_source
    assert "self.run_preparer.prepare" in run_source
    assert "def _prepare_content_production_run" not in run_source
    assert "select_assets" not in run_source
    assert "def prepare" in preparation_source
    assert "select_assets" in preparation_source
    assert "_assert_content_production_run_gates" in preparation_source
    assert "ContentProductionRunTemplateBuilder" in run_source
    assert "self.template_builder.build" in run_source
    assert "def content_production_run_template" in run_source
    assert "backend.content_production_run_template" not in run_source
    assert "def _model_data" not in run_source
    assert "def _replay_payload_with_overrides" not in run_source
    assert "class ContentProductionRunTemplateBuilder" in template_source
    assert "backend.content_production_run_template" in template_source
    assert "def _model_data" in payload_source
    assert "def _replay_payload_with_overrides" in payload_source


def test_experiment_job_store_delegates_presenter_helpers():
    jobs_source = (ROOT / "backend" / "jobs.py").read_text(encoding="utf-8")
    presenters_source = (ROOT / "backend" / "job_presenters.py").read_text(encoding="utf-8")
    run_service_source = (ROOT / "backend" / "services" / "content_production_runs.py").read_text(encoding="utf-8")

    assert "from .job_presenters import" in jobs_source
    assert "def enrich_content_run_result" not in jobs_source
    assert "def content_run_links" not in jobs_source
    assert "def _content_run_actions" not in jobs_source
    assert "def job_actions" not in jobs_source
    assert "def enrich_content_run_result" in presenters_source
    assert "def content_run_links" in presenters_source
    assert "def job_actions" in presenters_source
    assert "from ..job_presenters import enrich_content_run_result" in run_service_source
    assert "from ..jobs import InProcessExperimentJobStore" in run_service_source


def test_experiment_workbench_is_split_from_case_reports():
    package_source = (ROOT / "backend" / "experiments" / "__init__.py").read_text(encoding="utf-8")
    cases_source = (ROOT / "backend" / "experiments" / "cases.py").read_text(encoding="utf-8")
    workbench_source = (ROOT / "backend" / "experiments" / "workbench.py").read_text(encoding="utf-8")

    assert "from .workbench import content_production_experiment_workbench" in package_source
    assert "def content_production_experiment_workbench" not in cases_source
    assert "def _workbench_active_run_id" not in cases_source
    assert "def _workbench_case" not in cases_source
    assert "def _empty_workbench_case" not in cases_source
    assert "def _workbench_status" not in cases_source
    assert "def content_production_experiment_workbench" in workbench_source
    assert "content_production_diagnostics" in workbench_source
    assert "inspect_content_production_run_artifacts" in workbench_source
    assert "content_production_case_compare" in workbench_source
    assert "content_production_experiment_overview" in workbench_source


def test_experiment_case_comparisons_are_split_from_case_reports():
    package_source = (ROOT / "backend" / "experiments" / "__init__.py").read_text(encoding="utf-8")
    cases_source = (ROOT / "backend" / "experiments" / "cases.py").read_text(encoding="utf-8")
    report_source = (ROOT / "backend" / "experiments" / "case_reports.py").read_text(encoding="utf-8")
    comparison_source = (ROOT / "backend" / "experiments" / "comparisons.py").read_text(encoding="utf-8")
    workbench_source = (ROOT / "backend" / "experiments" / "workbench.py").read_text(encoding="utf-8")
    delivery_source = (ROOT / "backend" / "experiments" / "delivery.py").read_text(encoding="utf-8")

    assert "from .case_reports import content_production_experiment_report" in package_source
    assert "def content_production_experiment_report" not in cases_source
    assert "def _report_recommendations" not in cases_source
    assert "def content_production_experiment_report" in report_source
    assert "def _report_recommendations" in report_source
    assert "from .comparisons import content_production_case_compare" in package_source
    assert "def content_production_case_compare" not in cases_source
    assert "def _case_compare_candidate" not in cases_source
    assert "def content_production_case_compare" in comparison_source
    assert "def _case_compare_candidate" in comparison_source
    assert "from .case_reports import content_production_experiment_report" in comparison_source
    assert "from .comparisons import content_production_case_compare" in workbench_source
    assert "from .comparisons import content_production_case_compare" in delivery_source


def test_experiment_case_action_builders_are_split_from_action_orchestration():
    actions_source = (ROOT / "backend" / "experiments" / "actions.py").read_text(encoding="utf-8")
    builders_source = (ROOT / "backend" / "experiments" / "action_builders.py").read_text(encoding="utf-8")
    workbench_source = (ROOT / "backend" / "experiments" / "workbench.py").read_text(encoding="utf-8")

    assert "def content_production_case_next_actions" in actions_source
    assert "def _case_next_action_status" in actions_source
    assert "def _case_next_actions" in actions_source
    assert "from .action_builders import" in actions_source
    assert "def _reference_repair_payload" not in actions_source
    assert "def rerun_action" not in actions_source
    assert "def case_repair_actions" not in actions_source
    assert "def first_run_action" in builders_source
    assert "def case_review_actions" in builders_source
    assert "def case_repair_actions" in builders_source
    assert "def rerun_action" in builders_source
    assert "from .action_builders import first_run_action" in workbench_source
    assert "from .actions import _case_next_actions" not in workbench_source


def test_case_selection_payload_is_a_stable_selection_module_api():
    selection_source = (ROOT / "backend" / "experiments" / "selections.py").read_text(encoding="utf-8")
    dependent_modules = [
        "actions.py",
        "case_reports.py",
        "cases.py",
        "comparisons.py",
        "delivery.py",
    ]

    assert "def case_selection_payload" in selection_source
    assert "def _case_selection_payload" not in selection_source
    for module_name in dependent_modules:
        source = (ROOT / "backend" / "experiments" / module_name).read_text(encoding="utf-8")
        assert "from .selections import case_selection_payload" in source
        assert "_case_selection_payload" not in source


def test_experiment_artifact_exports_are_split_from_artifact_catalogs():
    package_source = (ROOT / "backend" / "experiments" / "__init__.py").read_text(encoding="utf-8")
    artifacts_source = (ROOT / "backend" / "experiments" / "artifacts.py").read_text(encoding="utf-8")
    exports_source = (ROOT / "backend" / "experiments" / "artifact_exports.py").read_text(encoding="utf-8")

    assert "from .artifact_exports import" in package_source
    assert "def build_content_production_run_export" not in artifacts_source
    assert "def build_content_production_case_export" not in artifacts_source
    assert "def build_content_production_case_delivery_export" not in artifacts_source
    assert "def build_content_production_run_export" in exports_source
    assert "def build_content_production_case_export" in exports_source
    assert "def build_content_production_case_delivery_export" in exports_source
    assert "def artifact_catalog_for_run" in artifacts_source
    assert "def inspect_content_production_run_artifacts" in artifacts_source
    assert "def resolve_content_production_artifact_path" in artifacts_source


def test_delivery_payloads_are_split_from_delivery_gate_and_exports():
    delivery_source = (ROOT / "backend" / "experiments" / "delivery.py").read_text(encoding="utf-8")
    payload_source = (ROOT / "backend" / "experiments" / "delivery_payloads.py").read_text(encoding="utf-8")
    exports_source = (ROOT / "backend" / "experiments" / "artifact_exports.py").read_text(encoding="utf-8")

    assert "def content_production_case_delivery" in delivery_source
    assert "def _case_delivery_status" in delivery_source
    assert "def case_delivery_payload" not in delivery_source
    assert "def delivery_review_evidence" not in delivery_source
    assert "def run_review_evidence" not in delivery_source
    assert "from .delivery_payloads import case_delivery_payload" in delivery_source
    assert "def case_delivery_payload" in payload_source
    assert "def delivery_review_evidence" in payload_source
    assert "def run_review_evidence" in payload_source
    assert "from .delivery import _delivery_review_evidence" not in exports_source
    assert "from .delivery import _run_review_evidence" not in exports_source
    assert "from .delivery_payloads import delivery_review_evidence, run_review_evidence" in exports_source


def test_image_reference_projections_are_split_from_artifact_catalogs():
    package_source = (ROOT / "backend" / "experiments" / "__init__.py").read_text(encoding="utf-8")
    artifacts_source = (ROOT / "backend" / "experiments" / "artifacts.py").read_text(encoding="utf-8")
    reference_source = (ROOT / "backend" / "experiments" / "reference_images.py").read_text(encoding="utf-8")
    runs_source = (ROOT / "backend" / "experiments" / "runs.py").read_text(encoding="utf-8")
    runner_manifest_source = (ROOT / "backend" / "experiments" / "runner_manifests.py").read_text(encoding="utf-8")

    assert "from .reference_images import image_reference_from_package, image_reference_summary" in package_source
    assert "def image_reference_summary" not in artifacts_source
    assert "def image_reference_from_package" not in artifacts_source
    assert "def _image_reference_trace_from_cover_result" not in artifacts_source
    assert "def _enrich_image_reference_trace" not in artifacts_source
    assert "from .reference_images import" in artifacts_source
    assert "def image_reference_summary" in reference_source
    assert "def image_reference_from_package" in reference_source
    assert "def _image_reference_trace_from_cover_result" in reference_source
    assert "def _enrich_image_reference_trace" in reference_source
    assert "from .reference_images import _enrich_image_reference_trace, image_reference_from_package" in runs_source
    assert "from .reference_images import _enrich_image_reference_trace, image_reference_summary" in runner_manifest_source


def test_experiment_runner_delegates_manifest_builders():
    runner_source = (ROOT / "backend" / "experiments" / "runner.py").read_text(encoding="utf-8")
    manifest_source = (ROOT / "backend" / "experiments" / "runner_manifests.py").read_text(encoding="utf-8")

    assert "from .runner_manifests import" in runner_source
    assert "def _run_response" not in runner_source
    assert "def _write_experiment_manifest" not in runner_source
    assert "def _experiment_manifest" not in runner_source
    assert "def _input_manifest" not in runner_source
    assert "def _replay_request" not in runner_source
    assert "def _manifest_asset" not in runner_source
    assert "def _reference_public_urls_by_path" not in runner_source
    assert "def _run_response" in manifest_source
    assert "def _write_experiment_manifest" in manifest_source
    assert "def _experiment_manifest" in manifest_source
    assert "def _input_manifest" in manifest_source
    assert "def _replay_request" in manifest_source
    assert "def _manifest_asset" in manifest_source
    assert "def _reference_public_urls_by_path" in manifest_source


def test_reference_acceptance_checks_are_split_from_acceptance_reports():
    package_source = (ROOT / "backend" / "experiments" / "__init__.py").read_text(encoding="utf-8")
    acceptance_source = (ROOT / "backend" / "experiments" / "acceptance.py").read_text(encoding="utf-8")
    proof_source = (ROOT / "backend" / "experiments" / "proofs.py").read_text(encoding="utf-8")
    reference_source = (ROOT / "backend" / "experiments" / "reference_acceptance.py").read_text(encoding="utf-8")
    runs_source = (ROOT / "backend" / "experiments" / "runs.py").read_text(encoding="utf-8")
    presenters_source = (ROOT / "backend" / "experiments" / "presenters.py").read_text(encoding="utf-8")

    assert "from .reference_acceptance import content_production_summary_reference_transfer" in package_source
    assert "def content_production_summary_reference_transfer" not in acceptance_source
    assert "from .proofs import content_production_run_proof" in package_source
    assert "def content_production_run_proof" not in acceptance_source
    assert "def _input_integrity_check" not in acceptance_source
    assert "_file_sha256" not in acceptance_source
    assert "def _acceptance_reference_check" not in acceptance_source
    assert "def _acceptance_reference_generation_check" not in acceptance_source
    assert "def _reference_transfer_check" not in acceptance_source
    assert "def _reference_generation_check_proof_check" not in acceptance_source
    assert "def _image_reference_check" not in acceptance_source
    assert "from .reference_acceptance import" in acceptance_source
    assert "def content_production_run_proof" in proof_source
    assert "def _input_integrity_check" in proof_source
    assert "from .reference_acceptance import" in proof_source
    assert "def content_production_summary_reference_transfer" in reference_source
    assert "def reference_transfer_proof_check" in reference_source
    assert "def reference_images_sent_proof_check" in reference_source
    assert "def acceptance_reference_check" in reference_source
    assert "def acceptance_reference_generation_check" in reference_source
    assert "from .proofs import content_production_run_proof" in runs_source
    assert "from .reference_acceptance import content_production_summary_reference_transfer" in runs_source
    assert "from .reference_acceptance import content_production_summary_reference_transfer" in presenters_source


def test_run_row_projection_is_split_from_run_summary_io():
    package_source = (ROOT / "backend" / "experiments" / "__init__.py").read_text(encoding="utf-8")
    runs_source = (ROOT / "backend" / "experiments" / "runs.py").read_text(encoding="utf-8")
    row_source = (ROOT / "backend" / "experiments" / "run_rows.py").read_text(encoding="utf-8")
    cases_source = (ROOT / "backend" / "experiments" / "cases.py").read_text(encoding="utf-8")
    presenters_source = (ROOT / "backend" / "experiments" / "presenters.py").read_text(encoding="utf-8")

    assert "from .run_rows import content_production_count_by" in package_source
    assert "def summarize_content_production_run" in runs_source
    assert "def content_production_comparison_run" not in runs_source
    assert "def _candidate_status" not in runs_source
    assert "def _asset_fingerprints" not in runs_source
    assert "def content_production_comparison_run" in row_source
    assert "def _candidate_status" in row_source
    assert "def content_production_value_diff" in row_source
    assert "from .run_rows import" in cases_source
    assert "from .run_rows import content_production_comparison_run" in presenters_source


def test_auto_review_gate_is_split_from_evaluation_persistence():
    reviews_source = (ROOT / "backend" / "experiments" / "reviews.py").read_text(encoding="utf-8")
    auto_reviews_source = (ROOT / "backend" / "experiments" / "auto_reviews.py").read_text(encoding="utf-8")
    run_health_source = (ROOT / "backend" / "experiments" / "run_health.py").read_text(encoding="utf-8")

    assert "from .auto_reviews import auto_evaluation_draft" in reviews_source
    assert "def _auto_evaluation_draft" not in reviews_source
    assert "def _run_health_review" not in reviews_source
    assert "def _evaluation_draft_from_reviews" not in reviews_source
    assert "visual_reference_review_for_evaluation" not in reviews_source
    assert "def auto_evaluation_draft" in auto_reviews_source
    assert "from .run_health import run_health_review" in auto_reviews_source
    assert "def _run_health_review" not in auto_reviews_source
    assert "def run_health_review" not in auto_reviews_source
    assert "def _evaluation_draft_from_reviews" in auto_reviews_source
    assert "visual_reference_review_for_evaluation" in auto_reviews_source
    assert "def run_health_review" in run_health_source
    assert "def _run_health_score" in run_health_source
    assert "def _run_health_suggestions" in run_health_source
    assert "def record_content_production_run_evaluation" in reviews_source
    assert "def evaluation_summary" in reviews_source
    assert "def _refresh_experiment_manifest_evaluations" in reviews_source


def test_reference_image_service_is_split_by_strategy_and_result_payloads():
    service_source = (ROOT / "backend" / "services" / "reference_images.py").read_text(encoding="utf-8")
    publishers_source = (ROOT / "backend" / "services" / "reference_image_publishers.py").read_text(encoding="utf-8")
    generation_source = (ROOT / "backend" / "services" / "reference_image_generation.py").read_text(encoding="utf-8")
    results_source = (ROOT / "backend" / "services" / "reference_image_results.py").read_text(encoding="utf-8")

    assert "class BackendReferenceImageService" in service_source
    assert "class ReferencePublishDiagnostic" not in service_source
    assert "class SessionReferenceAssetPublisher" not in service_source
    assert "class ReferenceImageGenerationChecker" not in service_source
    assert "def _reference_publish_check_result" not in service_source
    assert "def _session_reference_image_generation_check_result" not in service_source
    assert "class ReferencePublishDiagnostic" in publishers_source
    assert "class SessionReferenceAssetPublisher" in publishers_source
    assert "class ReferenceImageGenerationChecker" in generation_source
    assert "def _reference_publish_check_result" in results_source
    assert "def _session_reference_image_generation_check_result" in results_source


def test_fastapi_content_production_experiment_overview_route(tmp_path):
    run_dir = tmp_path / "cases" / "case1" / "runs" / "run1"
    covers_dir = run_dir / "covers"
    covers_dir.mkdir(parents=True)
    (covers_dir / "cover.png").write_bytes(b"png")
    (run_dir / "run.json").write_text('{"workflow":"content_production","status":"succeeded"}', encoding="utf-8")
    (run_dir / "workflow_run.json").write_text(
        '{"workflow_name":"content_production","status":"succeeded","started_at":"t1","finished_at":"t2"}',
        encoding="utf-8",
    )
    (run_dir / "content_package.json").write_text('{"package_id":"pkg"}', encoding="utf-8")
    (run_dir / "input_manifest.json").write_text(
        '{"brief":{"sha256":"brief"},"assets":[],"market_evidence":{"queries":["q"]},"run_options":{"require_image_references":false}}',
        encoding="utf-8",
    )
    (run_dir / "experiment_manifest.json").write_text(
        '{"schema_version":1,"experiment":{"case_id":"case1","run_id":"run1","status":"succeeded"},"reference_images":{"status":"not_selected","required":false,"sent":false},"artifacts":{"paths":{},"urls":{}}}',
        encoding="utf-8",
    )
    service = NoriBackend(experiment_runner=_project_runner(tmp_path))
    client = TestClient(create_app(backend=service))

    response = client.get("/experiments/content-production/overview?case_id=case1")

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["case_id"] == "case1"
    assert data["run_count"] == 1
    assert data["summary"]["ready_count"] == 1
    assert data["latest_runs"][0]["run_id"] == "run1"
    assert data["latest_runs"][0]["links"]["replay"] == "/workflows/content-production/runs/case1/run1/replay"

    report_response = client.get("/experiments/content-production/report?case_id=case1")

    assert report_response.status_code == 200
    report = report_response.json()["data"]
    assert report["case_id"] == "case1"
    assert report["run_count"] == 1
    assert report["best_run"]["run_id"] == "run1"
    assert report["latest_run"]["run_id"] == "run1"
    assert report["recommendations"]
    assert report["links"]["runs"] == "/workflows/content-production/runs?case_id=case1"

    selected_before_selection = client.get("/experiments/content-production/cases/case1/selected-run")
    no_fallback_selected = client.get(
        "/experiments/content-production/cases/case1/selected-run",
        params={"fallback_to_best": "false"},
    )

    assert selected_before_selection.status_code == 200
    assert selected_before_selection.json()["data"]["source"] == "best_run"
    assert selected_before_selection.json()["data"]["run_id"] == "run1"
    assert no_fallback_selected.status_code == 200
    assert no_fallback_selected.json()["data"]["resolved"] is False

    next_actions_before_selection = client.get("/experiments/content-production/cases/case1/next-actions")
    workbench_before_selection = client.get(
        "/experiments/content-production/workbench",
        params={"case_id": "case1", "include_diagnostics": "false"},
    )

    assert next_actions_before_selection.status_code == 200
    assert next_actions_before_selection.json()["data"]["status"] == "needs_selection"
    assert next_actions_before_selection.json()["data"]["primary_action"]["action_id"] == "select_best_run"
    assert next_actions_before_selection.json()["data"]["primary_action"]["payload"]["run_id"] == "run1"
    assert workbench_before_selection.status_code == 200
    workbench_before_data = workbench_before_selection.json()["data"]
    assert workbench_before_data["scope"] == "case"
    assert workbench_before_data["cases"][0]["primary_action"]["action_id"] == "select_best_run"
    assert workbench_before_data["primary_actions"][0]["case_id"] == "case1"
    assert workbench_before_data["case_compare"]["recommended_run_id"] == "run1"
    assert workbench_before_data["case_delivery"]["status"] == "needs_promotion"
    assert "not_promoted" in workbench_before_data["case_delivery"]["blocking_reasons"]
    assert workbench_before_data["case_delivery"]["run_id"] == "run1"
    assert workbench_before_data["active_run_id"] == "run1"
    assert workbench_before_data["active_run_artifacts"]["content_package"]["data"]["package_id"] == "pkg"
    assert workbench_before_data["links"]["case_delivery"] == "/experiments/content-production/cases/case1/delivery"
    assert workbench_before_data["links"]["case_delivery_export"] == (
        "/experiments/content-production/cases/case1/delivery/export"
    )
    assert workbench_before_data["links"]["case_replay"] == "/experiments/content-production/cases/case1/replay"
    assert workbench_before_data["links"]["case_evaluation_draft"] == (
        "/experiments/content-production/cases/case1/evaluations/draft"
    )
    assert workbench_before_data["links"]["case_evaluations"] == (
        "/experiments/content-production/cases/case1/evaluations"
    )
    assert workbench_before_data["links"]["active_run_artifacts"] == (
        "/workflows/content-production/runs/case1/run1/artifacts/inspect"
    )
    assert workbench_before_data["cases"][0]["links"]["case_evaluation_draft"] == (
        "/experiments/content-production/cases/case1/evaluations/draft"
    )
    assert workbench_before_data["cases"][0]["links"]["case_evaluations"] == (
        "/experiments/content-production/cases/case1/evaluations"
    )

    cases_response = client.get("/experiments/content-production/cases")

    assert cases_response.status_code == 200
    cases_data = cases_response.json()["data"]
    assert cases_data["case_count"] == 1
    assert cases_data["cases"][0]["case_id"] == "case1"
    assert cases_data["cases"][0]["latest_run_id"] == "run1"
    assert cases_data["cases"][0]["links"]["latest_export"] == "/workflows/content-production/runs/case1/run1/export"

    empty_selection = client.get("/experiments/content-production/cases/case1/selection")
    recorded_selection = client.post(
        "/experiments/content-production/cases/case1/selection",
        json={"run_id": "run1", "decision": "selected", "reviewer": "operator", "reason": "best available"},
    )
    loaded_selection = client.get("/experiments/content-production/cases/case1/selection")
    selected_after_selection = client.get("/experiments/content-production/cases/case1/selected-run")
    next_actions_after_selection = client.get("/experiments/content-production/cases/case1/next-actions")
    workbench_after_selection = client.get(
        "/experiments/content-production/workbench",
        params={"case_id": "case1", "include_diagnostics": "false"},
    )
    cases_after_selection = client.get("/experiments/content-production/cases")
    timeline = client.get("/experiments/content-production/cases/case1/timeline")
    case_export = client.get("/experiments/content-production/cases/case1/export")
    invalid_selection = client.post(
        "/experiments/content-production/cases/case1/selection",
        json={"run_id": "run1", "decision": "winner"},
    )

    assert empty_selection.status_code == 200
    assert empty_selection.json()["data"]["current"] == {}
    assert recorded_selection.status_code == 201
    assert recorded_selection.json()["data"]["selection"]["run_id"] == "run1"
    assert recorded_selection.json()["data"]["selection"]["decision"] == "selected"
    assert recorded_selection.json()["data"]["report"]["selection"]["run_id"] == "run1"
    assert loaded_selection.status_code == 200
    assert loaded_selection.json()["data"]["current"]["run_id"] == "run1"
    assert loaded_selection.json()["data"]["history"][0]["reason"] == "best available"
    assert selected_after_selection.status_code == 200
    assert selected_after_selection.json()["data"]["source"] == "selection"
    assert selected_after_selection.json()["data"]["run"]["run_id"] == "run1"
    assert selected_after_selection.json()["data"]["links"]["run_export"] == "/workflows/content-production/runs/case1/run1/export"
    assert next_actions_after_selection.status_code == 200
    assert next_actions_after_selection.json()["data"]["status"] == "needs_review"
    assert next_actions_after_selection.json()["data"]["primary_action"]["action_id"] == "draft_evaluation"
    assert workbench_after_selection.status_code == 200
    workbench_after_data = workbench_after_selection.json()["data"]
    assert workbench_after_data["cases"][0]["action_status"] == "needs_review"
    assert workbench_after_data["cases"][0]["primary_action"]["action_id"] == "draft_evaluation"
    assert workbench_after_data["case_compare"]["selected_run_id"] == "run1"
    assert workbench_after_data["case_delivery"]["status"] == "needs_promotion"
    assert workbench_after_data["active_run_artifacts"]["case_id"] == "case1"
    assert workbench_after_data["links"]["case_evaluation_draft"] == (
        "/experiments/content-production/cases/case1/evaluations/draft"
    )
    assert workbench_after_data["links"]["case_evaluations"] == (
        "/experiments/content-production/cases/case1/evaluations"
    )
    assert cases_after_selection.status_code == 200
    assert cases_after_selection.json()["data"]["cases"][0]["selected_run_id"] == "run1"
    assert cases_after_selection.json()["data"]["cases"][0]["selection_decision"] == "selected"
    assert cases_after_selection.json()["data"]["cases"][0]["links"]["selection"] == (
        "/experiments/content-production/cases/case1/selection"
    )
    assert timeline.status_code == 200
    timeline_data = timeline.json()["data"]
    assert timeline_data["case_id"] == "case1"
    assert timeline_data["summary"]["event_type_counts"]["selection_recorded"] == 1
    assert "selection_recorded" in {event["event_type"] for event in timeline_data["events"]}
    assert timeline_data["links"]["export"] == "/experiments/content-production/cases/case1/export"
    assert case_export.status_code == 200
    assert case_export.headers["content-type"] == "application/zip"
    assert 'filename="nori_content_production_case_case1.zip"' in case_export.headers["content-disposition"]
    with zipfile.ZipFile(io.BytesIO(case_export.content)) as archive:
        names = sorted(archive.namelist())
        manifest = json.loads(archive.read("case_export_manifest.json"))
        selection = json.loads(archive.read("case_selection.json"))
        assert "case_report.json" in names
        assert "case_summary.json" in names
        assert "runs/run1/summary.json" in names
    assert manifest["selected_run_id"] == "run1"
    assert selection["current"]["run_id"] == "run1"
    assert invalid_selection.status_code == 400
    assert "unsupported selection decision" in invalid_selection.json()["message"]


def test_fastapi_exports_content_production_run_bundle(tmp_path):
    run_dir = tmp_path / "cases" / "case1" / "runs" / "run1"
    covers_dir = run_dir / "covers"
    covers_dir.mkdir(parents=True)
    (run_dir / "input_manifest.json").write_text('{"input": true}', encoding="utf-8")
    (run_dir / "experiment_manifest.json").write_text('{"experiment": true}', encoding="utf-8")
    (run_dir / "summary.md").write_text("# Summary", encoding="utf-8")
    (run_dir / "private.txt").write_text("not exported", encoding="utf-8")
    (covers_dir / "cover.png").write_bytes(b"png")
    (covers_dir / "ignore.txt").write_text("not exported", encoding="utf-8")
    service = NoriBackend(experiment_runner=_project_runner(tmp_path))
    client = TestClient(create_app(backend=service))

    response = client.get("/workflows/content-production/runs/case1/run1/export")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/zip"
    assert 'filename="nori_content_production_case1_run1.zip"' in response.headers["content-disposition"]
    with zipfile.ZipFile(io.BytesIO(response.content)) as archive:
        names = sorted(archive.namelist())
        manifest = json.loads(archive.read("export_manifest.json"))
        artifact_inspection = json.loads(archive.read("artifact_inspection.json"))
        review_evidence = json.loads(archive.read("review_evidence.json"))
        assert names == [
            "artifact_inspection.json",
            "covers/cover.png",
            "experiment_manifest.json",
            "export_manifest.json",
            "input_manifest.json",
            "review_evidence.json",
            "run_summary.json",
            "summary.md",
        ]
        assert archive.read("covers/cover.png") == b"png"
        assert archive.read("summary.md") == b"# Summary"
    assert manifest["schema_version"] == 1
    assert manifest["case_id"] == "case1"
    assert manifest["run_id"] == "run1"
    assert manifest["include_inputs"] is False
    assert [row["path"] for row in manifest["files"]] == [
        "artifact_inspection.json",
        "review_evidence.json",
        "run_summary.json",
        "experiment_manifest.json",
        "input_manifest.json",
        "summary.md",
        "covers/cover.png",
    ]
    assert all(row.get("sha256") for row in manifest["files"] if row["path"].startswith(("covers/", "input_", "experiment_", "summary")))
    assert artifact_inspection["run_id"] == "run1"
    assert review_evidence["run_id"] == "run1"
    assert "visual_reference_review" in review_evidence


def test_fastapi_inspects_content_production_run_artifacts(tmp_path):
    run_dir = tmp_path / "cases" / "case1" / "runs" / "run1"
    covers_dir = run_dir / "covers"
    covers_dir.mkdir(parents=True)
    (covers_dir / "cover.png").write_bytes(b"png")
    (run_dir / "run.json").write_text('{"workflow":"content_production","status":"succeeded"}', encoding="utf-8")
    (run_dir / "workflow_run.json").write_text('{"status":"succeeded","stages":[]}', encoding="utf-8")
    (run_dir / "input_manifest.json").write_text(
        '{"brief":{"sha256":"brief"},"market_evidence":{"queries":["q"]},"run_options":{"require_image_references":false}}',
        encoding="utf-8",
    )
    (run_dir / "experiment_manifest.json").write_text(
        '{"schema_version":1,"experiment":{"case_id":"case1","run_id":"run1","status":"succeeded"},"reference_images":{"status":"not_selected","required":false,"sent":false}}',
        encoding="utf-8",
    )
    (run_dir / "replay_request.json").write_text('{"session_id":"session_1","brief_text":"brief"}', encoding="utf-8")
    (run_dir / "content_package.json").write_text('{"package_id":"pkg_1","title":"Ready package"}', encoding="utf-8")
    (run_dir / "summary.md").write_text("# Operator Summary", encoding="utf-8")
    service = NoriBackend(experiment_runner=_project_runner(tmp_path))
    client = TestClient(create_app(backend=service))

    response = client.get("/workflows/content-production/runs/case1/run1/artifacts/inspect")

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["case_id"] == "case1"
    assert data["run_id"] == "run1"
    assert data["content_package"]["available"] is True
    assert data["content_package"]["data"]["package_id"] == "pkg_1"
    assert data["content_package"]["json_summary"]["keys"] == ["package_id", "title"]
    assert data["manifests"]["input_manifest"]["data"]["market_evidence"]["queries"] == ["q"]
    assert data["manifests"]["experiment_manifest"]["data"]["schema_version"] == 1
    assert data["markdown"][0]["artifact_name"] == "summary.md"
    assert data["markdown"][0]["text"] == "# Operator Summary"
    assert data["covers"][0]["preview"] == {
        "kind": "image",
        "available": True,
        "url": "/workflows/content-production/runs/case1/run1/artifacts/covers/cover.png",
    }
    assert data["visual_reference_review"]["status"] == "not_applicable"
    assert data["visual_reference_review"]["cover_count"] == 1
    assert data["artifact_counts"] == {"total": 8, "json": 6, "markdown": 1, "covers": 1}
    assert data["missing_core_artifacts"] == []
    assert data["links"]["export"] == "/workflows/content-production/runs/case1/run1/export"


def test_fastapi_exports_content_production_run_bundle_with_input_assets(tmp_path):
    input_asset = tmp_path / "uploads" / "ref image.png"
    input_asset.parent.mkdir()
    input_asset.write_bytes(b"reference-image")
    missing_asset = tmp_path / "uploads" / "missing.png"
    run_dir = tmp_path / "cases" / "case1" / "runs" / "run1"
    run_dir.mkdir(parents=True)
    (run_dir / "input_manifest.json").write_text(
        json.dumps(
            {
                "assets": [
                    {"asset_id": "asset_ref", "filename": "ref image.png", "path": str(input_asset)},
                    {"asset_id": "asset_remote", "filename": "remote.png", "path": "https://cdn.nori.ai/ref.png"},
                    {"asset_id": "asset_missing", "filename": "missing.png", "path": str(missing_asset)},
                ]
            }
        ),
        encoding="utf-8",
    )
    (run_dir / "experiment_manifest.json").write_text('{"experiment": true}', encoding="utf-8")
    service = NoriBackend(experiment_runner=_project_runner(tmp_path))
    client = TestClient(create_app(backend=service))

    response = client.get("/workflows/content-production/runs/case1/run1/export", params={"include_inputs": "true"})

    assert response.status_code == 200
    with zipfile.ZipFile(io.BytesIO(response.content)) as archive:
        names = sorted(archive.namelist())
        manifest = json.loads(archive.read("export_manifest.json"))
        assert "inputs/asset_ref_ref_image.png" in names
        assert archive.read("inputs/asset_ref_ref_image.png") == b"reference-image"
    assert manifest["include_inputs"] is True
    assert "inputs/asset_ref_ref_image.png" in [row["path"] for row in manifest["files"]]
    assert manifest["skipped_inputs"] == [
        {"asset_id": "asset_remote", "path": "https://cdn.nori.ai/ref.png", "reason": "remote_url"},
        {"asset_id": "asset_missing", "path": str(missing_asset), "reason": "missing_file"},
    ]


def test_fastapi_export_content_production_run_reports_missing_run(tmp_path):
    service = NoriBackend(experiment_runner=_project_runner(tmp_path))
    client = TestClient(create_app(backend=service))

    response = client.get("/workflows/content-production/runs/case1/missing/export")

    assert response.status_code == 404
    assert response.json()["message"] == "content-production run not found: case1/missing"


def test_fastapi_session_lifecycle_routes_to_nori_session_manager(tmp_path):
    service = NoriBackend(experiment_runner=_project_runner(tmp_path))
    client = TestClient(create_app(backend=service))

    created = client.post(
        "/sessions",
        json={"user_id": "u1", "profile_id": "p1", "metadata": {"source": "web"}},
    )
    session = created.json()["data"]
    session_id = session["session_id"]

    turn = client.post(f"/sessions/{session_id}/turns", json={"role": "user", "content": "生成一篇小红书"})
    task = client.post(
        f"/sessions/{session_id}/tasks",
        json={
            "goal": "生成一篇小红书内容",
            "workflow_name": "content-production",
            "acceptance": ["has package"],
        },
    )
    fetched = client.get(f"/sessions/{session_id}")

    assert created.status_code == 201
    assert turn.status_code == 201
    assert task.status_code == 201
    assert fetched.json()["data"]["user_id"] == "u1"
    assert fetched.json()["data"]["turns"][0]["content"] == "生成一篇小红书"
    assert fetched.json()["data"]["task_goals"][0]["workflow_name"] == "content-production"
    assert fetched.json()["data"]["events"][0]["event_type"] == "task_started"


def test_fastapi_uploads_session_image_assets(tmp_path):
    service = NoriBackend(upload_root=tmp_path / "uploads", experiment_runner=_project_runner(tmp_path))
    client = TestClient(create_app(backend=service))
    session = client.post("/sessions", json={"user_id": "u1"}).json()["data"]

    response = client.post(
        f"/sessions/{session['session_id']}/assets",
        files=[("files", ("ref.png", b"fake-png-bytes", "image/png"))],
        data={"usage": "cover", "metadata_json": '{"source":"test"}'},
    )
    listed = client.get(f"/sessions/{session['session_id']}/assets")

    assert response.status_code == 201
    asset = response.json()["data"]["assets"][0]
    assert asset["kind"] == "image"
    assert asset["usage"] == "cover"
    assert asset["metadata"] == {"source": "test"}
    assert asset["file_url"] == f"/sessions/{session['session_id']}/assets/{asset['asset_id']}/file"
    assert Path(asset["path"]).is_file()
    assert listed.json()["data"]["assets"][0]["asset_id"] == asset["asset_id"]
    downloaded = client.get(asset["file_url"])
    assert downloaded.status_code == 200
    assert downloaded.content == b"fake-png-bytes"


def test_fastapi_content_production_run_template_builds_launch_request(monkeypatch, tmp_path):
    monkeypatch.setattr(CONTENT_RUN_MODULE, "experiment_readiness", lambda **_kwargs: _fake_reference_readiness(oss_configured=False))
    service = NoriBackend(upload_root=tmp_path / "uploads", experiment_runner=_project_runner(tmp_path))
    client = TestClient(create_app(backend=service))

    empty = client.get(
        "/experiments/content-production/run-template",
        params={"case_id": "case_new", "require_image_references": "true"},
    )

    assert empty.status_code == 200
    empty_data = empty.json()["data"]
    assert empty_data["ready_for_preflight"] is False
    assert "session" in empty_data["missing_fields"]
    assert "goal_or_brief_text" in empty_data["missing_fields"]
    empty_actions = {row["action_id"]: row for row in empty_data["actions"]}
    assert empty_actions["create_session"]["method"] == "POST"
    assert empty_actions["create_session"]["href"] == "/sessions"
    assert empty_actions["create_session"]["payload"]["metadata"]["case_id"] == "case_new"
    assert empty_actions["add_brief"]["method"] == "POST"
    assert empty_actions["add_brief"]["href"] == "/experiments/content-production/run-template"
    assert empty_actions["add_brief"]["input_fields"] == ["goal", "brief_text"]
    assert empty_actions["attach_market_evidence"]["method"] == "POST"
    assert empty_actions["attach_market_evidence"]["input_fields"] == ["market_evidence"]
    assert empty_actions["upload_reference_assets"]["href"] == "/sessions/{session_id}/assets"

    session = client.post(
        "/sessions",
        json={
            "user_id": "u1",
            "metadata": {
                "case_id": "Holly",
                "brief_text": "请参考上传图片生成内容",
                "market_evidence": {"platform": "xhs", "queries": ["test"], "hot_notes": [], "insufficient": []},
            },
        },
    ).json()["data"]
    uploaded = client.post(
        f"/sessions/{session['session_id']}/assets",
        files=[("files", ("cover.png", b"fake-png-bytes", "image/png"))],
    ).json()["data"]["assets"][0]

    ready = client.get(
        "/experiments/content-production/run-template",
        params={
            "session_id": session["session_id"],
            "require_image_references": "true",
            "backend_public_base_url": "https://backend.nori.ai",
        },
    )

    data = ready.json()["data"]
    assert ready.status_code == 200
    assert data["ready_for_preflight"] is True
    assert data["request"]["case_id"] == "Holly"
    assert data["request"]["brief_text"] == "请参考上传图片生成内容"
    assert data["request"]["asset_ids"] == [uploaded["asset_id"]]
    assert data["reference_images"]["can_send_selected_references"] is True
    assert data["assets"]["provider_fetchable_count"] == 1
    assert data["actions"][0]["action_id"] == "run_preflight"
    assert data["actions"][0]["payload"]["session_id"] == session["session_id"]
    assert data["actions"][1]["action_id"] == "run_experiment"
    assert data["actions"][1]["href"] == "/workflows/content-production/runs"
    assert data["actions"][2]["action_id"] == "check_reference_image_generation"
    assert data["actions"][2]["href"] == (
        f"/sessions/{session['session_id']}/assets/reference-image-generation-check"
    )
    assert data["actions"][2]["payload"]["asset_ids"] == [uploaded["asset_id"]]
    assert data["actions"][2]["payload"]["backend_public_base_url"] == "https://backend.nori.ai"
    assert data["actions"][2]["payload"]["verify_reference_urls"] is False
    assert data["actions"][2]["payload"]["reference_url_probe_timeout"] == 3.0

    post_session = client.post("/sessions", json={"user_id": "u2"}).json()["data"]
    post_uploaded = client.post(
        f"/sessions/{post_session['session_id']}/assets",
        files=[("files", ("poster.png", b"fake-png-bytes", "image/png"))],
    ).json()["data"]["assets"][0]
    from_body = client.post(
        "/experiments/content-production/run-template",
        json={
            "session_id": post_session["session_id"],
            "case_id": "case_from_form",
            "case_title": "Form Case",
            "brief_text": "表单里正在编辑的 brief",
            "asset_ids": [post_uploaded["asset_id"]],
            "backend_public_base_url": "https://backend.nori.ai",
            "require_image_references": True,
            "market_evidence": {"platform": "xhs", "queries": ["form"], "hot_notes": [], "insufficient": []},
            "config": {"brand_name": "Holly"},
            "metadata": {"source": "web_form"},
        },
    )

    body_data = from_body.json()["data"]
    assert from_body.status_code == 200
    assert body_data["ready_for_preflight"] is True
    assert body_data["request"]["case_id"] == "case_from_form"
    assert body_data["request"]["case_title"] == "Form Case"
    assert body_data["request"]["market_evidence"]["queries"] == ["form"]
    assert body_data["request"]["config"] == {"brand_name": "Holly"}
    assert body_data["request"]["metadata"]["source"] == "web_form"
    assert body_data["request"]["asset_ids"] == [post_uploaded["asset_id"]]


def test_fastapi_publishes_session_asset_references_and_preflight_reuses_public_url(monkeypatch, tmp_path):
    monkeypatch.setattr(CONTENT_RUN_MODULE, "experiment_readiness", lambda **_kwargs: _fake_reference_readiness(oss_configured=False))

    class FakeReferencePublisher:
        def __init__(self):
            self.calls = []

        def publish_path(self, path, *, project="", session="", public_url_map=None):
            self.calls.append({"path": path, "project": project, "session": session, "public_url_map": dict(public_url_map or {})})
            return SimpleNamespace(
                public_url="https://cdn.nori.ai/ref.png",
                url="https://signed.nori.ai/ref.png",
                key="nori/reference/ref.png",
                uploaded=True,
                reason="uploaded",
            )

    publisher = FakeReferencePublisher()
    service = NoriBackend(upload_root=tmp_path / "uploads", experiment_runner=_project_runner(tmp_path), reference_publisher=publisher)
    client = TestClient(create_app(backend=service))
    session = client.post("/sessions", json={"user_id": "u1"}).json()["data"]
    uploaded = client.post(
        f"/sessions/{session['session_id']}/assets",
        files=[("files", ("cover.png", b"fake-png-bytes", "image/png"))],
    ).json()["data"]["assets"][0]

    published = client.post(
        f"/sessions/{session['session_id']}/assets/publish-references",
        json={"asset_ids": [uploaded["asset_id"]], "project": "Holly"},
    )
    preflight = client.post(
        "/workflows/content-production/runs/preflight",
        json={
            "session_id": session["session_id"],
            "brief_text": "请参考上传图片生成内容",
            "asset_ids": [uploaded["asset_id"]],
            "require_image_references": True,
            "market_evidence": {"platform": "xhs", "queries": ["test"], "hot_notes": [], "insufficient": []},
        },
    )

    asset_row = client.get(f"/sessions/{session['session_id']}").json()["data"]["metadata"]["assets"][0]
    assert published.status_code == 200
    assert published.json()["data"]["ready"] is True
    assert published.json()["data"]["published_count"] == 1
    assert published.json()["data"]["assets"][0]["public_reference_url"] == "https://cdn.nori.ai/ref.png"
    assert publisher.calls[0]["project"] == "Holly"
    assert publisher.calls[0]["session"] == session["session_id"]
    assert asset_row["public_reference_url"] == "https://cdn.nori.ai/ref.png"
    assert asset_row["reference_object_key"] == "nori/reference/ref.png"
    assert preflight.json()["data"]["ready"] is True
    assert preflight.json()["data"]["reference_images"]["can_send_selected_references"] is True
    assert preflight.json()["data"]["assets"]["items"][0]["provider_fetchable_url"] == "https://cdn.nori.ai/ref.png"
    assert preflight.json()["data"]["actions"][0]["action_id"] == "run_experiment"
    assert preflight.json()["data"]["actions"][0]["href"] == "/workflows/content-production/runs"
    assert preflight.json()["data"]["links"]["run"] == "/workflows/content-production/runs"


def test_fastapi_reference_publish_check_uses_backend_owned_test_image(tmp_path):
    class FakeReferencePublisher:
        def __init__(self):
            self.calls = []

        def publish_path(self, path, *, project="", session="", public_url_map=None):
            self.calls.append({"path": path, "project": project, "session": session})
            assert Path(path).name == "reference_check.png"
            assert Path(path).read_bytes().startswith(b"\x89PNG")
            return SimpleNamespace(
                public_url="https://cdn.nori.ai/reference_check.png",
                url="https://signed.nori.ai/reference_check.png",
                key="nori/reference/check.png",
                uploaded=True,
                reason="uploaded",
            )

    publisher = FakeReferencePublisher()
    service = NoriBackend(experiment_runner=_project_runner(tmp_path), reference_publisher=publisher)
    client = TestClient(create_app(backend=service))

    response = client.post(
        "/experiments/content-production/reference-publish-check",
        json={"project": "Holly", "session": "diagnostics", "metadata": {"source": "test"}},
    )

    data = response.json()["data"]
    assert response.status_code == 200
    assert data["ready"] is True
    assert data["provider_fetchable"] is True
    assert data["public_reference_url"] == "https://cdn.nori.ai/reference_check.png"
    assert data["object_key"] == "nori/reference/check.png"
    assert data["metadata"] == {"source": "test"}
    assert data["next_actions"][0]["action_id"] == "run_strict_preflight"
    assert publisher.calls[0]["project"] == "Holly"
    assert publisher.calls[0]["session"] == "diagnostics"


def test_fastapi_reference_publish_check_reports_disabled_publisher(tmp_path):
    class DisabledReferencePublisher:
        def publish_path(self, path, *, project="", session="", public_url_map=None):
            return SimpleNamespace(public_url="", url="", key="", uploaded=False, reason="local_bytes")

    service = NoriBackend(experiment_runner=_project_runner(tmp_path), reference_publisher=DisabledReferencePublisher())
    client = TestClient(create_app(backend=service))

    response = client.post("/experiments/content-production/reference-publish-check", json={})

    data = response.json()["data"]
    assert response.status_code == 200
    assert data["ready"] is False
    assert data["provider_fetchable"] is False
    assert data["reason"] == "local_bytes"
    assert data["next_actions"][0]["action_id"] == "configure_reference_publisher"


def test_fastapi_reference_image_generation_check_calls_image_model(monkeypatch, tmp_path):
    calls = []

    def fake_image(prompt, *, usage="image", size="", reference_images=None, **kwargs):
        calls.append({"prompt": prompt, "usage": usage, "size": size, "reference_images": list(reference_images or [])})
        return ["data:image/png;base64,AAAA"]

    monkeypatch.setattr(REFERENCE_IMAGE_MODULE.llms, "image", fake_image)
    service = NoriBackend(experiment_runner=_project_runner(tmp_path))
    client = TestClient(create_app(backend=service))

    response = client.post(
        "/experiments/content-production/reference-image-generation-check",
        json={
            "prompt": "draw a product photo using the reference",
            "reference_images": ["https://assets.nori.ai/ref.png"],
            "size": "1024x1024",
            "metadata": {"source": "test"},
        },
    )

    data = response.json()["data"]
    assert response.status_code == 200
    assert data["ready"] is True
    assert data["reason"] == "image_generation_succeeded"
    assert data["reference_count"] == 1
    assert data["provider_fetchable_count"] == 1
    assert data["image_count"] == 1
    assert data["metadata"] == {"source": "test"}
    assert calls == [
        {
            "prompt": "draw a product photo using the reference",
            "usage": "image",
            "size": "1024x1024",
            "reference_images": ["https://assets.nori.ai/ref.png"],
        }
    ]


def test_fastapi_reference_image_generation_check_rejects_invalid_reference_url(monkeypatch, tmp_path):
    def fake_image(*_args, **_kwargs):
        raise AssertionError("invalid reference URLs should not call the image model")

    monkeypatch.setattr(REFERENCE_IMAGE_MODULE.llms, "image", fake_image)
    service = NoriBackend(experiment_runner=_project_runner(tmp_path))
    client = TestClient(create_app(backend=service))

    response = client.post(
        "/experiments/content-production/reference-image-generation-check",
        json={"reference_images": ["https://backend.example.test/ref.png"]},
    )

    data = response.json()["data"]
    assert response.status_code == 200
    assert data["ready"] is False
    assert data["reason"] == "invalid_reference_images"
    assert data["provider_fetchable_count"] == 0
    assert data["next_actions"][0]["action_id"] == "publish_reference_assets"


def test_fastapi_reference_image_generation_check_reports_provider_error(monkeypatch, tmp_path):
    def fake_image(*_args, **_kwargs):
        raise RuntimeError("provider rejected reference_images")

    monkeypatch.setattr(REFERENCE_IMAGE_MODULE.llms, "image", fake_image)
    service = NoriBackend(experiment_runner=_project_runner(tmp_path))
    client = TestClient(create_app(backend=service))

    response = client.post(
        "/experiments/content-production/reference-image-generation-check",
        json={"reference_images": ["https://assets.nori.ai/ref.png"]},
    )

    data = response.json()["data"]
    assert response.status_code == 200
    assert data["ready"] is False
    assert data["reason"] == "image_generation_error"
    assert data["error_type"] == "RuntimeError"
    assert data["error"] == "provider rejected reference_images"
    assert data["next_actions"][0]["action_id"] == "inspect_image_model_config"


def test_fastapi_session_reference_image_generation_check_publishes_and_calls_image_model(monkeypatch, tmp_path):
    calls = []

    def fake_image(prompt, *, usage="image", size="", reference_images=None, **kwargs):
        calls.append({"prompt": prompt, "usage": usage, "size": size, "reference_images": list(reference_images or [])})
        return ["data:image/png;base64,AAAA"]

    class DisabledReferencePublisher:
        def publish_path(self, path, *, project="", session="", public_url_map=None):
            raise AssertionError("backend public URL publishing should not call the object store")

    monkeypatch.setattr(REFERENCE_IMAGE_MODULE.llms, "image", fake_image)
    service = NoriBackend(
        upload_root=tmp_path / "uploads",
        experiment_runner=_project_runner(tmp_path),
        reference_publisher=DisabledReferencePublisher(),
    )
    client = TestClient(create_app(backend=service))
    session = client.post("/sessions", json={"user_id": "u1", "metadata": {"project": "Holly"}}).json()["data"]
    uploaded = client.post(
        f"/sessions/{session['session_id']}/assets",
        files=[("files", ("cover.png", b"fake-png-bytes", "image/png"))],
    ).json()["data"]["assets"][0]

    response = client.post(
        f"/sessions/{session['session_id']}/assets/reference-image-generation-check",
        json={
            "asset_ids": [uploaded["asset_id"]],
            "backend_public_base_url": "https://backend.nori.ai",
            "prompt": "draw with selected session reference",
            "size": "1024x1024",
            "metadata": {"source": "test"},
        },
    )

    expected_url = f"https://backend.nori.ai/sessions/{session['session_id']}/assets/{uploaded['asset_id']}/file"
    data = response.json()["data"]
    assert response.status_code == 200
    assert data["ready"] is True
    assert data["reason"] == "image_generation_succeeded"
    assert data["published_count"] == 1
    assert data["provider_fetchable_reference_images"] == [expected_url]
    assert data["publish"]["assets"][0]["reason"] == "backend_public_base_url"
    assert data["generation"]["ready"] is True
    assert data["next_actions"][0]["action_id"] == "run_strict_preflight"
    events = client.get(f"/sessions/{session['session_id']}").json()["data"]["events"]
    recorded = [event for event in events if event["event_type"] == "reference_image_generation_checked"]
    assert len(recorded) == 1
    assert recorded[0]["payload"]["ready"] is True
    assert recorded[0]["payload"]["reason"] == "image_generation_succeeded"
    assert recorded[0]["payload"]["provider_fetchable_reference_images"] == [expected_url]
    assert recorded[0]["payload"]["generation"]["image_count"] == 1
    fetched = client.get(f"/sessions/{session['session_id']}").json()["data"]
    listed_assets = client.get(f"/sessions/{session['session_id']}/assets").json()["data"]
    template = client.get(
        "/experiments/content-production/run-template",
        params={
            "session_id": session["session_id"],
            "require_image_references": "true",
            "backend_public_base_url": "https://backend.nori.ai",
        },
    ).json()["data"]
    preflight = client.post(
        "/workflows/content-production/runs/preflight",
        json={
            "session_id": session["session_id"],
            "brief_text": "brief",
            "case_id": "Holly",
            "asset_ids": [uploaded["asset_id"]],
            "backend_public_base_url": "https://backend.nori.ai",
            "require_image_references": True,
            "market_evidence": {"platform": "xhs", "queries": ["test"], "hot_notes": [], "insufficient": []},
        },
    ).json()["data"]
    assert fetched["latest_reference_image_generation_check"]["reason"] == "image_generation_succeeded"
    assert listed_assets["latest_reference_image_generation_check"]["provider_fetchable_reference_images"] == [expected_url]
    assert template["reference_images"]["latest_check"]["generation"]["image_count"] == 1
    assert preflight["reference_images"]["latest_check"]["ready"] is True
    assert calls == [
        {
            "prompt": "draw with selected session reference",
            "usage": "image",
            "size": "1024x1024",
            "reference_images": [expected_url],
        }
    ]


def test_fastapi_session_reference_image_generation_check_requires_fetchable_urls(monkeypatch, tmp_path):
    def fake_image(*_args, **_kwargs):
        raise AssertionError("image model should not be called without provider-fetchable references")

    class DisabledReferencePublisher:
        def publish_path(self, path, *, project="", session="", public_url_map=None):
            return SimpleNamespace(public_url="", url="", key="", uploaded=False, reason="local_bytes")

    monkeypatch.setattr(REFERENCE_IMAGE_MODULE.llms, "image", fake_image)
    service = NoriBackend(
        upload_root=tmp_path / "uploads",
        experiment_runner=_project_runner(tmp_path),
        reference_publisher=DisabledReferencePublisher(),
    )
    client = TestClient(create_app(backend=service))
    session = client.post("/sessions", json={"user_id": "u1"}).json()["data"]
    uploaded = client.post(
        f"/sessions/{session['session_id']}/assets",
        files=[("files", ("cover.png", b"fake-png-bytes", "image/png"))],
    ).json()["data"]["assets"][0]

    response = client.post(
        f"/sessions/{session['session_id']}/assets/reference-image-generation-check",
        json={"asset_ids": [uploaded["asset_id"]]},
    )

    data = response.json()["data"]
    assert response.status_code == 200
    assert data["ready"] is False
    assert data["reason"] == "no_provider_fetchable_reference_images"
    assert data["provider_fetchable_count"] == 0
    assert data["publish"]["failed_count"] == 1
    assert data["generation"] == {}
    assert data["next_actions"][0]["action_id"] == "set_backend_public_base_url_or_configure_oss"
    events = client.get(f"/sessions/{session['session_id']}").json()["data"]["events"]
    recorded = [event for event in events if event["event_type"] == "reference_image_generation_checked"]
    assert len(recorded) == 1
    assert recorded[0]["payload"]["ready"] is False
    assert recorded[0]["payload"]["reason"] == "no_provider_fetchable_reference_images"
    assert recorded[0]["payload"]["failed_count"] == 1


def test_fastapi_session_reference_image_generation_check_probes_urls_before_image_model(monkeypatch, tmp_path):
    probe_calls = []

    def fake_image(*_args, **_kwargs):
        raise AssertionError("image model should not be called when reference URL probe fails")

    def fake_probe(url, *, timeout=3.0):
        probe_calls.append({"url": url, "timeout": timeout})
        return {
            "url": url,
            "reachable": False,
            "status_code": 502,
            "content_type": "",
            "error_type": "HTTPStatusError",
            "error": "HTTP status 502",
        }

    class DisabledReferencePublisher:
        def publish_path(self, path, *, project="", session="", public_url_map=None):
            raise AssertionError("backend public URL publishing should not call the object store")

    monkeypatch.setattr(REFERENCE_IMAGE_MODULE.llms, "image", fake_image)
    monkeypatch.setattr(SESSION_ASSET_MODULE, "probe_reference_url", fake_probe)
    service = NoriBackend(
        upload_root=tmp_path / "uploads",
        experiment_runner=_project_runner(tmp_path),
        reference_publisher=DisabledReferencePublisher(),
    )
    client = TestClient(create_app(backend=service))
    session = client.post("/sessions", json={"user_id": "u1"}).json()["data"]
    uploaded = client.post(
        f"/sessions/{session['session_id']}/assets",
        files=[("files", ("cover.png", b"fake-png-bytes", "image/png"))],
    ).json()["data"]["assets"][0]

    response = client.post(
        f"/sessions/{session['session_id']}/assets/reference-image-generation-check",
        json={
            "asset_ids": [uploaded["asset_id"]],
            "backend_public_base_url": "https://backend.nori.ai",
            "verify_reference_urls": True,
            "reference_url_probe_timeout": 0.5,
        },
    )

    expected_url = f"https://backend.nori.ai/sessions/{session['session_id']}/assets/{uploaded['asset_id']}/file"
    data = response.json()["data"]
    assert response.status_code == 200
    assert data["ready"] is False
    assert data["reason"] == "reference_url_probe_failed"
    assert data["provider_fetchable_reference_images"] == [expected_url]
    assert data["url_probe"]["enabled"] is True
    assert data["url_probe"]["passed"] is False
    assert data["url_probe"]["failed_count"] == 1
    assert data["generation"] == {}
    assert data["next_actions"][0]["action_id"] == "fix_reference_url_reachability"
    assert probe_calls == [{"url": expected_url, "timeout": 0.5}]
    events = client.get(f"/sessions/{session['session_id']}").json()["data"]["events"]
    recorded = [event for event in events if event["event_type"] == "reference_image_generation_checked"]
    assert len(recorded) == 1
    assert recorded[0]["payload"]["reason"] == "reference_url_probe_failed"
    assert recorded[0]["payload"]["url_probe"]["enabled"] is True
    assert recorded[0]["payload"]["url_probe"]["failed_count"] == 1


def test_fastapi_publish_session_asset_references_reports_unconfigured_publisher(tmp_path):
    class DisabledReferencePublisher:
        def publish_path(self, path, *, project="", session="", public_url_map=None):
            return SimpleNamespace(public_url="", url="", key="", uploaded=False, reason="local_bytes")

    service = NoriBackend(
        upload_root=tmp_path / "uploads",
        experiment_runner=_project_runner(tmp_path),
        reference_publisher=DisabledReferencePublisher(),
    )
    client = TestClient(create_app(backend=service))
    session = client.post("/sessions", json={"user_id": "u1"}).json()["data"]
    uploaded = client.post(
        f"/sessions/{session['session_id']}/assets",
        files=[("files", ("cover.png", b"fake-png-bytes", "image/png"))],
    ).json()["data"]["assets"][0]

    response = client.post(
        f"/sessions/{session['session_id']}/assets/publish-references",
        json={"asset_ids": [uploaded["asset_id"]]},
    )

    asset_row = client.get(f"/sessions/{session['session_id']}").json()["data"]["metadata"]["assets"][0]
    assert response.status_code == 200
    assert response.json()["data"]["ready"] is False
    assert response.json()["data"]["failed_count"] == 1
    assert response.json()["data"]["assets"][0]["reason"] == "local_bytes"
    assert "public_reference_url" not in asset_row


def test_fastapi_publish_session_asset_references_can_use_backend_public_base_url(tmp_path):
    class DisabledReferencePublisher:
        def publish_path(self, path, *, project="", session="", public_url_map=None):
            raise AssertionError("backend public URL publishing should not call the object store")

    service = NoriBackend(
        upload_root=tmp_path / "uploads",
        experiment_runner=_project_runner(tmp_path),
        reference_publisher=DisabledReferencePublisher(),
    )
    client = TestClient(create_app(backend=service))
    session = client.post("/sessions", json={"user_id": "u1"}).json()["data"]
    uploaded = client.post(
        f"/sessions/{session['session_id']}/assets",
        files=[("files", ("cover.png", b"fake-png-bytes", "image/png"))],
    ).json()["data"]["assets"][0]

    response = client.post(
        f"/sessions/{session['session_id']}/assets/publish-references",
        json={"asset_ids": [uploaded["asset_id"]], "backend_public_base_url": "https://backend.nori.ai"},
    )

    expected_url = f"https://backend.nori.ai/sessions/{session['session_id']}/assets/{uploaded['asset_id']}/file"
    asset_row = client.get(f"/sessions/{session['session_id']}").json()["data"]["metadata"]["assets"][0]
    assert response.status_code == 200
    assert response.json()["data"]["ready"] is True
    assert response.json()["data"]["published_count"] == 1
    assert response.json()["data"]["assets"][0]["public_reference_url"] == expected_url
    assert response.json()["data"]["assets"][0]["reason"] == "backend_public_base_url"
    assert asset_row["public_reference_url"] == expected_url
    assert asset_row["reference_publish_reason"] == "backend_public_base_url"


def test_fastapi_backend_restores_persisted_session_assets_after_restart(tmp_path):
    class FakeReferencePublisher:
        def publish_path(self, path, *, project="", session="", public_url_map=None):
            return SimpleNamespace(
                public_url="https://cdn.nori.ai/ref.png",
                url="https://signed.nori.ai/ref.png",
                key="nori/reference/ref.png",
                uploaded=True,
                reason="uploaded",
            )

    runner = type("Runner", (), {"project_root": tmp_path})()
    service = NoriBackend(upload_root=tmp_path / "uploads", experiment_runner=runner, reference_publisher=FakeReferencePublisher())
    client = TestClient(create_app(backend=service))
    session = client.post("/sessions", json={"user_id": "u1", "metadata": {"project": "Holly"}}).json()["data"]
    uploaded = client.post(
        f"/sessions/{session['session_id']}/assets",
        files=[("files", ("cover.png", b"fake-png-bytes", "image/png"))],
    ).json()["data"]["assets"][0]
    client.post(
        f"/sessions/{session['session_id']}/assets/publish-references",
        json={"asset_ids": [uploaded["asset_id"]]},
    )

    restarted = NoriBackend(upload_root=tmp_path / "uploads", experiment_runner=runner, reference_publisher=FakeReferencePublisher())
    restarted_client = TestClient(create_app(backend=restarted))
    fetched = restarted_client.get(f"/sessions/{session['session_id']}").json()["data"]
    assets = restarted_client.get(f"/sessions/{session['session_id']}/assets").json()["data"]["assets"]

    assert (tmp_path / "data" / "backend" / "sessions" / f"{session['session_id']}.json").is_file()
    assert fetched["user_id"] == "u1"
    assert fetched["metadata"]["project"] == "Holly"
    assert assets[0]["asset_id"] == uploaded["asset_id"]
    assert assets[0]["public_reference_url"] == "https://cdn.nori.ai/ref.png"
    assert assets[0]["file_url"] == f"/sessions/{session['session_id']}/assets/{uploaded['asset_id']}/file"


def test_fastapi_content_production_run_uses_uploaded_session_assets(monkeypatch, tmp_path):
    monkeypatch.setattr(CONTENT_RUN_MODULE, "experiment_readiness", lambda **_kwargs: _fake_reference_readiness(oss_configured=False))

    class FakeExperimentRunner:
        project_root = tmp_path

        def __init__(self):
            self.calls = []

        def run(self, request, *, session_id, task_id, asset_rows):
            self.calls.append({
                "request": dict(request),
                "session_id": session_id,
                "task_id": task_id,
                "asset_rows": [dict(row) for row in asset_rows],
            })
            return {
                "workflow_name": "content_production",
                "run_id": "run_fake",
                "run_dir": str(tmp_path / "run_fake"),
                "status": "succeeded",
                "session_id": session_id,
                "task_id": task_id,
                "asset_paths": [row["path"] for row in asset_rows],
                "asset_ids": [row["asset_id"] for row in asset_rows],
                "artifact_paths": {},
                "cover_paths": [],
                "image_reference": {"status": "not_selected", "sent": False},
                "workflow_run": {"status": "succeeded", "session_id": session_id, "task_id": task_id},
            }

    runner = FakeExperimentRunner()
    service = NoriBackend(upload_root=tmp_path / "uploads", experiment_runner=runner)
    client = TestClient(create_app(backend=service))
    session = client.post("/sessions", json={"user_id": "u1"}).json()["data"]
    uploaded = client.post(
        f"/sessions/{session['session_id']}/assets",
        files=[("files", ("cover.png", b"fake-png-bytes", "image/png"))],
    ).json()["data"]["assets"][0]

    response = client.post(
        "/workflows/content-production/runs",
        json={
            "session_id": session["session_id"],
            "goal": "用上传图片生成小红书图文",
            "brief_text": "请参考上传图片生成内容",
            "asset_ids": [uploaded["asset_id"]],
            "backend_public_base_url": "https://backend.nori.ai",
            "require_image_references": True,
            "market_evidence": {"platform": "xhs", "queries": ["test"], "hot_notes": [], "insufficient": []},
        },
    )

    assert response.status_code == 201
    data = response.json()["data"]
    assert data["status"] == "succeeded"
    assert data["asset_paths"] == [uploaded["path"]]
    assert runner.calls[0]["asset_rows"][0]["path"] == uploaded["path"]
    assert runner.calls[0]["asset_rows"][0]["public_reference_url"] == (
        f"https://backend.nori.ai/sessions/{session['session_id']}/assets/{uploaded['asset_id']}/file"
    )
    assert runner.calls[0]["request"]["require_image_references"] is True
    fetched = client.get(f"/sessions/{session['session_id']}").json()["data"]
    assert fetched["task_goals"][0]["status"] == "succeeded"
    assert fetched["events"][-1]["event_type"] == "workflow_run_finished"


def test_fastapi_backend_restores_completed_run_task_state_after_restart(tmp_path):
    class FakeExperimentRunner:
        project_root = tmp_path

        def run(self, request, *, session_id, task_id, asset_rows):
            return {
                "workflow_name": "content_production",
                "run_id": "run_persisted_session",
                "run_dir": str(tmp_path / "run_persisted_session"),
                "status": "succeeded",
                "session_id": session_id,
                "task_id": task_id,
                "asset_paths": [row["path"] for row in asset_rows],
                "asset_ids": [row["asset_id"] for row in asset_rows],
                "artifact_paths": {},
                "cover_paths": [],
                "image_reference": {"status": "not_selected", "sent": False},
                "workflow_run": {"status": "succeeded", "session_id": session_id, "task_id": task_id},
            }

    runner = FakeExperimentRunner()
    service = NoriBackend(upload_root=tmp_path / "uploads", experiment_runner=runner)
    client = TestClient(create_app(backend=service))
    session = client.post("/sessions", json={"user_id": "u1"}).json()["data"]

    response = client.post(
        "/workflows/content-production/runs",
        json={
            "session_id": session["session_id"],
            "goal": "生成小红书图文",
            "brief_text": "brief",
            "market_evidence": {"platform": "xhs", "queries": ["test"], "hot_notes": [], "insufficient": []},
        },
    )

    restarted = NoriBackend(upload_root=tmp_path / "uploads", experiment_runner=runner)
    restarted_client = TestClient(create_app(backend=restarted))
    fetched = restarted_client.get(f"/sessions/{session['session_id']}").json()["data"]

    assert response.status_code == 201
    assert fetched["task_goals"][0]["status"] == "succeeded"
    assert fetched["task_goals"][0]["task_id"] == response.json()["data"]["task_id"]
    assert fetched["events"][-1]["event_type"] == "workflow_run_finished"


def test_fastapi_content_production_preflight_reports_reference_not_ready_without_public_url(monkeypatch, tmp_path):
    monkeypatch.setattr(CONTENT_RUN_MODULE, "experiment_readiness", lambda **_kwargs: _fake_reference_readiness(oss_configured=False))
    service = NoriBackend(upload_root=tmp_path / "uploads", experiment_runner=_project_runner(tmp_path))
    client = TestClient(create_app(backend=service))
    session = client.post("/sessions", json={"user_id": "u1"}).json()["data"]
    uploaded = client.post(
        f"/sessions/{session['session_id']}/assets",
        files=[("files", ("cover.png", b"fake-png-bytes", "image/png"))],
    ).json()["data"]["assets"][0]

    response = client.post(
        "/workflows/content-production/runs/preflight",
        json={
            "session_id": session["session_id"],
            "brief_text": "请参考上传图片生成内容",
            "asset_ids": [uploaded["asset_id"]],
            "require_image_references": True,
            "market_evidence": {"platform": "xhs", "queries": ["test"], "hot_notes": [], "insufficient": []},
        },
    )

    data = response.json()["data"]
    checks = {row["name"]: row for row in data["checks"]}
    fetched = client.get(f"/sessions/{session['session_id']}").json()["data"]
    assert response.status_code == 200
    assert data["ready"] is False
    assert data["assets"]["selected_count"] == 1
    assert data["assets"]["provider_fetchable_count"] == 0
    assert data["reference_images"]["can_send_selected_references"] is False
    assert data["reference_images"]["strict_reference_mode_ready"] is False
    assert checks["reference_transfer"]["status"] == "failed"
    action_ids = {row["action_id"] for row in data["actions"]}
    assert {"publish_reference_assets", "set_backend_public_base_url"} <= action_ids
    publish_action = next(row for row in data["actions"] if row["action_id"] == "publish_reference_assets")
    assert publish_action["href"] == f"/sessions/{session['session_id']}/assets/publish-references"
    assert publish_action["payload"]["asset_ids"] == [uploaded["asset_id"]]
    assert data["links"]["run_template"] == "/experiments/content-production/run-template"
    assert fetched["task_goals"] == []


def test_fastapi_content_production_preflight_accepts_public_backend_asset_url(monkeypatch, tmp_path):
    monkeypatch.setattr(CONTENT_RUN_MODULE, "experiment_readiness", lambda **_kwargs: _fake_reference_readiness(oss_configured=False))
    service = NoriBackend(upload_root=tmp_path / "uploads", experiment_runner=_project_runner(tmp_path))
    client = TestClient(create_app(backend=service))
    session = client.post("/sessions", json={"user_id": "u1"}).json()["data"]
    uploaded = client.post(
        f"/sessions/{session['session_id']}/assets",
        files=[("files", ("cover.png", b"fake-png-bytes", "image/png"))],
    ).json()["data"]["assets"][0]

    response = client.post(
        "/workflows/content-production/runs/preflight",
        json={
            "session_id": session["session_id"],
            "brief_text": "请参考上传图片生成内容",
            "asset_ids": [uploaded["asset_id"]],
            "backend_public_base_url": "https://backend.nori.ai",
            "require_image_references": True,
            "market_evidence": {"platform": "xhs", "queries": ["test"], "hot_notes": [], "insufficient": []},
        },
    )

    data = response.json()["data"]
    checks = {row["name"]: row for row in data["checks"]}
    assert response.status_code == 200
    assert data["ready"] is True
    assert data["assets"]["provider_fetchable_count"] == 1
    assert data["assets"]["items"][0]["provider_fetchable_url"] == (
        f"https://backend.nori.ai/sessions/{session['session_id']}/assets/{uploaded['asset_id']}/file"
    )
    assert data["reference_images"]["can_send_selected_references"] is True
    assert checks["reference_transfer"]["status"] == "passed"
    actions = {row["action_id"]: row for row in data["actions"]}
    assert actions["run_experiment"]["href"] == "/workflows/content-production/runs"
    assert actions["run_experiment"]["payload"]["backend_public_base_url"] == "https://backend.nori.ai"
    assert actions["check_reference_image_generation"]["severity"] == "optional"
    assert actions["check_reference_image_generation"]["href"] == (
        f"/sessions/{session['session_id']}/assets/reference-image-generation-check"
    )
    assert actions["check_reference_image_generation"]["payload"]["asset_ids"] == [uploaded["asset_id"]]
    assert actions["check_reference_image_generation"]["payload"]["backend_public_base_url"] == "https://backend.nori.ai"
    assert actions["check_reference_image_generation"]["payload"]["verify_reference_urls"] is False
    assert actions["check_reference_image_generation"]["payload"]["reference_url_probe_timeout"] == 3.0


def test_fastapi_content_production_preflight_rejects_placeholder_backend_asset_url(monkeypatch, tmp_path):
    monkeypatch.setattr(CONTENT_RUN_MODULE, "experiment_readiness", lambda **_kwargs: _fake_reference_readiness(oss_configured=False))
    service = NoriBackend(upload_root=tmp_path / "uploads", experiment_runner=_project_runner(tmp_path))
    client = TestClient(create_app(backend=service))
    session = client.post("/sessions", json={"user_id": "u1"}).json()["data"]
    uploaded = client.post(
        f"/sessions/{session['session_id']}/assets",
        files=[("files", ("cover.png", b"fake-png-bytes", "image/png"))],
    ).json()["data"]["assets"][0]

    response = client.post(
        "/workflows/content-production/runs/preflight",
        json={
            "session_id": session["session_id"],
            "brief_text": "请参考上传图片生成内容",
            "asset_ids": [uploaded["asset_id"]],
            "backend_public_base_url": "https://backend.example.test",
            "require_image_references": True,
            "market_evidence": {"platform": "xhs", "queries": ["test"], "hot_notes": [], "insufficient": []},
        },
    )

    data = response.json()["data"]
    checks = {row["name"]: row for row in data["checks"]}
    action_ids = {row["action_id"] for row in data["actions"]}
    assert response.status_code == 200
    assert data["ready"] is False
    assert data["assets"]["provider_fetchable_count"] == 0
    assert data["assets"]["items"][0]["provider_fetchable_url"] == ""
    assert data["reference_images"]["can_send_selected_references"] is False
    assert checks["reference_transfer"]["status"] == "failed"
    assert {"publish_reference_assets", "set_backend_public_base_url"} <= action_ids
    publish_action = next(row for row in data["actions"] if row["action_id"] == "publish_reference_assets")
    assert publish_action["payload"]["asset_ids"] == [uploaded["asset_id"]]
    assert publish_action["payload"]["backend_public_base_url"] == "https://backend.example.test"


def test_fastapi_content_production_preflight_can_verify_reference_url_reachability(monkeypatch, tmp_path):
    monkeypatch.setattr(CONTENT_RUN_MODULE, "experiment_readiness", lambda **_kwargs: _fake_reference_readiness(oss_configured=False))
    probe_calls = []

    def fake_probe(url, *, timeout):
        probe_calls.append({"url": url, "timeout": timeout})
        return {
            "url": url,
            "reachable": True,
            "status_code": 200,
            "content_type": "image/png",
            "error_type": "",
            "error": "",
        }

    monkeypatch.setattr(SESSION_ASSET_MODULE, "probe_reference_url", fake_probe)
    service = NoriBackend(upload_root=tmp_path / "uploads", experiment_runner=_project_runner(tmp_path))
    client = TestClient(create_app(backend=service))
    session = client.post("/sessions", json={"user_id": "u1"}).json()["data"]
    uploaded = client.post(
        f"/sessions/{session['session_id']}/assets",
        files=[("files", ("cover.png", b"fake-png-bytes", "image/png"))],
    ).json()["data"]["assets"][0]

    response = client.post(
        "/workflows/content-production/runs/preflight",
        json={
            "session_id": session["session_id"],
            "brief_text": "请参考上传图片生成内容",
            "asset_ids": [uploaded["asset_id"]],
            "backend_public_base_url": "https://backend.nori.ai",
            "require_image_references": True,
            "verify_reference_urls": True,
            "reference_url_probe_timeout": 0.5,
            "market_evidence": {"platform": "xhs", "queries": ["test"], "hot_notes": [], "insufficient": []},
        },
    )

    data = response.json()["data"]
    checks = {row["name"]: row for row in data["checks"]}
    assert response.status_code == 200
    assert data["ready"] is True
    assert checks["reference_url_reachability"]["status"] == "passed"
    assert data["reference_images"]["url_probe"]["passed"] is True
    assert data["reference_images"]["url_probe"]["reachable_count"] == 1
    assert probe_calls == [
        {
            "url": f"https://backend.nori.ai/sessions/{session['session_id']}/assets/{uploaded['asset_id']}/file",
            "timeout": 0.5,
        }
    ]


def test_fastapi_content_production_run_rejects_unreachable_reference_url_before_task(monkeypatch, tmp_path):
    monkeypatch.setattr(CONTENT_RUN_MODULE, "experiment_readiness", lambda **_kwargs: _fake_reference_readiness(oss_configured=False))
    monkeypatch.setattr(
        SESSION_ASSET_MODULE,
        "probe_reference_url",
        lambda url, *, timeout: {
            "url": url,
            "reachable": False,
            "status_code": 404,
            "content_type": "",
            "error_type": "HTTPError",
            "error": "not found",
        },
    )

    class FakeExperimentRunner:
        project_root = tmp_path

        def __init__(self):
            self.calls = []

        def run(self, request, *, session_id, task_id, asset_rows):
            self.calls.append({"request": request, "session_id": session_id, "task_id": task_id, "asset_rows": asset_rows})
            raise AssertionError("runner should not be called when reference URLs are unreachable")

    runner = FakeExperimentRunner()
    service = NoriBackend(upload_root=tmp_path / "uploads", experiment_runner=runner)
    client = TestClient(create_app(backend=service))
    session = client.post("/sessions", json={"user_id": "u1"}).json()["data"]
    uploaded = client.post(
        f"/sessions/{session['session_id']}/assets",
        files=[("files", ("cover.png", b"fake-png-bytes", "image/png"))],
    ).json()["data"]["assets"][0]

    response = client.post(
        "/workflows/content-production/runs",
        json={
            "session_id": session["session_id"],
            "brief_text": "请参考上传图片生成内容",
            "asset_ids": [uploaded["asset_id"]],
            "backend_public_base_url": "https://backend.nori.ai",
            "require_image_references": True,
            "verify_reference_urls": True,
            "market_evidence": {"platform": "xhs", "queries": ["test"], "hot_notes": [], "insufficient": []},
        },
    )

    data = response.json()
    repair_actions = {row["action_id"]: row for row in data["data"]["actions"]}
    failed_checks = {row["name"] for row in data["data"]["checks"]}
    assert response.status_code == 400
    assert "reference_url_reachability" in failed_checks
    assert repair_actions["verify_reference_urls"]["payload"]["verify_reference_urls"] is True
    assert repair_actions["set_backend_public_base_url"]["input_fields"] == ["backend_public_base_url"]
    assert runner.calls == []


def test_fastapi_content_production_preflight_reports_missing_market_evidence(monkeypatch, tmp_path):
    monkeypatch.setattr(CONTENT_RUN_MODULE, "experiment_readiness", lambda **_kwargs: _fake_reference_readiness(oss_configured=True))
    service = NoriBackend(experiment_runner=_project_runner(tmp_path))
    client = TestClient(create_app(backend=service))
    session = client.post("/sessions", json={"user_id": "u1"}).json()["data"]

    response = client.post(
        "/workflows/content-production/runs/preflight",
        json={
            "session_id": session["session_id"],
            "brief_text": "生成小红书内容",
        },
    )

    data = response.json()["data"]
    checks = {row["name"]: row for row in data["checks"]}
    assert response.status_code == 200
    assert data["ready"] is False
    assert data["market_evidence"]["provided"] is False
    assert checks["market_evidence"]["status"] == "failed"
    assert data["actions"][0]["action_id"] == "attach_market_evidence"
    assert data["actions"][0]["href"] == "/experiments/content-production/run-template"
    assert data["actions"][0]["input_fields"] == ["market_evidence"]


def test_fastapi_content_production_run_rejects_strict_reference_mode_without_assets(tmp_path):
    service = NoriBackend(upload_root=tmp_path / "uploads", experiment_runner=_project_runner(tmp_path))
    client = TestClient(create_app(backend=service))
    session = client.post("/sessions", json={"user_id": "u1"}).json()["data"]

    response = client.post(
        "/workflows/content-production/runs",
        json={
            "session_id": session["session_id"],
            "brief_text": "生成小红书内容",
            "require_image_references": True,
            "market_evidence": {"platform": "xhs", "queries": ["test"], "hot_notes": [], "insufficient": []},
        },
    )

    fetched = client.get(f"/sessions/{session['session_id']}").json()["data"]
    assert response.status_code == 400
    assert response.json()["message"] == "require_image_references=true requires at least one selected image asset"
    assert fetched["task_goals"] == []


def test_fastapi_content_production_run_rejects_strict_reference_transfer_before_task(monkeypatch, tmp_path):
    monkeypatch.setattr(CONTENT_RUN_MODULE, "experiment_readiness", lambda **_kwargs: _fake_reference_readiness(oss_configured=False))

    class FakeExperimentRunner:
        project_root = tmp_path

        def __init__(self):
            self.calls = []

        def run(self, request, *, session_id, task_id, asset_rows):
            self.calls.append({"request": request, "session_id": session_id, "task_id": task_id, "asset_rows": asset_rows})
            raise AssertionError("runner should not be called when strict references cannot be sent")

    runner = FakeExperimentRunner()
    service = NoriBackend(upload_root=tmp_path / "uploads", experiment_runner=runner)
    client = TestClient(create_app(backend=service))
    session = client.post("/sessions", json={"user_id": "u1"}).json()["data"]
    uploaded = client.post(
        f"/sessions/{session['session_id']}/assets",
        files=[("files", ("cover.png", b"fake-png-bytes", "image/png"))],
    ).json()["data"]["assets"][0]

    response = client.post(
        "/workflows/content-production/runs",
        json={
            "session_id": session["session_id"],
            "brief_text": "请参考上传图片生成内容",
            "asset_ids": [uploaded["asset_id"]],
            "require_image_references": True,
            "market_evidence": {"platform": "xhs", "queries": ["test"], "hot_notes": [], "insufficient": []},
        },
    )

    data = response.json()
    fetched = client.get(f"/sessions/{session['session_id']}").json()["data"]
    assert response.status_code == 400
    assert "content-production run preflight failed" in data["message"]
    assert data["data"]["checks"][0]["name"] == "reference_transfer"
    repair_actions = {row["action_id"]: row for row in data["data"]["actions"]}
    assert repair_actions["publish_reference_assets"]["href"] == (
        f"/sessions/{session['session_id']}/assets/publish-references"
    )
    assert repair_actions["publish_reference_assets"]["payload"]["asset_ids"] == [uploaded["asset_id"]]
    assert repair_actions["set_backend_public_base_url"]["input_fields"] == ["backend_public_base_url"]
    assert data["data"]["links"]["preflight"] == "/workflows/content-production/runs/preflight"
    assert runner.calls == []
    assert fetched["task_goals"] == []


def test_fastapi_content_production_run_rejects_missing_market_evidence_before_task(tmp_path):
    class FakeExperimentRunner:
        project_root = tmp_path

        def run(self, request, *, session_id, task_id, asset_rows):
            raise AssertionError("runner should not be called without required market evidence")

    service = NoriBackend(experiment_runner=FakeExperimentRunner())
    client = TestClient(create_app(backend=service))
    session = client.post("/sessions", json={"user_id": "u1"}).json()["data"]

    response = client.post(
        "/workflows/content-production/runs",
        json={
            "session_id": session["session_id"],
            "brief_text": "生成小红书内容",
        },
    )

    data = response.json()
    fetched = client.get(f"/sessions/{session['session_id']}").json()["data"]
    assert response.status_code == 400
    assert "market_evidence" in data["message"]
    assert data["data"]["checks"][0]["name"] == "market_evidence"
    assert fetched["task_goals"] == []


def test_fastapi_content_production_run_rejects_unready_models_for_real_runner(monkeypatch, tmp_path):
    monkeypatch.setattr(CONTENT_RUN_MODULE, "experiment_readiness", lambda **_kwargs: _fake_unready_model_readiness())
    service = NoriBackend(experiment_runner=ContentProductionExperimentRunner(project_root=tmp_path))
    client = TestClient(create_app(backend=service))
    session = client.post("/sessions", json={"user_id": "u1"}).json()["data"]

    response = client.post(
        "/workflows/content-production/runs",
        json={
            "session_id": session["session_id"],
            "brief_text": "生成小红书内容",
            "market_evidence": {"platform": "xhs", "queries": ["test"], "hot_notes": [], "insufficient": []},
        },
    )

    data = response.json()
    fetched = client.get(f"/sessions/{session['session_id']}").json()["data"]
    assert response.status_code == 400
    assert "models_ready" in data["message"]
    assert data["data"]["checks"][0]["name"] == "models_ready"
    assert fetched["task_goals"] == []


def test_fastapi_fake_runner_can_skip_model_readiness_gate(monkeypatch, tmp_path):
    monkeypatch.setattr(CONTENT_RUN_MODULE, "experiment_readiness", lambda **_kwargs: _fake_unready_model_readiness())

    class FakeExperimentRunner:
        project_root = tmp_path

        def __init__(self):
            self.calls = []

        def run(self, request, *, session_id, task_id, asset_rows):
            self.calls.append({"request": dict(request), "session_id": session_id, "task_id": task_id, "asset_rows": asset_rows})
            return {
                "workflow_name": "content_production",
                "run_id": "run_fake",
                "run_dir": str(tmp_path / "run_fake"),
                "status": "succeeded",
                "session_id": session_id,
                "task_id": task_id,
                "asset_paths": [],
                "asset_ids": [],
                "artifact_paths": {},
                "cover_paths": [],
                "image_reference": {"status": "not_selected", "sent": False},
                "workflow_run": {"status": "succeeded", "session_id": session_id, "task_id": task_id},
            }

    runner = FakeExperimentRunner()
    service = NoriBackend(experiment_runner=runner)
    client = TestClient(create_app(backend=service))
    session = client.post("/sessions", json={"user_id": "u1"}).json()["data"]

    response = client.post(
        "/workflows/content-production/runs",
        json={
            "session_id": session["session_id"],
            "brief_text": "生成小红书内容",
            "market_evidence": {"platform": "xhs", "queries": ["test"], "hot_notes": [], "insufficient": []},
        },
    )

    assert response.status_code == 201
    assert response.json()["data"]["status"] == "succeeded"
    assert runner.calls[0]["request"]["brief_text"] == "生成小红书内容"


def test_fastapi_content_production_run_receives_session_reference_check_evidence(monkeypatch, tmp_path):
    monkeypatch.setattr(CONTENT_RUN_MODULE, "experiment_readiness", lambda **_kwargs: _fake_reference_readiness(oss_configured=True))

    class FakeExperimentRunner:
        project_root = tmp_path

        def __init__(self):
            self.calls = []

        def run(self, request, *, session_id, task_id, asset_rows):
            self.calls.append({"request": dict(request), "session_id": session_id, "task_id": task_id, "asset_rows": asset_rows})
            return {
                "workflow_name": "content_production",
                "run_id": "run_fake",
                "run_dir": str(tmp_path / "run_fake"),
                "status": "succeeded",
                "session_id": session_id,
                "task_id": task_id,
                "asset_paths": [str(row.get("path") or "") for row in asset_rows],
                "asset_ids": [str(row.get("asset_id") or "") for row in asset_rows],
                "artifact_paths": {},
                "cover_paths": [],
                "image_reference": {"status": "sent", "sent": True},
                "workflow_run": {"status": "succeeded", "session_id": session_id, "task_id": task_id},
            }

    runner = FakeExperimentRunner()
    service = NoriBackend(experiment_runner=runner)
    client = TestClient(create_app(backend=service))
    session = client.post("/sessions", json={"user_id": "u1"}).json()["data"]
    uploaded = client.post(
        f"/sessions/{session['session_id']}/assets",
        files=[("files", ("cover.png", b"fake-png-bytes", "image/png"))],
    ).json()["data"]["assets"][0]
    expected_url = f"https://backend.nori.ai/sessions/{session['session_id']}/assets/{uploaded['asset_id']}/file"

    stored_session = service.session_manager.get_session(session["session_id"])
    stored_session.events.append(
        SessionEvent(
            event_type="reference_image_generation_checked",
            payload={
                "ready": True,
                "reason": "image_generation_succeeded",
                "provider_fetchable_reference_images": [expected_url],
                "generation": {"ready": True, "reason": "image_generation_succeeded", "image_count": 1},
            },
        )
    )
    service.session_manager.save_session(session["session_id"])

    response = client.post(
        "/workflows/content-production/runs",
        json={
            "session_id": session["session_id"],
            "brief_text": "请参考上传图片生成内容",
            "asset_ids": [uploaded["asset_id"]],
            "backend_public_base_url": "https://backend.nori.ai",
            "require_image_references": True,
            "market_evidence": {"platform": "xhs", "queries": ["test"], "hot_notes": [], "insufficient": []},
        },
    )

    assert response.status_code == 201
    evidence = runner.calls[0]["request"]["reference_image_generation_check"]
    assert evidence["ready"] is True
    assert evidence["reason"] == "image_generation_succeeded"
    assert evidence["selected_provider_fetchable_reference_images"] == [expected_url]
    assert evidence["covered_selected_reference_images"] == [expected_url]
    assert evidence["missing_selected_reference_images"] == []
    assert evidence["covers_selected_reference_images"] is True


def test_fastapi_content_production_run_can_require_reference_generation_check(monkeypatch, tmp_path):
    monkeypatch.setattr(CONTENT_RUN_MODULE, "experiment_readiness", lambda **_kwargs: _fake_reference_readiness(oss_configured=True))

    class FakeExperimentRunner:
        project_root = tmp_path

        def __init__(self):
            self.calls = []

        def run(self, request, *, session_id, task_id, asset_rows):
            self.calls.append({"request": dict(request), "session_id": session_id, "task_id": task_id, "asset_rows": asset_rows})
            raise AssertionError("runner should be blocked before generation check evidence exists")

    runner = FakeExperimentRunner()
    service = NoriBackend(experiment_runner=runner)
    client = TestClient(create_app(backend=service))
    session = client.post("/sessions", json={"user_id": "u1"}).json()["data"]
    uploaded = client.post(
        f"/sessions/{session['session_id']}/assets",
        files=[("files", ("cover.png", b"fake-png-bytes", "image/png"))],
    ).json()["data"]["assets"][0]
    payload = {
        "session_id": session["session_id"],
        "brief_text": "请参考上传图片生成内容",
        "asset_ids": [uploaded["asset_id"]],
        "backend_public_base_url": "https://backend.nori.ai",
        "require_image_references": True,
        "require_reference_image_generation_check": True,
        "market_evidence": {"platform": "xhs", "queries": ["test"], "hot_notes": [], "insufficient": []},
    }

    preflight = client.post("/workflows/content-production/runs/preflight", json=payload).json()["data"]
    response = client.post("/workflows/content-production/runs", json=payload)

    data = response.json()
    actions = {row["action_id"]: row for row in data["data"]["actions"]}
    assert preflight["ready"] is False
    assert preflight["checks"][-1]["name"] == "reference_image_generation_check"
    assert response.status_code == 400
    assert "reference_image_generation_check" in data["message"]
    assert actions["check_reference_image_generation"]["severity"] == "blocking"
    assert actions["check_reference_image_generation"]["href"] == (
        f"/sessions/{session['session_id']}/assets/reference-image-generation-check"
    )
    assert runner.calls == []


def test_fastapi_content_production_sync_failure_returns_failed_run_data(tmp_path):
    class FailingExperimentRunner:
        project_root = tmp_path

        def run(self, request, *, session_id, task_id, asset_rows):
            original = RuntimeError("image failed")
            raise ContentProductionRunFailed(
                original,
                failure_result=_failed_run_result(
                    case_id="case_failed",
                    run_id="run_failed",
                    session_id=session_id,
                    task_id=task_id,
                ),
            )

    service = NoriBackend(experiment_runner=FailingExperimentRunner())
    client = TestClient(create_app(backend=service))
    session = client.post("/sessions", json={"user_id": "u1"}).json()["data"]

    response = client.post(
        "/workflows/content-production/runs",
        json={
            "session_id": session["session_id"],
            "case_id": "case_failed",
            "brief_text": "生成小红书内容",
            "market_evidence": {"platform": "xhs", "queries": ["test"], "hot_notes": [], "insufficient": []},
        },
    )

    data = response.json()
    fetched = client.get(f"/sessions/{session['session_id']}").json()["data"]
    failed_run = data["data"]["run"]
    assert response.status_code == 500
    assert data["message"] == "content-production run failed: RuntimeError: image failed"
    assert failed_run["status"] == "failed"
    assert failed_run["run_id"] == "run_failed"
    assert failed_run["experiment_manifest"]["error"] == {"type": "RuntimeError", "message": "image failed"}
    assert failed_run["artifact_urls"]["experiment_manifest.json"].endswith(
        "/workflows/content-production/runs/case_failed/run_failed/artifacts/experiment_manifest.json"
    )
    assert failed_run["links"]["inspect_artifacts"] == (
        "/workflows/content-production/runs/case_failed/run_failed/artifacts/inspect"
    )
    assert [action["action_id"] for action in failed_run["actions"]][:2] == [
        "inspect_failure_artifacts",
        "replay_run",
    ]
    assert fetched["task_goals"][0]["status"] == "failed"
    assert fetched["events"][-1]["payload"]["run_id"] == "run_failed"
    assert fetched["events"][-1]["payload"]["actions"][0]["action_id"] == "inspect_failure_artifacts"


def test_fastapi_content_production_background_run_can_be_polled(tmp_path):
    class FakeExperimentRunner:
        project_root = tmp_path

        def __init__(self):
            self.calls = []

        def run(self, request, *, session_id, task_id, asset_rows):
            self.calls.append({
                "request": dict(request),
                "session_id": session_id,
                "task_id": task_id,
                "asset_rows": [dict(row) for row in asset_rows],
            })
            return {
                "workflow_name": "content_production",
                "run_id": "run_background",
                "run_dir": str(tmp_path / "run_background"),
                "status": "succeeded",
                "session_id": session_id,
                "task_id": task_id,
                "asset_paths": [row["path"] for row in asset_rows],
                "asset_ids": [row["asset_id"] for row in asset_rows],
                "artifact_paths": {},
                "cover_paths": [],
                "image_reference": {"status": "not_selected", "sent": False},
                "workflow_run": {"status": "succeeded", "session_id": session_id, "task_id": task_id},
            }

    runner = FakeExperimentRunner()
    service = NoriBackend(upload_root=tmp_path / "uploads", experiment_runner=runner)
    client = TestClient(create_app(backend=service))
    session = client.post("/sessions", json={"user_id": "u1"}).json()["data"]
    uploaded = client.post(
        f"/sessions/{session['session_id']}/assets",
        files=[("files", ("cover.png", b"fake-png-bytes", "image/png"))],
    ).json()["data"]["assets"][0]

    response = client.post(
        "/workflows/content-production/runs",
        json={
            "session_id": session["session_id"],
            "goal": "后台生成小红书图文",
            "brief_text": "请参考上传图片生成内容",
            "asset_ids": [uploaded["asset_id"]],
            "execution_mode": "background",
            "market_evidence": {"platform": "xhs", "queries": ["test"], "hot_notes": [], "insufficient": []},
        },
    )

    assert response.status_code == 202
    job = response.json()["data"]
    assert job["status"] in {"queued", "running", "succeeded"}
    assert job["job_type"] == "content_production"
    assert job["metadata"]["session_id"] == session["session_id"]
    assert job["metadata"]["task_id"]
    assert job["links"]["self"] == f"/experiments/jobs/{job['job_id']}"

    final_job = None
    for _ in range(20):
        polled = client.get(job["links"]["self"])
        assert polled.status_code == 200
        final_job = polled.json()["data"]["job"]
        if final_job["status"] == "succeeded":
            break
        time.sleep(0.01)

    assert final_job["status"] == "succeeded"
    assert final_job["result"]["run_id"] == "run_background"
    assert final_job["result"]["actions"][0]["action_id"] == "inspect_run"
    assert final_job["links"]["run"] == f"/workflows/content-production/runs/{session['session_id']}/run_background"
    assert final_job["links"]["export"] == f"/workflows/content-production/runs/{session['session_id']}/run_background/export"
    assert final_job["links"]["evaluations"] == f"/workflows/content-production/runs/{session['session_id']}/run_background/evaluations"
    assert final_job["links"]["replay"] == f"/workflows/content-production/runs/{session['session_id']}/run_background/replay"
    assert final_job["actions"][0]["action_id"] == "inspect_run"
    assert any(action["action_id"] == "draft_evaluation" for action in final_job["actions"])
    assert runner.calls[0]["asset_rows"][0]["path"] == uploaded["path"]
    fetched = client.get(f"/sessions/{session['session_id']}").json()["data"]
    assert fetched["task_goals"][0]["status"] == "succeeded"
    assert fetched["events"][-1]["event_type"] == "workflow_run_finished"


def test_fastapi_cancel_queued_content_job_updates_session_task(tmp_path):
    blocker_started = Event()
    blocker_release = Event()

    def blocker():
        blocker_started.set()
        blocker_release.wait(2)
        return {"status": "succeeded"}

    class NeverRunExperimentRunner:
        project_root = tmp_path

        def run(self, *_args, **_kwargs):
            raise AssertionError("queued job should be cancelled before runner starts")

    job_store = InProcessExperimentJobStore(storage_root=tmp_path / "jobs", max_workers=1)
    blocker_job = job_store.submit(job_type="blocker", metadata={}, target=blocker)
    assert blocker_started.wait(1)

    service = NoriBackend(
        upload_root=tmp_path / "uploads",
        experiment_runner=NeverRunExperimentRunner(),
        job_store=job_store,
    )
    client = TestClient(create_app(backend=service))
    session = client.post("/sessions", json={"user_id": "u1"}).json()["data"]

    run_response = client.post(
        "/workflows/content-production/runs",
        json={
            "session_id": session["session_id"],
            "goal": "后台生成小红书图文",
            "brief_text": "brief",
            "execution_mode": "background",
            "market_evidence": {"platform": "xhs", "queries": ["test"], "hot_notes": [], "insufficient": []},
        },
    )
    job = run_response.json()["data"]

    cancel_response = client.post(
        f"/experiments/jobs/{job['job_id']}/cancel",
        json={"reason": "operator cancelled before model calls"},
    )
    duplicate_cancel = client.post(
        f"/experiments/jobs/{job['job_id']}/cancel",
        json={"reason": "operator cancelled before model calls"},
    )
    fetched = client.get(f"/sessions/{session['session_id']}").json()["data"]
    cancel_events = [event for event in fetched["events"] if event["event_type"] == "workflow_run_cancelled"]

    assert run_response.status_code == 202
    assert cancel_response.status_code == 200
    assert cancel_response.json()["data"]["job"]["status"] == "cancelled"
    assert cancel_response.json()["data"]["session"]["task_status"] == "cancelled"
    assert duplicate_cancel.json()["data"]["session"]["task_status"] == "cancelled"
    assert fetched["task_goals"][0]["status"] == "cancelled"
    assert len(cancel_events) == 1
    assert cancel_events[0]["payload"]["job_id"] == job["job_id"]
    assert cancel_events[0]["payload"]["reason"] == "operator cancelled before model calls"

    blocker_release.set()
    for _ in range(20):
        blocker_final = job_store.get(blocker_job["job_id"])
        if blocker_final and blocker_final["status"] == "succeeded":
            break
        time.sleep(0.01)


def test_fastapi_cancel_running_content_job_marks_session_task_cancelling(tmp_path):
    runner_started = Event()
    runner_release = Event()

    class BlockingExperimentRunner:
        project_root = tmp_path

        def run(self, request, *, session_id, task_id, asset_rows):
            runner_started.set()
            runner_release.wait(2)
            return {
                "workflow_name": "content_production",
                "run_id": "run_after_cancel_request",
                "run_dir": str(tmp_path / "run_after_cancel_request"),
                "status": "succeeded",
                "session_id": session_id,
                "task_id": task_id,
                "asset_paths": [row["path"] for row in asset_rows],
                "asset_ids": [row["asset_id"] for row in asset_rows],
                "artifact_paths": {},
                "cover_paths": [],
                "image_reference": {"status": "not_selected", "sent": False},
                "workflow_run": {"status": "succeeded", "session_id": session_id, "task_id": task_id},
            }

    job_store = InProcessExperimentJobStore(storage_root=tmp_path / "jobs", max_workers=1)
    service = NoriBackend(
        upload_root=tmp_path / "uploads",
        experiment_runner=BlockingExperimentRunner(),
        job_store=job_store,
    )
    client = TestClient(create_app(backend=service))
    session = client.post("/sessions", json={"user_id": "u1"}).json()["data"]

    run_response = client.post(
        "/workflows/content-production/runs",
        json={
            "session_id": session["session_id"],
            "goal": "后台生成小红书图文",
            "brief_text": "brief",
            "execution_mode": "background",
            "market_evidence": {"platform": "xhs", "queries": ["test"], "hot_notes": [], "insufficient": []},
        },
    )
    job = run_response.json()["data"]
    assert runner_started.wait(1)

    cancel_response = client.post(
        f"/experiments/jobs/{job['job_id']}/cancel",
        json={"reason": "operator cancelled during model call"},
    )
    cancelling_session = client.get(f"/sessions/{session['session_id']}").json()["data"]
    cancel_events = [
        event for event in cancelling_session["events"] if event["event_type"] == "workflow_run_cancel_requested"
    ]

    assert run_response.status_code == 202
    assert cancel_response.status_code == 200
    assert cancel_response.json()["data"]["job"]["status"] == "cancelling"
    assert cancel_response.json()["data"]["session"]["task_status"] == "cancelling"
    assert cancelling_session["task_goals"][0]["status"] == "cancelling"
    assert len(cancel_events) == 1
    assert cancel_events[0]["payload"]["reason"] == "operator cancelled during model call"

    runner_release.set()
    final_job = None
    for _ in range(20):
        final_job = client.get(job["links"]["self"]).json()["data"]["job"]
        if final_job["status"] == "succeeded":
            break
        time.sleep(0.01)
    completed_session = client.get(f"/sessions/{session['session_id']}").json()["data"]

    assert final_job["status"] == "succeeded"
    assert completed_session["task_goals"][0]["status"] == "succeeded"
    assert completed_session["events"][-1]["event_type"] == "workflow_run_finished"


def test_fastapi_lists_and_persists_background_experiment_jobs(tmp_path):
    class FakeExperimentRunner:
        project_root = tmp_path

        def run(self, request, *, session_id, task_id, asset_rows):
            return {
                "workflow_name": "content_production",
                "run_id": "run_persisted",
                "run_dir": str(tmp_path / "run_persisted"),
                "status": "succeeded",
                "session_id": session_id,
                "task_id": task_id,
                "asset_paths": [row["path"] for row in asset_rows],
                "asset_ids": [row["asset_id"] for row in asset_rows],
                "artifact_paths": {},
                "cover_paths": [],
                "image_reference": {"status": "not_selected", "sent": False},
                "workflow_run": {"status": "succeeded", "session_id": session_id, "task_id": task_id},
            }

    job_store = InProcessExperimentJobStore(storage_root=tmp_path / "jobs")
    service = NoriBackend(
        upload_root=tmp_path / "uploads",
        experiment_runner=FakeExperimentRunner(),
        job_store=job_store,
    )
    client = TestClient(create_app(backend=service))
    session = client.post("/sessions", json={"user_id": "u1"}).json()["data"]

    response = client.post(
        "/workflows/content-production/runs",
        json={
            "session_id": session["session_id"],
            "case_id": "case_jobs",
            "goal": "后台生成小红书图文",
            "brief_text": "brief",
            "execution_mode": "background",
            "market_evidence": {"platform": "xhs", "queries": ["test"], "hot_notes": [], "insufficient": []},
        },
    )
    job = response.json()["data"]

    final_job = None
    for _ in range(20):
        final_job = client.get(job["links"]["self"]).json()["data"]["job"]
        if final_job["status"] == "succeeded":
            break
        time.sleep(0.01)

    listed = client.get("/experiments/jobs", params={"session_id": session["session_id"]})
    listed_by_case = client.get("/experiments/jobs", params={"case_id": "case_jobs", "status": "succeeded"})

    assert final_job["status"] == "succeeded"
    assert listed.status_code == 200
    assert listed.json()["data"]["jobs"][0]["job_id"] == job["job_id"]
    assert listed_by_case.status_code == 200
    assert listed_by_case.json()["data"]["jobs"][0]["metadata"]["case_id"] == "case_jobs"
    job_file = tmp_path / "jobs" / f"{job['job_id']}.json"
    assert job_file.is_file()
    restored_store = InProcessExperimentJobStore(storage_root=tmp_path / "jobs", max_workers=1)
    restored_job = restored_store.get(job["job_id"])
    assert restored_job["status"] == "succeeded"
    assert restored_job["result"]["run_id"] == "run_persisted"
    assert restored_job["result"]["links"]["case_next_actions"] == (
        "/experiments/content-production/cases/case_jobs/next-actions"
    )
    assert any(action["action_id"] == "draft_evaluation" for action in restored_job["actions"])
    assert restored_job["links"]["run"] == "/workflows/content-production/runs/case_jobs/run_persisted"
    assert restored_job["links"]["export"] == "/workflows/content-production/runs/case_jobs/run_persisted/export"


def test_fastapi_restores_interrupted_job_state_to_session_task_after_restart(tmp_path):
    service = NoriBackend(experiment_runner=_project_runner(tmp_path))
    client = TestClient(create_app(backend=service))
    session = client.post("/sessions", json={"user_id": "u1"}).json()["data"]
    task = client.post(
        f"/sessions/{session['session_id']}/tasks",
        json={"goal": "后台生成小红书图文", "workflow_name": "content-production"},
    ).json()["data"]
    stored_session = service.session_manager.get_session(session["session_id"])
    stored_session.task_goals[0].status = "running"
    service.session_manager.save_session(session["session_id"])
    job = service.job_store.create(
        job_type="content_production",
        metadata={"session_id": session["session_id"], "task_id": task["task_id"], "case_id": "case_restore"},
    )
    job_file = tmp_path / "data" / "backend" / "jobs" / f"{job['job_id']}.json"
    job_data = json.loads(job_file.read_text(encoding="utf-8"))
    job_data["status"] = "running"
    job_data["started_at"] = "2026-06-08T00:00:00"
    job_file.write_text(json.dumps(job_data, ensure_ascii=False, indent=2), encoding="utf-8")

    restored_service = NoriBackend(experiment_runner=_project_runner(tmp_path))
    restored_client = TestClient(create_app(backend=restored_service))
    restored_job = restored_client.get(f"/experiments/jobs/{job['job_id']}").json()["data"]["job"]
    restored_session = restored_client.get(f"/sessions/{session['session_id']}").json()["data"]
    persisted_job = json.loads(job_file.read_text(encoding="utf-8"))

    assert restored_job["status"] == "interrupted"
    assert restored_job["error"]["error_type"] == "ProcessInterrupted"
    assert persisted_job["status"] == "interrupted"
    assert restored_session["task_goals"][0]["status"] == "interrupted"
    interrupted_events = [
        event for event in restored_session["events"] if event["event_type"] == "workflow_run_interrupted"
    ]
    assert len(interrupted_events) == 1
    assert interrupted_events[0]["payload"]["job_id"] == job["job_id"]
    assert interrupted_events[0]["payload"]["task_id"] == task["task_id"]

    restarted_again = NoriBackend(experiment_runner=_project_runner(tmp_path))
    restarted_client = TestClient(create_app(backend=restarted_again))
    session_after_second_restart = restarted_client.get(f"/sessions/{session['session_id']}").json()["data"]
    interrupted_events_after_second_restart = [
        event for event in session_after_second_restart["events"] if event["event_type"] == "workflow_run_interrupted"
    ]
    assert len(interrupted_events_after_second_restart) == 1


def test_fastapi_content_production_background_job_records_failures(tmp_path):
    class FailingRunner:
        project_root = tmp_path

        def run(self, *_args, **_kwargs):
            raise RuntimeError("provider unavailable")

    service = NoriBackend(upload_root=tmp_path / "uploads", experiment_runner=FailingRunner())
    client = TestClient(create_app(backend=service))
    session = client.post("/sessions", json={"user_id": "u1"}).json()["data"]

    response = client.post(
        "/workflows/content-production/runs",
        json={
            "session_id": session["session_id"],
            "goal": "后台生成小红书图文",
            "brief_text": "brief",
            "execution_mode": "background",
            "market_evidence": {"platform": "xhs", "queries": ["test"], "hot_notes": [], "insufficient": []},
        },
    )
    job = response.json()["data"]

    final_job = None
    for _ in range(20):
        final_job = client.get(job["links"]["self"]).json()["data"]["job"]
        if final_job["status"] == "failed":
            break
        time.sleep(0.01)

    assert response.status_code == 202
    assert final_job["status"] == "failed"
    assert final_job["error"]["error_type"] == "RuntimeError"
    assert final_job["error"]["error"] == "provider unavailable"
    fetched = client.get(f"/sessions/{session['session_id']}").json()["data"]
    assert fetched["task_goals"][0]["status"] == "failed"


def test_fastapi_background_failed_run_keeps_result_and_links(tmp_path):
    class FailingExperimentRunner:
        project_root = tmp_path

        def run(self, request, *, session_id, task_id, asset_rows):
            original = RuntimeError("image failed")
            raise ContentProductionRunFailed(
                original,
                failure_result=_failed_run_result(
                    case_id="case_failed",
                    run_id="run_failed",
                    session_id=session_id,
                    task_id=task_id,
                ),
            )

    job_store = InProcessExperimentJobStore(storage_root=tmp_path / "jobs")
    service = NoriBackend(experiment_runner=FailingExperimentRunner(), job_store=job_store)
    client = TestClient(create_app(backend=service))
    session = client.post("/sessions", json={"user_id": "u1"}).json()["data"]

    response = client.post(
        "/workflows/content-production/runs",
        json={
            "session_id": session["session_id"],
            "case_id": "case_failed",
            "brief_text": "生成小红书内容",
            "execution_mode": "background",
            "market_evidence": {"platform": "xhs", "queries": ["test"], "hot_notes": [], "insufficient": []},
        },
    )
    job = response.json()["data"]

    final_job = None
    for _ in range(20):
        final_job = client.get(job["links"]["self"]).json()["data"]["job"]
        if final_job["status"] == "failed":
            break
        time.sleep(0.01)

    assert response.status_code == 202
    assert final_job["status"] == "failed"
    assert final_job["error"]["error_type"] == "ContentProductionRunFailed"
    assert final_job["result"]["status"] == "failed"
    assert final_job["result"]["run_id"] == "run_failed"
    assert final_job["result"]["actions"][0]["action_id"] == "inspect_failure_artifacts"
    assert final_job["links"]["run"] == "/workflows/content-production/runs/case_failed/run_failed"
    assert final_job["links"]["export"] == "/workflows/content-production/runs/case_failed/run_failed/export"
    assert any(action["action_id"] == "replay_run" for action in final_job["actions"])
    restored_store = InProcessExperimentJobStore(storage_root=tmp_path / "jobs", max_workers=1)
    restored_job = restored_store.get(job["job_id"])
    assert restored_job["result"]["run_id"] == "run_failed"
    assert restored_job["links"]["replay"] == "/workflows/content-production/runs/case_failed/run_failed/replay"
    assert restored_job["actions"][0]["action_id"] == "inspect_failure_artifacts"


def test_fastapi_replays_content_production_run_from_replay_request(tmp_path):
    asset_path = tmp_path / "reference.png"
    asset_path.write_bytes(b"fake-png")
    run_dir = tmp_path / "cases" / "source_case" / "runs" / "source_run"
    run_dir.mkdir(parents=True)
    (run_dir / "replay_request.json").write_text(
        json.dumps(
            {
                "session_id": "old_session",
                "task_id": "old_task",
                "goal": "旧目标",
                "brief_text": "请参考图片生成小红书图文",
                "case_id": "source_case",
                "case_title": "Source Case",
                "asset_ids": ["old_asset"],
                "asset_paths": [str(asset_path)],
                "market_evidence": {"platform": "xhs", "queries": ["test"], "hot_notes": [], "insufficient": []},
                "human_gate_mode": "skip",
                "metadata": {"original": True},
            }
        ),
        encoding="utf-8",
    )

    class FakeExperimentRunner:
        project_root = tmp_path

        def __init__(self):
            self.calls = []

        def run(self, request, *, session_id, task_id, asset_rows):
            self.calls.append({
                "request": dict(request),
                "session_id": session_id,
                "task_id": task_id,
                "asset_rows": [dict(row) for row in asset_rows],
            })
            return {
                "workflow_name": "content_production",
                "run_id": "replay_run",
                "run_dir": str(tmp_path / "replay_run"),
                "status": "succeeded",
                "session_id": session_id,
                "task_id": task_id,
                "asset_paths": [row["path"] for row in asset_rows],
                "asset_ids": [row["asset_id"] for row in asset_rows],
                "artifact_paths": {},
                "cover_paths": [],
                "image_reference": {"status": "not_selected", "sent": False},
                "workflow_run": {"status": "succeeded", "session_id": session_id, "task_id": task_id},
            }

    runner = FakeExperimentRunner()
    service = NoriBackend(experiment_runner=runner)
    client = TestClient(create_app(backend=service))

    response = client.post(
        "/workflows/content-production/runs/source_case/source_run/replay",
        json={"metadata": {"operator": "test"}},
    )

    assert response.status_code == 201
    data = response.json()["data"]
    assert data["status"] == "succeeded"
    assert data["asset_paths"] == [str(asset_path)]
    assert data["session_id"] != "old_session"
    assert data["task_id"] != "old_task"
    assert runner.calls[0]["request"]["asset_ids"] == []
    assert runner.calls[0]["request"]["metadata"]["original"] is True
    assert runner.calls[0]["request"]["metadata"]["operator"] == "test"
    assert runner.calls[0]["request"]["metadata"]["replay_of"] == {"case_id": "source_case", "run_id": "source_run"}
    assert runner.calls[0]["asset_rows"][0]["path"] == str(asset_path)
    sessions = client.get("/sessions").json()["data"]["sessions"]
    assert sessions[0]["metadata"]["source"] == "backend.replay_content_production_run"
    assert sessions[0]["metadata"]["original_session_id"] == "old_session"


def test_fastapi_replay_requires_current_session_reference_generation_check(monkeypatch, tmp_path):
    monkeypatch.setattr(CONTENT_RUN_MODULE, "experiment_readiness", lambda **_kwargs: _fake_reference_readiness(oss_configured=False))
    run_dir = tmp_path / "cases" / "source_case" / "runs" / "source_run"
    run_dir.mkdir(parents=True)
    reference_url = "https://cdn.nori.ai/ref.png"
    (run_dir / "replay_request.json").write_text(
        json.dumps(
            {
                "session_id": "old_session",
                "brief_text": "请参考图片生成小红书图文",
                "case_id": "source_case",
                "asset_paths": [reference_url],
                "require_image_references": True,
                "require_reference_image_generation_check": True,
                "reference_image_generation_check": {
                    "ready": True,
                    "reason": "stale_replay_snapshot",
                    "provider_fetchable_reference_images": [reference_url],
                    "covers_selected_reference_images": True,
                },
                "market_evidence": {"platform": "xhs", "queries": ["test"], "hot_notes": [], "insufficient": []},
                "human_gate_mode": "skip",
            }
        ),
        encoding="utf-8",
    )

    class FakeExperimentRunner:
        project_root = tmp_path

        def __init__(self):
            self.calls = []

        def run(self, request, *, session_id, task_id, asset_rows):
            self.calls.append({"request": dict(request), "session_id": session_id, "task_id": task_id, "asset_rows": asset_rows})
            raise AssertionError("runner should be blocked until the current session has provider-check evidence")

    runner = FakeExperimentRunner()
    service = NoriBackend(experiment_runner=runner)
    client = TestClient(create_app(backend=service))

    response = client.post("/workflows/content-production/runs/source_case/source_run/replay", json={})

    data = response.json()
    assert response.status_code == 400
    assert "reference_image_generation_check" in data["message"]
    assert data["data"]["checks"][0]["name"] == "reference_image_generation_check"
    assert runner.calls == []


def test_fastapi_replay_can_reuse_explicit_session_reference_generation_check(monkeypatch, tmp_path):
    monkeypatch.setattr(CONTENT_RUN_MODULE, "experiment_readiness", lambda **_kwargs: _fake_reference_readiness(oss_configured=False))
    run_dir = tmp_path / "cases" / "source_case" / "runs" / "source_run"
    run_dir.mkdir(parents=True)
    reference_url = "https://cdn.nori.ai/ref.png"
    (run_dir / "replay_request.json").write_text(
        json.dumps(
            {
                "session_id": "old_session",
                "brief_text": "请参考图片生成小红书图文",
                "case_id": "source_case",
                "asset_paths": [reference_url],
                "require_image_references": True,
                "require_reference_image_generation_check": True,
                "market_evidence": {"platform": "xhs", "queries": ["test"], "hot_notes": [], "insufficient": []},
                "human_gate_mode": "skip",
            }
        ),
        encoding="utf-8",
    )

    class FakeExperimentRunner:
        project_root = tmp_path

        def __init__(self):
            self.calls = []

        def run(self, request, *, session_id, task_id, asset_rows):
            self.calls.append({
                "request": dict(request),
                "session_id": session_id,
                "task_id": task_id,
                "asset_rows": [dict(row) for row in asset_rows],
            })
            return {
                "workflow_name": "content_production",
                "run_id": "replay_run",
                "run_dir": str(tmp_path / "replay_run"),
                "status": "succeeded",
                "session_id": session_id,
                "task_id": task_id,
                "asset_paths": [row["path"] for row in asset_rows],
                "asset_ids": [row["asset_id"] for row in asset_rows],
                "artifact_paths": {},
                "cover_paths": [],
                "image_reference": {"status": "sent", "sent": True},
                "workflow_run": {"status": "succeeded", "session_id": session_id, "task_id": task_id},
            }

    runner = FakeExperimentRunner()
    service = NoriBackend(experiment_runner=runner)
    client = TestClient(create_app(backend=service))
    session = client.post("/sessions", json={"user_id": "u1"}).json()["data"]
    stored_session = service.session_manager.get_session(session["session_id"])
    stored_session.events.append(
        SessionEvent(
            event_type="reference_image_generation_checked",
            payload={
                "ready": True,
                "reason": "image_generation_succeeded",
                "provider_fetchable_reference_images": [reference_url],
                "generation": {"ready": True, "reason": "image_generation_succeeded", "image_count": 1},
            },
        )
    )
    service.session_manager.save_session(session["session_id"])

    response = client.post(
        "/workflows/content-production/runs/source_case/source_run/replay",
        json={"session_id": session["session_id"]},
    )

    assert response.status_code == 201
    evidence = runner.calls[0]["request"]["reference_image_generation_check"]
    assert runner.calls[0]["session_id"] == session["session_id"]
    assert runner.calls[0]["asset_rows"][0]["path"] == reference_url
    assert evidence["ready"] is True
    assert evidence["selected_provider_fetchable_reference_images"] == [reference_url]
    assert evidence["covered_selected_reference_images"] == [reference_url]
    assert evidence["covers_selected_reference_images"] is True


def test_fastapi_replays_content_production_case_selected_run(tmp_path):
    asset_path = tmp_path / "reference.png"
    asset_path.write_bytes(b"fake-png")
    run_dir = tmp_path / "cases" / "source_case" / "runs" / "source_run"
    covers_dir = run_dir / "covers"
    covers_dir.mkdir(parents=True)
    (covers_dir / "cover.png").write_bytes(b"cover")
    (run_dir / "run.json").write_text('{"workflow":"content_production","status":"succeeded"}', encoding="utf-8")
    (run_dir / "workflow_run.json").write_text(
        '{"workflow_name":"content_production","status":"succeeded","started_at":"t1","finished_at":"t2"}',
        encoding="utf-8",
    )
    (run_dir / "content_package.json").write_text('{"package_id":"pkg"}', encoding="utf-8")
    (run_dir / "input_manifest.json").write_text(
        json.dumps(
            {
                "brief": {"sha256": "brief"},
                "assets": [{"asset_id": "asset_1", "path": str(asset_path)}],
                "reference_transfer": {"required": False, "selected_count": 1, "provider_fetchable_count": 1},
                "market_evidence": {"queries": ["q"], "hot_note_count": 1},
                "run_options": {"require_image_references": False},
            }
        ),
        encoding="utf-8",
    )
    (run_dir / "experiment_manifest.json").write_text(
        json.dumps(
            {
                "schema_version": 1,
                "experiment": {"case_id": "source_case", "run_id": "source_run", "status": "succeeded"},
                "inputs": {
                    "brief": {"sha256": "brief"},
                    "assets": [{"asset_id": "asset_1", "path": str(asset_path)}],
                    "reference_transfer": {"required": False, "selected_count": 1, "provider_fetchable_count": 1},
                    "market_evidence": {"queries": ["q"], "hot_note_count": 1},
                    "run_options": {"require_image_references": False},
                },
                "reference_images": {"status": "sent", "required": False, "sent": True, "selected_count": 1},
                "evaluations": {"items": [], "summary": {"count": 1, "status": "passed", "score": 90}},
            }
        ),
        encoding="utf-8",
    )
    (run_dir / "replay_request.json").write_text(
        json.dumps(
            {
                "session_id": "old_session",
                "brief_text": "请参考图片生成小红书图文",
                "case_id": "source_case",
                "asset_paths": [str(asset_path)],
                "market_evidence": {"platform": "xhs", "queries": ["test"], "hot_notes": [], "insufficient": []},
            }
        ),
        encoding="utf-8",
    )

    class FakeExperimentRunner:
        project_root = tmp_path

        def __init__(self):
            self.calls = []

        def run(self, request, *, session_id, task_id, asset_rows):
            self.calls.append({"request": dict(request), "session_id": session_id, "task_id": task_id})
            return {
                "workflow_name": "content_production",
                "run_id": "case_replay_run",
                "run_dir": str(tmp_path / "case_replay_run"),
                "status": "succeeded",
                "session_id": session_id,
                "task_id": task_id,
                "asset_paths": [row["path"] for row in asset_rows],
                "asset_ids": [row["asset_id"] for row in asset_rows],
                "artifact_paths": {},
                "cover_paths": [],
                "image_reference": {"status": "not_selected", "sent": False},
                "workflow_run": {"status": "succeeded", "session_id": session_id, "task_id": task_id},
            }

    runner = FakeExperimentRunner()
    service = NoriBackend(experiment_runner=runner)
    client = TestClient(create_app(backend=service))
    selected = client.post(
        "/experiments/content-production/cases/source_case/selection",
        json={"run_id": "source_run", "decision": "selected", "reviewer": "operator"},
    )

    response = client.post(
        "/experiments/content-production/cases/source_case/replay",
        json={"case_id": "replayed_case", "metadata": {"operator": "case"}},
    )

    assert selected.status_code == 201
    assert response.status_code == 201
    data = response.json()["data"]
    assert data["run_id"] == "case_replay_run"
    assert data["source"] == "case_replay"
    assert data["source_case_id"] == "source_case"
    assert data["source_run_id"] == "source_run"
    assert data["source_run_selector"] == "selection"
    assert runner.calls[0]["request"]["case_id"] == "replayed_case"
    assert runner.calls[0]["request"]["metadata"]["operator"] == "case"
    assert runner.calls[0]["request"]["metadata"]["replay_of"] == {"case_id": "source_case", "run_id": "source_run"}


def test_fastapi_replays_content_production_run_as_background_job(tmp_path):
    asset_path = tmp_path / "reference.png"
    asset_path.write_bytes(b"fake-png")
    run_dir = tmp_path / "cases" / "source_case" / "runs" / "source_run"
    run_dir.mkdir(parents=True)
    (run_dir / "replay_request.json").write_text(
        json.dumps(
            {
                "session_id": "old_session",
                "brief_text": "请参考图片生成小红书图文",
                "case_id": "source_case",
                "asset_paths": [str(asset_path)],
                "market_evidence": {"platform": "xhs", "queries": ["test"], "hot_notes": [], "insufficient": []},
            }
        ),
        encoding="utf-8",
    )

    class FakeExperimentRunner:
        project_root = tmp_path

        def run(self, request, *, session_id, task_id, asset_rows):
            return {
                "workflow_name": "content_production",
                "run_id": "replay_background",
                "run_dir": str(tmp_path / "replay_background"),
                "status": "succeeded",
                "session_id": session_id,
                "task_id": task_id,
                "asset_paths": [row["path"] for row in asset_rows],
                "asset_ids": [row["asset_id"] for row in asset_rows],
                "artifact_paths": {},
                "cover_paths": [],
                "image_reference": {"status": "not_selected", "sent": False},
                "workflow_run": {"status": "succeeded", "session_id": session_id, "task_id": task_id},
            }

    service = NoriBackend(experiment_runner=FakeExperimentRunner())
    client = TestClient(create_app(backend=service))

    response = client.post(
        "/workflows/content-production/runs/source_case/source_run/replay",
        json={"execution_mode": "background", "case_id": "replayed_case"},
    )

    assert response.status_code == 202
    job = response.json()["data"]
    assert job["job_type"] == "content_production"
    assert job["metadata"]["case_id"] == "replayed_case"

    final_job = None
    for _ in range(20):
        final_job = client.get(job["links"]["self"]).json()["data"]["job"]
        if final_job["status"] == "succeeded":
            break
        time.sleep(0.01)

    assert final_job["status"] == "succeeded"
    assert final_job["result"]["run_id"] == "replay_background"


def test_fastapi_replay_returns_404_when_replay_request_is_missing(tmp_path):
    service = NoriBackend(experiment_runner=_project_runner(tmp_path))
    (tmp_path / "cases" / "source_case" / "runs" / "source_run").mkdir(parents=True)
    client = TestClient(create_app(backend=service))

    response = client.post("/workflows/content-production/runs/source_case/source_run/replay", json={})

    assert response.status_code == 404
    assert response.json()["message"] == "replay_request.json not found for run: source_case/source_run"


def test_fastapi_returns_404_for_missing_experiment_job():
    client = TestClient(create_app())

    response = client.get("/experiments/jobs/job_missing")

    assert response.status_code == 404
    assert response.json()["message"] == "experiment job not found: job_missing"


def test_fastapi_returns_404_for_missing_experiment_job_cancel():
    client = TestClient(create_app())

    response = client.post("/experiments/jobs/job_missing/cancel", json={"reason": "operator"})

    assert response.status_code == 404
    assert response.json()["message"] == "experiment job not found: job_missing"


def test_fastapi_cancels_queued_background_experiment_job(tmp_path):
    job_store = InProcessExperimentJobStore(storage_root=tmp_path / "jobs", max_workers=1)
    service = NoriBackend(experiment_runner=_project_runner(tmp_path), job_store=job_store)
    client = TestClient(create_app(backend=service))
    job = job_store.create(job_type="content_production", metadata={"case_id": "case_cancel"})

    response = client.post(
        f"/experiments/jobs/{job['job_id']}/cancel",
        json={"reason": "operator stopped the run"},
    )
    restored = InProcessExperimentJobStore(storage_root=tmp_path / "jobs", max_workers=1).get(job["job_id"])

    data = response.json()["data"]["job"]
    assert response.status_code == 200
    assert data["status"] == "cancelled"
    assert data["cancel_requested"] is True
    assert data["error"]["error_type"] == "JobCancelled"
    assert data["metadata"]["cancel_request"]["reason"] == "operator stopped the run"
    assert "cancel_job" not in [action["action_id"] for action in data["actions"]]
    assert restored["status"] == "cancelled"
    assert restored["cancel_requested"] is True


def test_fastapi_marks_running_background_experiment_job_cancelling(tmp_path):
    started = Event()
    release = Event()

    def target():
        started.set()
        release.wait(2)
        return {"status": "succeeded", "run_id": "run_after_cancel"}

    job_store = InProcessExperimentJobStore(storage_root=tmp_path / "jobs", max_workers=1)
    service = NoriBackend(experiment_runner=_project_runner(tmp_path), job_store=job_store)
    client = TestClient(create_app(backend=service))
    job = job_store.submit(
        job_type="content_production",
        metadata={"case_id": "case_cancel_running"},
        target=target,
    )
    assert started.wait(1)

    response = client.post(
        f"/experiments/jobs/{job['job_id']}/cancel",
        json={"reason": "operator stopped a long model call"},
    )
    cancelling = response.json()["data"]["job"]
    action_ids = [action["action_id"] for action in cancelling["actions"]]

    assert response.status_code == 200
    assert cancelling["status"] == "cancelling"
    assert cancelling["cancel_requested"] is True
    assert cancelling["error"]["error_type"] == "CancellationRequested"
    assert cancelling["metadata"]["cancel_request"]["reason"] == "operator stopped a long model call"
    assert "poll_job" in action_ids
    assert "cancel_job" not in action_ids

    release.set()
    final_job = None
    for _ in range(20):
        final_job = client.get(job["links"]["self"]).json()["data"]["job"]
        if final_job["status"] == "succeeded":
            break
        time.sleep(0.01)

    assert final_job["status"] == "succeeded"
    assert final_job["cancel_requested"] is True
    assert final_job["error"] is None
    assert final_job["result"]["run_id"] == "run_after_cancel"


def test_fastapi_exposes_experiment_readiness_and_run_summaries(tmp_path):
    service = NoriBackend(experiment_runner=_project_runner(tmp_path))
    run_dir = tmp_path / "cases" / "case1" / "runs" / "run1"
    run_dir.mkdir(parents=True)
    (run_dir / "run.json").write_text('{"workflow":"content_production","status":"succeeded"}', encoding="utf-8")
    (run_dir / "workflow_run.json").write_text('{"status":"succeeded","stages":[]}', encoding="utf-8")
    (run_dir / "content_package.json").write_text(
        '{"prompts":{"cover_result":{"reference_paths":["/tmp/ref.png"],"extra":{"reference_images_sent":false,"reference_image_fallback":"local_refs_not_supported"}}}}',
        encoding="utf-8",
    )
    (run_dir / "summary.md").write_text("# Summary", encoding="utf-8")
    client = TestClient(create_app(backend=service))

    readiness = client.get("/experiments/readiness")
    diagnostics = client.get("/experiments/content-production/diagnostics")
    listed = client.get("/workflows/content-production/runs", params={"case_id": "case1"})
    detail = client.get("/workflows/content-production/runs/case1/run1")
    acceptance = client.get("/workflows/content-production/runs/case1/run1/acceptance")

    assert readiness.status_code == 200
    assert "reference_images" in readiness.json()["data"]
    assert diagnostics.status_code == 200
    assert "recommended_actions" in diagnostics.json()["data"]
    assert "strict_reference_mode" in {row["name"] for row in diagnostics.json()["data"]["checks"]}
    assert (
        diagnostics.json()["data"]["routes"]["session_reference_image_generation_check"]
        == "/sessions/{session_id}/assets/reference-image-generation-check"
    )
    assert listed.status_code == 200
    assert listed.json()["data"]["runs"][0]["run_id"] == "run1"
    assert listed.json()["data"]["runs"][0]["proof_status"] == "blocked"
    assert detail.status_code == 200
    assert detail.json()["data"]["image_reference"]["status"] == "fallback"
    assert detail.json()["data"]["proof"]["status"] == "blocked"
    assert "cover_output" in detail.json()["data"]["proof"]["failed_checks"]
    assert detail.json()["data"]["acceptance"]["status"] == "rejected"
    assert "proof_ready" in detail.json()["data"]["acceptance"]["blocking_checks"]
    assert acceptance.status_code == 200
    assert acceptance.json()["data"]["acceptance"]["status"] == "rejected"
    artifact_catalog = {row["artifact_name"]: row for row in detail.json()["data"]["artifact_catalog"]}
    assert artifact_catalog["content_package.json"]["media_type"] == "application/json"
    assert artifact_catalog["summary.md"]["preview"]["text"] == "# Summary"


def test_fastapi_compares_content_production_runs(tmp_path):
    service = NoriBackend(experiment_runner=_project_runner(tmp_path))

    def write_run(run_id: str, *, sent: bool, with_cover: bool) -> None:
        run_dir = tmp_path / "cases" / "case1" / "runs" / run_id
        run_dir.mkdir(parents=True)
        if with_cover:
            covers_dir = run_dir / "covers"
            covers_dir.mkdir()
            (covers_dir / "cover.png").write_bytes(b"cover")
        (run_dir / "run.json").write_text('{"workflow":"content_production","status":"succeeded"}', encoding="utf-8")
        (run_dir / "workflow_run.json").write_text('{"status":"succeeded","stages":[]}', encoding="utf-8")
        (run_dir / "content_package.json").write_text("{}", encoding="utf-8")
        (run_dir / "input_manifest.json").write_text(
            json.dumps(
                {
                    "brief": {"sha256": f"brief-{run_id}"},
                    "assets": [{"asset_id": f"asset-{run_id}", "sha256": f"asset-{run_id}"}],
                    "market_evidence": {"queries": [run_id]},
                    "run_options": {"require_image_references": True, "human_gate_mode": "skip"},
                }
            ),
            encoding="utf-8",
        )
        (run_dir / "experiment_manifest.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "experiment": {"case_id": "case1", "run_id": run_id, "status": "succeeded"},
                    "inputs": {
                        "brief": {"sha256": f"brief-{run_id}"},
                        "assets": [{"asset_id": f"asset-{run_id}", "sha256": f"asset-{run_id}"}],
                        "market_evidence": {"queries": [run_id]},
                        "run_options": {"require_image_references": True, "human_gate_mode": "skip"},
                    },
                    "reference_images": {"status": "sent" if sent else "fallback", "required": True, "sent": sent},
                    "models": {"image": {"key": "image", "provider_id": "relay", "model_id": "gpt-image"}},
                }
            ),
            encoding="utf-8",
        )

    write_run("run_a", sent=True, with_cover=True)
    write_run("run_b", sent=False, with_cover=False)
    client = TestClient(create_app(backend=service))

    selected = client.post(
        "/experiments/content-production/cases/case1/selection",
        json={"run_id": "run_a", "decision": "selected", "reviewer": "operator", "reason": "reference sent"},
    )
    response = client.get(
        "/workflows/content-production/runs/compare",
        params=[("case_id", "case1"), ("run_id", "run_a"), ("run_id", "run_b")],
    )
    case_compare = client.get("/experiments/content-production/cases/case1/compare")
    invalid = client.get("/workflows/content-production/runs/compare", params={"case_id": "case1", "run_ids": "run_a"})
    filtered = client.get(
        "/workflows/content-production/runs",
        params={
            "case_id": "case1",
            "reference_status": "fallback",
            "proof_status": "blocked",
            "search": "run_b",
            "limit": 1,
        },
    )

    data = response.json()["data"]
    case_data = case_compare.json()["data"]
    assert selected.status_code == 201
    assert response.status_code == 200
    assert data["summary"]["ready_run_ids"] == ["run_a"]
    assert data["summary"]["blocked_run_ids"] == ["run_b"]
    assert data["differences"]["brief_sha256"]["changed"] is True
    assert data["runs"][1]["candidate"]["blocking_reasons"] == ["missing_cover", "strict_reference_not_sent"]
    assert case_compare.status_code == 200
    assert case_data["case_id"] == "case1"
    assert case_data["run_count"] == 2
    assert case_data["selected_run_id"] == "run_a"
    assert case_data["best_run_id"] == "run_a"
    assert case_data["recommended_run_id"] == "run_a"
    assert case_data["recommended_run"]["run_id"] == "run_a"
    candidates_by_id = {row["run_id"]: row for row in case_data["candidates"]}
    assert candidates_by_id["run_a"]["is_selected"] is True
    assert candidates_by_id["run_a"]["is_recommended"] is True
    assert candidates_by_id["run_b"]["candidate"]["blocking_reasons"] == ["missing_cover", "strict_reference_not_sent"]
    assert case_data["differences"]["brief_sha256"]["changed"] is True
    assert case_data["comparison_summary"]["ready_run_ids"] == ["run_a"]
    assert case_data["primary_action"]["action_id"] == "fix_reference_transfer"
    assert case_data["primary_action"] == case_data["next_actions"]["primary_action"]
    assert case_data["links"]["compare_runs"].startswith("/workflows/content-production/runs/compare?case_id=case1")
    assert invalid.status_code == 400
    assert "at least two run_ids" in invalid.json()["message"]
    filtered_data = filtered.json()["data"]
    assert filtered.status_code == 200
    assert filtered_data["total_count"] == 2
    assert filtered_data["filtered_count"] == 1
    assert filtered_data["returned_count"] == 1
    assert filtered_data["filters"]["proof_status"] == "blocked"
    assert filtered_data["runs"][0]["run_id"] == "run_b"


def test_fastapi_promotes_accepted_content_production_run(tmp_path):
    service = NoriBackend(experiment_runner=_project_runner(tmp_path))

    def write_run(run_id: str, *, accepted: bool) -> None:
        run_dir = tmp_path / "cases" / "case1" / "runs" / run_id
        covers_dir = run_dir / "covers"
        covers_dir.mkdir(parents=True)
        (covers_dir / "cover.png").write_bytes(b"cover")
        brief_text = "brief"
        market_evidence = {"queries": ["q"]}
        (run_dir / "original_brief.md").write_text(brief_text, encoding="utf-8")
        (run_dir / "run.json").write_text('{"workflow":"content_production","status":"succeeded"}', encoding="utf-8")
        (run_dir / "workflow_run.json").write_text(
            '{"workflow_name":"content_production","status":"succeeded","started_at":"t1","finished_at":"t2"}',
            encoding="utf-8",
        )
        (run_dir / "content_package.json").write_text('{"package_id":"pkg"}', encoding="utf-8")
        replay_request = {
            "session_id": "session_1",
            "brief_text": brief_text,
            "market_evidence": market_evidence,
            "config": {},
            "metadata": {},
        }
        (run_dir / "replay_request.json").write_text(json.dumps(replay_request, ensure_ascii=False), encoding="utf-8")
        fingerprints = {
            "brief_sha256": hashlib.sha256(brief_text.encode("utf-8")).hexdigest(),
            "replay_request_sha256": _file_sha256_for_test(run_dir / "replay_request.json"),
            "config_sha256": _json_sha256_for_test({}),
            "market_evidence_sha256": _json_sha256_for_test(market_evidence),
            "metadata_sha256": _json_sha256_for_test({}),
            "asset_sha256s": [],
        }
        (run_dir / "input_manifest.json").write_text(
            json.dumps(
                {
                    "replay_request_path": "replay_request.json",
                    "brief": {"text_path": "original_brief.md", "sha256": fingerprints["brief_sha256"]},
                    "assets": [
                        {
                            "asset_id": f"asset_{run_id}",
                            "path": f"/tmp/{run_id}.png",
                            "public_reference_url": f"https://cdn.nori.ai/{run_id}.png",
                        }
                    ],
                    "reference_transfer": {
                        "required": True,
                        "selected_count": 1,
                        "provider_fetchable_count": 1,
                    },
                    "market_evidence": {"queries": ["q"], "hot_note_count": 1},
                    "config": {},
                    "metadata": {},
                    "run_options": {"require_image_references": True, "human_gate_mode": "skip"},
                    "fingerprints": fingerprints,
                }
            ),
            encoding="utf-8",
        )
        status = "passed" if accepted else "pending"
        (run_dir / "experiment_manifest.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "experiment": {"case_id": "case1", "run_id": run_id, "status": "succeeded"},
                        "inputs": {
                            "brief": {"text_path": "original_brief.md", "sha256": fingerprints["brief_sha256"]},
                            "assets": [{"asset_id": f"asset_{run_id}", "path": f"/tmp/{run_id}.png"}],
                            "reference_transfer": {
                                "required": True,
                                "selected_count": 1,
                                "provider_fetchable_count": 1,
                            },
                            "market_evidence": {"queries": ["q"], "hot_note_count": 1},
                            "config": {},
                            "metadata": {},
                            "run_options": {"require_image_references": True, "human_gate_mode": "skip"},
                            "fingerprints": fingerprints,
                        },
                        "reference_images": {"status": "sent", "required": True, "sent": True, "selected_count": 1},
                        "evaluations": {"items": [], "summary": {"count": 1, "status": status, "score": 95 if accepted else None}},
                    }
                ),
            encoding="utf-8",
        )

    write_run("run_ready", accepted=True)
    write_run("run_pending", accepted=False)
    client = TestClient(create_app(backend=service))

    before_delivery = client.get("/experiments/content-production/cases/case1/delivery")
    preview_delivery = client.get(
        "/experiments/content-production/cases/case1/delivery",
        params={"allow_unpromoted": True},
    )
    blocked_delivery_export = client.get("/experiments/content-production/cases/case1/delivery/export")
    promoted = client.post(
        "/experiments/content-production/cases/case1/promotion",
        json={"run_id": "run_ready", "reviewer": "operator", "reason": "ship this"},
    )
    delivery = client.get("/experiments/content-production/cases/case1/delivery")
    delivery_export = client.get("/experiments/content-production/cases/case1/delivery/export")
    selection = client.get("/experiments/content-production/cases/case1/selection")
    next_actions = client.get("/experiments/content-production/cases/case1/next-actions")
    rejected = client.post(
        "/experiments/content-production/cases/case1/promotion",
        json={"run_id": "run_pending", "reviewer": "operator"},
    )
    overridden = client.post(
        "/experiments/content-production/cases/case1/promotion",
        json={"run_id": "run_pending", "reviewer": "lead", "allow_unaccepted": True, "reason": "manual override"},
    )

    data = promoted.json()["data"]
    before_data = before_delivery.json()["data"]
    preview_data = preview_delivery.json()["data"]
    delivery_data = delivery.json()["data"]
    assert before_delivery.status_code == 200
    assert before_data["ready"] is False
    assert before_data["status"] == "needs_promotion"
    assert before_data["blocking_reasons"] == ["not_promoted"]
    assert before_data["run_id"] == "run_ready"
    assert preview_delivery.status_code == 200
    assert preview_data["ready"] is True
    assert preview_data["status"] == "preview_ready"
    assert preview_data["warning_reasons"] == ["unpromoted_preview"]
    assert blocked_delivery_export.status_code == 400
    assert "case delivery is not ready: not_promoted" in blocked_delivery_export.json()["message"]
    assert promoted.status_code == 201
    assert data["promoted"] is True
    assert data["override"] is False
    assert data["selection"]["decision"] == "promoted"
    assert data["selection"]["reason"] == "ship this"
    assert data["acceptance"]["status"] == "accepted"
    assert data["links"]["artifact_inspection"] == (
        "/workflows/content-production/runs/case1/run_ready/artifacts/inspect"
    )
    assert delivery.status_code == 200
    assert delivery_data["ready"] is True
    assert delivery_data["status"] == "ready"
    assert delivery_data["promoted"] is True
    assert delivery_data["run_id"] == "run_ready"
    assert delivery_data["acceptance"]["status"] == "accepted"
    assert delivery_data["delivery"]["export_url"] == "/workflows/content-production/runs/case1/run_ready/export"
    assert delivery_data["delivery"]["content_package"]["available"] is True
    assert delivery_data["artifact_inspection"]["missing_core_artifacts"] == []
    assert delivery_data["case_compare"]["recommended_run_id"] == "run_ready"
    assert delivery_data["next_actions"]["status"] == "promoted"
    assert delivery_data["links"]["delivery_export"] == "/experiments/content-production/cases/case1/delivery/export"
    assert delivery_export.status_code == 200
    assert delivery_export.headers["content-type"] == "application/zip"
    assert 'filename="nori_content_production_delivery_case1_run_ready.zip"' in (
        delivery_export.headers["content-disposition"]
    )
    with zipfile.ZipFile(io.BytesIO(delivery_export.content)) as archive:
        names = sorted(archive.namelist())
        manifest = json.loads(archive.read("delivery_export_manifest.json"))
        delivery_json = json.loads(archive.read("delivery.json"))
    assert "run/content_package.json" in names
    assert "run/covers/cover.png" in names
    assert manifest["ready"] is True
    assert manifest["run_id"] == "run_ready"
    assert delivery_json["ready"] is True
    assert selection.status_code == 200
    assert selection.json()["data"]["current"]["decision"] == "promoted"
    assert next_actions.status_code == 200
    assert next_actions.json()["data"]["status"] == "promoted"
    assert next_actions.json()["data"]["primary_action"]["action_id"] == "export_promoted_run"
    assert rejected.status_code == 400
    assert "run is not accepted" in rejected.json()["message"]
    assert overridden.status_code == 201
    assert overridden.json()["data"]["override"] is True
    assert overridden.json()["data"]["selection"]["metadata"]["allow_unaccepted"] is True
    empty_delivery = client.get("/experiments/content-production/cases/case_empty/delivery")
    assert empty_delivery.status_code == 200
    assert empty_delivery.json()["data"]["ready"] is False
    assert empty_delivery.json()["data"]["status"] == "needs_run"
    assert empty_delivery.json()["data"]["blocking_reasons"] == ["no_run"]


def test_fastapi_records_and_reads_content_production_run_evaluations(tmp_path):
    service = NoriBackend(experiment_runner=_project_runner(tmp_path))
    run_dir = tmp_path / "cases" / "case1" / "runs" / "run1"
    covers_dir = run_dir / "covers"
    covers_dir.mkdir(parents=True)
    (covers_dir / "cover.png").write_bytes(b"cover")
    (run_dir / "run.json").write_text('{"workflow":"content_production","status":"succeeded"}', encoding="utf-8")
    (run_dir / "workflow_run.json").write_text('{"status":"succeeded","stages":[]}', encoding="utf-8")
    (run_dir / "content_package.json").write_text("{}", encoding="utf-8")
    (run_dir / "input_manifest.json").write_text('{"brief":{"sha256":"brief"},"assets":[]}', encoding="utf-8")
    (run_dir / "experiment_manifest.json").write_text(
        '{"schema_version":1,"experiment":{"case_id":"case1","run_id":"run1","status":"succeeded"},"reference_images":{"status":"not_selected","required":false,"sent":false},"artifacts":{"paths":{},"urls":{}}}',
        encoding="utf-8",
    )
    client = TestClient(create_app(backend=service))

    recorded = client.post(
        "/workflows/content-production/runs/case1/run1/evaluations",
        json={
            "reviewer": "operator",
            "status": "blocked",
            "score": 48,
            "notes": "参考图不够像",
            "issues": [{"code": "reference_fit", "severity": "high"}],
        },
    )
    listed = client.get("/workflows/content-production/runs/case1/run1/evaluations")
    detail = client.get("/workflows/content-production/runs/case1/run1")
    invalid = client.post(
        "/workflows/content-production/runs/case1/run1/evaluations",
        json={"status": "great", "score": 101},
    )

    assert recorded.status_code == 201
    assert recorded.json()["data"]["summary"]["status"] == "blocked"
    assert recorded.json()["data"]["summary"]["high_issue_count"] == 1
    assert listed.status_code == 200
    assert listed.json()["data"]["evaluations"][0]["reviewer"] == "operator"
    assert detail.json()["data"]["evaluations"]["summary"]["status"] == "blocked"
    assert detail.json()["data"]["experiment_manifest"]["evaluations"]["summary"]["status"] == "blocked"
    assert (run_dir / "experiment_evaluations.json").is_file()
    assert invalid.status_code == 400
    assert "unsupported evaluation status" in invalid.json()["message"]


def test_fastapi_builds_content_production_evaluation_draft(tmp_path):
    service = NoriBackend(experiment_runner=_project_runner(tmp_path))
    run_dir = tmp_path / "cases" / "case1" / "runs" / "run1"
    run_dir.mkdir(parents=True)
    (run_dir / "run.json").write_text('{"workflow":"content_production","status":"succeeded"}', encoding="utf-8")
    (run_dir / "workflow_run.json").write_text('{"status":"succeeded","stages":[]}', encoding="utf-8")
    (run_dir / "input_manifest.json").write_text(
        '{"session_id":"session_1","task_id":"task_1","assets":[],"market_evidence":{"queries":["Holly"]}}',
        encoding="utf-8",
    )
    (run_dir / "replay_request.json").write_text(
        '{"goal":"做品牌种草","config":{"brand_name":"Holly","topic":"怪趣文创","goals":["做品牌种草"]}}',
        encoding="utf-8",
    )
    (run_dir / "content_package.json").write_text(
        '{"package_id":"pkg","task_id":"task_1","platform":"xhs","title":"Holly 怪趣文创","body":"Holly 怪趣文创种草内容","tags":["Holly"],"prompts":{"cover_result":{"prompt":"Holly 怪趣文创封面"}}}',
        encoding="utf-8",
    )
    client = TestClient(create_app(backend=service))

    draft = client.post(
        "/workflows/content-production/runs/case1/run1/evaluations/draft",
        json={"reviewer": "auto", "persist": False},
    )
    persisted = client.post(
        "/workflows/content-production/runs/case1/run1/evaluations/draft",
        json={"reviewer": "auto", "persist": True, "metadata": {"batch_id": "batch_1"}},
    )

    assert draft.status_code == 200
    assert draft.json()["data"]["persisted"] is False
    assert draft.json()["data"]["draft"]["status"] in {"passed", "needs_revision", "blocked"}
    assert draft.json()["data"]["draft"]["metrics"]["review_count"] == 4
    assert "run_health" in draft.json()["data"]["draft"]["metrics"]["status_by_reviewer"]
    assert draft.json()["data"]["context"]["visual_reference_review"]["status"] == "not_applicable"
    assert persisted.status_code == 200
    assert persisted.json()["data"]["persisted"] is True
    assert persisted.json()["data"]["recorded"]["evaluation"]["metadata"]["batch_id"] == "batch_1"
    assert (run_dir / "experiment_evaluations.json").is_file()


def test_fastapi_builds_and_records_case_level_content_production_evaluations(tmp_path):
    service = NoriBackend(experiment_runner=_project_runner(tmp_path))
    run_dir = tmp_path / "cases" / "case1" / "runs" / "run1"
    run_dir.mkdir(parents=True)
    (run_dir / "run.json").write_text('{"workflow":"content_production","status":"succeeded"}', encoding="utf-8")
    (run_dir / "workflow_run.json").write_text('{"status":"succeeded","stages":[]}', encoding="utf-8")
    (run_dir / "input_manifest.json").write_text(
        '{"session_id":"session_1","task_id":"task_1","assets":[],"market_evidence":{"queries":["Holly"]}}',
        encoding="utf-8",
    )
    (run_dir / "replay_request.json").write_text(
        '{"goal":"做品牌种草","config":{"brand_name":"Holly","topic":"怪趣文创","goals":["做品牌种草"]}}',
        encoding="utf-8",
    )
    (run_dir / "content_package.json").write_text(
        '{"package_id":"pkg","task_id":"task_1","platform":"xhs","title":"Holly 怪趣文创","body":"Holly 怪趣文创种草内容","tags":["Holly"],"prompts":{"cover_result":{"prompt":"Holly 怪趣文创封面"}}}',
        encoding="utf-8",
    )
    client = TestClient(create_app(backend=service))

    selected = client.post(
        "/experiments/content-production/cases/case1/selection",
        json={"run_id": "run1", "decision": "selected", "reviewer": "operator"},
    )
    draft = client.post(
        "/experiments/content-production/cases/case1/evaluations/draft",
        json={"reviewer": "auto", "persist": True, "metadata": {"batch_id": "case_batch"}},
    )
    recorded = client.post(
        "/experiments/content-production/cases/case1/evaluations",
        json={"status": "passed", "score": 91, "reviewer": "operator", "notes": "ship"},
    )

    assert selected.status_code == 201
    assert draft.status_code == 200
    draft_data = draft.json()["data"]
    assert draft_data["source"] == "case_evaluation_draft"
    assert draft_data["source_run_id"] == "run1"
    assert draft_data["source_run_selector"] == "selection"
    assert draft_data["persisted"] is True
    assert draft_data["recorded"]["evaluation"]["metadata"]["batch_id"] == "case_batch"
    assert recorded.status_code == 201
    recorded_data = recorded.json()["data"]
    assert recorded_data["source"] == "case_evaluation"
    assert recorded_data["source_run_id"] == "run1"
    assert recorded_data["summary"]["status"] == "passed"
    assert (run_dir / "experiment_evaluations.json").is_file()


def test_fastapi_serves_content_production_run_artifacts_from_backend(tmp_path):
    service = NoriBackend(experiment_runner=_project_runner(tmp_path))
    run_dir = tmp_path / "cases" / "case1" / "runs" / "run1"
    covers_dir = run_dir / "covers"
    covers_dir.mkdir(parents=True)
    (run_dir / "run.json").write_text('{"workflow":"content_production","status":"succeeded"}', encoding="utf-8")
    (run_dir / "workflow_run.json").write_text('{"status":"succeeded","stages":[]}', encoding="utf-8")
    (run_dir / "summary.md").write_text("# Summary", encoding="utf-8")
    (run_dir / "content_package.json").write_text("{}", encoding="utf-8")
    (covers_dir / "cover.png").write_bytes(b"cover-png")
    client = TestClient(create_app(backend=service))

    detail = client.get("/workflows/content-production/runs/case1/run1").json()["data"]
    summary = client.get(detail["artifact_urls"]["summary.md"])
    cover = client.get(detail["cover_urls"][0])
    blocked = client.get("/workflows/content-production/runs/case1/run1/artifacts/../run.json")

    assert detail["artifact_urls"]["summary.md"] == "/workflows/content-production/runs/case1/run1/artifacts/summary.md"
    assert detail["cover_urls"] == ["/workflows/content-production/runs/case1/run1/artifacts/covers/cover.png"]
    assert summary.status_code == 200
    assert summary.text == "# Summary"
    assert cover.status_code == 200
    assert cover.content == b"cover-png"
    assert blocked.status_code in {400, 404}


def test_fastapi_workflow_catalog_exposes_content_production_without_running_it():
    client = TestClient(create_app())

    response = client.get("/workflows/content-production")

    assert response.status_code == 200
    workflow = response.json()["data"]
    assert workflow["workflow_id"] == "content-production"
    assert workflow["owner"] == "nori.workflows.content_production"
    assert workflow["human_gate_default"] == "skip"
    assert "content_design_spec" in workflow["stages"]
    assert "content_package" in workflow["stages"]


def test_fastapi_exposes_content_generation_options_and_actions():
    client = TestClient(create_app())

    capabilities = client.get("/capabilities").json()["data"]
    options = client.get("/content/generation/options").json()["data"]
    cover_options = client.get("/content/generation/options/cover_strategy").json()["data"]
    actions = client.get("/content/generation/actions").json()["data"]
    cover_action = client.get("/content/generation/actions/content.cover").json()["data"]

    assert "content_generation" in {row["capability_id"] for row in capabilities["capabilities"]}
    content_capability = next(row for row in capabilities["capabilities"] if row["capability_id"] == "content_generation")
    assert (
        content_capability["routes"]["session_reference_image_generation_check"]
        == "/sessions/{session_id}/assets/reference-image-generation-check"
    )
    assert "image_source" in options["option_groups"]
    assert "cover_strategy" in options["option_groups"]
    assert {row["option_id"] for row in cover_options["options"]} >= {"auto", "manual_references", "text_only_prompt"}
    assert "content.cover" in {row["action_id"] for row in actions["actions"]}
    assert "workflow.content_production" in {row["action_id"] for row in actions["actions"]}
    assert cover_action["route"] == "/content/generation/cover"
    assert cover_action["execution_mode"] == "direct_agent"
    assert cover_action["requires_image_model"] is True


def test_fastapi_content_generation_plan_can_choose_direct_action_without_workflow_id():
    client = TestClient(create_app())

    response = client.post(
        "/content/generation/plan",
        json={
            "platform": "xhs",
            "artifact_type": "image_text_post",
            "cover_strategy": "manual_references",
            "image_source": "uploaded_assets",
        },
    )

    assert response.status_code == 200
    plan = response.json()["data"]
    assert plan["selected_action_id"] == "content.cover"
    assert plan["selected_route"] == "/content/generation/cover"
    assert plan["workflow_id"] == ""
    assert plan["requires_workflow_id"] is False
    assert plan["normalized_options"]["entry_mode"] == "direct_action"


def test_fastapi_content_generation_plan_can_choose_workflow_when_requested():
    client = TestClient(create_app())

    response = client.post(
        "/content/generation/plan",
        json={
            "goal": "端到端生成小红书内容",
            "entry_mode": "workflow",
        },
    )

    assert response.status_code == 200
    plan = response.json()["data"]
    assert plan["selected_action_id"] == "workflow.content_production"
    assert plan["workflow_id"] == "content-production"
    assert plan["selected_route"] == "/workflows/content-production/runs"
    assert plan["requires_workflow_id"] is True


def test_fastapi_workflow_resolver_supports_generic_and_direct_modes():
    client = TestClient(create_app())

    workflow = client.post("/workflows/resolve", json={"capability_id": "content_generation"})
    direct = client.post(
        "/workflows/resolve",
        json={"capability_id": "content_generation", "prefer_direct_action": True},
    )

    assert workflow.status_code == 200
    assert workflow.json()["data"]["selected_workflow_id"] == "content-production"
    assert workflow.json()["data"]["entry_mode"] == "workflow"
    assert direct.status_code == 200
    assert direct.json()["data"]["selected_workflow_id"] == ""
    assert direct.json()["data"]["entry_mode"] == "direct_action"


def test_fastapi_returns_clear_errors_for_invalid_request_shapes(tmp_path):
    service = NoriBackend(experiment_runner=_project_runner(tmp_path))
    client = TestClient(create_app(backend=service))

    session = client.post("/sessions", json={}).json()["data"]
    missing_goal = client.post(f"/sessions/{session['session_id']}/tasks", json={"goal": ""})
    missing_session = client.post("/sessions/session_missing/tasks", json={"goal": "run"})
    invalid_shape = client.post("/sessions", json=[])
    not_found = client.get("/missing")

    assert missing_goal.status_code == 400
    assert missing_goal.json()["message"] == "goal is required"
    assert missing_session.status_code == 404
    assert missing_session.json()["message"] == "session not found: session_missing"
    assert invalid_shape.status_code == 422
    assert invalid_shape.json()["message"] == "request validation failed"
    assert not_found.status_code == 404


def test_create_app_can_use_injected_service_instance(tmp_path):
    service = NoriBackend(experiment_runner=_project_runner(tmp_path))
    client = TestClient(create_app(backend=service))

    created = client.post("/sessions", json={"user_id": "shared"})

    session_id = created.json()["data"]["session_id"]
    assert service.session_manager.get_session(session_id) is not None
