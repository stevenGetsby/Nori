"""Typed identifiers for backend experiment storage."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ContentCaseRef:
    """Stable identity for one content-production case."""

    case_id: str

    def __post_init__(self) -> None:
        if not str(self.case_id or "").strip():
            raise ValueError("case_id is required")


@dataclass(frozen=True)
class ContentRunRef:
    """Stable identity for one content-production run."""

    case_id: str
    run_id: str

    def __post_init__(self) -> None:
        if not str(self.case_id or "").strip():
            raise ValueError("case_id is required")
        if not str(self.run_id or "").strip():
            raise ValueError("run_id is required")
