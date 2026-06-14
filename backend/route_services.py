"""Route-facing backend service facets."""
from __future__ import annotations

from dataclasses import dataclass

from .services import (
    BackendCatalogService,
    BackendContentProductionAdminService,
    BackendContentProductionConsoleService,
    BackendContentProductionRunService,
    BackendExperimentJobService,
    BackendReferenceImageService,
    BackendServiceBundle,
    BackendSessionAssetService,
)


@dataclass(frozen=True)
class SystemRouteService:
    catalog_service: BackendCatalogService

    def health(self) -> dict[str, str]:
        return {
            "status": "ok",
            "service": "nori-backend",
            "runtime": "fastapi",
        }


@dataclass(frozen=True)
class WorkflowRouteService:
    catalog_service: BackendCatalogService


@dataclass(frozen=True)
class ContentGenerationRouteService:
    catalog_service: BackendCatalogService


@dataclass(frozen=True)
class ContentProductionAdminRouteService:
    admin_service: BackendContentProductionAdminService
    console_service: BackendContentProductionConsoleService
    reference_image_service: BackendReferenceImageService
    run_service: BackendContentProductionRunService


@dataclass(frozen=True)
class ExperimentJobRouteService:
    job_service: BackendExperimentJobService


@dataclass(frozen=True)
class SessionRouteService:
    session_asset_service: BackendSessionAssetService
    reference_image_service: BackendReferenceImageService


@dataclass(frozen=True)
class ContentProductionRunRouteService:
    run_service: BackendContentProductionRunService
    console_service: BackendContentProductionConsoleService


@dataclass(frozen=True)
class ContentProductionCaseRouteService:
    run_service: BackendContentProductionRunService
    console_service: BackendContentProductionConsoleService


@dataclass(frozen=True)
class BackendRouteServices:
    """Domain-specific service collection for FastAPI route registration."""

    system: SystemRouteService
    workflows: WorkflowRouteService
    content_generation: ContentGenerationRouteService
    content_production_admin: ContentProductionAdminRouteService
    experiment_jobs: ExperimentJobRouteService
    sessions: SessionRouteService
    content_production_runs: ContentProductionRunRouteService
    content_production_cases: ContentProductionCaseRouteService

    @classmethod
    def from_bundle(cls, bundle: BackendServiceBundle) -> "BackendRouteServices":
        return cls(
            system=SystemRouteService(catalog_service=bundle.catalog_service),
            workflows=WorkflowRouteService(catalog_service=bundle.catalog_service),
            content_generation=ContentGenerationRouteService(catalog_service=bundle.catalog_service),
            content_production_admin=ContentProductionAdminRouteService(
                admin_service=bundle.content_production_admin,
                console_service=bundle.content_production_console,
                reference_image_service=bundle.reference_image_service,
                run_service=bundle.content_production_run_service,
            ),
            experiment_jobs=ExperimentJobRouteService(job_service=bundle.experiment_job_service),
            sessions=SessionRouteService(
                session_asset_service=bundle.session_asset_service,
                reference_image_service=bundle.reference_image_service,
            ),
            content_production_runs=ContentProductionRunRouteService(
                run_service=bundle.content_production_run_service,
                console_service=bundle.content_production_console,
            ),
            content_production_cases=ContentProductionCaseRouteService(
                run_service=bundle.content_production_run_service,
                console_service=bundle.content_production_console,
            ),
        )
