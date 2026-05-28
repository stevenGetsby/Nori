"""Provider-specific image request helpers for the LLM gateway."""
from __future__ import annotations

import base64
import io
from typing import Any

from .image_inputs import bytes_to_data_uri, sniff_mime
from .results import collect_image_results


def image_relay_generate_with_references(
    bundle,
    prompt: str,
    ref_bytes_list: list[bytes],
    size: str | None,
    kwargs: dict,
    *,
    ref_urls: list[str] | None = None,
) -> list[str]:
    """relay gpt-image-2 image-to-image via generation extra_body variants."""
    urls = [url for url in (ref_urls or []) if url]
    data_uris = [bytes_to_data_uri(raw) for raw in ref_bytes_list if raw]
    payload_variants: list[dict[str, Any]] = []
    if urls:
        payload_variants.extend([
            {"image_urls": urls},
            {"images": urls},
            {"image": urls[0] if len(urls) == 1 else urls},
        ])
    if data_uris:
        payload_variants.extend([
            {"image_urls": data_uris},
            {"images": data_uris},
            {"image": data_uris[0] if len(data_uris) == 1 else data_uris},
        ])
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
            return collect_image_results(resp)
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            if not is_retryable_relay_reference_error(exc):
                raise

    if last_error:
        if is_relay_base64_reference_error(last_error):
            raise RuntimeError(
                "relay rejected local/base64 reference_images; provide public HTTPS image URLs "
                "for true image reference generation"
            )
        raise last_error
    return []


def image_openai_edit(
    bundle,
    prompt: str,
    ref_bytes_list: list[bytes],
    size: str | None,
    kwargs: dict,
) -> list[str]:
    """OpenAI-compatible images.edit request with in-memory reference files."""
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
    return collect_image_results(resp)


def is_retryable_relay_reference_error(exc: Exception) -> bool:
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


def is_relay_base64_reference_error(exc: Exception) -> bool:
    text = str(exc).lower()
    return "base64" in text or "不支持base64" in text


def image_google(
    prompt: str,
    model,
    size: str | None,
    ref_bytes_list: list[bytes] | None = None,
    *,
    api_key: str,
) -> list[str]:
    """Google Gemini native image generation. Returns data-uri images."""
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)

    contents: list[Any]
    if ref_bytes_list:
        parts: list[Any] = [prompt]
        for raw in ref_bytes_list:
            parts.append(
                types.Part.from_bytes(data=raw, mime_type=sniff_mime(raw))
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
