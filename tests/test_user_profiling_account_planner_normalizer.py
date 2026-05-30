"""Tests for AccountPlanner LLM result normalization helpers."""

from __future__ import annotations

from nori.agents.user_profiling.models import AccountPlanResult
from nori.agents.user_profiling.account_planner import normalizer as account_plan_normalizer


def _fallback() -> AccountPlanResult:
    return AccountPlanResult(
        tags={
            "track": "待判断",
            "goal": "涨粉",
            "platform": "小红书",
            "product": "待判断",
            "positioning": "待判断",
        },
        recommended_positioning="需要 LLM 推理账号定位。",
        audience_profile=["默认受众"],
        content_directions=["默认方向"],
        benchmark_accounts={
            "keyword_levels": [],
            "search_keywords": [],
            "accounts": [],
            "search_results": [],
        },
        unique_selling_points=["默认卖点"],
        ip_portrait_report={
            "account_name_suggestions": ["默认账号名"],
            "account_keywords": ["默认关键词"],
            "content_pillars": [],
            "benchmark_creators": [],
            "cover_design_formats": [],
        },
        metadata={"source": "fallback"},
    )


def test_normalize_llm_result_cleans_keywords_and_derives_ip_benchmarks():
    data = {
        "tags": {
            "track": "怪趣文创",
            "goal": "涨粉带货",
            "platform": "小红书",
            "product": "文创周边",
            "positioning": "反焦虑主理人",
        },
        "recommended_positioning": "做一个用怪趣表达反焦虑的文创主理人账号。",
        "audience_profile": ["高压打工人", "高压打工人", "怪趣审美用户"],
        "content_directions": ["厕所哲学短故事"],
        "benchmark_accounts": {
            "keyword_levels": [
                {"level": 1, "role": "赛道", "keyword": "文创 小红书", "reason": "看文创大盘"},
                {"level": 2, "role": "主题", "keyword": "反焦虑 文创 xhs", "reason": "看文创大盘"},
                {"level": 3, "role": "内容点", "keyword": "怪趣 主理人", "reason": "看账号表达调性"},
            ],
            "accounts": [
                {"name": "搜索：反焦虑文创", "platform": "小红书", "reason": "找相似表达", "keyword": "反焦虑 文创 xhs"}
            ],
        },
        "unique_selling_points": ["粗俗语言包装体面诉求"],
        "ip_portrait_report": {
            "account_name_suggestions": ["便便精神合作社"],
            "account_keywords": ["反焦虑", "怪趣文创"],
            "content_pillars": [{"name": "厕所哲学", "description": "用轻观点表达反焦虑"}],
            "cover_design_formats": [{"name": "大字观点封面", "layout": "大字加IP"}],
        },
    }
    search_results = [{"title": "搜索命中", "keyword": "文创"}]

    result = account_plan_normalizer.normalize_llm_result(data, _fallback(), search_results)

    assert result.metadata == {"source": "fallback"}
    assert result.benchmark_accounts["search_results"] == search_results
    assert result.benchmark_accounts["search_keywords"] == ["文创", "反焦虑文创", "怪趣主理人"]
    assert result.benchmark_accounts["keyword_levels"][1]["reason"] == "用于聚焦本次内容创作主题。"
    assert result.benchmark_accounts["accounts"][0]["keyword"] == "反焦虑文创"
    assert result.ip_portrait_report["benchmark_creators"] == [
        {"name": "搜索：反焦虑文创", "platform": "小红书", "reason": "找相似表达", "keyword": "反焦虑文创"}
    ]
    assert result.ip_portrait_report["cover_design_formats"][0]["ratio"] == "3:4"


def test_normalize_llm_result_uses_search_keywords_when_levels_missing():
    data = {
        "benchmark_accounts": {
            "keyword_levels": "bad",
            "search_keywords": ["小红书 香薰", "通勤 香气", "复购 香薰", "第四个不进入"],
        }
    }

    result = account_plan_normalizer.normalize_llm_result(data, _fallback(), [])

    assert result.tags["goal"] == "涨粉"
    assert result.benchmark_accounts["search_keywords"] == ["香薰", "通勤香气", "复购香薰"]
    assert [item["level"] for item in result.benchmark_accounts["keyword_levels"]] == [1, 2, 3]
    assert result.audience_profile == ["默认受众"]
