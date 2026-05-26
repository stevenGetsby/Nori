"""Runtime configuration dataclass contracts shared by nori and llms."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ProviderConfig:
    id: str
    base_url: str
    api_key: str
    api_key_env: str = ""


@dataclass
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
    extra_body: dict = field(default_factory=dict)
    resolution_options: list[str] = field(default_factory=list)
    supports_reference_image: bool = False
    duration_options: list[int] = field(default_factory=list)
    supports_audio: bool = False


@dataclass
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
    extra_body: dict = field(default_factory=dict)
    resolution_options: list[str] = field(default_factory=list)
    supports_reference_image: bool = False
    duration_options: list[int] = field(default_factory=list)
    supports_audio: bool = False


__all__ = ["ProviderConfig", "ModelConfig", "ResolvedModel"]
