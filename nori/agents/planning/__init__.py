"""Context-building module."""
from __future__ import annotations

from nori.core import AssetLibrary, AssetRecord
from nori.core import AccountOperationProject, ContentCalendar, ContentTask, KPIPlan, OperationPlan
from nori.core.lazy_exports import lazy_export


_LAZY_EXPORTS = {
    "OperationPlannerAgent": "operation_planner",
    "plan_operation": "operation_planner",
    "KPIPlannerAgent": "kpi_planner",
    "plan_kpi": "kpi_planner",
    "CalendarPlannerAgent": "calendar_planner",
    "plan_calendar": "calendar_planner",
}

__all__ = [
    "AccountOperationProject",
    "AssetLibrary",
    "AssetRecord",
    "CalendarPlannerAgent",
    "ContentCalendar",
    "ContentTask",
    "KPIPlan",
    "KPIPlannerAgent",
    "OperationPlan",
    "OperationPlannerAgent",
    "plan_calendar",
    "plan_kpi",
    "plan_operation",
]


def __getattr__(name: str):
    return lazy_export(__name__, _LAZY_EXPORTS, name)
