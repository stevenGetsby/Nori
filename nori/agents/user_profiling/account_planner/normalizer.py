"""AccountPlanner result normalization helpers."""
from __future__ import annotations

from typing import Any

from nori.shared.normalization import dedupe_preserve_order, string_list
from nori.agents.user_profiling.models import AccountPlanResult

from . import keywords as _keywords
from . import portrait as _portrait


TAG_KEYS = ("track", "goal", "platform", "product", "positioning")


def normalize_llm_result(
    data: dict[str, Any],
    fallback: AccountPlanResult,
    search_results: list[dict[str, Any]],
) -> AccountPlanResult:
    """Normalize AccountPlanner JSON into a stable AccountPlanResult."""
    tags_data = data.get("tags") if isinstance(data.get("tags"), dict) else {}
    tags = {key: short_text(tags_data.get(key), fallback.tags.get(key, "")) for key in TAG_KEYS}
    benchmark_data = data.get("benchmark_accounts") if isinstance(data.get("benchmark_accounts"), dict) else {}
    search_keyword_sources = _string_list(
        benchmark_data.get("search_keywords"),
        fallback.benchmark_accounts.get("search_keywords", []),
        limit=3,
    )
    keyword_levels = _keywords.normalize_keyword_levels(
        benchmark_data.get("keyword_levels"),
        fallback=fallback.benchmark_accounts.get("keyword_levels", []),
        search_keywords=search_keyword_sources,
    )
    benchmark_accounts = {
        "keyword_levels": keyword_levels,
        "search_keywords": _keywords.keywords_from_levels(keyword_levels),
        "accounts": _portrait.account_list(
            benchmark_data.get("accounts"),
            fallback.benchmark_accounts.get("accounts", []),
        ),
        "search_results": list(search_results or benchmark_data.get("search_results") or []),
    }
    ip_portrait_report = _portrait.normalize_ip_portrait_report(
        data.get("ip_portrait_report"),
        fallback.ip_portrait_report,
        benchmark_accounts,
    )
    return AccountPlanResult(
        tags=tags,
        recommended_positioning=_text(data.get("recommended_positioning"), fallback.recommended_positioning),
        audience_profile=_string_list(data.get("audience_profile"), fallback.audience_profile, limit=5),
        content_directions=_string_list(data.get("content_directions"), fallback.content_directions, limit=5),
        benchmark_accounts=benchmark_accounts,
        unique_selling_points=_string_list(data.get("unique_selling_points"), fallback.unique_selling_points, limit=5),
        ip_portrait_report=ip_portrait_report,
        metadata=dict(fallback.metadata),
    )


def merge_search_results(result: AccountPlanResult, search_results: list[dict[str, Any]]) -> AccountPlanResult:
    """Attach search results to an existing plan without an LLM refinement pass."""
    benchmark_accounts = dict(result.benchmark_accounts)
    benchmark_accounts["search_results"] = search_results
    if search_results:
        benchmark_accounts["accounts"] = [
            {
                "name": str(item.get("author") or item.get("nickname") or item.get("title") or "搜索结果"),
                "platform": str(item.get("platform") or "xhs"),
                "reason": str(item.get("summary") or item.get("desc") or item.get("title") or "搜索命中结果。"),
                "keyword": _keywords.clean_keyword(item.get("keyword") or ""),
            }
            for item in search_results[:5]
        ]
    return AccountPlanResult(
        tags=result.tags,
        recommended_positioning=result.recommended_positioning,
        audience_profile=result.audience_profile,
        content_directions=result.content_directions,
        benchmark_accounts=benchmark_accounts,
        unique_selling_points=result.unique_selling_points,
        ip_portrait_report=_portrait.merge_report_benchmarks(result.ip_portrait_report, benchmark_accounts),
        metadata=dict(result.metadata),
    )


def platform_label(platform: str) -> str:
    value = str(platform or "xhs").lower()
    if value in {"xhs", "xiaohongshu", "小红书"}:
        return "小红书"
    if value in {"dy", "douyin", "抖音"}:
        return "抖音"
    if value in {"bili", "bilibili", "b站"}:
        return "B站"
    if value in {"wechat", "视频号"}:
        return "视频号"
    return str(platform or "xhs")


def platform_id(platform: str) -> str:
    if platform in {"小红书", "xhs", "xiaohongshu"}:
        return "xhs"
    if platform in {"抖音", "dy", "douyin"}:
        return "dy"
    if platform in {"B站", "bili", "bilibili"}:
        return "bili"
    if platform in {"视频号", "wechat"}:
        return "wechat"
    return platform or "xhs"


def short_text(value: Any, fallback: str) -> str:
    text = _text(value, fallback)
    return text[:20]


def clean_keyword(value: Any) -> str:
    return _keywords.clean_keyword(value)


def dedupe(items: list[str]) -> list[str]:
    return dedupe_preserve_order(items)


def _text(value: Any, fallback: str) -> str:
    text = str(value or "").strip()
    return text or fallback


def _string_list(value: Any, fallback: list[str], *, limit: int) -> list[str]:
    return dedupe(string_list(value, fallback))[:limit]
