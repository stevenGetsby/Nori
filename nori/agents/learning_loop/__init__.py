"""Learning-loop module."""
from __future__ import annotations

from nori.core import LearningSignal, PerformanceSnapshot
from nori.core.lazy_exports import lazy_export

from .schemas import ComplianceReview, MetricsSnapshot, StrategyIteration

_LAZY_EXPORTS = {
    "LearningLoopFacade": "facade",
    "build_capability_snapshot": "facade",
    "ComplianceReviewerAgent": "review",
    "ConsistencyReviewerAgent": "review",
    "QualityReviewerAgent": "review",
    "ReviewGateAgent": "review",
    "review_content_package": "review",
    "validate_capability_snapshot": "facade",
    "MetricsSnapshotAgent": "strategy",
    "StrategyIterationAgent": "strategy",
    "create_strategy_iteration": "strategy",
    "record_metrics_snapshot": "strategy",
}

__all__ = [
    "ComplianceReview",
    "ConsistencyReviewerAgent",
    "LearningLoopFacade",
    "LearningSignal",
    "MetricsSnapshot",
    "MetricsSnapshotAgent",
    "PerformanceSnapshot",
    "QualityReviewerAgent",
    "ReviewGateAgent",
    "StrategyIteration",
    "StrategyIterationAgent",
    "build_capability_snapshot",
    "create_strategy_iteration",
    "record_metrics_snapshot",
    "review_content_package",
    "validate_capability_snapshot",
]


def __getattr__(name: str):
    return lazy_export(__name__, _LAZY_EXPORTS, name)
