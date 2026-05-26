"""Pure normalization helpers for Nori runtime configuration."""
from __future__ import annotations

import os
from typing import Any


class NoriConfigError(ValueError):
    """Raised when api_config.yaml has an invalid structural shape."""


def parse_model_key(key: str) -> tuple[str, str]:
    key = str(key or "").strip()
    parts = key.split("::", 1)
    if len(parts) != 2 or not parts[0].strip() or not parts[1].strip():
        raise ValueError(f"无效模型键: {key}")
    return parts[0].strip(), parts[1].strip()


def format_model_key(provider_id: str, model_id: str) -> str:
    return f"{provider_id.strip()}::{model_id.strip()}"


def format_provider_id(provider_id: str) -> str:
    provider_id = str(provider_id or "").strip()
    if not provider_id:
        raise ValueError("无效服务商 id")
    return provider_id


def resolve_api_key(raw_value: Any, env_name_value: str = "") -> str:
    name = env_name(env_name_value)
    if name:
        env_value = os.getenv(name, "")
        if env_value:
            return env_value
    value = str(raw_value or "")
    if value.startswith("${") and value.endswith("}"):
        return os.getenv(env_name(value[2:-1]), "")
    return value


def env_name(value: Any) -> str:
    return str(value or "").strip()


def config_section_mapping(value: Any, section: str) -> dict[str, Any]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise NoriConfigError(f"api_config.yaml.{section} 必须是 mapping")
    return value


def config_entry_mapping(value: Any, section: str, key: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise NoriConfigError(f"api_config.yaml.{section}.{key} 必须是 mapping")
    return value


def active_model_map(value: Any) -> dict[str, str]:
    if not isinstance(value, dict):
        return {}
    active: dict[str, str] = {}
    for usage, model_key in value.items():
        usage_text = str(usage or "").strip()
        if model_key is None:
            continue
        model_key_text = str(model_key).strip()
        if usage_text and model_key_text:
            try:
                active[usage_text] = format_model_key(*parse_model_key(model_key_text))
            except ValueError:
                active[usage_text] = model_key_text
    return active


def keyed_mapping(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        return {}
    result: dict[str, Any] = {}
    for key, item in value.items():
        text = str(key or "").strip()
        if text:
            result[text] = item
    return result


def mode_key(value: Any, *, default: str = "") -> str:
    text = str(value or "").strip()
    return text or default


def select_active_models(
    active_models: Any,
    mode: str,
    *,
    fallback_mode: str | None,
) -> dict[str, str]:
    active_models = keyed_mapping(active_models)
    selected_mode = mode_key(mode)
    fallback = mode_key(fallback_mode) if fallback_mode is not None else None
    mode_block = active_models.get(selected_mode)
    if isinstance(mode_block, dict):
        return active_model_map(mode_block)
    if any(isinstance(value, dict) for value in active_models.values()):
        if fallback is None:
            return {}
        return active_model_map(active_models.get(fallback))
    return active_model_map(active_models)


__all__ = [
    "NoriConfigError",
    "active_model_map",
    "config_entry_mapping",
    "config_section_mapping",
    "env_name",
    "format_model_key",
    "format_provider_id",
    "keyed_mapping",
    "mode_key",
    "parse_model_key",
    "resolve_api_key",
    "select_active_models",
]
