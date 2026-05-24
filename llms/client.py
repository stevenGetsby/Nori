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

from .config import get_active
from nori.nori_config import ResolvedModel


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
    return ClientBundle(
        client=OpenAI(api_key=model.api_key, base_url=model.base_url),
        model=model,
    )


def get_async_client(usage: str = "llm") -> ClientBundle:
    """异步客户端。"""
    model = get_active(usage)
    return ClientBundle(
        client=AsyncOpenAI(api_key=model.api_key, base_url=model.base_url),
        model=model,
    )
