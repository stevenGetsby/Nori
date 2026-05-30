"""Learning loop domain models."""
from __future__ import annotations

from typing import Any

from nori._compat import dataclass, field
from nori.core.contracts import dict_list as _dict_list, int_value as _int, mapping as _mapping, string_list as _string_list


@dataclass(slots=True)
class ComplianceReview:
    """Review report for generated content before publish handoff."""

    review_id: str = ""
    package_id: str = ""
    task_id: str = ""
    status: str = "pending"
    score: int = 0
    issues: list[dict[str, Any]] = field(default_factory=list)
    fix_suggestions: list[str] = field(default_factory=list)
    reviewer: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "review_id": self.review_id,
            "package_id": self.package_id,
            "task_id": self.task_id,
            "status": self.status,
            "score": self.score,
            "issues": _dict_list(self.issues),
            "fix_suggestions": list(self.fix_suggestions),
            "reviewer": self.reviewer,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "ComplianceReview":
        data = _mapping(data)
        return cls(
            review_id=str(data.get("review_id") or ""),
            package_id=str(data.get("package_id") or ""),
            task_id=str(data.get("task_id") or ""),
            status=str(data.get("status") or "pending"),
            score=_int(data.get("score"), default=0),
            issues=_dict_list(data.get("issues")),
            fix_suggestions=_string_list(data.get("fix_suggestions")),
            reviewer=str(data.get("reviewer") or ""),
            metadata=_mapping(data.get("metadata")),
        )


@dataclass(slots=True)
class MetricsSnapshot:
    """Observed metrics for a task, package, or operation cycle."""

    snapshot_id: str = ""
    ref_id: str = ""
    captured_at: str = ""
    metrics: dict[str, Any] = field(default_factory=dict)
    source: str = ""
    notes: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "ref_id": self.ref_id,
            "captured_at": self.captured_at,
            "metrics": dict(self.metrics),
            "source": self.source,
            "notes": list(self.notes),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "MetricsSnapshot":
        data = _mapping(data)
        return cls(
            snapshot_id=str(data.get("snapshot_id") or ""),
            ref_id=str(data.get("ref_id") or ""),
            captured_at=str(data.get("captured_at") or ""),
            metrics=_mapping(data.get("metrics")),
            source=str(data.get("source") or ""),
            notes=_string_list(data.get("notes")),
            metadata=_mapping(data.get("metadata")),
        )


@dataclass(slots=True)
class StrategyIteration:
    """Learning record that turns review and metrics into next-cycle changes."""

    iteration_id: str = ""
    project_id: str = ""
    input_refs: list[str] = field(default_factory=list)
    diagnosis: list[str] = field(default_factory=list)
    decisions: list[str] = field(default_factory=list)
    next_actions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "iteration_id": self.iteration_id,
            "project_id": self.project_id,
            "input_refs": list(self.input_refs),
            "diagnosis": list(self.diagnosis),
            "decisions": list(self.decisions),
            "next_actions": list(self.next_actions),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "StrategyIteration":
        data = _mapping(data)
        return cls(
            iteration_id=str(data.get("iteration_id") or ""),
            project_id=str(data.get("project_id") or ""),
            input_refs=_string_list(data.get("input_refs")),
            diagnosis=_string_list(data.get("diagnosis")),
            decisions=_string_list(data.get("decisions")),
            next_actions=_string_list(data.get("next_actions")),
            metadata=_mapping(data.get("metadata")),
        )


ComplianceReview.__module__ = __name__
MetricsSnapshot.__module__ = __name__
StrategyIteration.__module__ = __name__

__all__ = ["ComplianceReview", "MetricsSnapshot", "StrategyIteration"]
