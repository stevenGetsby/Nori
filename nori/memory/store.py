"""Memory store interfaces backed by LangGraph store primitives."""
from __future__ import annotations

from typing import Any, Protocol

from langgraph.store.memory import InMemoryStore

from .schemas import MemoryRecord, SessionMemory, StableProfile, TaskMemory

PROFILE_NS = ("nori", "memory", "profiles")
SESSION_NS = ("nori", "memory", "sessions")
TASK_NS = ("nori", "memory", "tasks")
MEMORY_NS = ("nori", "memory")


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


class InMemoryMemoryStore(InMemoryStore):
    """Nori memory adapter built on LangGraph's in-process store.

    Nori keeps typed memory contracts and promotion policy, while LangGraph owns
    the generic namespace/key/value store behavior used by runtime agents.
    """

    def __init__(self, store: InMemoryStore | None = None) -> None:
        super().__init__()
        if store is not None:
            for namespace in store.list_namespaces():
                for item in store.search(namespace, limit=1000):
                    self.put(tuple(item.namespace), item.key, dict(item.value))

    def get_profile(self, profile_id: str) -> StableProfile | None:
        item = self.get(PROFILE_NS, profile_id)
        return StableProfile.from_dict(item.value) if item else None

    def save_profile(self, profile: StableProfile) -> StableProfile:
        self.put(PROFILE_NS, profile.profile_id or profile.user_id, profile.to_dict())
        return profile

    def get_session_memory(self, session_id: str) -> SessionMemory | None:
        item = self.get(SESSION_NS, session_id)
        return SessionMemory.from_dict(item.value) if item else None

    def save_session_memory(self, memory: SessionMemory) -> SessionMemory:
        self.put(SESSION_NS, memory.session_id, memory.to_dict())
        return memory

    def get_task_memory(self, task_id: str) -> TaskMemory | None:
        item = self.get(TASK_NS, task_id)
        return TaskMemory.from_dict(item.value) if item else None

    def save_task_memory(self, memory: TaskMemory) -> TaskMemory:
        self.put(TASK_NS, memory.task_id, memory.to_dict())
        return memory

    def search(
        self,
        query_or_namespace: str | tuple[str, ...] = "",
        /,
        *,
        query: str | None = None,
        filter: dict[str, Any] | None = None,
        limit: int = 8,
        offset: int = 0,
        refresh_ttl: bool | None = None,
        user_id: str = "",
        session_id: str = "",
    ):
        if isinstance(query_or_namespace, tuple):
            return super().search(
                query_or_namespace,
                query=query,
                filter=filter,
                limit=limit,
                offset=offset,
                refresh_ttl=refresh_ttl,
            )
        nori_query = str(query_or_namespace or query or "")
        terms = [term.lower() for term in nori_query.split() if term.strip()]
        records: list[MemoryRecord] = []
        for item in super().search(MEMORY_NS, query=nori_query or None, limit=max(limit * 3, limit)):
            records.extend(_records_from_item(item.value, user_id=user_id, session_id=session_id))
        if terms:
            records = [record for record in records if any(term in record.text.lower() for term in terms)]
        return records[:limit]


def _records_from_item(value: dict, *, user_id: str = "", session_id: str = "") -> list[MemoryRecord]:
    if "profile_id" in value or "facts" in value:
        profile = StableProfile.from_dict(value)
        if user_id and profile.user_id != user_id:
            return []
        return list(profile.facts)

    if "session_id" in value and "goal" not in value:
        session = SessionMemory.from_dict(value)
        if user_id and session.user_id != user_id:
            return []
        if session_id and session.session_id != session_id:
            return []
        return list(session.records)

    if "task_id" in value:
        task = TaskMemory.from_dict(value)
        if session_id and task.session_id != session_id:
            return []
        return list(task.records)

    return []


__all__ = [
    "InMemoryMemoryStore",
    "MEMORY_NS",
    "MemoryStore",
    "PROFILE_NS",
    "SESSION_NS",
    "TASK_NS",
]
