from __future__ import annotations

from pathlib import Path

import pytest

from nori.core import ArtifactStore, WorkflowBase
from nori.workflows import HumanGateRequired, HumanGateSpec, StageSpec, WorkflowSpec, WorkflowRunner
from nori.workflows import workflow_spec_from_base


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


def test_workflow_runner_records_stored_artifact_refs(tmp_path):
    store = ArtifactStore(tmp_path)

    spec = WorkflowSpec(
        name="stored_artifact_graph",
        stages=[
            StageSpec("save", lambda value: store.save_stage("save", value)),
            StageSpec(
                "save_nested",
                lambda value: {"_artifact_refs": {"save_nested": store.save_stage("save_nested", {"ok": True})}},
            ),
        ],
    )

    _, run = WorkflowRunner().run(spec, {"brand": "Holly"})

    assert [stage.output_ref for stage in run.stages] == [
        str(tmp_path / "save.json"),
        str(tmp_path / "save_nested.json"),
    ]
    assert run.artifact_refs == [str(tmp_path / "save.json"), str(tmp_path / "save_nested.json")]


def test_workflow_runner_skips_human_gate_by_default_and_continues():
    spec = WorkflowSpec(
        name="human_gate_graph",
        stages=[
            StageSpec(
                "publish",
                lambda value: {**value, "published": True},
                human_gate=HumanGateSpec(
                    name="approve_draft",
                    prompt="Approve generated draft before publish.",
                    metadata={"surface": "editor"},
                ),
            ),
        ],
    )

    output, run = WorkflowRunner().run(spec, {"draft": "hello"})

    assert output == {"draft": "hello", "published": True}
    assert run.status == "succeeded"
    assert run.metadata["human_gate_mode"] == "skip"
    assert [stage.stage_name for stage in run.stages] == ["human_gate:approve_draft", "publish"]
    assert [stage.status for stage in run.stages] == ["skipped", "succeeded"]
    assert run.stages[0].metadata == {
        "type": "human_gate",
        "mode": "skip",
        "target_stage": "publish",
        "prompt": "Approve generated draft before publish.",
        "surface": "editor",
    }


def test_workflow_runner_can_pause_at_human_gate_without_marking_failure():
    spec = WorkflowSpec(
        name="human_gate_pause_graph",
        stages=[
            StageSpec(
                "publish",
                lambda value: {**value, "published": True},
                human_gate=HumanGateSpec(name="approve_draft"),
            ),
        ],
    )

    with pytest.raises(HumanGateRequired, match="approve_draft") as exc_info:
        WorkflowRunner().run(spec, {"draft": "hello"}, human_gate_mode="pause")

    workflow_run = exc_info.value.workflow_run

    assert workflow_run.status == "waiting_for_human"
    assert workflow_run.metadata["human_gate_mode"] == "pause"
    assert [stage.stage_name for stage in workflow_run.stages] == ["human_gate:approve_draft"]
    assert workflow_run.stages[0].status == "waiting_for_human"
    assert workflow_run.stages[0].metadata["target_stage"] == "publish"


def test_workflow_base_can_be_adapted_to_langgraph_workflow_spec():
    workflow = WorkflowBase(
        workflow_name="base_demo",
        steps=[
            ("double", lambda value: value * 2),
            ("increment", lambda value: value + 1),
        ],
    )

    spec = workflow_spec_from_base(workflow)
    output, run = WorkflowRunner().run(spec, 3)

    assert isinstance(spec, WorkflowSpec)
    assert spec.name == "base_demo"
    assert [stage.name for stage in spec.stages] == ["double", "increment"]
    assert output == 7
    assert run.workflow_name == "base_demo"
    assert [stage.stage_name for stage in run.stages] == ["double", "increment"]


def test_workflow_base_adapter_can_attach_runtime_human_gates():
    workflow = WorkflowBase(
        workflow_name="approval_demo",
        steps=[("publish", lambda value: {**value, "published": True})],
    )

    spec = workflow_spec_from_base(
        workflow,
        human_gates={"publish": HumanGateSpec(name="approve_publish")},
    )

    assert spec.stages[0].human_gate == HumanGateSpec(name="approve_publish")

    with pytest.raises(HumanGateRequired):
        WorkflowRunner().run(spec, {"draft": "ready"}, human_gate_mode="pause")
