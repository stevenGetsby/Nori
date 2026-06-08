"""Project-level AI gateway entrypoints."""
from __future__ import annotations

from typing import Any

from . import client as _client_module
from .client import (
    NoriAIClient,
    current_mode,
    ensure_ready,
    get_active,
    set_mode,
)
from nori.core.contracts import (
    ChatCapabilityError,
    ChatJSONError,
    ChatResultError,
    ImageCapabilityError,
    ImageResultError,
    LLMClientConfigError,
)
from .telemetry import set_telemetry_sink


def chat(
    messages: list[dict[str, Any]],
    *,
    usage: str = "llm",
    **kwargs: Any,
) -> str:
    return _client_module.get_default_client().chat(messages, usage=usage, **kwargs)


async def achat(
    messages: list[dict[str, Any]],
    *,
    usage: str = "llm",
    **kwargs: Any,
) -> str:
    return await _client_module.get_default_client().achat(messages, usage=usage, **kwargs)


def chat_json(
    messages: list[dict[str, Any]],
    *,
    usage: str = "llm",
    **kwargs: Any,
) -> dict[str, Any]:
    return _client_module.get_default_client().chat_json(messages, usage=usage, **kwargs)


def image(
    prompt: str,
    *,
    usage: str = "image",
    **kwargs: Any,
) -> list[str]:
    return _client_module.get_default_client().image(prompt, usage=usage, **kwargs)


__all__ = [
    "get_active",
    "current_mode",
    "set_mode",
    "ensure_ready",
    "NoriAIClient",
    "LLMClientConfigError",
    "chat",
    "chat_json",
    "set_telemetry_sink",
    "ChatCapabilityError",
    "ChatJSONError",
    "ChatResultError",
    "ImageCapabilityError",
    "ImageResultError",
    "achat",
    "image",
]
