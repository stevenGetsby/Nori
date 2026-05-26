"""Reference image selection helpers for CoverDirector."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from nori.content_generation.models import NoteDraft
from nori.core import UserAsset
from nori.shared.prompting import json_block, json_prompt


DEFAULT_MAX_REFERENCES = 8
DEFAULT_MAX_PROMPT_REFERENCES = 3

JsonCall = Callable[..., dict[str, Any]]


def select_references_llm(
    draft: NoteDraft,
    skill: dict[str, Any],
    intent: dict[str, Any],
    tagged_assets: list[UserAsset],
    *,
    json_call: JsonCall,
    max_references: int = DEFAULT_MAX_REFERENCES,
) -> list[str]:
    """Use tagged user assets to select reference image paths for cover generation."""
    images = [
        {
            "index": i,
            "path": a.path,
            "subject": a.subject,
            "vision_roles": list(a.vision_roles),
            "brand_signals": list(a.brand_signals),
            "usable_for": list(a.usable_for),
            "quality": a.quality,
        }
        for i, a in enumerate(tagged_assets)
        if a.kind == "image" and a.path
    ]
    if not images:
        return []

    user_text = str(intent.get("user_text") or "").strip() or "用户未提供额外文本说明。"
    user_prompt = (
        f"小红书封面需要选择参考图。\n"
        f"用户原始诉求：{user_text}\n\n"
        f"note 标题：{draft.title}\n"
        f"语气：{skill.get('tone', '')}；类型：{skill.get('note_type', '')}\n"
        f"创作目标：{skill.get('creative_goal', '')}\n"
        f"用户意图：{json_prompt(intent)}\n\n"
        f"封面规则：{json_prompt(skill.get('cover_rules') or [])}\n"
        f"视觉规则：{json_prompt(skill.get('visual_rules') or [])}\n\n"
        f"资产池（已经被 Intaker 打过语义标签）：\n"
        f"{json_block(images)}\n\n"
        "请结合用户原始诉求从资产池里选出本次封面需要作为参考的图片 index：\n"
        "  - 你可以选 0 张（纯文生图）、也可以选多张；推荐 1~5 张\n"
        "  - 优先 usable_for 包含 cover 的\n"
        "  - 优先 brand_signals 非空且跟 note 主题/用户诉求相关的\n"
        "  - usable_for=not_usable 或 quality=low 的不要选\n"
        "  - 不要选重复主体的图\n\n"
        '输出 JSON：{"chosen_indices": [<选中的 index>], "rationale": "<一句话说明为什么选这几张>"}'
    )

    data = json_call(
        system="你是 Nori 的封面参考图选取工序，只输出 JSON。",
        user=user_prompt,
        timeout=45,
    )

    chosen = data.get("chosen_indices")
    if not isinstance(chosen, list):
        return []

    paths: list[str] = []
    seen: set[str] = set()
    for value in chosen:
        try:
            idx = int(value)
        except (TypeError, ValueError):
            continue
        if 0 <= idx < len(tagged_assets):
            asset = tagged_assets[idx]
            if asset.kind == "image" and asset.path and asset.path not in seen and Path(asset.path).exists():
                paths.append(asset.path)
                seen.add(asset.path)
        if len(paths) >= max_references:
            break
    return paths


def collect_reference_paths(
    draft: NoteDraft,
    reference_assets: list[UserAsset] | None,
    *,
    max_references: int = DEFAULT_MAX_PROMPT_REFERENCES,
) -> list[str]:
    """Collect legacy draft/reference-asset paths for cover prompt image inputs."""
    paths: list[str] = []
    seen: set[str] = set()

    def _add(path: str) -> None:
        if path and Path(path).exists() and path not in seen:
            paths.append(path)
            seen.add(path)

    if draft.cover_path:
        _add(draft.cover_path)
    for path in draft.image_paths:
        if len(paths) >= max_references:
            break
        _add(path)

    if not paths and reference_assets:
        for asset in reference_assets:
            if asset.kind == "image":
                _add(asset.path)
                if len(paths) >= max_references:
                    break

    return paths[:max_references]
