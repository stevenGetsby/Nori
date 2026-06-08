"""Content-generation product API catalog."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ContentOption:
    option_id: str
    label: str
    description: str
    default: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "option_id": self.option_id,
            "label": self.label,
            "description": self.description,
            "default": self.default,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True)
class ContentAction:
    action_id: str
    label: str
    description: str
    route: str
    execution_mode: str
    owned_by: str
    accepts: list[str] = field(default_factory=list)
    returns: list[str] = field(default_factory=list)
    requires_llm: bool = False
    requires_image_model: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "action_id": self.action_id,
            "label": self.label,
            "description": self.description,
            "route": self.route,
            "execution_mode": self.execution_mode,
            "owned_by": self.owned_by,
            "accepts": list(self.accepts),
            "returns": list(self.returns),
            "requires_llm": self.requires_llm,
            "requires_image_model": self.requires_image_model,
            "metadata": dict(self.metadata),
        }


CONTENT_OPTION_GROUPS: dict[str, list[ContentOption]] = {
    "platform": [
        ContentOption("xhs", "Xiaohongshu", "XHS image-text note and cover workflow.", default=True),
        ContentOption("wechat", "WeChat Official Account", "Article plus 21:9 and 1:1 cover-pair planning."),
    ],
    "artifact_type": [
        ContentOption("image_text_post", "Image-text post", "Spec-driven XHS image-text post.", default=True),
        ContentOption("note", "Note", "Text note with optional cover image."),
        ContentOption("article", "Article", "Long-form article with cover planning."),
    ],
    "image_source": [
        ContentOption("uploaded_assets", "Uploaded assets", "Use user-provided images as reference/material.", default=True),
        ContentOption("market_evidence", "Market evidence", "Use collected hot-note images as inspiration/evidence references."),
        ContentOption("generated_only", "Generated only", "Generate a cover without image references."),
        ContentOption("mixed", "Mixed", "Combine uploaded assets, market evidence, and generated imagery."),
    ],
    "cover_strategy": [
        ContentOption("auto", "Auto", "Let Nori choose references and write the image prompt.", default=True),
        ContentOption("manual_references", "Manual references", "User or frontend provides selected reference image paths."),
        ContentOption("text_only_prompt", "Text-only prompt", "Skip reference images and generate from prompt only."),
        ContentOption("reuse_existing_cover", "Reuse existing cover", "Use an existing cover path without image generation."),
    ],
    "image_reference_policy": [
        ContentOption("prefer_cover_usable", "Prefer cover-usable assets", "Prioritize assets tagged usable_for=cover.", default=True),
        ContentOption("limit_3_prompt_refs", "Limit prompt refs to 3", "Keep prompt context compact while generation may receive more refs."),
        ContentOption("max_8_generation_refs", "Max 8 generation refs", "Current CoverDirector reference cap."),
    ],
    "human_gate_mode": [
        ContentOption("skip", "Skip", "Default test/local mode; record gate as skipped and continue.", default=True),
        ContentOption("pause", "Pause", "Stop before gated stage and wait for human approval."),
    ],
    "entry_mode": [
        ContentOption("direct_action", "Direct action", "Call a concrete content capability route.", default=True),
        ContentOption("workflow", "Workflow", "Run an orchestrated workflow such as content-production."),
    ],
}


CONTENT_ACTIONS = [
    ContentAction(
        action_id="content.options",
        label="Inspect content generation options",
        description="Return selectable platforms, artifact types, image sources, cover strategies, and gate modes.",
        route="/content/generation/options",
        execution_mode="metadata",
        owned_by="backend.content",
        returns=["ContentGenerationOptions"],
    ),
    ContentAction(
        action_id="content.plan",
        label="Plan content generation entrypoint",
        description="Normalize a product request and recommend direct action versus workflow execution.",
        route="/content/generation/plan",
        execution_mode="planner",
        owned_by="backend.content",
        accepts=["ContentGenerationPlanRequest"],
        returns=["ContentGenerationPlan"],
    ),
    ContentAction(
        action_id="content.design_spec",
        label="Design content spec",
        description="Future direct route for ContentSpecAgent; creates an inspectable ContentDesignSpec.",
        route="/content/generation/spec",
        execution_mode="direct_agent",
        owned_by="nori.agents.content_generation.spec_designer",
        accepts=["ContextView"],
        returns=["ContentDesignSpec"],
        requires_llm=True,
        metadata={"status": "planned_backend_route"},
    ),
    ContentAction(
        action_id="content.package",
        label="Generate content package",
        description="Future direct route for ArtifactGenerationAgent; executes a ContentDesignSpec.",
        route="/content/generation/package",
        execution_mode="direct_agent",
        owned_by="nori.agents.content_generation.artifact_generator",
        accepts=["ContentDesignSpec", "ContentTask", "NoteSkill[]", "UserAsset[]"],
        returns=["ContentPackage"],
        requires_llm=True,
        requires_image_model=True,
        metadata={"status": "planned_backend_route"},
    ),
    ContentAction(
        action_id="content.cover",
        label="Generate or choose cover",
        description="Future direct route for CoverDirector; selects references, writes image prompt, and calls image provider.",
        route="/content/generation/cover",
        execution_mode="direct_agent",
        owned_by="nori.agents.content_generation.cover_director",
        accepts=["NoteDraft", "NoteSkill", "UserAsset[]"],
        returns=["CoverResult"],
        requires_llm=True,
        requires_image_model=True,
        metadata={"status": "planned_backend_route"},
    ),
    ContentAction(
        action_id="workflow.content_production",
        label="Run content production workflow",
        description="Run the full orchestrated content-production workflow when the product needs end-to-end generation.",
        route="/workflows/content-production/runs",
        execution_mode="workflow",
        owned_by="nori.workflows.content_production",
        accepts=["ContentProductionRunRequest", "Session", "TaskGoal", "UserAsset[]", "MarketEvidence"],
        returns=["WorkflowRun", "ContentPackage", "Review[]", "Artifacts"],
        requires_llm=True,
        requires_image_model=True,
        metadata={"catalog_route": "/workflows/content-production"},
    ),
]


class ContentGenerationCatalog:
    """Product-facing content-generation options and action resolver."""

    def option_groups(self) -> dict[str, list[dict[str, Any]]]:
        return {
            group_id: [option.to_dict() for option in options]
            for group_id, options in CONTENT_OPTION_GROUPS.items()
        }

    def option_group(self, group_id: str) -> list[dict[str, Any]] | None:
        options = CONTENT_OPTION_GROUPS.get(group_id)
        return [option.to_dict() for option in options] if options is not None else None

    def actions(self) -> list[dict[str, Any]]:
        return [action.to_dict() for action in CONTENT_ACTIONS]

    def action(self, action_id: str) -> dict[str, Any] | None:
        for action in CONTENT_ACTIONS:
            if action.action_id == action_id:
                return action.to_dict()
        return None

    def plan(self, request: dict[str, Any]) -> dict[str, Any]:
        platform = _choose(request, "platform", "xhs")
        artifact_type = _choose(request, "artifact_type", "image_text_post")
        image_source = _choose(request, "image_source", "uploaded_assets")
        cover_strategy = _choose(request, "cover_strategy", "auto")
        human_gate_mode = _choose(request, "human_gate_mode", "skip")
        entry_mode = _choose(request, "entry_mode", "")
        requested_action = str(request.get("action_id") or "").strip()
        workflow_id = str(request.get("workflow_id") or "").strip()

        if requested_action:
            selected_action = requested_action
        elif entry_mode == "workflow" or workflow_id:
            selected_action = "workflow.content_production"
        elif cover_strategy in {"manual_references", "text_only_prompt", "reuse_existing_cover"}:
            selected_action = "content.cover"
        elif artifact_type in {"image_text_post", "note", "article"}:
            selected_action = "content.design_spec"
        else:
            selected_action = "content.plan"

        route = (self.action(selected_action) or {}).get("route", "")
        selected_workflow_id = workflow_id or ("content-production" if selected_action == "workflow.content_production" else "")
        return {
            "capability_id": "content_generation",
            "selected_action_id": selected_action,
            "selected_route": route,
            "workflow_id": selected_workflow_id,
            "normalized_options": {
                "platform": platform,
                "artifact_type": artifact_type,
                "image_source": image_source,
                "cover_strategy": cover_strategy,
                "human_gate_mode": human_gate_mode,
                "entry_mode": entry_mode or ("workflow" if selected_workflow_id else "direct_action"),
            },
            "requires_workflow_id": selected_action.startswith("workflow."),
            "rationale": _rationale(selected_action),
        }


def _choose(request: dict[str, Any], field_name: str, default: str) -> str:
    value = str(request.get(field_name) or "").strip()
    return value or default


def _rationale(action_id: str) -> str:
    if action_id == "workflow.content_production":
        return "Use the workflow when the product needs end-to-end orchestration across market evidence, spec, package, review, and artifacts."
    if action_id == "content.cover":
        return "Use the cover sub-capability when the product is choosing or generating imagery without rerunning the whole workflow."
    if action_id == "content.design_spec":
        return "Use the spec sub-capability when the product needs an inspectable generation blueprint before execution."
    return "Use metadata/planning when the product is still choosing generation controls."


__all__ = ["ContentGenerationCatalog", "ContentOption", "ContentAction"]
