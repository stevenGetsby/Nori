"""Account Planner Agent: turn user context into account strategy."""
from __future__ import annotations

from typing import Any

from nori.core import AgentBase, LLMFactory
from nori.user_profiling.models import AccountPlanResult, AccountPlannerInput
from nori.shared.llm_json import attach_llm_error, try_stage_json

from . import fallback as _plan_fallback
from . import inputs as _plan_inputs
from . import normalizer as _plan_normalizer
from . import prompts as _plan_prompts
from .search import EmptySearchProvider, SearchProvider
from .search import run_search as _run_search


class AccountPlannerAgent(AgentBase):
	"""LLM-first account planner with a minimal structural fallback."""

	stage_name = "account_planner"

	def __init__(
		self,
		*,
		use_llm: bool = True,
		search_provider: SearchProvider | None = None,
		llm_factory: LLMFactory | None = None,
	) -> None:
		super().__init__(stage_name=self.stage_name, use_llm=use_llm, llm_factory=llm_factory)
		self.search_provider = search_provider or EmptySearchProvider()

	def run(
		self,
		user_input: AccountPlannerInput | str,
		images: list[str] | None = None,
		links: list[str] | None = None,
		*,
		use_llm: bool | None = None,
		enable_search: bool | None = None,
	) -> AccountPlanResult:
		normalized = _plan_inputs.normalize_input(user_input, images, links)
		if enable_search is not None:
			normalized.enable_search = enable_search

		fallback = _plan_fallback.fallback_plan(normalized)
		should_use_llm = self.should_use_llm(use_llm)
		result = self._draft_plan(normalized, fallback, should_use_llm)

		if normalized.enable_search:
			result = self._enrich_with_search(normalized, result, should_use_llm)

		return result

	def _draft_plan(
		self,
		normalized: AccountPlannerInput,
		fallback: AccountPlanResult,
		should_use_llm: bool,
	) -> AccountPlanResult:
		if not should_use_llm:
			return fallback
		return _llm_plan(normalized, fallback, [], llm_factory=self.llm_factory) or fallback

	def _enrich_with_search(
		self,
		normalized: AccountPlannerInput,
		result: AccountPlanResult,
		should_use_llm: bool,
	) -> AccountPlanResult:
		search_results = _run_search(self.search_provider, normalized, result)
		if not search_results:
			return result
		if should_use_llm:
			refined = _llm_plan(normalized, result, search_results, llm_factory=self.llm_factory)
			if refined:
				return refined
		return _plan_normalizer.merge_search_results(result, search_results)


account_plan = AccountPlannerAgent().run


SYSTEM_PROMPT = _plan_prompts.SYSTEM_PROMPT
USER_PROMPT = _plan_prompts.USER_PROMPT_TEMPLATE


def _llm_plan(
	normalized: AccountPlannerInput,
	fallback: AccountPlanResult,
	search_results: list[dict[str, Any]],
	*,
	llm_factory: LLMFactory | None = None,
) -> AccountPlanResult | None:
	llm_gateway = llm_factory or LLMFactory()
	data, error = try_stage_json(
		system=SYSTEM_PROMPT,
		user=_plan_prompts.build_user_prompt(normalized, search_results),
		chat_func=llm_gateway.chat_func,
		chat_json_func=llm_gateway.chat_json_func,
	)
	if data is None:
		if error:
			attach_llm_error(fallback.metadata, "account_planner", error)
		return None
	result = _plan_normalizer.normalize_llm_result(data, fallback, search_results)
	result.metadata = {**dict(result.metadata), "llm_enhanced": True}
	return result
