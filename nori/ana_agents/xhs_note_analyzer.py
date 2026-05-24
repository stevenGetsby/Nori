"""Analyze Xiaohongshu notes into cold-start seed skill drafts.

旧入口 ``analyze_note`` 处理本地 cold_start_data 单篇 meta.json。
新入口 ``collect_for_session`` 根据 context 调用 data_collect 接口
搜回平台高赞笔记 → 聚类 → 给每类输出可执行 NoteSkill。
"""
from __future__ import annotations

import argparse
import json
import random
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import llms
from nori.agent_models import (
    NoteEvidence,
    NoteSkill,
    SessionSkillReport,
    XHSNoteSample,
    XHSSeedSkillDraft,
)
from nori.agent_utils.case_log import write_agent_log


class XHSNoteAnalyzer:
    """Extract executable XHS note-making skill drafts from crawled note data."""

    def __init__(self, data_root: str | Path = "cold_start_data/xhs", *, use_llm: bool = True) -> None:
        self.data_root = Path(data_root)
        self.use_llm = use_llm

    def iter_note_meta_paths(self, category: str) -> list[Path]:
        category_dir = self.data_root / category
        if not category_dir.exists():
            raise FileNotFoundError(f"XHS cold-start category not found: {category_dir}")
        return sorted(category_dir.glob("*/posts/*/meta.json"))

    def pick_random_note(self, category: str = "设计", *, seed: int | None = None) -> XHSNoteSample:
        paths = self.iter_note_meta_paths(category)
        if not paths:
            raise FileNotFoundError(f"No XHS note meta files found in {self.data_root / category}")
        rng = random.Random(seed)
        return self.load_note(rng.choice(paths))

    def load_note(self, meta_path: str | Path) -> XHSNoteSample:
        path = Path(meta_path)
        data = _read_json(path)
        author_dir = path.parent.parent.parent
        author_data = _read_json(author_dir / "meta.json") if (author_dir / "meta.json").exists() else {}
        return XHSNoteSample(
            meta_path=path,
            category=author_dir.parent.name,
            author_id=str(data.get("user_id") or author_data.get("user_id") or author_dir.name),
            author_name=str(author_data.get("nickname") or ""),
            note_id=str(data.get("note_id") or path.parent.name),
            title=str(data.get("title") or "").strip(),
            desc=str(data.get("desc") or "").strip(),
            tags=_tags(data),
            metrics={
                "liked": _count(data.get("liked_count")),
                "collected": _count(data.get("collected_count")),
                "commented": _count(data.get("comment_count")),
                "shared": _count(data.get("share_count")),
            },
            image_count=int(data.get("image_count") or _count(data.get("image_count"))),
            note_type=str(data.get("note_type") or data.get("type") or ""),
            note_url=str(data.get("note_url") or ""),
        )

    def analyze_note(self, note: XHSNoteSample, *, use_llm: bool | None = None) -> XHSSeedSkillDraft:
        rule_draft = _rule_analyze_note(note)
        should_use_llm = self.use_llm if use_llm is None else use_llm
        if not should_use_llm:
            return rule_draft
        return _llm_enhance_note(note, rule_draft) or _mark_llm_fallback(rule_draft)

    # ============ 会话级：搜索 → 聚类 → 技能 ============

    def collect_for_session(
        self,
        context: dict[str, Any],
        *,
        dc=None,
        max_keywords: int = 3,
    ) -> SessionSkillReport:
        """根据 context 出关键词 → 拉热门 → 聚类 → 每类一条 NoteSkill。

        context 字段（都可选）：
          - topic / account_position / target_audience : 描述走 LLM 出词
          - keywords : list[str]，给了就直接用，不走 LLM
          - platform : 默认 'xhs'
          - days : 默认 30
          - top_k_per_keyword : 默认 5
          - min_liked : 默认 500
          - pool_size : 默认 20，每轮最多一页候选
          - download_media : 默认 True
                    - data_dir : 默认 nori/skill_base/data/xhs_note_analyzer
        """
        from data_collect import DataCollector, TopNotesRule

        if not self.use_llm:
            raise ValueError("会话级 XHS Note 分析必须启用 LLM，不能使用纯规则模式产出 skill")

        # 1) 关键词
        keywords = [str(k).strip() for k in (context.get("keywords") or []) if str(k).strip()]
        if not keywords:
            if not self.use_llm:
                raise ValueError("context.keywords 缺失且未启用 LLM，无法生成关键词")
            keywords = _llm_generate_keywords(context, max_n=max_keywords)
        keywords = keywords[:max_keywords]
        if not keywords:
            raise ValueError("无法从 context 推出搜索关键词")

        # 2) 调用 data_collect.collect_top_notes
        platform = context.get("platform", "xhs")
        rule = TopNotesRule(
            platform=platform,
            keywords=keywords,
            days=int(context.get("days", 30)),
            top_k_per_keyword=int(context.get("top_k_per_keyword", 5)),
            min_liked=int(context.get("min_liked", 500)),
            pool_size=int(context.get("pool_size", 20)),
            download_media=bool(context.get("download_media", True)),
            data_dir=str(context.get("data_dir") or "nori/skill_base/data/xhs_note_analyzer"),
        )
        owned_dc = dc is None
        dc = dc or DataCollector()
        try:
            if platform == "xhs":
                dc.start_sign_server()
            top_result = dc.collect_top_notes(rule)
        finally:
            if owned_dc:
                dc.stop_all()

        if top_result.insufficient:
            raise RuntimeError(f"高赞采集不足，停止生成 skill: {top_result.insufficient}")

        hot_notes = top_result.hot_notes

        # 3) 聚类
        clusters, leftover, llm_used = self._cluster_hot_notes(hot_notes)

        # 4) 每桶 NoteSkill
        skills = [self._build_note_skill(c, context) for c in clusters]

        # 5) 装 report + case log
        report = SessionSkillReport(
            context=dict(context),
            keywords=list(keywords),
            skills=skills,
            coverage={
                "total_notes": len(hot_notes),
                "buckets": {s.label: len(s.evidence_notes) for s in skills},
            },
            leftover_note_ids=leftover,
            source_data_dir=top_result.source_data_dir,
            source_keyword_dirs=dict(getattr(top_result, "source_keyword_dirs", {})),
            insufficient=list(top_result.insufficient),
            llm_enhanced=llm_used,
        )
        if report.source_data_dir:
            report_stamp = _report_stamp(report.source_keyword_dirs)
            report_path = Path(report.source_data_dir) / f"{report_stamp}_session_skill_report.json"
            report_path.parent.mkdir(parents=True, exist_ok=True)
            report_path.write_text(
                json.dumps(report.to_dict(), ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            skills_path = Path(report.source_data_dir) / f"{report_stamp}_note_skill_guides.json"
            skills_path.write_text(
                json.dumps(_skills_output(report), ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

        write_agent_log(
            agent="xhs_note_analyzer",
            case="session_skill",
            input_data={
                "context": dict(context),
                "search": {
                    "platform": platform,
                    "keywords": list(keywords),
                    "days": rule.days,
                    "top_k_per_keyword": rule.top_k_per_keyword,
                    "pool_size": rule.pool_size,
                    "download_media": rule.download_media,
                    "data_dir": rule.data_dir,
                },
            },
            output_data=report.to_dict(),
            config={"use_llm": self.use_llm},
        )
        return report

    def _cluster_hot_notes(self, hot_notes):
        """规则桶 + LLM 标签 → 收敛 1-4 桶。"""
        if not hot_notes:
            return [], [], False

        rule_labels: dict[str, str] = {n.note_id: _rule_goal(n.title, n.desc) for n in hot_notes}

        if not self.use_llm:
            raise ValueError("会话级 XHS Note 分析必须启用 LLM")
        llm_labels = _llm_label_notes(hot_notes)
        if not llm_labels:
            raise RuntimeError("LLM 标签结果为空，停止生成 skill")
        missing_ids = [n.note_id for n in hot_notes if n.note_id not in llm_labels]
        if missing_ids:
            raise RuntimeError(f"LLM 标签缺失 {len(missing_ids)} 篇笔记，停止生成 skill: {missing_ids[:5]}")
        llm_used = True

        final_labels: dict[str, tuple[str, str]] = {}
        for n in hot_notes:
            info = llm_labels.get(n.note_id) or {}
            goal = info.get("goal") or rule_labels.get(n.note_id) or "general"
            tone = info.get("tone") or ""
            final_labels[n.note_id] = (goal, tone)

        buckets: dict[str, list] = defaultdict(list)
        tones_per_bucket: dict[str, list[str]] = defaultdict(list)
        for n in hot_notes:
            goal, tone = final_labels[n.note_id]
            buckets[goal].append(n)
            if tone:
                tones_per_bucket[goal].append(tone)

        sorted_buckets = sorted(buckets.items(), key=lambda x: -len(x[1]))
        keep = sorted_buckets[:4]
        leftover: list[str] = []
        for _, notes in sorted_buckets[4:]:
            leftover.extend(n.note_id for n in notes)

        clusters = []
        for goal, notes in keep:
            tones = tones_per_bucket.get(goal) or []
            tone = Counter(tones).most_common(1)[0][0] if tones else ""
            clusters.append({
                "goal": goal,
                "notes": notes,
                "tone": tone,
                "rule_goal_distribution": dict(Counter(rule_labels[n.note_id] for n in notes)),
            })
        return clusters, leftover, llm_used

    def _build_note_skill(self, cluster, context):
        notes = cluster["notes"]
        goal = cluster["goal"]
        tone = cluster["tone"]

        title_rules = _merge_rules([_title_rules(n.title) for n in notes], limit=6)
        opening_rules = _merge_rules([_opening_rules(_content_lines(n.desc)) for n in notes], limit=5)
        body_rules = _merge_rules([_body_steps_hot(n) for n in notes], limit=6)
        interaction_rules = _merge_rules([_interaction_rules_hot(n) for n in notes], limit=4)
        visual_rules = _merge_rules([_visual_rules_hot(n) for n in notes], limit=4)
        cover_rules = _cover_rules_for_cluster(notes, goal, tone)
        avoid_rules = _dedupe([r for n in notes for r in _avoid_rules_hot(n)])[:6]

        likes = [n.liked for n in notes]
        collecteds = [n.collected for n in notes]
        metrics_summary = {
            "liked_p25": _percentile(likes, 0.25),
            "liked_p50": _percentile(likes, 0.5),
            "liked_p75": _percentile(likes, 0.75),
            "collected_p50": _percentile(collecteds, 0.5),
            "sample": len(notes),
        }

        evidence_notes = [
            NoteEvidence(
                note_id=n.note_id,
                note_url=n.note_url,
                title=n.title,
                liked=n.liked,
                collected=n.collected,
                keyword=n.keyword,
                cover_path=n.cover_path,
                image_paths=list(n.image_paths),
                video_path=n.video_path,
                quoted_segments=_content_lines(n.desc)[:2],
            )
            for n in notes
        ]

        label = _goal_label(goal, tone)
        return NoteSkill(
            skill_id=f"{label}笔记制作指南",
            label=label,
            goal=goal,
            note_type=_majority_note_type([n.note_type for n in notes]),
            tone=tone or "未标注",
            creative_goal=_goal_creative(goal),
            title_rules=title_rules,
            opening_rules=opening_rules,
            body_structure=body_rules,
            interaction_rules=interaction_rules,
            visual_rules=visual_rules,
            cover_rules=cover_rules,
            avoid_rules=avoid_rules,
            metrics_summary=metrics_summary,
            evidence_notes=evidence_notes,
            cluster_signals={
                "rule_goal_distribution": cluster.get("rule_goal_distribution", {}),
                "size": len(notes),
            },
        )


SYSTEM_PROMPT = "你是 Nori 的 XHS Note Skill Analyzer。只输出 JSON。"

USER_PROMPT = """\
基于规则 analyzer 已抽取的结构和证据，深化小红书 note 的 seed skill draft。

原始 note：
{note}

规则草案：
{rule_draft}

你要做的事：
1. 只基于原始 note 和规则草案，不编造没有证据的事实。
2. 把规则写得更像可执行创作技能，而不是复述原文内容。
3. 保留单篇草案定位，不要声称这是稳定 skill。
4. evidence 字段只能引用给定 note 或规则草案中的证据。

输出 JSON，字段固定：
{{
    "match": {{
        "scene": "具体 note 场景",
        "goals": ["目标，3个以内"],
        "note_type": "图文/视频"
    }},
    "craft": {{
        "creative_goal": "一句话说明这类 note 的创作目标",
        "title_rules": [{{"name": "规则名", "rule": "可执行规则", "evidence": "证据片段"}}],
        "opening_rules": [{{"name": "规则名", "rule": "可执行规则", "evidence": "证据片段"}}],
        "body_structure": [{{"name": "结构步骤", "rule": "可执行规则", "evidence": "证据片段"}}],
        "interaction_rules": [{{"name": "规则名", "rule": "可执行规则", "evidence": "证据片段"}}],
        "visual_rules": [{{"name": "规则名", "rule": "可执行规则", "evidence": "证据片段"}}],
        "avoid_rules": ["禁忌，必须可执行"]
    }},
    "evidence": {{
        "llm_observations": ["LLM 基于证据提炼出的观察，5条以内"]
    }},
    "validation": {{
        "llm_notes": ["这份草案仍需如何验证，3条以内"]
    }}
}}
"""


def _rule_analyze_note(note: XHSNoteSample) -> XHSSeedSkillDraft:
        lines = _content_lines(note.desc)
        title_rules = _title_rules(note.title)
        opening_rules = _opening_rules(lines)
        body_steps = _body_steps(note, lines)
        interaction_rules = _interaction_rules(note, lines)
        visual_rules = _visual_rules(note)
        avoid_rules = _avoid_rules(note, lines)
        scene = _scene(note, lines)
        goals = _goals(note, lines)
        confidence = _confidence(note, title_rules, body_steps)
        return XHSSeedSkillDraft(
            skill_id=f"seed.xhs.{_slug(note.category)}.note.single.{note.note_id}",
            category=note.category,
            match={
                "platform": ["小红书"],
                "category": [note.category],
                "scene": scene,
                "goals": goals,
                "note_type": note.note_type or "图文",
            },
            craft={
                "creative_goal": _creative_goal(scene),
                "title_rules": title_rules,
                "opening_rules": opening_rules,
                "body_structure": body_steps,
                "interaction_rules": interaction_rules,
                "visual_rules": visual_rules,
                "avoid_rules": avoid_rules,
            },
            evidence={
                "note_count": 1,
                "confidence": confidence,
                "source_note": {
                    "note_id": note.note_id,
                    "title": note.title,
                    "author": note.author_name,
                    "metrics": note.metrics,
                    "image_count": note.image_count,
                    "tags": note.tags,
                    "meta_path": str(note.meta_path),
                    "note_url": note.note_url,
                },
                "text_evidence": {
                    "opening": lines[:2],
                    "section_markers": _section_markers(lines),
                    "cta_lines": _cta_lines(lines),
                },
            },
            validation={
                "result": "draft_only",
                "llm_enhanced": False,
                "pipeline": ["rule_analyzer"],
                "reason": "单篇笔记只能形成候选规则，不能证明稳定 seed skill。",
                "next_check": [
                    "同类笔记中重复出现的规则才可升为 seed skill。",
                    "需要用留出笔记验证结构可解释性。",
                    "需要与无 skill 生成结果做对照评估。",
                ],
            },
        )


def _llm_enhance_note(note: XHSNoteSample, rule_draft: XHSSeedSkillDraft) -> XHSSeedSkillDraft | None:
    try:
        data = llms.chat_json(
            [
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": USER_PROMPT.format(
                        note=json.dumps(note.to_dict(), ensure_ascii=False),
                        rule_draft=json.dumps(rule_draft.to_dict(), ensure_ascii=False),
                    ),
                },
            ],
            usage="llm",
            timeout=60,
            _chat=llms.chat,
        )
        return _normalize_llm_draft(data, rule_draft)
    except Exception as exc:  # noqa: BLE001 - analysis must keep a deterministic fallback.
        fallback = _mark_llm_fallback(rule_draft)
        fallback.validation["llm_error"] = str(exc)[:300]
        return fallback


def _normalize_llm_draft(data: dict[str, Any], fallback: XHSSeedSkillDraft) -> XHSSeedSkillDraft:
    match_data = data.get("match") if isinstance(data.get("match"), dict) else {}
    craft_data = data.get("craft") if isinstance(data.get("craft"), dict) else {}
    evidence_data = data.get("evidence") if isinstance(data.get("evidence"), dict) else {}
    validation_data = data.get("validation") if isinstance(data.get("validation"), dict) else {}

    match = dict(fallback.match)
    match["scene"] = _text(match_data.get("scene"), fallback.match.get("scene", ""), limit=30)
    match["goals"] = _string_list(match_data.get("goals"), fallback.match.get("goals", []), limit=3)
    match["note_type"] = _text(match_data.get("note_type"), fallback.match.get("note_type", "图文"), limit=20)

    craft = dict(fallback.craft)
    craft["creative_goal"] = _text(
        craft_data.get("creative_goal"),
        fallback.craft.get("creative_goal", ""),
        limit=120,
    )
    for key in ("title_rules", "opening_rules", "body_structure", "interaction_rules", "visual_rules"):
        craft[key] = _rule_items(craft_data.get(key), fallback.craft.get(key, []), limit=6)
    craft["avoid_rules"] = _string_list(craft_data.get("avoid_rules"), fallback.craft.get("avoid_rules", []), limit=8)

    evidence = dict(fallback.evidence)
    llm_observations = _string_list(evidence_data.get("llm_observations"), [], limit=5)
    if llm_observations:
        evidence["llm_observations"] = llm_observations

    validation = dict(fallback.validation)
    validation["result"] = "draft_only"
    validation["llm_enhanced"] = True
    validation["pipeline"] = ["rule_analyzer", "llm_enhancer", "format_normalizer"]
    validation["llm_notes"] = _string_list(validation_data.get("llm_notes"), [], limit=3)

    return XHSSeedSkillDraft(
        skill_id=fallback.skill_id,
        category=fallback.category,
        match=match,
        craft=craft,
        evidence=evidence,
        validation=validation,
        type=fallback.type,
        status=fallback.status,
        platform=fallback.platform,
        source_scope=fallback.source_scope,
    )


def _mark_llm_fallback(draft: XHSSeedSkillDraft) -> XHSSeedSkillDraft:
    validation = dict(draft.validation)
    validation["result"] = "draft_only"
    validation["llm_enhanced"] = False
    validation["pipeline"] = ["rule_analyzer", "llm_enhancer_failed", "format_normalizer"]
    return XHSSeedSkillDraft(
        skill_id=draft.skill_id,
        category=draft.category,
        match=dict(draft.match),
        craft=dict(draft.craft),
        evidence=dict(draft.evidence),
        validation=validation,
        type=draft.type,
        status=draft.status,
        platform=draft.platform,
        source_scope=draft.source_scope,
    )


def _text(value: Any, fallback: str, *, limit: int) -> str:
    text = str(value or "").strip()
    if not text:
        text = str(fallback or "").strip()
    return text[:limit]


def _string_list(value: Any, fallback: list[Any], *, limit: int) -> list[str]:
    if isinstance(value, str):
        items = [value]
    elif isinstance(value, list):
        items = [str(item).strip() for item in value if str(item).strip()]
    else:
        items = []
    if not items:
        items = [str(item).strip() for item in fallback if str(item).strip()]
    return _dedupe(items)[:limit]


def _rule_items(value: Any, fallback: list[dict[str, Any]], *, limit: int) -> list[dict[str, str]]:
    if not isinstance(value, list):
        value = []
    items: list[dict[str, str]] = []
    for item in value:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name") or "").strip()
        rule = str(item.get("rule") or item.get("description") or "").strip()
        evidence = str(item.get("evidence") or "").strip()
        if name and rule:
            items.append({"name": name[:30], "rule": rule[:180], "evidence": evidence[:220]})
    if not items:
        for item in fallback:
            if not isinstance(item, dict):
                continue
            name = str(item.get("name") or "").strip()
            rule = str(item.get("rule") or "").strip()
            evidence = str(item.get("evidence") or "").strip()
            if name and rule:
                items.append({"name": name[:30], "rule": rule[:180], "evidence": evidence[:220]})
    return items[:limit]


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return data


def _content_lines(desc: str) -> list[str]:
    return [line.strip() for line in re.split(r"[\r\n]+", desc or "") if line.strip()]


def _tags(data: dict[str, Any]) -> list[str]:
    tag_list = str(data.get("tag_list") or "")
    desc = str(data.get("desc") or "")
    raw = re.findall(r"#[^#\s]+", f"{tag_list} {desc}")
    cleaned = []
    for tag in raw:
        tag = tag.replace("[话题]", "").strip()
        if tag and tag not in cleaned:
            cleaned.append(tag)
    return cleaned


def _count(value: Any) -> int:
    if isinstance(value, int):
        return value
    text = str(value or "0").strip().replace(",", "")
    if not text:
        return 0
    multiplier = 1
    if text.endswith("万"):
        multiplier = 10000
        text = text[:-1]
    try:
        return int(float(text) * multiplier)
    except ValueError:
        return 0


def _title_rules(title: str) -> list[dict[str, str]]:
    rules: list[dict[str, str]] = []
    if "｜" in title or "|" in title:
        rules.append({"name": "栏目式标题", "rule": "用栏目名加项目名，让用户先知道内容类型。", "evidence": title})
    if "？" in title or "?" in title:
        rules.append({"name": "提问式标题", "rule": "用一个具体问题制造点击理由。", "evidence": title})
    if "！" in title or "!" in title:
        rules.append({"name": "口播感标题", "rule": "用强语气让标题像一句现场发言。", "evidence": title})
    if re.search(r"\d", title):
        rules.append({"name": "数字钩子", "rule": "标题里放数字，暗示清单、步骤或结果。", "evidence": title})
    if len(title) <= 18:
        rules.append({"name": "短标题", "rule": "标题控制在短句内，先给情绪或悬念。", "evidence": title})
    if not rules:
        rules.append({"name": "观点标题", "rule": "用一句明确观点承载整篇 note 的角度。", "evidence": title})
    return rules


def _opening_rules(lines: list[str]) -> list[dict[str, str]]:
    if not lines:
        return []
    first = lines[0]
    rules = [{"name": "首句定场", "rule": "第一句先给场景、情绪或判断，不急着解释信息。", "evidence": first}]
    if len(first) <= 18:
        rules.append({"name": "短句开场", "rule": "用短句开场，让用户快速进入语境。", "evidence": first})
    if "？" in first or "?" in first:
        rules.append({"name": "问题开场", "rule": "开头抛问题，后文负责回答。", "evidence": first})
    return rules


def _body_steps(note: XHSNoteSample, lines: list[str]) -> list[dict[str, str]]:
    if _is_design_case(note, lines):
        return _design_case_body_steps(lines)
    steps: list[dict[str, str]] = []
    if lines:
        steps.append({"name": "开场", "rule": "先给情绪、场景或核心判断。", "evidence": lines[0]})
    question_lines = [line for line in lines if "？" in line or "?" in line]
    if question_lines:
        steps.append({"name": "连续追问", "rule": "用问题串推动阅读，让用户带着疑问往下看。", "evidence": question_lines[0]})
    section_lines = _section_markers(lines)
    if section_lines:
        steps.append({"name": "模块分段", "rule": "用明确小标题承载规则、方向、奖励或清单信息。", "evidence": section_lines[0]})
    cta_lines = _cta_lines(lines)
    if cta_lines:
        steps.append({"name": "行动收口", "rule": "结尾给发布、搜索、参与、收藏或购买动作。", "evidence": cta_lines[0]})
    tag_lines = [line for line in lines if "#" in line]
    if tag_lines:
        steps.append({"name": "话题归档", "rule": "用话题标签承接平台分发和活动入口。", "evidence": tag_lines[-1]})
    if len(steps) == 1 and len(lines) > 2:
        steps.append({"name": "叙事展开", "rule": "用多段短句逐步补充原因、细节和结果。", "evidence": lines[min(1, len(lines) - 1)]})
    return steps


def _interaction_rules(note: XHSNoteSample, lines: list[str]) -> list[dict[str, str]]:
    rules = []
    if note.tags:
        rules.append({"name": "话题入口", "rule": "保留核心话题标签，方便平台识别主题。", "evidence": " ".join(note.tags[:3])})
    cta_lines = _cta_lines(lines)
    if cta_lines:
        rules.append({"name": "明确动作", "rule": "给用户一个低成本动作，如搜索、发布、参与、收藏。", "evidence": cta_lines[0]})
    if note.metrics.get("commented", 0) > 0:
        rules.append({"name": "评论触发", "rule": "标题或正文要留下可回答的问题。", "evidence": f"comment_count={note.metrics['commented']}"})
    return rules


def _visual_rules(note: XHSNoteSample) -> list[dict[str, str]]:
    rules = [{"name": "封面先承担点击", "rule": "封面必须先表达主题、情绪或问题，不只是放素材。", "evidence": "cover.jpg"}]
    if note.image_count >= 3:
        rules.append({"name": "多图递进", "rule": "图集应承担信息递进：封面吸引，后续图补充细节。", "evidence": f"image_count={note.image_count}"})
    else:
        rules.append({"name": "少图集中", "rule": "少图笔记要让单张图完成主题表达。", "evidence": f"image_count={note.image_count}"})
    return rules


def _avoid_rules(note: XHSNoteSample, lines: list[str]) -> list[str]:
    rules = ["不要照搬原笔记句子，只抽结构和方法。", "不要把单篇个例直接当稳定规律。"]
    text = f"{note.title}\n" + "\n".join(lines)
    if "活动" in text or "奖励" in text:
        rules.append("活动型 note 不要只堆规则，要先给用户参与理由。")
    if "搜索" in text:
        rules.append("搜索引导要自然出现，不要像硬插入口令。")
    return rules


def _scene(note: XHSNoteSample, lines: list[str]) -> str:
    text = f"{note.title}\n" + "\n".join(lines)
    if _is_design_case(note, lines):
        return "设计案例解析型 note"
    if any(word in text for word in ("参与方式", "活动奖励", "发起", "活动页")):
        return "活动招募型 note"
    if any(word in text for word in ("教程", "步骤", "攻略", "怎么")):
        return "教程攻略型 note"
    if any(word in text for word in ("好物", "种草", "值得买", "推荐")):
        return "种草推荐型 note"
    if "？" in note.title or "?" in note.title:
        return "问题悬念型 note"
    return "观点叙事型 note"


def _goals(note: XHSNoteSample, lines: list[str]) -> list[str]:
    text = f"{note.title}\n" + "\n".join(lines)
    if _is_design_case(note, lines):
        return ["作品展示", "设计灵感", "品牌表达"]
    goals = []
    if any(word in text for word in ("参与", "发布", "活动", "奖励")):
        goals.append("活动参与")
    if any(word in text for word in ("搜索", "活动页", "话题")):
        goals.append("平台搜索")
    if any(word in text for word in ("收藏", "攻略", "清单")):
        goals.append("收藏")
    if any(word in text for word in ("评论", "你觉得", "谁说了算")):
        goals.append("互动")
    return goals or ["阅读完成"]


def _creative_goal(scene: str) -> str:
    if scene == "设计案例解析型 note":
        return "把一个设计项目讲成有背景、有方法、有审美判断的作品案例。"
    if scene == "活动招募型 note":
        return "先让用户理解参与理由，再交代参与方式和奖励。"
    if scene == "教程攻略型 note":
        return "把复杂信息拆成可收藏、可执行的步骤。"
    if scene == "种草推荐型 note":
        return "把产品或对象包装成具体生活场景里的解决方案。"
    if scene == "问题悬念型 note":
        return "用问题带动点击和评论，再在正文里逐步给答案。"
    return "用一个清晰观点组织内容，让用户愿意继续读完。"


def _section_markers(lines: list[str]) -> list[str]:
    return [line for line in lines if re.search(r"^【.+】", line) or line.endswith("：")][:5]


def _cta_lines(lines: list[str]) -> list[str]:
    keywords = ("搜索", "发布", "收藏", "评论", "私信", "下单", "购买", "进入", "参与方式", "参与活动")
    return [line for line in lines if any(keyword in line for keyword in keywords)][:5]


def _is_design_case(note: XHSNoteSample, lines: list[str]) -> bool:
    text = f"{note.title}\n" + "\n".join(lines)
    design_signals = ("视觉", "设计", "海报", "平面", "创作团队", "项目时间", "原创设计", "设计灵感")
    return note.category == "设计" and sum(1 for signal in design_signals if signal in text) >= 2


def _design_case_body_steps(lines: list[str]) -> list[dict[str, str]]:
    steps: list[dict[str, str]] = []
    if lines:
        steps.append({"name": "项目缘起", "rule": "先交代项目来源、主题或活动背景。", "evidence": lines[0]})
    context_line = _first_line_with(lines, ("通过", "在", "邀请", "起点"), start=1)
    if context_line:
        steps.append({"name": "场景展开", "rule": "用地点、对象或行动把设计项目放进真实语境。", "evidence": context_line})
    visual_line = _first_line_with(lines, ("视觉", "海报", "结构", "色", "图形", "字体"), start=1)
    if visual_line:
        steps.append({"name": "视觉方法", "rule": "说明设计系统、色彩、图形或版式如何服务主题。", "evidence": visual_line})
    meaning_line = _first_line_with(lines, ("不只是", "不只", "牵动", "意义", "联结"), start=1)
    if meaning_line:
        steps.append({"name": "概念升华", "rule": "从视觉方法上升到情绪、文化或品牌意义。", "evidence": meaning_line})
    credit_line = _first_line_with(lines, ("项目时间", "创作团队", "版权所有"), start=1)
    if credit_line:
        steps.append({"name": "项目信息", "rule": "保留项目时间、团队和版权信息，建立作品可信度。", "evidence": credit_line})
    tag_lines = [line for line in lines if "#" in line]
    if tag_lines:
        steps.append({"name": "话题归档", "rule": "用设计相关话题承接搜索、收藏和同好分发。", "evidence": tag_lines[-1]})
    return steps


def _first_line_with(lines: list[str], keywords: tuple[str, ...], *, start: int = 0) -> str:
    for line in lines[start:]:
        if any(keyword in line for keyword in keywords):
            return line
    return ""


def _confidence(note: XHSNoteSample, title_rules: list[dict[str, str]], body_steps: list[dict[str, str]]) -> float:
    score = 0.35
    if note.title:
        score += 0.1
    if note.desc:
        score += 0.1
    if note.tags:
        score += 0.08
    if note.image_count:
        score += 0.07
    if len(title_rules) >= 2:
        score += 0.1
    if len(body_steps) >= 3:
        score += 0.1
    if sum(note.metrics.values()) > 0:
        score += 0.1
    return round(min(score, 0.9), 2)


def _slug(value: str) -> str:
    text = str(value or "skill").strip().lower()
    text = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "_", text)
    return text.strip("_") or "skill"


def _report_stamp(source_keyword_dirs: dict[str, str]) -> str:
    for path_text in source_keyword_dirs.values():
        name = Path(path_text).name
        match = re.match(r"(\d{8}_\d{6})_", name)
        if match:
            return match.group(1)
    return "session"


def _skills_output(report: SessionSkillReport) -> dict[str, Any]:
    return {"skills": [skill.to_dict() for skill in report.skills]}


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result


# ============ 会话级辅助：规则桶 / 聚合 / metrics ============

GOAL_KEYWORDS = {
    "tutorial": ("教程", "攻略", "步骤", "怎么", "如何", "保姆", "上手", "入门", "新手"),
    "planting": ("推荐", "好物", "种草", "值得", "必入", "亲测", "宝藏"),
    "debrief": ("踩坑", "翻车", "经验", "复盘", "教训", "总结", "避雷"),
    "opinion": ("观点", "为什么", "我觉得", "看法", "本质", "其实", "争议"),
    "news": ("发布", "上线", "更新", "新版本", "首发", "官宣", "曝光", "重磅"),
    "rant": ("吐槽", "崩溃", "受不了", "无语", "笑死", "破防", "醉了"),
}

GOAL_LABEL_ZH = {
    "tutorial": "教程攻略",
    "planting": "种草推荐",
    "debrief": "经验复盘",
    "opinion": "观点输出",
    "news": "资讯爆料",
    "rant": "情绪吐槽",
    "general": "综合通用",
}

GOAL_CREATIVE = {
    "tutorial": "把复杂信息拆成可收藏、可照做的步骤。",
    "planting": "把产品或对象包装成具体生活场景里的解决方案。",
    "debrief": "用真实经历换一份可执行的避雷清单。",
    "opinion": "用一个清晰观点带动判断和讨论。",
    "news": "把第一手信息打成可二次传播的爆点片段。",
    "rant": "用情绪共鸣带出评论欲，再给一句缓冲收口。",
    "general": "用一个明确角度组织内容，让用户愿意读完。",
}


def _rule_goal(title: str, desc: str) -> str:
    text = f"{title}\n{desc}"
    scores: dict[str, int] = {}
    for goal, words in GOAL_KEYWORDS.items():
        hits = sum(1 for w in words if w in text)
        if hits:
            scores[goal] = hits
    if not scores:
        return "general"
    return max(scores, key=lambda k: scores[k])


def _merge_rules(rule_groups: list[list[dict[str, str]]], *, limit: int = 6) -> list[dict[str, str]]:
    """按 name 合并多篇规则；保留首次 evidence，限制条数。"""
    seen: dict[str, dict[str, str]] = {}
    for group in rule_groups:
        for item in group:
            name = (item.get("name") or "").strip()
            if not name or name in seen:
                continue
            seen[name] = {
                "name": name,
                "rule": item.get("rule", ""),
                "evidence": (item.get("evidence") or "")[:160],
            }
            if len(seen) >= limit:
                return list(seen.values())
    return list(seen.values())


def _body_steps_hot(note) -> list[dict[str, str]]:
    """HotNote 版 body 步骤抽取（不依赖 category）。"""
    lines = _content_lines(note.desc)
    steps: list[dict[str, str]] = []
    if lines:
        steps.append({"name": "开场", "rule": "先给情绪、场景或核心判断。", "evidence": lines[0]})
    question_lines = [l for l in lines if "？" in l or "?" in l]
    if question_lines:
        steps.append({"name": "连续追问", "rule": "用问题串推动阅读，让用户带着疑问往下看。", "evidence": question_lines[0]})
    section_lines = _section_markers(lines)
    if section_lines:
        steps.append({"name": "模块分段", "rule": "用明确小标题承载规则、方向、奖励或清单信息。", "evidence": section_lines[0]})
    cta_lines = _cta_lines(lines)
    if cta_lines:
        steps.append({"name": "行动收口", "rule": "结尾给发布、搜索、参与、收藏或购买动作。", "evidence": cta_lines[0]})
    tag_lines = [l for l in lines if "#" in l]
    if tag_lines:
        steps.append({"name": "话题归档", "rule": "用话题标签承接平台分发和活动入口。", "evidence": tag_lines[-1]})
    if len(steps) == 1 and len(lines) > 2:
        steps.append({"name": "叙事展开", "rule": "用多段短句逐步补充原因、细节和结果。", "evidence": lines[min(1, len(lines) - 1)]})
    return steps


def _interaction_rules_hot(note) -> list[dict[str, str]]:
    lines = _content_lines(note.desc)
    rules: list[dict[str, str]] = []
    if note.tags:
        rules.append({"name": "话题入口", "rule": "保留核心话题标签，方便平台识别主题。", "evidence": " ".join(note.tags[:3])})
    cta_lines = _cta_lines(lines)
    if cta_lines:
        rules.append({"name": "明确动作", "rule": "给用户一个低成本动作，如搜索、发布、参与、收藏。", "evidence": cta_lines[0]})
    if note.comment > 0:
        rules.append({"name": "评论触发", "rule": "标题或正文要留下可回答的问题。", "evidence": f"comment_count={note.comment}"})
    return rules


def _visual_rules_hot(note) -> list[dict[str, str]]:
    cover_evidence = note.cover_path or "cover"
    rules: list[dict[str, str]] = [
        {"name": "封面先承担点击", "rule": "封面必须先表达主题、情绪或问题，不只是放素材。", "evidence": cover_evidence}
    ]
    if note.image_count >= 3:
        rules.append({"name": "多图递进", "rule": "图集应承担信息递进：封面吸引，后续图补充细节。", "evidence": f"image_count={note.image_count}"})
    elif note.image_count > 0:
        rules.append({"name": "少图集中", "rule": "少图笔记要让单张图完成主题表达。", "evidence": f"image_count={note.image_count}"})
    if (note.note_type or "").lower() in ("video", "视频"):
        rules.append({"name": "前 3 秒钩子", "rule": "视频前 3 秒要先抛主题或情绪，不留缓冲。", "evidence": "note_type=video"})
    return rules


def _cover_rules_for_cluster(notes, goal: str, tone: str) -> list[dict[str, str]]:
    sample = notes[0] if notes else None
    title = (sample.title if sample else "") or ""
    cover_evidence = next((n.cover_path for n in notes if n.cover_path), "cover")
    image_counts = [n.image_count for n in notes if n.image_count]
    max_image_count = max(image_counts, default=0)
    rules = [
        {
            "name": "封面一句话钩子",
            "rule": f"封面主文案用 6-14 个字说清这类内容的点击理由，优先承接标题里的结果、问题或情绪；不要把正文摘要整段搬上封面。类型：{_goal_label(goal, tone)}。",
            "evidence": title[:80] or cover_evidence,
        },
        {
            "name": "双层信息层级",
            "rule": "封面只保留主标题和一个辅助信息层：主标题最大、辅助信息更小，可放数字、对象或场景；不要超过 3 组文字块。",
            "evidence": cover_evidence,
        },
        {
            "name": "主体画面占位",
            "rule": "产品、人物、截图或设计稿必须成为第一视觉主体，占画面约 60%-75%；四周留安全边，避免标题压住主体关键细节。",
            "evidence": f"image_count={max_image_count}" if max_image_count else cover_evidence,
        },
        {
            "name": "情绪符号强化",
            "rule": f"根据语气加一个明确情绪符号：吐槽类用夸张表情或反差字词，专业类用干净标签和编号，朋友安利用生活化场景词。当前语气：{tone or '未标注'}。",
            "evidence": tone or title[:80] or cover_evidence,
        },
        {
            "name": "图文一致校验",
            "rule": "封面承诺必须能在标题或正文第一屏找到对应信息；不能用与笔记证据无关的大词、夸张收益或误导性前后对比。",
            "evidence": title[:80] or cover_evidence,
        },
    ]
    if max_image_count >= 3:
        rules.append({
            "name": "多图封面分工",
            "rule": "封面只负责点击和主题判断，后续图片再拆步骤、细节、清单或案例；不要把所有卖点塞进第一张。",
            "evidence": f"image_count={max_image_count}",
        })
    return rules


def _avoid_rules_hot(note) -> list[str]:
    rules = ["不要照搬原笔记句子，只抽结构和方法。", "不要把单篇个例直接当稳定规律。"]
    text = (note.title or "") + "\n" + (note.desc or "")
    if "活动" in text or "奖励" in text:
        rules.append("活动型 note 不要只堆规则，要先给用户参与理由。")
    if "搜索" in text:
        rules.append("搜索引导要自然出现，不要像硬插入口令。")
    return rules


def _percentile(values: list[int], q: float) -> int:
    if not values:
        return 0
    sorted_v = sorted(values)
    idx = max(0, min(len(sorted_v) - 1, int(round((len(sorted_v) - 1) * q))))
    return int(sorted_v[idx])


def _majority_note_type(types: list[str]) -> str:
    cleaned = [str(t).strip().lower() for t in types if t and str(t).strip()]
    if not cleaned:
        return "图文"
    counter = Counter(cleaned)
    top, count = counter.most_common(1)[0]
    if count * 2 < len(cleaned):
        return "混合"
    if top in ("video", "视频"):
        return "视频"
    return "图文"


def _goal_label(goal: str, tone: str) -> str:
    base = GOAL_LABEL_ZH.get(goal, goal)
    return f"{base}·{tone}" if tone else base


def _goal_creative(goal: str) -> str:
    return GOAL_CREATIVE.get(goal, GOAL_CREATIVE["general"])


# ============ 关键词 / 标签 LLM ============

KEYWORD_SYSTEM_PROMPT = "你是 Nori 的小红书选词助手，只输出 JSON。"

KEYWORD_USER_PROMPT = """\
根据本次创作 context，给出 1-{max_n} 个小红书搜索关键词。

context:
{context}

要求：
1. 每个关键词长度 2-12 个汉字，能让小红书搜索召回到相关内容。
2. 关键词要覆盖 context 里描述的话题或场景，不要发散。
3. 不要返回品牌名或带 #/【】 等特殊符号。
4. 输出 JSON: {{"keywords": ["...", "..."]}}
"""

LABEL_SYSTEM_PROMPT = "你是 Nori 的小红书笔记目标识别助手，只输出 JSON。"

LABEL_USER_PROMPT = """\
给下面这批小红书笔记每篇打 goal 和 tone 标签。

候选 goal: tutorial / planting / debrief / opinion / news / rant / general
候选 tone（不限于）: 科普 / 吐槽 / 朋友安利 / 专业测评 / 干货 / 个人经验

笔记列表:
{notes}

输出 JSON: {{"labels": [{{"note_id": "...", "goal": "...", "tone": "..."}}, ...]}}
"""


def _llm_generate_keywords(context: dict[str, Any], *, max_n: int = 3) -> list[str]:
    data = llms.chat_json(
        [
            {"role": "system", "content": KEYWORD_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": KEYWORD_USER_PROMPT.format(
                    max_n=max_n,
                    context=json.dumps(
                        {k: v for k, v in context.items() if k != "keywords"},
                        ensure_ascii=False,
                    ),
                ),
            },
        ],
        usage="llm",
        timeout=30,
        _chat=llms.chat,
    )
    items = data.get("keywords") if isinstance(data, dict) else None
    if not isinstance(items, list):
        return []
    out: list[str] = []
    for item in items:
        text = str(item or "").strip()
        if text and text not in out:
            out.append(text[:20])
        if len(out) >= max_n:
            break
    return out


def _llm_label_notes(hot_notes) -> dict[str, dict[str, str]]:
    if not hot_notes:
        return {}
    items = [
        {
            "note_id": n.note_id,
            "title": n.title,
            "desc": (n.desc or "")[:200],
            "tags": list(n.tags)[:5],
            "metrics": {"liked": n.liked, "collected": n.collected},
        }
        for n in hot_notes
    ]
    data = llms.chat_json(
        [
            {"role": "system", "content": LABEL_SYSTEM_PROMPT},
            {"role": "user", "content": LABEL_USER_PROMPT.format(notes=json.dumps(items, ensure_ascii=False))},
        ],
        usage="llm",
        timeout=120,
        _chat=llms.chat,
    )
    out: dict[str, dict[str, str]] = {}
    if not isinstance(data, dict):
        return out
    labels = data.get("labels")
    if not isinstance(labels, list):
        return out
    valid_goals = set(GOAL_KEYWORDS) | {"general"}
    for item in labels:
        if not isinstance(item, dict):
            continue
        nid = str(item.get("note_id") or "").strip()
        if not nid:
            continue
        goal = str(item.get("goal") or "").strip().lower()
        if goal not in valid_goals:
            goal = "general"
        tone = str(item.get("tone") or "").strip()[:20]
        out[nid] = {"goal": goal, "tone": tone}
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze XHS note data into a seed skill draft.")
    parser.add_argument("--data-root", default="cold_start_data/xhs")
    parser.add_argument("--category", default="设计")
    parser.add_argument("--meta-path", default="")
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--no-llm", action="store_true")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    analyzer = XHSNoteAnalyzer(args.data_root, use_llm=not args.no_llm)
    note = analyzer.load_note(args.meta_path) if args.meta_path else analyzer.pick_random_note(args.category, seed=args.seed)
    skill = analyzer.analyze_note(note)
    print(json.dumps(skill.to_dict(), ensure_ascii=False, indent=2 if args.pretty else None))


if __name__ == "__main__":
    main()
