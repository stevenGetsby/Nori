"""Keyword normalization helpers for AccountPlanner results."""
from __future__ import annotations

import re
from typing import Any

from nori.shared.normalization import dedupe_preserve_order


KEYWORD_ROLES = {1: "赛道", 2: "主题", 3: "内容点"}
KEYWORD_REASON_FALLBACKS = {
    1: "用于覆盖本次内容创作所在赛道。",
    2: "用于聚焦本次内容创作主题。",
    3: "用于贴近本次内容创作的具体内容点。",
}
PLATFORM_KEYWORD_TOKENS = ("小红书", "xhs", "xiaohongshu", "抖音", "douyin", "dy", "视频号", "B站", "bilibili")


def clean_keyword(value: Any) -> str:
    keyword = str(value or "").strip()
    for token in PLATFORM_KEYWORD_TOKENS:
        keyword = re.sub(re.escape(token), "", keyword, flags=re.I)
    keyword = re.sub(r"\s+", "", keyword)
    return keyword.strip("：:，,、；;|/\\")


def normalize_keyword_levels(
    value: Any,
    *,
    fallback: list[dict[str, Any]],
    search_keywords: list[str],
) -> list[dict[str, Any]]:
    sources = keyword_sources(value, search_keywords, fallback)
    levels: list[dict[str, Any]] = []
    used_keywords: set[str] = set()
    used_reasons: set[str] = set()
    for index, source in enumerate(sources[:3], start=1):
        level = level_number(source.get("level"), index)
        keyword = clean_keyword(source.get("keyword") or "")
        if not keyword or keyword in used_keywords:
            continue
        reason = text(source.get("reason"), KEYWORD_REASON_FALLBACKS.get(level, "用于本次账号规划搜索。"))
        if reason in used_reasons:
            reason = KEYWORD_REASON_FALLBACKS.get(level, "用于本次账号规划搜索。")
        used_keywords.add(keyword)
        used_reasons.add(reason)
        levels.append(
            {
                "level": level,
                "role": str(source.get("role") or KEYWORD_ROLES.get(level, "")),
                "keyword": keyword,
                "reason": reason,
            }
        )
    return sorted(levels, key=lambda item: int(item.get("level") or 0))


def keyword_sources(value: Any, search_keywords: list[str], fallback: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if isinstance(value, list):
        sources = [item for item in value if isinstance(item, dict)]
        if sources:
            return sources
    if search_keywords:
        return [{"level": index, "keyword": keyword} for index, keyword in enumerate(search_keywords[:3], start=1)]
    return [item for item in fallback[:3] if isinstance(item, dict)]


def level_number(value: Any, fallback: int) -> int:
    try:
        level = int(value)
    except (TypeError, ValueError):
        level = fallback
    return level if level in KEYWORD_ROLES else fallback


def keywords_from_levels(keyword_levels: list[dict[str, Any]]) -> list[str]:
    return dedupe([
        clean_keyword(item.get("keyword") or "")
        for item in keyword_levels
        if isinstance(item, dict) and clean_keyword(item.get("keyword") or "")
    ])


def dedupe(items: list[str]) -> list[str]:
    return dedupe_preserve_order(items)


def text(value: Any, fallback: str) -> str:
    cleaned = str(value or "").strip()
    return cleaned or fallback
