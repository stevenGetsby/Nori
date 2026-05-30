"""Rules for promoting task/session observations into stable memory."""
from __future__ import annotations

from .models import MemoryRecord, SessionMemory, StableProfile, utc_now_iso


class MemoryPromotionPolicy:
    """Conservative default memory promotion policy."""

    stable_tags = {"brand", "preference", "constraint", "positioning", "audience"}

    def promotable_records(self, session_memory: SessionMemory) -> list[MemoryRecord]:
        return [
            record
            for record in session_memory.records
            if record.scope == "stable" or bool(set(record.tags) & self.stable_tags)
        ]

    def promote(self, profile: StableProfile, session_memory: SessionMemory) -> StableProfile:
        existing = {record.text for record in profile.facts}
        for record in self.promotable_records(session_memory):
            if record.text and record.text not in existing:
                profile.facts.append(record)
                existing.add(record.text)
        profile.updated_at = utc_now_iso()
        return profile
