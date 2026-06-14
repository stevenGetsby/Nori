"""Shared JSON LLM call utilities for Nori runtime stages."""
from __future__ import annotations

from typing import Any

import nori.core.llms as llms


def call_stage_json(
    *,
    system: str,
    user: str,
    timeout: int,
    error_type,
    usage: str = "llm",
    json_mode: bool = True,
    retry_max_tokens: int | None = 8192,
    retry_transient_errors: int = 1,
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
        retry_max_tokens=retry_max_tokens,
        retry_transient_errors=retry_transient_errors,
        chat_json_func=chat_json_func,
    )


def call_stage_messages_json(
    *,
    messages: list[dict[str, Any]],
    timeout: int,
    error_type,
    usage: str = "llm",
    json_mode: bool = True,
    retry_max_tokens: int | None = 8192,
    retry_transient_errors: int = 1,
    chat_json_func=None,
) -> dict[str, Any]:
    """Call the project LLM gateway for JSON using pre-built messages."""
    chat_json_func = chat_json_func or llms.chat_json
    try:
        return _call_chat_json(
            chat_json_func,
            messages,
            usage=usage,
            timeout=timeout,
            json_mode=json_mode,
        )
    except llms.ChatJSONError as exc:
        if retry_max_tokens and _should_retry_json_parse(exc):
            try:
                return _call_chat_json(
                    chat_json_func,
                    messages,
                    usage=usage,
                    timeout=timeout,
                    json_mode=json_mode,
                    max_tokens=retry_max_tokens,
            )
            except llms.ChatJSONError as retry_exc:
                raise error_type(f"LLM 输出无法解析为 JSON: {retry_exc.preview!r}") from retry_exc
        raise error_type(f"LLM 输出无法解析为 JSON: {exc.preview!r}") from exc
    except Exception as exc:  # noqa: BLE001
        if retry_transient_errors > 0 and _is_transient_connection_error(exc):
            try:
                return _call_chat_json(
                    chat_json_func,
                    messages,
                    usage=usage,
                    timeout=timeout,
                    json_mode=json_mode,
                )
            except llms.ChatJSONError as retry_json_exc:
                raise error_type(f"LLM 输出无法解析为 JSON: {retry_json_exc.preview!r}") from retry_json_exc
            except Exception as retry_exc:  # noqa: BLE001
                raise error_type(
                    f"llms.chat_json 失败: {type(retry_exc).__name__}: {retry_exc}"
                ) from retry_exc
        raise error_type(f"llms.chat_json 失败: {type(exc).__name__}: {exc}") from exc


def _call_chat_json(
    chat_json_func,
    messages: list[dict[str, Any]],
    *,
    usage: str,
    timeout: int,
    json_mode: bool,
    max_tokens: int | None = None,
) -> dict[str, Any]:
    kwargs: dict[str, Any] = {
        "usage": usage,
        "timeout": timeout,
        "json_mode": json_mode,
    }
    if max_tokens:
        kwargs["max_tokens"] = max_tokens
    return chat_json_func(messages, **kwargs)


def _should_retry_json_parse(exc: llms.ChatJSONError) -> bool:
    raw = exc.raw.strip()
    if not raw:
        return False
    return raw.count("{") != raw.count("}") or raw.count("[") != raw.count("]") or len(raw) > 120


def _is_transient_connection_error(exc: Exception) -> bool:
    return type(exc).__name__ in {"APIConnectionError", "APITimeoutError"} or isinstance(
        exc,
        (ConnectionError, TimeoutError),
    )


def _chat_json_error_reason(exc: llms.ChatJSONError) -> str:
    return "empty_response" if not exc.raw.strip() else "parse_error"


def try_stage_json(
    *,
    system: str,
    user: str,
    timeout: int | None = None,
    usage: str = "llm",
    json_mode: bool = True,
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
        chat_json_func=chat_json_func,
    )


def try_stage_messages_json(
    *,
    messages: list[dict[str, Any]],
    timeout: int | None = None,
    usage: str = "llm",
    json_mode: bool = True,
    chat_json_func=None,
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    """Call optional JSON LLM stages using pre-built messages and fallback metadata."""
    chat_json_func = chat_json_func or llms.chat_json
    kwargs: dict[str, Any] = {
        "usage": usage,
        "json_mode": json_mode,
    }
    if timeout is not None:
        kwargs["timeout"] = timeout
    try:
        data = chat_json_func(messages, **kwargs)
    except llms.ChatJSONError as exc:
        return None, {
            "reason": _chat_json_error_reason(exc),
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
