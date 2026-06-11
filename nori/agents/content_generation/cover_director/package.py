"""Class-owned package contract for CoverDirectorAgent."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, TypeVar

from nori.agents.content_generation.schemas import NoteDraft
from nori.agents.content_generation.social_card_guides import cover_prompt_guidance
from nori.core import AgentPromptBuilder, UserAsset
from nori.shared.image_io import image_to_bytes
from nori.shared.prompting import json_block, json_prompt


DEFAULT_MAX_REFERENCES = 8
DEFAULT_MAX_PROMPT_REFERENCES = 3

JsonCall = Callable[..., dict[str, Any]]
ErrorT = TypeVar("ErrorT", bound=Exception)


class CoverReferenceSelector:
    """Select and prepare reference images for cover generation."""

    max_references = DEFAULT_MAX_REFERENCES
    max_prompt_references = DEFAULT_MAX_PROMPT_REFERENCES

    def select_with_llm(
        self,
        draft: NoteDraft,
        skill: dict[str, Any],
        intent: dict[str, Any],
        tagged_assets: list[UserAsset],
        *,
        json_call: JsonCall,
        max_references: int | None = None,
    ) -> list[str]:
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
        limit = max_references if max_references is not None else self.max_references
        for value in chosen:
            try:
                idx = int(value)
            except (TypeError, ValueError):
                continue
            if 0 <= idx < len(tagged_assets):
                asset = tagged_assets[idx]
                if asset.kind == "image" and asset.path and asset.path not in seen and self.reference_exists(asset.path):
                    paths.append(asset.path)
                    seen.add(asset.path)
            if len(paths) >= limit:
                break
        return paths

    def collect_legacy_paths(
        self,
        draft: NoteDraft,
        reference_assets: list[UserAsset] | None,
        *,
        max_references: int | None = None,
    ) -> list[str]:
        paths: list[str] = []
        seen: set[str] = set()
        limit = max_references if max_references is not None else self.max_prompt_references

        def add(path: str) -> None:
            if path and self.reference_exists(path) and path not in seen:
                paths.append(path)
                seen.add(path)

        if draft.cover_path:
            add(draft.cover_path)
        for path in draft.image_paths:
            if len(paths) >= limit:
                break
            add(path)

        if not paths and reference_assets:
            for asset in reference_assets:
                if asset.kind == "image":
                    add(asset.path)
                    if len(paths) >= limit:
                        break

        return paths[:limit]

    def to_image_input(self, path: str) -> bytes | str:
        if path.startswith(("http://", "https://")):
            return path
        return image_to_bytes(path)

    def reference_exists(self, path: str) -> bool:
        if path.startswith(("http://", "https://")):
            return True
        return Path(path).exists()


class CoverPromptBuilder(AgentPromptBuilder):
    system_prompt = "你是 Nori 的封面 prompt 工序，只输出 JSON。"

    def design_with_llm(
        self,
        draft: NoteDraft,
        skill: dict[str, Any],
        reference_paths: list[str],
        intent: dict[str, Any],
        *,
        json_call: JsonCall,
        error_type: type[ErrorT],
    ) -> str:
        user_prompt = self.build_user_prompt(draft, skill, reference_paths, intent)
        data = json_call(
            system=self.system_prompt,
            user=user_prompt,
            timeout=60,
        )
        prompt = str(data.get("prompt") or "").strip()
        if not prompt:
            raise error_type("CoverPromptWriter 返回空 prompt")
        return prompt

    def build_user_prompt(
        self,
        draft: NoteDraft,
        skill: dict[str, Any],
        reference_paths: list[str],
        intent: dict[str, Any],
    ) -> str:
        bundle_dict = draft.asset_bundle or {}
        brand_facts = list(bundle_dict.get("brand_facts") or [])
        text_points = list(bundle_dict.get("text_points") or [])
        social_guidance = cover_prompt_guidance(intent)

        return (
            f"小红书 note 标题：{draft.title}\n"
            f"语气：{skill.get('tone', '')}；类型：{skill.get('note_type', '')}\n"
            f"创作目标：{skill.get('creative_goal', '')}\n"
            f"用户意图：{json_prompt(intent)}\n\n"
            f"品牌信息：{json_prompt(brand_facts)}\n"
            f"主要卖点：{json_prompt(text_points[:3])}\n\n"
            f"封面规则：\n{json_block(skill.get('cover_rules') or [])}\n\n"
            f"视觉规则：\n{json_block(skill.get('visual_rules') or [])}\n\n"
            f"{_social_card_prompt_block(social_guidance)}"
            f"禁止项：{json_prompt(skill.get('avoid_rules') or [])}\n"
            f"参考图数量：{len(reference_paths)}（已作为 reference_images 传给生图模型）\n\n"
            "参考图保真约束（最高优先级）：\n"
            "  - 用户上传的产品参考图是主体形态锁定参考，不是普通风格图；必须保留产品的核心轮廓、人体/脸部/身体美学造型、银色材质、比例关系和关键结构。\n"
            "  - 如果市场热帖视觉规则与用户产品形态冲突，必须优先用户产品形态；热帖只允许影响摄影方法、光线、背景、构图、文字层级和信息密度。\n"
            "  - 不要把用户产品改造成普通戒指、手镯、项链、抽象银块或其他竞品款式；不要新增不存在的宝石、链条、logo、水印或品牌符号。\n"
            "  - 可以改善拍摄质感、清理水印、重做场景和光影，但产品主体必须一眼仍是参考图里的「人体美学银饰/聆」。\n\n"
            "封面标题视觉约束：\n"
            "  - 主标题只允许 6-10 个汉字，必须大、清楚、少字，优先放在左上或上方安全区；不要超过两行。\n"
            "  - 副标题最多 8-12 个汉字，字号明显小于主标题；整张封面最多 2 组文字，不要底部堆关键词。\n"
            "  - 字体风格应高级、干净、克制；文字不得遮挡产品脸部、身体曲线、银面高光和关键工艺细节。\n"
            "  - 标题语义要围绕产品独特点：光影表情、人体美学、女性力量、原创银饰；不要写泛泛的种草词。\n\n"
            "请为这条小红书 note 写一段 gpt-image-2 视觉 prompt：\n"
            "  - 首图一眼看懂：画面在 1 秒内说明用户利益点，不只做氛围图\n"
            "  - 热点/账号适配：如果借势热点，画面必须落到账号可信场景或产品真实用途\n"
            "  - 用一段英文叙述 + 中文标题文字（封面文字 6-14 字，标题可压缩但保留核心钩子）\n"
            "  - 明确构图、主体、色彩、光线、风格、文字版式；3:4 竖图\n"
            "  - 若有参考图，请显式说明严格保留参考图的产品主体形态和关键结构，再迁移市场热帖的摄影/排版风格\n"
            "  - 不要硬广价格、不要伪造 logo / 第三方认证 / UI 截图\n"
            "  - 不要伪造 UI 截图、官方通知、用户背书、医疗金融证明\n\n"
            '只输出 JSON：{"prompt": "<一段完整的视觉 prompt>"}'
        )


def _social_card_prompt_block(profile: dict[str, Any]) -> str:
    if not profile:
        return ""
    if profile.get("platform") == "xhs":
        canvas = profile.get("canvas") if isinstance(profile.get("canvas"), dict) else {}
        page_count = profile.get("page_count") if isinstance(profile.get("page_count"), dict) else {}
        summary = {
            "source": profile.get("source", ""),
            "artifact": profile.get("artifact", ""),
            "canvas": canvas,
            "page_count": page_count,
            "layout_principles": profile.get("layout_principles") or [],
        }
        return (
            "社交卡片设计约束（来自 content_design_spec）：\n"
            f"{json_block(summary)}\n\n"
            "封面必须按 1080x1440 的 3:4 小红书首图设计：大钩子、一个强视觉、底部 3-5 个关键词；"
            "所有标题和主体留在安全区内；不要生成整套海报文字，也不要把正文塞满首图。\n\n"
        )
    if profile.get("platform") == "wechat":
        return (
            "公众号封面设计约束（来自 content_design_spec）：\n"
            f"{json_block(profile)}\n\n"
            "如果执行公众号封面，21:9 主封面和 1:1 方封面需要分别构图；方封面使用短标题，不做硬裁切。\n\n"
        )
    return f"社交卡片设计约束：\n{json_block(profile)}\n\n"


__all__ = [
    "CoverPromptBuilder",
    "CoverReferenceSelector",
    "DEFAULT_MAX_PROMPT_REFERENCES",
    "DEFAULT_MAX_REFERENCES",
]
