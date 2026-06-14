"""Pure builders used by content-production workflow stages."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from data_collect.adapter import HotNote, TopNotesResult
from nori.agents.market_analysis import SessionSkillReport, XHSNoteAnalyzer
from nori.agents.market_analysis.xhs_note_analyzer import build_note_skill, write_session_outputs
from nori.core import AssetLibrary, AssetRecord, ClientBrief
from nori.core.paths import infer_project_root_from_cases_path, repo_relative_path


def build_market_report(
    *,
    config: Any,
    analyzer: XHSNoteAnalyzer,
    top_result: TopNotesResult,
    brief_text: str,
) -> SessionSkillReport:
    context = {
        "platform": config.platform,
        "topic": config.topic,
        "account_position": config.account_position,
        "target_audience": config.target_audience,
        "keywords": list(top_result.queries),
        "case_brief": brief_text[: config.market_case_brief_chars],
        "data_dir": top_result.source_data_dir,
        "top_k_per_keyword": config.top_k_per_keyword,
        "download_media": config.download_media,
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


def build_client_brief(*, config: Any, brief_text: str, account_plan: Any, top_result: TopNotesResult) -> ClientBrief:
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
        client_name=config.client_name,
        brand_name=config.brand_name,
        platform=config.platform,
        goals=list(config.goals),
        audience=list(account_plan.audience_profile),
        positioning_notes=[account_plan.recommended_positioning, *config.positioning_notes],
        constraints=list(config.constraints),
        taboos=list(config.taboos),
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


def select_task(calendar: Any) -> Any:
    if not calendar.tasks:
        raise RuntimeError("calendar has no content tasks")
    return sorted(calendar.tasks, key=lambda task: (task.priority, task.scheduled_date or ""))[0]


def content_strategy(task: Any) -> dict[str, Any]:
    return {
        "artifact_type": task.content_type,
        "creative_angle": task.brief.get("angle") or task.objective or task.topic,
        "objective": task.objective,
    }


def asset_library_from_user_assets(assets: list[Any]) -> AssetLibrary:
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


def render_summary_markdown(
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
    root = infer_project_root_from_cases_path(run_dir)
    display_run_dir = repo_relative_path(run_dir, root) if root is not None else str(run_dir)
    display_cover_path = (
        repo_relative_path(str(package.cover_path), root) if root is not None else str(package.cover_path)
    )
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
            f"- Run dir: `{display_run_dir}`",
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
            f"- cover: `{display_cover_path}`",
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
