"""Tests for KPIPlanner prompt construction helpers."""

from __future__ import annotations

from nori.core import OperationPlan

from nori.context_building.kpi_planner import prompts as kpi_planner_prompts


def _operation_plan() -> OperationPlan:
    return OperationPlan(
        plan_id="plan_7d",
        horizon_days=7,
        objectives=["建立本地认知"],
        content_pillars=["花艺知识"],
        kpi_targets={"followers": 50},
    )


def test_build_user_prompt_serializes_operation_plan_and_project_context():
    prompt = kpi_planner_prompts.build_user_prompt(
        _operation_plan(),
        {"project_id": "ops_001", "content_task_count": 3},
    )

    assert "运营计划" in prompt
    assert '"plan_id": "plan_7d"' in prompt
    assert '"followers": 50' in prompt
    assert '"project_id": "ops_001"' in prompt
    assert '"content_task_count": 3' in prompt
    assert "{operation_plan}" not in prompt
    assert "{project_context}" not in prompt


def test_kpi_prompt_constants_keep_json_only_contract():
    assert "只输出 JSON" in kpi_planner_prompts.SYSTEM_PROMPT
    assert "输出 JSON，字段固定" in kpi_planner_prompts.USER_PROMPT_TEMPLATE
