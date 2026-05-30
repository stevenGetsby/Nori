"""Build session-level NoteSkill objects from clustered XHS hot notes."""
from __future__ import annotations

from collections import Counter
from typing import Any

from nori.agents.market_analysis.models import NoteEvidence, NoteSkill
from nori.shared.normalization import dedupe_preserve_order
from . import rules as xhs_note_rules


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


def build_note_skill(cluster: dict[str, Any], context: dict[str, Any] | None = None) -> NoteSkill:
    notes = cluster["notes"]
    goal = cluster["goal"]
    tone = cluster["tone"]

    title_rule_rows = merge_rules([xhs_note_rules.title_rules(note.title) for note in notes], limit=6)
    opening_rule_rows = merge_rules([xhs_note_rules.opening_rules(xhs_note_rules.content_lines(note.desc)) for note in notes], limit=5)
    body_rule_rows = merge_rules([body_steps_hot(note) for note in notes], limit=6)
    interaction_rule_rows = merge_rules([interaction_rules_hot(note) for note in notes], limit=4)
    visual_rule_rows = merge_rules([visual_rules_hot(note) for note in notes], limit=4)
    cover_rule_rows = cover_rules_for_cluster(notes, goal, tone)
    avoid_rule_rows = dedupe([rule for note in notes for rule in avoid_rules_hot(note)])[:6]

    likes = [note.liked for note in notes]
    collecteds = [note.collected for note in notes]
    metrics_summary = {
        "liked_p25": percentile(likes, 0.25),
        "liked_p50": percentile(likes, 0.5),
        "liked_p75": percentile(likes, 0.75),
        "collected_p50": percentile(collecteds, 0.5),
        "sample": len(notes),
    }

    evidence_notes = [
        NoteEvidence(
            note_id=note.note_id,
            note_url=note.note_url,
            title=note.title,
            liked=note.liked,
            collected=note.collected,
            keyword=note.keyword,
            cover_path=note.cover_path,
            image_paths=list(note.image_paths),
            video_path=note.video_path,
            quoted_segments=xhs_note_rules.content_lines(note.desc)[:2],
        )
        for note in notes
    ]

    label = goal_label(goal, tone)
    return NoteSkill(
        skill_id=f"{label}笔记制作指南",
        label=label,
        goal=goal,
        note_type=majority_note_type([note.note_type for note in notes]),
        tone=tone or "未标注",
        creative_goal=goal_creative(goal),
        title_rules=title_rule_rows,
        opening_rules=opening_rule_rows,
        body_structure=body_rule_rows,
        interaction_rules=interaction_rule_rows,
        visual_rules=visual_rule_rows,
        cover_rules=cover_rule_rows,
        avoid_rules=avoid_rule_rows,
        metrics_summary=metrics_summary,
        evidence_notes=evidence_notes,
        cluster_signals={
            "rule_goal_distribution": cluster.get("rule_goal_distribution", {}),
            "size": len(notes),
        },
    )


def merge_rules(rule_groups: list[list[dict[str, str]]], *, limit: int = 6) -> list[dict[str, str]]:
    """Merge rule rows by name, preserving first evidence."""

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


def body_steps_hot(note: Any) -> list[dict[str, str]]:
    lines = xhs_note_rules.content_lines(note.desc)
    steps: list[dict[str, str]] = []
    if lines:
        steps.append({"name": "开场", "rule": "先给情绪、场景或核心判断。", "evidence": lines[0]})
    question_lines = [line for line in lines if "？" in line or "?" in line]
    if question_lines:
        steps.append({"name": "连续追问", "rule": "用问题串推动阅读，让用户带着疑问往下看。", "evidence": question_lines[0]})
    section_lines = xhs_note_rules.section_markers(lines)
    if section_lines:
        steps.append({"name": "模块分段", "rule": "用明确小标题承载规则、方向、奖励或清单信息。", "evidence": section_lines[0]})
    cta_lines = xhs_note_rules.cta_lines(lines)
    if cta_lines:
        steps.append({"name": "行动收口", "rule": "结尾给发布、搜索、参与、收藏或购买动作。", "evidence": cta_lines[0]})
    tag_lines = [line for line in lines if "#" in line]
    if tag_lines:
        steps.append({"name": "话题归档", "rule": "用话题标签承接平台分发和活动入口。", "evidence": tag_lines[-1]})
    if len(steps) == 1 and len(lines) > 2:
        steps.append({"name": "叙事展开", "rule": "用多段短句逐步补充原因、细节和结果。", "evidence": lines[min(1, len(lines) - 1)]})
    return steps


def interaction_rules_hot(note: Any) -> list[dict[str, str]]:
    lines = xhs_note_rules.content_lines(note.desc)
    rules: list[dict[str, str]] = []
    if note.tags:
        rules.append({"name": "话题入口", "rule": "保留核心话题标签，方便平台识别主题。", "evidence": " ".join(note.tags[:3])})
    cta_lines = xhs_note_rules.cta_lines(lines)
    if cta_lines:
        rules.append({"name": "明确动作", "rule": "给用户一个低成本动作，如搜索、发布、参与、收藏。", "evidence": cta_lines[0]})
    if note.comment > 0:
        rules.append({"name": "评论触发", "rule": "标题或正文要留下可回答的问题。", "evidence": f"comment_count={note.comment}"})
    return rules


def visual_rules_hot(note: Any) -> list[dict[str, str]]:
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


def cover_rules_for_cluster(notes: list[Any], goal: str, tone: str) -> list[dict[str, str]]:
    sample = notes[0] if notes else None
    title = (sample.title if sample else "") or ""
    cover_evidence = next((note.cover_path for note in notes if note.cover_path), "cover")
    image_counts = [note.image_count for note in notes if note.image_count]
    max_image_count = max(image_counts, default=0)
    rules = [
        {
            "name": "封面一句话钩子",
            "rule": f"封面主文案用 6-14 个字说清这类内容的点击理由，优先承接标题里的结果、问题或情绪；不要把正文摘要整段搬上封面。类型：{goal_label(goal, tone)}。",
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
        rules.append(
            {
                "name": "多图封面分工",
                "rule": "封面只负责点击和主题判断，后续图片再拆步骤、细节、清单或案例；不要把所有卖点塞进第一张。",
                "evidence": f"image_count={max_image_count}",
            }
        )
    return rules


def avoid_rules_hot(note: Any) -> list[str]:
    rules = ["不要照搬原笔记句子，只抽结构和方法。", "不要把单篇个例直接当稳定规律。"]
    text = (note.title or "") + "\n" + (note.desc or "")
    if "活动" in text or "奖励" in text:
        rules.append("活动型 note 不要只堆规则，要先给用户参与理由。")
    if "搜索" in text:
        rules.append("搜索引导要自然出现，不要像硬插入口令。")
    return rules


def percentile(values: list[int], q: float) -> int:
    if not values:
        return 0
    sorted_values = sorted(values)
    index = max(0, min(len(sorted_values) - 1, int(round((len(sorted_values) - 1) * q))))
    return int(sorted_values[index])


def majority_note_type(types: list[str]) -> str:
    cleaned = [str(value).strip().lower() for value in types if value and str(value).strip()]
    if not cleaned:
        return "图文"
    counter = Counter(cleaned)
    top, count = counter.most_common(1)[0]
    if count * 2 < len(cleaned):
        return "混合"
    if top in ("video", "视频"):
        return "视频"
    return "图文"


def goal_label(goal: str, tone: str) -> str:
    base = GOAL_LABEL_ZH.get(goal, goal)
    return f"{base}·{tone}" if tone else base


def goal_creative(goal: str) -> str:
    return GOAL_CREATIVE.get(goal, GOAL_CREATIVE["general"])


def dedupe(items: list[str]) -> list[str]:
    return dedupe_preserve_order(items)


__all__ = [
    "GOAL_CREATIVE",
    "GOAL_LABEL_ZH",
    "avoid_rules_hot",
    "body_steps_hot",
    "build_note_skill",
    "cover_rules_for_cluster",
    "dedupe",
    "goal_creative",
    "goal_label",
    "interaction_rules_hot",
    "majority_note_type",
    "merge_rules",
    "percentile",
    "visual_rules_hot",
]
