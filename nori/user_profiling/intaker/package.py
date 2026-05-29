"""Class-owned prompt contract for IntakeAgent."""
from __future__ import annotations

from nori.core import AgentPromptBuilder
from nori.shared.prompting import json_prompt
from nori.user_profiling.models import UserInput


class IntakeTextPromptBuilder(AgentPromptBuilder):
    system_prompt = "你是 Nori 的 Intaker Agent。只输出 JSON。"

    user_prompt_template = """\
把用户输入整理成 Nori 后续 Agent 可用的 Intention + Context。

用户文字：
{text}

用户图片：
{images}

输出 JSON，字段固定：
{{
  "intention": {{
        "goal": "品牌认知 | 获客留资 | 产品种草 | 新品发布 | 销售转化 | 课程销售 | 涨粉 | 商务合作 | 未知",
        "format": "小红书图文 | 短视频 | Vlog | 直播 | 直播带货 | 未知",
        "tone": ["专业 | 高级 | 亲和 | 有趣 | 走心 | 干货 | 犀利"],
        "anti": ["不要硬广 | 不要低价感 | 保持人设 | 不要太商业 | 不要违规"]
  }},
  "context": {{
        "creative_assets": ["品牌标志 | 设计语言 | 品牌色 | 人设 | IP角色 | 口号 | 图片资产"],
        "commercial_assets": ["店铺链接 | 商品链接 | 优惠 | 课程 | 合作品 | 橱窗"],
        "guardrails": ["品牌规范 | 禁用词 | 人设边界 | 品类边界 | 不要硬广 | 不要低价感 | 保持人设 | 不要太商业 | 不要违规"],
        "data_refs": ["账号数据 | 对标内容 | 受众画像 | 同类账号 | 爆款案例"]
  }},
  "missing": ["goal | topic"],
  "questions": ["必要澄清问题"]
}}

要求：
- 不要编造用户没有表达的资产。
- 图片存在时 creative_assets 必须包含 image_assets。
- 如果目标不明确，missing 包含 goal。
- 如果用户文字为空，missing 包含 topic。
- 只问必要问题，最多 2 个。
"""

    def build_user_prompt(self, normalized: UserInput) -> str:
        return self.user_prompt_template.format(
            text=normalized.text.strip() or "无",
            images=json_prompt(normalized.images),
        )


class IntakeVisionPromptBuilder(AgentPromptBuilder):
    system_prompt = (
        "你是 Nori Intaker 的视觉打标工序，只输出 JSON。"
        "你收到一段用户需求 + 一张候选素材图，"
        "请结合需求理解图片内容、用途，为这张图填一份语义标签。"
    )

    user_prompt_template = (
        "用户的内容创作需求：\n{user_text}\n\n"
        "下面是一张候选素材图。请结合上面的需求理解这张图，填一份标签：\n"
        "{{\n"
        '  "vision_roles": [<1-3 个>],   // brand_logo / ip_character / product_shot / '
        'scene_photo / lifestyle / data_chart / reference_style / raw_material / '
        'portrait / unknown\n'
        '  "subject": "<一句话描述图中主体 + 与用户需求的关联，<=60 字>",\n'
        '  "brand_signals": ["<画面里可识别的品牌字标 / logo / 产品名>", ...],\n'
        '  "usable_for": [<cover / body / background_only / not_usable>],\n'
        '  "quality": "high|medium|low"\n'
        "}}\n\n"
        "严格规则：\n"
        "  - vision_roles 必须从给定字典里挑\n"
        "  - 看不清就用 unknown / not_usable / low\n"
        "  - 不要编造未出现在画面里的品牌名\n\n"
        '输出 JSON（只输出这个对象，不要包裭）。'
    )

    def build_user_prompt(self, user_text: str) -> str:
        return self.user_prompt_template.format(user_text=user_text)


__all__ = ["IntakeTextPromptBuilder", "IntakeVisionPromptBuilder"]
