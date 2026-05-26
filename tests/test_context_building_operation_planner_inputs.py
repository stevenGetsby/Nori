"""Tests for OperationPlanner input normalization helpers."""

from __future__ import annotations

from nori.core import ClientBrief

from datetime import date

from nori.user_profiling.models import AccountPlanResult
from nori.context_building.operation_planner import inputs as operation_planner_inputs


def test_normalize_client_brief_restores_dicts_and_preserves_instances():
    brief = ClientBrief(client_name="花店主理人", brand_name="春日花房", goals=["建立认知"])

    assert operation_planner_inputs.normalize_client_brief(brief) is brief

    restored = operation_planner_inputs.normalize_client_brief(brief.to_dict())

    assert restored.client_name == "花店主理人"
    assert restored.brand_name == "春日花房"
    assert restored.goals == ["建立认知"]


def test_normalize_account_plan_restores_clean_dict_fields():
    value = {
        "tags": {"track": "花艺", "platform": "小红书"},
        "recommended_positioning": "社区花艺顾问",
        "audience_profile": [" 周边家庭 ", "", None],
        "content_directions": "花材养护",
        "benchmark_accounts": {"search_keywords": ["花艺"]},
        "unique_selling_points": [" 本地配送快 "],
        "ip_portrait_report": {"content_pillars": []},
    }

    plan = operation_planner_inputs.normalize_account_plan(value)

    assert isinstance(plan, AccountPlanResult)
    assert plan.tags == {"track": "花艺", "platform": "小红书"}
    assert plan.audience_profile == ["周边家庭"]
    assert plan.content_directions == ["花材养护"]
    assert plan.unique_selling_points == ["本地配送快"]
    assert plan.benchmark_accounts == {"search_keywords": ["花艺"]}
    assert plan.ip_portrait_report == {"content_pillars": []}
    assert operation_planner_inputs.normalize_account_plan(None) is None


def test_account_plan_dict_returns_empty_mapping_for_absent_plan():
    plan = AccountPlanResult(
        tags={"track": "花艺"},
        recommended_positioning="社区花艺顾问",
        audience_profile=["周边家庭"],
        content_directions=[],
        benchmark_accounts={},
        unique_selling_points=[],
        ip_portrait_report={},
    )

    assert operation_planner_inputs.account_plan_dict(plan)["recommended_positioning"] == "社区花艺顾问"
    assert operation_planner_inputs.account_plan_dict(None) == {}


def test_run_parameters_are_bounded_and_dates_are_normalized():
    assert operation_planner_inputs.bounded_horizon(None) == 7
    assert operation_planner_inputs.bounded_horizon(True) == 7
    assert operation_planner_inputs.bounded_horizon(0) == 1
    assert operation_planner_inputs.bounded_horizon(120) == 90
    assert operation_planner_inputs.bounded_horizon("14") == 14
    assert operation_planner_inputs.normalize_start_date("2026-05-25") == date(2026, 5, 25)
    assert operation_planner_inputs.normalize_start_date(date(2026, 5, 26)) == date(2026, 5, 26)
