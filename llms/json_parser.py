"""JSON parsing helpers for LLM text responses."""
from __future__ import annotations

import json
import re
from typing import Any

from .errors import ChatJSONError


def parse_json_object(raw: str | None) -> dict[str, Any]:
    """Parse a model response into a JSON object, accepting fenced/embedded JSON."""

    text = (raw or "").strip()
    if not text:
        raise ChatJSONError("LLM 输出为空，无法解析为 JSON", raw or "")

    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
        text = re.sub(r"\n?```$", "", text).strip()

    parsed = _loads_json_object(text, raw or "")
    if parsed is not None:
        return parsed

    parsed = _loads_first_embedded_json_object(text, raw or "")
    if parsed is not None:
        return parsed

    raise ChatJSONError("LLM 输出无法解析为 JSON object", raw or "")


def _loads_json_object(text: str, raw: str) -> dict[str, Any] | None:
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return None
    if not isinstance(data, dict):
        raise ChatJSONError(f"LLM 输出 JSON 不是 object: {type(data).__name__}", raw)
    return data


def _loads_first_embedded_json_object(text: str, raw: str) -> dict[str, Any] | None:
    decoder = json.JSONDecoder()
    for index, char in enumerate(text):
        if char != "{":
            continue
        try:
            data, _end = decoder.raw_decode(text[index:])
        except json.JSONDecodeError:
            continue
        if not isinstance(data, dict):
            raise ChatJSONError(f"LLM 输出 JSON 不是 object: {type(data).__name__}", raw)
        return data
    return None
