"""Runtime service composition for the FastAPI backend facade."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from nori.sessions import SessionManager

from ..content import ContentGenerationCatalog
from ..experiments import ContentProductionExperimentRunner, PROJECT_ROOT
from ..jobs import InProcessExperimentJobStore
from ..workflows import WorkflowCatalog
from .catalogs import BackendCatalogService
from .content_production_console import BackendContentProductionConsoleService
from .content_production_runs import BackendContentProductionRunService
from .experiment_jobs import BackendExperimentJobService
from .reference_images import BackendReferenceImageService
from .session_assets import BackendSessionAssetService
from .session_store import BackendSessionStore


@dataclass(frozen=True)
class BackendServiceBundle:
    """Constructed backend service graph used by NoriBackend."""

    catalog_service: BackendCatalogService
    experiment_runner: Any
    enforce_model_readiness: bool
    project_root: Path
    content_production_console: BackendContentProductionConsoleService
    session_manager: SessionManager
    session_store: BackendSessionStore
    upload_root: Path
    session_asset_service: BackendSessionAssetService
    reference_image_service: BackendReferenceImageService
    reference_publisher: Any
    job_store: InProcessExperimentJobStore
    experiment_job_service: BackendExperimentJobService
    content_production_run_service: BackendContentProductionRunService

    @classmethod
    def create(
        cls,
        *,
        session_manager: SessionManager | None = None,
        workflow_catalog: WorkflowCatalog | None = None,
        content_catalog: ContentGenerationCatalog | None = None,
        experiment_runner: Any | None = None,
        job_store: InProcessExperimentJobStore | None = None,
        reference_publisher: Any | None = None,
        upload_root: str | Path | None = None,
        enforce_model_readiness: bool | None = None,
    ) -> "BackendServiceBundle":
        catalog_service = BackendCatalogService(
            workflow_catalog=workflow_catalog,
            content_catalog=content_catalog,
        )
        runner = experiment_runner or ContentProductionExperimentRunner()
        should_enforce_model_readiness = (
            isinstance(runner, ContentProductionExperimentRunner)
            if enforce_model_readiness is None
            else bool(enforce_model_readiness)
        )
        project_root = experiment_project_root(runner)
        content_production_console = BackendContentProductionConsoleService(project_root=project_root)
        manager = session_manager or SessionManager(storage_root=project_root / "data" / "backend" / "sessions")
        session_store = BackendSessionStore(manager)
        resolved_upload_root = Path(upload_root or project_root / "data" / "backend" / "uploads")
        session_asset_service = BackendSessionAssetService(
            session_store=session_store,
            upload_root=resolved_upload_root,
        )
        reference_image_service = BackendReferenceImageService(
            session_store=session_store,
            reference_publisher=reference_publisher,
        )
        resolved_job_store = job_store or InProcessExperimentJobStore(
            storage_root=project_root / "data" / "backend" / "jobs"
        )
        experiment_job_service = BackendExperimentJobService(
            job_store=resolved_job_store,
            session_store=session_store,
        )
        content_production_run_service = BackendContentProductionRunService(
            experiment_runner=runner,
            session_store=session_store,
            job_store=resolved_job_store,
            enforce_model_readiness=should_enforce_model_readiness,
        )
        experiment_job_service.sync_interrupted_experiment_jobs()
        return cls(
            catalog_service=catalog_service,
            experiment_runner=runner,
            enforce_model_readiness=should_enforce_model_readiness,
            project_root=project_root,
            content_production_console=content_production_console,
            session_manager=manager,
            session_store=session_store,
            upload_root=resolved_upload_root,
            session_asset_service=session_asset_service,
            reference_image_service=reference_image_service,
            reference_publisher=reference_image_service.reference_publisher,
            job_store=resolved_job_store,
            experiment_job_service=experiment_job_service,
            content_production_run_service=content_production_run_service,
        )


def experiment_project_root(experiment_runner: Any) -> Path:
    return Path(getattr(experiment_runner, "project_root", PROJECT_ROOT))
