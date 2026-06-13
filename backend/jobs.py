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
            "actions": _job_actions(
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


def enrich_content_run_result(
    result: dict[str, Any] | None,
    *,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Attach backend-owned follow-up links and actions to a run result."""

    if not isinstance(result, dict):
        return None
    enriched = dict(result)
    links = dict(enriched.get("links") or {})
    links.update(content_run_links(metadata=dict(metadata or {}), result=enriched))
    if links:
        enriched["links"] = links
    actions = _content_run_actions(result=enriched, links=links)
    if actions:
        enriched["actions"] = actions
    return enriched


def content_run_links(*, metadata: dict[str, Any], result: dict[str, Any] | None) -> dict[str, str]:
    data = result if isinstance(result, dict) else {}
    manifest = data.get("experiment_manifest") if isinstance(data.get("experiment_manifest"), dict) else {}
    experiment = manifest.get("experiment") if isinstance(manifest.get("experiment"), dict) else {}
    input_manifest = data.get("input_manifest") if isinstance(data.get("input_manifest"), dict) else {}
    case_id = str(data.get("case_id") or experiment.get("case_id") or input_manifest.get("case_id") or metadata.get("case_id") or "").strip()
    run_id = str(data.get("run_id") or experiment.get("run_id") or "").strip()
    if not case_id or not run_id:
        return {}
    base = f"/workflows/content-production/runs/{case_id}/{run_id}"
    return {
        "run": base,
        "acceptance": f"{base}/acceptance",
        "evaluations": f"{base}/evaluations",
        "evaluation_draft": f"{base}/evaluations/draft",
        "replay": f"{base}/replay",
        "export": f"{base}/export",
        "inspect_artifacts": f"{base}/artifacts/inspect",
        "case_compare": f"/experiments/content-production/cases/{case_id}/compare",
        "case_next_actions": f"/experiments/content-production/cases/{case_id}/next-actions",
        "case_selected_run": f"/experiments/content-production/cases/{case_id}/selected-run",
        "case_evaluation_draft": f"/experiments/content-production/cases/{case_id}/evaluations/draft",
        "case_evaluations": f"/experiments/content-production/cases/{case_id}/evaluations",
        "case_replay": f"/experiments/content-production/cases/{case_id}/replay",
        "case_promotion": f"/experiments/content-production/cases/{case_id}/promotion",
        "case_delivery": f"/experiments/content-production/cases/{case_id}/delivery",
        "case_timeline": f"/experiments/content-production/cases/{case_id}/timeline",
        "case_export": f"/experiments/content-production/cases/{case_id}/export",
    }


def _content_run_actions(*, result: dict[str, Any], links: dict[str, str]) -> list[dict[str, Any]]:
    run_id = str(result.get("run_id") or "").strip()
    if not run_id:
        return []
    status = str(result.get("status") or "").strip()
    action_ids = (
        [
            "inspect_failure_artifacts",
            "replay_run",
            "case_next_actions",
            "export_run",
        ]
        if status == "failed"
        else [
            "inspect_run",
            "draft_evaluation",
            "case_next_actions",
            "export_run",
            "replay_run",
            "promote_run",
        ]
    )
    actions_by_id = {
        "inspect_run": {
            "action_id": "inspect_run",
            "severity": "next_step",
            "method": "GET",
            "href": links.get("inspect_artifacts", ""),
            "message": "Inspect generated artifacts, cover previews, proof, acceptance, and evaluation state.",
        },
        "inspect_failure_artifacts": {
            "action_id": "inspect_failure_artifacts",
            "severity": "next_step",
            "method": "GET",
            "href": links.get("inspect_artifacts", ""),
            "message": "Inspect failure artifacts and manifests before deciding whether to replay.",
        },
        "draft_evaluation": {
            "action_id": "draft_evaluation",
            "severity": "next_step",
            "method": "POST",
            "href": links.get("case_evaluation_draft", ""),
            "payload": {"run_id": run_id, "reviewer": "operator", "persist": False},
            "message": "Build a review draft for this run without hard-coding the run-level URL.",
        },
        "case_next_actions": {
            "action_id": "case_next_actions",
            "severity": "next_step",
            "method": "GET",
            "href": links.get("case_next_actions", ""),
            "message": "Ask the backend for the current case-level decision plan.",
        },
        "export_run": {
            "action_id": "export_run",
            "severity": "optional",
            "method": "GET",
            "href": links.get("export", ""),
            "message": "Download a review/archive bundle for this run.",
        },
        "replay_run": {
            "action_id": "replay_run",
            "severity": "optional",
            "method": "POST",
            "href": links.get("case_replay", ""),
            "payload": {"run_id": run_id, "human_gate_mode": "skip"},
            "message": "Replay this run from its stored request snapshot.",
        },
        "promote_run": {
            "action_id": "promote_run",
            "severity": "optional",
            "method": "POST",
            "href": links.get("case_promotion", ""),
            "payload": {
                "run_id": run_id,
                "reviewer": "operator",
                "reason": "Promote the accepted experiment run.",
                "allow_unaccepted": False,
            },
            "message": "Promote this run after acceptance/evaluation confirms it is ready.",
        },
    }
    return [actions_by_id[action_id] for action_id in action_ids if actions_by_id[action_id].get("href")]


def _job_actions(
    *,
    status: str,
    links: dict[str, str],
    result: dict[str, Any] | None,
    cancel_requested: bool = False,
) -> list[dict[str, Any]]:
    actions: list[dict[str, Any]] = []
    if status in {"queued", "running", "cancelling"} and links.get("self"):
        actions.append(
            {
                "action_id": "poll_job",
                "severity": "next_step",
                "method": "GET",
                "href": links["self"],
                "message": "Poll this background experiment job until it reaches a terminal status.",
            }
        )
    if status in {"queued", "running"} and not cancel_requested and links.get("cancel"):
        actions.append(
            {
                "action_id": "cancel_job",
                "severity": "optional",
                "method": "POST",
                "href": links["cancel"],
                "payload": {"reason": "operator requested cancellation"},
                "message": "Request cancellation for this background experiment job.",
            }
        )
    if isinstance(result, dict):
        actions.extend(list(result.get("actions") or []))
    return actions


__all__ = ["ExperimentJob", "InProcessExperimentJobStore", "content_run_links", "enrich_content_run_result"]
