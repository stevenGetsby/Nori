"""Build a deterministic context bundle for an agent call."""
from __future__ import annotations

from typing import Any

from nori.memory import MemoryQuery, MemoryRetriever, MemoryStore

from nori.core import ContextPack

from .models import ContextBundle, ContextSlice, ContextSource, ContextTrace, ContextView


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

    def for_agent(
        self,
        agent_name: str,
        context_pack: ContextPack | dict[str, Any],
        *,
        required_kinds: list[str] | None = None,
    ) -> ContextView:
        pack = context_pack if isinstance(context_pack, ContextPack) else ContextPack.from_dict(context_pack)
        order = required_kinds or _default_agent_kinds(agent_name)
        available = [ContextSlice.from_dict(item) for item in pack.context_slices]
        selected = []
        for kind in order:
            selected.extend([item for item in available if item.kind == kind])
        return ContextView(
            agent_name=str(agent_name or ""),
            task_id=str(pack.task_intent.get("task_id") or ""),
            slices=selected,
            trace=ContextTrace(
                resolver=self.__class__.__name__,
                source_refs=[pack.context_pack_id] if pack.context_pack_id else [],
                notes=[f"context_view={agent_name}"],
            ),
        )

    def _memory_rows(self, query: str, *, user_id: str, session_id: str) -> list[dict[str, Any]]:
        if self.memory_store is None:
            return []
        retriever = MemoryRetriever(self.memory_store)
        records = retriever.retrieve(MemoryQuery(query, user_id=user_id, session_id=session_id, limit=self.memory_limit))
        return [record.to_dict() for record in records]


def _default_agent_kinds(agent_name: str) -> list[str]:
    if agent_name == "ContentSpecAgent":
        return [
            "task_intent",
            "brand_profile",
            "platform_strategy",
            "market_hotspots",
            "learned_skills",
            "content_strategy",
            "asset_context",
            "constraints",
        ]
    if agent_name == "ArtifactGenerationAgent":
        return ["task_intent", "content_strategy", "learned_skills", "asset_context", "constraints"]
    if agent_name == "ReviewGateAgent":
        return ["task_intent", "brand_profile", "platform_strategy", "content_strategy", "constraints"]
    return ["task_intent", "brand_profile", "market_hotspots", "asset_context", "constraints"]
