"""Manual metrics and rule-based strategy iteration agents."""
from __future__ import annotations

from nori.core import AccountOperationProject
from datetime import date
from typing import Any

from nori.core import AgentBase
from nori.agents.content_generation.schemas import ContentPackage
from nori.core import ContentTask

from .package import StrategyIterationInputPreparer
from . import policy as _policy
from . import state as _state
from ..schemas import ComplianceReview, MetricsSnapshot, StrategyIteration


_INPUT_PREPARER = StrategyIterationInputPreparer()


class MetricsSnapshotAgent(AgentBase):
    """Normalize manual metrics into a project-attachable snapshot."""

    stage_name = "metrics_snapshot"

    def __init__(self) -> None:
        super().__init__(stage_name=self.stage_name, use_llm=False)

    def run(
        self,
        ref: ContentPackage | ContentTask | str | dict[str, Any],
        metrics: dict[str, Any],
        *,
        captured_at: str | date | None = None,
        source: str = "manual",
        notes: list[str] | None = None,
        project: AccountOperationProject | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> MetricsSnapshot:
        ref_id, ref_type = _policy.ref_identity(ref)
        captured = _policy.date_text(captured_at)
        snapshot = MetricsSnapshot(
            snapshot_id=f"metric_{_policy.slug(ref_id)}_{captured.replace('-', '')}",
            ref_id=ref_id,
            captured_at=captured,
            metrics=dict(metrics or {}),
            source=source,
            notes=list(notes or []),
            metadata={
                "ref_type": ref_type,
                "summary": _policy.metric_summary(metrics or {}),
                **dict(metadata or {}),
            },
        )
        _state.attach_metrics_snapshot(project, snapshot)
        return snapshot


class StrategyIterationAgent(AgentBase):
    """Turn reviews and metrics into next-cycle strategy actions."""

    stage_name = "strategy_iteration"

    def __init__(self) -> None:
        super().__init__(stage_name=self.stage_name, use_llm=False)

    def run(
        self,
        *,
        project: AccountOperationProject | None = None,
        reviews: list[ComplianceReview | dict[str, Any]] | None = None,
        metrics_snapshots: list[MetricsSnapshot | dict[str, Any]] | None = None,
        project_id: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> StrategyIteration:
        normalized_reviews = _INPUT_PREPARER.normalize_reviews(reviews, project)
        normalized_metrics = _INPUT_PREPARER.normalize_metrics_snapshots(metrics_snapshots, project)
        pid = project_id or (project.project_id if project else "")
        review_summary = _policy.review_summary(normalized_reviews)
        metric_summary = _policy.metrics_summary(normalized_metrics)
        diagnosis = _policy.diagnosis(review_summary, metric_summary)
        decisions = _policy.decisions(review_summary, metric_summary)
        next_actions = _policy.next_actions(review_summary, metric_summary)
        iteration = StrategyIteration(
            iteration_id=f"iter_{_policy.slug(pid or 'project')}_{len(normalized_reviews)}r_{len(normalized_metrics)}m",
            project_id=pid,
            input_refs=[
                *[review.review_id for review in normalized_reviews if review.review_id],
                *[snapshot.snapshot_id for snapshot in normalized_metrics if snapshot.snapshot_id],
            ],
            diagnosis=diagnosis,
            decisions=decisions,
            next_actions=next_actions,
            metadata={
                "source": "rule_based_strategy_iteration",
                "review_summary": review_summary,
                "metrics_summary": metric_summary,
                **dict(metadata or {}),
            },
        )
        _state.attach_strategy_iteration(project, iteration)
        return iteration


def record_metrics_snapshot(
    ref: ContentPackage | ContentTask | str | dict[str, Any],
    metrics: dict[str, Any],
    **kwargs: Any,
) -> MetricsSnapshot:
    """Convenience wrapper for one-shot manual metric recording."""

    return MetricsSnapshotAgent().run(ref, metrics, **kwargs)


def create_strategy_iteration(**kwargs: Any) -> StrategyIteration:
    """Convenience wrapper for one-shot strategy iteration."""

    return StrategyIterationAgent().run(**kwargs)


__all__ = [
    "MetricsSnapshotAgent",
    "StrategyIterationAgent",
    "create_strategy_iteration",
    "record_metrics_snapshot",
]
