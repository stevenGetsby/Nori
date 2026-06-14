"""Tests for AccountPlanner search execution helpers."""

from __future__ import annotations

from nori.agents.user_profiling.schemas import AccountPlanResult, AccountPlannerInput
from nori.agents.user_profiling.account_planner import search as account_plan_search


def _result() -> AccountPlanResult:
    return AccountPlanResult(
        tags={"platform": "小红书"},
        recommended_positioning="",
        audience_profile=[],
        content_directions=[],
        benchmark_accounts={
            "search_keywords": ["小红书 文创", "文创 xhs", "反焦虑 文创", ""],
            "keyword_levels": [],
            "accounts": [],
            "search_results": [],
        },
        unique_selling_points=[],
        ip_portrait_report={},
    )


def test_run_search_cleans_dedupes_keywords_and_adds_defaults():
    class Provider:
        def __init__(self):
            self.calls = []

        def search(self, *, platform, keyword, limit):
            self.calls.append({"platform": platform, "keyword": keyword, "limit": limit})
            return [{"title": f"{keyword} case"}, {"title": "overflow"}]

    provider = Provider()
    rows = account_plan_search.run_search(
        provider,
        AccountPlannerInput(platform="xhs", search_limit=1),
        _result(),
    )

    assert provider.calls == [
        {"platform": "xhs", "keyword": "文创", "limit": 1},
        {"platform": "xhs", "keyword": "反焦虑文创", "limit": 1},
    ]
    assert rows == [
        {"title": "文创 case", "platform": "xhs", "keyword": "文创"},
        {"title": "反焦虑文创 case", "platform": "xhs", "keyword": "反焦虑文创"},
    ]


def test_run_search_isolates_provider_errors_and_empty_provider_returns_empty():
    class FailingProvider:
        def search(self, *, platform, keyword, limit):  # noqa: ARG002
            raise RuntimeError("provider down")

    assert account_plan_search.run_search(
        account_plan_search.EmptySearchProvider(),
        AccountPlannerInput(platform="dy"),
        _result(),
    ) == []
    assert account_plan_search.run_search(
        FailingProvider(),
        AccountPlannerInput(platform="dy"),
        _result(),
    ) == []
