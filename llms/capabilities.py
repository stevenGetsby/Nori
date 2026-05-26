"""Capability guards for LLM gateway model requests."""
from __future__ import annotations

from typing import Any

from .errors import ChatCapabilityError, ImageCapabilityError


def ensure_image_capability(model: Any, ref_bytes_list: list[bytes]) -> None:
    """Validate an image request before provider dispatch."""

    if getattr(model, "type", "image") != "image":
        raise ImageCapabilityError(
            f"active image model {getattr(model, 'key', '')!r} has type "
            f"{getattr(model, 'type', '')!r}; expected type='image'"
        )
    if ref_bytes_list and not getattr(model, "supports_reference_image", False):
        raise ImageCapabilityError(
            f"active image model {model.key!r} does not support reference_images; "
            "set models.<key>.supports_reference_image=true or switch active_models.image"
        )


def ensure_chat_capability(model: Any, messages: list[dict[str, Any]], usage: str) -> None:
    """Validate a chat request before provider dispatch."""

    model_type = getattr(model, "type", "llm")
    if model_type not in {"llm", "vision"}:
        raise ChatCapabilityError(
            f"active chat model {getattr(model, 'key', '')!r} has type {model_type!r}; "
            "expected type='llm' or type='vision'"
        )
    if (usage == "vision" or messages_need_vision(messages)) and not getattr(model, "supports_vision", False):
        raise ChatCapabilityError(
            f"active chat model {getattr(model, 'key', '')!r} does not support vision messages; "
            "set supports_vision=true or switch active model"
        )


def messages_need_vision(messages: list[dict[str, Any]]) -> bool:
    """Return whether OpenAI-style messages contain image parts."""

    for message in messages or []:
        content = message.get("content") if isinstance(message, dict) else None
        if not isinstance(content, list):
            continue
        for part in content:
            if not isinstance(part, dict):
                continue
            part_type = str(part.get("type") or "")
            if part_type in {"image_url", "input_image", "image"}:
                return True
            if part.get("image_url") or part.get("image"):
                return True
    return False
