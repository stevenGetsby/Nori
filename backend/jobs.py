"""In-process experiment job tracking for local/backend runs."""
from __future__ import annotations

from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime
import json
from pathlib import Path
from threading import RLock
from typing import Any, Callable
from uuid import uuid4

from nori.core.paths import infer_project_root_from_backend_jobs_path, make_portable_paths

from .job_presenters import content_run_links, enrich_content_run_result, job_actions


def _now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


@dataclass
class ExperimentJob:
    """Inspectable in-process background job record."""

    job_id: str
    job_type: str
    status: str = "queued"
    created_at: str = field(default_factory=_now_iso)
    started_at: str = ""
    finished_at: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    result: dict[str, Any] | None = None
    error: dict[str, Any] | None = None
    cancel_requested: bool = False

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ExperimentJob":
        return cls(
            job_id=str(data.get("job_id") or ""),
            job_type=str(data.get("job_type") or ""),
            status=str(data.get("status") or "queued"),
            created_at=str(data.get("created_at") or ""),
            started_at=str(data.get("started_at") or ""),
            finished_at=str(data.get("finished_at") or ""),
            metadata=dict(data.get("metadata") or {}),
            result=dict(data.get("result") or {}) if data.get("result") is not None else None,
            error=dict(data.get("error") or {}) if data.get("error") is not None else None,
            cancel_requested=bool(data.get("cancel_requested")),
        )

    def to_dict(self) -> dict[str, Any]:
        links = {
            "self": f"/experiments/jobs/{self.job_id}",
            "cancel": f"/experiments/jobs/{self.job_id}/cancel",
        }
        result = enrich_content_run_result(self.result, metadata=self.metadata)
        links.update(content_run_links(metadata=self.metadata, result=result))
        return {
            "job_id": self.job_id,
            "job_type": self.job_type,
            "status": self.status,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "metadata": dict(self.metadata),
            "result": result,
            "error": dict(self.error or {}) if self.error is not None else None,
            "cancel_requested": bool(self.cancel_requested),
            "links": links,
            "actions": job_actions(
                status=self.status,
                links=links,
                result=result,
                cancel_requested=bool(self.cancel_requested),
            ),
        }


class InProcessExperimentJobStore:
    """Small local job store for long-running experiment requests.

    This is intentionally process-local. It gives the product/backend surface a
    real pollable execution mode for local experiments without pretending to be
    a durable production queue.
    """

    def __init__(self, *, max_workers: int = 2, storage_root: str | Path | None = None) -> None:
        self._jobs: dict[str, ExperimentJob] = {}
        self._futures: dict[str, Future] = {}
        self._lock = RLock()
        self.storage_root = Path(storage_root) if storage_root is not None else None
        self.portable_root = _portable_root_for_storage(self.storage_root)
        self._load()
        self._executor = ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="nori-experiment")

    def submit(
        self,
        *,
        job_type: str,
        metadata: dict[str, Any] | None = None,
        target: Callable[[], dict[str, Any]],
    ) -> dict[str, Any]:
        job = self.create(job_type=job_type, metadata=metadata)
        self.start(job["job_id"], target=target)
        return job

    def create(
        self,
        *,
        job_type: str,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        job = ExperimentJob(
            job_id=f"job_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid4().hex[:8]}",
            job_type=job_type,
            metadata=dict(metadata or {}),
        )
        with self._lock:
            self._jobs[job.job_id] = job
            self._persist_locked(job)
            return self._job_to_dict(job)

    def start(self, job_id: str, *, target: Callable[[], dict[str, Any]]) -> None:
        with self._lock:
            if job_id not in self._jobs:
                raise KeyError(job_id)
            if self._jobs[job_id].status == "cancelled":
                return
        future = self._executor.submit(self._run, job_id, target)
        with self._lock:
            self._futures[job_id] = future

    def get(self, job_id: str) -> dict[str, Any] | None:
        with self._lock:
            job = self._jobs.get(job_id)
            return self._job_to_dict(job) if job is not None else None

    def cancel(self, job_id: str, *, reason: str = "") -> dict[str, Any] | None:
        with self._lock:
            job = self._jobs.get(job_id)
            if job is None:
                return None
            if job.status in {"succeeded", "failed", "cancelled", "interrupted"}:
                return job.to_dict()
            job.cancel_requested = True
            metadata = dict(job.metadata)
            metadata["cancel_request"] = {
                "requested_at": _now_iso(),
                "reason": reason or "operator requested cancellation",
            }
            job.metadata = metadata
            future = self._futures.get(job_id)
            if job.status == "queued" and (future is None or future.cancel()):
                job.status = "cancelled"
                job.finished_at = _now_iso()
                job.error = {
                    "error_type": "JobCancelled",
                    "error": reason or "job was cancelled before it started",
                }
            elif job.status in {"queued", "running", "cancelling"}:
                job.status = "cancelling"
                job.error = {
                    "error_type": "CancellationRequested",
                    "error": reason or "cancellation requested; running in-process work may finish before it can stop",
                }
            self._persist_locked(job)
            return self._job_to_dict(job)

    def list_jobs(
        self,
        *,
        status: str = "",
        session_id: str = "",
        case_id: str = "",
        job_type: str = "",
    ) -> list[dict[str, Any]]:
        with self._lock:
            jobs = [self._job_to_dict(job) for job in self._jobs.values()]
        if status:
            jobs = [job for job in jobs if job.get("status") == status]
        if session_id:
            jobs = [job for job in jobs if (job.get("metadata") or {}).get("session_id") == session_id]
        if case_id:
            jobs = [job for job in jobs if (job.get("metadata") or {}).get("case_id") == case_id]
        if job_type:
            jobs = [job for job in jobs if job.get("job_type") == job_type]
        return sorted(jobs, key=lambda row: str(row.get("created_at") or ""), reverse=True)

    def _run(self, job_id: str, target: Callable[[], dict[str, Any]]) -> None:
        with self._lock:
            job = self._jobs[job_id]
            if job.status == "cancelled":
                self._persist_locked(job)
                return
            job.status = "cancelling" if job.cancel_requested else "running"
            job.started_at = _now_iso()
            self._persist_locked(job)
        try:
            result = target()
        except Exception as exc:  # noqa: BLE001
            with self._lock:
                job = self._jobs[job_id]
                job.status = "failed"
                job.finished_at = _now_iso()
                job.error = {"error_type": type(exc).__name__, "error": str(exc)}
                failure_result = getattr(exc, "failure_result", None)
                if isinstance(failure_result, dict):
                    job.result = dict(failure_result)
                self._persist_locked(job)
            return
        with self._lock:
            job = self._jobs[job_id]
            job.status = str(result.get("status") or "succeeded")
            if job.status not in {"succeeded", "failed", "cancelled"}:
                job.status = "succeeded"
            job.finished_at = _now_iso()
            job.result = dict(result)
            if job.status == "succeeded":
                job.error = None
            self._persist_locked(job)

    def _load(self) -> None:
        if self.storage_root is None or not self.storage_root.is_dir():
            return
        for path in sorted(self.storage_root.glob("job_*.json")):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except Exception:  # noqa: BLE001
                continue
            if not isinstance(data, dict):
                continue
            job = ExperimentJob.from_dict(data)
            if not job.job_id:
                continue
            if job.status in {"queued", "running", "cancelling"}:
                job.status = "interrupted"
                job.finished_at = job.finished_at or _now_iso()
                job.error = job.error or {
                    "error_type": "ProcessInterrupted",
                    "error": "job was loaded from disk without an active in-process worker",
                }
            self._jobs[job.job_id] = job
            self._persist_locked(job)

    def _persist_locked(self, job: ExperimentJob) -> None:
        if self.storage_root is None:
            return
        self.storage_root.mkdir(parents=True, exist_ok=True)
        path = self.storage_root / f"{job.job_id}.json"
        path.write_text(json.dumps(self._job_to_dict(job), ensure_ascii=False, indent=2), encoding="utf-8")

    def _job_to_dict(self, job: ExperimentJob) -> dict[str, Any]:
        return make_portable_paths(job.to_dict(), self.portable_root)


def _portable_root_for_storage(storage_root: Path | None) -> Path | None:
    if storage_root is None:
        return None
    return infer_project_root_from_backend_jobs_path(storage_root) or storage_root.parent


__all__ = ["ExperimentJob", "InProcessExperimentJobStore", "content_run_links", "enrich_content_run_result"]
