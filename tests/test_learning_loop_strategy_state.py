"""Tests for strategy iteration state helpers."""

from __future__ import annotations

from nori.core import AccountOperationProject
from nori.agents.learning_loop.strategy import state as strategy_iteration_state
from nori.agents.learning_loop.models import MetricsSnapshot, StrategyIteration


def test_attach_metrics_snapshot_appends_to_project_when_present():
    project = AccountOperationProject(project_id="ops_001")
    snapshot = MetricsSnapshot(snapshot_id="metric_001", ref_id="pkg_001")

    strategy_iteration_state.attach_metrics_snapshot(project, snapshot)

    assert project.metrics_snapshots == [snapshot]


def test_attach_metrics_snapshot_ignores_missing_project():
    snapshot = MetricsSnapshot(snapshot_id="metric_001", ref_id="pkg_001")

    assert strategy_iteration_state.attach_metrics_snapshot(None, snapshot) is None


def test_attach_strategy_iteration_appends_to_project_when_present():
    project = AccountOperationProject(project_id="ops_001")
    iteration = StrategyIteration(iteration_id="iter_001", project_id="ops_001")

    strategy_iteration_state.attach_strategy_iteration(project, iteration)

    assert project.strategy_iterations == [iteration]


def test_attach_strategy_iteration_preserves_existing_iterations_and_appends():
    first = StrategyIteration(iteration_id="iter_001", project_id="ops_001")
    second = StrategyIteration(iteration_id="iter_002", project_id="ops_001")
    project = AccountOperationProject(project_id="ops_001", strategy_iterations=[first])

    strategy_iteration_state.attach_strategy_iteration(project, second)

    assert project.strategy_iterations == [first, second]
