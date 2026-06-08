"""Context models for agent-call assembly."""
from __future__ import annotations

from typing import Any

from nori._compat import dataclass, field
from nori.core.contracts import mapping, mapping_list


@dataclass(slots=True)
class ContextSource:
    source_type: str = ""
    ref: str = ""
    payload: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {"source_type": self.source_type, "ref": self.ref, "payload": dict(self.payload)}

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "ContextSource":
        data = mapping(data)
        return cls(
            source_type=str(data.get("source_type") or data.get("type") or ""),
            ref=str(data.get("ref") or ""),
            payload=mapping(data.get("payload")),
        )


@dataclass(slots=True)
class ContextTrace:
    resolver: str = "ContextResolver"
    source_refs: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {"resolver": self.resolver, "source_refs": list(self.source_refs), "notes": list(self.notes)}


@dataclass(slots=True)
class ContextSlice:
    """One typed business-context unit available to agent-specific views."""

    kind: str
    payload: dict[str, Any] = field(default_factory=dict)
    scope: dict[str, Any] = field(default_factory=dict)
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    confidence: float = 1.0
    priority: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "payload": dict(self.payload),
            "scope": dict(self.scope),
            "source_refs": [dict(item) for item in self.source_refs],
            "confidence": self.confidence,
            "priority": self.priority,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "ContextSlice":
        data = mapping(data)
        return cls(
            kind=str(data.get("kind") or ""),
            payload=mapping(data.get("payload")),
            scope=mapping(data.get("scope")),
            source_refs=mapping_list(data.get("source_refs")),
            confidence=float(data.get("confidence") if data.get("confidence") is not None else 1.0),
            priority=int(data.get("priority") or 0),
        )


@dataclass(slots=True)
class ContextView:
    """Agent-specific projection of a task ContextPack."""

    agent_name: str
    task_id: str = ""
    slices: list[ContextSlice] = field(default_factory=list)
    trace: ContextTrace = field(default_factory=ContextTrace)

    @property
    def kinds(self) -> list[str]:
        return [item.kind for item in self.slices]

    @property
    def payload(self) -> dict[str, Any]:
        return {item.kind: dict(item.payload) for item in self.slices}

    def slice(self, kind: str) -> ContextSlice | None:
        for item in self.slices:
            if item.kind == kind:
                return item
        return None

    def to_dict(self) -> dict[str, Any]:
        return {
            "agent_name": self.agent_name,
            "task_id": self.task_id,
            "slices": [item.to_dict() for item in self.slices],
            "trace": self.trace.to_dict(),
        }


@dataclass(slots=True)
class ContextBundle:
    session_id: str = ""
    task_id: str = ""
    user_id: str = ""
    goal: str = ""
    sources: list[ContextSource] = field(default_factory=list)
    memory: list[dict[str, Any]] = field(default_factory=list)
    artifacts: list[dict[str, Any]] = field(default_factory=list)
    payload: dict[str, Any] = field(default_factory=dict)
    trace: ContextTrace = field(default_factory=ContextTrace)

    def to_dict(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "task_id": self.task_id,
            "user_id": self.user_id,
            "goal": self.goal,
            "sources": [source.to_dict() for source in self.sources],
            "memory": [dict(item) for item in self.memory],
            "artifacts": [dict(item) for item in self.artifacts],
            "payload": dict(self.payload),
            "trace": self.trace.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "ContextBundle":
        data = mapping(data)
        return cls(
            session_id=str(data.get("session_id") or ""),
            task_id=str(data.get("task_id") or ""),
            user_id=str(data.get("user_id") or ""),
            goal=str(data.get("goal") or ""),
            sources=[ContextSource.from_dict(item) for item in mapping_list(data.get("sources"))],
            memory=mapping_list(data.get("memory")),
            artifacts=mapping_list(data.get("artifacts")),
            payload=mapping(data.get("payload")),
            trace=ContextTrace(**mapping(data.get("trace"))) if data.get("trace") else ContextTrace(),
        )
