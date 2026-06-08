"""Tests for XHS session skill-building helpers."""

from __future__ import annotations

from data_collect import HotNote
from nori.agents.market_analysis.schemas import NoteSkill
from nori.agents.market_analysis.xhs_note_analyzer import skill_builder as xhs_skill_builder


def _note(
    note_id: str,
    title: str,
    *,
    desc: str,
    liked: int,
    collected: int,
    note_type: str = "normal",
    image_count: int = 2,
) -> HotNote:
    return HotNote(
        note_id=note_id,
        keyword="测试关键词",
        title=title,
        desc=desc,
        author_id=f"author_{note_id}",
        author_name=f"作者 {note_id}",
        liked=liked,
        collected=collected,
        comment=3,
        share=1,
        tags=["封面设计", "小红书运营"],
        image_count=image_count,
        note_type=note_type,
        note_url=f"https://www.xiaohongshu.com/explore/{note_id}",
        time_ms=1778000000000,
        cover_path=f"/tmp/{note_id}/cover.jpg",
        image_paths=[f"/tmp/{note_id}/image_0.jpg"],
    )


def test_build_note_skill_aggregates_rules_metrics_and_evidence():
    notes = [
        _note("n1", "3 个方法做出有点击欲的封面", desc="先给结果。\n评论区告诉我你喜欢哪版。", liked=100, collected=20, image_count=4),
        _note("n2", "这类种草封面为什么更想点", desc="用真实场景承接产品价值。\n最后给收藏理由。", liked=80, collected=18),
    ]
    cluster = {
        "goal": "planting",
        "tone": "朋友安利",
        "notes": notes,
        "rule_goal_distribution": {"planting": 2},
    }

    skill = xhs_skill_builder.build_note_skill(cluster, context={"topic": "封面设计"})

    assert isinstance(skill, NoteSkill)
    assert skill.skill_id == "种草推荐·朋友安利笔记制作指南"
    assert skill.label == "种草推荐·朋友安利"
    assert skill.goal == "planting"
    assert skill.tone == "朋友安利"
    assert skill.note_type == "图文"
    assert skill.metrics_summary == {
        "liked_p25": 80,
        "liked_p50": 80,
        "liked_p75": 100,
        "collected_p50": 18,
        "sample": 2,
    }
    assert skill.evidence_notes[0].note_id == "n1"
    assert skill.evidence_notes[0].quoted_segments == ["先给结果。", "评论区告诉我你喜欢哪版。"]
    assert skill.cluster_signals == {"rule_goal_distribution": {"planting": 2}, "size": 2}
    assert any(rule["name"] == "封面一句话钩子" for rule in skill.cover_rules)


def test_majority_note_type_and_percentile_helpers_are_stable():
    assert xhs_skill_builder.majority_note_type(["video", "video", "normal"]) == "视频"
    assert xhs_skill_builder.majority_note_type(["video", "normal"]) == "视频"
    assert xhs_skill_builder.majority_note_type([]) == "图文"
    assert xhs_skill_builder.percentile([80, 100, 120], 0.5) == 100
    assert xhs_skill_builder.percentile([], 0.5) == 0
