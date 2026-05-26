"""AccountPlanner IP portrait and benchmark cleanup helpers."""
from __future__ import annotations

from typing import Any

from nori.shared.normalization import dedupe_preserve_order, string_list as _shared_string_list

from . import keywords as _keywords


def normalize_ip_portrait_report(
    value: Any,
    fallback: dict[str, Any],
    benchmark_accounts: dict[str, Any],
) -> dict[str, Any]:
    data = value if isinstance(value, dict) else {}
    benchmark_creators = creator_list(data.get("benchmark_creators"), fallback.get("benchmark_creators", []))
    if not benchmark_creators:
        benchmark_creators = report_benchmark_creators(benchmark_accounts)
    return {
        "account_name_suggestions": string_list(
            data.get("account_name_suggestions"),
            fallback.get("account_name_suggestions", []),
            limit=5,
        ),
        "account_keywords": string_list(data.get("account_keywords"), fallback.get("account_keywords", []), limit=5),
        "content_pillars": content_pillar_list(data.get("content_pillars"), fallback.get("content_pillars", [])),
        "benchmark_creators": benchmark_creators[:5],
        "cover_design_formats": cover_format_list(
            data.get("cover_design_formats"),
            fallback.get("cover_design_formats", []),
        ),
    }


def merge_report_benchmarks(report: dict[str, Any], benchmark_accounts: dict[str, Any]) -> dict[str, Any]:
    merged = dict(report)
    merged["benchmark_creators"] = report_benchmark_creators(benchmark_accounts)
    return merged


def report_benchmark_creators(benchmark_accounts: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "name": str(item.get("name") or "").strip(),
            "platform": str(item.get("platform") or "").strip(),
            "reason": str(item.get("reason") or "").strip(),
            "keyword": _keywords.clean_keyword(item.get("keyword") or ""),
        }
        for item in benchmark_accounts.get("accounts", [])[:5]
        if isinstance(item, dict)
    ]


def content_pillar_list(value: Any, fallback: list[dict[str, Any]]) -> list[dict[str, str]]:
    items = dict_list(value, keys=("name", "description"), fallback=fallback)
    return [
        {"name": item.get("name") or item.get("description", "")[:12], "description": item.get("description") or item.get("name", "")}
        for item in items
        if item.get("name") or item.get("description")
    ][:5]


def creator_list(value: Any, fallback: list[dict[str, Any]]) -> list[dict[str, str]]:
    items = dict_list(value, keys=("name", "platform", "reason", "keyword"), fallback=fallback)
    return [
        {
            "name": item.get("name", ""),
            "platform": item.get("platform", ""),
            "reason": item.get("reason", ""),
            "keyword": _keywords.clean_keyword(item.get("keyword") or ""),
        }
        for item in items
    ][:5]


def cover_format_list(value: Any, fallback: list[dict[str, Any]]) -> list[dict[str, str]]:
    items = dict_list(value, keys=("name", "ratio", "layout", "reason"), fallback=fallback)
    return [
        {
            "name": item.get("name", ""),
            "ratio": item.get("ratio") or "3:4",
            "layout": item.get("layout", ""),
            "reason": item.get("reason", ""),
        }
        for item in items
    ][:5]


def account_list(value: Any, fallback: list[dict[str, Any]]) -> list[dict[str, str]]:
    items = dict_list(value, keys=("name", "platform", "reason", "keyword"), fallback=fallback)
    return [
        {
            "name": item.get("name", ""),
            "platform": item.get("platform", ""),
            "reason": item.get("reason", ""),
            "keyword": _keywords.clean_keyword(item.get("keyword") or ""),
        }
        for item in items
    ][:5]


def dict_list(value: Any, *, keys: tuple[str, ...], fallback: list[dict[str, Any]]) -> list[dict[str, str]]:
    rows = value if isinstance(value, list) else fallback
    items: list[dict[str, str]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        item = {key: str(row.get(key) or "").strip() for key in keys}
        if any(item.values()):
            items.append(item)
    return items


def string_list(value: Any, fallback: list[str], *, limit: int) -> list[str]:
    return dedupe(_shared_string_list(value, fallback))[:limit]


def dedupe(items: list[str]) -> list[str]:
    return dedupe_preserve_order(items)
