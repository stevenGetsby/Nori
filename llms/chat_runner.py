"""Sync and async chat execution for the LLM gateway."""
from __future__ import annotations

import time
from typing import Any, Callable

from .capabilities import ensure_chat_capability
from .client import get_async_client, get_client
from .request_params import merge_chat_kwargs
from .results import extract_chat_text
from .telemetry import emit_telemetry


def chat_text(
    messages: list[dict[str, Any]],
    *,
    usage: str = "llm",
    _get_client: Callable[[str], Any] | None = None,
    **kwargs: Any,
) -> str:
    """Run a synchronous chat request and return normalized text."""
    client_factory = _get_client or get_client
    bundle = client_factory(usage)
    params = merge_chat_kwargs(bundle.model, kwargs)
    started = time.perf_counter()
    try:
        ensure_chat_capability(bundle.model, messages, usage)
        resp = bundle.client.chat.completions.create(
            model=bundle.model_id,
            messages=messages,
            **params,
        )
        text = extract_chat_text(resp, bundle.model)
    except Exception as exc:  # noqa: BLE001
        emit_telemetry("chat", usage, bundle.model, started, error=exc)
        raise
    emit_telemetry("chat", usage, bundle.model, started)
    return text


async def achat_text(
    messages: list[dict[str, Any]],
    *,
    usage: str = "llm",
    _get_async_client: Callable[[str], Any] | None = None,
    **kwargs: Any,
) -> str:
    """Run an asynchronous chat request and return normalized text."""
    client_factory = _get_async_client or get_async_client
    bundle = client_factory(usage)
    params = merge_chat_kwargs(bundle.model, kwargs)
    started = time.perf_counter()
    try:
        ensure_chat_capability(bundle.model, messages, usage)
        resp = await bundle.client.chat.completions.create(
            model=bundle.model_id,
            messages=messages,
            **params,
        )
        text = extract_chat_text(resp, bundle.model)
    except Exception as exc:  # noqa: BLE001
        emit_telemetry("achat", usage, bundle.model, started, error=exc)
        raise
    emit_telemetry("achat", usage, bundle.model, started)
    return text
