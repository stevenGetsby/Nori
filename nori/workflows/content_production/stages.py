"""Stage handlers for the content production workflow."""
from __future__ import annotations

from datetime import date
from typing import Any

from nori.agents.content_generation import ArtifactGenerationAgent, ContentSpecAgent
from nori.agents.learning_loop import ReviewGateAgent
from nori.agents.market_analysis import XHSNoteAnalyzer
from nori.agents.market_analysis.xhs_note_analyzer import skills_output
from nori.agents.planning import CalendarPlannerAgent, KPIPlannerAgent, OperationPlannerAgent
from nori.agents.user_profiling import AccountPlannerAgent, AccountPlannerInput, IntakeAgent, UserInput
from nori.context import ContextPackBuilder, ContextResolver

from .artifacts import with_artifact, write_json
from .stage_support import (
    asset_library_from_user_assets,
    build_client_brief,
    build_market_report,
    content_strategy,
    render_summary_markdown,
    select_task,
    top_notes_result_from_dict,
)
from .state import ContentProductionState

__all__ = ["ContentProductionStages", "top_notes_result_from_dict"]


class ContentProductionStages:
    """Callable stage owner for content production orchestration."""

    def __init__(self, config: Any) -> None:
        self.config = config

    def xhs_top_notes(self, state: ContentProductionState) -> ContentProductionState:
        top_result = state["top_notes_collector"](state["market_dir"])
        path = state["run_dir"] / "xhs_top_notes_result.json"
        write_json(path, top_result.to_dict())
        state = {**state, "top_result": top_result}
        return with_artifact(state, "xhs_top_notes", path)

    def market_skill_report(self, state: ContentProductionState) -> ContentProductionState:
        analyzer = XHSNoteAnalyzer(use_llm=True, llm_factory=state["llm_factory"])
        market_report = build_market_report(
            config=self.config,
            analyzer=analyzer,
            top_result=state["top_result"],
            brief_text=state["brief_text"],
        )
        report_path = state["run_dir"] / "market_session_skill_report.json"
        guides_path = state["run_dir"] / "note_skill_guides.json"
        write_json(report_path, market_report.to_dict())
        write_json(guides_path, skills_output(market_report))
        state = {**state, "market_report": market_report}
        return with_artifact(state, "market_skill_report", report_path)

    def intake(self, state: ContentProductionState) -> ContentProductionState:
        intake = IntakeAgent(use_llm=True, use_vision=True, llm_factory=state["llm_factory"]).run(
            UserInput(text=state["brief_text"], images=[str(path) for path in state["asset_paths"]])
        )
        path = state["run_dir"] / "intake_result.json"
        write_json(path, intake.to_dict())
        state = {**state, "intake": intake}
        return with_artifact(state, "intake", path)

    def account_plan(self, state: ContentProductionState) -> ContentProductionState:
        account_plan = AccountPlannerAgent(use_llm=True, llm_factory=state["llm_factory"]).run(
            AccountPlannerInput.from_intaker(
                state["intake"],
                text=state["brief_text"],
                images=[str(path) for path in state["asset_paths"]],
                platform=self.config.platform,
                enable_search=False,
            )
        )
        path = state["run_dir"] / "account_plan.json"
        write_json(path, account_plan.to_dict())
        state = {**state, "account_plan": account_plan}
        return with_artifact(state, "account_plan", path)

    def client_brief(self, state: ContentProductionState) -> ContentProductionState:
        client_brief = build_client_brief(
            config=self.config,
            brief_text=state["brief_text"],
            account_plan=state["account_plan"],
            top_result=state["top_result"],
        )
        path = state["run_dir"] / "client_brief.json"
        write_json(path, client_brief.to_dict())
        state = {**state, "client_brief": client_brief}
        return with_artifact(state, "client_brief", path)

    def operation_project(self, state: ContentProductionState) -> ContentProductionState:
        project = OperationPlannerAgent(use_llm=True, llm_factory=state["llm_factory"]).run(
            state["client_brief"],
            state["account_plan"],
            project_id=f"{self.config.project_id_prefix}_{state['run_dir'].name}",
            project_name=self.config.project_name,
            start_date=date.today(),
            horizon_days=self.config.horizon_days,
        )
        path = state["run_dir"] / "operation_project.json"
        write_json(path, project.to_dict())
        state = {**state, "project": project}
        return with_artifact(state, "operation_project", path)

    def kpi_plan(self, state: ContentProductionState) -> ContentProductionState:
        kpi_plan = KPIPlannerAgent(use_llm=True, llm_factory=state["llm_factory"]).run(state["project"])
        path = state["run_dir"] / "kpi_plan.json"
        write_json(path, kpi_plan.to_dict())
        state = {**state, "kpi_plan": kpi_plan}
        return with_artifact(state, "kpi_plan", path)

    def content_calendar(self, state: ContentProductionState) -> ContentProductionState:
        calendar = CalendarPlannerAgent(use_llm=True, llm_factory=state["llm_factory"]).run(
            state["project"],
            kpi_plan=state["kpi_plan"],
            client_brief=state["client_brief"],
            start_date=date.today(),
            horizon_days=self.config.horizon_days,
        )
        path = state["run_dir"] / "content_calendar.json"
        write_json(path, calendar.to_dict())
        state = {**state, "calendar": calendar}
        return with_artifact(state, "content_calendar", path)

    def selected_task(self, state: ContentProductionState) -> ContentProductionState:
        task = select_task(state["calendar"])
        path = state["run_dir"] / "selected_task.json"
        write_json(path, task.to_dict())
        state = {**state, "task": task}
        return with_artifact(state, "selected_task", path)

    def content_context(self, state: ContentProductionState) -> ContentProductionState:
        context_pack = ContextPackBuilder().build_from_project(
            state["project"],
            task=state["task"],
            asset_library=asset_library_from_user_assets(state["intake"].assets),
            skills=state["market_report"].skills,
            platform_rules=self.config.platform_rules,
            content_strategy=content_strategy(state["task"]),
        )
        context_view = ContextResolver().for_agent("ContentSpecAgent", context_pack)
        path = state["run_dir"] / "content_context_pack.json"
        write_json(path, context_pack.to_dict())
        state = {**state, "content_context_pack": context_pack, "content_context_view": context_view}
        return with_artifact(state, "content_context", path)

    def content_design_spec(self, state: ContentProductionState) -> ContentProductionState:
        content_spec = ContentSpecAgent(llm_factory=state["llm_factory"]).run(
            context_view=state["content_context_view"],
        )
        path = state["run_dir"] / "content_design_spec.json"
        write_json(path, content_spec.to_dict())
        state = {**state, "content_spec": content_spec}
        return with_artifact(state, "content_design_spec", path)

    def content_package(self, state: ContentProductionState) -> ContentProductionState:
        package = ArtifactGenerationAgent(llm_factory=state["llm_factory"]).run(
            spec=state["content_spec"],
            task=state["task"],
            skills=state["market_report"].skills,
            assets=state["intake"].assets,
            out_dir=state["covers_dir"],
            client_brief=state["client_brief"],
            project=state["project"],
            intent={
                "require_image_references": self.config.require_image_references,
                "run_id": state["run_dir"].name,
                "reference_public_urls_by_path": dict(state.get("reference_public_urls_by_path") or {}),
            },
            use_cover=True,
        )
        path = state["run_dir"] / "content_package.json"
        write_json(path, package.to_dict())
        state = {**state, "package": package}
        return with_artifact(state, "content_package", path)

    def reviews(self, state: ContentProductionState) -> ContentProductionState:
        reviews = ReviewGateAgent().run(
            state["package"],
            task=state["task"],
            client_brief=state["client_brief"],
            project=state["project"],
        )
        path = state["run_dir"] / "reviews.json"
        write_json(path, [review.to_dict() for review in reviews])
        state = {**state, "reviews": reviews}
        return with_artifact(state, "reviews", path)

    def summary(self, state: ContentProductionState) -> ContentProductionState:
        summary = render_summary_markdown(
            run_dir=state["run_dir"],
            top_result=state["top_result"],
            market_report=state["market_report"],
            account_plan=state["account_plan"],
            task=state["task"],
            package=state["package"],
            reviews=state["reviews"],
            llm_label=self.config.llm_label,
            image_label=self.config.image_label,
        )
        path = state["run_dir"] / "summary.md"
        path.write_text(summary, encoding="utf-8")
        return with_artifact(state, "summary", path)
