from __future__ import annotations

import ast
from dataclasses import replace
from pathlib import Path

from nori.core import LLMFactory
from nori.workflows.content_production.artifacts import persist_final_state_artifacts
from nori.workflows.content_production import ContentProductionConfig, ContentProductionWorkflow


def _config() -> ContentProductionConfig:
    return ContentProductionConfig(
        workflow_name="test_content_production",
        client_name="Holly",
        brand_name="Holly Shit",
        platform="xhs",
        project_id_prefix="holly",
        project_name="Holly Project",
        topic="test topic",
        account_position="test account position",
        target_audience="test audience",
        goals=["goal"],
        positioning_notes=["positioning"],
        constraints=["constraint"],
        taboos=["taboo"],
        platform_rules=[{"rule": "rule"}],
    )


def test_content_production_workflow_declares_coarse_agent_stages_in_order():
    spec = ContentProductionWorkflow(config=_config()).build_spec()
    stage_names = [stage.name for stage in spec.stages]

    assert spec.name == "test_content_production"
    assert stage_names == [
        "xhs_top_notes",
        "market_skill_report",
        "intake",
        "account_plan",
        "client_brief",
        "operation_project",
        "kpi_plan",
        "content_calendar",
        "selected_task",
        "content_context",
        "content_design_spec",
        "content_package",
        "reviews",
        "summary",
    ]
    assert spec.stages[11].human_gate is not None
    assert spec.stages[11].human_gate.name == "approve_content_design_spec"
    assert spec.stages[11].human_gate.metadata == {"artifact": "content_design_spec.json"}
    assert all(stage.timeout_seconds == 180 for stage in spec.stages if stage.name != "content_package")
    assert spec.stages[11].timeout_seconds == 240


def test_content_production_workflow_allows_content_package_timeout_override():
    config = replace(_config(), stage_timeout_seconds=9, content_package_timeout_seconds=12)

    spec = ContentProductionWorkflow(config=config).build_spec()

    assert all(stage.timeout_seconds == 9 for stage in spec.stages if stage.name != "content_package")
    assert spec.stages[11].name == "content_package"
    assert spec.stages[11].timeout_seconds == 12


def test_content_production_workflow_initial_state_keeps_io_and_infra_injected(tmp_path):
    factory = LLMFactory()

    def collect(_market_dir: Path):
        raise AssertionError("collector should only be called by xhs_top_notes stage")

    state = ContentProductionWorkflow(config=_config()).initial_state(
        run_dir=tmp_path,
        market_dir=tmp_path / "market",
        covers_dir=tmp_path / "covers",
        llm_factory=factory,
        brief_text="brief",
        asset_paths=[tmp_path / "asset.png"],
        top_notes_collector=collect,
    )

    assert state["run_dir"] == tmp_path
    assert state["llm_factory"] is factory
    assert state["top_notes_collector"] is collect
    assert state["_artifact_refs"] == {}


def test_content_production_stage_support_owns_pure_builders():
    root = Path(__file__).resolve().parents[1]
    stages_path = root / "nori" / "workflows" / "content_production" / "stages.py"
    support_path = root / "nori" / "workflows" / "content_production" / "stage_support.py"
    stages_source = stages_path.read_text(encoding="utf-8")
    support_source = support_path.read_text(encoding="utf-8")
    stages_tree = ast.parse(stages_source)
    support_tree = ast.parse(support_source)

    assert support_path.is_file()
    assert "render_summary_markdown" in support_source
    assert "build_market_report" in support_source
    assert "asset_library_from_user_assets" in support_source
    assert "render_summary_markdown(" in stages_source
    assert "build_market_report(" in stages_source

    stage_function_names = {
        node.name
        for node in ast.walk(stages_tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    support_function_names = {
        node.name
        for node in ast.walk(support_tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    assert not {
        "build_market_report",
        "build_client_brief",
        "select_task",
        "content_strategy",
        "asset_library_from_user_assets",
        "render_summary_markdown",
    } & stage_function_names
    assert {
        "build_market_report",
        "build_client_brief",
        "select_task",
        "content_strategy",
        "asset_library_from_user_assets",
        "render_summary_markdown",
    } <= support_function_names


class _Dictable:
    def __init__(self, **data):
        self.data = data

    def to_dict(self):
        return dict(self.data)


def test_persist_final_state_artifacts_materializes_completed_state(tmp_path):
    state = {
        "run_dir": tmp_path,
        "top_result": _Dictable(hot_notes=[]),
        "market_report": _Dictable(skills=[]),
        "intake": _Dictable(ok="intake"),
        "account_plan": _Dictable(ok="account"),
        "client_brief": _Dictable(ok="brief"),
        "project": _Dictable(ok="project"),
        "kpi_plan": _Dictable(ok="kpi"),
        "calendar": _Dictable(ok="calendar"),
        "task": _Dictable(ok="task"),
        "content_context_pack": _Dictable(ok="context"),
        "content_spec": _Dictable(ok="spec"),
        "package": _Dictable(ok="package"),
        "reviews": [_Dictable(ok="review")],
    }

    persist_final_state_artifacts(state)

    assert (tmp_path / "xhs_top_notes_result.json").is_file()
    assert (tmp_path / "market_session_skill_report.json").is_file()
    assert (tmp_path / "note_skill_guides.json").is_file()
    assert (tmp_path / "content_design_spec.json").is_file()
    assert (tmp_path / "content_package.json").is_file()
    assert (tmp_path / "reviews.json").is_file()
