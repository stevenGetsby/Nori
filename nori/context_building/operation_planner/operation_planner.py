"""Operation planner for account-operations SOP projects."""
from __future__ import annotations

from nori.core import AccountOperationProject
from datetime import date
from typing import Any

from nori.core import AgentBase, LLMFactory
from nori.user_profiling.models import AccountPlanResult
from nori.shared.llm_json import attach_llm_error, try_stage_json
from nori.core import ClientBrief

from . import normalizer as _plan_normalizer
from . import inputs as _planner_inputs
from . import prompts as _planner_prompts
from . import project_builder as _project_builder
from .. import planner_critics as _planner_critics


SYSTEM_PROMPT = _planner_prompts.SYSTEM_PROMPT
USER_PROMPT = _planner_prompts.USER_PROMPT_TEMPLATE


class OperationPlannerAgent(AgentBase):
    """Turn account positioning into a bounded operation project."""

    stage_name = "operation_planner"

    def __init__(self, *, use_llm: bool = True, llm_factory: LLMFactory | None = None) -> None:
        super().__init__(stage_name=self.stage_name, use_llm=use_llm, llm_factory=llm_factory)

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
        brief = _planner_inputs.normalize_client_brief(client_brief)
        normalized_plan = _planner_inputs.normalize_account_plan(account_plan)
        days = _planner_inputs.bounded_horizon(horizon_days)
        start = _planner_inputs.normalize_start_date(start_date)
        fallback = _project_builder.fallback_project(
            brief,
            normalized_plan,
            project_id=project_id,
            project_name=project_name,
            start_date=start,
            horizon_days=days,
        )

        should_use_llm = self.should_use_llm(use_llm)
        if not should_use_llm:
            return _with_critic(fallback, brief, normalized_plan)

        planned = _llm_project(
            brief,
            normalized_plan,
            fallback,
            start_date=start,
            horizon_days=days,
            llm_factory=self.llm_factory,
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
    llm_factory: LLMFactory | None = None,
) -> AccountOperationProject | None:
    llm_gateway = llm_factory or LLMFactory()
    data, error = try_stage_json(
        system=SYSTEM_PROMPT,
        user=_planner_prompts.build_user_prompt(brief, account_plan, horizon_days=horizon_days),
        chat_func=llm_gateway.chat_func,
        chat_json_func=llm_gateway.chat_json_func,
    )
    if data is None:
        if error:
            attach_llm_error(fallback.metadata, "operation_planner", error)
        return None
    return _with_critic(
        _plan_normalizer.merge_llm_project(data, fallback, start_date=start_date, horizon_days=horizon_days),
        brief,
        account_plan,
    )


def _with_critic(
    project: AccountOperationProject,
    brief: ClientBrief,
    account_plan: AccountPlanResult | None,
) -> AccountOperationProject:
    metadata = dict(project.metadata)
    metadata["critic"] = _planner_critics.critic_operation_project(project, brief, account_plan)
    project.metadata = metadata
    return project


__all__ = ["OperationPlannerAgent", "plan_operation"]
