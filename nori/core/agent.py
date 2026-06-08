"""Base class for concrete Nori runtime agents."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from nori.shared.llm_json import attach_llm_error, call_stage_json, call_stage_messages_json, try_stage_json

from .llm import LLMFactory


@dataclass(frozen=True)
class AgentPrompt:
    """A fully rendered system/user prompt pair for one JSON stage."""

    system: str
    user: str


class AgentInputPreparer:
    """Base marker for class-owned stage input restoration.

    Stage packages use subclasses to keep coercion, defaults, and run-window
    normalization together instead of scattering standalone helper functions.
    """


class AgentPromptBuilder:
    """Base class for class-owned prompt contracts."""

    system_prompt = ""
    user_prompt_template = ""

    def build_user_prompt(self, *args: Any, **kwargs: Any) -> str:
        raise NotImplementedError

    def build(self, *args: Any, **kwargs: Any) -> AgentPrompt:
        return AgentPrompt(system=self.system_prompt, user=self.build_user_prompt(*args, **kwargs))


class AgentBase:
    """Common runtime shell for stage agents.

    Subclasses keep their domain-specific ``run`` signature, but share LLM
    injection, stage naming, and JSON-call helpers here.
    """

    stage_name = ""

    def __init__(
        self,
        *,
        stage_name: str | None = None,
        use_llm: bool = True,
        llm_factory: LLMFactory | None = None,
    ) -> None:
        if stage_name is not None:
            self.stage_name = stage_name
        self.use_llm = use_llm
        self.llm_factory = llm_factory or LLMFactory()

    def messages(self, system: str, user: Any) -> list[dict[str, Any]]:
        return [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]

    def should_use_llm(self, override: bool | None = None) -> bool:
        return self.use_llm if override is None else override

    def call_json(
        self,
        *,
        system: str,
        user: str,
        error_type,
        timeout: int = 60,
        usage: str = "llm",
        json_mode: bool = True,
    ) -> dict[str, Any]:
        return call_stage_json(
            system=system,
            user=user,
            timeout=timeout,
            usage=usage,
            json_mode=json_mode,
            error_type=error_type,
            chat_json_func=self.llm_factory.chat_json_func,
        )

    def call_messages_json(
        self,
        *,
        messages: list[dict[str, Any]],
        error_type,
        timeout: int = 60,
        usage: str = "llm",
        json_mode: bool = True,
    ) -> dict[str, Any]:
        return call_stage_messages_json(
            messages=messages,
            timeout=timeout,
            usage=usage,
            json_mode=json_mode,
            error_type=error_type,
            chat_json_func=self.llm_factory.chat_json_func,
        )

    def try_json(
        self,
        *,
        system: str,
        user: str,
        timeout: int | None = None,
        usage: str = "llm",
        json_mode: bool = True,
    ) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
        return try_stage_json(
            system=system,
            user=user,
            timeout=timeout,
            usage=usage,
            json_mode=json_mode,
            chat_json_func=self.llm_factory.chat_json_func,
        )

    def attach_llm_error(self, target: dict[str, Any], error: dict[str, Any], *, stage: str | None = None) -> None:
        attach_llm_error(target, stage or self.stage_name, error)


__all__ = ["AgentBase", "AgentInputPreparer", "AgentPrompt", "AgentPromptBuilder"]
