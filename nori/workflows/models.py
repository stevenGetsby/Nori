"""Workflow run contracts."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Callable
from uuid import uuid4

from nori._compat import dataclass, field


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def run_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


@dataclass(slots=True)
class HumanGateSpec:
    name: str
    prompt: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class StageSpec:
    name: str
    handler: Callable[[Any], Any]
    human_gate: HumanGateSpec | None = None


@dataclass(slots=True)
class WorkflowSpec:
    name: str
    stages: list[StageSpec] = field(default_factory=list)


@dataclass(slots=True)
class StageRun:
    stage_name: str
    status: str = "pending"
    input_ref: str = ""
    output_ref: str = ""
    error: str = ""
    started_at: str = ""
    finished_at: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def start(self) -> None:
        self.status = "running"
        self.started_at = utc_now_iso()

    def finish(self, *, output_ref: str = "") -> None:
        self.status = "succeeded"
        self.output_ref = output_ref
        self.finished_at = utc_now_iso()

    def fail(self, error: Exception) -> None:
        self.status = "failed"
        self.error = f"{type(error).__name__}: {error}"
        self.finished_at = utc_now_iso()

    def skip(self) -> None:
        self.status = "skipped"
        self.finished_at = utc_now_iso()

    def wait_for_human(self) -> None:
        self.status = "waiting_for_human"

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage_name": self.stage_name,
            "status": self.status,
            "input_ref": self.input_ref,
            "output_ref": self.output_ref,
            "error": self.error,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "metadata": dict(self.metadata),
        }


@dataclass(slots=True)
class WorkflowRun:
    workflow_name: str
    run_id: str = field(default_factory=lambda: run_id("workflow"))
    session_id: str = ""
    task_id: str = ""
    status: str = "pending"
    stages: list[StageRun] = field(default_factory=list)
    artifact_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    started_at: str = ""
    finished_at: str = ""

    def start(self) -> None:
        self.status = "running"
        self.started_at = utc_now_iso()

    def finish(self) -> None:
        self.status = "succeeded"
        self.finished_at = utc_now_iso()

    def fail(self, error: Exception) -> None:
        self.status = "failed"
        self.metadata["error"] = f"{type(error).__name__}: {error}"
        self.finished_at = utc_now_iso()

    def wait_for_human(self, *, gate_name: str, stage_name: str) -> None:
        self.status = "waiting_for_human"
        self.metadata["human_gate"] = {
            "gate_name": gate_name,
            "stage_name": stage_name,
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "workflow_name": self.workflow_name,
            "run_id": self.run_id,
            "session_id": self.session_id,
            "task_id": self.task_id,
            "status": self.status,
            "stages": [stage.to_dict() for stage in self.stages],
            "artifact_refs": list(self.artifact_refs),
            "metadata": dict(self.metadata),
            "started_at": self.started_at,
            "finished_at": self.finished_at,
        }


class HumanGateRequired(RuntimeError):
    """Raised when a workflow reaches a human gate in pause mode."""

    def __init__(self, gate_name: str, stage_name: str, workflow_run: WorkflowRun) -> None:
        super().__init__(f"human gate required: {gate_name} before {stage_name}")
        self.gate_name = gate_name
        self.stage_name = stage_name
        self.workflow_run = workflow_run
