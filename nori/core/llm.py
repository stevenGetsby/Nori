"""Core LLM gateway factory for runtime stages."""
from __future__ import annotations

from typing import Any, Callable

import nori.core.llms as llms


class LLMFactory:
    """Small injectable facade around the core LLM infra gateway."""

    def __init__(
        self,
        *,
        chat_func: Callable[..., str] | None = None,
        chat_json_func: Callable[..., dict[str, Any]] | None = None,
        image_func: Callable[..., list[str]] | None = None,
    ) -> None:
        self.chat_func = chat_func or llms.chat
        self.chat_json_func = chat_json_func or llms.chat_json
        self.image_func = image_func or llms.image

    def chat(self, messages: list[dict[str, Any]], **kwargs: Any) -> str:
        return self.chat_func(messages, **kwargs)

    def chat_json(self, messages: list[dict[str, Any]], **kwargs: Any) -> dict[str, Any]:
        return self.chat_json_func(messages, **kwargs)

    def image(self, prompt: str, **kwargs: Any) -> list[str]:
        return self.image_func(prompt, **kwargs)


__all__ = ["LLMFactory"]
