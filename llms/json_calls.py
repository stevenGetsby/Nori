"""JSON chat-call retry plumbing for the LLM gateway."""
from __future__ import annotations

from typing import Any, Callable


def chat_json_raw(
    messages: list[dict[str, Any]],
    *,
    usage: str,
    json_mode: bool,
    retry_without_response_format: bool,
    chat_func: Callable[..., str],
    params: dict[str, Any],
) -> str:
    """Run a chat function and return raw text with optional JSON-mode fallback."""
    request_params = dict(params)
    if json_mode:
        request_params.setdefault("response_format", {"type": "json_object"})
    try:
        return chat_func(messages, usage=usage, **request_params)
    except TypeError as exc:
        if not (
            should_retry_without_response_format(request_params, json_mode, retry_without_response_format)
            and is_response_format_error(exc)
        ):
            raise
        return chat_func(messages, usage=usage, **without_response_format(request_params))
    except Exception as exc:  # noqa: BLE001
        if not (
            should_retry_without_response_format(request_params, json_mode, retry_without_response_format)
            and is_response_format_error(exc)
        ):
            raise
        return chat_func(messages, usage=usage, **without_response_format(request_params))


def should_retry_without_response_format(
    params: dict[str, Any],
    json_mode: bool,
    retry_without_response_format: bool,
) -> bool:
    return json_mode and retry_without_response_format and "response_format" in params


def without_response_format(params: dict[str, Any]) -> dict[str, Any]:
    retry_params = dict(params)
    retry_params.pop("response_format", None)
    return retry_params


def is_response_format_error(exc: Exception) -> bool:
    msg = str(exc).lower()
    normalized = msg.replace("-", "_").replace(" ", "_")
    if "response_format" in normalized or "json_object" in normalized:
        return True
    return "unsupported" in normalized and "json" in normalized
