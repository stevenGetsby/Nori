"""Workflow catalog exposed by the product backend."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class WorkflowCatalogEntry:
    """Small backend-facing description of a workflow the product can surface."""

    workflow_id: str
    label: str
    owner: str
    description: str
    stages: list[str] = field(default_factory=list)
    human_gate_default: str = "skip"
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "workflow_id": self.workflow_id,
            "label": self.label,
            "owner": self.owner,
            "description": self.description,
            "stages": list(self.stages),
            "human_gate_default": self.human_gate_default,
            "metadata": dict(self.metadata),
        }


CONTENT_PRODUCTION_STAGES = [
    "xhs_top_notes",
    "market_skill_report",
    "intake",
    "account_plan",
    "client_brief",
    "operation_project",
    "kpi_plan",
    "content_calendar",
    "selected_task",
    "content_context",
    "content_design_spec",
    "content_package",
    "reviews",
    "summary",
]


DEFAULT_WORKFLOWS = [
    WorkflowCatalogEntry(
        workflow_id="content-production",
        label="Content Production",
        owner="nori.workflows.content_production",
        description="Generate a content package from user intent, market evidence, context, assets, and review gates.",
        stages=CONTENT_PRODUCTION_STAGES,
        human_gate_default="skip",
        metadata={
            "engine": "langgraph",
            "runtime_owner": "nori.workflows",
            "session_owner": "nori.sessions",
        },
    ),
]


class WorkflowCatalog:
    """In-process workflow registry for backend product surfaces."""

    def __init__(self, entries: list[WorkflowCatalogEntry] | None = None) -> None:
        self._entries = {entry.workflow_id: entry for entry in (entries or DEFAULT_WORKFLOWS)}

    def list_workflows(self) -> list[dict[str, Any]]:
        return [entry.to_dict() for entry in self._entries.values()]

    def get_workflow(self, workflow_id: str) -> dict[str, Any] | None:
        entry = self._entries.get(workflow_id)
        return entry.to_dict() if entry is not None else None

    def resolve(self, request: dict[str, Any]) -> dict[str, Any]:
        workflow_id = str(request.get("workflow_id") or "").strip()
        capability_id = str(request.get("capability_id") or "").strip()
        action_id = str(request.get("action_id") or "").strip()
        prefer_direct_action = bool(request.get("prefer_direct_action"))
        goal = str(request.get("goal") or "").lower()

        if workflow_id and workflow_id in self._entries:
            selected = workflow_id
        elif capability_id == "content_generation" and not prefer_direct_action:
            selected = "content-production"
        elif any(token in goal for token in ("content", "生成", "小红书", "cover", "封面", "note")) and not prefer_direct_action:
            selected = "content-production"
        else:
            selected = ""

        return {
            "selected_workflow_id": selected,
            "selected_action_id": action_id or ("content.design_spec" if prefer_direct_action else ""),
            "workflow": self.get_workflow(selected) if selected else None,
            "entry_mode": "workflow" if selected else "direct_action",
            "rationale": (
                "Resolved to content-production workflow for end-to-end content generation."
                if selected
                else "Resolved to direct action; no workflow id is required for this request."
            ),
        }
