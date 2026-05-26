"""Small normalization primitives shared by runtime agents."""
from __future__ import annotations

from typing import Any, Iterable


def mapping(value: Any) -> dict[str, Any]:
    """Return a shallow copy when value is a dict, otherwise an empty mapping."""
    return dict(value) if isinstance(value, dict) else {}


def string_list(
    value: Any,
    fallback: Iterable[str] | None = None,
    *,
    limit: int | None = None,
) -> list[str]:
    """Normalize a scalar or list-like value into a stripped string list."""
    if isinstance(value, str):
        items = [value]
    elif isinstance(value, list):
        items = [str(item) for item in value if item is not None]
    else:
        items = list(fallback or [])
    output = [item.strip() for item in items if item.strip()]
    if not output and fallback is not None:
        output = [str(item).strip() for item in fallback if str(item).strip()]
    if limit is not None:
        return output[:limit]
    return output


def dedupe_preserve_order(items: Iterable[str]) -> list[str]:
    """Return items without repeats while preserving the original order."""
    seen: set[str] = set()
    output: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        output.append(item)
    return output


def int_value(value: Any, *, default: int) -> int:
    """Coerce value to int, rejecting bool because bool is an int subclass."""
    if isinstance(value, bool):
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def bounded_int(value: Any, *, default: int, minimum: int, maximum: int) -> int:
    """Coerce value to int and clamp it into an inclusive range."""
    number = int_value(value, default=default)
    return min(max(number, minimum), maximum)


def milestone_rows(
    value: Any,
    fallback: list[dict[str, Any]],
    *,
    horizon_days: int,
    limit: int = 5,
) -> list[dict[str, Any]]:
    """Normalize LLM milestone rows into day/target records."""
    rows = value if isinstance(value, list) else []
    output: list[dict[str, Any]] = []
    max_day = max(1, horizon_days)
    for row in rows[:limit]:
        if not isinstance(row, dict):
            continue
        day = bounded_int(row.get("day"), default=1, minimum=1, maximum=max_day)
        target = str(row.get("target") or row.get("name") or "").strip()
        if target:
            output.append({"day": day, "target": target})
    return output or list(fallback)


__all__ = [
    "bounded_int",
    "dedupe_preserve_order",
    "int_value",
    "mapping",
    "milestone_rows",
    "string_list",
]
