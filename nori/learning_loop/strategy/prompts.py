"""Prompt registry for strategy agents.

The current strategy iteration flow is rule-based and has no direct LLM prompt.
"""
from __future__ import annotations

STAGE_PROMPTS: dict[str, str] = {}

__all__ = ["STAGE_PROMPTS"]
