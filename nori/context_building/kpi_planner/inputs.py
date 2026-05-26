"""KPIPlanner input normalization helpers."""
from __future__ import annotations

from nori.core import AccountOperationProject
from typing import Any

from nori.shared.normalization import mapping

from ..models import OperationPlan


def normalize_plan_and_context(
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
    data = mapping(value)
    if "operation_plan" in data and isinstance(data.get("operation_plan"), dict):
        context = {key: data[key] for key in ("project_id", "name", "client_brief") if key in data}
        context.update(project_context or {})
        return OperationPlan.from_dict(data.get("operation_plan")), context
    return OperationPlan.from_dict(data), dict(project_context or {})
