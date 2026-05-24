"""Data models for Xiaohongshu note analysis and seed skills."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class XHSNoteSample:
    meta_path: Path
    category: str
    author_id: str
    author_name: str
    note_id: str
    title: str
    desc: str
    tags: list[str] = field(default_factory=list)
    metrics: dict[str, int] = field(default_factory=dict)
    image_count: int = 0
    note_type: str = ""
    note_url: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "meta_path": str(self.meta_path),
            "category": self.category,
            "author_id": self.author_id,
            "author_name": self.author_name,
            "note_id": self.note_id,
            "title": self.title,
            "desc": self.desc,
            "tags": list(self.tags),
            "metrics": dict(self.metrics),
            "image_count": self.image_count,
            "note_type": self.note_type,
            "note_url": self.note_url,
        }


@dataclass(slots=True)
class XHSSeedSkillDraft:
    skill_id: str
    category: str
    match: dict[str, Any]
    craft: dict[str, Any]
    evidence: dict[str, Any]
    validation: dict[str, Any]
    type: str = "xhs_note_seed_skill"
    status: str = "single_note_draft"
    platform: str = "小红书"
    source_scope: str = "single_note"

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.skill_id,
            "type": self.type,
            "status": self.status,
            "platform": self.platform,
            "category": self.category,
            "source_scope": self.source_scope,
            "match": dict(self.match),
            "craft": dict(self.craft),
            "evidence": dict(self.evidence),
            "validation": dict(self.validation),
        }


@dataclass(slots=True)
class NoteEvidence:
    """单条 NoteSkill 的笔记证据。"""
    note_id: str
    note_url: str
    title: str
    liked: int
    collected: int
    keyword: str = ""
    cover_path: str | None = None
    image_paths: list[str] = field(default_factory=list)
    video_path: str | None = None
    quoted_segments: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "note_id": self.note_id,
            "note_url": self.note_url,
            "title": self.title,
            "liked": self.liked,
            "collected": self.collected,
            "keyword": self.keyword,
            "cover_path": self.cover_path,
            "image_paths": list(self.image_paths),
            "video_path": self.video_path,
            "quoted_segments": list(self.quoted_segments),
        }


@dataclass(slots=True)
class NoteSkill:
    """一类目标对应的完整笔记创作技能（本次会话产出）。"""
    skill_id: str
    label: str                                  # 给上层的人话标签
    goal: str                                   # tutorial / planting / debrief / opinion / news / rant
    note_type: str                              # 图文 / 视频 / 混合
    tone: str                                   # 科普 / 吐槽 / 朋友安利 / 专业测评
    creative_goal: str                          # 一句话定位
    title_rules: list[dict[str, str]] = field(default_factory=list)
    opening_rules: list[dict[str, str]] = field(default_factory=list)
    body_structure: list[dict[str, str]] = field(default_factory=list)
    interaction_rules: list[dict[str, str]] = field(default_factory=list)
    visual_rules: list[dict[str, str]] = field(default_factory=list)
    cover_rules: list[dict[str, str]] = field(default_factory=list)
    avoid_rules: list[str] = field(default_factory=list)
    metrics_summary: dict[str, Any] = field(default_factory=dict)
    evidence_notes: list[NoteEvidence] = field(default_factory=list)
    cluster_signals: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "skill_id": self.skill_id,
            "label": self.label,
            "goal": self.goal,
            "note_type": self.note_type,
            "tone": self.tone,
            "creative_goal": self.creative_goal,
            "title_rules": list(self.title_rules),
            "opening_rules": list(self.opening_rules),
            "body_structure": list(self.body_structure),
            "interaction_rules": list(self.interaction_rules),
            "visual_rules": list(self.visual_rules),
            "cover_rules": list(self.cover_rules),
            "avoid_rules": list(self.avoid_rules),
            "metrics_summary": dict(self.metrics_summary),
            "evidence_notes": [e.to_dict() for e in self.evidence_notes],
            "cluster_signals": dict(self.cluster_signals),
        }


@dataclass(slots=True)
class SessionSkillReport:
    """本次会话的搜索→聚类→技能产出报告。"""
    context: dict[str, Any]
    keywords: list[str]
    skills: list[NoteSkill]
    coverage: dict[str, Any] = field(default_factory=dict)
    leftover_note_ids: list[str] = field(default_factory=list)
    source_data_dir: str = ""
    source_keyword_dirs: dict[str, str] = field(default_factory=dict)
    source_db: str = ""
    insufficient: list[dict[str, Any]] = field(default_factory=list)
    llm_enhanced: bool = False

    def to_dict(self) -> dict[str, Any]:
        data = {
            "context": dict(self.context),
            "keywords": list(self.keywords),
            "skills": [s.to_dict() for s in self.skills],
            "coverage": dict(self.coverage),
            "leftover_note_ids": list(self.leftover_note_ids),
            "source_data_dir": self.source_data_dir,
            "source_keyword_dirs": dict(self.source_keyword_dirs),
            "insufficient": list(self.insufficient),
            "llm_enhanced": self.llm_enhanced,
        }
        if self.source_db:
            data["source_db"] = self.source_db
        return data


__all__ = [
    "XHSNoteSample",
    "XHSSeedSkillDraft",
    "NoteEvidence",
    "NoteSkill",
    "SessionSkillReport",
]
