"""Calendar Planner: turn operation strategy and KPIs into content tasks."""
from __future__ import annotations

from nori.core import AccountOperationProject
from datetime import date
from typing import Any

from nori.core import AgentBase, LLMFactory
from nori.shared.llm_json import attach_llm_error, try_stage_json
from nori.core import ClientBrief

from . import inputs as _planner_inputs
from . import prompts as _planner_prompts
from . import normalizer as _calendar_normalizer
from .. import planner_critics as _planner_critics
from ..models import ContentCalendar, KPIPlan, OperationPlan


SYSTEM_PROMPT = _planner_prompts.SYSTEM_PROMPT
USER_PROMPT = _planner_prompts.USER_PROMPT_TEMPLATE


class CalendarPlannerAgent(AgentBase):
    """Create a ContentCalendar from an operation plan and KPI plan."""

    stage_name = "calendar_planner"

    def __init__(self, *, use_llm: bool = True, llm_factory: LLMFactory | None = None) -> None:
        super().__init__(stage_name=self.stage_name, use_llm=use_llm, llm_factory=llm_factory)

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
        plan, kpi, brief, inherited_calendar = _planner_inputs.normalize_inputs(
            operation_plan,
            kpi_plan=kpi_plan,
            client_brief=client_brief,
        )
        start, days = _planner_inputs.normalize_run_window(
            start_date=start_date,
            horizon_days=horizon_days,
            plan=plan,
            inherited_calendar=inherited_calendar,
        )
        fallback = _calendar_normalizer.fallback_calendar(plan, kpi, brief, start_date=start, horizon_days=days)
        should_use_llm = self.should_use_llm(use_llm)
        if not should_use_llm:
            return _with_critic(fallback, plan, kpi)
        planned = _llm_calendar(plan, kpi, brief, fallback, start_date=start, horizon_days=days, llm_factory=self.llm_factory)
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
    llm_factory: LLMFactory | None = None,
) -> ContentCalendar | None:
    llm_gateway = llm_factory or LLMFactory()
    data, error = try_stage_json(
        system=SYSTEM_PROMPT,
        user=_planner_prompts.build_user_prompt(
            plan,
            kpi,
            brief,
            start_date=start_date,
            horizon_days=horizon_days,
        ),
        chat_func=llm_gateway.chat_func,
        chat_json_func=llm_gateway.chat_json_func,
    )
    if data is None:
        if error:
            attach_llm_error(fallback.metadata, "calendar_planner", error)
        return None
    return _calendar_normalizer.merge_llm_calendar(
        data,
        fallback,
        plan,
        brief,
        start_date=start_date,
        horizon_days=horizon_days,
    )


def _with_critic(calendar: ContentCalendar, plan: OperationPlan, kpi: KPIPlan) -> ContentCalendar:
    metadata = dict(calendar.metadata)
    metadata["critic"] = _planner_critics.critic_calendar(calendar, plan, kpi)
    calendar.metadata = metadata
    return calendar


__all__ = ["CalendarPlannerAgent", "plan_calendar"]
