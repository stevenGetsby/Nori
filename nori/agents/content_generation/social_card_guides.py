"""Reusable social-card design guidance for content generation specs."""
from __future__ import annotations

from typing import Any

from nori.core import ContentTask, UserAsset


SOURCE = "guizang_social_card_skill"


def social_card_profile(
    task: ContentTask,
    *,
    artifact_type: str,
    assets: list[UserAsset] | None = None,
) -> dict[str, Any]:
    """Return a Nori-native design profile distilled from social-card best practice."""
    platform = str(task.platform or "").strip().lower()
    if _is_xhs_image_post(platform, artifact_type):
        return _xhs_profile(task, assets or [])
    if _is_wechat_cover_pair(platform, artifact_type):
        return _wechat_profile(task)
    return {}


def social_card_acceptance_checks(profile: dict[str, Any]) -> list[str]:
    if not profile:
        return []
    checks = [
        "每张图只承载一个清晰观点，不把整篇正文塞进图片",
        "封面在手机缩略图下一眼看懂钩子和用户收益",
        "所有正文和关键主体落在平台安全区内",
        "截图、照片、生成图都必须服务于证据或场景，不做无意义装饰",
        "不得伪造截图、官方通知、用户背书、价格、认证或第三方证明",
    ]
    if profile.get("platform") == "xhs":
        checks.extend([
            "3:4 图文页填充感达标：有效内容覆盖至少 75% 画布高度",
            "页面结构有变化，不连续复用同一种标题加卡片版式",
        ])
    if profile.get("platform") == "wechat":
        checks.extend([
            "公众号 21:9 主封面和 1:1 方封面必须分别构图，不直接裁切复用",
            "1:1 方封面使用短标题，不挤入完整长标题和复杂副标题",
        ])
    return checks


def social_card_visual_rules(profile: dict[str, Any]) -> dict[str, Any]:
    if not profile:
        return {}
    return {
        "source": SOURCE,
        "core_principle": "先把内容变成视觉论证，再决定文字、证据和版式。",
        "style_modes": [
            {
                "mode": "editorial_eink",
                "stance": "杂志特写感，适合叙事、生活方式、观点和慢节奏解释。",
                "identity_checks": [
                    "标题使用宋体/衬线气质，背景至少有纸张、颗粒、墨迹或纹理层之一",
                    "至少使用大图、引语、边注、ledger 行或杂志栏结构之一",
                    "避免只有平铺纸色、mono 标签和孤立标题",
                ],
            },
            {
                "mode": "swiss_international",
                "stance": "工程化、系统化、数据化，适合产品更新、工具教程、对比和清单。",
                "identity_checks": [
                    "大标题用轻字重和严格左轴网格",
                    "全组只使用一个高饱和强调色",
                    "使用细线、矩阵、KPI、横条或编号陈述，不使用装饰渐变和随机形状",
                ],
            },
        ],
        "shared_rules": [
            "内容形状决定版式，不先套漂亮模板",
            "真实图片、截图或图表是证据层，不是背景填充",
            "一组图片必须通过网格、字体、色彩、页码/标签保持连续",
            "避免随机圆形、贴纸、光斑、装饰渐变、嵌套卡片和过度圆角",
        ],
        "image_rules": [
            "UI 截图、代码、表格等细节材料优先完整可读，必要时减少同页文字",
            "照片裁切必须保留主体、人脸、手、产品和关键文字",
            "生成图只生成视觉素材，不生成带标题、页码、logo 或假 UI 的成品海报",
        ],
    }


def cover_prompt_guidance(intent: dict[str, Any]) -> dict[str, Any]:
    spec = intent.get("content_design_spec") if isinstance(intent, dict) else None
    if not isinstance(spec, dict):
        return {}
    media_plan = spec.get("media_plan")
    if not isinstance(media_plan, dict):
        return {}
    profile = media_plan.get("social_card") or media_plan.get("wechat_cover_pair")
    return dict(profile) if isinstance(profile, dict) else {}


def _xhs_profile(task: ContentTask, assets: list[UserAsset]) -> dict[str, Any]:
    image_count = sum(1 for asset in assets if asset.kind == "image")
    return {
        "source": SOURCE,
        "platform": "xhs",
        "artifact": "social_card_carousel",
        "canvas": {
            "width": 1080,
            "height": 1440,
            "ratio": "3:4",
            "safe_area_px": {"left": 72, "right": 72, "top": 96, "bottom": 96},
            "export": "png",
        },
        "page_count": {"min": 5, "max": 9, "target": 6},
        "available_image_count": image_count,
        "compression_ladder": [
            "核心观点一句话",
            "读者刷完能获得什么",
            "拆成 4-8 个页面观点",
            "每页压成短钩子和必要解释",
            "复杂细节放正文，不塞进图片",
        ],
        "page_plan": [
            {"slot": "cover", "role": "hook_cover", "intent": "大钩子、一个强视觉、3-5 个底部关键词"},
            {"slot": "hotspot_bridge", "role": "problem_scene", "intent": "把热点或场景痛点说清楚"},
            {"slot": "account_fit", "role": "credibility", "intent": "说明账号、产品或经验为什么能参与这个话题"},
            {"slot": "proof_or_example", "role": "evidence", "intent": "给真实素材、截图、案例或对比"},
            {"slot": "method_or_choice", "role": "checklist_or_flow", "intent": "给可收藏的方法、清单、步骤或选择标准"},
            {"slot": "save_or_comment_cta", "role": "summary", "intent": "用三点总结、收藏理由或评论动作收口"},
        ],
        "layout_principles": [
            "Page 1 是封面钩子，Page 2-N 每页只讲一个观点",
            "图文页承载钩子、比较、清单和尖锐结论，正文承载细节和解释",
            "不要让每页都变成重复的标题加卡片；交替使用场景、对比、证据、清单、流程、总结",
            "如果连续出现大块空白，合并页面或补充证据、边注、ledger、引语或图像区域",
        ],
    }


def _wechat_profile(task: ContentTask) -> dict[str, Any]:
    title = task.title or task.topic
    return {
        "source": SOURCE,
        "platform": "wechat",
        "artifact": "wechat_cover_pair",
        "main_cover": {
            "width": 2100,
            "height": 900,
            "ratio": "21:9",
            "title": title,
            "intent": "保留完整或近完整标题、一个强视觉关系和清晰中心左侧阅读区",
        },
        "square_cover": {
            "width": 1080,
            "height": 1080,
            "ratio": "1:1",
            "intent": "从长标题提炼 4-10 字短标题，默认不放复杂副标题或图片",
        },
        "pair_rules": [
            "同一个 HTML/视觉系统内设计主封面和方封面，交付前并排检查",
            "方封面单独构图，不能从 21:9 主封面硬裁",
            "主封面避免中间空洞，标题、图像或结构需要撑住画面中心",
        ],
    }


def _is_xhs_image_post(platform: str, artifact_type: str) -> bool:
    return platform in {"xhs", "xiaohongshu", "rednote", "小红书"} and artifact_type == "image_text_post"


def _is_wechat_cover_pair(platform: str, artifact_type: str) -> bool:
    return platform in {"wechat", "wechat_public_account", "公众号"} and artifact_type == "article"


__all__ = [
    "SOURCE",
    "cover_prompt_guidance",
    "social_card_acceptance_checks",
    "social_card_profile",
    "social_card_visual_rules",
]
