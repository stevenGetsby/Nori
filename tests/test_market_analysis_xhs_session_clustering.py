"""Tests for XHS session note clustering helpers."""

from __future__ import annotations

import pytest

from data_collect import HotNote
from nori.market_analysis.xhs_note_analyzer import session_clustering as xhs_session_clustering


def _note(note_id: str, title: str, *, desc: str = "", liked: int = 100) -> HotNote:
    return HotNote(
        note_id=note_id,
        keyword="测试关键词",
        title=title,
        desc=desc,
        author_id=f"author_{note_id}",
        author_name=f"作者 {note_id}",
        liked=liked,
        collected=10,
        comment=1,
        share=1,
        tags=[],
        image_count=1,
        note_type="normal",
        note_url=f"https://www.xiaohongshu.com/explore/{note_id}",
        time_ms=1778000000000,
    )


def test_rule_goal_classifies_text_from_keyword_signals():
    assert xhs_session_clustering.rule_goal("3 个新手教程", "保姆级步骤") == "tutorial"
    assert xhs_session_clustering.rule_goal("宝藏好物推荐", "亲测值得买") == "planting"
    assert xhs_session_clustering.rule_goal("普通日常", "没有明显信号") == "general"


def test_cluster_hot_notes_groups_by_llm_goal_and_tracks_leftovers():
    notes = [
        _note("n1", "教程 1"),
        _note("n2", "教程 2"),
        _note("n3", "推荐 1"),
        _note("n4", "复盘 1"),
        _note("n5", "观点 1"),
        _note("n6", "资讯 1"),
    ]
    labels = {
        "n1": {"goal": "tutorial", "tone": "干货"},
        "n2": {"goal": "tutorial", "tone": "干货"},
        "n3": {"goal": "planting", "tone": "朋友安利"},
        "n4": {"goal": "debrief", "tone": "个人经验"},
        "n5": {"goal": "opinion", "tone": "观点"},
        "n6": {"goal": "news", "tone": "资讯"},
    }

    clusters, leftover, llm_used = xhs_session_clustering.cluster_hot_notes(
        notes,
        label_notes=lambda value: labels,
    )

    assert llm_used is True
    assert [cluster["goal"] for cluster in clusters] == ["tutorial", "planting", "debrief", "opinion"]
    assert clusters[0]["tone"] == "干货"
    assert [note.note_id for note in clusters[0]["notes"]] == ["n1", "n2"]
    assert leftover == ["n6"]


def test_cluster_hot_notes_fails_when_llm_labels_are_empty_or_missing():
    notes = [_note("n1", "教程 1"), _note("n2", "教程 2")]

    with pytest.raises(RuntimeError, match="LLM 标签结果为空"):
        xhs_session_clustering.cluster_hot_notes(notes, label_notes=lambda value: {})

    with pytest.raises(RuntimeError, match="LLM 标签缺失 1 篇笔记"):
        xhs_session_clustering.cluster_hot_notes(
            notes,
            label_notes=lambda value: {"n1": {"goal": "tutorial", "tone": "干货"}},
        )
