"""Asset contracts shared across planning, generation, and review."""
from __future__ import annotations

from typing import Any

from nori._compat import dataclass, field
from nori.core.contracts import mapping as _mapping
from nori.core.contracts import mapping_list as _mapping_list
from nori.core.contracts import string_list as _string_list


@dataclass(slots=True)
class UserAsset:
    """One user-provided image or text asset shared across workflow stages."""

    kind: str
    path: str = ""
    text: str = ""
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

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "UserAsset":
        data = _mapping(data)
        kind = str(data.get("kind") or "")
        if not kind:
            kind = "image" if data.get("path") else "text" if data.get("text") else ""
        return cls(
            kind=kind,
            path=str(data.get("path") or ""),
            text=str(data.get("text") or ""),
            vision_roles=_string_list(data.get("vision_roles"), drop_blank=True),
            subject=str(data.get("subject") or ""),
            brand_signals=_string_list(data.get("brand_signals"), drop_blank=True),
            usable_for=_string_list(data.get("usable_for"), drop_blank=True),
            quality=str(data.get("quality") or ""),
        )


@dataclass(slots=True)
class AssetRecord:
    """A normalized client or production asset reference."""

    asset_id: str = ""
    kind: str = ""
    path: str = ""
    text: str = ""
    usage: list[str] = field(default_factory=list)
    status: str = "available"
    tags: list[str] = field(default_factory=list)
    source: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "asset_id": self.asset_id,
            "kind": self.kind,
            "path": self.path,
            "text": self.text,
            "usage": list(self.usage),
            "status": self.status,
            "tags": list(self.tags),
            "source": self.source,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "AssetRecord":
        data = _mapping(data)
        return cls(
            asset_id=str(data.get("asset_id") or data.get("id") or ""),
            kind=str(data.get("kind") or ""),
            path=str(data.get("path") or ""),
            text=str(data.get("text") or ""),
            usage=_string_list(data.get("usage") or data.get("usable_for")),
            status=str(data.get("status") or "available"),
            tags=_string_list(data.get("tags")),
            source=str(data.get("source") or ""),
            metadata=_mapping(data.get("metadata")),
        )


@dataclass(slots=True)
class AssetLibrary:
    """Project-level asset index for source materials and generated assets."""

    library_id: str = ""
    assets: list[AssetRecord] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "library_id": self.library_id,
            "assets": [asset.to_dict() for asset in self.assets],
            "notes": list(self.notes),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "AssetLibrary":
        data = _mapping(data)
        return cls(
            library_id=str(data.get("library_id") or ""),
            assets=[AssetRecord.from_dict(item) for item in _mapping_list(data.get("assets"))],
            notes=_string_list(data.get("notes")),
            metadata=_mapping(data.get("metadata")),
        )

    def get(self, asset_id: str) -> AssetRecord | None:
        for asset in self.assets:
            if asset.asset_id == asset_id:
                return asset
        return None

    def usable_assets(self, usage: str | None = None) -> list[AssetRecord]:
        return [
            asset
            for asset in self.assets
            if asset.status == "available" and (usage is None or usage in asset.usage)
        ]


__all__ = ["AssetLibrary", "AssetRecord", "UserAsset"]
