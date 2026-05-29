"""Tests for CalendarPlanner prompt construction helpers."""

from __future__ import annotations

from nori.core import KPIPlan, OperationPlan, ClientBrief

from datetime import date

from nori.context_building.calendar_planner.package import CalendarPlannerPromptBuilder


calendar_planner_prompts = CalendarPlannerPromptBuilder()


def _operation_plan() -> OperationPlan:
    return OperationPlan(
        plan_id="plan_7d",
        horizon_days=7,
        objectives=["建立认知"],
        content_pillars=["花艺知识"],
    )


def _kpi_plan() -> KPIPlan:
    return KPIPlan(plan_id="kpi_7d", targets={"content_tasks": 3})


def _brief() -> ClientBrief:
    return ClientBrief(brand_name="春日花房", platform="xhs", audience=["周边家庭"])


def test_build_user_prompt_serializes_plan_kpi_brief_and_window():
    prompt = calendar_planner_prompts.build_user_prompt(
        _operation_plan(),
        _kpi_plan(),
        _brief(),
        start_date=date(2026, 5, 25),
        horizon_days=7,
    )

    assert "运营计划" in prompt
    assert '"plan_id": "plan_7d"' in prompt
    assert '"content_tasks": 3' in prompt
    assert '"brand_name": "春日花房"' in prompt
    assert "只规划 7 天，从 2026-05-25 开始" in prompt
    assert "{operation_plan}" not in prompt
    assert "{kpi_plan}" not in prompt
    assert "{client_context}" not in prompt


def test_calendar_prompt_constants_keep_json_only_contract():
    assert "只输出 JSON" in calendar_planner_prompts.system_prompt
    assert "输出 JSON，字段固定" in calendar_planner_prompts.user_prompt_template
