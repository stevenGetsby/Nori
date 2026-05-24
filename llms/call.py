"""高层调用函数。

职能：
  - chat(messages, usage=...)         同步文本补全
  - achat(messages, usage=...)        异步文本补全
  - chat_json(messages, usage=...)    同步 JSON 对象补全
  - image(prompt, usage="image",
          reference_images=None)      文生图 / 图生图（吃原图字节）

封装 temperature_fixed、max_output、extra_body 等模型约束，
调用方不必关心每个服务商的特殊参数。
Google 生图走原生 google-genai SDK；OpenAI 兼容默认有参考图走
images.edit；relay 的 gpt-image-2 参考图走 images.generate + image_urls。
"""
from __future__ import annotations

import base64
import io
import json
import re
from pathlib import Path
from typing import Any, Callable

from .client import get_async_client, get_client
from .config import get_active


class ChatJSONError(ValueError):
    """Raised when a chat response cannot be parsed as a JSON object."""

    def __init__(self, message: str, raw: str | None = None) -> None:
        super().__init__(message)
        self.raw = raw or ""

    @property
    def preview(self) -> str:
        return self.raw[:200]


def _merge_kwargs(model, kwargs: dict) -> dict:
    """把模型级约束合并进 kwargs。"""
    out = dict(kwargs)
    if model.temperature_fixed is not None:
        out["temperature"] = model.temperature_fixed
    max_output_param = _max_output_param_name(model)
    if model.max_output:
        if max_output_param == "max_completion_tokens":
            if "max_tokens" in out and "max_completion_tokens" not in out:
                out["max_completion_tokens"] = out.pop("max_tokens")
            elif "max_completion_tokens" not in out:
                out["max_completion_tokens"] = model.max_output
        elif "max_tokens" not in out and "max_completion_tokens" not in out:
            out["max_tokens"] = model.max_output
    if model.extra_body:
        out.setdefault("extra_body", {}).update(model.extra_body)
    return out


def _max_output_param_name(model) -> str:
    model_id = model.model_id.lower()
    if model.provider_id in {"ghc", "openai"} and model_id.startswith("gpt-5"):
        return "max_completion_tokens"
    return "max_tokens"


def chat(
    messages: list[dict[str, Any]],
    *,
    usage: str = "llm",
    **kwargs: Any,
) -> str:
    """同步 chat，返回首条消息 content。"""
    bundle = get_client(usage)
    params = _merge_kwargs(bundle.model, kwargs)
    resp = bundle.client.chat.completions.create(
        model=bundle.model_id,
        messages=messages,
        **params,
    )
    return (resp.choices[0].message.content or "").strip()


def chat_json(
    messages: list[dict[str, Any]],
    *,
    usage: str = "llm",
    _chat: Callable[..., str] | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    """同步 chat，并把返回内容解析成 JSON object。

    不默认注入 response_format，避免改变不同 provider 的兼容行为；调用方如需
    JSON mode 可以继续显式传入 response_format。
    """
    chat_func = _chat or chat
    raw = chat_func(messages, usage=usage, **kwargs)
    return parse_json_object(raw)


def parse_json_object(raw: str | None) -> dict[str, Any]:
    """Parse a model response into a JSON object, accepting fenced/embedded JSON."""
    text = (raw or "").strip()
    if not text:
        raise ChatJSONError("LLM 输出为空，无法解析为 JSON", raw or "")

    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
        text = re.sub(r"\n?```$", "", text).strip()

    parsed = _loads_json_object(text, raw or "")
    if parsed is not None:
        return parsed

    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        parsed = _loads_json_object(match.group(0), raw or "")
        if parsed is not None:
            return parsed

    raise ChatJSONError("LLM 输出无法解析为 JSON object", raw or "")


def _loads_json_object(text: str, raw: str) -> dict[str, Any] | None:
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return None
    if not isinstance(data, dict):
        raise ChatJSONError(f"LLM 输出 JSON 不是 object: {type(data).__name__}", raw)
    return data


async def achat(
    messages: list[dict[str, Any]],
    *,
    usage: str = "llm",
    **kwargs: Any,
) -> str:
    """异步 chat，返回首条消息 content。"""
    bundle = get_async_client(usage)
    params = _merge_kwargs(bundle.model, kwargs)
    resp = await bundle.client.chat.completions.create(
        model=bundle.model_id,
        messages=messages,
        **params,
    )
    return (resp.choices[0].message.content or "").strip()


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

    若 reference_images 非空但当前 provider 没有图编辑能力（例如纯文生图模型），
    会抛出来自 provider SDK 的异常；调用方根据需要降级或切换 active model。
    """
    ref_bytes_list: list[bytes] = []
    if reference_images:
        ref_bytes_list = [_load_image_bytes(item) for item in reference_images]
        ref_bytes_list = [b for b in ref_bytes_list if b]

    model = get_active(usage)

    if model.provider_id == "google":
        return _image_google(prompt, model, size, ref_bytes_list)

    # OpenAI 兼容路径
    bundle = get_client(usage)
    if size is None and bundle.model.resolution_options:
        size = bundle.model.resolution_options[0]
    if model.provider_id == "relay":
        # relay 在 response_format=url 时返回的相对短期 url 会在数秒内过期；
        # 改用 b64_json 时它实际仍然返回 url，但是是稳定可下载的绝对路径。
        kwargs.setdefault("response_format", "b64_json")

    if ref_bytes_list and model.provider_id == "relay":
        return _image_relay_generate_with_references(bundle, prompt, ref_bytes_list, size, kwargs)

    if ref_bytes_list:
        return _image_openai_edit(bundle, prompt, ref_bytes_list, size, kwargs)

    resp = bundle.client.images.generate(
        model=bundle.model_id,
        prompt=prompt,
        size=size,
        **kwargs,
    )
    return _collect_image_results(resp)


def _image_relay_generate_with_references(
    bundle,
    prompt: str,
    ref_bytes_list: list[bytes],
    size: str | None,
    kwargs: dict,
) -> list[str]:
    """relay gpt-image-2 图生图：使用 /images/generations 的扩展字段。"""
    data_uris = [_bytes_to_data_uri(raw) for raw in ref_bytes_list if raw]
    payload_variants: list[dict[str, Any]] = [
        {"image_urls": data_uris},
        {"images": data_uris},
        {"image": data_uris[0] if len(data_uris) == 1 else data_uris},
    ]
    last_error: Exception | None = None

    for extra in payload_variants:
        generate_kwargs = dict(kwargs)
        extra_body = dict(generate_kwargs.get("extra_body") or {})
        extra_body.update(extra)
        generate_kwargs["extra_body"] = extra_body
        if size is not None:
            generate_kwargs["size"] = size
        try:
            resp = bundle.client.images.generate(
                model=bundle.model_id,
                prompt=prompt,
                **generate_kwargs,
            )
            return _collect_image_results(resp)
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            if not _is_retryable_relay_reference_error(exc):
                raise

    if last_error:
        raise last_error
    return []


def _image_openai_edit(
    bundle,
    prompt: str,
    ref_bytes_list: list[bytes],
    size: str | None,
    kwargs: dict,
) -> list[str]:
    """走 OpenAI 兼容 images.edit。"""
    files = []
    for idx, raw in enumerate(ref_bytes_list):
        buf = io.BytesIO(raw)
        buf.name = f"input_{idx}.png"
        files.append(buf)
    image_arg = files[0] if len(files) == 1 else files
    edit_kwargs = dict(kwargs)
    if size is not None:
        edit_kwargs["size"] = size
    resp = bundle.client.images.edit(
        model=bundle.model_id,
        image=image_arg,
        prompt=prompt,
        **edit_kwargs,
    )
    return _collect_image_results(resp)


def _collect_image_results(resp: Any) -> list[str]:
    results: list[str] = []
    for item in getattr(resp, "data", []) or []:
        url = getattr(item, "url", None)
        if url:
            results.append(url)
            continue
        b64_json = getattr(item, "b64_json", None)
        if b64_json:
            results.append(f"data:image/png;base64,{b64_json}")
    return results


def _bytes_to_data_uri(raw: bytes) -> str:
    return f"data:{_sniff_mime(raw)};base64,{base64.b64encode(raw).decode()}"


def _is_retryable_relay_reference_error(exc: Exception) -> bool:
    text = str(exc).lower()
    return any(token in text for token in (
        "image_urls",
        "images",
        "image",
        "unknown",
        "unsupported",
        "invalid_request_error",
        "字段",
        "参数",
    ))


def _image_google(
    prompt: str,
    model,
    size: str | None,
    ref_bytes_list: list[bytes] | None = None,
) -> list[str]:
    """Google Gemini 原生生图 / 图生图。返回 data:image/png;base64,... 列表。"""
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=model.api_key)

    contents: list[Any]
    if ref_bytes_list:
        parts: list[Any] = [prompt]
        for raw in ref_bytes_list:
            parts.append(
                types.Part.from_bytes(data=raw, mime_type=_sniff_mime(raw))
            )
        contents = parts
    else:
        contents = prompt  # type: ignore[assignment]

    response = client.models.generate_content(
        model=model.model_id,
        contents=contents,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE", "TEXT"],
        ),
    )

    results: list[str] = []
    if response.candidates:
        for part in response.candidates[0].content.parts:
            if part.inline_data and part.inline_data.data:
                b64 = base64.b64encode(part.inline_data.data).decode()
                mime = part.inline_data.mime_type or "image/png"
                results.append(f"data:{mime};base64,{b64}")
    return results


# ---------------------------------------------------------------------- helpers


def _load_image_bytes(item: Any) -> bytes:
    """把多种来源归一化为 bytes。失败返回空 bytes（被上层过滤）。"""
    if item is None:
        return b""
    if isinstance(item, (bytes, bytearray)):
        return bytes(item)
    if isinstance(item, Path):
        try:
            return item.read_bytes()
        except Exception:  # noqa: BLE001
            return b""
    if isinstance(item, str):
        s = item.strip()
        if not s:
            return b""
        if s.startswith("data:"):
            # data:image/png;base64,XXX
            _, _, payload = s.partition(",")
            try:
                return base64.b64decode(payload)
            except Exception:  # noqa: BLE001
                return b""
        if s.startswith(("http://", "https://")):
            # 暂不主动下载远程图，留给调用方先 fetch 到本地或字节
            return b""
        # 文件路径
        try:
            p = Path(s)
            if p.is_file():
                return p.read_bytes()
        except Exception:  # noqa: BLE001
            pass
        # 兜底：当 base64 字符串处理
        try:
            return base64.b64decode(s, validate=True)
        except Exception:  # noqa: BLE001
            return b""
    return b""


def _sniff_mime(raw: bytes) -> str:
    if raw.startswith(b"\x89PNG"):
        return "image/png"
    if raw[:3] == b"\xff\xd8\xff":
        return "image/jpeg"
    if raw[:6] in (b"GIF87a", b"GIF89a"):
        return "image/gif"
    if raw[:4] == b"RIFF" and raw[8:12] == b"WEBP":
        return "image/webp"
    return "image/png"
