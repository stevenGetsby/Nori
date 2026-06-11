from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

from data_collect.adapter import TopNotesResult
from nori.core import ClientBrief, ContentTask, LLMFactory
from nori.workflows.content_production.artifacts import persist_final_state_artifacts
from nori.workflows.content_production import ContentProductionConfig, ContentProductionWorkflow
from nori.workflows.content_production.stages import ContentProductionStages


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
        "intake",
        "search_query_plan",
        "xhs_top_notes",
        "market_skill_report",
        "account_plan",
        "client_brief",
        "operation_project",
        "kpi_plan",
        "content_calendar",
        "selected_task",
        "intent_contract",
        "content_context",
        "content_design_spec",
        "content_package",
        "reviews",
        "summary",
    ]
    assert spec.stages[13].human_gate is not None
    assert spec.stages[13].human_gate.name == "approve_content_design_spec"
    assert spec.stages[13].human_gate.metadata == {"artifact": "content_design_spec.json"}
    assert all(stage.timeout_seconds == 180 for stage in spec.stages if stage.name != "content_package")
    assert spec.stages[13].timeout_seconds == 240


def test_content_production_workflow_allows_content_package_timeout_override():
    config = replace(_config(), stage_timeout_seconds=9, content_package_timeout_seconds=12)

    spec = ContentProductionWorkflow(config=config).build_spec()

    assert all(stage.timeout_seconds == 9 for stage in spec.stages if stage.name != "content_package")
    assert spec.stages[13].name == "content_package"
    assert spec.stages[13].timeout_seconds == 12


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
        "search_query_plan": _Dictable(ok="search"),
        "account_plan": _Dictable(ok="account"),
        "client_brief": _Dictable(ok="brief"),
        "project": _Dictable(ok="project"),
        "kpi_plan": _Dictable(ok="kpi"),
        "calendar": _Dictable(ok="calendar"),
        "task": _Dictable(ok="task"),
        "intent_contract": _Dictable(ok="intent"),
        "content_context_pack": _Dictable(ok="context"),
        "content_spec": _Dictable(ok="spec"),
        "package": _Dictable(ok="package"),
        "reviews": [_Dictable(ok="review")],
    }

    persist_final_state_artifacts(state)

    assert (tmp_path / "xhs_top_notes_result.json").is_file()
    assert (tmp_path / "market_session_skill_report.json").is_file()
    assert (tmp_path / "note_skill_guides.json").is_file()
    assert (tmp_path / "search_query_plan.json").is_file()
    assert (tmp_path / "intent_contract.json").is_file()
    assert (tmp_path / "content_design_spec.json").is_file()
    assert (tmp_path / "content_package.json").is_file()
    assert (tmp_path / "reviews.json").is_file()


def test_intent_contract_stage_freezes_selected_task_and_client_brief(tmp_path):
    stages = ContentProductionStages(_config())
    task = ContentTask(
        task_id="task_1",
        title="AI工具伪需求判断",
        platform="xhs",
        content_type="image_text_post",
        topic="AI工具伪需求",
        objective="生成可收藏判断框架",
        brief={"must_include": ["5步判断", "伪需求"], "tone": ["干货"]},
    )
    state = {
        "run_dir": tmp_path,
        "client_brief": ClientBrief(
            brand_name="Nori",
            platform="xhs",
            goals=["提升内容可信度"],
            audience=["AI工具用户"],
            constraints=["干货专业"],
            taboos=["不要编造数据"],
        ),
        "task": task,
        "_artifact_refs": {},
    }

    next_state = stages.intent_contract(state)

    contract = next_state["intent_contract"]
    assert contract.contract_id == f"intent_{tmp_path.name}_task_1"
    assert contract.must_include == ["Nori", "AI工具伪需求", "5步判断", "伪需求"]
    assert contract.deliverables == ["image_text_post"]
    assert contract.taboos == ["不要编造数据"]
    assert next_state["_artifact_refs"]["intent_contract"] == str(tmp_path / "intent_contract.json")
    assert json.loads((tmp_path / "intent_contract.json").read_text(encoding="utf-8"))["contract_id"] == contract.contract_id


def test_search_query_plan_uses_intaker_result_and_three_keyword_layers(tmp_path):
    stages = ContentProductionStages(_config())
    factory = LLMFactory(chat_json_func=lambda *_args, **_kwargs: {
        "track_keywords": ["AI工具", "效率工具"],
        "topic_keywords": ["AI工具更新", "新功能判断"],
        "content_point_keywords": ["伪需求判断", "工具避坑"],
        "rationale": "从赛道到具体判断框架递进。",
    })
    state = {
        "run_dir": tmp_path,
        "brief_text": "做一篇 AI 工具更新后如何判断是不是伪需求的小红书图文",
        "intake": _Dictable(
            intention={"goal": "产品种草", "format": "小红书图文"},
            context={"guardrails": ["不要编造数据"]},
        ),
        "llm_factory": factory,
        "_artifact_refs": {},
    }

    next_state = stages.search_query_plan(state)

    plan = next_state["search_query_plan"]
    assert [layer["level"] for layer in plan["layers"]] == ["track", "topic", "content_point"]
    assert plan["layers"][0]["keywords"] == ["AI工具", "效率工具"]
    assert plan["layers"][1]["keywords"] == ["AI工具更新", "新功能判断"]
    assert plan["layers"][2]["keywords"] == ["伪需求判断", "工具避坑"]
    assert plan["flattened_keywords"] == ["AI工具", "效率工具", "AI工具更新", "新功能判断", "伪需求判断", "工具避坑"]
    assert plan["top_k_per_keyword"] == 3
    assert (tmp_path / "search_query_plan.json").is_file()


def test_xhs_top_notes_passes_layered_search_context_to_collector(tmp_path):
    captured = {}

    def collect(market_dir, search_context):
        captured["market_dir"] = market_dir
        captured["search_context"] = search_context
        return TopNotesResult(platform="xhs", queries=list(search_context["keywords"]), hot_notes=[], insufficient=[])

    stages = ContentProductionStages(_config())
    state = {
        "run_dir": tmp_path,
        "market_dir": tmp_path / "market",
        "top_notes_collector": collect,
        "search_query_plan": {
            "flattened_keywords": ["AI工具", "AI工具更新", "伪需求判断"],
            "top_k_per_keyword": 3,
        },
        "_artifact_refs": {},
    }
    state["market_dir"].mkdir()

    next_state = stages.xhs_top_notes(state)

    assert captured["market_dir"] == tmp_path / "market"
    assert captured["search_context"]["keywords"] == ["AI工具", "AI工具更新", "伪需求判断"]
    assert captured["search_context"]["top_k_per_keyword"] == 3
    assert next_state["top_result"].queries == ["AI工具", "AI工具更新", "伪需求判断"]
