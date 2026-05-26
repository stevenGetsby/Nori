"""Tests for AccountPlanner keyword normalization helpers."""

from __future__ import annotations

from nori.user_profiling.account_planner import keywords as account_plan_keywords


def test_clean_keyword_strips_platform_tokens_and_separators():
    assert account_plan_keywords.clean_keyword("小红书 反焦虑 文创 xhs") == "反焦虑文创"
    assert account_plan_keywords.clean_keyword("抖音：本地 花店 / dy") == "本地花店"


def test_normalize_keyword_levels_uses_explicit_rows_with_reason_fallbacks():
    levels = account_plan_keywords.normalize_keyword_levels(
        [
            {"level": 1, "role": "赛道", "keyword": "文创 小红书", "reason": "看文创大盘"},
            {"level": 2, "role": "主题", "keyword": "反焦虑 文创 xhs", "reason": "看文创大盘"},
            {"level": 9, "keyword": "怪趣 主理人"},
            {"level": 3, "keyword": "怪趣 主理人"},
        ],
        fallback=[],
        search_keywords=[],
    )

    assert levels == [
        {"level": 1, "role": "赛道", "keyword": "文创", "reason": "看文创大盘"},
        {"level": 2, "role": "主题", "keyword": "反焦虑文创", "reason": "用于聚焦本次内容创作主题。"},
        {"level": 3, "role": "内容点", "keyword": "怪趣主理人", "reason": "用于贴近本次内容创作的具体内容点。"},
    ]


def test_normalize_keyword_levels_falls_back_to_search_keywords_then_fallback_rows():
    search_levels = account_plan_keywords.normalize_keyword_levels(
        "bad",
        fallback=[],
        search_keywords=["小红书 香薰", "通勤 香气", "复购 香薰", "ignored"],
    )
    fallback_levels = account_plan_keywords.normalize_keyword_levels(
        "bad",
        fallback=[{"level": 1, "keyword": "花艺 xhs", "reason": "fallback"}],
        search_keywords=[],
    )

    assert [item["keyword"] for item in search_levels] == ["香薰", "通勤香气", "复购香薰"]
    assert account_plan_keywords.keywords_from_levels(search_levels) == ["香薰", "通勤香气", "复购香薰"]
    assert fallback_levels == [{"level": 1, "role": "赛道", "keyword": "花艺", "reason": "fallback"}]
