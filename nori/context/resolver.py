"""Build a deterministic context bundle for an agent call."""
from __future__ import annotations

from typing import Any

from nori.memory import MemoryQuery, MemoryRetriever, MemoryStore

from .models import ContextBundle, ContextSource, ContextTrace


class ContextResolver:
    """Resolve user input, session state, memory, and artifacts into context."""

    def __init__(self, *, memory_store: MemoryStore | None = None, memory_limit: int = 8) -> None:
        self.memory_store = memory_store
        self.memory_limit = memory_limit

    def build(
        self,
        *,
        session: Any | None = None,
        task_goal: Any | None = None,
        user_input: dict[str, Any] | None = None,
        artifacts: list[dict[str, Any]] | None = None,
        extra: dict[str, Any] | None = None,
    ) -> ContextBundle:
        session_id = str(getattr(session, "session_id", "") or "")
        user_id = str(getattr(session, "user_id", "") or "")
        task_id = str(getattr(task_goal, "task_id", "") or "")
        goal = str(getattr(task_goal, "goal", "") or "")
        sources = [
            ContextSource(source_type="user_input", ref="current", payload=dict(user_input or {})),
        ]
        artifact_rows = [dict(item) for item in (artifacts or [])]
        memory_rows = self._memory_rows(goal or str(user_input or ""), user_id=user_id, session_id=session_id)
        payload = {
            "input": dict(user_input or {}),
            "extra": dict(extra or {}),
        }
        trace = ContextTrace(
            source_refs=[source.ref for source in sources],
            notes=["memory_store=enabled" if self.memory_store else "memory_store=disabled"],
        )
        return ContextBundle(
            session_id=session_id,
            task_id=task_id,
            user_id=user_id,
            goal=goal,
            sources=sources,
            memory=memory_rows,
            artifacts=artifact_rows,
            payload=payload,
            trace=trace,
        )

    def _memory_rows(self, query: str, *, user_id: str, session_id: str) -> list[dict[str, Any]]:
        if self.memory_store is None:
            return []
        retriever = MemoryRetriever(self.memory_store)
        records = retriever.retrieve(MemoryQuery(query, user_id=user_id, session_id=session_id, limit=self.memory_limit))
        return [record.to_dict() for record in records]
