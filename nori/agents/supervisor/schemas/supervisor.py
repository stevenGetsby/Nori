"""Contracts for the user-facing Nori supervisor agent."""
from __future__ import annotations

from collections.abc import Callable
from typing import Any

from nori._compat import dataclass, field
from nori.core.contracts import bool_value as _bool
from nori.core.contracts import float_value as _float
from nori.core.contracts import mapping as _mapping
from nori.core.contracts import string_list as _string_list


@dataclass(slots=True)
class SupervisorIntent:
    """One routed user intent from the main chat surface."""

    name: str = "unknown"
    summary: str = ""
    confidence: float = 0.0
    arguments: dict[str, Any] = field(default_factory=dict)
    rationale: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "summary": self.summary,
            "confidence": self.confidence,
            "arguments": dict(self.arguments),
            "rationale": self.rationale,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "SupervisorIntent":
        data = _mapping(data)
        return cls(
            name=str(data.get("name") or "unknown"),
            summary=str(data.get("summary") or ""),
            confidence=float(_float(data.get("confidence"), default=0.0) or 0.0),
            arguments=_mapping(data.get("arguments")),
            rationale=str(data.get("rationale") or ""),
        )


@dataclass(slots=True)
class SupervisorToolCall:
    """A planned call from the supervisor into one subagent/subworkflow tool."""

    tool_name: str
    arguments: dict[str, Any] = field(default_factory=dict)
    reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "tool_name": self.tool_name,
            "arguments": dict(self.arguments),
            "reason": self.reason,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "SupervisorToolCall":
        data = _mapping(data)
        return cls(
            tool_name=str(data.get("tool_name") or ""),
            arguments=_mapping(data.get("arguments")),
            reason=str(data.get("reason") or ""),
        )


@dataclass(slots=True)
class SupervisorToolResult:
    """Normalized result returned by a supervisor tool handler."""

    status: str = "succeeded"
    message: str = ""
    output: dict[str, Any] = field(default_factory=dict)
    artifact_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "message": self.message,
            "output": dict(self.output),
            "artifact_refs": list(self.artifact_refs),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "SupervisorToolResult":
        data = _mapping(data)
        return cls(
            status=str(data.get("status") or "succeeded"),
            message=str(data.get("message") or ""),
            output=_mapping(data.get("output")),
            artifact_refs=_string_list(data.get("artifact_refs")),
            metadata=_mapping(data.get("metadata")),
        )


@dataclass(slots=True)
class SupervisorToolRequest:
    """Input envelope passed to one injected subagent/subworkflow handler."""

    user_message: str
    intent: SupervisorIntent = field(default_factory=SupervisorIntent)
    session_id: str = ""
    task_id: str = ""
    context: dict[str, Any] = field(default_factory=dict)
    arguments: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "user_message": self.user_message,
            "intent": self.intent.to_dict(),
            "session_id": self.session_id,
            "task_id": self.task_id,
            "context": dict(self.context),
            "arguments": dict(self.arguments),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "SupervisorToolRequest":
        data = _mapping(data)
        return cls(
            user_message=str(data.get("user_message") or ""),
            intent=SupervisorIntent.from_dict(data.get("intent")),
            session_id=str(data.get("session_id") or ""),
            task_id=str(data.get("task_id") or ""),
            context=_mapping(data.get("context")),
            arguments=_mapping(data.get("arguments")),
            metadata=_mapping(data.get("metadata")),
        )


SupervisorToolHandler = Callable[[SupervisorToolRequest], Any]


@dataclass(slots=True)
class SupervisorTool:
    """A callable capability exposed to the supervisor.

    The handler is intentionally injected. This keeps the supervisor independent
    from concrete workflow runtimes while still allowing backend/workflow layers
    to expose subworkflows as tools.
    """

    name: str
    description: str
    intent_names: tuple[str, ...] = ()
    keywords: tuple[str, ...] = ()
    handler: SupervisorToolHandler | None = None
    is_workflow: bool = False
    requires_human_approval: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "intent_names": list(self.intent_names),
            "keywords": list(self.keywords),
            "is_workflow": self.is_workflow,
            "requires_human_approval": self.requires_human_approval,
            "has_handler": self.handler is not None,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "SupervisorTool":
        data = _mapping(data)
        return cls(
            name=str(data.get("name") or ""),
            description=str(data.get("description") or ""),
            intent_names=tuple(_string_list(data.get("intent_names"))),
            keywords=tuple(_string_list(data.get("keywords"))),
            is_workflow=_bool(data.get("is_workflow")),
            requires_human_approval=_bool(data.get("requires_human_approval")),
            metadata=_mapping(data.get("metadata")),
        )


@dataclass(slots=True)
class SupervisorTurnResult:
    """One main-chat supervisor turn."""

    status: str
    intent: SupervisorIntent = field(default_factory=SupervisorIntent)
    selected_tool: str = ""
    tool_call: SupervisorToolCall | None = None
    tool_result: SupervisorToolResult | None = None
    assistant_message: str = ""
    next_questions: list[str] = field(default_factory=list)
    artifact_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "intent": self.intent.to_dict(),
            "selected_tool": self.selected_tool,
            "tool_call": self.tool_call.to_dict() if self.tool_call else None,
            "tool_result": self.tool_result.to_dict() if self.tool_result else None,
            "assistant_message": self.assistant_message,
            "next_questions": list(self.next_questions),
            "artifact_refs": list(self.artifact_refs),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "SupervisorTurnResult":
        data = _mapping(data)
        tool_call = data.get("tool_call")
        tool_result = data.get("tool_result")
        return cls(
            status=str(data.get("status") or ""),
            intent=SupervisorIntent.from_dict(data.get("intent")),
            selected_tool=str(data.get("selected_tool") or ""),
            tool_call=SupervisorToolCall.from_dict(tool_call) if isinstance(tool_call, dict) else None,
            tool_result=SupervisorToolResult.from_dict(tool_result) if isinstance(tool_result, dict) else None,
            assistant_message=str(data.get("assistant_message") or ""),
            next_questions=_string_list(data.get("next_questions")),
            artifact_refs=_string_list(data.get("artifact_refs")),
            metadata=_mapping(data.get("metadata")),
        )
