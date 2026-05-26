"""Small coercion helpers shared by provider-free data models."""
from __future__ import annotations

from typing import Any

from nori.shared.normalization import int_value as _shared_int_value
from nori.shared.normalization import mapping as _shared_mapping


def mapping(value: Any) -> dict[str, Any]:
    return _shared_mapping(value)


def mapping_list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [dict(item) for item in value if isinstance(item, dict)]


def dict_list(value: Any) -> list[dict[str, Any]]:
    return mapping_list(value)


def string_list(value: Any, *, drop_blank: bool = False) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        items = [value]
    elif isinstance(value, list):
        items = [str(item) for item in value]
    else:
        return []
    if drop_blank:
        return [item for item in items if item.strip()]
    return items


def optional_str(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value)
    return text if text else None


def int_value(value: Any, *, default: int = 0) -> int:
    return _shared_int_value(value, default=default)


def int_list(value: Any, *, drop_non_positive: bool = False) -> list[int]:
    if value is None:
        return []
    items = value if isinstance(value, list) else [value]
    values: list[int] = []
    for item in items:
        parsed = int_value(item, default=0)
        if drop_non_positive and parsed <= 0:
            continue
        values.append(parsed)
    return values


def float_value(value: Any, *, default: float | None = None) -> float | None:
    if isinstance(value, bool):
        return default
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def bool_value(value: Any, *, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"1", "true", "yes", "y", "on"}:
            return True
        if normalized in {"0", "false", "no", "n", "off", ""}:
            return False
        return default
    if isinstance(value, (int, float)):
        return bool(value)
    if value is None:
        return default
    return default
