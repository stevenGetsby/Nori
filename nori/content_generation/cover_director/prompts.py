"""Cover prompt construction helpers for CoverDirectorAgent."""
from __future__ import annotations

from typing import Any, Callable, TypeVar

from nori.content_generation.models import NoteDraft
from nori.shared.prompting import json_block, json_prompt


JsonCall = Callable[..., dict[str, Any]]
ErrorT = TypeVar("ErrorT", bound=Exception)


def design_prompt_llm(
    draft: NoteDraft,
    skill: dict[str, Any],
    reference_paths: list[str],
    intent: dict[str, Any],
    *,
    json_call: JsonCall,
    error_type: type[ErrorT],
) -> str:
    """Build the image-generation prompt for an XHS cover."""
    bundle_dict = draft.asset_bundle or {}
    brand_facts = list(bundle_dict.get("brand_facts") or [])
    text_points = list(bundle_dict.get("text_points") or [])

    user_prompt = (
        f"小红书 note 标题：{draft.title}\n"
        f"语气：{skill.get('tone', '')}；类型：{skill.get('note_type', '')}\n"
        f"创作目标：{skill.get('creative_goal', '')}\n"
        f"用户意图：{json_prompt(intent)}\n\n"
        f"品牌信息：{json_prompt(brand_facts)}\n"
        f"主要卖点：{json_prompt(text_points[:3])}\n\n"
        f"封面规则：\n{json_block(skill.get('cover_rules') or [])}\n\n"
        f"视觉规则：\n{json_block(skill.get('visual_rules') or [])}\n\n"
        f"禁止项：{json_prompt(skill.get('avoid_rules') or [])}\n"
        f"参考图数量：{len(reference_paths)}（已作为 reference_images 传给生图模型）\n\n"
        "请为这条小红书 note 写一段 gpt-image-2 视觉 prompt：\n"
        "  - 用一段英文叙述 + 中文标题文字（标题原样置入画面，6-14 字）\n"
        "  - 明确构图、主体、色彩、光线、风格、文字版式；3:4 竖图\n"
        "  - 若有参考图，请显式说明保留参考图的主体/品牌元素\n"
        "  - 不要硬广价格、不要伪造 logo / 第三方认证 / UI 截图\n\n"
        '只输出 JSON：{"prompt": "<一段完整的视觉 prompt>"}'
    )

    data = json_call(
        system="你是 Nori 的封面 prompt 工序，只输出 JSON。",
        user=user_prompt,
        timeout=60,
    )
    prompt = str(data.get("prompt") or "").strip()
    if not prompt:
        raise error_type("CoverPromptWriter 返回空 prompt")
    return prompt
