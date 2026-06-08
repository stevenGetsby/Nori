"""Stage handlers for the content production workflow."""
from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from data_collect.adapter import HotNote, TopNotesResult
from nori.agents.content_generation import ArtifactGenerationAgent, ContentSpecAgent
from nori.agents.learning_loop import ReviewGateAgent
from nori.agents.market_analysis import SessionSkillReport, XHSNoteAnalyzer
from nori.agents.market_analysis.xhs_note_analyzer import build_note_skill, skills_output, write_session_outputs
from nori.agents.planning import CalendarPlannerAgent, KPIPlannerAgent, OperationPlannerAgent
from nori.agents.user_profiling import AccountPlannerAgent, AccountPlannerInput, IntakeAgent, UserInput
from nori.context import ContextPackBuilder, ContextResolver
from nori.core import AssetLibrary, AssetRecord, ClientBrief

from .artifacts import with_artifact, write_json
from .state import ContentProductionState


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
        market_report = self._build_market_report(analyzer, state["top_result"], state["brief_text"])
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
        client_brief = self._client_brief(state["brief_text"], state["account_plan"], state["top_result"])
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
        task = _select_task(state["calendar"])
        path = state["run_dir"] / "selected_task.json"
        write_json(path, task.to_dict())
        state = {**state, "task": task}
        return with_artifact(state, "selected_task", path)

    def content_context(self, state: ContentProductionState) -> ContentProductionState:
        context_pack = ContextPackBuilder().build_from_project(
            state["project"],
            task=state["task"],
            asset_library=_asset_library_from_user_assets(state["intake"].assets),
            skills=state["market_report"].skills,
            platform_rules=self.config.platform_rules,
            content_strategy=_content_strategy(state["task"]),
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
        summary = _summary_markdown(
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

    def _build_market_report(
        self,
        analyzer: XHSNoteAnalyzer,
        top_result: TopNotesResult,
        brief_text: str,
    ) -> SessionSkillReport:
        context = {
            "platform": self.config.platform,
            "topic": self.config.topic,
            "account_position": self.config.account_position,
            "target_audience": self.config.target_audience,
            "keywords": list(top_result.queries),
            "case_brief": brief_text[: self.config.market_case_brief_chars],
            "data_dir": top_result.source_data_dir,
            "top_k_per_keyword": self.config.top_k_per_keyword,
            "download_media": self.config.download_media,
        }
        if top_result.insufficient:
            raise RuntimeError(f"XHS hot-note collection insufficient: {top_result.insufficient}")
        clusters, leftover, llm_used = analyzer._cluster_hot_notes(top_result.hot_notes)
        skills = [build_note_skill(cluster, context) for cluster in clusters]
        report = SessionSkillReport(
            context=context,
            keywords=list(top_result.queries),
            skills=skills,
            coverage={"total_notes": len(top_result.hot_notes), "buckets": {s.label: len(s.evidence_notes) for s in skills}},
            leftover_note_ids=leftover,
            source_data_dir=top_result.source_data_dir,
            source_keyword_dirs=dict(top_result.source_keyword_dirs),
            source_db=top_result.source_db,
            insufficient=list(top_result.insufficient),
            llm_enhanced=llm_used,
        )
        write_session_outputs(report)
        return report

    def _client_brief(self, brief_text: str, account_plan: Any, top_result: TopNotesResult) -> ClientBrief:
        source_refs = [
            {
                "type": "xhs_note",
                "keyword": note.keyword,
                "title": note.title,
                "url": note.note_url,
                "liked": note.liked,
                "collected": note.collected,
            }
            for note in top_result.hot_notes
        ]
        return ClientBrief(
            client_name=self.config.client_name,
            brand_name=self.config.brand_name,
            platform=self.config.platform,
            goals=list(self.config.goals),
            audience=list(account_plan.audience_profile),
            positioning_notes=[account_plan.recommended_positioning, *self.config.positioning_notes],
            constraints=list(self.config.constraints),
            taboos=list(self.config.taboos),
            source_materials=source_refs,
            context={"case_brief": brief_text},
        )


def top_notes_result_from_dict(data: dict[str, Any]) -> TopNotesResult:
    notes = [HotNote(**item) for item in data.get("hot_notes", [])]
    return TopNotesResult(
        platform=str(data.get("platform") or "xhs"),
        queries=list(data.get("queries") or []),
        hot_notes=notes,
        insufficient=list(data.get("insufficient") or []),
        source_data_dir=str(data.get("source_data_dir") or ""),
        source_keyword_dirs=dict(data.get("source_keyword_dirs") or {}),
        source_db=str(data.get("source_db") or ""),
    )


def _select_task(calendar: Any) -> Any:
    if not calendar.tasks:
        raise RuntimeError("calendar has no content tasks")
    return sorted(calendar.tasks, key=lambda task: (task.priority, task.scheduled_date or ""))[0]


def _content_strategy(task: Any) -> dict[str, Any]:
    return {
        "artifact_type": task.content_type,
        "creative_angle": task.brief.get("angle") or task.objective or task.topic,
        "objective": task.objective,
    }


def _asset_library_from_user_assets(assets: list[Any]) -> AssetLibrary:
    return AssetLibrary(
        assets=[
            AssetRecord(
                asset_id=f"intake_asset_{index + 1}",
                kind=asset.kind,
                path=asset.path,
                text=asset.text,
                usage=list(asset.usable_for),
                tags=[*asset.vision_roles, *asset.brand_signals],
                source="intake",
                metadata={"subject": asset.subject, "quality": asset.quality},
            )
            for index, asset in enumerate(assets)
        ]
    )


def _summary_markdown(
    *,
    run_dir: Path,
    top_result: TopNotesResult,
    market_report: SessionSkillReport,
    account_plan: Any,
    task: Any,
    package: Any,
    reviews: list[Any],
    llm_label: str,
    image_label: str,
) -> str:
    review_lines = []
    for review in reviews:
        data = review.to_dict()
        issues = data.get("issues") or []
        review_lines.append(f"- {data.get('reviewer', '')}: {data.get('status', '')}; issues={len(issues)}")
        for issue in issues[:5]:
            review_lines.append(f"  - {issue.get('severity', '')}: {issue.get('message', '')}")

    note_lines: list[str] = []
    for note in top_result.hot_notes:
        note_lines.extend(
            [
                f"- `{note.keyword}` {note.title} | liked={note.liked} collected={note.collected} comments={note.comment}",
                f"  {note.note_url}",
            ]
        )

    return "\n".join(
        [
            "# Holly Live Case Summary",
            "",
            f"- Run dir: `{run_dir}`",
            f"- LLM: `{llm_label}`",
            f"- Image: `{image_label}`",
            f"- XHS keywords: {', '.join(top_result.queries)}",
            f"- Hot notes collected: {len(top_result.hot_notes)}",
            "",
            "## Market Evidence",
            *note_lines,
            "",
            "## Learned Note Skills",
            *[
                f"- {skill.label}: goal={skill.goal}, tone={skill.tone}, evidence={len(skill.evidence_notes)}"
                for skill in market_report.skills
            ],
            "",
            "## Account Direction",
            account_plan.recommended_positioning,
            "",
            "## Selected Task",
            f"- {task.title}",
            f"- topic: {task.topic}",
            f"- objective: {task.objective}",
            "",
            "## Generated Note",
            f"- title: {package.title}",
            f"- tags: {' '.join(package.tags)}",
            f"- cover: `{package.cover_path}`",
            "",
            package.body,
            "",
            "## Review",
            *review_lines,
            "",
            "## Quality Notes",
            "- 产出已经接入真实小红书搜索结果、真实 LLM、真实图片模型；market evidence 可回溯到 `xhs_top_notes_result.json` 和各 keyword 目录。",
            "- 当前样本量适合端到端 smoke/live case，不足以作为稳定内容策略结论。",
            "- 下一步优化应扩大关键词和 top_k，增加竞品账号维度，并对封面进行多候选 A/B 生成与人工选择。",
            "",
        ]
    )
