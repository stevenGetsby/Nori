"""Pure OperationPlanner fallback policy helpers."""
from __future__ import annotations

from typing import Any

from nori.core import ClientBrief
from nori.shared.normalization import dedupe_preserve_order
from nori.user_profiling.models import AccountPlanResult
from nori.user_profiling.models import AccountPositioning

from ..calendar_planner.policy import cadence_for_horizon, required_assets, scheduled_dates, short_brand
from nori.core import KPIPlan, OperationPlan


def account_positioning(value: AccountPlanResult | None) -> AccountPositioning:
    return AccountPositioning.from_account_plan(value)


def content_pillars(brief: ClientBrief, account_plan: AccountPlanResult | None) -> list[str]:
    report = account_plan.ip_portrait_report if account_plan else {}
    raw_pillars = report.get("content_pillars") if isinstance(report, dict) else []
    raw_pillars = raw_pillars if isinstance(raw_pillars, list) else []
    pillars = [
        str(item.get("name") or item.get("description") or "").strip()
        for item in raw_pillars
        if isinstance(item, dict) and (item.get("name") or item.get("description"))
    ]
    pillars.extend(account_plan.content_directions if account_plan else [])
    pillars.extend(brief.positioning_notes)
    pillars.extend(brief.goals)
    return dedupe([item for item in pillars if item])[:5] or ["账号定位", "产品价值", "用户场景"]


def objectives_for_plan(brief: ClientBrief, account_plan: AccountPlanResult | None) -> list[str]:
    objectives = list(brief.goals)
    if account_plan and account_plan.recommended_positioning:
        objectives.append(f"验证定位：{account_plan.recommended_positioning}")
    if account_plan:
        objectives.extend(account_plan.unique_selling_points[:2])
    return dedupe([item for item in objectives if item])[:4] or ["建立账号基础认知", "沉淀可复用内容方向"]


def risk_controls_for_brief(brief: ClientBrief) -> list[str]:
    controls = ["每条内容发布前做平台合规审核", "封面和正文保持同一主题"]
    controls.extend([f"避免：{item}" for item in brief.taboos[:3]])
    controls.extend(brief.constraints[:2])
    return dedupe(controls)[:5]


def topic_pool(brief: ClientBrief, account_plan: AccountPlanResult | None, pillars: list[str]) -> list[str]:
    topics: list[str] = []
    topics.extend(account_plan.content_directions if account_plan else [])
    topics.extend(account_plan.unique_selling_points if account_plan else [])
    topics.extend(pillars)
    topics.extend(brief.positioning_notes)
    topics.extend(brief.goals)
    brand = brief.brand_name or brief.client_name
    if brand:
        topics.append(f"{brand}账号定位")
    return dedupe([item for item in topics if item]) or ["账号定位", "用户痛点", "产品价值"]


def task_references(account_plan: AccountPlanResult | None) -> list[dict[str, Any]]:
    if account_plan is None:
        return []
    benchmark = account_plan.benchmark_accounts if isinstance(account_plan.benchmark_accounts, dict) else {}
    return [
        {"source": "account_plan_keyword", "keyword": str(keyword)}
        for keyword in benchmark.get("search_keywords", [])[:3]
    ]


def default_milestones(horizon_days: int) -> list[dict[str, Any]]:
    mid = max(1, min(horizon_days, (horizon_days + 1) // 2))
    return [
        {"day": 1, "target": "确认账号定位与本周期内容支柱"},
        {"day": mid, "target": "完成首批内容任务制作与审核"},
        {"day": horizon_days, "target": "复盘本周期内容产出并准备下一轮选题"},
    ]


def kpi_plan_from_operation(operation_plan: OperationPlan) -> KPIPlan:
    return KPIPlan(
        plan_id=f"kpi_{operation_plan.plan_id}" if operation_plan.plan_id else "kpi_plan",
        horizon_days=operation_plan.horizon_days,
        targets=dict(operation_plan.kpi_targets),
        milestones=list(operation_plan.milestones),
        measurement_notes=[
            "当前为运营计划派生 KPI，后续可由 KPIPlanner 精细化。",
            "默认只记录可人工核验指标，不触发自动数据抓取。",
        ],
        metadata={"source": "operation_plan"},
    )


def project_title(brief: ClientBrief) -> str:
    name = brief.brand_name or brief.client_name or "Nori"
    return f"{name}账号代运营"


def stable_id(prefix: str, value: str) -> str:
    cleaned = "".join(ch.lower() for ch in value if ch.isalnum())
    return f"{prefix}_{cleaned[:16] or 'local'}"


def dedupe(values: list[str]) -> list[str]:
    return dedupe_preserve_order(values)
