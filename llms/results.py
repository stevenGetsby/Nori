"""Provider response normalization for LLM gateway calls."""
from __future__ import annotations

from typing import Any

from .errors import ChatResultError, ImageResultError


def extract_chat_text(resp: Any, model: Any) -> str:
    """Return the first usable chat text or raise a stable result error."""

    choices = response_value(resp, "choices")
    first_choice = None
    if choices:
        try:
            first_choice = choices[0]
        except (IndexError, KeyError, TypeError):
            first_choice = None
    message = response_value(first_choice, "message")
    return ensure_chat_text(response_value(message, "content"), model)


def response_value(value: Any, key: str) -> Any:
    if isinstance(value, dict):
        return value.get(key)
    return getattr(value, key, None)


def ensure_chat_text(content: Any, model: Any) -> str:
    text = str(content or "").strip()
    if text:
        return text
    raise ChatResultError(f"文本模型未返回可用文本: {getattr(model, 'key', '')}")


def collect_image_results(resp: Any) -> list[str]:
    """Collect image URLs/data URIs from an OpenAI-compatible response."""

    results: list[str] = []
    for item in getattr(resp, "data", []) or []:
        url = getattr(item, "url", None)
        if url:
            results.append(url)
            continue
        b64_json = getattr(item, "b64_json", None)
        if b64_json:
            results.append(f"data:image/png;base64,{b64_json}")
    return ensure_image_results(results)


def ensure_image_results(results: list[str], model: Any | None = None) -> list[str]:
    if results:
        return results
    model_key = getattr(model, "key", "") if model is not None else ""
    suffix = f": {model_key}" if model_key else ""
    raise ImageResultError(f"图片服务未返回可用图片{suffix}")
