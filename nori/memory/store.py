"""Memory store interfaces and local implementation."""
from __future__ import annotations

from typing import Protocol

from .models import MemoryRecord, SessionMemory, StableProfile, TaskMemory


class MemoryStore(Protocol):
    """Storage boundary for stable, session, and task memory."""

    def get_profile(self, profile_id: str) -> StableProfile | None:
        ...

    def save_profile(self, profile: StableProfile) -> StableProfile:
        ...

    def get_session_memory(self, session_id: str) -> SessionMemory | None:
        ...

    def save_session_memory(self, memory: SessionMemory) -> SessionMemory:
        ...

    def get_task_memory(self, task_id: str) -> TaskMemory | None:
        ...

    def save_task_memory(self, memory: TaskMemory) -> TaskMemory:
        ...

    def search(self, query: str, *, user_id: str = "", session_id: str = "", limit: int = 8) -> list[MemoryRecord]:
        ...


class InMemoryMemoryStore:
    """Deterministic in-process memory store for tests and local runs."""

    def __init__(self) -> None:
        self.profiles: dict[str, StableProfile] = {}
        self.sessions: dict[str, SessionMemory] = {}
        self.tasks: dict[str, TaskMemory] = {}

    def get_profile(self, profile_id: str) -> StableProfile | None:
        return self.profiles.get(profile_id)

    def save_profile(self, profile: StableProfile) -> StableProfile:
        self.profiles[profile.profile_id or profile.user_id] = profile
        return profile

    def get_session_memory(self, session_id: str) -> SessionMemory | None:
        return self.sessions.get(session_id)

    def save_session_memory(self, memory: SessionMemory) -> SessionMemory:
        self.sessions[memory.session_id] = memory
        return memory

    def get_task_memory(self, task_id: str) -> TaskMemory | None:
        return self.tasks.get(task_id)

    def save_task_memory(self, memory: TaskMemory) -> TaskMemory:
        self.tasks[memory.task_id] = memory
        return memory

    def search(self, query: str, *, user_id: str = "", session_id: str = "", limit: int = 8) -> list[MemoryRecord]:
        terms = [term.lower() for term in query.split() if term.strip()]
        records: list[MemoryRecord] = []
        for profile in self.profiles.values():
            if user_id and profile.user_id != user_id:
                continue
            records.extend(profile.facts)
        if session_id and session_id in self.sessions:
            records.extend(self.sessions[session_id].records)
        for task in self.tasks.values():
            if session_id and task.session_id != session_id:
                continue
            records.extend(task.records)
        if terms:
            records = [record for record in records if any(term in record.text.lower() for term in terms)]
        return records[:limit]
