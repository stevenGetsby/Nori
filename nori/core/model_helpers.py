"""Small normalization helpers shared by core model owner modules."""
from __future__ import annotations

from typing import Any

from nori.core.contracts import mapping_list as _mapping_list


def dict_rows(values: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [dict(value) for value in values if isinstance(value, dict)]


def stage_rows(values: Any) -> list[dict[str, Any]]:
    rows = _mapping_list(values)
    for row in rows:
        if "stage" not in row and "agent" in row:
            row["stage"] = row.pop("agent")
    return rows


def float_value(value: Any) -> float:
    if isinstance(value, bool):
        return 0.0
    try:
        return float(value or 0.0)
    except (TypeError, ValueError):
        return 0.0


__all__ = ["dict_rows", "float_value", "stage_rows"]
