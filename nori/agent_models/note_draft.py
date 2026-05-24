"""Data models for NoteMakerAgent (skill + assets → xhs note draft)."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class UserAsset:
    """单条用户素材（图片或文本）。

    图片类型会被 Intaker 的 vision 打标工序填以下字段：
      vision_roles  brand_logo / ip_character / product_shot / scene_photo /
                    lifestyle / data_chart / reference_style / raw_material /
                    portrait / unknown
      subject       一句话主体描述（<=60 字）
      brand_signals 画面里可识别的品牌字标 / logo / 产品名
      usable_for    cover / body / background_only / not_usable
      quality       high / medium / low
    文本类型不打这些标。
    """
    kind: str                                       # image / text
    path: str = ""                                  # 图片本地路径；text 时为空
    text: str = ""                                  # 文本内容；image 时为空

    # Intaker vision 工序填充
    vision_roles: list[str] = field(default_factory=list)
    subject: str = ""
    brand_signals: list[str] = field(default_factory=list)
    usable_for: list[str] = field(default_factory=list)
    quality: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "path": self.path,
            "text": self.text,
            "vision_roles": list(self.vision_roles),
            "subject": self.subject,
            "brand_signals": list(self.brand_signals),
            "usable_for": list(self.usable_for),
            "quality": self.quality,
        }


@dataclass(slots=True)
class AssetBundle:
    """工序 2 整理后的素材包，给后续工序消费。"""
    main_images: list[UserAsset] = field(default_factory=list)
    aux_images: list[UserAsset] = field(default_factory=list)
    text_points: list[str] = field(default_factory=list)     # 卖点 / 描述短句
    brand_facts: list[str] = field(default_factory=list)     # 品牌名、口号、人设
    data_points: list[str] = field(default_factory=list)     # 数据 / 案例 / 数字

    def to_dict(self) -> dict[str, Any]:
        return {
            "main_images": [a.to_dict() for a in self.main_images],
            "aux_images": [a.to_dict() for a in self.aux_images],
            "text_points": list(self.text_points),
            "brand_facts": list(self.brand_facts),
            "data_points": list(self.data_points),
        }


@dataclass(slots=True)
class CandidateTitle:
    text: str
    rule_name: str = ""             # 命中的 title_rule.name
    rationale: str = ""             # 为什么这么写

    def to_dict(self) -> dict[str, Any]:
        return {
            "text": self.text,
            "rule_name": self.rule_name,
            "rationale": self.rationale,
        }


@dataclass(slots=True)
class NoteDraft:
    """NoteMakerAgent 的最终产出：一篇可发布的 xhs note。"""
    skill_id: str
    title: str
    body: str
    tags: list[str] = field(default_factory=list)
    comment_hook: str = ""
    cover_path: str = ""
    image_paths: list[str] = field(default_factory=list)
    candidate_titles: list[CandidateTitle] = field(default_factory=list)
    metrics_target: dict[str, Any] = field(default_factory=dict)
    asset_bundle: dict[str, Any] = field(default_factory=dict)
    validation: dict[str, Any] = field(default_factory=dict)
    llm_enhanced: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "skill_id": self.skill_id,
            "title": self.title,
            "body": self.body,
            "tags": list(self.tags),
            "comment_hook": self.comment_hook,
            "cover_path": self.cover_path,
            "image_paths": list(self.image_paths),
            "candidate_titles": [c.to_dict() for c in self.candidate_titles],
            "metrics_target": dict(self.metrics_target),
            "asset_bundle": dict(self.asset_bundle),
            "validation": dict(self.validation),
            "llm_enhanced": self.llm_enhanced,
        }
