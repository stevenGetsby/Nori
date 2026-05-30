"""Shared rule-based critic policies for planning agents."""
from __future__ import annotations

from nori.core import AccountOperationProject
from typing import Any

from nori.agents.user_profiling.models import AccountPlanResult
from nori.core import ClientBrief, ContentCalendar, KPIPlan, OperationPlan

from .calendar_planner import normalizer as _calendar_normalizer


def critic_operation_project(
    project: AccountOperationProject,
    brief: ClientBrief,
    account_plan: AccountPlanResult | None,
) -> dict[str, Any]:
    """Assess whether an operation project is structurally usable."""
    issues: list[str] = []
    checks = {
        "objectives": bool(project.operation_plan.objectives),
        "content_pillars": bool(project.operation_plan.content_pillars),
        "tasks": bool(project.content_tasks),
        "calendar": bool(project.content_calendar.tasks),
        "risk_controls": bool(project.operation_plan.risk_controls),
    }
    if not checks["objectives"]:
        issues.append("缺少运营目标")
    if not checks["content_pillars"]:
        issues.append("缺少内容支柱")
    if not checks["tasks"]:
        issues.append("缺少内容任务")
    if not checks["calendar"]:
        issues.append("缺少内容排期")
    if not checks["risk_controls"]:
        issues.append("缺少风险控制")
    if project.metadata.get("planner") == "rule_fallback":
        issues.append("当前结果仍依赖规则兜底，应优先切换为 LLM 主线")
    if account_plan and account_plan.recommended_positioning and account_plan.recommended_positioning not in project.operation_plan.objectives:
        checks["positioning_alignment"] = True
    else:
        checks["positioning_alignment"] = False if account_plan else True
    if brief.platform and project.client_brief.platform != brief.platform:
        issues.append("平台与客户简报不一致")
    return {
        "source": "rules",
        "status": "pass" if not issues else "warn",
        "issues": issues,
        "checks": checks,
    }


def critic_kpi_plan(plan: KPIPlan, operation_plan: OperationPlan) -> dict[str, Any]:
    """Assess whether a KPI plan has measurable targets and cadence."""
    issues: list[str] = []
    checks = {
        "targets": bool(plan.targets),
        "milestones": bool(plan.milestones),
        "measurement_notes": bool(plan.measurement_notes),
    }
    if not checks["targets"]:
        issues.append("缺少 KPI 目标")
    if not checks["milestones"]:
        issues.append("缺少 KPI 里程碑")
    if not checks["measurement_notes"]:
        issues.append("缺少核验说明")
    if operation_plan.horizon_days <= 7 and plan.targets.get("manual_metrics_check") == "每周手动核验 1 次":
        issues.append("7 天计划的核验频率过粗")
    if plan.metadata.get("planner") == "rule_fallback":
        issues.append("当前 KPI 仍依赖规则兜底，应优先切换为 LLM 主线")
    return {
        "source": "rules",
        "status": "pass" if not issues else "warn",
        "issues": issues,
        "checks": checks,
    }


def critic_calendar(calendar: ContentCalendar, plan: OperationPlan, kpi: KPIPlan) -> dict[str, Any]:
    """Assess whether a content calendar can enter production orchestration."""
    issues: list[str] = []
    checks = {
        "themes": bool(calendar.themes),
        "tasks": bool(calendar.tasks),
        "date_range": bool(calendar.start_date and calendar.end_date),
        "planned_status": all(task.status == "planned" for task in calendar.tasks),
        "task_briefs": all(bool(task.brief) for task in calendar.tasks),
    }
    if not checks["themes"]:
        issues.append("缺少周期主题")
    if not checks["tasks"]:
        issues.append("缺少内容任务")
    if not checks["date_range"]:
        issues.append("缺少排期日期范围")
    if not checks["planned_status"]:
        issues.append("存在非 planned 状态任务")
    if not checks["task_briefs"]:
        issues.append("存在缺少 brief 的任务")
    target_count = _calendar_normalizer.target_task_count(kpi)
    if target_count and len(calendar.tasks) < min(target_count, 7):
        issues.append("任务数量少于 KPI 计划目标")
    if plan.content_pillars and not set(calendar.themes).intersection(plan.content_pillars):
        issues.append("周期主题未覆盖运营计划内容支柱")
    if calendar.metadata.get("planner") == "rule_fallback":
        issues.append("当前排期仍依赖规则兜底，应优先切换为 LLM 主线")
    return {
        "source": "rules",
        "status": "pass" if not issues else "warn",
        "issues": issues,
        "checks": checks,
    }
