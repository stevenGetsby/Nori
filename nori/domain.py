"""Legacy domain-architecture entrypoints.

New code should use :mod:`nori.capabilities`. This module stays as a
compatibility layer for callers that still expect ``DomainSnapshot``.
"""
from __future__ import annotations

from typing import Any

from nori.capabilities import build_capability_snapshot as _build_capability_snapshot
from nori.core import AccountOperationProject, CapabilitySnapshot
from nori.core.architecture import domain_module_names
from nori.core.models import DomainSnapshot


def build_domain_snapshot(
    project: AccountOperationProject | dict[str, Any] | None,
    *,
    task_ids: list[str] | None = None,
    selected_candidate_ids: dict[str, str] | None = None,
    signal_source: str = "metrics",
    signal_target: str = "preference",
    confidence: float = 0.5,
) -> DomainSnapshot:
    """Project an account-operation project into a legacy domain snapshot."""

    capability_snapshot = _build_capability_snapshot(
        project,
        task_ids=task_ids,
        selected_candidate_ids=selected_candidate_ids,
        signal_source=signal_source,
        signal_target=signal_target,
        confidence=confidence,
    )
    return _domain_snapshot_from_capability_snapshot(capability_snapshot)


def validate_domain_snapshot(snapshot: DomainSnapshot | dict[str, Any] | None) -> list[dict[str, Any]]:
    """Validate a snapshot object or persisted snapshot dictionary."""

    normalized = snapshot if isinstance(snapshot, DomainSnapshot) else DomainSnapshot.from_dict(snapshot)
    return normalized.validate()


def _domain_snapshot_from_capability_snapshot(snapshot: CapabilitySnapshot) -> DomainSnapshot:
    return DomainSnapshot(
        snapshot_id=_legacy_domain_snapshot_id(snapshot.snapshot_id),
        project_id=snapshot.project_id,
        module_names=domain_module_names(),
        user_profile=snapshot.user_profile,
        market_analysis=snapshot.market_analysis,
        context_packs=list(snapshot.context_packs),
        candidate_sets=list(snapshot.candidate_sets),
        performance_snapshots=list(snapshot.performance_snapshots),
        learning_signals=list(snapshot.learning_signals),
        source_refs=list(snapshot.source_refs),
        metadata={
            **dict(snapshot.metadata),
            "source_snapshot_id": snapshot.snapshot_id,
            "architecture": "domain_compat",
        },
    )


def _legacy_domain_snapshot_id(snapshot_id: str) -> str:
    if snapshot_id.startswith("capability_"):
        return f"domain_{snapshot_id.removeprefix('capability_')}"
    return f"domain_{snapshot_id or 'project'}"


__all__ = [
    "build_domain_snapshot",
    "validate_domain_snapshot",
]
