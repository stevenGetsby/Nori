"""Content production workflow definition."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from nori.core import LLMFactory, WorkflowBase, named_workflow_steps
from nori.workflows.schemas import HumanGateSpec, StageSpec, WorkflowRun, WorkflowSpec
from nori.workflows.runner import WorkflowRunner

from .state import ContentProductionState, TopNotesCollector
from .stages import ContentProductionStages
from .artifacts import persist_final_state_artifacts


@dataclass(frozen=True)
class ContentProductionConfig:
    """Business configuration for one content production workflow."""

    workflow_name: str
    client_name: str
    brand_name: str
    platform: str
    project_id_prefix: str
    project_name: str
    topic: str
    account_position: str
    target_audience: str
    goals: list[str]
    positioning_notes: list[str]
    constraints: list[str]
    taboos: list[str]
    platform_rules: list[dict[str, str]]
    top_k_per_keyword: int = 1
    download_media: bool = False
    horizon_days: int = 7
    market_case_brief_chars: int = 1200
    llm_label: str = ""
    image_label: str = ""
    require_image_references: bool = False
    stage_timeout_seconds: float = 180
    content_package_timeout_seconds: float = 240
    human_gate_name: str = "approve_content_design_spec"
    human_gate_prompt: str = "Review content_design_spec.json before generating final copy and cover."
    human_gate_metadata: dict[str, Any] = field(default_factory=lambda: {"artifact": "content_design_spec.json"})


class ContentProductionWorkflow(WorkflowBase):
    """Product workflow that orchestrates content production agents."""

    def __init__(
        self,
        *,
        config: ContentProductionConfig,
        runner: WorkflowRunner | None = None,
    ) -> None:
        super().__init__(
            workflow_name=config.workflow_name,
            steps=named_workflow_steps(
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
            ),
        )
        self.config = config
        self.runner = runner or WorkflowRunner()
        self.stages = ContentProductionStages(config)

    def initial_state(
        self,
        *,
        run_dir: Path,
        market_dir: Path,
        covers_dir: Path,
        llm_factory: LLMFactory,
        brief_text: str,
        asset_paths: list[Path],
        top_notes_collector: TopNotesCollector,
        reference_public_urls_by_path: dict[str, str] | None = None,
    ) -> ContentProductionState:
        return {
            "run_dir": run_dir,
            "market_dir": market_dir,
            "covers_dir": covers_dir,
            "llm_factory": llm_factory,
            "brief_text": brief_text,
            "asset_paths": asset_paths,
            "reference_public_urls_by_path": dict(reference_public_urls_by_path or {}),
            "top_notes_collector": top_notes_collector,
            "_artifact_refs": {},
        }

    def build_spec(self) -> WorkflowSpec:
        default_timeout = self.config.stage_timeout_seconds
        return WorkflowSpec(
            name=self.config.workflow_name,
            stages=[
                StageSpec("xhs_top_notes", self.stages.xhs_top_notes, timeout_seconds=default_timeout),
                StageSpec("market_skill_report", self.stages.market_skill_report, timeout_seconds=default_timeout),
                StageSpec("intake", self.stages.intake, timeout_seconds=default_timeout),
                StageSpec("account_plan", self.stages.account_plan, timeout_seconds=default_timeout),
                StageSpec("client_brief", self.stages.client_brief, timeout_seconds=default_timeout),
                StageSpec("operation_project", self.stages.operation_project, timeout_seconds=default_timeout),
                StageSpec("kpi_plan", self.stages.kpi_plan, timeout_seconds=default_timeout),
                StageSpec("content_calendar", self.stages.content_calendar, timeout_seconds=default_timeout),
                StageSpec("selected_task", self.stages.selected_task, timeout_seconds=default_timeout),
                StageSpec("content_context", self.stages.content_context, timeout_seconds=default_timeout),
                StageSpec("content_design_spec", self.stages.content_design_spec, timeout_seconds=default_timeout),
                StageSpec(
                    "content_package",
                    self.stages.content_package,
                    human_gate=HumanGateSpec(
                        name=self.config.human_gate_name,
                        prompt=self.config.human_gate_prompt,
                        metadata=dict(self.config.human_gate_metadata),
                    ),
                    timeout_seconds=self.config.content_package_timeout_seconds,
                ),
                StageSpec("reviews", self.stages.reviews, timeout_seconds=default_timeout),
                StageSpec("summary", self.stages.summary, timeout_seconds=default_timeout),
            ],
        )

    def run(
        self,
        initial: ContentProductionState,
        *,
        session_id: str = "",
        task_id: str = "",
        human_gate_mode: str = "skip",
    ) -> tuple[ContentProductionState, WorkflowRun]:
        final_state, workflow_run = self.runner.run(
            self.build_spec(),
            initial,
            session_id=session_id,
            task_id=task_id,
            human_gate_mode=human_gate_mode,
        )
        persist_final_state_artifacts(final_state)
        return final_state, workflow_run
