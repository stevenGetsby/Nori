"""Market-analysis module."""
from __future__ import annotations

from nori.core import MarketAnalysis
from nori.core.lazy_exports import lazy_export

from .schemas import (
    CompetitorResearch,
    CompetitorSample,
    NoteEvidence,
    NoteSkill,
    SessionSkillReport,
    XHSNoteSample,
    XHSSeedSkillDraft,
)
from .note_skill_fixture import load_note_skills, note_skill_fixture, write_note_skill_fixture

_LAZY_EXPORTS = {
    "MarketAnalysisFacade": "facade",
    "XHSNoteAnalyzer": "xhs_note_analyzer",
    "XHSNoteAnalyzerLLMError": "xhs_note_analyzer",
}

__all__ = [
    "CompetitorResearch",
    "CompetitorSample",
    "MarketAnalysis",
    "MarketAnalysisFacade",
    "NoteEvidence",
    "NoteSkill",
    "load_note_skills",
    "note_skill_fixture",
    "SessionSkillReport",
    "write_note_skill_fixture",
    "XHSNoteAnalyzer",
    "XHSNoteAnalyzerLLMError",
    "XHSNoteSample",
    "XHSSeedSkillDraft",
]


def __getattr__(name: str):
    return lazy_export(__name__, _LAZY_EXPORTS, name)
