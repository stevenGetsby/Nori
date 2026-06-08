"""Artifact helpers for content production workflow stages."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .state import ContentProductionState
from nori.agents.market_analysis.xhs_note_analyzer import skills_output


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, default=str), encoding="utf-8")


def with_artifact(state: ContentProductionState, stage_name: str, path: Path) -> ContentProductionState:
    refs = dict(state.get("_artifact_refs") or {})
    refs[stage_name] = str(path)
    return {**state, "_artifact_refs": refs}


def persist_final_state_artifacts(state: ContentProductionState) -> None:
    """Materialize canonical JSON artifacts from a completed content-production state."""

    run_dir = state["run_dir"]
    _write_if_present(run_dir / "xhs_top_notes_result.json", state.get("top_result"))
    _write_if_present(run_dir / "market_session_skill_report.json", state.get("market_report"))
    market_report = state.get("market_report")
    if market_report is not None:
        write_json(run_dir / "note_skill_guides.json", skills_output(_to_dict(market_report)))
    _write_if_present(run_dir / "intake_result.json", state.get("intake"))
    _write_if_present(run_dir / "account_plan.json", state.get("account_plan"))
    _write_if_present(run_dir / "client_brief.json", state.get("client_brief"))
    _write_if_present(run_dir / "operation_project.json", state.get("project"))
    _write_if_present(run_dir / "kpi_plan.json", state.get("kpi_plan"))
    _write_if_present(run_dir / "content_calendar.json", state.get("calendar"))
    _write_if_present(run_dir / "selected_task.json", state.get("task"))
    _write_if_present(run_dir / "content_context_pack.json", state.get("content_context_pack"))
    _write_if_present(run_dir / "content_design_spec.json", state.get("content_spec"))
    _write_if_present(run_dir / "content_package.json", state.get("package"))
    reviews = state.get("reviews")
    if reviews is not None:
        write_json(run_dir / "reviews.json", [_to_dict(review) for review in reviews])


def _write_if_present(path: Path, value: Any) -> None:
    if value is not None:
        write_json(path, _to_dict(value))


def _to_dict(value: Any) -> Any:
    if hasattr(value, "to_dict"):
        return value.to_dict()
    return value
