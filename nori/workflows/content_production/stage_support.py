"""Pure builders used by content-production workflow stages."""
from __future__ import annotations

import inspect
import json
from pathlib import Path
from typing import Any

from data_collect.adapter import HotNote, TopNotesResult
from nori.agents.market_analysis import SessionSkillReport, XHSNoteAnalyzer
from nori.agents.market_analysis.xhs_note_analyzer import build_note_skill, write_session_outputs
from nori.core import AssetLibrary, AssetRecord, ClientBrief
from nori.core.paths import infer_project_root_from_cases_path, repo_relative_path
from nori.shared.llm_json import try_stage_json


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


def build_xhs_search_query_plan(
    *,
    brief_text: str,
    intake: Any,
    config: Any,
    llm_factory: Any,
) -> dict[str, Any]:
    fallback = _fallback_search_query_plan(brief_text=brief_text, intake=intake, config=config)
    system = "你是 Nori 的小红书搜索策略规划器。只输出 JSON。"
    user = f"""\
基于用户 Intaker 结果，为小红书搜索生成三层关键词计划。

用户原始 brief:
{brief_text[:1600]}

Intaker 结果:
{_jsonish(intake)}

项目配置:
{_jsonish({
    "platform": getattr(config, "platform", "xhs"),
    "topic": getattr(config, "topic", ""),
    "account_position": getattr(config, "account_position", ""),
    "target_audience": getattr(config, "target_audience", ""),
    "goals": list(getattr(config, "goals", []) or []),
    "constraints": list(getattr(config, "constraints", []) or []),
    "taboos": list(getattr(config, "taboos", []) or []),
})}

你要输出适合 XHS 搜索的三个层级：
1. track_keywords: 赛道层，搜大盘内容范式，比如 AI工具、效率工具、职场成长。
2. topic_keywords: 主题层，搜这次内容主题，比如 AI工具更新、新功能判断。
3. content_point_keywords: 内容点层，搜具体切口/钩子，比如 伪需求判断、工具避坑、5步判断。

规则：
- 每层 1-{int(getattr(config, "search_keywords_per_layer", 2) or 2)} 个关键词。
- 每个关键词 2-12 个汉字，适合直接放进小红书搜索框。
- 不要返回品牌名，不要带 #、【】、标点或营销口号。
- 关键词必须从宽到窄递进，不能三层重复。
- 每个关键词后续会取热度最高的 {int(getattr(config, "search_top_k_per_keyword", 3) or 3)} 篇笔记。

输出 JSON，字段固定：
{{
  "track_keywords": ["..."],
  "topic_keywords": ["..."],
  "content_point_keywords": ["..."],
  "rationale": "一句话说明搜索策略"
}}
"""
    data, error = try_stage_json(
        system=system,
        user=user,
        timeout=45,
        chat_json_func=llm_factory.chat_json_func,
    )
    plan = _normalize_search_query_plan(data or {}, fallback=fallback, config=config)
    if error:
        plan["metadata"]["llm_error"] = {"stage": "search_query_plan", **error}
    return plan


def call_top_notes_collector(collector: Any, market_dir: Path, *, search_context: dict[str, Any]) -> TopNotesResult:
    try:
        signature = inspect.signature(collector)
    except (TypeError, ValueError):
        return collector(market_dir, search_context)
    params = list(signature.parameters.values())
    accepts_varargs = any(param.kind == inspect.Parameter.VAR_POSITIONAL for param in params)
    positional = [
        param for param in params
        if param.kind in {inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD}
    ]
    if accepts_varargs or len(positional) >= 2:
        return collector(market_dir, search_context)
    return collector(market_dir)


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


def _fallback_search_query_plan(*, brief_text: str, intake: Any, config: Any) -> dict[str, Any]:
    intention = dict(getattr(intake, "intention", {}) or {})
    context = dict(getattr(intake, "context", {}) or {})
    topic = _clean_keyword(getattr(config, "topic", "")) or _clean_keyword(brief_text[:24]) or "小红书图文"
    goal = _clean_keyword(intention.get("goal")) or _clean_keyword((getattr(config, "goals", []) or [""])[0])
    fmt = _clean_keyword(intention.get("format")) or "小红书图文"
    track = _dedupe_keywords([
        _clean_keyword(getattr(config, "account_position", "")),
        _clean_keyword(getattr(config, "target_audience", "")),
        topic,
    ])[:2]
    topic_keywords = _dedupe_keywords([topic, goal])[:2]
    points = _dedupe_keywords([
        *_stringish_list(context.get("guardrails")),
        *_stringish_list(context.get("data_refs")),
        goal,
        fmt,
        topic,
    ])[:2]
    return _plan_dict(
        track_keywords=track or [topic],
        topic_keywords=topic_keywords or [topic],
        content_point_keywords=points or [topic],
        rationale="规则兜底：从 Intaker 和 workflow config 提取赛道、主题、内容点关键词。",
        source="rule_fallback",
        config=config,
    )


def _normalize_search_query_plan(data: dict[str, Any], *, fallback: dict[str, Any], config: Any) -> dict[str, Any]:
    track = _dedupe_keywords(data.get("track_keywords") or data.get("track") or [])
    topic = _dedupe_keywords(data.get("topic_keywords") or data.get("topic") or [])
    points = _dedupe_keywords(data.get("content_point_keywords") or data.get("content_points") or [])
    if not track:
        track = list(fallback["layers"][0]["keywords"])
    if not topic:
        topic = list(fallback["layers"][1]["keywords"])
    if not points:
        points = list(fallback["layers"][2]["keywords"])
    limit = max(1, int(getattr(config, "search_keywords_per_layer", 2) or 2))
    return _plan_dict(
        track_keywords=track[:limit],
        topic_keywords=topic[:limit],
        content_point_keywords=points[:limit],
        rationale=str(data.get("rationale") or fallback.get("rationale") or ""),
        source="llm_intake_query_plan" if data else fallback.get("source", "rule_fallback"),
        config=config,
    )


def _plan_dict(
    *,
    track_keywords: list[str],
    topic_keywords: list[str],
    content_point_keywords: list[str],
    rationale: str,
    source: str,
    config: Any,
) -> dict[str, Any]:
    top_k = _bounded_int(getattr(config, "search_top_k_per_keyword", 3), default=3, minimum=3, maximum=5)
    layers = [
        {"level": "track", "label": "赛道", "keywords": _dedupe_keywords(track_keywords), "top_k_per_keyword": top_k},
        {"level": "topic", "label": "主题", "keywords": _dedupe_keywords(topic_keywords), "top_k_per_keyword": top_k},
        {
            "level": "content_point",
            "label": "内容点",
            "keywords": _dedupe_keywords(content_point_keywords),
            "top_k_per_keyword": top_k,
        },
    ]
    flattened = _dedupe_keywords([keyword for layer in layers for keyword in layer["keywords"]])
    return {
        "schema_version": 1,
        "platform": "xhs",
        "source": source,
        "layers": layers,
        "flattened_keywords": flattened,
        "top_k_per_keyword": top_k,
        "rationale": rationale,
        "metadata": {
            "search_rule": "track/topic/content_point layered XHS popular search",
            "keyword_count": len(flattened),
            "per_keyword_candidate_pool": 40,
            "per_keyword_selected_notes": top_k,
        },
    }


def _jsonish(value: Any) -> str:
    if hasattr(value, "to_dict"):
        value = value.to_dict()
    try:
        return json.dumps(value, ensure_ascii=False, indent=2, default=str)
    except TypeError:
        return json.dumps(str(value), ensure_ascii=False)


def _stringish_list(value: Any) -> list[str]:
    if isinstance(value, (list, tuple, set)):
        return [str(item) for item in value if str(item or "").strip()]
    text = str(value or "").strip()
    return [text] if text else []


def _clean_keyword(value: Any) -> str:
    text = str(value or "").strip()
    for token in ("#", "【", "】", "「", "」", "：", ":", "，", ",", "。", "！", "!", "？", "?"):
        text = text.replace(token, " ")
    text = "".join(part for part in text.split())
    if not text:
        return ""
    return text[:12]


def _dedupe_keywords(values: Any) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for value in _stringish_list(values):
        keyword = _clean_keyword(value)
        if not keyword or keyword in seen:
            continue
        out.append(keyword)
        seen.add(keyword)
    return out


def _bounded_int(value: Any, *, default: int, minimum: int, maximum: int) -> int:
    try:
        number = int(value)
    except (TypeError, ValueError):
        number = default
    return max(minimum, min(maximum, number))


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
