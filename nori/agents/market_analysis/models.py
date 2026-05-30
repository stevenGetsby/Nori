"""Market analysis domain models."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from nori._compat import dataclass, field
from nori.core.contracts import (
    bool_value as _bool,
    dict_list as _dict_list,
    int_value as _int,
    mapping as _mapping,
    mapping_list as _mapping_list,
    optional_str as _optional_str,
    string_list as _coerce_string_list,
)


@dataclass(slots=True)
class XHSNoteSample:
    """One local Xiaohongshu note sample restored from collected metadata."""

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

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "XHSNoteSample":
        data = _mapping(data)
        metrics = {
            str(key): _int(value)
            for key, value in _mapping(data.get("metrics")).items()
        }
        return cls(
            meta_path=Path(str(data.get("meta_path") or "")),
            category=str(data.get("category") or ""),
            author_id=str(data.get("author_id") or ""),
            author_name=str(data.get("author_name") or ""),
            note_id=str(data.get("note_id") or ""),
            title=str(data.get("title") or ""),
            desc=str(data.get("desc") or ""),
            tags=_string_list(data.get("tags")),
            metrics=metrics,
            image_count=_int(data.get("image_count")),
            note_type=str(data.get("note_type") or ""),
            note_url=str(data.get("note_url") or ""),
        )


@dataclass(slots=True)
class XHSSeedSkillDraft:
    """Single-note seed-skill draft derived from one XHS note."""

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

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "XHSSeedSkillDraft":
        data = _mapping(data)
        return cls(
            skill_id=str(data.get("skill_id") or data.get("id") or ""),
            category=str(data.get("category") or ""),
            match=_mapping(data.get("match")),
            craft=_mapping(data.get("craft")),
            evidence=_mapping(data.get("evidence")),
            validation=_mapping(data.get("validation")),
            type=str(data.get("type") or "xhs_note_seed_skill"),
            status=str(data.get("status") or "single_note_draft"),
            platform=str(data.get("platform") or "小红书"),
            source_scope=str(data.get("source_scope") or "single_note"),
        )


@dataclass(slots=True)
class NoteEvidence:
    """One evidence note backing a reusable NoteSkill."""

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

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "NoteEvidence":
        data = _mapping(data)
        return cls(
            note_id=str(data.get("note_id") or ""),
            note_url=str(data.get("note_url") or ""),
            title=str(data.get("title") or ""),
            liked=_int(data.get("liked")),
            collected=_int(data.get("collected")),
            keyword=str(data.get("keyword") or ""),
            cover_path=_optional_str(data.get("cover_path")),
            image_paths=_string_list(data.get("image_paths")),
            video_path=_optional_str(data.get("video_path")),
            quoted_segments=_string_list(data.get("quoted_segments")),
        )


@dataclass(slots=True)
class NoteSkill:
    """Reusable XHS note-writing skill learned from market evidence."""

    skill_id: str
    label: str
    goal: str
    note_type: str
    tone: str
    creative_goal: str
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

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "NoteSkill":
        data = _mapping(data)
        return cls(
            skill_id=str(data.get("skill_id") or data.get("id") or ""),
            label=str(data.get("label") or ""),
            goal=str(data.get("goal") or ""),
            note_type=str(data.get("note_type") or ""),
            tone=str(data.get("tone") or ""),
            creative_goal=str(data.get("creative_goal") or ""),
            title_rules=_dict_list(data.get("title_rules")),
            opening_rules=_dict_list(data.get("opening_rules")),
            body_structure=_dict_list(data.get("body_structure")),
            interaction_rules=_dict_list(data.get("interaction_rules")),
            visual_rules=_dict_list(data.get("visual_rules")),
            cover_rules=_dict_list(data.get("cover_rules")),
            avoid_rules=_string_list(data.get("avoid_rules")),
            metrics_summary=_mapping(data.get("metrics_summary")),
            evidence_notes=[NoteEvidence.from_dict(item) for item in _mapping_list(data.get("evidence_notes"))],
            cluster_signals=_mapping(data.get("cluster_signals")),
        )


@dataclass(slots=True)
class SessionSkillReport:
    """Search -> clustering -> learned NoteSkill session report."""

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

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "SessionSkillReport":
        data = _mapping(data)
        return cls(
            context=_mapping(data.get("context")),
            keywords=_string_list(data.get("keywords")),
            skills=[NoteSkill.from_dict(item) for item in _mapping_list(data.get("skills"))],
            coverage=_mapping(data.get("coverage")),
            leftover_note_ids=_string_list(data.get("leftover_note_ids")),
            source_data_dir=str(data.get("source_data_dir") or ""),
            source_keyword_dirs={str(key): str(value) for key, value in _mapping(data.get("source_keyword_dirs")).items()},
            source_db=str(data.get("source_db") or ""),
            insufficient=_dict_list(data.get("insufficient")),
            llm_enhanced=_bool(data.get("llm_enhanced")),
        )


@dataclass(slots=True)
class CompetitorSample:
    """A normalized competitor or benchmark content sample."""

    sample_id: str = ""
    platform: str = "xhs"
    author_name: str = ""
    note_id: str = ""
    title: str = ""
    url: str = ""
    keyword: str = ""
    metrics: dict[str, Any] = field(default_factory=dict)
    summary: str = ""
    content_angles: list[str] = field(default_factory=list)
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "sample_id": self.sample_id,
            "platform": self.platform,
            "author_name": self.author_name,
            "note_id": self.note_id,
            "title": self.title,
            "url": self.url,
            "keyword": self.keyword,
            "metrics": dict(self.metrics),
            "summary": self.summary,
            "content_angles": list(self.content_angles),
            "source_refs": _dict_list(self.source_refs),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "CompetitorSample":
        data = _mapping(data)
        return cls(
            sample_id=str(data.get("sample_id") or data.get("id") or ""),
            platform=str(data.get("platform") or "xhs"),
            author_name=str(data.get("author_name") or data.get("author") or ""),
            note_id=str(data.get("note_id") or ""),
            title=str(data.get("title") or ""),
            url=str(data.get("url") or data.get("note_url") or ""),
            keyword=str(data.get("keyword") or ""),
            metrics=_mapping(data.get("metrics")),
            summary=str(data.get("summary") or ""),
            content_angles=_string_list(data.get("content_angles") or data.get("angles")),
            source_refs=_dict_list(data.get("source_refs")),
            metadata=_mapping(data.get("metadata")),
        )


@dataclass(slots=True)
class CompetitorResearch:
    """Project-level benchmark evidence collected from competitor content."""

    research_id: str = ""
    platform: str = "xhs"
    keywords: list[str] = field(default_factory=list)
    samples: list[CompetitorSample] = field(default_factory=list)
    insights: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "research_id": self.research_id,
            "platform": self.platform,
            "keywords": list(self.keywords),
            "samples": [sample.to_dict() for sample in self.samples],
            "insights": list(self.insights),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "CompetitorResearch":
        data = _mapping(data)
        return cls(
            research_id=str(data.get("research_id") or ""),
            platform=str(data.get("platform") or "xhs"),
            keywords=_string_list(data.get("keywords")),
            samples=[CompetitorSample.from_dict(item) for item in _mapping_list(data.get("samples"))],
            insights=_string_list(data.get("insights")),
            metadata=_mapping(data.get("metadata")),
        )

    def top_samples(self, metric: str = "liked", limit: int = 5) -> list[CompetitorSample]:
        return sorted(
            self.samples,
            key=lambda sample: _metric_value(sample.metrics, metric),
            reverse=True,
        )[: max(0, limit)]

    def to_task_references(self, limit: int = 5) -> list[dict[str, Any]]:
        refs = []
        for sample in self.top_samples(limit=limit):
            refs.append({
                "source": "competitor_research",
                "sample_id": sample.sample_id,
                "platform": sample.platform,
                "note_id": sample.note_id,
                "title": sample.title,
                "keyword": sample.keyword,
                "url": sample.url,
            })
        return refs


def _metric_value(metrics: dict[str, Any], key: str) -> float:
    aliases = {
        "liked": ("liked", "likes"),
        "collected": ("collected", "collections", "saves"),
    }
    keys = aliases.get(key, (key,))
    for item in keys:
        try:
            value = metrics.get(item)
            if value is not None:
                return float(value or 0)
        except (TypeError, ValueError):
            continue
    return 0.0


CompetitorSample.__module__ = __name__
CompetitorResearch.__module__ = __name__
NoteEvidence.__module__ = __name__
NoteSkill.__module__ = __name__
SessionSkillReport.__module__ = __name__
XHSNoteSample.__module__ = __name__
XHSSeedSkillDraft.__module__ = __name__


def _string_list(value: Any) -> list[str]:
    return _coerce_string_list(value, drop_blank=True)


__all__ = [
    "CompetitorResearch",
    "CompetitorSample",
    "NoteEvidence",
    "NoteSkill",
    "SessionSkillReport",
    "XHSNoteSample",
    "XHSSeedSkillDraft",
]
