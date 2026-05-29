"""Tests for strategy iteration input normalization helpers."""

from __future__ import annotations

from nori.core import AccountOperationProject
from nori.learning_loop.strategy.package import StrategyIterationInputPreparer
from nori.learning_loop.models import ComplianceReview, MetricsSnapshot


strategy_iteration_inputs = StrategyIterationInputPreparer()


def test_normalize_reviews_restores_dicts_and_preserves_instances():
    review = ComplianceReview(review_id="rev_001", package_id="pkg_001")

    assert strategy_iteration_inputs.normalize_reviews([review]) == [review]
    assert strategy_iteration_inputs.normalize_reviews([review.to_dict()])[0].review_id == "rev_001"


def test_normalize_reviews_defaults_to_project_reviews():
    review = ComplianceReview(review_id="rev_001", package_id="pkg_001")
    project = AccountOperationProject(project_id="ops_001", compliance_reviews=[review])

    assert strategy_iteration_inputs.normalize_reviews(None, project) == [review]
    assert strategy_iteration_inputs.normalize_reviews(None, None) == []


def test_normalize_metrics_snapshots_restores_dicts_and_preserves_instances():
    snapshot = MetricsSnapshot(snapshot_id="metric_001", ref_id="pkg_001")

    assert strategy_iteration_inputs.normalize_metrics_snapshots([snapshot]) == [snapshot]
    restored = strategy_iteration_inputs.normalize_metrics_snapshots([snapshot.to_dict()])
    assert restored[0].snapshot_id == "metric_001"


def test_normalize_metrics_snapshots_defaults_to_project_snapshots():
    snapshot = MetricsSnapshot(snapshot_id="metric_001", ref_id="pkg_001")
    project = AccountOperationProject(project_id="ops_001", metrics_snapshots=[snapshot])

    assert strategy_iteration_inputs.normalize_metrics_snapshots(None, project) == [snapshot]
    assert strategy_iteration_inputs.normalize_metrics_snapshots(None, None) == []
