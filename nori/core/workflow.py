"""Base workflow runner for multi-agent orchestration."""
from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Any


WorkflowStep = tuple[str, Callable[[Any], Any]]


def passthrough_step(value: Any) -> Any:
    """Return the current workflow value unchanged."""
    return value


def named_workflow_steps(*names: str) -> list[WorkflowStep]:
    """Build named no-op steps for workflows whose public methods own execution."""
    return [(name, passthrough_step) for name in names]


class WorkflowBase:
    """Ordered step runner for workflows that compose multiple agents."""

    def __init__(self, *, workflow_name: str = "", steps: Iterable[WorkflowStep] | None = None) -> None:
        self.workflow_name = workflow_name
        self.steps = list(steps or [])

    @property
    def step_names(self) -> list[str]:
        return [name for name, _step in self.steps]

    def run_steps(self, initial: Any) -> Any:
        value = initial
        for _name, step in self.steps:
            value = step(value)
        return value


__all__ = ["WorkflowBase", "WorkflowStep", "named_workflow_steps", "passthrough_step"]
