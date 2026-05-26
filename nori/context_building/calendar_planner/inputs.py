"""CalendarPlanner input and run-parameter normalization helpers."""
from __future__ import annotations

from nori.core import AccountOperationProject
from datetime import date
from typing import Any

from nori.core import ClientBrief
from nori.shared.normalization import mapping

from ..models import ContentCalendar, KPIPlan, OperationPlan

from .policy import bounded_horizon, normalize_start_date


def normalize_inputs(
    value: OperationPlan | AccountOperationProject | dict[str, Any] | None,
    *,
    kpi_plan: KPIPlan | dict[str, Any] | None = None,
    client_brief: ClientBrief | dict[str, Any] | None = None,
) -> tuple[OperationPlan, KPIPlan, ClientBrief, ContentCalendar]:
    """Restore CalendarPlanner inputs into typed operation, KPI, brief, and calendar models."""
    if isinstance(value, AccountOperationProject):
        return (
            value.operation_plan,
            normalize_kpi(kpi_plan) if kpi_plan is not None else value.kpi_plan,
            normalize_brief(client_brief) if client_brief is not None else value.client_brief,
            value.content_calendar,
        )
    if isinstance(value, OperationPlan):
        return value, normalize_kpi(kpi_plan), normalize_brief(client_brief), ContentCalendar()
    data = mapping(value)
    if "operation_plan" in data and isinstance(data.get("operation_plan"), dict):
        return (
            OperationPlan.from_dict(data.get("operation_plan")),
            normalize_kpi(kpi_plan or data.get("kpi_plan")),
            normalize_brief(client_brief or data.get("client_brief")),
            ContentCalendar.from_dict(data.get("content_calendar")),
        )
    return OperationPlan.from_dict(data), normalize_kpi(kpi_plan), normalize_brief(client_brief), ContentCalendar()


def normalize_kpi(value: KPIPlan | dict[str, Any] | None) -> KPIPlan:
    if isinstance(value, KPIPlan):
        return value
    return KPIPlan.from_dict(value if isinstance(value, dict) else {})


def normalize_brief(value: ClientBrief | dict[str, Any] | None) -> ClientBrief:
    if isinstance(value, ClientBrief):
        return value
    return ClientBrief.from_dict(value if isinstance(value, dict) else {})


def normalize_run_window(
    *,
    start_date: str | date | None,
    horizon_days: int | None,
    plan: OperationPlan,
    inherited_calendar: ContentCalendar,
) -> tuple[date, int]:
    days = bounded_horizon(horizon_days or plan.horizon_days)
    start = normalize_start_date(start_date or inherited_calendar.start_date)
    return start, days
