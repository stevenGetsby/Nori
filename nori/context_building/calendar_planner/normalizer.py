"""ContentCalendar normalization helpers for CalendarPlanner."""
from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from nori.core import ClientBrief

from . import task_builder as _task_builder
from .policy import (
    bounded_horizon,
    cadence_for_horizon,
    calendar_id,
    dedupe,
    normalize_start_date,
    target_task_count,
)
from ..models import ContentCalendar, ContentTask, KPIPlan, OperationPlan


def merge_llm_calendar(
    data: dict[str, Any],
    fallback: ContentCalendar,
    plan: OperationPlan,
    brief: ClientBrief,
    *,
    start_date: date,
    horizon_days: int,
) -> ContentCalendar:
    """Merge LLM calendar JSON into a stable ContentCalendar."""
    tasks = tasks_from_llm(
        data.get("tasks"),
        fallback.tasks,
        plan,
        brief,
        start_date=start_date,
        horizon_days=horizon_days,
    )
    themes = _task_builder.string_list(data.get("themes"), fallback.themes, limit=4)
    return ContentCalendar(
        calendar_id=fallback.calendar_id,
        start_date=start_date.isoformat(),
        end_date=(start_date + timedelta(days=horizon_days - 1)).isoformat(),
        cadence=str(data.get("cadence") or fallback.cadence),
        themes=themes,
        tasks=tasks,
        notes=_task_builder.string_list(data.get("notes"), fallback.notes, limit=5),
        metadata={**fallback.metadata, "planner": "llm_with_fallback", "theme_count": len(themes)},
    )


def fallback_calendar(
    plan: OperationPlan,
    kpi: KPIPlan,
    brief: ClientBrief,
    *,
    start_date: date,
    horizon_days: int,
) -> ContentCalendar:
    """Build deterministic calendar fallback from operation, KPI, and brief context."""
    pillars = plan.content_pillars or brief.positioning_notes or brief.goals or ["账号定位", "产品价值", "用户场景"]
    tasks = _task_builder.fallback_tasks(
        plan,
        kpi,
        brief,
        start_date=start_date,
        horizon_days=horizon_days,
    )
    themes = dedupe(pillars)[:4]
    return ContentCalendar(
        calendar_id=calendar_id(start_date, horizon_days),
        start_date=start_date.isoformat(),
        end_date=(start_date + timedelta(days=horizon_days - 1)).isoformat(),
        cadence=plan.cadence or cadence_for_horizon(horizon_days),
        themes=themes,
        tasks=tasks,
        notes=[
            "规则 fallback 仅用于兜底排期；正式排期应优先由 LLM 生成。",
            "所有任务默认停留在 planned，不触发真实发布。",
        ],
        metadata={
            "planner": "rule_fallback",
            "source_plan_id": plan.plan_id,
            "source_kpi_plan_id": kpi.plan_id,
            "horizon_days": horizon_days,
            "theme_count": len(themes),
        },
    )


def tasks_from_llm(
    value: Any,
    fallback_tasks: list[ContentTask],
    plan: OperationPlan,
    brief: ClientBrief,
    *,
    start_date: date,
    horizon_days: int,
) -> list[ContentTask]:
    return _task_builder.tasks_from_llm(
        value,
        fallback_tasks,
        plan,
        brief,
        start_date=start_date,
        horizon_days=horizon_days,
    )
