"""Backend service facade used by FastAPI routes."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from nori.sessions import SessionManager

from .content import ContentGenerationCatalog
from .jobs import InProcessExperimentJobStore
from .route_services import BackendRouteServices
from .services import BackendServiceBundle
from .workflows import WorkflowCatalog


class NoriBackend:
    """Composition root for the product backend service graph."""

    def __init__(
        self,
        *,
        session_manager: SessionManager | None = None,
        workflow_catalog: WorkflowCatalog | None = None,
        content_catalog: ContentGenerationCatalog | None = None,
        experiment_runner: Any | None = None,
        job_store: InProcessExperimentJobStore | None = None,
        reference_publisher: Any | None = None,
        upload_root: str | Path | None = None,
        enforce_model_readiness: bool | None = None,
        service_bundle: BackendServiceBundle | None = None,
    ) -> None:
        bundle = service_bundle or BackendServiceBundle.create(
            session_manager=session_manager,
            workflow_catalog=workflow_catalog,
            content_catalog=content_catalog,
            experiment_runner=experiment_runner,
            job_store=job_store,
            reference_publisher=reference_publisher,
            upload_root=upload_root,
            enforce_model_readiness=enforce_model_readiness,
        )
        self.service_bundle = bundle
        self.routes = BackendRouteServices.from_bundle(bundle)

        self.catalog_service = bundle.catalog_service
        self.experiment_runner = bundle.experiment_runner
        self.enforce_model_readiness = bundle.enforce_model_readiness
        self.content_production_admin = bundle.content_production_admin
        self.content_production_console = bundle.content_production_console
        self.session_manager = bundle.session_manager
        self.session_store = bundle.session_store
        self.upload_root = bundle.upload_root
        self.session_asset_service = bundle.session_asset_service
        self.reference_image_service = bundle.reference_image_service
        self.reference_publisher = bundle.reference_publisher
        self.job_store = bundle.job_store
        self.experiment_job_service = bundle.experiment_job_service
        self.content_production_run_service = bundle.content_production_run_service

    def health(self) -> dict[str, str]:
        return self.routes.system.health()

    def list_capabilities(self) -> dict[str, Any]:
        return self.catalog_service.list_capabilities()
