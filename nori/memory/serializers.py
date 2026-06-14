"""Serialization helpers for memory payloads."""
from __future__ import annotations

from typing import Any


def to_memory_dict(value: Any) -> dict[str, Any]:
    if hasattr(value, "to_dict"):
        data = value.to_dict()
        return data if isinstance(data, dict) else {}
    return dict(value) if isinstance(value, dict) else {}
