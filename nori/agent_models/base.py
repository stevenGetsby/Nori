"""Common type aliases shared by Nori agent models."""
from __future__ import annotations

from typing import Any

Intention = dict[str, Any]
Context = dict[str, Any]
AgentInput = dict[str, Any]
AgentOutput = dict[str, Any]
BenchmarkAccounts = dict[str, Any]
IPPortraitReport = dict[str, Any]

__all__ = [
    "AgentInput",
    "AgentOutput",
    "BenchmarkAccounts",
    "Context",
    "IPPortraitReport",
    "Intention",
]
