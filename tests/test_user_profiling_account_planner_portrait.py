"""Tests for AccountPlanner IP portrait and benchmark cleanup."""

from __future__ import annotations

from nori.agents.user_profiling.account_planner import portrait as account_plan_portrait


def test_account_list_cleans_keywords_limits_rows_and_uses_fallback():
    fallback = [{"name": "默认账号", "platform": "小红书", "reason": "默认理由", "keyword": "默认 小红书"}]

    assert account_plan_portrait.account_list("bad", fallback) == [
        {"name": "默认账号", "platform": "小红书", "reason": "默认理由", "keyword": "默认"}
    ]

    rows = [
        {"name": f"账号{i}", "platform": "小红书", "reason": "参考", "keyword": f"关键词{i} xhs"}
        for i in range(6)
    ]

    cleaned = account_plan_portrait.account_list(rows, fallback)

    assert len(cleaned) == 5
    assert cleaned[0] == {"name": "账号0", "platform": "小红书", "reason": "参考", "keyword": "关键词0"}


def test_normalize_ip_portrait_report_uses_explicit_creators_and_defaults_cover_ratio():
    report = account_plan_portrait.normalize_ip_portrait_report(
        {
            "account_name_suggestions": ["春日花房"],
            "account_keywords": ["花艺", "社区"],
            "content_pillars": [{"description": "花材养护和搭配"}],
            "benchmark_creators": [
                {"name": "花艺参考号", "platform": "小红书", "reason": "本地内容", "keyword": "花艺 xhs"}
            ],
            "cover_design_formats": [{"name": "大字封面", "layout": "大字加实拍", "reason": "清晰"}],
        },
        fallback={},
        benchmark_accounts={"accounts": []},
    )

    assert report["content_pillars"] == [{"name": "花材养护和搭配", "description": "花材养护和搭配"}]
    assert report["benchmark_creators"] == [
        {"name": "花艺参考号", "platform": "小红书", "reason": "本地内容", "keyword": "花艺"}
    ]
    assert report["cover_design_formats"] == [
        {"name": "大字封面", "ratio": "3:4", "layout": "大字加实拍", "reason": "清晰"}
    ]


def test_normalize_ip_portrait_report_derives_creators_from_benchmark_accounts():
    report = account_plan_portrait.normalize_ip_portrait_report(
        {},
        fallback={"account_keywords": ["默认关键词"], "benchmark_creators": []},
        benchmark_accounts={
            "accounts": [
                {"name": "搜索命中", "platform": "小红书", "reason": "相似表达", "keyword": "花艺 小红书"}
            ]
        },
    )

    assert report["account_keywords"] == ["默认关键词"]
    assert report["benchmark_creators"] == [
        {"name": "搜索命中", "platform": "小红书", "reason": "相似表达", "keyword": "花艺"}
    ]


def test_merge_report_benchmarks_replaces_creators_only():
    report = {"account_keywords": ["花艺"], "benchmark_creators": [{"name": "old"}]}
    benchmark_accounts = {
        "accounts": [
            {"name": "new", "platform": "小红书", "reason": "命中", "keyword": "社区花店 xhs"}
        ]
    }

    merged = account_plan_portrait.merge_report_benchmarks(report, benchmark_accounts)

    assert merged["account_keywords"] == ["花艺"]
    assert merged["benchmark_creators"] == [
        {"name": "new", "platform": "小红书", "reason": "命中", "keyword": "社区花店"}
    ]
