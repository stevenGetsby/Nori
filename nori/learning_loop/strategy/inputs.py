"""Input normalization helpers for strategy iteration workflows."""
from __future__ import annotations

from nori.core import AccountOperationProject
from typing import Any


from ..models import ComplianceReview, MetricsSnapshot


def normalize_reviews(
    values: list[ComplianceReview | dict[str, Any]] | None,
    project: AccountOperationProject | None = None,
) -> list[ComplianceReview]:
    source = values if values is not None else (project.compliance_reviews if project else [])
    return [
        value if isinstance(value, ComplianceReview) else ComplianceReview.from_dict(value)
        for value in source
    ]


def normalize_metrics_snapshots(
    values: list[MetricsSnapshot | dict[str, Any]] | None,
    project: AccountOperationProject | None = None,
) -> list[MetricsSnapshot]:
    source = values if values is not None else (project.metrics_snapshots if project else [])
    return [
        value if isinstance(value, MetricsSnapshot) else MetricsSnapshot.from_dict(value)
        for value in source
    ]


__all__ = ["normalize_metrics_snapshots", "normalize_reviews"]
