"""Sequential workflow runner with run/stage bookkeeping."""
from __future__ import annotations

from typing import Any

from .models import StageRun, WorkflowRun, WorkflowSpec


class WorkflowRunner:
    """Run a workflow spec while recording stage status."""

    def run(
        self,
        spec: WorkflowSpec,
        initial: Any,
        *,
        session_id: str = "",
        task_id: str = "",
    ) -> tuple[Any, WorkflowRun]:
        workflow_run = WorkflowRun(workflow_name=spec.name, session_id=session_id, task_id=task_id)
        workflow_run.start()
        value = initial
        try:
            for stage in spec.stages:
                stage_run = StageRun(stage_name=stage.name)
                workflow_run.stages.append(stage_run)
                stage_run.start()
                value = stage.handler(value)
                stage_run.finish()
            workflow_run.finish()
            return value, workflow_run
        except Exception as exc:
            if workflow_run.stages:
                workflow_run.stages[-1].fail(exc)
            workflow_run.fail(exc)
            raise
