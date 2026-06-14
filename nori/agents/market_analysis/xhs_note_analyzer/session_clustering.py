"""Session-level clustering helpers for XHS hot notes."""
from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any, Callable


GOAL_KEYWORDS = {
    "tutorial": ("教程", "攻略", "步骤", "怎么", "如何", "保姆", "上手", "入门", "新手"),
    "planting": ("推荐", "好物", "种草", "值得", "必入", "亲测", "宝藏"),
    "debrief": ("踩坑", "翻车", "经验", "复盘", "教训", "总结", "避雷"),
    "opinion": ("观点", "为什么", "我觉得", "看法", "本质", "其实", "争议"),
    "news": ("发布", "上线", "更新", "新版本", "首发", "官宣", "曝光", "重磅"),
    "rant": ("吐槽", "崩溃", "受不了", "无语", "笑死", "破防", "醉了"),
}


def cluster_hot_notes(
    hot_notes: list[Any],
    *,
    label_notes: Callable[[list[Any]], dict[str, dict[str, str]]],
) -> tuple[list[dict[str, Any]], list[str], bool]:
    """Cluster hot notes into at most four goal buckets using LLM labels."""

    if not hot_notes:
        return [], [], False

    rule_labels: dict[str, str] = {note.note_id: rule_goal(note.title, note.desc) for note in hot_notes}
    llm_labels = label_notes(hot_notes)
    if not llm_labels:
        raise RuntimeError("LLM 标签结果为空，停止生成 skill")
    final_labels: dict[str, tuple[str, str]] = {}
    for note in hot_notes:
        info = llm_labels.get(note.note_id) or {}
        goal = info.get("goal") or rule_labels.get(note.note_id) or "general"
        tone = info.get("tone") or ""
        final_labels[note.note_id] = (goal, tone)

    buckets: dict[str, list[Any]] = defaultdict(list)
    tones_per_bucket: dict[str, list[str]] = defaultdict(list)
    for note in hot_notes:
        goal, tone = final_labels[note.note_id]
        buckets[goal].append(note)
        if tone:
            tones_per_bucket[goal].append(tone)

    sorted_buckets = sorted(buckets.items(), key=lambda item: -len(item[1]))
    keep = sorted_buckets[:4]
    leftover: list[str] = []
    for _goal, notes in sorted_buckets[4:]:
        leftover.extend(note.note_id for note in notes)

    clusters = []
    for goal, notes in keep:
        tones = tones_per_bucket.get(goal) or []
        tone = Counter(tones).most_common(1)[0][0] if tones else ""
        clusters.append(
            {
                "goal": goal,
                "notes": notes,
                "tone": tone,
                "rule_goal_distribution": dict(Counter(rule_labels[note.note_id] for note in notes)),
            }
        )
    return clusters, leftover, True


def rule_goal(title: str, desc: str) -> str:
    text = f"{title}\n{desc}"
    scores: dict[str, int] = {}
    for goal, words in GOAL_KEYWORDS.items():
        hits = sum(1 for word in words if word in text)
        if hits:
            scores[goal] = hits
    if not scores:
        return "general"
    return max(scores, key=lambda key: scores[key])


__all__ = ["GOAL_KEYWORDS", "cluster_hot_notes", "rule_goal"]
