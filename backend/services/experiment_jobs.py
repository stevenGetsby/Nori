"""Experiment job lifecycle service."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from nori.sessions import SessionEvent

from ..contracts import ApiError, ExperimentJobCancelRequest
from ..jobs import InProcessExperimentJobStore
from .session_store import BackendSessionStore


class BackendExperimentJobService:
    """Owns job lookup/cancellation and session task status synchronization."""

    def __init__(
        self,
        *,
        job_store: InProcessExperimentJobStore,
        session_store: BackendSessionStore,
    ) -> None:
        self.job_store = job_store
        self.session_store = session_store
        self.session_manager = session_store.session_manager

    def get_experiment_job(self, job_id: str) -> dict[str, Any]:
        job = self.job_store.get(job_id)
        if job is None:
            raise ApiError(f"experiment job not found: {job_id}", status_code=404)
        return {"job": job}

    def cancel_experiment_job(self, job_id: str, request: ExperimentJobCancelRequest) -> dict[str, Any]:
        job = self.job_store.cancel(job_id, reason=str(request.reason or ""))
        if job is None:
            raise ApiError(f"experiment job not found: {job_id}", status_code=404)
        return {"job": job, "session": self.sync_cancelled_experiment_job(job)}

    def list_experiment_jobs(
        self,
        *,
        status: str = "",
        session_id: str = "",
        case_id: str = "",
        job_type: str = "",
    ) -> dict[str, Any]:
        return {
            "jobs": self.job_store.list_jobs(
                status=status,
                session_id=session_id,
                case_id=case_id,
                job_type=job_type,
            )
        }

    def sync_interrupted_experiment_jobs(self) -> None:
        for job in self.job_store.list_jobs(status="interrupted"):
            metadata = job.get("metadata") if isinstance(job.get("metadata"), dict) else {}
            session_id = str(metadata.get("session_id") or "").strip()
            task_id = str(metadata.get("task_id") or "").strip()
            if not session_id or not task_id:
                continue
            session = self.session_store.get_session(session_id)
            if session is None:
                continue
            task = self.session_store.find_task(session, task_id)
            if task is None:
                continue
            if task.status not in {"succeeded", "failed", "cancelled", "interrupted"}:
                task.status = "interrupted"
            if not session_has_job_event(
                session.events,
                event_type="workflow_run_interrupted",
                job_id=str(job.get("job_id") or ""),
            ):
                session.events.append(
                    SessionEvent(
                        event_type="workflow_run_interrupted",
                        payload={
                            "job_id": str(job.get("job_id") or ""),
                            "job_status": "interrupted",
                            "task_id": task_id,
                            "error": dict(job.get("error") or {}) if isinstance(job.get("error"), dict) else {},
                        },
                    )
                )
            session.updated_at = utc_now_iso()
            self.session_store.save_session(session_id)

    def sync_cancelled_experiment_job(self, job: dict[str, Any]) -> dict[str, Any]:
        metadata = job.get("metadata") if isinstance(job.get("metadata"), dict) else {}
        session_id = str(metadata.get("session_id") or "").strip()
        task_id = str(metadata.get("task_id") or "").strip()
        if not session_id or not task_id:
            return {}
        session = self.session_store.get_session(session_id)
        if session is None:
            return {"session_id": session_id, "task_id": task_id, "task_found": False}
        task = self.session_store.find_task(session, task_id)
        if task is None:
            return {"session_id": session_id, "task_id": task_id, "task_found": False}

        job_status = str(job.get("status") or "")
        if job_status == "cancelled":
            task_status = "cancelled"
            event_type = "workflow_run_cancelled"
        elif job_status == "cancelling":
            task_status = "cancelling"
            event_type = "workflow_run_cancel_requested"
        else:
            return {
                "session_id": session_id,
                "task_id": task_id,
                "task_found": True,
                "task_status": task.status,
                "event_type": "",
            }

        if task.status not in {"succeeded", "failed", "cancelled"}:
            task.status = task_status
        if not session_has_job_event(session.events, event_type=event_type, job_id=str(job.get("job_id") or "")):
            cancel_request = metadata.get("cancel_request") if isinstance(metadata.get("cancel_request"), dict) else {}
            session.events.append(
                SessionEvent(
                    event_type=event_type,
                    payload={
                        "job_id": str(job.get("job_id") or ""),
                        "job_status": job_status,
                        "task_id": task_id,
                        "reason": str(cancel_request.get("reason") or ""),
                    },
                )
            )
        session.updated_at = utc_now_iso()
        self.session_store.save_session(session_id)
        return {
            "session_id": session_id,
            "task_id": task_id,
            "task_found": True,
            "task_status": task.status,
            "event_type": event_type,
        }


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def session_has_job_event(events: list[SessionEvent], *, event_type: str, job_id: str) -> bool:
    return any(
        event.event_type == event_type and str((event.payload or {}).get("job_id") or "") == job_id
        for event in events
    )
