"""Shared utilities for Nori runtime stages."""
from __future__ import annotations

from importlib import import_module
from typing import Final


_LAZY_EXPORTS: Final[dict[str, str]] = {
    "attach_llm_error": "llm_json",
    "bounded_int": "normalization",
    "call_stage_json": "llm_json",
    "call_stage_messages_json": "llm_json",
    "dedupe_preserve_order": "normalization",
    "image_to_bytes": "image_io",
    "image_to_data_uri": "image_io",
    "int_value": "normalization",
    "json_block": "prompting",
    "json_inline": "prompting",
    "json_prompt": "prompting",
    "mapping": "normalization",
    "milestone_rows": "normalization",
    "render_prompt": "prompting",
    "string_list": "normalization",
    "try_stage_json": "llm_json",
    "try_stage_messages_json": "llm_json",
    "write_stage_log": "case_log",
}


def __getattr__(name: str):
    module_name = _LAZY_EXPORTS.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module = import_module(f"{__name__}.{module_name}")
    value = getattr(module, name)
    globals()[name] = value
    return value


__all__ = list(_LAZY_EXPORTS)
