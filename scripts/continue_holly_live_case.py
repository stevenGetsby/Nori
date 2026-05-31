"""Continue a Holly live case run after market/profile/planning artifacts exist."""
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import llms
from data_collect.adapter import HotNote, TopNotesResult
from nori.agents.content_generation import ContentSpecAgent, ArtifactGenerationAgent
from nori.agents.planning.calendar_planner import CalendarPlannerAgent
from nori.context import ContextPackBuilder, ContextResolver
from nori.core import AccountOperationProject, AssetLibrary, AssetRecord, ClientBrief, KPIPlan, LLMFactory
from nori.agents.learning_loop.review import ReviewGateAgent
from nori.agents.market_analysis.models import SessionSkillReport
from nori.agents.user_profiling.models import AccountPlanResult, IntakeResult


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        raise SystemExit("Usage: python scripts/continue_holly_live_case.py <run_dir>")
    run_dir = Path(argv[1]).expanduser().resolve()
    covers_dir = run_dir / "covers"
    covers_dir.mkdir(parents=True, exist_ok=True)

    _assert_active_models()
    llm_factory = _llm_factory()

    top_result = _top_notes(run_dir / "xhs_top_notes_result.json")
    market_report = SessionSkillReport.from_dict(_read_json(run_dir / "market_session_skill_report.json"))
    intake = IntakeResult.from_dict(_read_json(run_dir / "intake_result.json"))
    account_plan = AccountPlanResult.from_dict(_read_json(run_dir / "account_plan.json"))
    client_brief = ClientBrief.from_dict(_read_json(run_dir / "client_brief.json"))
    project = AccountOperationProject.from_dict(_read_json(run_dir / "operation_project.json"))
    kpi_plan = KPIPlan.from_dict(_read_json(run_dir / "kpi_plan.json"))

    calendar = CalendarPlannerAgent(use_llm=False, llm_factory=llm_factory).run(
        project,
        kpi_plan=kpi_plan,
        client_brief=client_brief,
        start_date=date.today(),
        horizon_days=7,
        use_llm=False,
    )
    _write_json(run_dir / "content_calendar.json", calendar.to_dict())

    task = sorted(calendar.tasks, key=lambda task: (task.priority, task.scheduled_date or ""))[0]
    _write_json(run_dir / "selected_task.json", task.to_dict())

    context_pack = ContextPackBuilder().build_from_project(
        project,
        task=task,
        asset_library=_asset_library_from_user_assets(intake.assets),
        skills=market_report.skills,
        platform_rules=_platform_rules("xhs"),
        content_strategy=_content_strategy(task),
    )
    _write_json(run_dir / "content_context_pack.json", context_pack.to_dict())
    context_view = ContextResolver().for_agent("ContentSpecAgent", context_pack)

    content_spec = ContentSpecAgent(llm_factory=llm_factory).run(context_view=context_view)
    _write_json(run_dir / "content_design_spec.json", content_spec.to_dict())

    package = ArtifactGenerationAgent(llm_factory=llm_factory).run(
        spec=content_spec,
        task=task,
        skills=market_report.skills,
        assets=intake.assets,
        out_dir=covers_dir,
        client_brief=client_brief,
        project=project,
        use_cover=True,
    )
    _write_json(run_dir / "content_package.json", package.to_dict())

    reviews = ReviewGateAgent().run(package, task=task, client_brief=client_brief, project=project)
    _write_json(run_dir / "reviews.json", [review.to_dict() for review in reviews])
    (run_dir / "summary.md").write_text(
        _summary_markdown(
            run_dir=run_dir,
            top_result=top_result,
            market_report=market_report,
            account_plan=account_plan,
            task=task,
            package=package,
            reviews=reviews,
        ),
        encoding="utf-8",
    )
    print(json.dumps({"run_dir": str(run_dir), "summary": str(run_dir / "summary.md")}, ensure_ascii=False))
    return 0


def _assert_active_models() -> None:
    active = {usage: llms.get_active(usage).key for usage in ("llm", "vision", "image")}
    expected = {
        "llm": "lumina::gpt-5.5",
        "vision": "lumina::gpt-5.5",
        "image": "relay::gpt-image-2",
    }
    if active != expected:
        raise RuntimeError(f"active model mismatch: expected={expected}, actual={active}")


def _llm_factory() -> LLMFactory:
    def chat(messages: list[dict[str, Any]], **kwargs: Any) -> str:
        kwargs.setdefault("timeout", 180)
        return llms.chat(messages, **kwargs)

    def chat_json(messages: list[dict[str, Any]], **kwargs: Any) -> dict[str, Any]:
        kwargs.setdefault("timeout", 180)
        return llms.chat_json(messages, **kwargs)

    def image(prompt: str, **kwargs: Any) -> list[str]:
        kwargs.setdefault("timeout", 300)
        return llms.image(prompt, **kwargs)

    return LLMFactory(chat_func=chat, chat_json_func=chat_json, image_func=image)


def _top_notes(path: Path) -> TopNotesResult:
    data = _read_json(path)
    return TopNotesResult(
        platform=str(data.get("platform") or "xhs"),
        queries=list(data.get("queries") or []),
        hot_notes=[HotNote(**item) for item in data.get("hot_notes", [])],
        insufficient=list(data.get("insufficient") or []),
        source_data_dir=str(data.get("source_data_dir") or ""),
        source_keyword_dirs=dict(data.get("source_keyword_dirs") or {}),
        source_db=str(data.get("source_db") or ""),
    )


def _platform_rules(platform: str) -> list[dict[str, str]]:
    if platform == "xhs":
        return [
            {"rule": "小红书图文首屏必须一眼看出情绪利益点和收藏理由。"},
            {"rule": "标题、封面和正文开头要围绕同一个点击钩子。"},
        ]
    return []


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
    account_plan: AccountPlanResult,
    task: Any,
    package: Any,
    reviews: list[Any],
) -> str:
    note_lines: list[str] = []
    for note in top_result.hot_notes:
        note_lines.extend(
            [
                f"- `{note.keyword}` {note.title} | liked={note.liked} collected={note.collected} comments={note.comment}",
                f"  {note.note_url}",
            ]
        )

    review_lines: list[str] = []
    for review in reviews:
        data = review.to_dict()
        issues = data.get("issues") or []
        review_lines.append(f"- {data.get('reviewer', '')}: {data.get('status', '')}; issues={len(issues)}")
        for issue in issues[:5]:
            review_lines.append(f"  - {issue.get('severity', '')}: {issue.get('message', '')}")

    return "\n".join(
        [
            "# Holly Live Case Summary",
            "",
            f"- Run dir: `{run_dir}`",
            "- LLM: `lumina::gpt-5.5`",
            "- Image: `relay::gpt-image-2`",
            f"- XHS keywords: {', '.join(top_result.queries)}",
            f"- Hot notes collected: {len(top_result.hot_notes)}",
            "- Calendar: deterministic fallback resume after upstream live LLM planning artifacts were written",
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
            "- 产出已接入真实小红书搜索结果、真实 LLM 生成链路和真实图片模型。",
            "- 样本量为每个关键词 1 篇，适合端到端 live case，不足以作为稳定策略结论。",
            "- 本次 vision 有单图超时，calendar 在恢复阶段使用 deterministic fallback；后续应增加阶段级 checkpoint/resume 和更细粒度 telemetry。",
            "- 下一步优化应扩大关键词和 top_k，增加竞品账号维度，并对封面进行多候选 A/B 生成与人工选择。",
            "",
        ]
    )


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, default=str), encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
