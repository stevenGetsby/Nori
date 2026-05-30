"""Memory retrieval helpers used by context assembly."""
from __future__ import annotations

from nori._compat import dataclass

from .models import MemoryRecord
from .store import MemoryStore


@dataclass(slots=True)
class MemoryQuery:
    text: str = ""
    user_id: str = ""
    session_id: str = ""
    limit: int = 8


class MemoryRetriever:
    """Small retrieval adapter around a MemoryStore."""

    def __init__(self, store: MemoryStore) -> None:
        self.store = store

    def retrieve(self, query: MemoryQuery) -> list[MemoryRecord]:
        return self.store.search(
            query.text,
            user_id=query.user_id,
            session_id=query.session_id,
            limit=query.limit,
        )
