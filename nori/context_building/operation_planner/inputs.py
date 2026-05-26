"""OperationPlanner input and run-parameter normalization helpers."""
from __future__ import annotations

from datetime import date
from typing import Any

from nori.core import ClientBrief
from nori.shared.normalization import bounded_int, int_value, mapping, string_list
from nori.user_profiling.models import AccountPlanResult


def normalize_client_brief(value: ClientBrief | dict[str, Any] | None) -> ClientBrief:
    if isinstance(value, ClientBrief):
        return value
    return ClientBrief.from_dict(value if isinstance(value, dict) else {})


def normalize_account_plan(value: AccountPlanResult | dict[str, Any] | None) -> AccountPlanResult | None:
    if isinstance(value, AccountPlanResult):
        return value
    if not isinstance(value, dict):
        return None
    return AccountPlanResult(
        tags=mapping(value.get("tags")),
        recommended_positioning=str(value.get("recommended_positioning") or ""),
        audience_profile=string_list(value.get("audience_profile"), []),
        content_directions=string_list(value.get("content_directions"), []),
        benchmark_accounts=mapping(value.get("benchmark_accounts")),
        unique_selling_points=string_list(value.get("unique_selling_points"), []),
        ip_portrait_report=mapping(value.get("ip_portrait_report")),
    )


def account_plan_dict(value: AccountPlanResult | None) -> dict[str, Any]:
    return value.to_dict() if isinstance(value, AccountPlanResult) else {}


def normalize_start_date(value: str | date | None) -> date:
    if isinstance(value, date):
        return value
    if isinstance(value, str) and value:
        try:
            return date.fromisoformat(value)
        except ValueError:
            pass
    return date.today()


def bounded_horizon(value: Any) -> int:
    return bounded_int(value, default=7, minimum=1, maximum=90)
