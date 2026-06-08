"""Deterministic project builder for OperationPlanner fallback."""
from __future__ import annotations

from nori.core import AccountOperationProject
from datetime import date, timedelta

from nori.agents.user_profiling.schemas import AccountPlanResult
from nori.core import ClientBrief

from nori.core import ContentCalendar, ContentTask, OperationPlan
from .project_policy import (
    account_positioning,
    cadence_for_horizon,
    content_pillars,
    default_milestones,
    kpi_plan_from_operation,
    objectives_for_plan,
    project_title,
    required_assets,
    risk_controls_for_brief,
    scheduled_dates,
    short_brand,
    stable_id,
    task_references,
    topic_pool,
)


def fallback_project(
    brief: ClientBrief,
    account_plan: AccountPlanResult | None,
    *,
    project_id: str,
    project_name: str,
    start_date: date,
    horizon_days: int,
) -> AccountOperationProject:
    """Build a deterministic account-operations project without live LLM calls."""
    plan_id = f"plan_{horizon_days}d"
    calendar_id = f"cal_{start_date.isoformat()}_{horizon_days}d"
    project = project_id or stable_id("ops", brief.brand_name or brief.client_name or "local")
    name = project_name or project_title(brief)
    pillars = content_pillars(brief, account_plan)
    objectives = objectives_for_plan(brief, account_plan)
    risk_controls = risk_controls_for_brief(brief)
    cadence = cadence_for_horizon(horizon_days)
    tasks = fallback_tasks(
        brief,
        account_plan,
        pillars=pillars,
        objectives=objectives,
        start_date=start_date,
        horizon_days=horizon_days,
    )
    operation_plan = OperationPlan(
        plan_id=plan_id,
        horizon_days=horizon_days,
        objectives=objectives,
        content_pillars=pillars,
        cadence=cadence,
        kpi_targets={"content_tasks": len(tasks), "review_pass_rate": ">= 90%"},
        milestones=default_milestones(horizon_days),
        risk_controls=risk_controls,
        notes=["规则 fallback 生成，后续可由 LLM 或人工补强。"],
    )
    calendar = ContentCalendar(
        calendar_id=calendar_id,
        start_date=start_date.isoformat(),
        end_date=(start_date + timedelta(days=horizon_days - 1)).isoformat(),
        cadence=cadence,
        themes=pillars[:3],
        tasks=tasks,
        notes=["所有任务默认停留在 planned，不触发真实发布。"],
        metadata={"horizon_days": horizon_days},
    )
    return AccountOperationProject(
        project_id=project,
        name=name,
        status="planning",
        client_brief=brief,
        account_positioning=account_positioning(account_plan),
        operation_plan=operation_plan,
        kpi_plan=kpi_plan_from_operation(operation_plan),
        content_calendar=calendar,
        content_tasks=list(tasks),
        artifacts={},
        metadata={"planner": "rule_fallback"},
    )


def fallback_tasks(
    brief: ClientBrief,
    account_plan: AccountPlanResult | None,
    *,
    pillars: list[str],
    objectives: list[str],
    start_date: date,
    horizon_days: int,
) -> list[ContentTask]:
    task_count = min(3, max(1, horizon_days // 2))
    topics = topic_pool(brief, account_plan, pillars)
    dates = scheduled_dates(start_date, horizon_days, task_count)
    tasks: list[ContentTask] = []
    for index in range(task_count):
        topic = topics[index % len(topics)]
        objective = objectives[index % len(objectives)] if objectives else "建立账号认知"
        task_id = f"task_d{(dates[index] - start_date).days + 1:02d}_{index + 1:02d}"
        title = f"{topic}｜{short_brand(brief)}"
        tasks.append(
            ContentTask(
                task_id=task_id,
                title=title,
                scheduled_date=dates[index].isoformat(),
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
                    "content_pillar": pillars[index % len(pillars)] if pillars else "",
                },
                required_assets=required_assets(brief),
                references=task_references(account_plan),
                notes=["生成前需做内容合规与素材可用性检查。"],
                metadata={"source": "operation_planner_fallback"},
            )
        )
    return tasks
