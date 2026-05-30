"""Session models for user-scoped runtime workspaces."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from nori._compat import dataclass, field
from nori.core.contracts import mapping, mapping_list, string_list


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(slots=True)
class Turn:
    turn_id: str = field(default_factory=lambda: new_id("turn"))
    role: str = "user"
    content: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> dict[str, Any]:
        return {
            "turn_id": self.turn_id,
            "role": self.role,
            "content": self.content,
            "metadata": dict(self.metadata),
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "Turn":
        data = mapping(data)
        return cls(
            turn_id=str(data.get("turn_id") or new_id("turn")),
            role=str(data.get("role") or "user"),
            content=str(data.get("content") or ""),
            metadata=mapping(data.get("metadata")),
            created_at=str(data.get("created_at") or utc_now_iso()),
        )


@dataclass(slots=True)
class TaskGoal:
    task_id: str = field(default_factory=lambda: new_id("task"))
    goal: str = ""
    status: str = "active"
    workflow_name: str = ""
    acceptance: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "goal": self.goal,
            "status": self.status,
            "workflow_name": self.workflow_name,
            "acceptance": list(self.acceptance),
            "metadata": dict(self.metadata),
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "TaskGoal":
        data = mapping(data)
        return cls(
            task_id=str(data.get("task_id") or new_id("task")),
            goal=str(data.get("goal") or ""),
            status=str(data.get("status") or "active"),
            workflow_name=str(data.get("workflow_name") or ""),
            acceptance=string_list(data.get("acceptance"), drop_blank=True),
            metadata=mapping(data.get("metadata")),
            created_at=str(data.get("created_at") or utc_now_iso()),
        )


@dataclass(slots=True)
class SessionEvent:
    event_id: str = field(default_factory=lambda: new_id("event"))
    event_type: str = ""
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "payload": dict(self.payload),
            "created_at": self.created_at,
        }


@dataclass(slots=True)
class Session:
    session_id: str = field(default_factory=lambda: new_id("session"))
    user_id: str = ""
    profile_id: str = ""
    status: str = "active"
    turns: list[Turn] = field(default_factory=list)
    task_goals: list[TaskGoal] = field(default_factory=list)
    events: list[SessionEvent] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=utc_now_iso)
    updated_at: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "profile_id": self.profile_id,
            "status": self.status,
            "turns": [turn.to_dict() for turn in self.turns],
            "task_goals": [goal.to_dict() for goal in self.task_goals],
            "events": [event.to_dict() for event in self.events],
            "metadata": dict(self.metadata),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "Session":
        data = mapping(data)
        return cls(
            session_id=str(data.get("session_id") or new_id("session")),
            user_id=str(data.get("user_id") or ""),
            profile_id=str(data.get("profile_id") or ""),
            status=str(data.get("status") or "active"),
            turns=[Turn.from_dict(item) for item in mapping_list(data.get("turns"))],
            task_goals=[TaskGoal.from_dict(item) for item in mapping_list(data.get("task_goals"))],
            events=[
                SessionEvent(event_type=str(item.get("event_type") or ""), payload=mapping(item.get("payload")))
                for item in mapping_list(data.get("events"))
            ],
            metadata=mapping(data.get("metadata")),
            created_at=str(data.get("created_at") or utc_now_iso()),
            updated_at=str(data.get("updated_at") or utc_now_iso()),
        )
