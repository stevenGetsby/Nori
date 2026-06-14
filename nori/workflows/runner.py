"""LangGraph-backed workflow runner with run/stage bookkeeping."""
from __future__ import annotations

from contextlib import contextmanager
import queue
import signal
import threading
from typing import Any

from langchain_core.runnables import RunnableLambda
from langgraph.graph import END, START, StateGraph
from nori.core import StoredArtifact

from .schemas import HumanGateRequired, StageRun, StageTimeoutError, WorkflowRun, WorkflowSpec


class WorkflowRunner:
    """Execute a WorkflowSpec as a LangGraph state graph."""

    def __init__(self, *, checkpointer: Any | None = None) -> None:
        self.checkpointer = checkpointer

    def run(
        self,
        spec: WorkflowSpec,
        initial: Any,
        *,
        session_id: str = "",
        task_id: str = "",
        human_gate_mode: str = "skip",
    ) -> tuple[Any, WorkflowRun]:
        workflow_run = WorkflowRun(workflow_name=spec.name, session_id=session_id, task_id=task_id)
        workflow_run.metadata.update({
            "engine": "langgraph",
            "langchain_runnable": "RunnableLambda",
            "checkpoint_saver": type(self.checkpointer).__name__ if self.checkpointer is not None else "",
            "human_gate_mode": _normalize_human_gate_mode(human_gate_mode),
        })
        workflow_run.start()
        if not spec.stages:
            workflow_run.finish()
            return initial, workflow_run

        graph = _compile_graph(spec, human_gate_mode=human_gate_mode, checkpointer=self.checkpointer)
        state = {
            "value": initial,
            "workflow_run": workflow_run,
        }
        try:
            result = graph.invoke(
                state,
                config={"configurable": {"thread_id": workflow_run.run_id}},
            )
        except HumanGateRequired as exc:
            if not hasattr(exc, "workflow_run"):
                setattr(exc, "workflow_run", workflow_run)
            raise
        except Exception as exc:
            if not hasattr(exc, "workflow_run"):
                setattr(exc, "workflow_run", workflow_run)
            if workflow_run.status != "failed":
                workflow_run.fail(exc)
            raise
        workflow_run.finish()
        return result["value"], workflow_run


def _compile_graph(spec: WorkflowSpec, *, human_gate_mode: str, checkpointer: Any | None = None):
    builder = StateGraph(dict)
    node_names = []
    for index, stage in enumerate(spec.stages):
        node_name = f"{index:03d}_{stage.name}"
        node_names.append(node_name)
        builder.add_node(node_name, _stage_node(stage, RunnableLambda(stage.handler), human_gate_mode))
    builder.add_edge(START, node_names[0])
    for current, next_node in zip(node_names, node_names[1:]):
        builder.add_edge(current, next_node)
    builder.add_edge(node_names[-1], END)
    return builder.compile(checkpointer=checkpointer)


def _stage_node(stage, runnable: RunnableLambda, human_gate_mode: str):
    def run_stage(state: dict[str, Any]) -> dict[str, Any]:
        workflow_run = state["workflow_run"]
        _handle_human_gate(stage, workflow_run, human_gate_mode)
        stage_run = StageRun(stage_name=stage.name)
        workflow_run.stages.append(stage_run)
        stage_run.start()
        timeout_seconds = _stage_timeout_seconds(stage)
        if timeout_seconds is not None:
            stage_run.metadata.update(_stage_timeout_metadata(timeout_seconds))
        try:
            value = _invoke_stage_handler(stage.name, runnable, state["value"], timeout_seconds)
        except Exception as exc:
            stage_run.fail(exc)
            workflow_run.fail(exc)
            setattr(exc, "workflow_run", workflow_run)
            raise
        artifact_ref = _artifact_ref_for(stage.name, value)
        stage_run.finish(output_ref=artifact_ref)
        if artifact_ref:
            workflow_run.artifact_refs.append(artifact_ref)
        return {
            "value": value,
            "workflow_run": workflow_run,
        }

    return run_stage


def _stage_timeout_seconds(stage: Any) -> float | None:
    value = getattr(stage, "timeout_seconds", None)
    if value is None:
        return None
    try:
        seconds = float(value)
    except (TypeError, ValueError):
        return None
    return seconds if seconds > 0 else None


def _stage_timeout_metadata(timeout_seconds: float) -> dict[str, Any]:
    if threading.current_thread() is threading.main_thread():
        return {
            "timeout_seconds": timeout_seconds,
            "timeout_enforcement": "signal",
            "timeout_cancellation": "interrupts_current_call",
        }
    return {
        "timeout_seconds": timeout_seconds,
        "timeout_enforcement": "worker_thread",
        "timeout_cancellation": "request_returns_worker_may_continue",
    }


def _invoke_stage_handler(stage_name: str, runnable: RunnableLambda, value: Any, timeout_seconds: float | None) -> Any:
    if timeout_seconds is None:
        return runnable.invoke(value)
    if threading.current_thread() is threading.main_thread():
        with _stage_timeout(stage_name, timeout_seconds):
            return runnable.invoke(value)
    return _invoke_stage_handler_in_daemon_thread(stage_name, runnable, value, timeout_seconds)


def _invoke_stage_handler_in_daemon_thread(
    stage_name: str,
    runnable: RunnableLambda,
    value: Any,
    timeout_seconds: float,
) -> Any:
    result_queue: queue.Queue[tuple[str, Any]] = queue.Queue(maxsize=1)

    def target() -> None:
        try:
            result_queue.put(("ok", runnable.invoke(value)))
        except Exception as exc:  # noqa: BLE001
            result_queue.put(("error", exc))

    worker = threading.Thread(target=target, name=f"nori-stage-{stage_name}", daemon=True)
    worker.start()
    worker.join(timeout_seconds)
    if worker.is_alive():
        raise StageTimeoutError(stage_name, timeout_seconds)
    status, payload = result_queue.get_nowait()
    if status == "error":
        raise payload
    return payload


@contextmanager
def _stage_timeout(stage_name: str, timeout_seconds: float | None):
    if timeout_seconds is None:
        yield
        return

    previous_handler = signal.getsignal(signal.SIGALRM)
    previous_timer = signal.setitimer(signal.ITIMER_REAL, timeout_seconds)

    def _raise_timeout(_signum, _frame):
        raise StageTimeoutError(stage_name, timeout_seconds)

    signal.signal(signal.SIGALRM, _raise_timeout)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous_handler)
        if previous_timer[0] > 0:
            signal.setitimer(signal.ITIMER_REAL, previous_timer[0], previous_timer[1])


def _handle_human_gate(stage, workflow_run: WorkflowRun, human_gate_mode: str) -> None:
    gate = getattr(stage, "human_gate", None)
    if gate is None:
        return
    mode = _normalize_human_gate_mode(human_gate_mode)
    gate_run = StageRun(stage_name=f"human_gate:{gate.name}")
    gate_run.metadata.update({
        "type": "human_gate",
        "mode": mode,
        "target_stage": stage.name,
    })
    if gate.prompt:
        gate_run.metadata["prompt"] = gate.prompt
    gate_run.metadata.update(dict(gate.metadata))
    workflow_run.stages.append(gate_run)
    gate_run.start()
    if mode in {"skip", "ignore", "test", "off"}:
        gate_run.skip()
        return
    if mode in {"pause", "require", "required"}:
        gate_run.wait_for_human()
        workflow_run.wait_for_human(gate_name=gate.name, stage_name=stage.name)
        raise HumanGateRequired(gate.name, stage.name, workflow_run)
    raise ValueError(f"unknown human_gate_mode: {human_gate_mode}")


def _normalize_human_gate_mode(mode: str) -> str:
    return str(mode or "skip").strip().lower() or "skip"


def _artifact_ref_for(stage_name: str, value: Any) -> str:
    if isinstance(value, StoredArtifact):
        return str(value.path)
    if not isinstance(value, dict):
        return ""
    refs = value.get("_artifact_refs")
    if isinstance(refs, dict):
        ref = _artifact_ref_value(refs.get(stage_name))
        if ref:
            return ref
    return _artifact_ref_value(value.get("_artifact_ref"))


def _artifact_ref_value(value: Any) -> str:
    if isinstance(value, StoredArtifact):
        return str(value.path)
    return str(value or "").strip()


__all__ = ["WorkflowRunner"]
