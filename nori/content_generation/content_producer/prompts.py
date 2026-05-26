"""Prompt registry for ContentProducerAgent.

ContentProducerAgent orchestrates NoteMakerAgent and CoverDirectorAgent; it has
no direct LLM prompt of its own.
"""
from __future__ import annotations

STAGE_PROMPTS: dict[str, str] = {}

__all__ = ["STAGE_PROMPTS"]
