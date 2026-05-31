"""LangGraph-backed workflow execution."""
from __future__ import annotations

from typing import Any

from langchain_core.runnables import RunnableLambda
from langgraph.graph import END, START, StateGraph

from .models import StageRun, WorkflowRun, WorkflowSpec


class LangGraphWorkflowRunner:
    """Execute a WorkflowSpec as a LangGraph state graph."""

    def run(
        self,
        spec: WorkflowSpec,
        initial: Any,
        *,
        session_id: str = "",
        task_id: str = "",
    ) -> tuple[Any, WorkflowRun]:
        workflow_run = WorkflowRun(workflow_name=spec.name, session_id=session_id, task_id=task_id)
        workflow_run.metadata.update({
            "engine": "langgraph",
            "langchain_runnable": "RunnableLambda",
        })
        workflow_run.start()
        if not spec.stages:
            workflow_run.finish()
            return initial, workflow_run

        graph = _compile_graph(spec)
        state = {
            "value": initial,
            "workflow_run": workflow_run,
        }
        try:
            result = graph.invoke(state)
        except Exception as exc:
            if not hasattr(exc, "workflow_run"):
                setattr(exc, "workflow_run", workflow_run)
            if workflow_run.status != "failed":
                workflow_run.fail(exc)
            raise
        workflow_run.finish()
        return result["value"], workflow_run


def _compile_graph(spec: WorkflowSpec):
    builder = StateGraph(dict)
    node_names = []
    for index, stage in enumerate(spec.stages):
        node_name = f"{index:03d}_{stage.name}"
        node_names.append(node_name)
        builder.add_node(node_name, _stage_node(stage.name, RunnableLambda(stage.handler)))
    builder.add_edge(START, node_names[0])
    for current, next_node in zip(node_names, node_names[1:]):
        builder.add_edge(current, next_node)
    builder.add_edge(node_names[-1], END)
    return builder.compile()


def _stage_node(stage_name: str, runnable: RunnableLambda):
    def run_stage(state: dict[str, Any]) -> dict[str, Any]:
        workflow_run = state["workflow_run"]
        stage_run = StageRun(stage_name=stage_name)
        workflow_run.stages.append(stage_run)
        stage_run.start()
        try:
            value = runnable.invoke(state["value"])
        except Exception as exc:
            stage_run.fail(exc)
            workflow_run.fail(exc)
            setattr(exc, "workflow_run", workflow_run)
            raise
        artifact_ref = _artifact_ref_for(stage_name, value)
        stage_run.finish(output_ref=artifact_ref)
        if artifact_ref:
            workflow_run.artifact_refs.append(artifact_ref)
        return {
            "value": value,
            "workflow_run": workflow_run,
        }

    return run_stage


def _artifact_ref_for(stage_name: str, value: Any) -> str:
    if not isinstance(value, dict):
        return ""
    refs = value.get("_artifact_refs")
    if isinstance(refs, dict):
        ref = str(refs.get(stage_name) or "").strip()
        if ref:
            return ref
    return str(value.get("_artifact_ref") or "").strip()


__all__ = ["LangGraphWorkflowRunner"]
