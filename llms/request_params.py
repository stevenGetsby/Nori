"""Request-parameter helpers for LLM gateway calls."""
from __future__ import annotations

from typing import Any


def merge_chat_kwargs(model: Any, kwargs: dict) -> dict:
    """Merge chat model constraints without mutating caller kwargs."""

    out = dict(kwargs)
    if model.temperature_fixed is not None:
        out["temperature"] = model.temperature_fixed
    max_output_param = max_output_param_name(model)
    if max_output_param == "max_completion_tokens":
        if "max_completion_tokens" in out:
            out.pop("max_tokens", None)
        elif "max_tokens" in out:
            out["max_completion_tokens"] = out.pop("max_tokens")
        elif model.max_output:
            out["max_completion_tokens"] = model.max_output
    else:
        if "max_tokens" in out:
            out.pop("max_completion_tokens", None)
        elif "max_completion_tokens" in out:
            out["max_tokens"] = out.pop("max_completion_tokens")
        elif model.max_output:
            out["max_tokens"] = model.max_output
    merge_model_extra_body(out, model)
    return out


def merge_image_kwargs(model: Any, kwargs: dict) -> dict:
    """Merge image-generation kwargs without chat-only token/temperature fields."""

    out = dict(kwargs)
    merge_model_extra_body(out, model)
    return out


def merge_model_extra_body(out: dict, model: Any) -> None:
    model_extra_body = getattr(model, "extra_body", {}) or {}
    if not model_extra_body:
        return
    caller_extra_body = out.get("extra_body") if isinstance(out.get("extra_body"), dict) else {}
    extra_body = dict(caller_extra_body)
    extra_body.update(model_extra_body)
    out["extra_body"] = extra_body


def max_output_param_name(model: Any) -> str:
    model_id = model.model_id.lower()
    if model_id.startswith("gpt-5"):
        return "max_completion_tokens"
    return "max_tokens"
