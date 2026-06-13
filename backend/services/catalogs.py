"""Workflow, content-generation, and capability catalog service."""
from __future__ import annotations

from typing import Any

from ..content import ContentGenerationCatalog
from ..contracts import ApiError, ContentGenerationPlanRequest, WorkflowResolveRequest
from ..workflows import WorkflowCatalog


class BackendCatalogService:
    """Owns read-only product catalogs exposed by the backend API."""

    def __init__(
        self,
        *,
        workflow_catalog: WorkflowCatalog | None = None,
        content_catalog: ContentGenerationCatalog | None = None,
    ) -> None:
        self.workflow_catalog = workflow_catalog or WorkflowCatalog()
        self.content_catalog = content_catalog or ContentGenerationCatalog()

    def list_workflows(self) -> dict[str, Any]:
        return {"workflows": self.workflow_catalog.list_workflows()}

    def get_workflow(self, workflow_id: str) -> dict[str, Any]:
        workflow = self.workflow_catalog.get_workflow(workflow_id)
        if workflow is None:
            raise ApiError(f"workflow not found: {workflow_id}", status_code=404)
        return workflow

    def resolve_workflow(self, request: WorkflowResolveRequest) -> dict[str, Any]:
        return self.workflow_catalog.resolve(_model_data(request))

    def list_capabilities(self) -> dict[str, Any]:
        return {
            "capabilities": [
                {
                    "capability_id": "content_generation",
                    "label": "Content Generation",
                    "description": "Product-facing content generation controls, direct actions, and workflow entrypoints.",
                    "routes": {
                        "options": "/content/generation/options",
                        "actions": "/content/generation/actions",
                        "plan": "/content/generation/plan",
                        "readiness": "/experiments/readiness",
                        "upload_assets": "/sessions/{session_id}/assets",
                        "asset_file": "/sessions/{session_id}/assets/{asset_id}/file",
                        "publish_asset_references": "/sessions/{session_id}/assets/publish-references",
                        "session_reference_image_generation_check": "/sessions/{session_id}/assets/reference-image-generation-check",
                        "reference_publish_check": "/experiments/content-production/reference-publish-check",
                        "reference_image_generation_check": "/experiments/content-production/reference-image-generation-check",
                        "experiment_diagnostics": "/experiments/content-production/diagnostics",
                        "experiment_workbench": "/experiments/content-production/workbench",
                        "experiment_overview": "/experiments/content-production/overview",
                        "experiment_report": "/experiments/content-production/report",
                        "run_template": "/experiments/content-production/run-template",
                        "experiment_cases": "/experiments/content-production/cases",
                        "case_selection": "/experiments/content-production/cases/{case_id}/selection",
                        "case_selected_run": "/experiments/content-production/cases/{case_id}/selected-run",
                        "case_compare": "/experiments/content-production/cases/{case_id}/compare",
                        "case_next_actions": "/experiments/content-production/cases/{case_id}/next-actions",
                        "case_promotion": "/experiments/content-production/cases/{case_id}/promotion",
                        "case_replay": "/experiments/content-production/cases/{case_id}/replay",
                        "case_evaluation_draft": "/experiments/content-production/cases/{case_id}/evaluations/draft",
                        "case_evaluations": "/experiments/content-production/cases/{case_id}/evaluations",
                        "case_delivery": "/experiments/content-production/cases/{case_id}/delivery",
                        "case_delivery_export": "/experiments/content-production/cases/{case_id}/delivery/export",
                        "case_timeline": "/experiments/content-production/cases/{case_id}/timeline",
                        "case_export": "/experiments/content-production/cases/{case_id}/export",
                        "run_workflow": "/workflows/content-production/runs",
                        "preflight_run": "/workflows/content-production/runs/preflight",
                        "compare_runs": "/workflows/content-production/runs/compare",
                        "run_acceptance": "/workflows/content-production/runs/{case_id}/{run_id}/acceptance",
                        "run_evaluations": "/workflows/content-production/runs/{case_id}/{run_id}/evaluations",
                        "run_evaluation_draft": "/workflows/content-production/runs/{case_id}/{run_id}/evaluations/draft",
                        "replay_run": "/workflows/content-production/runs/{case_id}/{run_id}/replay",
                        "export_run": "/workflows/content-production/runs/{case_id}/{run_id}/export",
                        "inspect_run_artifacts": "/workflows/content-production/runs/{case_id}/{run_id}/artifacts/inspect",
                        "list_jobs": "/experiments/jobs",
                        "job_status": "/experiments/jobs/{job_id}",
                        "cancel_job": "/experiments/jobs/{job_id}/cancel",
                    },
                },
                {
                    "capability_id": "workflow_orchestration",
                    "label": "Workflow Orchestration",
                    "description": "End-to-end workflow catalog and resolver.",
                    "routes": {
                        "catalog": "/workflows",
                        "resolve": "/workflows/resolve",
                    },
                },
            ]
        }

    def content_options(self) -> dict[str, Any]:
        return {"option_groups": self.content_catalog.option_groups()}

    def content_option_group(self, group_id: str) -> dict[str, Any]:
        group = self.content_catalog.option_group(group_id)
        if group is None:
            raise ApiError(f"content option group not found: {group_id}", status_code=404)
        return {"group_id": group_id, "options": group}

    def content_actions(self) -> dict[str, Any]:
        return {"actions": self.content_catalog.actions()}

    def content_action(self, action_id: str) -> dict[str, Any]:
        action = self.content_catalog.action(action_id)
        if action is None:
            raise ApiError(f"content action not found: {action_id}", status_code=404)
        return action

    def plan_content_generation(self, request: ContentGenerationPlanRequest) -> dict[str, Any]:
        return self.content_catalog.plan(_model_data(request))


def _model_data(model: Any) -> dict[str, Any]:
    if hasattr(model, "model_dump"):
        return model.model_dump()
    return model.dict()
