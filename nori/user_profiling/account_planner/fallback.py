"""AccountPlanner deterministic fallback result builder."""
from __future__ import annotations

from nori.user_profiling.models import AccountPlanResult, AccountPlannerInput

from . import normalizer as _plan_normalizer


def fallback_plan(normalized: AccountPlannerInput) -> AccountPlanResult:
    platform = _plan_normalizer.platform_label(normalized.platform)
    goal = _plan_normalizer.short_text(normalized.intention.get("goal"), "待判断")
    tags = {
        "track": "待判断",
        "goal": goal,
        "platform": platform,
        "product": "待判断",
        "positioning": "待判断",
    }
    benchmark_accounts = {"keyword_levels": [], "search_keywords": [], "accounts": [], "search_results": []}
    return AccountPlanResult(
        tags=tags,
        recommended_positioning="需要 LLM 根据 Intention + Context 推理账号定位。",
        audience_profile=[],
        content_directions=[],
        benchmark_accounts=benchmark_accounts,
        unique_selling_points=[],
        ip_portrait_report={
            "account_name_suggestions": [],
            "account_keywords": [],
            "content_pillars": [],
            "benchmark_creators": [],
            "cover_design_formats": [],
        },
    )
