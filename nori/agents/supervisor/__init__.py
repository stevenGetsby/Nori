"""User-facing supervisor agent boundary."""
from __future__ import annotations

from nori.core.lazy_exports import lazy_export

from .schemas import (
    SupervisorIntent,
    SupervisorTool,
    SupervisorToolCall,
    SupervisorToolRequest,
    SupervisorToolResult,
    SupervisorTurnResult,
)

_LAZY_EXPORTS = {
    "NoriSupervisorAgent": "supervisor",
    "SupervisorDecisionError": "supervisor",
    "default_supervisor_tools": "supervisor",
}

__all__ = [
    "NoriSupervisorAgent",
    "SupervisorDecisionError",
    "SupervisorIntent",
    "SupervisorTool",
    "SupervisorToolCall",
    "SupervisorToolRequest",
    "SupervisorToolResult",
    "SupervisorTurnResult",
    "default_supervisor_tools",
]


def __getattr__(name: str):
    return lazy_export(__name__, _LAZY_EXPORTS, name)
