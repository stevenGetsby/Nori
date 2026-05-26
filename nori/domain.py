"""Public domain-architecture entrypoints.

This module gives CLI/API/UI callers one stable import path for the shared +
five-module architecture while keeping implementation ownership in the domain
facades.
"""
from __future__ import annotations

from typing import Any

from nori.core import AccountOperationProject, DomainSnapshot
from nori.learning_loop.facade import LearningLoopFacade


def build_domain_snapshot(
    project: AccountOperationProject | dict[str, Any] | None,
    *,
    task_ids: list[str] | None = None,
    selected_candidate_ids: dict[str, str] | None = None,
    signal_source: str = "metrics",
    signal_target: str = "preference",
    confidence: float = 0.5,
) -> DomainSnapshot:
    """Project an account-operation project into the full domain snapshot."""

    return LearningLoopFacade().domain_snapshot_from_project(
        project,
        task_ids=task_ids,
        selected_candidate_ids=selected_candidate_ids,
        signal_source=signal_source,
        signal_target=signal_target,
        confidence=confidence,
    )


def validate_domain_snapshot(snapshot: DomainSnapshot | dict[str, Any] | None) -> list[dict[str, Any]]:
    """Validate a snapshot object or persisted snapshot dictionary."""

    normalized = snapshot if isinstance(snapshot, DomainSnapshot) else DomainSnapshot.from_dict(snapshot)
    return normalized.validate()


__all__ = [
    "build_domain_snapshot",
    "validate_domain_snapshot",
]
