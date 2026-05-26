"""Input/output contracts for NoteMakerAgent."""
from __future__ import annotations

from nori.content_generation.models import AssetBundle, CandidateTitle, NoteDraft
from nori.core import UserAsset
from nori.market_analysis.models import NoteSkill

__all__ = ["AssetBundle", "CandidateTitle", "NoteDraft", "NoteSkill", "UserAsset"]
