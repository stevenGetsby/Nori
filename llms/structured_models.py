"""Structured LLM helper result dataclass contracts."""
from __future__ import annotations

from typing import Any

from nori._compat import dataclass, field


@dataclass(slots=True)
class StructuredCallResult:
    data: dict[str, Any] | None = None
    raw: str = ""
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.error is None and self.data is not None


@dataclass(slots=True)
class IntentLLMResult:
    """LLM intent extraction result."""

    fields: dict[str, str] = field(default_factory=dict)
    candidates: dict[str, list[str]] = field(default_factory=dict)
    raw: str = ""
    model: str | None = None
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.error is None and bool(self.fields)


@dataclass(slots=True)
class TargetSelectionResult:
    """LLM edit-target selection result."""

    target_selector: str | None = None
    refined_instruction: str | None = None
    alternatives: list[str] = field(default_factory=list)
    confidence: str = "low"
    reason: str | None = None
    raw: str = ""
    model: str | None = None
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.error is None and self.target_selector is not None


__all__ = ["IntentLLMResult", "StructuredCallResult", "TargetSelectionResult"]
