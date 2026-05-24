"""Operation planner for account-operations SOP projects."""
from __future__ import annotations

import json
from datetime import date, timedelta
from typing import Any

import llms
from nori.agent_models import AccountPlanResult
from nori.ops_models import (
    AccountOperationProject,
    ClientBrief,
    ContentCalendar,
    ContentTask,
    KPIPlan,
    OperationPlan,
)


SYSTEM_PROMPT = "你是 Nori 的账号代运营 SOP 运营计划助手。只输出 JSON。"

USER_PROMPT = """\
根据客户简报和账号定位结果，生成一个可执行的账号代运营计划。

客户简报：
{client_brief}

账号定位结果：
{account_plan}

计划要求：
- 只规划 {horizon_days} 天。
- 默认平台是客户简报中的 platform。
- 不要设计真实发布、自动互动、自动抓取数据等未实现能力。
- 内容任务要能后续交给 ContentTask -> NoteMakerAgent -> CoverDirectorAgent。

输出 JSON，字段固定：
{{
  "operation_plan": {{
    "objectives": ["运营目标，2-4 条"],
    "content_pillars": ["内容支柱，2-5 条"],
    "cadence": "发布/制作节奏",
    "kpi_targets": {{"metric": "target"}},
    "milestones": [
      {{"day": 1, "target": "阶段目标"}}
    ],
    "risk_controls": ["风险控制，2-4 条"],
    "notes": ["补充说明，可为空"]
  }},
  "content_calendar": {{
    "themes": ["本周期主题，1-4 条"],
    "tasks": [
      {{
        "title": "任务标题",
        "day": 1,
        "content_type": "note",
        "topic": "内容主题",
        "objective": "本条内容目标",
        "priority": 1,
        "brief": {{"cover_title": "封面标题建议"}},
        "required_assets": ["需要的素材类型"],
        "notes": ["制作注意事项"]
      }}
    ],
    "notes": ["排期说明，可为空"]
  }}
}}
"""


class OperationPlannerAgent:
    """Turn account positioning into a bounded operation project."""

    def __init__(self, *, use_llm: bool = True) -> None:
        self.use_llm = use_llm

    def run(
        self,
        client_brief: ClientBrief | dict[str, Any] | None,
        account_plan: AccountPlanResult | dict[str, Any] | None = None,
        *,
        project_id: str = "",
        project_name: str = "",
        start_date: str | date | None = None,
        horizon_days: int = 7,
        use_llm: bool | None = None,
    ) -> AccountOperationProject:
        brief = _normalize_client_brief(client_brief)
        normalized_plan = _normalize_account_plan(account_plan)
        days = _bounded_horizon(horizon_days)
        start = _normalize_start_date(start_date)
        fallback = _fallback_project(
            brief,
            normalized_plan,
            project_id=project_id,
            project_name=project_name,
            start_date=start,
            horizon_days=days,
        )

        should_use_llm = self.use_llm if use_llm is None else use_llm
        if not should_use_llm:
            return _with_critic(fallback, brief, normalized_plan)

        planned = _llm_project(
            brief,
            normalized_plan,
            fallback,
            start_date=start,
            horizon_days=days,
        )
        return _with_critic(planned or fallback, brief, normalized_plan)


def plan_operation(
    client_brief: ClientBrief | dict[str, Any] | None,
    account_plan: AccountPlanResult | dict[str, Any] | None = None,
    **kwargs: Any,
) -> AccountOperationProject:
    """Convenience wrapper for one-shot operation planning."""

    return OperationPlannerAgent().run(client_brief, account_plan, **kwargs)


def _llm_project(
    brief: ClientBrief,
    account_plan: AccountPlanResult | None,
    fallback: AccountOperationProject,
    *,
    start_date: date,
    horizon_days: int,
) -> AccountOperationProject | None:
    try:
        data = llms.chat_json(
            [
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": USER_PROMPT.format(
                        client_brief=json.dumps(brief.to_dict(), ensure_ascii=False),
                        account_plan=json.dumps(_account_plan_dict(account_plan), ensure_ascii=False),
                        horizon_days=horizon_days,
                    ),
                },
            ],
            usage="llm",
            _chat=llms.chat,
        )
    except Exception:  # noqa: BLE001 - ops planning must keep deterministic fallback.
        return None
    return _with_critic(
        _merge_llm_project(data, fallback, start_date=start_date, horizon_days=horizon_days),
        brief,
        account_plan,
    )


def _merge_llm_project(
    data: dict[str, Any],
    fallback: AccountOperationProject,
    *,
    start_date: date,
    horizon_days: int,
) -> AccountOperationProject:
    plan_data = _mapping(data.get("operation_plan"))
    calendar_data = _mapping(data.get("content_calendar"))
    fallback_plan = fallback.operation_plan
    operation_plan = OperationPlan(
        plan_id=fallback_plan.plan_id,
        horizon_days=horizon_days,
        objectives=_string_list(plan_data.get("objectives"), fallback_plan.objectives, limit=4),
        content_pillars=_string_list(plan_data.get("content_pillars"), fallback_plan.content_pillars, limit=5),
        cadence=str(plan_data.get("cadence") or fallback_plan.cadence),
        kpi_targets=_mapping(plan_data.get("kpi_targets")) or dict(fallback_plan.kpi_targets),
        milestones=_milestones(plan_data.get("milestones"), fallback_plan.milestones, horizon_days=horizon_days),
        risk_controls=_string_list(plan_data.get("risk_controls"), fallback_plan.risk_controls, limit=4),
        notes=_string_list(plan_data.get("notes"), fallback_plan.notes, limit=5),
    )
    themes = _string_list(calendar_data.get("themes"), fallback.content_calendar.themes, limit=4)
    tasks = _tasks_from_llm(
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
        notes=_string_list(calendar_data.get("notes"), fallback.content_calendar.notes, limit=5),
        metadata=dict(fallback.content_calendar.metadata),
    )
    return AccountOperationProject(
        project_id=fallback.project_id,
        name=fallback.name,
        status="planning",
        client_brief=fallback.client_brief,
        account_positioning=dict(fallback.account_positioning),
        operation_plan=operation_plan,
        kpi_plan=_kpi_plan(operation_plan),
        content_calendar=content_calendar,
        content_tasks=list(tasks),
        artifacts=dict(fallback.artifacts),
        metadata={**fallback.metadata, "planner": "llm_with_fallback"},
    )


def _fallback_project(
    brief: ClientBrief,
    account_plan: AccountPlanResult | None,
    *,
    project_id: str,
    project_name: str,
    start_date: date,
    horizon_days: int,
) -> AccountOperationProject:
    plan_id = f"plan_{horizon_days}d"
    calendar_id = f"cal_{start_date.isoformat()}_{horizon_days}d"
    project = project_id or _stable_id("ops", brief.brand_name or brief.client_name or "local")
    name = project_name or _project_name(brief)
    pillars = _content_pillars(brief, account_plan)
    objectives = _objectives(brief, account_plan)
    risk_controls = _risk_controls(brief)
    cadence = _cadence(horizon_days)
    tasks = _fallback_tasks(
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
        milestones=_default_milestones(horizon_days),
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
        account_positioning=_account_positioning(account_plan),
        operation_plan=operation_plan,
        kpi_plan=_kpi_plan(operation_plan),
        content_calendar=calendar,
        content_tasks=list(tasks),
        artifacts={},
        metadata={"planner": "rule_fallback"},
    )


def _fallback_tasks(
    brief: ClientBrief,
    account_plan: AccountPlanResult | None,
    *,
    pillars: list[str],
    objectives: list[str],
    start_date: date,
    horizon_days: int,
) -> list[ContentTask]:
    task_count = min(3, max(1, horizon_days // 2))
    topics = _topic_pool(brief, account_plan, pillars)
    dates = _scheduled_dates(start_date, horizon_days, task_count)
    tasks: list[ContentTask] = []
    for index in range(task_count):
        topic = topics[index % len(topics)]
        objective = objectives[index % len(objectives)] if objectives else "建立账号认知"
        task_id = f"task_d{(dates[index] - start_date).days + 1:02d}_{index + 1:02d}"
        title = f"{topic}｜{_short_brand(brief)}"
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
                required_assets=_required_assets(brief),
                references=_task_references(account_plan),
                notes=["生成前需做内容合规与素材可用性检查。"],
                metadata={"source": "operation_planner_fallback"},
            )
        )
    return tasks


def _tasks_from_llm(
    value: Any,
    fallback_tasks: list[ContentTask],
    *,
    start_date: date,
    horizon_days: int,
    platform: str,
) -> list[ContentTask]:
    rows = value if isinstance(value, list) else []
    tasks: list[ContentTask] = []
    for index, row in enumerate(rows[: max(1, min(7, horizon_days))]):
        if not isinstance(row, dict):
            continue
        scheduled_date = _date_from_day(row.get("day"), start_date, horizon_days)
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
            priority=_int(row.get("priority"), default=index + 1),
            brief=_mapping(row.get("brief")),
            required_assets=_string_list(row.get("required_assets"), [], limit=6),
            references=[],
            notes=_string_list(row.get("notes"), [], limit=4),
            metadata={"source": "operation_planner_llm"},
        )
        tasks.append(task)
    return tasks or list(fallback_tasks)


def _with_critic(
    project: AccountOperationProject,
    brief: ClientBrief,
    account_plan: AccountPlanResult | None,
) -> AccountOperationProject:
    metadata = dict(project.metadata)
    metadata["critic"] = _critic_operation_project(project, brief, account_plan)
    project.metadata = metadata
    return project


def _critic_operation_project(
    project: AccountOperationProject,
    brief: ClientBrief,
    account_plan: AccountPlanResult | None,
) -> dict[str, Any]:
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


def _normalize_client_brief(value: ClientBrief | dict[str, Any] | None) -> ClientBrief:
    if isinstance(value, ClientBrief):
        return value
    return ClientBrief.from_dict(value if isinstance(value, dict) else {})


def _normalize_account_plan(value: AccountPlanResult | dict[str, Any] | None) -> AccountPlanResult | None:
    if isinstance(value, AccountPlanResult):
        return value
    if not isinstance(value, dict):
        return None
    return AccountPlanResult(
        tags=_mapping(value.get("tags")),
        recommended_positioning=str(value.get("recommended_positioning") or ""),
        audience_profile=_string_list(value.get("audience_profile"), []),
        content_directions=_string_list(value.get("content_directions"), []),
        benchmark_accounts=_mapping(value.get("benchmark_accounts")),
        unique_selling_points=_string_list(value.get("unique_selling_points"), []),
        ip_portrait_report=_mapping(value.get("ip_portrait_report")),
    )


def _account_plan_dict(value: AccountPlanResult | None) -> dict[str, Any]:
    return value.to_dict() if isinstance(value, AccountPlanResult) else {}


def _account_positioning(value: AccountPlanResult | None) -> dict[str, Any]:
    if value is None:
        return {}
    return {
        "tags": dict(value.tags),
        "recommended_positioning": value.recommended_positioning,
        "audience_profile": list(value.audience_profile),
        "unique_selling_points": list(value.unique_selling_points),
        "ip_portrait_report": dict(value.ip_portrait_report),
    }


def _content_pillars(brief: ClientBrief, account_plan: AccountPlanResult | None) -> list[str]:
    report = account_plan.ip_portrait_report if account_plan else {}
    raw_pillars = report.get("content_pillars") if isinstance(report, dict) else []
    pillars = [
        str(item.get("name") or item.get("description") or "").strip()
        for item in raw_pillars
        if isinstance(item, dict) and (item.get("name") or item.get("description"))
    ]
    pillars.extend(account_plan.content_directions if account_plan else [])
    pillars.extend(brief.positioning_notes)
    pillars.extend(brief.goals)
    return _dedupe([item for item in pillars if item])[:5] or ["账号定位", "产品价值", "用户场景"]


def _objectives(brief: ClientBrief, account_plan: AccountPlanResult | None) -> list[str]:
    objectives = list(brief.goals)
    if account_plan and account_plan.recommended_positioning:
        objectives.append(f"验证定位：{account_plan.recommended_positioning}")
    if account_plan:
        objectives.extend(account_plan.unique_selling_points[:2])
    return _dedupe([item for item in objectives if item])[:4] or ["建立账号基础认知", "沉淀可复用内容方向"]


def _risk_controls(brief: ClientBrief) -> list[str]:
    controls = ["每条内容发布前做平台合规审核", "封面和正文保持同一主题"]
    controls.extend([f"避免：{item}" for item in brief.taboos[:3]])
    controls.extend(brief.constraints[:2])
    return _dedupe(controls)[:5]


def _topic_pool(brief: ClientBrief, account_plan: AccountPlanResult | None, pillars: list[str]) -> list[str]:
    topics: list[str] = []
    topics.extend(account_plan.content_directions if account_plan else [])
    topics.extend(account_plan.unique_selling_points if account_plan else [])
    topics.extend(pillars)
    topics.extend(brief.positioning_notes)
    topics.extend(brief.goals)
    brand = brief.brand_name or brief.client_name
    if brand:
        topics.append(f"{brand}账号定位")
    return _dedupe([item for item in topics if item]) or ["账号定位", "用户痛点", "产品价值"]


def _task_references(account_plan: AccountPlanResult | None) -> list[dict[str, Any]]:
    if account_plan is None:
        return []
    benchmark = account_plan.benchmark_accounts if isinstance(account_plan.benchmark_accounts, dict) else {}
    return [
        {"source": "account_plan_keyword", "keyword": str(keyword)}
        for keyword in benchmark.get("search_keywords", [])[:3]
    ]


def _required_assets(brief: ClientBrief) -> list[str]:
    if not brief.source_materials:
        return ["品牌基础信息", "可用图片素材"]
    assets = [
        str(item.get("type") or item.get("kind") or item.get("usage") or "素材")
        for item in brief.source_materials
        if isinstance(item, dict)
    ]
    return _dedupe(assets) or ["品牌基础信息", "可用图片素材"]


def _default_milestones(horizon_days: int) -> list[dict[str, Any]]:
    mid = max(1, min(horizon_days, (horizon_days + 1) // 2))
    return [
        {"day": 1, "target": "确认账号定位与本周期内容支柱"},
        {"day": mid, "target": "完成首批内容任务制作与审核"},
        {"day": horizon_days, "target": "复盘本周期内容产出并准备下一轮选题"},
    ]


def _milestones(value: Any, fallback: list[dict[str, Any]], *, horizon_days: int) -> list[dict[str, Any]]:
    rows = value if isinstance(value, list) else []
    milestones = []
    for row in rows[:5]:
        if not isinstance(row, dict):
            continue
        day = _int(row.get("day"), default=1)
        day = min(max(day, 1), horizon_days)
        target = str(row.get("target") or row.get("name") or "").strip()
        if target:
            milestones.append({"day": day, "target": target})
    return milestones or list(fallback)


def _kpi_plan(operation_plan: OperationPlan) -> KPIPlan:
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


def _scheduled_dates(start: date, horizon_days: int, count: int) -> list[date]:
    if count <= 1:
        return [start]
    last_offset = max(0, horizon_days - 1)
    return [start + timedelta(days=round(index * last_offset / (count - 1))) for index in range(count)]


def _date_from_day(value: Any, start: date, horizon_days: int) -> date:
    day = _int(value, default=1)
    day = min(max(day, 1), horizon_days)
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


def _bounded_horizon(value: int) -> int:
    return min(max(_int(value, default=7), 1), 90)


def _cadence(horizon_days: int) -> str:
    if horizon_days <= 7:
        return "7 天内规划 3 条内容任务"
    if horizon_days <= 30:
        return "每周 3 条内容任务"
    return "每周 3-5 条内容任务"


def _project_name(brief: ClientBrief) -> str:
    name = brief.brand_name or brief.client_name or "Nori"
    return f"{name}账号代运营"


def _short_brand(brief: ClientBrief) -> str:
    return brief.brand_name or brief.client_name or "账号"


def _stable_id(prefix: str, value: str) -> str:
    cleaned = "".join(ch.lower() for ch in value if ch.isalnum())
    return f"{prefix}_{cleaned[:16] or 'local'}"


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


__all__ = ["OperationPlannerAgent", "plan_operation"]
