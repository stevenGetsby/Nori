"""Class-owned input contract for strategy iteration agents."""
from __future__ import annotations

from typing import Any

from nori.core import AccountOperationProject, AgentInputPreparer

from ..schemas import ComplianceReview, MetricsSnapshot


class StrategyIterationInputPreparer(AgentInputPreparer):
    """Restore review and metric evidence for strategy iteration."""

    def normalize_reviews(
        self,
        values: list[ComplianceReview | dict[str, Any]] | None,
        project: AccountOperationProject | None = None,
    ) -> list[ComplianceReview]:
        source = values if values is not None else (project.compliance_reviews if project else [])
        return [
            value if isinstance(value, ComplianceReview) else ComplianceReview.from_dict(value)
            for value in source
        ]

    def normalize_metrics_snapshots(
        self,
        values: list[MetricsSnapshot | dict[str, Any]] | None,
        project: AccountOperationProject | None = None,
    ) -> list[MetricsSnapshot]:
        source = values if values is not None else (project.metrics_snapshots if project else [])
        return [
            value if isinstance(value, MetricsSnapshot) else MetricsSnapshot.from_dict(value)
            for value in source
        ]


__all__ = ["StrategyIterationInputPreparer"]
