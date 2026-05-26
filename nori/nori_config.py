"""统一 API 配置加载器。"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml

from nori.config_models import ModelConfig, ProviderConfig, ResolvedModel
from nori.config_normalization import (
    NoriConfigError,
    active_model_map as _active_model_map,
    config_entry_mapping as _config_entry_mapping,
    config_section_mapping as _config_section_mapping,
    env_name as _env_name,
    format_model_key,
    format_provider_id,
    keyed_mapping as _keyed_mapping,
    mode_key as _mode_key,
    parse_model_key,
    resolve_api_key as _resolve_api_key,
    select_active_models as _select_active_models,
)
from nori._model_coercion import (
    bool_value as _bool,
    float_value as _float,
    int_list as _int_list,
    int_value as _int,
    mapping as _mapping,
    string_list as _string_list,
)


class NoriConfig:
    def __init__(self, config_path=None):
        self._providers = {}
        self._models = {}
        self._active = {}
        self._evolution = {}
        self._mode = "direct"
        self._raw = {}
        self._config_path = None
        if config_path is None:
            config_path = self._find_config()
        if config_path and Path(config_path).is_file():
            self._config_path = Path(config_path)
            self._load(self._config_path)
        self._apply_env_overrides()

    def _find_config(self):
        env_path = os.getenv("NORI_CONFIG", "").strip()
        if env_path:
            p = Path(env_path).expanduser()
            if p.is_file():
                return p
            raise FileNotFoundError(f"NORI_CONFIG 指向的配置文件不存在: {p}")
        for p in [
            Path.cwd() / "api_config.yaml",
            Path(__file__).parent / "api_config.yaml",
            Path(__file__).parent.parent / "api_config.yaml",
        ]:
            if p.is_file():
                return p
        return None

    def _load(self, path):
        with open(path, "r", encoding="utf-8") as f:
            raw = yaml.safe_load(f) or {}
        if not isinstance(raw, dict):
            raise NoriConfigError("api_config.yaml 顶层必须是 mapping")
        self._raw = raw
        for pid, pd in _config_section_mapping(self._raw.get("providers"), "providers").items():
            provider_id = format_provider_id(pid)
            pd = _config_entry_mapping(pd, "providers", provider_id)
            api_key_env = _env_name(pd.get("api_key_env"))
            api_key = _resolve_api_key(pd.get("api_key"), api_key_env)
            self._providers[provider_id] = ProviderConfig(
                id=provider_id,
                base_url=str(pd.get("base_url") or ""),
                api_key=api_key,
                api_key_env=api_key_env,
            )
        for mkey, md in _config_section_mapping(self._raw.get("models"), "models").items():
            pid, mid = parse_model_key(mkey)
            normalized_key = format_model_key(pid, mid)
            md = _config_entry_mapping(md, "models", normalized_key)
            self._models[normalized_key] = ModelConfig(
                key=normalized_key,
                provider_id=pid,
                model_id=mid,
                type=str(md.get("type") or "llm"),
                name=str(md.get("name") or mid),
                context_window=_int(md.get("context_window"), default=0),
                max_output=_int(md.get("max_output"), default=4096),
                supports_vision=_bool(md.get("supports_vision")),
                supports_thinking=_bool(md.get("supports_thinking")),
                temperature_fixed=_float(md.get("temperature_fixed")),
                extra_body=_mapping(md.get("extra_body")),
                resolution_options=_string_list(md.get("resolution_options")),
                supports_reference_image=_bool(md.get("supports_reference_image")),
                duration_options=_int_list(md.get("duration_options"), drop_non_positive=True),
                supports_audio=_bool(md.get("supports_audio")),
            )
        self._mode = _mode_key(self._raw.get("mode"), default="direct")
        self._active = _select_active_models(
            self._raw.get("active_models", {}),
            self._mode,
            fallback_mode="direct",
        )
        self._evolution = _mapping(self._raw.get("evolution"))

    def _apply_env_overrides(self):
        em = os.getenv("NORI_MODE", "").strip()
        if em:
            self._mode = em
            self._active = _select_active_models(
                self._raw.get("active_models", {}),
                self._mode,
                fallback_mode=None,
            )

    def get_active(self, usage):
        usage = str(usage or "").strip()
        mk = self._active.get(usage)
        if not mk:
            raise KeyError(f"未配置 active_models.{usage}")
        return self.resolve(mk)

    def resolve(self, model_key):
        pid, mid = parse_model_key(model_key)
        normalized_key = format_model_key(pid, mid)
        prov = self._providers.get(pid)
        if not prov:
            raise KeyError(f"未配置服务商: {pid}")
        m = self._models.get(normalized_key)
        if not m:
            raise KeyError(f"未配置模型: {normalized_key}")
        return ResolvedModel(
            key=normalized_key, provider_id=pid, model_id=mid,
            type=m.type, name=m.name,
            api_key=prov.api_key, base_url=prov.base_url,
            context_window=m.context_window,
            max_output=m.max_output,
            supports_vision=m.supports_vision,
            supports_thinking=m.supports_thinking,
            temperature_fixed=m.temperature_fixed,
            extra_body=dict(m.extra_body),
            resolution_options=list(m.resolution_options),
            supports_reference_image=m.supports_reference_image,
            duration_options=list(m.duration_options),
            supports_audio=m.supports_audio,
        )

    def get_provider(self, provider_id):
        normalized_provider_id = format_provider_id(provider_id)
        p = self._providers.get(normalized_provider_id)
        if not p:
            raise KeyError(f"未配置服务商: {normalized_provider_id}")
        return p

    @property
    def mode(self):
        return self._mode

    @property
    def active_summary(self):
        return dict(self._active)

    @property
    def config_path(self):
        return str(self._config_path) if self._config_path else ""

    def evolution_param(self, key, default=None):
        return self._evolution.get(key, default)


cfg = NoriConfig()
