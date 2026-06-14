"""Experiment job routes."""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from ..contracts import ExperimentJobCancelRequest, api_ok
from .service_contracts import ExperimentJobRouteServiceProtocol


def build_experiment_jobs_router(service: ExperimentJobRouteServiceProtocol) -> APIRouter:
    router = APIRouter(tags=["experiment-jobs"])

    @router.get("/experiments/jobs", summary="List background experiment jobs")
    def list_experiment_jobs(
        status: str = "",
        session_id: str = "",
        case_id: str = "",
        job_type: str = "",
    ) -> dict[str, Any]:
        return api_ok(
            service.job_service.list_experiment_jobs(
                status=status,
                session_id=session_id,
                case_id=case_id,
                job_type=job_type,
            )
        )

    @router.get("/experiments/jobs/{job_id}", summary="Inspect one background experiment job")
    def get_experiment_job(job_id: str) -> dict[str, Any]:
        return api_ok(service.job_service.get_experiment_job(job_id))

    @router.post("/experiments/jobs/{job_id}/cancel", summary="Request cancellation for one background experiment job")
    def cancel_experiment_job(job_id: str, request: ExperimentJobCancelRequest) -> dict[str, Any]:
        return api_ok(service.job_service.cancel_experiment_job(job_id, request))

    return router
