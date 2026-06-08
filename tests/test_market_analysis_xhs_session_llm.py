"""Tests for XHS session LLM keyword and label helpers."""

from __future__ import annotations

import json

import nori.core.llms as llms
import pytest

from data_collect import HotNote
from nori.agents.market_analysis.xhs_note_analyzer import session_llm as xhs_session_llm


def _note(note_id: str, *, desc: str = "", tags: list[str] | None = None) -> HotNote:
    return HotNote(
        note_id=note_id,
        keyword="测试关键词",
        title=f"标题 {note_id}",
        desc=desc,
        author_id=f"author_{note_id}",
        author_name=f"作者 {note_id}",
        liked=100,
        collected=10,
        comment=1,
        share=1,
        tags=tags or [],
        image_count=1,
        note_type="normal",
        note_url=f"https://www.xiaohongshu.com/explore/{note_id}",
        time_ms=1778000000000,
    )


def test_generate_keywords_routes_through_shared_json_helper(monkeypatch):
    calls: list[dict] = []

    def fake_chat_json(messages, *, usage="llm", **kwargs):
        calls.append({"messages": messages, "usage": usage, "kwargs": kwargs})
        return {"keywords": [" 封面设计 ", "封面设计", "小红书运营", "超出数量"]}

    monkeypatch.setattr(llms, "chat_json", fake_chat_json)

    keywords = xhs_session_llm.generate_keywords({"topic": "封面设计", "keywords": ["ignored"]}, max_n=2)

    assert keywords == ["封面设计", "小红书运营"]
    assert calls
    assert calls[0]["usage"] == "llm"
    assert "_chat" not in calls[0]["kwargs"]
    assert calls[0]["kwargs"]["timeout"] == 30
    assert calls[0]["kwargs"]["json_mode"] is True
    assert "ignored" not in calls[0]["messages"][1]["content"]


def test_label_notes_normalizes_llm_labels(monkeypatch):
    calls: list[dict] = []

    def fake_chat_json(messages, *, usage="llm", **kwargs):
        calls.append({"messages": messages, "usage": usage, "kwargs": kwargs})
        assert "笔记列表" in messages[1]["content"]
        assert "TAIL_AFTER_200" not in messages[1]["content"]
        return {
            "labels": [
                {"note_id": "n1", "goal": "planting", "tone": "朋友安利"},
                {"note_id": "n2", "goal": "unknown", "tone": "1234567890123456789012345"},
                {"note_id": "", "goal": "tutorial", "tone": "干货"},
            ]
        }

    monkeypatch.setattr(llms, "chat_json", fake_chat_json)
    notes = [
        _note("n1", desc="正常描述", tags=["a", "b", "c", "d", "e", "f"]),
        _note("n2", desc=("长描述" * 70) + "TAIL_AFTER_200"),
    ]

    labels = xhs_session_llm.label_notes(notes)

    assert labels == {
        "n1": {"goal": "planting", "tone": "朋友安利"},
        "n2": {"goal": "general", "tone": "12345678901234567890"},
    }
    assert "_chat" not in calls[0]["kwargs"]
    assert calls[0]["kwargs"]["timeout"] == 120
    assert calls[0]["kwargs"]["json_mode"] is True
    notes_json = calls[0]["messages"][1]["content"].split("笔记列表:\n", 1)[1].split("\n\n输出 JSON:", 1)[0]
    prompt_notes = json.loads(notes_json)
    assert prompt_notes[0]["tags"] == ["a", "b", "c", "d", "e"]
    assert len(prompt_notes[1]["desc"]) == 200


def test_label_notes_returns_empty_for_empty_notes_without_llm(monkeypatch):
    def fail_chat_json(*args, **kwargs):
        raise AssertionError("LLM should not be called for empty notes")

    monkeypatch.setattr(llms, "chat_json", fail_chat_json)

    assert xhs_session_llm.label_notes([]) == {}


def test_generate_keywords_raises_stage_specific_error(monkeypatch):
    def broken_chat_json(*args, **kwargs):
        raise RuntimeError("llm down")

    monkeypatch.setattr(llms, "chat_json", broken_chat_json)

    with pytest.raises(xhs_session_llm.XHSSessionLLMError, match="llm down"):
        xhs_session_llm.generate_keywords({"topic": "封面设计"})
