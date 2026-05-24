"""Calendar Planner: turn operation strategy and KPIs into content tasks."""
from __future__ import annotations

import json
from datetime import date, timedelta
from typing import Any

import llms
from nori.ops_models import (
    AccountOperationProject,
    ClientBrief,
    ContentCalendar,
    ContentTask,
    KPIPlan,
    OperationPlan,
)


SYSTEM_PROMPT = "你是 Nori 的账号代运营排期规划器，只输出 JSON。"

USER_PROMPT = """\
根据运营计划、KPI 计划和客户上下文，生成可交给内容生产链路的内容排期。

运营计划：
{operation_plan}

KPI 计划：
{kpi_plan}

客户上下文：
{client_context}

计划要求：
- 只规划 {horizon_days} 天，从 {start_date} 开始。
- 不要安排真实发布、自动互动、自动抓取数据等未实现能力。
- 每个任务后续要能交给 ContentTask -> NoteMakerAgent -> CoverDirectorAgent。
- 任务状态必须保持 planned。
- 输出任务数量要服务 KPI，但不要超过 7 条。

输出 JSON，字段固定：
{{
  "themes": ["本周期主题，1-4 条"],
  "cadence": "制作/排期节奏",
  "tasks": [
    {{
      "title": "任务标题",
      "day": 1,
      "content_type": "note",
      "topic": "内容主题",
      "objective": "本条内容目标",
      "priority": 1,
      "brief": {{
        "cover_title": "封面标题建议",
        "content_pillar": "对应内容支柱",
        "angle": "切入角度"
      }},
      "required_assets": ["需要的素材类型"],
      "notes": ["制作注意事项"]
    }}
  ],
  "notes": ["排期说明，可为空"]
}}
"""


class CalendarPlannerAgent:
    """Create a ContentCalendar from an operation plan and KPI plan."""

    def __init__(self, *, use_llm: bool = True) -> None:
        self.use_llm = use_llm

    def run(
        self,
        operation_plan: OperationPlan | AccountOperationProject | dict[str, Any] | None,
        *,
        kpi_plan: KPIPlan | dict[str, Any] | None = None,
        client_brief: ClientBrief | dict[str, Any] | None = None,
        start_date: str | date | None = None,
        horizon_days: int | None = None,
        use_llm: bool | None = None,
    ) -> ContentCalendar:
        plan, kpi, brief, inherited_calendar = _normalize_inputs(
            operation_plan,
            kpi_plan=kpi_plan,
            client_brief=client_brief,
        )
        days = _bounded_horizon(horizon_days or plan.horizon_days)
        start = _normalize_start_date(start_date or inherited_calendar.start_date)
        fallback = _fallback_calendar(plan, kpi, brief, start_date=start, horizon_days=days)
        should_use_llm = self.use_llm if use_llm is None else use_llm
        if not should_use_llm:
            return _with_critic(fallback, plan, kpi)
        planned = _llm_calendar(plan, kpi, brief, fallback, start_date=start, horizon_days=days)
        return _with_critic(planned or fallback, plan, kpi)


def plan_calendar(
    operation_plan: OperationPlan | AccountOperationProject | dict[str, Any] | None,
    **kwargs: Any,
) -> ContentCalendar:
    """Convenience wrapper for one-shot calendar planning."""

    return CalendarPlannerAgent().run(operation_plan, **kwargs)


def _llm_calendar(
    plan: OperationPlan,
    kpi: KPIPlan,
    brief: ClientBrief,
    fallback: ContentCalendar,
    *,
    start_date: date,
    horizon_days: int,
) -> ContentCalendar | None:
    try:
        data = llms.chat_json(
            [
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": USER_PROMPT.format(
                        operation_plan=json.dumps(plan.to_dict(), ensure_ascii=False),
                        kpi_plan=json.dumps(kpi.to_dict(), ensure_ascii=False),
                        client_context=json.dumps(brief.to_dict(), ensure_ascii=False),
                        start_date=start_date.isoformat(),
                        horizon_days=horizon_days,
                    ),
                },
            ],
            usage="llm",
            _chat=llms.chat,
        )
    except Exception:  # noqa: BLE001 - calendar planning must keep deterministic fallback.
        return None
    return _merge_llm_calendar(data, fallback, plan, brief, start_date=start_date, horizon_days=horizon_days)


def _merge_llm_calendar(
    data: dict[str, Any],
    fallback: ContentCalendar,
    plan: OperationPlan,
    brief: ClientBrief,
    *,
    start_date: date,
    horizon_days: int,
) -> ContentCalendar:
    tasks = _tasks_from_llm(
        data.get("tasks"),
        fallback.tasks,
        plan,
        brief,
        start_date=start_date,
        horizon_days=horizon_days,
    )
    return ContentCalendar(
        calendar_id=fallback.calendar_id,
        start_date=start_date.isoformat(),
        end_date=(start_date + timedelta(days=horizon_days - 1)).isoformat(),
        cadence=str(data.get("cadence") or fallback.cadence),
        themes=_string_list(data.get("themes"), fallback.themes, limit=4),
        tasks=tasks,
        notes=_string_list(data.get("notes"), fallback.notes, limit=5),
        metadata={**fallback.metadata, "planner": "llm_with_fallback"},
    )


def _fallback_calendar(
    plan: OperationPlan,
    kpi: KPIPlan,
    brief: ClientBrief,
    *,
    start_date: date,
    horizon_days: int,
) -> ContentCalendar:
    task_count = _task_count(plan, kpi, horizon_days)
    dates = _scheduled_dates(start_date, horizon_days, task_count)
    pillars = plan.content_pillars or brief.positioning_notes or brief.goals or ["账号定位", "产品价值", "用户场景"]
    objectives = plan.objectives or brief.goals or ["建立账号认知"]
    tasks: list[ContentTask] = []
    for index in range(task_count):
        pillar = pillars[index % len(pillars)]
        objective = objectives[index % len(objectives)]
        topic = _topic_for_task(pillar, objective, brief)
        scheduled_date = dates[index]
        day = (scheduled_date - start_date).days + 1
        tasks.append(
            ContentTask(
                task_id=f"task_d{day:02d}_{index + 1:02d}",
                title=f"{topic}｜{_short_brand(brief)}",
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
                required_assets=_required_assets(brief),
                notes=["生成前需做内容合规与素材可用性检查。"],
                metadata={"source": "calendar_planner_fallback"},
            )
        )
    themes = _dedupe(pillars)[:4]
    return ContentCalendar(
        calendar_id=_calendar_id(start_date, horizon_days),
        start_date=start_date.isoformat(),
        end_date=(start_date + timedelta(days=horizon_days - 1)).isoformat(),
        cadence=plan.cadence or _cadence(horizon_days),
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


def _tasks_from_llm(
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
        scheduled_date = _date_from_day(row.get("day"), start_date, horizon_days)
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
            objective=str(row.get("objective") or _objective(plan, index)),
            status="planned",
            priority=_int(row.get("priority"), default=index + 1),
            brief=_mapping(row.get("brief")),
            required_assets=_string_list(row.get("required_assets"), _required_assets(brief), limit=6),
            references=[],
            notes=_string_list(row.get("notes"), [], limit=4),
            metadata={"source": "calendar_planner_llm"},
        )
        if "content_pillar" not in task.brief and plan.content_pillars:
            task.brief["content_pillar"] = plan.content_pillars[index % len(plan.content_pillars)]
        tasks.append(task)
    return tasks or list(fallback_tasks)


def _with_critic(calendar: ContentCalendar, plan: OperationPlan, kpi: KPIPlan) -> ContentCalendar:
    metadata = dict(calendar.metadata)
    metadata["critic"] = _critic_calendar(calendar, plan, kpi)
    calendar.metadata = metadata
    return calendar


def _critic_calendar(calendar: ContentCalendar, plan: OperationPlan, kpi: KPIPlan) -> dict[str, Any]:
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
    target_count = _target_task_count(kpi)
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


def _normalize_inputs(
    value: OperationPlan | AccountOperationProject | dict[str, Any] | None,
    *,
    kpi_plan: KPIPlan | dict[str, Any] | None,
    client_brief: ClientBrief | dict[str, Any] | None,
) -> tuple[OperationPlan, KPIPlan, ClientBrief, ContentCalendar]:
    if isinstance(value, AccountOperationProject):
        return (
            value.operation_plan,
            _normalize_kpi(kpi_plan) if kpi_plan is not None else value.kpi_plan,
            _normalize_brief(client_brief) if client_brief is not None else value.client_brief,
            value.content_calendar,
        )
    if isinstance(value, OperationPlan):
        return value, _normalize_kpi(kpi_plan), _normalize_brief(client_brief), ContentCalendar()
    data = _mapping(value)
    if "operation_plan" in data and isinstance(data.get("operation_plan"), dict):
        return (
            OperationPlan.from_dict(data.get("operation_plan")),
            _normalize_kpi(kpi_plan or data.get("kpi_plan")),
            _normalize_brief(client_brief or data.get("client_brief")),
            ContentCalendar.from_dict(data.get("content_calendar")),
        )
    return OperationPlan.from_dict(data), _normalize_kpi(kpi_plan), _normalize_brief(client_brief), ContentCalendar()


def _normalize_kpi(value: KPIPlan | dict[str, Any] | None) -> KPIPlan:
    if isinstance(value, KPIPlan):
        return value
    return KPIPlan.from_dict(value if isinstance(value, dict) else {})


def _normalize_brief(value: ClientBrief | dict[str, Any] | None) -> ClientBrief:
    if isinstance(value, ClientBrief):
        return value
    return ClientBrief.from_dict(value if isinstance(value, dict) else {})


def _task_count(plan: OperationPlan, kpi: KPIPlan, horizon_days: int) -> int:
    target = _target_task_count(kpi)
    if target:
        return max(1, min(7, target))
    explicit = _int(plan.kpi_targets.get("content_tasks"), default=0)
    if explicit > 0:
        return max(1, min(7, explicit))
    if horizon_days <= 7:
        return 3
    weeks = max(1, round(horizon_days / 7))
    return max(1, min(7, weeks * 3))


def _target_task_count(kpi: KPIPlan) -> int:
    return _int(kpi.targets.get("content_tasks"), default=0)


def _scheduled_dates(start: date, horizon_days: int, count: int) -> list[date]:
    if count <= 1:
        return [start]
    last_offset = max(0, horizon_days - 1)
    return [start + timedelta(days=round(index * last_offset / (count - 1))) for index in range(count)]


def _date_from_day(value: Any, start: date, horizon_days: int) -> date:
    day = _int(value, default=1)
    day = min(max(day, 1), max(1, horizon_days))
    return start + timedelta(days=day - 1)


def _normalize_start_date(value: str | date | None) -> date:
    if isinstance(value, date):
        return value
    if isinstance(value, str) and value:
        try:
            return date.fromisoformat(value)
        except ValueError:
            pass
    return date.today()


def _bounded_horizon(value: int | None) -> int:
    return min(max(_int(value, default=7), 1), 90)


def _calendar_id(start_date: date, horizon_days: int) -> str:
    return f"cal_{start_date.isoformat()}_{horizon_days}d"


def _cadence(horizon_days: int) -> str:
    if horizon_days <= 7:
        return "7 天内规划 3 条内容任务"
    if horizon_days <= 30:
        return "每周 3 条内容任务"
    return "每周 3-5 条内容任务"


def _topic_for_task(pillar: str, objective: str, brief: ClientBrief) -> str:
    brand = brief.brand_name or brief.client_name
    if brand and pillar not in brand:
        return f"{brand}{pillar}"
    if objective:
        return objective[:24]
    return pillar or "账号内容"


def _objective(plan: OperationPlan, index: int) -> str:
    if plan.objectives:
        return plan.objectives[index % len(plan.objectives)]
    return "完成本周期内容目标"


def _short_brand(brief: ClientBrief) -> str:
    return brief.brand_name or brief.client_name or "账号"


def _required_assets(brief: ClientBrief) -> list[str]:
    if not brief.source_materials:
        return ["品牌基础信息", "可用图片素材"]
    assets = [
        str(item.get("type") or item.get("kind") or item.get("usage") or "素材")
        for item in brief.source_materials
        if isinstance(item, dict)
    ]
    return _dedupe(assets) or ["品牌基础信息", "可用图片素材"]


def _mapping(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, dict) else {}


def _string_list(value: Any, fallback: list[str], *, limit: int | None = None) -> list[str]:
    if isinstance(value, str):
        items = [value]
    elif isinstance(value, list):
        items = [str(item) for item in value if item is not None]
    else:
        items = list(fallback)
    items = [item.strip() for item in items if item.strip()]
    if limit is not None:
        return items[:limit]
    return items


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        output.append(value)
    return output


def _int(value: Any, *, default: int) -> int:
    if isinstance(value, bool):
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


__all__ = ["CalendarPlannerAgent", "plan_calendar"]
