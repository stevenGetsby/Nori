"""Data models for the Intaker Agent."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .base import Context, Intention
from .note_draft import UserAsset


@dataclass(slots=True)
class UserInput:
    text: str
    images: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "text": self.text,
            "images": list(self.images),
        }


@dataclass(slots=True)
class IntakeResult:
    intention: Intention
    context: Context
    missing: list[str]
    questions: list[str]
    assets: list[UserAsset] = field(default_factory=list)  # 打过 vision tag 的资产池

    @property
    def ready(self) -> bool:
        return not self.missing

    def to_dict(self) -> dict[str, Any]:
        return {
            "intention": dict(self.intention),
            "context": dict(self.context),
            "ready": self.ready,
            "missing": list(self.missing),
            "questions": list(self.questions),
            "assets": [a.to_dict() for a in self.assets],
        }


__all__ = ["IntakeResult", "UserInput"]
