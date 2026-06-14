"""Capability guards for LLM gateway model requests."""
from __future__ import annotations

from typing import Any

from langchain_core.messages.utils import convert_to_openai_messages

from nori.core.contracts import ChatCapabilityError, ImageCapabilityError


def ensure_image_capability(
    model: Any,
    ref_bytes_list: list[bytes] | None = None,
    ref_urls: list[str] | None = None,
) -> None:
    """Validate an image request before provider dispatch."""

    has_references = bool(ref_bytes_list) or bool(ref_urls)
    if getattr(model, "type", "image") != "image":
        raise ImageCapabilityError(
            f"active image model {getattr(model, 'key', '')!r} has type "
            f"{getattr(model, 'type', '')!r}; expected type='image'"
        )
    if has_references and not getattr(model, "supports_reference_image", False):
        raise ImageCapabilityError(
            f"active image model {model.key!r} does not support reference_images; "
            "set models.<key>.supports_reference_image=true or switch active_models.image"
        )


def ensure_chat_capability(model: Any, messages: list[Any], usage: str) -> None:
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


def messages_need_vision(messages: list[Any]) -> bool:
    """Return whether LangChain/OpenAI-style messages contain image parts."""

    for message in normalize_chat_messages(messages):
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


def normalize_chat_messages(messages: list[Any] | None) -> list[dict[str, Any]]:
    """Normalize LangChain message objects and dicts to OpenAI-style messages."""

    normalized_inputs = [_normalize_message_input(message) for message in messages or []]
    return list(convert_to_openai_messages(normalized_inputs))


def _normalize_message_input(message: Any) -> Any:
    if not isinstance(message, dict):
        return message
    content = message.get("content")
    if not isinstance(content, list):
        return dict(message)
    out = dict(message)
    out["content"] = [_normalize_content_block(block) for block in content]
    return out


def _normalize_content_block(block: Any) -> Any:
    if not isinstance(block, dict) or block.get("type"):
        return block
    if block.get("image_url"):
        return {"type": "image_url", **block}
    if block.get("image"):
        return {"type": "image", **block}
    return block
