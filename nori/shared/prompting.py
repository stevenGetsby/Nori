"""Prompt rendering helpers shared by runtime agents."""
from __future__ import annotations

import json
from typing import Any


def json_inline(value: Any) -> str:
    """Serialize prompt data as compact UTF-8 JSON."""
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def json_block(value: Any, *, indent: int = 2) -> str:
    """Serialize prompt data as pretty UTF-8 JSON."""
    return json.dumps(value, ensure_ascii=False, indent=indent)


def json_prompt(value: Any) -> str:
    """Serialize prompt data as readable one-line UTF-8 JSON."""
    return json.dumps(value, ensure_ascii=False)


def render_prompt(template: str, **values: Any) -> str:
    """Format a prompt template, JSON-serializing containers by default."""
    rendered = {
        key: json_inline(value) if isinstance(value, (dict, list)) else value
        for key, value in values.items()
    }
    return template.format(**rendered)


__all__ = ["json_block", "json_inline", "json_prompt", "render_prompt"]
