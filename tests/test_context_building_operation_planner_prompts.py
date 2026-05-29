"""Tests for OperationPlanner prompt construction helpers."""

from __future__ import annotations

from nori.core import ClientBrief

from nori.user_profiling.models import AccountPlanResult
from nori.context_building.operation_planner.package import OperationPlannerPromptBuilder


operation_planner_prompts = OperationPlannerPromptBuilder()


def _brief() -> ClientBrief:
    return ClientBrief(
        client_name="花店主理人",
        brand_name="春日花房",
        platform="xhs",
        goals=["建立本地认知"],
    )


def _account_plan() -> AccountPlanResult:
    return AccountPlanResult(
        tags={"track": "花艺", "platform": "小红书"},
        recommended_positioning="社区花艺顾问",
        audience_profile=["周边家庭"],
        content_directions=["节日花束"],
        benchmark_accounts={"search_keywords": ["花艺"]},
        unique_selling_points=["本地配送快"],
        ip_portrait_report={"content_pillars": [{"name": "花艺知识"}]},
    )


def test_build_user_prompt_serializes_brief_account_plan_and_horizon():
    prompt = operation_planner_prompts.build_user_prompt(
        _brief(),
        _account_plan(),
        horizon_days=14,
    )

    assert "客户简报" in prompt
    assert '"brand_name": "春日花房"' in prompt
    assert '"recommended_positioning": "社区花艺顾问"' in prompt
    assert "只规划 14 天" in prompt
    assert "{client_brief}" not in prompt
    assert "{account_plan}" not in prompt
    assert "{horizon_days}" not in prompt


def test_build_user_prompt_uses_empty_account_plan_mapping_when_absent():
    prompt = operation_planner_prompts.build_user_prompt(_brief(), None, horizon_days=7)

    assert "账号定位结果：\n{}" in prompt
    assert "只规划 7 天" in prompt


def test_operation_planner_prompt_constants_keep_json_only_contract():
    assert "只输出 JSON" in operation_planner_prompts.system_prompt
    assert "输出 JSON，字段固定" in operation_planner_prompts.user_prompt_template
