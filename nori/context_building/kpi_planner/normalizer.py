"""KPIPlan normalization helpers for KPIPlanner."""
from __future__ import annotations

from typing import Any

from nori.shared.normalization import mapping, milestone_rows, string_list

from ..models import KPIPlan, OperationPlan


def merge_llm_kpi_plan(data: dict[str, Any], fallback: KPIPlan, plan: OperationPlan) -> KPIPlan:
    """Merge LLM KPI JSON into a stable KPIPlan."""
    targets = mapping(data.get("targets")) or dict(fallback.targets)
    milestones = milestones_from_rows(data.get("milestones"), fallback.milestones, plan.horizon_days)
    notes = _string_list(data.get("measurement_notes"), fallback.measurement_notes, limit=5)
    return KPIPlan(
        plan_id=fallback.plan_id,
        horizon_days=fallback.horizon_days,
        targets=targets,
        milestones=milestones,
        measurement_notes=notes,
        metadata={**fallback.metadata, "planner": "llm_with_fallback"},
    )


def fallback_kpi_plan(plan: OperationPlan, context: dict[str, Any]) -> KPIPlan:
    """Build deterministic KPI fallback from an operation plan and project context."""
    targets = dict(plan.kpi_targets)
    targets.setdefault("content_tasks", content_task_target(plan, context))
    targets.setdefault("review_pass_rate", ">= 90%")
    targets.setdefault("manual_metrics_check", check_cadence(plan.horizon_days))
    if plan.horizon_days <= 7:
        targets.setdefault("cycle_review", "完成 1 次周期复盘")
    else:
        targets.setdefault("weekly_review", "每周完成 1 次复盘")

    return KPIPlan(
        plan_id=f"kpi_{plan.plan_id}" if plan.plan_id else "kpi_plan",
        horizon_days=plan.horizon_days,
        targets=targets,
        milestones=milestones_from_rows(plan.milestones, default_milestones(plan.horizon_days), plan.horizon_days),
        measurement_notes=[
            "所有指标默认人工记录或从平台后台读取。",
            "内容数量以已完成审核的 ContentTask 计数。",
            "审核通过率以 ComplianceReview status=passed 的比例计算。",
        ],
        metadata={"planner": "rule_fallback", "source_plan_id": plan.plan_id},
    )


def content_task_target(plan: OperationPlan, context: dict[str, Any]) -> int:
    explicit = context.get("content_task_count")
    if isinstance(explicit, int) and explicit > 0:
        return explicit
    if plan.horizon_days <= 7:
        return 3
    weeks = max(1, round(plan.horizon_days / 7))
    return weeks * 3


def check_cadence(horizon_days: int) -> str:
    if horizon_days <= 7:
        return "周期结束手动核验 1 次"
    return "每周手动核验 1 次"


def default_milestones(horizon_days: int) -> list[dict[str, Any]]:
    mid = max(1, min(horizon_days, (horizon_days + 1) // 2))
    return [
        {"day": 1, "target": "确认本周期 KPI 基线"},
        {"day": mid, "target": "检查内容产出和审核通过率"},
        {"day": horizon_days, "target": "完成 KPI 复盘记录"},
    ]


def milestones_from_rows(value: Any, fallback: list[dict[str, Any]], horizon_days: int) -> list[dict[str, Any]]:
    return milestone_rows(value, fallback, horizon_days=horizon_days)


def _string_list(value: Any, fallback: list[str], *, limit: int | None = None) -> list[str]:
    return string_list(value, fallback, limit=limit)
