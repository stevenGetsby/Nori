"""Input/output contracts for CoverDirectorAgent."""
from __future__ import annotations

from nori.content_generation.models import CoverResult, NoteDraft
from nori.core import UserAsset
from nori.market_analysis.models import NoteSkill

__all__ = ["CoverResult", "NoteDraft", "NoteSkill", "UserAsset"]
