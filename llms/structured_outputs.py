"""Shared normalization helpers for structured LLM utility outputs."""
from __future__ import annotations

from typing import Any

from .errors import ChatJSONError


def clean_str(value: Any) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        value = str(value)
    text = value.strip().strip("'\"").strip()
    if not text:
        return None
    if text.lower() in {"null", "none", "n/a", "未知"}:
        return None
    return text


def chat_json_error_reason(exc: ChatJSONError) -> str:
    return "empty_response" if not exc.raw.strip() else "parse_error"


def normalize_field_value(
    node: Any,
    *,
    allowed: list[str] | None,
    max_candidates: int,
) -> tuple[str | None, list[str]]:
    """Normalize an LLM field node into a primary value and alternative candidates."""
    value: str | None = None
    candidates: list[str] = []

    if node is None:
        return None, []

    if isinstance(node, str):
        value = node
    elif isinstance(node, dict):
        raw_value = node.get("value")
        if isinstance(raw_value, str):
            value = raw_value
        elif isinstance(raw_value, list) and raw_value:
            value = str(raw_value[0]) if raw_value[0] is not None else None
            candidates.extend(str(item) for item in raw_value[1:] if item)
        raw_candidates = node.get("candidates")
        if isinstance(raw_candidates, list):
            candidates.extend(str(item) for item in raw_candidates if item)
    elif isinstance(node, list):
        items = [str(item) for item in node if item]
        if items:
            value = items[0]
            candidates.extend(items[1:])

    value = clean_str(value)
    candidates = [item for item in (clean_str(candidate) or "" for candidate in candidates) if item]

    if allowed is not None:
        allowed_set = set(allowed)
        if value is not None and value not in allowed_set:
            value = None
        candidates = [candidate for candidate in candidates if candidate in allowed_set]

    seen: set[str] = set()
    deduped: list[str] = []
    if value:
        seen.add(value)
        deduped.append(value)
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        deduped.append(candidate)
        if len(deduped) - (1 if value else 0) >= max_candidates:
            break

    final_candidates = [candidate for candidate in deduped if candidate != value]
    return value, final_candidates


def normalize_selector_options(options: list[dict[str, Any]]) -> list[dict[str, str]]:
    """Clean and dedupe target-selector option rows."""
    seen: set[str] = set()
    cleaned: list[dict[str, str]] = []
    for raw in options or []:
        if not isinstance(raw, dict):
            continue
        selector = clean_str(raw.get("selector"))
        if not selector or selector in seen:
            continue
        seen.add(selector)
        cleaned.append(
            {
                "selector": selector,
                "role": clean_str(raw.get("role")) or "",
                "kind": clean_str(raw.get("kind")) or "",
                "summary": clean_str(raw.get("summary")) or "",
            }
        )
    return cleaned


def normalize_confidence(value: Any) -> str:
    confidence = clean_str(value) or "low"
    if confidence not in ("high", "medium", "low"):
        return "low"
    return confidence


def normalize_selector_alternatives(
    value: Any,
    *,
    selector_set: set[str],
    target: str,
    max_alternatives: int,
) -> list[str]:
    alternatives: list[str] = []
    if not isinstance(value, list):
        return alternatives
    for item in value:
        selector = clean_str(item)
        if selector and selector in selector_set and selector != target and selector not in alternatives:
            alternatives.append(selector)
        if len(alternatives) >= max_alternatives:
            break
    return alternatives
