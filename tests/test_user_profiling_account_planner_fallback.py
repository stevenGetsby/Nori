"""Tests for AccountPlanner deterministic fallback plan."""

from __future__ import annotations

from nori.agents.user_profiling.models import AccountPlannerInput
from nori.agents.user_profiling.account_planner import fallback as account_plan_fallback


def test_fallback_plan_preserves_platform_and_goal_without_keyword_inference():
    normalized = AccountPlannerInput(
        text="做一个花店账号",
        intention={"goal": "提升到店咨询并沉淀复购用户"},
        platform="xhs",
    )

    result = account_plan_fallback.fallback_plan(normalized)

    assert result.tags == {
        "track": "待判断",
        "goal": "提升到店咨询并沉淀复购用户"[:20],
        "platform": "小红书",
        "product": "待判断",
        "positioning": "待判断",
    }
    assert result.recommended_positioning == "需要 LLM 根据 Intention + Context 推理账号定位。"
    assert result.audience_profile == []
    assert result.content_directions == []
    assert result.unique_selling_points == []
    assert result.benchmark_accounts == {
        "keyword_levels": [],
        "search_keywords": [],
        "accounts": [],
        "search_results": [],
    }


def test_fallback_plan_uses_empty_ip_portrait_sections_and_platform_labels():
    result = account_plan_fallback.fallback_plan(AccountPlannerInput(text="", platform="douyin"))

    assert result.tags["goal"] == "待判断"
    assert result.tags["platform"] == "抖音"
    assert result.ip_portrait_report == {
        "account_name_suggestions": [],
        "account_keywords": [],
        "content_pillars": [],
        "benchmark_creators": [],
        "cover_design_formats": [],
    }
