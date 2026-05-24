"""统一 API 配置加载器。"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

import yaml


def parse_model_key(key: str) -> tuple[str, str]:
    parts = key.split("::", 1)
    if len(parts) != 2:
        raise ValueError(f"无效模型键: {key}")
    return parts[0], parts[1]


@dataclass
class ProviderConfig:
    id: str
    base_url: str
    api_key: str


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


class NoriConfig:
    def __init__(self, config_path=None):
        self._providers = {}
        self._models = {}
        self._active = {}
        self._evolution = {}
        self._mode = "direct"
        self._raw = {}
        if config_path is None:
            config_path = self._find_config()
        if config_path and Path(config_path).is_file():
            self._load(Path(config_path))
        self._apply_env_overrides()

    def _find_config(self):
        for p in [
            Path(os.getenv("NORI_CONFIG", "")),
            Path.cwd() / "api_config.yaml",
            Path(__file__).parent / "api_config.yaml",
            Path(__file__).parent.parent / "api_config.yaml",
        ]:
            if p.is_file():
                return p
        return None

    def _load(self, path):
        with open(path, "r", encoding="utf-8") as f:
            self._raw = yaml.safe_load(f) or {}
        for pid, pd in self._raw.get("providers", {}).items():
            self._providers[pid] = ProviderConfig(id=pid, base_url=pd.get("base_url",""), api_key=pd.get("api_key",""))
        for mkey, md in self._raw.get("models", {}).items():
            pid, mid = parse_model_key(mkey)
            self._models[mkey] = ModelConfig(
                key=mkey, provider_id=pid, model_id=mid, type=md.get("type","llm"),
                name=md.get("name",mid), context_window=md.get("context_window",0),
                max_output=md.get("max_output",4096), supports_vision=md.get("supports_vision",False),
                supports_thinking=md.get("supports_thinking",False), temperature_fixed=md.get("temperature_fixed"),
                extra_body=md.get("extra_body",{}), resolution_options=md.get("resolution_options",[]),
                supports_reference_image=md.get("supports_reference_image",False),
                duration_options=md.get("duration_options",[]), supports_audio=md.get("supports_audio",False),
            )
        self._mode = str(self._raw.get("mode", "direct"))
        ar = self._raw.get("active_models", {})
        if self._mode in ar and isinstance(ar[self._mode], dict):
            self._active = dict(ar[self._mode])
        elif any(isinstance(v, dict) for v in ar.values()):
            self._active = dict(ar.get("direct", {}))
        else:
            self._active = dict(ar)
        self._evolution = dict(self._raw.get("evolution", {}))

    def _apply_env_overrides(self):
        em = os.getenv("NORI_MODE", "")
        if em:
            self._mode = em
            ar = self._raw.get("active_models", {})
            if self._mode in ar and isinstance(ar[self._mode], dict):
                self._active = dict(ar[self._mode])

    def get_active(self, usage):
        mk = self._active.get(usage)
        if not mk:
            raise KeyError(f"未配置 active_models.{usage}")
        return self.resolve(mk)

    def resolve(self, model_key):
        pid, mid = parse_model_key(model_key)
        prov = self._providers.get(pid)
        if not prov:
            raise KeyError(f"未配置服务商: {pid}")
        m = self._models.get(model_key)
        return ResolvedModel(
            key=model_key, provider_id=pid, model_id=mid,
            type=m.type if m else "llm", name=m.name if m else mid,
            api_key=prov.api_key, base_url=prov.base_url,
            context_window=m.context_window if m else 0,
            max_output=m.max_output if m else 4096,
            supports_vision=m.supports_vision if m else False,
            supports_thinking=m.supports_thinking if m else False,
            temperature_fixed=m.temperature_fixed if m else None,
            extra_body=dict(m.extra_body) if m else {},
            resolution_options=list(m.resolution_options) if m else [],
            supports_reference_image=m.supports_reference_image if m else False,
        )

    def get_provider(self, provider_id):
        p = self._providers.get(provider_id)
        if not p:
            raise KeyError(f"未配置服务商: {provider_id}")
        return p

    @property
    def mode(self):
        return self._mode

    @property
    def active_summary(self):
        return dict(self._active)

    def evolution_param(self, key, default=None):
        return self._evolution.get(key, default)


cfg = NoriConfig()
