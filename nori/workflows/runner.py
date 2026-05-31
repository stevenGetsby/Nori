"""Workflow runner with run/stage bookkeeping."""
from __future__ import annotations

from typing import Any

from .langgraph_runner import LangGraphWorkflowRunner
from .models import WorkflowRun, WorkflowSpec


class WorkflowRunner:
    """Run a workflow spec through the configured graph execution engine."""

    def __init__(self, engine: LangGraphWorkflowRunner | None = None) -> None:
        self.engine = engine or LangGraphWorkflowRunner()

    def run(
        self,
        spec: WorkflowSpec,
        initial: Any,
        *,
        session_id: str = "",
        task_id: str = "",
    ) -> tuple[Any, WorkflowRun]:
        return self.engine.run(spec, initial, session_id=session_id, task_id=task_id)
