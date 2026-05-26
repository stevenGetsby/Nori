"""Asset curation helpers for NoteMakerAgent."""
from __future__ import annotations

from typing import Any, Callable

from nori.content_generation.models import AssetBundle, UserAsset
from nori.shared.prompting import json_block, json_prompt
from . import prompts as _prompts


JsonCall = Callable[..., dict[str, Any]]


def curate_assets_llm(
    assets: list[UserAsset],
    skill: dict[str, Any],
    intent: dict[str, Any],
    *,
    json_call: JsonCall,
) -> AssetBundle:
    """Ask the LLM to group tagged assets into NoteMaker's AssetBundle contract."""
    images = [(i, a) for i, a in enumerate(assets) if a.kind == "image"]
    texts = [(i, a) for i, a in enumerate(assets) if a.kind == "text" and a.text.strip()]

    image_input = [
        {
            "index": i,
            "path": a.path,
            "vision_roles": list(a.vision_roles),
            "subject": a.subject,
            "brand_signals": list(a.brand_signals),
            "usable_for": list(a.usable_for),
            "quality": a.quality,
        }
        for i, a in images
    ]
    text_input = [
        {"index": i, "text": a.text.strip()[:400]}
        for i, a in texts
    ]

    if not image_input and not text_input:
        return AssetBundle()

    data = json_call(
        system=_prompts.ASSET_CURATOR_SYSTEM_PROMPT,
        user=(
            f"创作目标：{skill.get('creative_goal', '')}\n"
            f"语气：{skill.get('tone', '')}；类型：{skill.get('note_type', '')}\n"
            f"用户意图：{json_prompt(intent)}\n\n"
            f"图片素材（按 index 引用）：\n{json_block(image_input)}\n\n"
            f"文本素材（按 index 引用）：\n{json_block(text_input)}\n\n"
            "请把素材整理成 5 个桶：\n"
            "  - main_image_indices：主视觉图片 index（封面优先）\n"
            "  - aux_image_indices：辅助图 index\n"
            "  - text_points：用户的卖点/描述短句\n"
            "  - brand_facts：品牌名/口号/理念/人设\n"
            "  - data_points：数据/数字/案例\n"
            "保留原文，不要改写。每个文本桶最多 6 条。\n"
            '输出 JSON：{"main_image_indices": [], "aux_image_indices": [], '
            '"text_points": [], "brand_facts": [], "data_points": []}'
        ),
        timeout=60,
    )
    return bundle_from_curator_data(data, assets)


def bundle_from_curator_data(data: dict[str, Any], assets: list[UserAsset]) -> AssetBundle:
    """Normalize LLM-selected asset indices and text buckets into an AssetBundle."""
    images = [(i, a) for i, a in enumerate(assets) if a.kind == "image"]
    bundle = AssetBundle()
    main_idx = int_list(data.get("main_image_indices"))
    aux_idx = int_list(data.get("aux_image_indices"))
    used: set[int] = set()
    for i in main_idx:
        if 0 <= i < len(assets) and assets[i].kind == "image" and i not in used:
            bundle.main_images.append(assets[i])
            used.add(i)
    for i in aux_idx:
        if 0 <= i < len(assets) and assets[i].kind == "image" and i not in used:
            bundle.aux_images.append(assets[i])
            used.add(i)
    for i, asset in images:
        if i not in used:
            bundle.aux_images.append(asset)
    if not bundle.main_images and bundle.aux_images:
        bundle.main_images.append(bundle.aux_images.pop(0))

    bundle.text_points = str_list(data.get("text_points"))[:6]
    bundle.brand_facts = str_list(data.get("brand_facts"))[:6]
    bundle.data_points = str_list(data.get("data_points"))[:6]
    return bundle


def pick_visual_paths(bundle: AssetBundle) -> tuple[str, list[str]]:
    """Use the first main image as cover and keep up to 8 remaining gallery images."""
    cover = bundle.main_images[0].path if bundle.main_images else ""
    others = [a.path for a in bundle.main_images[1:] + bundle.aux_images if a.path]
    return cover, others[:8]


def int_list(value: Any) -> list[int]:
    out: list[int] = []
    for item in value or []:
        try:
            out.append(int(item))
        except (TypeError, ValueError):
            continue
    return out


def str_list(value: Any) -> list[str]:
    return [str(item).strip() for item in (value or []) if str(item).strip()]


__all__ = [
    "bundle_from_curator_data",
    "curate_assets_llm",
    "int_list",
    "pick_visual_paths",
    "str_list",
]
