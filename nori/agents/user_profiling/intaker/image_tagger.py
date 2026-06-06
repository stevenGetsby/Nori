"""Vision tagging helpers for IntakeAgent image assets."""
from __future__ import annotations

import concurrent.futures
import sys
from typing import Any

from nori.core import LLMFactory, UserAsset
from nori.shared.image_io import image_to_data_uri
from nori.shared.llm_json import call_stage_messages_json
from nori.agents.user_profiling.models import UserInput
from .package import IntakeVisionPromptBuilder


VISION_PARALLELISM = 6

ALLOWED_VISION_ROLES = {
    "brand_logo", "ip_character", "product_shot", "scene_photo",
    "lifestyle", "data_chart", "reference_style", "raw_material",
    "portrait", "unknown",
}
ALLOWED_USABLE_FOR = {"cover", "body", "background_only", "not_usable"}
ALLOWED_QUALITY = {"high", "medium", "low"}


class IntakeVisionLLMError(RuntimeError):
    """Raised when one optional per-image vision tagging call fails."""


_VISION_PROMPT_BUILDER = IntakeVisionPromptBuilder()
VISION_SYSTEM_PROMPT = _VISION_PROMPT_BUILDER.system_prompt
VISION_USER_TEMPLATE = _VISION_PROMPT_BUILDER.user_prompt_template


def build_tagged_assets(
    normalized: UserInput,
    *,
    use_vision: bool,
    parallelism: int = VISION_PARALLELISM,
    llm_factory: LLMFactory | None = None,
) -> list[UserAsset]:
    """Convert normalized input images and text into tagged user assets."""
    assets: list[UserAsset] = []

    image_paths = [p for p in normalized.images if p]
    user_text = normalized.text.strip() or "用户未提供文本输入。"
    if use_vision and image_paths:
        tags = tag_images_llm(image_paths, user_text, parallelism=parallelism, llm_factory=llm_factory)
    else:
        tags = [None] * len(image_paths)
    for path, tag in zip(image_paths, tags):
        assets.append(make_image_asset(path, tag))

    text = normalized.text.strip()
    if text:
        assets.append(UserAsset(kind="text", text=text))

    return assets


def tag_images_llm(
    image_paths: list[str],
    user_text: str,
    *,
    parallelism: int = VISION_PARALLELISM,
    llm_factory: LLMFactory | None = None,
) -> list[dict[str, Any] | None]:
    """Run one optional vision tagging call per image and isolate per-image failures."""
    if not image_paths:
        return []

    out: list[dict[str, Any] | None] = [None] * len(image_paths)
    with concurrent.futures.ThreadPoolExecutor(max_workers=parallelism) as pool:
        futures = {
            pool.submit(tag_one_image_llm, path, user_text, llm_factory=llm_factory): i
            for i, path in enumerate(image_paths)
        }
        for fut in concurrent.futures.as_completed(futures):
            i = futures[fut]
            try:
                out[i] = fut.result()
            except Exception as exc:  # noqa: BLE001 - one failed image should not block the batch.
                print(
                    f"[warn] vision tag failed for {image_paths[i]}: "
                    f"{type(exc).__name__}: {exc}",
                    file=sys.stderr,
                )
                out[i] = None
    return out


def tag_one_image_llm(
    path: str,
    user_text: str,
    *,
    llm_factory: LLMFactory | None = None,
) -> dict[str, Any] | None:
    data_uri = image_to_data_uri(path)
    if not data_uri:
        return None
    llm_gateway = llm_factory or LLMFactory()
    return call_stage_messages_json(
        messages=[
            {"role": "system", "content": VISION_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": _VISION_PROMPT_BUILDER.build_user_prompt(user_text)},
                    {"type": "image_url", "image_url": {"url": data_uri}},
                ],
            },
        ],
        usage="vision",
        timeout=60,
        error_type=IntakeVisionLLMError,
        retry_max_tokens=None,
        chat_func=llm_gateway.chat_func,
        chat_json_func=llm_gateway.chat_json_func,
    )


def make_image_asset(path: str, tag: dict[str, Any] | None) -> UserAsset:
    if not isinstance(tag, dict):
        return UserAsset(kind="image", path=path)
    vision_roles = filter_allowed(tag.get("vision_roles"), ALLOWED_VISION_ROLES)
    usable_for = filter_allowed(tag.get("usable_for"), ALLOWED_USABLE_FOR)
    brand_signals = [str(b).strip() for b in (tag.get("brand_signals") or []) if str(b).strip()]
    subject = str(tag.get("subject") or "").strip()[:60]
    quality_raw = str(tag.get("quality") or "").strip().lower()
    quality = quality_raw if quality_raw in ALLOWED_QUALITY else ""
    return UserAsset(
        kind="image",
        path=path,
        vision_roles=vision_roles,
        subject=subject,
        brand_signals=brand_signals,
        usable_for=usable_for,
        quality=quality,
    )


def filter_allowed(value: Any, allowed: set[str]) -> list[str]:
    if isinstance(value, str):
        items = [value]
    elif isinstance(value, list):
        items = [str(v) for v in value]
    else:
        items = []
    out: list[str] = []
    seen: set[str] = set()
    for item in items:
        v = item.strip().lower()
        if v in allowed and v not in seen:
            out.append(v)
            seen.add(v)
    return out


__all__ = [
    "ALLOWED_QUALITY",
    "ALLOWED_USABLE_FOR",
    "ALLOWED_VISION_ROLES",
    "IntakeVisionLLMError",
    "VISION_PARALLELISM",
    "VISION_SYSTEM_PROMPT",
    "VISION_USER_TEMPLATE",
    "build_tagged_assets",
    "filter_allowed",
    "make_image_asset",
    "tag_images_llm",
    "tag_one_image_llm",
]
