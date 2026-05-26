"""Pure CalendarPlanner policy helpers."""
from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from nori.core import ClientBrief
from nori.shared.normalization import dedupe_preserve_order, int_value

from nori.core import KPIPlan, OperationPlan


def task_count_from_targets(plan: OperationPlan, kpi: KPIPlan, horizon_days: int) -> int:
    target = target_task_count(kpi)
    if target:
        return max(1, min(7, target))
    explicit = int_value(plan.kpi_targets.get("content_tasks"), default=0)
    if explicit > 0:
        return max(1, min(7, explicit))
    if horizon_days <= 7:
        return 3
    weeks = max(1, round(horizon_days / 7))
    return max(1, min(7, weeks * 3))


def target_task_count(kpi: KPIPlan) -> int:
    return int_value(kpi.targets.get("content_tasks"), default=0)


def scheduled_dates(start: date, horizon_days: int, count: int) -> list[date]:
    if count <= 1:
        return [start]
    last_offset = max(0, horizon_days - 1)
    return [start + timedelta(days=round(index * last_offset / (count - 1))) for index in range(count)]


def date_from_day(value: Any, start: date, horizon_days: int) -> date:
    day = int_value(value, default=1)
    day = min(max(day, 1), max(1, horizon_days))
    return start + timedelta(days=day - 1)


def normalize_start_date(value: str | date | None) -> date:
    if isinstance(value, date):
        return value
    if isinstance(value, str) and value:
        try:
            return date.fromisoformat(value)
        except ValueError:
            pass
    return date.today()


def bounded_horizon(value: int | None) -> int:
    return min(max(int_value(value, default=7), 1), 90)


def calendar_id(start_date: date, horizon_days: int) -> str:
    return f"cal_{start_date.isoformat()}_{horizon_days}d"


def cadence_for_horizon(horizon_days: int) -> str:
    if horizon_days <= 7:
        return "7 天内规划 3 条内容任务"
    if horizon_days <= 30:
        return "每周 3 条内容任务"
    return "每周 3-5 条内容任务"


def topic_for_task(pillar: str, objective: str, brief: ClientBrief) -> str:
    brand = brief.brand_name or brief.client_name
    if brand and pillar not in brand:
        return f"{brand}{pillar}"
    if objective:
        return objective[:24]
    return pillar or "账号内容"


def objective_for_index(plan: OperationPlan, index: int) -> str:
    if plan.objectives:
        return plan.objectives[index % len(plan.objectives)]
    return "完成本周期内容目标"


def short_brand(brief: ClientBrief) -> str:
    return brief.brand_name or brief.client_name or "账号"


def required_assets(brief: ClientBrief) -> list[str]:
    if not brief.source_materials:
        return ["品牌基础信息", "可用图片素材"]
    assets = [
        str(item.get("type") or item.get("kind") or item.get("usage") or "素材")
        for item in brief.source_materials
        if isinstance(item, dict)
    ]
    return dedupe(assets) or ["品牌基础信息", "可用图片素材"]


def dedupe(values: list[str]) -> list[str]:
    return dedupe_preserve_order(values)
