"""Content generation domain models."""
from __future__ import annotations

from typing import Any

from nori._compat import dataclass, field
from nori.core import UserAsset
from nori.core.contracts import (
    bool_value as _bool,
    dict_list as _dict_list,
    mapping as _mapping,
    mapping_list as _mapping_list,
    string_list as _string_list,
)


@dataclass(slots=True)
class AssetBundle:
    """Curated asset package consumed by note composition."""

    main_images: list[UserAsset] = field(default_factory=list)
    aux_images: list[UserAsset] = field(default_factory=list)
    text_points: list[str] = field(default_factory=list)
    brand_facts: list[str] = field(default_factory=list)
    data_points: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "main_images": [a.to_dict() for a in self.main_images],
            "aux_images": [a.to_dict() for a in self.aux_images],
            "text_points": list(self.text_points),
            "brand_facts": list(self.brand_facts),
            "data_points": list(self.data_points),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "AssetBundle":
        data = _mapping(data)
        return cls(
            main_images=[UserAsset.from_dict(item) for item in _mapping_list(data.get("main_images"))],
            aux_images=[UserAsset.from_dict(item) for item in _mapping_list(data.get("aux_images"))],
            text_points=_string_list(data.get("text_points")),
            brand_facts=_string_list(data.get("brand_facts")),
            data_points=_string_list(data.get("data_points")),
        )


@dataclass(slots=True)
class CandidateTitle:
    """One candidate title proposed by NoteMaker."""

    text: str
    rule_name: str = ""
    rationale: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "text": self.text,
            "rule_name": self.rule_name,
            "rationale": self.rationale,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "CandidateTitle":
        data = _mapping(data)
        return cls(
            text=str(data.get("text") or ""),
            rule_name=str(data.get("rule_name") or ""),
            rationale=str(data.get("rationale") or ""),
        )


@dataclass(slots=True)
class NoteDraft:
    """Generated note draft before production packaging."""

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

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "NoteDraft":
        data = _mapping(data)
        return cls(
            skill_id=str(data.get("skill_id") or ""),
            title=str(data.get("title") or ""),
            body=str(data.get("body") or ""),
            tags=_string_list(data.get("tags")),
            comment_hook=str(data.get("comment_hook") or ""),
            cover_path=str(data.get("cover_path") or ""),
            image_paths=_string_list(data.get("image_paths")),
            candidate_titles=[
                CandidateTitle.from_dict(item)
                for item in _mapping_list(data.get("candidate_titles"))
            ],
            metrics_target=_mapping(data.get("metrics_target")),
            asset_bundle=_mapping(data.get("asset_bundle")),
            validation=_mapping(data.get("validation")),
            llm_enhanced=_bool(data.get("llm_enhanced")),
        )


@dataclass(slots=True)
class CoverResult:
    """Generated cover image artifact."""

    cover_path: str
    prompt: str
    size: str = ""
    reference_paths: list[str] = field(default_factory=list)
    source: str = ""
    extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "cover_path": self.cover_path,
            "prompt": self.prompt,
            "size": self.size,
            "reference_paths": list(self.reference_paths),
            "source": self.source,
            "extra": dict(self.extra),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "CoverResult":
        data = _mapping(data)
        return cls(
            cover_path=str(data.get("cover_path") or ""),
            prompt=str(data.get("prompt") or ""),
            size=str(data.get("size") or ""),
            reference_paths=_string_list(data.get("reference_paths")),
            source=str(data.get("source") or ""),
            extra=_mapping(data.get("extra")),
        )


@dataclass(slots=True)
class ContentPackage:
    """Generated content artifacts attached to a content task."""

    package_id: str = ""
    task_id: str = ""
    platform: str = "xhs"
    title: str = ""
    body: str = ""
    tags: list[str] = field(default_factory=list)
    cover_path: str = ""
    image_paths: list[str] = field(default_factory=list)
    prompts: dict[str, Any] = field(default_factory=dict)
    material_usage: list[dict[str, Any]] = field(default_factory=list)
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    status: str = "draft"
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "package_id": self.package_id,
            "task_id": self.task_id,
            "platform": self.platform,
            "title": self.title,
            "body": self.body,
            "tags": list(self.tags),
            "cover_path": self.cover_path,
            "image_paths": list(self.image_paths),
            "prompts": dict(self.prompts),
            "material_usage": _dict_list(self.material_usage),
            "source_refs": _dict_list(self.source_refs),
            "status": self.status,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "ContentPackage":
        data = _mapping(data)
        return cls(
            package_id=str(data.get("package_id") or ""),
            task_id=str(data.get("task_id") or ""),
            platform=str(data.get("platform") or "xhs"),
            title=str(data.get("title") or ""),
            body=str(data.get("body") or ""),
            tags=_string_list(data.get("tags")),
            cover_path=str(data.get("cover_path") or ""),
            image_paths=_string_list(data.get("image_paths")),
            prompts=_mapping(data.get("prompts")),
            material_usage=_dict_list(data.get("material_usage")),
            source_refs=_dict_list(data.get("source_refs")),
            status=str(data.get("status") or "draft"),
            metadata=_mapping(data.get("metadata")),
        )


AssetBundle.__module__ = __name__
CandidateTitle.__module__ = __name__
ContentPackage.__module__ = __name__
CoverResult.__module__ = __name__
NoteDraft.__module__ = __name__

__all__ = [
    "AssetBundle",
    "CandidateTitle",
    "ContentPackage",
    "CoverResult",
    "NoteDraft",
    "UserAsset",
]
