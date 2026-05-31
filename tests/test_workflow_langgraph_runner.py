from __future__ import annotations

from pathlib import Path

import pytest

from nori.workflows import StageSpec, WorkflowSpec, WorkflowRunner


ROOT = Path(__file__).resolve().parents[1]


def test_root_project_declares_langchain_and_langgraph_dependencies():
    source = (ROOT / "pyproject.toml").read_text()

    assert '"langchain-core>=0.3.79,<0.4"' in source
    assert '"langgraph>=0.6.10,<0.7"' in source


def test_workflow_runner_executes_stage_spec_through_langgraph():
    spec = WorkflowSpec(
        name="demo_graph",
        stages=[
            StageSpec("collect", lambda value: {**value, "count": value["count"] + 1}),
            StageSpec("publish", lambda value: {**value, "published": True}),
        ],
    )

    output, run = WorkflowRunner().run(
        spec,
        {"count": 1},
        session_id="session_001",
        task_id="task_001",
    )

    assert output == {"count": 2, "published": True}
    assert run.status == "succeeded"
    assert run.session_id == "session_001"
    assert run.task_id == "task_001"
    assert [stage.stage_name for stage in run.stages] == ["collect", "publish"]
    assert [stage.status for stage in run.stages] == ["succeeded", "succeeded"]
    assert run.metadata["engine"] == "langgraph"
    assert run.metadata["langchain_runnable"] == "RunnableLambda"


def test_workflow_runner_records_failing_langgraph_stage():
    def explode(value):
        raise RuntimeError(f"bad value: {value}")

    spec = WorkflowSpec(
        name="failing_graph",
        stages=[
            StageSpec("first", lambda value: value + 1),
            StageSpec("explode", explode),
            StageSpec("never", lambda value: value + 1),
        ],
    )

    with pytest.raises(RuntimeError, match="bad value: 2") as exc_info:
        WorkflowRunner().run(spec, 1)

    workflow_run = getattr(exc_info.value, "workflow_run")

    assert workflow_run.status == "failed"
    assert [stage.stage_name for stage in workflow_run.stages] == ["first", "explode"]
    assert [stage.status for stage in workflow_run.stages] == ["succeeded", "failed"]
    assert "RuntimeError: bad value: 2" in workflow_run.stages[-1].error


def test_workflow_runner_records_stage_artifact_refs_from_state():
    spec = WorkflowSpec(
        name="artifact_graph",
        stages=[
            StageSpec("write_a", lambda value: {**value, "_artifact_ref": "runs/a.json"}),
            StageSpec(
                "write_b",
                lambda value: {**value, "_artifact_refs": {"write_b": "runs/b.json"}},
            ),
        ],
    )

    _, run = WorkflowRunner().run(spec, {})

    assert [stage.output_ref for stage in run.stages] == ["runs/a.json", "runs/b.json"]
    assert run.artifact_refs == ["runs/a.json", "runs/b.json"]
