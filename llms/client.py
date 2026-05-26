"""OpenAI 兼容客户端工厂。

职能：
  - 依据 usage → 激活模型 → 生成 OpenAI / AsyncOpenAI 客户端
  - 附带 model_id、max_output 等元信息供调用方使用

交接：
  - 上游：llms.config.get_active
  - 下游：llms.call、外部直接使用 openai SDK 的代码
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from openai import AsyncOpenAI, OpenAI

from nori.config_models import ResolvedModel

from .config import get_active
from .errors import LLMClientConfigError


@dataclass
class ClientBundle:
    """客户端 + 模型元信息。"""
    client: Any
    model: ResolvedModel

    @property
    def model_id(self) -> str:
        return self.model.model_id


def get_client(usage: str = "llm") -> ClientBundle:
    """同步客户端。"""
    model = get_active(usage)
    return build_client_bundle(model, usage)


def get_async_client(usage: str = "llm") -> ClientBundle:
    """异步客户端。"""
    model = get_active(usage)
    return build_async_client_bundle(model, usage)


def build_client_bundle(model: ResolvedModel, usage: str = "llm") -> ClientBundle:
    """Build a sync client bundle from an already-resolved model."""
    client_options = validate_client_config(model, usage)
    return ClientBundle(
        client=OpenAI(**client_options),
        model=model,
    )


def build_async_client_bundle(model: ResolvedModel, usage: str = "llm") -> ClientBundle:
    """Build an async client bundle from an already-resolved model."""
    client_options = validate_client_config(model, usage)
    return ClientBundle(
        client=AsyncOpenAI(**client_options),
        model=model,
    )


def validate_api_key(model: ResolvedModel, usage: str) -> str:
    """Return a trimmed API key or raise an explicit config error."""
    api_key = str(model.api_key or "").strip()
    if not api_key:
        raise LLMClientConfigError(
            f"{usage} 模型 {model.key} 的 api_key 为空，请检查 api_config.yaml"
        )
    return api_key


def validate_client_config(model: ResolvedModel, usage: str) -> dict[str, str]:
    """Return trimmed OpenAI client options or raise an explicit config error."""
    api_key = validate_api_key(model, usage)
    base_url = str(model.base_url or "").strip()
    if not base_url:
        raise LLMClientConfigError(
            f"{usage} 模型 {model.key} 的 base_url 为空，请检查 api_config.yaml"
        )
    return {"api_key": api_key, "base_url": base_url}


def _client_options(model: ResolvedModel, usage: str) -> dict[str, str]:
    return validate_client_config(model, usage)
