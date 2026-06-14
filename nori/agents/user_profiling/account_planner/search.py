"""Search execution helpers for AccountPlanner."""
from __future__ import annotations

from typing import Any, Protocol

from nori.agents.user_profiling.schemas import AccountPlanResult, AccountPlannerInput

from . import normalizer as _plan_normalizer


class SearchProvider(Protocol):
    def search(self, *, platform: str, keyword: str, limit: int) -> list[dict[str, Any]]:
        """Search social platform content by keyword."""


class EmptySearchProvider:
    def search(self, *, platform: str, keyword: str, limit: int) -> list[dict[str, Any]]:  # noqa: ARG002
        return []


def run_search(
    search_provider: SearchProvider,
    normalized: AccountPlannerInput,
    result: AccountPlanResult,
) -> list[dict[str, Any]]:
    platform = _plan_normalizer.platform_id(result.tags.get("platform") or normalized.platform)
    keywords = result.benchmark_accounts.get("search_keywords") or []
    output: list[dict[str, Any]] = []
    for keyword in search_keywords(keywords)[:3]:
        try:
            rows = search_provider.search(platform=platform, keyword=keyword, limit=normalized.search_limit)
        except Exception:  # noqa: BLE001
            rows = []
        for row in rows[: normalized.search_limit]:
            item = dict(row)
            item.setdefault("platform", platform)
            item.setdefault("keyword", keyword)
            output.append(item)
    return output


def search_keywords(values: list[Any]) -> list[str]:
    return _plan_normalizer.dedupe([
        keyword
        for keyword in (_plan_normalizer.clean_keyword(value) for value in values)
        if keyword
    ])
