"""User and account profile contracts."""
from __future__ import annotations

from typing import Any

from nori._compat import dataclass, field
from nori.core.contracts import mapping as _mapping
from nori.core.contracts import mapping_list as _mapping_list
from nori.core.contracts import string_list as _string_list
from nori.core.model_helpers import dict_rows as _dict_rows


@dataclass(slots=True)
class UserProfile:
    """Long-lived user/account/brand profile used before task-specific work."""

    user_id: str = ""
    display_name: str = ""
    platform: str = "xhs"
    account_profile: dict[str, Any] = field(default_factory=dict)
    brand_profile: dict[str, Any] = field(default_factory=dict)
    preferences: dict[str, Any] = field(default_factory=dict)
    constraints: list[str] = field(default_factory=list)
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "user_id": self.user_id,
            "display_name": self.display_name,
            "platform": self.platform,
            "account_profile": dict(self.account_profile),
            "brand_profile": dict(self.brand_profile),
            "preferences": dict(self.preferences),
            "constraints": list(self.constraints),
            "source_refs": _dict_rows(self.source_refs),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "UserProfile":
        data = _mapping(data)
        return cls(
            user_id=str(data.get("user_id") or ""),
            display_name=str(data.get("display_name") or data.get("name") or ""),
            platform=str(data.get("platform") or "xhs"),
            account_profile=_mapping(data.get("account_profile")),
            brand_profile=_mapping(data.get("brand_profile")),
            preferences=_mapping(data.get("preferences")),
            constraints=_string_list(data.get("constraints")),
            source_refs=_mapping_list(data.get("source_refs")),
            metadata=_mapping(data.get("metadata")),
        )


__all__ = ["UserProfile"]
