"""KPI Planner: turn operation strategy into measurable targets."""
from __future__ import annotations

import json
from typing import Any

import llms
from nori.ops_models import AccountOperationProject, KPIPlan, OperationPlan


SYSTEM_PROMULGATION = "你是 Nori 的账号代运营 KPI 规划器，只输出 JSON。"

USER_PROMPT = """\
根据运营计划生成可人工核验的 KPI 计划。

运营计划：
{operation_plan}

项目上下文：
{project_context}

要求：
- 不要假设已经有自动数据抓取能力。
- 指标必须能人工记录或从平台后台读取。
- 不做真实发布承诺，只做目标和核验方法。

输出 JSON，字段固定：
{{
  "targets": {{
    "content_tasks": 3,
    "review_pass_rate": ">= 90%",
    "manual_metrics_check": "每周 1 次"
  }},
  "milestones": [
    {{"day": 1, "target": "确认基线指标"}},
    {{"day": 7, "target": "完成本周期复盘"}}
  ],
  "measurement_notes": ["如何核验指标，2-5 条"]
}}
"""


class KPIPlannerAgent:
    """Create a KPIPlan from an operation plan with deterministic fallback."""

    def __init__(self, *, use_llm: bool = True) -> None:
        self.use_llm = use_llm

    def run(
        self,
        operation_plan: OperationPlan | AccountOperationProject | dict[str, Any] | None,
        *,
        project_context: dict[str, Any] | None = None,
        use_llm: bool | None = None,
    ) -> KPIPlan:
        plan, context = _normalize_plan_and_context(operation_plan, project_context)
        fallback = _fallback_kpi_plan(plan, context)
        should_use_llm = self.use_llm if use_llm is None else use_llm
        if not should_use_llm:
            return _with_critic(fallback, plan)
        planned = _llm_kpi_plan(plan, context, fallback)
        return _with_critic(planned or fallback, plan)


def plan_kpi(
    operation_plan: OperationPlan | AccountOperationProject | dict[str, Any] | None,
    **kwargs: Any,
) -> KPIPlan:
    """Convenience wrapper for one-shot KPI planning."""

    return KPIPlannerAgent().run(operation_plan, **kwargs)


def _llm_kpi_plan(
    plan: OperationPlan,
    context: dict[str, Any],
    fallback: KPIPlan,
) -> KPIPlan | None:
    try:
        data = llms.chat_json(
            [
                {"role": "system", "content": SYSTEM_PROMULGATION},
                {
                    "role": "user",
                    "content": USER_PROMPT.format(
                        operation_plan=json.dumps(plan.to_dict(), ensure_ascii=False),
                        project_context=json.dumps(context, ensure_ascii=False),
                    ),
                },
            ],
            usage="llm",
            _chat=llms.chat,
        )
    except Exception:  # noqa: BLE001 - KPI planner must keep a usable fallback.
        return None
    targets = _mapping(data.get("targets")) or dict(fallback.targets)
    milestones = _milestones(data.get("milestones"), fallback.milestones, plan.horizon_days)
    notes = _string_list(data.get("measurement_notes"), fallback.measurement_notes, limit=5)
    return KPIPlan(
        plan_id=fallback.plan_id,
        horizon_days=fallback.horizon_days,
        targets=targets,
        milestones=milestones,
        measurement_notes=notes,
        metadata={**fallback.metadata, "planner": "llm_with_fallback"},
    )


def _fallback_kpi_plan(plan: OperationPlan, context: dict[str, Any]) -> KPIPlan:
    targets = dict(plan.kpi_targets)
    targets.setdefault("content_tasks", _content_task_target(plan, context))
    targets.setdefault("review_pass_rate", ">= 90%")
    targets.setdefault("manual_metrics_check", _check_cadence(plan.horizon_days))
    if plan.horizon_days <= 7:
        targets.setdefault("cycle_review", "完成 1 次周期复盘")
    else:
        targets.setdefault("weekly_review", "每周完成 1 次复盘")

    return KPIPlan(
        plan_id=f"kpi_{plan.plan_id}" if plan.plan_id else "kpi_plan",
        horizon_days=plan.horizon_days,
        targets=targets,
        milestones=_milestones(plan.milestones, _default_milestones(plan.horizon_days), plan.horizon_days),
        measurement_notes=[
            "所有指标默认人工记录或从平台后台读取。",
            "内容数量以已完成审核的 ContentTask 计数。",
            "审核通过率以 ComplianceReview status=passed 的比例计算。",
        ],
        metadata={"planner": "rule_fallback", "source_plan_id": plan.plan_id},
    )


def _with_critic(plan: KPIPlan, operation_plan: OperationPlan) -> KPIPlan:
    metadata = dict(plan.metadata)
    metadata["critic"] = _critic_kpi_plan(plan, operation_plan)
    plan.metadata = metadata
    return plan


def _critic_kpi_plan(plan: KPIPlan, operation_plan: OperationPlan) -> dict[str, Any]:
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


def _normalize_plan_and_context(
    value: OperationPlan | AccountOperationProject | dict[str, Any] | None,
    project_context: dict[str, Any] | None,
) -> tuple[OperationPlan, dict[str, Any]]:
    if isinstance(value, AccountOperationProject):
        context = {
            "project_id": value.project_id,
            "project_name": value.name,
            "client_brief": value.client_brief.to_dict(),
            "content_task_count": len(value.content_tasks),
            **dict(project_context or {}),
        }
        return value.operation_plan, context
    if isinstance(value, OperationPlan):
        return value, dict(project_context or {})
    data = _mapping(value)
    if "operation_plan" in data and isinstance(data.get("operation_plan"), dict):
        context = {key: data[key] for key in ("project_id", "name", "client_brief") if key in data}
        context.update(project_context or {})
        return OperationPlan.from_dict(data.get("operation_plan")), context
    return OperationPlan.from_dict(data), dict(project_context or {})


def _content_task_target(plan: OperationPlan, context: dict[str, Any]) -> int:
    explicit = context.get("content_task_count")
    if isinstance(explicit, int) and explicit > 0:
        return explicit
    if plan.horizon_days <= 7:
        return 3
    weeks = max(1, round(plan.horizon_days / 7))
    return weeks * 3


def _check_cadence(horizon_days: int) -> str:
    if horizon_days <= 7:
        return "周期结束手动核验 1 次"
    return "每周手动核验 1 次"


def _default_milestones(horizon_days: int) -> list[dict[str, Any]]:
    mid = max(1, min(horizon_days, (horizon_days + 1) // 2))
    return [
        {"day": 1, "target": "确认本周期 KPI 基线"},
        {"day": mid, "target": "检查内容产出和审核通过率"},
        {"day": horizon_days, "target": "完成 KPI 复盘记录"},
    ]


def _milestones(value: Any, fallback: list[dict[str, Any]], horizon_days: int) -> list[dict[str, Any]]:
    rows = value if isinstance(value, list) else []
    output: list[dict[str, Any]] = []
    for row in rows[:5]:
        if not isinstance(row, dict):
            continue
        day = _int(row.get("day"), default=1)
        day = min(max(day, 1), max(1, horizon_days))
        target = str(row.get("target") or row.get("name") or "").strip()
        if target:
            output.append({"day": day, "target": target})
    return output or list(fallback)


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


def _int(value: Any, *, default: int) -> int:
    if isinstance(value, bool):
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default
