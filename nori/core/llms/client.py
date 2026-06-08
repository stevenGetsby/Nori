"""LLM runtime config, readiness checks, and provider client factories.

职能：
  - 复用 NoriConfig，按 usage 解析激活模型
  - 切换 direct / ghc 并做 readiness 预检
  - 依据 usage → 激活模型 → 生成 OpenAI / AsyncOpenAI 客户端
  - 为文本 chat 生成 LangChain chat model adapter
  - 附带 model_id、max_output 等元信息供调用方使用
"""
from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Any
from typing import Literal

import httpx
from langchain.chat_models import init_chat_model
from openai import AsyncOpenAI, OpenAI

from nori.config_normalization import mode_key
from nori.core.contracts import LLMClientConfigError as _LLMClientConfigError
from nori.core.contracts import ResolvedModel
from nori.nori_config import NoriConfig, cfg as _default_cfg


Mode = Literal["direct", "ghc"]
_cfg: NoriConfig = _default_cfg

@dataclass
class ClientBundle:
    """客户端 + 模型元信息。"""
    client: Any
    model: ResolvedModel

    @property
    def model_id(self) -> str:
        return self.model.model_id


class NoriAIClient:
    """Aggregate project AI gateway with separate LM and image clients."""

    def __init__(
        self,
        *,
        lm: Any | None = None,
        imager: Any | None = None,
    ) -> None:
        if lm is None:
            from .lm import LanguageModelClient

            lm = LanguageModelClient()
        if imager is None:
            from .imager import ImageClient

            imager = ImageClient()
        self.lm = lm
        self.imager = imager

    def chat(
        self,
        messages: list[dict[str, Any]],
        *,
        usage: str = "llm",
        **kwargs: Any,
    ) -> str:
        return self.lm.chat(messages, usage=usage, **kwargs)

    async def achat(
        self,
        messages: list[dict[str, Any]],
        *,
        usage: str = "llm",
        **kwargs: Any,
    ) -> str:
        return await self.lm.achat(messages, usage=usage, **kwargs)

    def chat_json(
        self,
        messages: list[dict[str, Any]],
        *,
        usage: str = "llm",
        **kwargs: Any,
    ) -> dict[str, Any]:
        return self.lm.chat_json(messages, usage=usage, **kwargs)

    def image(
        self,
        prompt: str,
        *,
        usage: str = "image",
        **kwargs: Any,
    ) -> list[str]:
        return self.imager.image(prompt, usage=usage, **kwargs)


_default_ai_client: NoriAIClient | None = None


def get_default_client() -> NoriAIClient:
    """Return the process-local aggregate AI gateway."""
    global _default_ai_client
    if _default_ai_client is None:
        _default_ai_client = NoriAIClient()
    return _default_ai_client


def get_config() -> NoriConfig:
    """Return the process-local runtime config singleton."""
    return _cfg


def _reload_config() -> NoriConfig:
    global _cfg
    _cfg = NoriConfig()
    return _cfg


def get_active(usage: str = "llm") -> ResolvedModel:
    """Return the active model for a usage key under the current runtime mode."""
    return _cfg.get_active(usage)


def resolve(model_key: str) -> ResolvedModel:
    """Resolve a provider::model key into a complete model config."""
    return _cfg.resolve(model_key)


def current_mode() -> str:
    """Return the active runtime mode, preferring NORI_MODE over yaml config."""
    return mode_key(os.getenv("NORI_MODE")) or mode_key(get_config().mode)


def set_mode(mode: Mode | str) -> str:
    """Switch direct/ghc runtime mode and reload config."""
    mode = mode_key(mode)
    if mode not in ("direct", "ghc"):
        raise ValueError(f"非法 mode: {mode}")
    os.environ["NORI_MODE"] = mode
    _reload_config()
    return current_mode()


def ensure_ready(usage: str = "llm", timeout: float = 3.0) -> None:
    """Validate config and preflight the local GHC proxy when needed."""
    model = get_active(usage)
    client_options = validate_client_config(model, usage)
    if current_mode() != "ghc":
        return

    url = f"{client_options['base_url'].rstrip('/')}/models"
    try:
        response = httpx.get(
            url,
            headers={"Authorization": f"Bearer {client_options['api_key']}"},
            timeout=timeout,
        )
        response.raise_for_status()
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(
            f"ghc 代理不可用: {url} ({exc}). "
            f"请先启动 ghc-api: "
            f"source ~/.venvs/ghc-api/bin/activate && "
            f"ghc-api -p 8313 -a 127.0.0.1"
        ) from exc


def get_client(usage: str = "llm") -> ClientBundle:
    """同步客户端。"""
    model = get_active(usage)
    return build_client_bundle(model, usage)


def get_async_client(usage: str = "llm") -> ClientBundle:
    """异步客户端。"""
    model = get_active(usage)
    return build_async_client_bundle(model, usage)


def get_chat_model(usage: str = "llm") -> ClientBundle:
    """LangChain chat model for synchronous text/vision chat calls."""
    model = get_active(usage)
    return build_chat_model_bundle(model, usage)


def get_async_chat_model(usage: str = "llm") -> ClientBundle:
    """LangChain chat model for asynchronous text/vision chat calls."""
    model = get_active(usage)
    return build_chat_model_bundle(model, usage)


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


def build_chat_model_bundle(model: ResolvedModel, usage: str = "llm") -> ClientBundle:
    """Build a LangChain chat model bundle from an already-resolved model."""
    client_options = validate_client_config(model, usage)
    return ClientBundle(
        client=init_chat_model(
            model.model_id,
            model_provider="openai",
            **client_options,
        ),
        model=model,
    )


def validate_api_key(model: ResolvedModel, usage: str) -> str:
    """Return a trimmed API key or raise an explicit config error."""
    api_key = str(model.api_key or "").strip()
    if not api_key:
        raise _LLMClientConfigError(
            f"{usage} 模型 {model.key} 的 api_key 为空，请检查 api_config.yaml"
        )
    return api_key


def validate_client_config(model: ResolvedModel, usage: str) -> dict[str, str]:
    """Return trimmed OpenAI client options or raise an explicit config error."""
    api_key = validate_api_key(model, usage)
    base_url = str(model.base_url or "").strip()
    if not base_url:
        raise _LLMClientConfigError(
            f"{usage} 模型 {model.key} 的 base_url 为空，请检查 api_config.yaml"
        )
    return {"api_key": api_key, "base_url": base_url}
