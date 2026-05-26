"""Prompt registry for review agents.

The current review gate is rule-based and has no direct LLM prompt.
"""
from __future__ import annotations

STAGE_PROMPTS: dict[str, str] = {}

__all__ = ["STAGE_PROMPTS"]
