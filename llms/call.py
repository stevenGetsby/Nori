"""高层调用函数。

职能：
  - chat(messages, usage=...)         同步文本补全
  - achat(messages, usage=...)        异步文本补全
  - chat_json(messages, usage=...)    同步 JSON 对象补全
  - chat_json_with_raw(...)           JSON 对象补全 + 原始文本
  - image(prompt, usage="image",
          reference_images=None)      文生图 / 图生图（吃原图字节）

封装 temperature_fixed、max_output、extra_body 等模型约束，
调用方不必关心每个服务商的特殊参数。
Google 生图走原生 google-genai SDK；OpenAI 兼容默认有参考图走
images.edit；relay 的 gpt-image-2 参考图走 images.generate + image_urls。
"""
from __future__ import annotations

from typing import Any, Callable

from .chat_runner import achat_text as _achat_text
from .chat_runner import chat_text as _chat_text
from .client import build_client_bundle, get_async_client, get_client, validate_api_key
from .config import get_active
from .image_runner import image_outputs as _image_outputs
from .json_calls import chat_json_raw
from .json_parser import parse_json_object
from .telemetry import set_telemetry_sink


def chat(
    messages: list[dict[str, Any]],
    *,
    usage: str = "llm",
    **kwargs: Any,
) -> str:
    """同步 chat，返回首条消息 content。"""
    return _chat_text(messages, usage=usage, _get_client=get_client, **kwargs)


def chat_json(
    messages: list[dict[str, Any]],
    *,
    usage: str = "llm",
    json_mode: bool = False,
    retry_without_response_format: bool = True,
    _chat: Callable[..., str] | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    """同步 chat，并把返回内容解析成 JSON object。

    默认不注入 response_format，避免改变不同 provider 的兼容行为。调用方可用
    json_mode=True 请求 OpenAI 兼容 JSON object mode；若 provider/SDK 拒绝
    response_format，则默认去掉 response_format 重试一次。
    """
    data, _raw = chat_json_with_raw(
        messages,
        usage=usage,
        json_mode=json_mode,
        retry_without_response_format=retry_without_response_format,
        _chat=_chat,
        **kwargs,
    )
    return data


def chat_json_with_raw(
    messages: list[dict[str, Any]],
    *,
    usage: str = "llm",
    json_mode: bool = False,
    retry_without_response_format: bool = True,
    _chat: Callable[..., str] | None = None,
    **kwargs: Any,
) -> tuple[dict[str, Any], str]:
    """同步 chat，返回解析后的 JSON object 和原始模型文本。"""
    chat_func = _chat or chat
    raw = chat_json_raw(
        messages,
        usage=usage,
        json_mode=json_mode,
        retry_without_response_format=retry_without_response_format,
        chat_func=chat_func,
        params=kwargs,
    )
    return parse_json_object(raw), raw


async def achat(
    messages: list[dict[str, Any]],
    *,
    usage: str = "llm",
    **kwargs: Any,
) -> str:
    """异步 chat，返回首条消息 content。"""
    return await _achat_text(messages, usage=usage, _get_async_client=get_async_client, **kwargs)


def image(
    prompt: str,
    *,
    usage: str = "image",
    size: str | None = None,
    reference_images: list[Any] | None = None,
    **kwargs: Any,
) -> list[str]:
    """文生图 / 图生图，返回 url 或 data-uri 列表。

    reference_images:
      可选；每项支持以下载体：
        - bytes / bytearray            原始图字节
        - str(以 "data:" 开头)         data-uri，自动解 base64
        - str / Path（可读文件路径）   读字节
        - 其他 str / 不可读路径        视为已编码 base64 字符串

    Provider 分派：
      - Google      → 原生 google-genai SDK，参考图作为 Part 加入 contents
    - Relay       → 有参考图走 OpenAI 兼容 images.generate + image_urls
    - 其他        → 有参考图走 OpenAI 兼容 images.edit，否则 images.generate

    若有效 reference bytes 非空但当前模型未声明支持参考图，会先抛出
    ImageCapabilityError，避免请求进入 provider SDK 后才失败。不可读取或无效的
    reference_images 会被过滤；无有效参考图时按文生图处理。
    """
    return _image_outputs(
        prompt,
        usage=usage,
        size=size,
        reference_images=reference_images,
        _get_active=get_active,
        _build_client_bundle=build_client_bundle,
        **kwargs,
    )
