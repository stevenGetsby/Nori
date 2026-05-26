"""Public runtime contracts shared by Nori core and the LLM gateway."""
from __future__ import annotations

from dataclasses import dataclass as _stdlib_dataclass
from dataclasses import field as _stdlib_field
from typing import Any, Optional

from nori._compat import dataclass, field
from nori.shared.normalization import int_value as _shared_int_value
from nori.shared.normalization import mapping as _shared_mapping


@_stdlib_dataclass
class ProviderConfig:
    id: str
    base_url: str
    api_key: str
    api_key_env: str = ""


@_stdlib_dataclass
class ModelConfig:
    key: str
    provider_id: str
    model_id: str
    type: str
    name: str = ""
    context_window: int = 0
    max_output: int = 4096
    supports_vision: bool = False
    supports_thinking: bool = False
    temperature_fixed: Optional[float] = None
    extra_body: dict = _stdlib_field(default_factory=dict)
    resolution_options: list[str] = _stdlib_field(default_factory=list)
    supports_reference_image: bool = False
    duration_options: list[int] = _stdlib_field(default_factory=list)
    supports_audio: bool = False


@_stdlib_dataclass
class ResolvedModel:
    key: str
    provider_id: str
    model_id: str
    type: str
    name: str
    api_key: str
    base_url: str
    context_window: int = 0
    max_output: int = 4096
    supports_vision: bool = False
    supports_thinking: bool = False
    temperature_fixed: Optional[float] = None
    extra_body: dict = _stdlib_field(default_factory=dict)
    resolution_options: list[str] = _stdlib_field(default_factory=list)
    supports_reference_image: bool = False
    duration_options: list[int] = _stdlib_field(default_factory=list)
    supports_audio: bool = False


class LLMClientConfigError(ValueError):
    """Raised when an active model cannot build a provider client."""


class ChatJSONError(ValueError):
    """Raised when a chat response cannot be parsed as a JSON object."""

    def __init__(self, message: str, raw: str | None = None) -> None:
        super().__init__(message)
        self.raw = raw or ""

    @property
    def preview(self) -> str:
        return self.raw[:200]


class ChatResultError(ValueError):
    """Raised when a chat provider response contains no usable text content."""


class ChatCapabilityError(ValueError):
    """Raised when a chat request asks for unsupported model capabilities."""


class ImageCapabilityError(ValueError):
    """Raised when an image request asks for unsupported model capabilities."""


class ImageResultError(ValueError):
    """Raised when an image provider response contains no usable image result."""


@dataclass(slots=True)
class StructuredCallResult:
    data: dict[str, Any] | None = None
    raw: str = ""
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.error is None and self.data is not None


@dataclass(slots=True)
class IntentLLMResult:
    """LLM intent extraction result."""

    fields: dict[str, str] = field(default_factory=dict)
    candidates: dict[str, list[str]] = field(default_factory=dict)
    raw: str = ""
    model: str | None = None
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.error is None and bool(self.fields)


@dataclass(slots=True)
class TargetSelectionResult:
    """LLM edit-target selection result."""

    target_selector: str | None = None
    refined_instruction: str | None = None
    alternatives: list[str] = field(default_factory=list)
    confidence: str = "low"
    reason: str | None = None
    raw: str = ""
    model: str | None = None
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.error is None and self.target_selector is not None


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


__all__ = [
    "ChatCapabilityError",
    "ChatJSONError",
    "ChatResultError",
    "ImageCapabilityError",
    "ImageResultError",
    "IntentLLMResult",
    "LLMClientConfigError",
    "ModelConfig",
    "ProviderConfig",
    "ResolvedModel",
    "StructuredCallResult",
    "TargetSelectionResult",
    "bool_value",
    "dict_list",
    "float_value",
    "int_list",
    "int_value",
    "mapping",
    "mapping_list",
    "optional_str",
    "string_list",
]
