"""KPI Planner: turn operation strategy into measurable targets."""
from __future__ import annotations

from nori.core import AccountOperationProject
from typing import Any

from nori.core import AgentBase, LLMFactory
from nori.shared.llm_json import attach_llm_error, try_stage_json

from . import normalizer as _kpi_normalizer
from .package import KPIPlannerInputPreparer, KPIPlannerPromptBuilder
from .. import planner_critics as _planner_critics
from nori.core import KPIPlan, OperationPlan


_INPUT_PREPARER = KPIPlannerInputPreparer()
_PROMPT_BUILDER = KPIPlannerPromptBuilder()
SYSTEM_PROMULGATION = _PROMPT_BUILDER.system_prompt
USER_PROMPT = _PROMPT_BUILDER.user_prompt_template


class KPIPlannerAgent(AgentBase):
    """Create a KPIPlan from an operation plan with deterministic fallback."""

    stage_name = "kpi_planner"

    def __init__(self, *, use_llm: bool = True, llm_factory: LLMFactory | None = None) -> None:
        super().__init__(stage_name=self.stage_name, use_llm=use_llm, llm_factory=llm_factory)
        self.input_preparer = _INPUT_PREPARER
        self.prompt_builder = _PROMPT_BUILDER

    def run(
        self,
        operation_plan: OperationPlan | AccountOperationProject | dict[str, Any] | None,
        *,
        project_context: dict[str, Any] | None = None,
        use_llm: bool | None = None,
    ) -> KPIPlan:
        prepared = self.input_preparer.prepare(operation_plan, project_context)
        fallback = _kpi_normalizer.fallback_kpi_plan(prepared.operation_plan, prepared.project_context)
        should_use_llm = self.should_use_llm(use_llm)
        if not should_use_llm:
            return _with_critic(fallback, prepared.operation_plan)
        planned = _llm_kpi_plan(
            prepared.operation_plan,
            prepared.project_context,
            fallback,
            llm_factory=self.llm_factory,
            prompt_builder=self.prompt_builder,
        )
        return _with_critic(planned or fallback, prepared.operation_plan)


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
    *,
    llm_factory: LLMFactory | None = None,
    prompt_builder: KPIPlannerPromptBuilder | None = None,
) -> KPIPlan | None:
    llm_gateway = llm_factory or LLMFactory()
    prompts = prompt_builder or _PROMPT_BUILDER
    data, error = try_stage_json(
        system=prompts.system_prompt,
        user=prompts.build_user_prompt(plan, context),
        chat_json_func=llm_gateway.chat_json_func,
    )
    if data is None:
        if error:
            attach_llm_error(fallback.metadata, "kpi_planner", error)
        return None
    return _kpi_normalizer.merge_llm_kpi_plan(data, fallback, plan)


def _with_critic(plan: KPIPlan, operation_plan: OperationPlan) -> KPIPlan:
    metadata = dict(plan.metadata)
    metadata["critic"] = _planner_critics.critic_kpi_plan(plan, operation_plan)
    plan.metadata = metadata
    return plan
