"""State mutation helpers for metrics and strategy iteration workflows."""
from __future__ import annotations


from nori.core import AccountOperationProject
from ..models import MetricsSnapshot, StrategyIteration


def attach_metrics_snapshot(
    project: AccountOperationProject | None,
    snapshot: MetricsSnapshot,
) -> None:
    if project is not None:
        project.metrics_snapshots.append(snapshot)


def attach_strategy_iteration(
    project: AccountOperationProject | None,
    iteration: StrategyIteration,
) -> None:
    if project is not None:
        project.strategy_iterations.append(iteration)


__all__ = ["attach_metrics_snapshot", "attach_strategy_iteration"]
