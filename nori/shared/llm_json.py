"""Shared JSON LLM call utilities for Nori runtime stages."""
from __future__ import annotations

from typing import Any

import llms
from llms.structured_outputs import chat_json_error_reason


def call_stage_json(
    *,
    system: str,
    user: str,
    timeout: int,
    error_type,
    usage: str = "llm",
    json_mode: bool = True,
    chat_func=None,
    chat_json_func=None,
) -> dict[str, Any]:
    """Call the project LLM gateway for a JSON object and raise a domain error.

    Runtime stages should keep their domain-specific exception class, but they should
    not each reimplement JSON-mode retry, parser preview, or package-level chat
    injection.
    """
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]
    return call_stage_messages_json(
        messages=messages,
        timeout=timeout,
        error_type=error_type,
        usage=usage,
        json_mode=json_mode,
        chat_func=chat_func,
        chat_json_func=chat_json_func,
    )


def call_stage_messages_json(
    *,
    messages: list[dict[str, Any]],
    timeout: int,
    error_type,
    usage: str = "llm",
    json_mode: bool = True,
    chat_func=None,
    chat_json_func=None,
) -> dict[str, Any]:
    """Call the project LLM gateway for JSON using pre-built messages."""
    try:
        chat_func = chat_func or llms.chat
        chat_json_func = chat_json_func or llms.chat_json
        return chat_json_func(
            messages,
            usage=usage,
            timeout=timeout,
            json_mode=json_mode,
            _chat=chat_func,
        )
    except llms.ChatJSONError as exc:
        raise error_type(f"LLM 输出无法解析为 JSON: {exc.preview!r}") from exc
    except Exception as exc:  # noqa: BLE001
        raise error_type(f"llms.chat 失败: {type(exc).__name__}: {exc}") from exc


def try_stage_json(
    *,
    system: str,
    user: str,
    timeout: int | None = None,
    usage: str = "llm",
    json_mode: bool = True,
    chat_func=None,
    chat_json_func=None,
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    """Call a JSON LLM stage for flows that must keep deterministic fallback."""
    return try_stage_messages_json(
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        timeout=timeout,
        usage=usage,
        json_mode=json_mode,
        chat_func=chat_func,
        chat_json_func=chat_json_func,
    )


def try_stage_messages_json(
    *,
    messages: list[dict[str, Any]],
    timeout: int | None = None,
    usage: str = "llm",
    json_mode: bool = True,
    chat_func=None,
    chat_json_func=None,
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    """Call optional JSON LLM stages using pre-built messages and fallback metadata."""
    chat_func = chat_func or llms.chat
    chat_json_func = chat_json_func or llms.chat_json
    kwargs: dict[str, Any] = {
        "usage": usage,
        "json_mode": json_mode,
        "_chat": chat_func,
    }
    if timeout is not None:
        kwargs["timeout"] = timeout
    try:
        data = chat_json_func(messages, **kwargs)
    except llms.ChatJSONError as exc:
        return None, {
            "reason": chat_json_error_reason(exc),
            "error_type": "ChatJSONError",
            "preview": exc.preview,
        }
    except Exception as exc:  # noqa: BLE001
        return None, {
            "reason": "api_error",
            "error_type": type(exc).__name__,
            "message": str(exc)[:200],
        }
    return data, None


def attach_llm_error(target: dict[str, Any], stage: str, error: dict[str, Any]) -> None:
    """Attach a redacted optional-LLM failure using the shared field shape."""
    target["llm_error"] = {
        **dict(error),
        "stage": stage,
    }


__all__ = [
    "attach_llm_error",
    "call_stage_json",
    "call_stage_messages_json",
    "try_stage_json",
    "try_stage_messages_json",
]
