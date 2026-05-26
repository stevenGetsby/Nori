"""Compatibility re-exports for structured LLM result contracts."""
from __future__ import annotations

from nori.core.contracts import IntentLLMResult, StructuredCallResult, TargetSelectionResult

__all__ = ["IntentLLMResult", "StructuredCallResult", "TargetSelectionResult"]
