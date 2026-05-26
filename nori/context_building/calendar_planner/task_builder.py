"""ContentTask construction helpers for CalendarPlanner."""
from __future__ import annotations

from datetime import date
from typing import Any

from nori.core import ClientBrief
from nori.shared.normalization import int_value, mapping, string_list

from nori.core import ContentTask, KPIPlan, OperationPlan

from .policy import (
    date_from_day,
    objective_for_index,
    required_assets,
    scheduled_dates,
    short_brand,
    task_count_from_targets,
    topic_for_task,
)


def fallback_tasks(
    plan: OperationPlan,
    kpi: KPIPlan,
    brief: ClientBrief,
    *,
    start_date: date,
    horizon_days: int,
) -> list[ContentTask]:
    task_count = task_count_from_targets(plan, kpi, horizon_days)
    dates = scheduled_dates(start_date, horizon_days, task_count)
    pillars = plan.content_pillars or brief.positioning_notes or brief.goals or ["账号定位", "产品价值", "用户场景"]
    objectives = plan.objectives or brief.goals or ["建立账号认知"]
    tasks: list[ContentTask] = []
    for index in range(task_count):
        pillar = pillars[index % len(pillars)]
        objective = objectives[index % len(objectives)]
        topic = topic_for_task(pillar, objective, brief)
        scheduled_date = dates[index]
        day = (scheduled_date - start_date).days + 1
        tasks.append(
            ContentTask(
                task_id=f"task_d{day:02d}_{index + 1:02d}",
                title=f"{topic}｜{short_brand(brief)}",
                scheduled_date=scheduled_date.isoformat(),
                platform=brief.platform or "xhs",
                content_type="note",
                topic=topic,
                objective=objective,
                status="planned",
                priority=index + 1,
                brief={
                    "brand_name": brief.brand_name,
                    "audience": list(brief.audience),
                    "cover_title": topic[:18],
                    "content_pillar": pillar,
                },
                required_assets=required_assets(brief),
                notes=["生成前需做内容合规与素材可用性检查。"],
                metadata={"source": "calendar_planner_fallback"},
            )
        )
    return tasks


def tasks_from_llm(
    value: Any,
    fallback_tasks: list[ContentTask],
    plan: OperationPlan,
    brief: ClientBrief,
    *,
    start_date: date,
    horizon_days: int,
) -> list[ContentTask]:
    rows = value if isinstance(value, list) else []
    tasks: list[ContentTask] = []
    max_tasks = max(1, min(7, horizon_days))
    for index, row in enumerate(rows[:max_tasks]):
        if not isinstance(row, dict):
            continue
        scheduled_date = date_from_day(row.get("day"), start_date, horizon_days)
        title = str(row.get("title") or row.get("topic") or "").strip()
        topic = str(row.get("topic") or title or "").strip()
        if not title and not topic:
            continue
        day = (scheduled_date - start_date).days + 1
        task = ContentTask(
            task_id=f"task_d{day:02d}_{index + 1:02d}",
            title=title or topic,
            scheduled_date=scheduled_date.isoformat(),
            platform=brief.platform or "xhs",
            content_type=str(row.get("content_type") or "note"),
            topic=topic or title,
            objective=str(row.get("objective") or objective_for_index(plan, index)),
            status="planned",
            priority=int_value(row.get("priority"), default=index + 1),
            brief=mapping(row.get("brief")),
            required_assets=string_list(row.get("required_assets"), required_assets(brief), limit=6),
            references=[],
            notes=string_list(row.get("notes"), [], limit=4),
            metadata={"source": "calendar_planner_llm"},
        )
        if "content_pillar" not in task.brief and plan.content_pillars:
            task.brief["content_pillar"] = plan.content_pillars[index % len(plan.content_pillars)]
        tasks.append(task)
    return tasks or list(fallback_tasks)


__all__ = ["fallback_tasks", "int_value", "mapping", "string_list", "tasks_from_llm"]
