"""Runtime run recorder for session/context/workflow bookkeeping."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from nori.context import ContextBundle, ContextResolver
from nori.sessions import Session, SessionManager, TaskGoal

from .models import StageRun, WorkflowRun


@dataclass(frozen=True)
class RuntimeRun:
    """The runtime state that wraps one concrete workflow execution."""

    session: Session
    task_goal: TaskGoal
    context: ContextBundle
    workflow_run: WorkflowRun


class RuntimeRunRecorder:
    """Own session, context, and workflow-run recording for scripts/apps."""

    def __init__(
        self,
        *,
        user_id: str,
        profile_id: str = "",
        workflow_name: str,
        goal: str,
        context_resolver: ContextResolver | None = None,
        session_manager: SessionManager | None = None,
    ) -> None:
        self.user_id = user_id
        self.profile_id = profile_id
        self.workflow_name = workflow_name
        self.goal = goal
        self.context_resolver = context_resolver or ContextResolver()
        self.session_manager = session_manager or SessionManager()

    def start(
        self,
        *,
        user_input: dict[str, Any] | None = None,
        run_dir: str | Path,
        source: str = "",
        acceptance: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> RuntimeRun:
        run_path = Path(run_dir)
        session = self.session_manager.create_session(
            user_id=self.user_id,
            profile_id=self.profile_id,
            metadata={"run_dir": str(run_path), **dict(metadata or {})},
        )
        self.session_manager.append_turn(
            session.session_id,
            role="user",
            content=str((user_input or {}).get("brief_text") or (user_input or {}).get("text") or ""),
            metadata={"source": source},
        )
        task_goal = self.session_manager.start_task(
            session.session_id,
            goal=self.goal,
            workflow_name=self.workflow_name,
            acceptance=list(acceptance or []),
        )
        context = self.context_resolver.build(
            session=session,
            task_goal=task_goal,
            user_input=dict(user_input or {}),
            artifacts=[{"kind": "run_dir", "path": str(run_path)}],
        )
        workflow_run = WorkflowRun(
            workflow_name=self.workflow_name,
            session_id=session.session_id,
            task_id=task_goal.task_id,
        )
        workflow_run.start()
        return RuntimeRun(session=session, task_goal=task_goal, context=context, workflow_run=workflow_run)

    @staticmethod
    def record_stage(runtime: RuntimeRun, stage_name: str, artifact_path: str | Path) -> StageRun:
        stage = StageRun(stage_name=stage_name)
        stage.start()
        stage.finish(output_ref=str(artifact_path))
        runtime.workflow_run.stages.append(stage)
        runtime.workflow_run.artifact_refs.append(str(artifact_path))
        return stage

    @staticmethod
    def finish(runtime: RuntimeRun) -> None:
        runtime.workflow_run.finish()

    @staticmethod
    def write_snapshot(runtime: RuntimeRun, run_dir: str | Path) -> None:
        run_path = Path(run_dir)
        run_path.mkdir(parents=True, exist_ok=True)
        _write_json(run_path / "session.json", runtime.session.to_dict())
        _write_json(run_path / "context_bundle.json", runtime.context.to_dict())
        _write_json(run_path / "workflow_run.json", runtime.workflow_run.to_dict())


def _write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
