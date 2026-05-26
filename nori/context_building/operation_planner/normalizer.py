"""LLM output normalization helpers for OperationPlanner."""
from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from nori.core import AccountOperationProject
from nori.shared.normalization import int_value, mapping, milestone_rows, string_list
from nori.user_profiling.models import AccountPositioning

from ..models import ContentCalendar, ContentTask, KPIPlan, OperationPlan


def merge_llm_project(
    data: dict[str, Any],
    fallback: AccountOperationProject,
    *,
    start_date: date,
    horizon_days: int,
) -> AccountOperationProject:
    """Merge LLM operation/calendar JSON with a fallback project shell."""
    plan_data = mapping(data.get("operation_plan"))
    calendar_data = mapping(data.get("content_calendar"))
    fallback_plan = fallback.operation_plan
    operation_plan = OperationPlan(
        plan_id=fallback_plan.plan_id,
        horizon_days=horizon_days,
        objectives=string_list(plan_data.get("objectives"), fallback_plan.objectives, limit=4),
        content_pillars=string_list(plan_data.get("content_pillars"), fallback_plan.content_pillars, limit=5),
        cadence=str(plan_data.get("cadence") or fallback_plan.cadence),
        kpi_targets=mapping(plan_data.get("kpi_targets")) or dict(fallback_plan.kpi_targets),
        milestones=milestone_rows(plan_data.get("milestones"), fallback_plan.milestones, horizon_days=horizon_days),
        risk_controls=string_list(plan_data.get("risk_controls"), fallback_plan.risk_controls, limit=4),
        notes=string_list(plan_data.get("notes"), fallback_plan.notes, limit=5),
    )
    themes = string_list(calendar_data.get("themes"), fallback.content_calendar.themes, limit=4)
    tasks = tasks_from_llm(
        calendar_data.get("tasks"),
        fallback.content_tasks,
        start_date=start_date,
        horizon_days=horizon_days,
        platform=fallback.client_brief.platform,
    )
    content_calendar = ContentCalendar(
        calendar_id=fallback.content_calendar.calendar_id,
        start_date=fallback.content_calendar.start_date,
        end_date=fallback.content_calendar.end_date,
        cadence=operation_plan.cadence,
        themes=themes,
        tasks=tasks,
        notes=string_list(calendar_data.get("notes"), fallback.content_calendar.notes, limit=5),
        metadata=dict(fallback.content_calendar.metadata),
    )
    return AccountOperationProject(
        project_id=fallback.project_id,
        name=fallback.name,
        status="planning",
        client_brief=fallback.client_brief,
        account_positioning=AccountPositioning.from_dict(dict(fallback.account_positioning)),
        operation_plan=operation_plan,
        kpi_plan=kpi_plan(operation_plan),
        content_calendar=content_calendar,
        content_tasks=list(tasks),
        artifacts=dict(fallback.artifacts),
        metadata={**fallback.metadata, "planner": "llm_with_fallback"},
    )


def tasks_from_llm(
    value: Any,
    fallback_tasks: list[ContentTask],
    *,
    start_date: date,
    horizon_days: int,
    platform: str,
) -> list[ContentTask]:
    """Normalize LLM calendar task rows into ContentTask records."""
    rows = value if isinstance(value, list) else []
    tasks: list[ContentTask] = []
    for index, row in enumerate(rows[: max(1, min(7, horizon_days))]):
        if not isinstance(row, dict):
            continue
        scheduled_date = date_from_day(row.get("day"), start_date, horizon_days)
        title = str(row.get("title") or row.get("topic") or "").strip()
        topic = str(row.get("topic") or title or "").strip()
        if not title and not topic:
            continue
        task = ContentTask(
            task_id=f"task_d{(scheduled_date - start_date).days + 1:02d}_{index + 1:02d}",
            title=title or topic,
            scheduled_date=scheduled_date.isoformat(),
            platform=platform or "xhs",
            content_type=str(row.get("content_type") or "note"),
            topic=topic or title,
            objective=str(row.get("objective") or "完成本周期内容目标"),
            status="planned",
            priority=int_value(row.get("priority"), default=index + 1),
            brief=mapping(row.get("brief")),
            required_assets=string_list(row.get("required_assets"), [], limit=6),
            references=[],
            notes=string_list(row.get("notes"), [], limit=4),
            metadata={"source": "operation_planner_llm"},
        )
        tasks.append(task)
    return tasks or list(fallback_tasks)


def kpi_plan(operation_plan: OperationPlan) -> KPIPlan:
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


def date_from_day(value: Any, start: date, horizon_days: int) -> date:
    day = int_value(value, default=1)
    day = min(max(day, 1), horizon_days)
    return start + timedelta(days=day - 1)
