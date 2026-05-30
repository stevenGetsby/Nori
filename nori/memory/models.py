"""Typed memory models for Nori runtime state."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from nori._compat import dataclass, field
from nori.core.contracts import mapping, mapping_list, string_list


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(slots=True)
class MemoryRecord:
    """One retrievable memory fact with provenance."""

    record_id: str = ""
    scope: str = "task"
    text: str = ""
    tags: list[str] = field(default_factory=list)
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> dict[str, Any]:
        return {
            "record_id": self.record_id,
            "scope": self.scope,
            "text": self.text,
            "tags": list(self.tags),
            "source_refs": [dict(item) for item in self.source_refs],
            "metadata": dict(self.metadata),
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "MemoryRecord":
        data = mapping(data)
        return cls(
            record_id=str(data.get("record_id") or data.get("id") or ""),
            scope=str(data.get("scope") or "task"),
            text=str(data.get("text") or ""),
            tags=string_list(data.get("tags"), drop_blank=True),
            source_refs=mapping_list(data.get("source_refs")),
            metadata=mapping(data.get("metadata")),
            created_at=str(data.get("created_at") or utc_now_iso()),
        )


@dataclass(slots=True)
class StableProfile:
    """Long-lived profile memory shared across sessions."""

    profile_id: str = ""
    user_id: str = ""
    brand_profile: dict[str, Any] = field(default_factory=dict)
    account_profile: dict[str, Any] = field(default_factory=dict)
    preferences: dict[str, Any] = field(default_factory=dict)
    constraints: list[str] = field(default_factory=list)
    facts: list[MemoryRecord] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    updated_at: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> dict[str, Any]:
        return {
            "profile_id": self.profile_id,
            "user_id": self.user_id,
            "brand_profile": dict(self.brand_profile),
            "account_profile": dict(self.account_profile),
            "preferences": dict(self.preferences),
            "constraints": list(self.constraints),
            "facts": [item.to_dict() for item in self.facts],
            "metadata": dict(self.metadata),
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "StableProfile":
        data = mapping(data)
        return cls(
            profile_id=str(data.get("profile_id") or ""),
            user_id=str(data.get("user_id") or ""),
            brand_profile=mapping(data.get("brand_profile")),
            account_profile=mapping(data.get("account_profile")),
            preferences=mapping(data.get("preferences")),
            constraints=string_list(data.get("constraints"), drop_blank=True),
            facts=[MemoryRecord.from_dict(item) for item in mapping_list(data.get("facts"))],
            metadata=mapping(data.get("metadata")),
            updated_at=str(data.get("updated_at") or utc_now_iso()),
        )


@dataclass(slots=True)
class SessionMemory:
    """Memory accumulated inside one user session."""

    session_id: str = ""
    user_id: str = ""
    records: list[MemoryRecord] = field(default_factory=list)
    artifact_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    updated_at: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "records": [item.to_dict() for item in self.records],
            "artifact_refs": list(self.artifact_refs),
            "metadata": dict(self.metadata),
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "SessionMemory":
        data = mapping(data)
        return cls(
            session_id=str(data.get("session_id") or ""),
            user_id=str(data.get("user_id") or ""),
            records=[MemoryRecord.from_dict(item) for item in mapping_list(data.get("records"))],
            artifact_refs=string_list(data.get("artifact_refs"), drop_blank=True),
            metadata=mapping(data.get("metadata")),
            updated_at=str(data.get("updated_at") or utc_now_iso()),
        )


@dataclass(slots=True)
class TaskMemory:
    """Memory specific to one task goal or workflow run."""

    task_id: str = ""
    session_id: str = ""
    goal: str = ""
    records: list[MemoryRecord] = field(default_factory=list)
    artifact_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    updated_at: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "session_id": self.session_id,
            "goal": self.goal,
            "records": [item.to_dict() for item in self.records],
            "artifact_refs": list(self.artifact_refs),
            "metadata": dict(self.metadata),
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "TaskMemory":
        data = mapping(data)
        return cls(
            task_id=str(data.get("task_id") or ""),
            session_id=str(data.get("session_id") or ""),
            goal=str(data.get("goal") or ""),
            records=[MemoryRecord.from_dict(item) for item in mapping_list(data.get("records"))],
            artifact_refs=string_list(data.get("artifact_refs"), drop_blank=True),
            metadata=mapping(data.get("metadata")),
            updated_at=str(data.get("updated_at") or utc_now_iso()),
        )
