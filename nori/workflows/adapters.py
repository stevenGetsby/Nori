"""Adapters from core workflow abstractions to runtime workflow specs."""
from __future__ import annotations

from collections.abc import Mapping

from nori.core.workflow import WorkflowBase

from .models import HumanGateSpec, StageSpec, WorkflowSpec


def workflow_spec_from_base(
    workflow: WorkflowBase,
    *,
    human_gates: Mapping[str, HumanGateSpec] | None = None,
) -> WorkflowSpec:
    """Convert a core WorkflowBase into a runtime WorkflowSpec.

    Core workflows describe stable capability/facade step shape. Runtime
    workflow specs are what the LangGraph-backed runner executes and records.
    Keeping this adapter in ``nori.workflows`` preserves the dependency
    direction: runtime can depend on core, but core stays backend-free.
    """
    gates = dict(human_gates or {})
    return WorkflowSpec(
        name=workflow.workflow_name,
        stages=[
            StageSpec(name, handler, human_gate=gates.get(name))
            for name, handler in workflow.steps
        ],
    )


__all__ = ["workflow_spec_from_base"]
