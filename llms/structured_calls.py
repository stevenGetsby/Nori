"""Shared non-throwing JSON call wrapper for structured LLM helpers."""
from __future__ import annotations

from collections.abc import Callable
from typing import Any

from .call import chat_json_with_raw
from nori.core.contracts import ChatJSONError, StructuredCallResult
from .structured_outputs import chat_json_error_reason


def call_structured_json(
    messages: list[dict[str, Any]],
    *,
    usage: str = "llm",
    timeout: float = 6.0,
    chat_json_with_raw_func: Callable[..., tuple[dict[str, Any], str]] = chat_json_with_raw,
) -> StructuredCallResult:
    """Call JSON mode and convert parse/provider failures into result metadata."""
    raw = ""
    try:
        data, raw = chat_json_with_raw_func(
            messages,
            usage=usage,
            timeout=timeout,
            json_mode=True,
        )
    except ChatJSONError as exc:
        return StructuredCallResult(raw=exc.raw, error=chat_json_error_reason(exc))
    except Exception as exc:  # noqa: BLE001
        return StructuredCallResult(raw=raw, error=f"api_error:{type(exc).__name__}")
    return StructuredCallResult(data=data, raw=raw)
