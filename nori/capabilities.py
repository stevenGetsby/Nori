"""Public capability-architecture entrypoints."""
from __future__ import annotations

from typing import Any

from nori.core import (
    CAPABILITY_MODULES,
    AccountOperationProject,
    CapabilityModule,
    CapabilitySnapshot,
    capability_module_names,
    get_capability_module,
)
from nori.learning_loop.facade import LearningLoopFacade


def capability_registry_snapshot() -> dict[str, Any]:
    """Return a JSON-serializable view of the agent-owned capability registry."""

    return {
        "module_names": capability_module_names(),
        "modules": [module.to_dict() for module in CAPABILITY_MODULES],
    }


def build_capability_snapshot(
    project: AccountOperationProject | dict[str, Any] | None,
    *,
    task_ids: list[str] | None = None,
    selected_candidate_ids: dict[str, str] | None = None,
    signal_source: str = "metrics",
    signal_target: str = "preference",
    confidence: float = 0.5,
) -> CapabilitySnapshot:
    """Project an operation project into the current agent capability view."""

    return LearningLoopFacade().capability_snapshot_from_project(
        project,
        task_ids=task_ids,
        selected_candidate_ids=selected_candidate_ids,
        signal_source=signal_source,
        signal_target=signal_target,
        confidence=confidence,
    )


def validate_capability_snapshot(snapshot: CapabilitySnapshot | dict[str, Any] | None) -> list[dict[str, Any]]:
    """Validate a capability snapshot object or persisted dictionary."""

    normalized = snapshot if isinstance(snapshot, CapabilitySnapshot) else CapabilitySnapshot.from_dict(snapshot)
    return normalized.validate()


__all__ = [
    "CAPABILITY_MODULES",
    "CapabilitySnapshot",
    "CapabilityModule",
    "build_capability_snapshot",
    "capability_module_names",
    "capability_registry_snapshot",
    "get_capability_module",
    "validate_capability_snapshot",
]
