"""Content-generation module."""
from __future__ import annotations

from nori.core import CandidateSet
from nori.core.lazy_exports import lazy_export

from .models import AssetBundle, CandidateTitle, ContentDesignSpec, ContentPackage, CoverResult, NoteDraft

_LAZY_EXPORTS = {
    "ArtifactGenerationAgent": "artifact_generator",
    "ContentGenerationFacade": "facade",
    "ContentSpecAgent": "spec_designer",
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
    "ContentDesignSpec",
    "ContentPackage",
    "ContentGenerationFacade",
    "ContentProducerAgent",
    "ContentProductionError",
    "ContentSpecAgent",
    "ArtifactGenerationAgent",
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
