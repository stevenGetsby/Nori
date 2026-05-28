"""Content-generation module."""
from __future__ import annotations

from nori.core import CandidateSet
from nori.core.lazy_exports import lazy_export

from .models import AssetBundle, CandidateTitle, ContentPackage, CoverResult, NoteDraft

_LAZY_EXPORTS = {
    "ContentGenerationFacade": "facade",
    "GenerationAgent": "generation",
    "ContentProducerAgent": "content_producer",
    "ContentProductionError": "content_producer",
    "produce_content_package": "content_producer",
    "CoverDirectorAgent": "cover_director",
    "CoverDirectorError": "cover_director",
    "make_cover": "cover_director",
    "NoteMakerAgent": "note_maker",
    "NoteMakerLLMError": "note_maker",
    "make_note": "note_maker",
}

__all__ = [
    "AssetBundle",
    "CandidateSet",
    "CandidateTitle",
    "ContentPackage",
    "ContentGenerationFacade",
    "ContentProducerAgent",
    "ContentProductionError",
    "GenerationAgent",
    "CoverDirectorAgent",
    "CoverDirectorError",
    "CoverResult",
    "NoteDraft",
    "NoteMakerAgent",
    "NoteMakerLLMError",
    "make_cover",
    "make_note",
    "produce_content_package",
]


def __getattr__(name: str):
    return lazy_export(__name__, _LAZY_EXPORTS, name)
