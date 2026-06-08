"""Tests for XHS single-note optional LLM enhancement helpers."""

from __future__ import annotations

from pathlib import Path

import nori.core.llms as llms

from nori.agents.market_analysis.schemas import XHSNoteSample
from nori.agents.market_analysis.xhs_note_analyzer import note_llm as xhs_note_llm
from nori.agents.market_analysis.xhs_note_analyzer import rules as xhs_note_rules


def _note() -> XHSNoteSample:
    return XHSNoteSample(
        meta_path=Path("cold_start_data/xhs/设计/author_1/posts/note_1/meta.json"),
        category="设计",
        author_id="author_1",
        author_name="测试作者",
        note_id="note_1",
        title="报告！ 年夜饭薯该宠幸谁？",
        desc="年夜饭的仪式感很多。\n什么？你问这些搭配中不中？\n在搜索框输入答案之书。",
        tags=["新年答案之书"],
        metrics={"liked": 102, "collected": 22, "comment": 20, "share": 6},
        image_count=3,
        note_type="normal",
        note_url="https://www.xiaohongshu.com/explore/note_1",
    )


def _draft():
    return xhs_note_rules.rule_analyze_note(_note())


def test_enhance_note_routes_optional_json_stage_through_shared_helper(monkeypatch):
    calls: list[dict] = []

    def fake_chat_json(messages, *, usage="llm", **kwargs):
        calls.append({"messages": messages, "usage": usage, "kwargs": kwargs})
        return {
            "match": {"scene": "chat_json 场景", "goals": ["收藏"], "note_type": "图文"},
            "craft": {"creative_goal": "通过统一 JSON helper 增强规则。"},
            "evidence": {"llm_observations": ["已路由到 llms.chat_json"]},
            "validation": {"llm_notes": ["保持 analyzer 降级语义不变。"]},
        }

    monkeypatch.setattr(llms, "chat_json", fake_chat_json)

    enhanced = xhs_note_llm.enhance_note(_note(), _draft())

    assert enhanced.match["scene"] == "chat_json 场景"
    assert enhanced.validation["llm_enhanced"] is True
    assert calls
    assert calls[0]["usage"] == "llm"
    assert "_chat" not in calls[0]["kwargs"]
    assert calls[0]["kwargs"]["timeout"] == 60
    assert calls[0]["kwargs"]["json_mode"] is True
    assert "规则草案" in calls[0]["messages"][1]["content"]


def test_normalize_llm_draft_preserves_fallbacks_and_caps_fields():
    fallback = _draft()
    normalized = xhs_note_llm.normalize_llm_draft(
        {
            "match": {"scene": "很长" * 20, "goals": ["互动", "活动参与", "收藏", "多余"]},
            "craft": {
                "title_rules": [{"name": "问题钩子" * 10, "description": "标题先抛问题" * 40}],
                "avoid_rules": ["不要硬广"] * 10,
            },
            "evidence": {"llm_observations": ["观察"] * 8},
            "validation": {"llm_notes": ["验证"] * 5},
        },
        fallback,
    )

    assert len(normalized.match["scene"]) == 30
    assert normalized.match["goals"] == ["互动", "活动参与", "收藏"]
    assert normalized.craft["creative_goal"] == fallback.craft["creative_goal"]
    assert len(normalized.craft["title_rules"][0]["name"]) == 30
    assert len(normalized.craft["title_rules"][0]["rule"]) == 180
    assert len(normalized.craft["avoid_rules"]) == 1
    assert normalized.evidence["llm_observations"] == ["观察"]
    assert normalized.validation["llm_notes"] == ["验证"]
    assert normalized.validation["pipeline"] == ["rule_analyzer", "llm_enhancer", "format_normalizer"]


def test_enhance_note_fallback_attaches_redacted_llm_error(monkeypatch):
    def broken_chat_json(*args, **kwargs):
        raise RuntimeError("llm down")

    monkeypatch.setattr(llms, "chat_json", broken_chat_json)

    fallback = xhs_note_llm.enhance_note(_note(), _draft())

    assert fallback.validation["llm_enhanced"] is False
    assert fallback.validation["pipeline"] == ["rule_analyzer", "llm_enhancer_failed", "format_normalizer"]
    assert fallback.validation["llm_error"]["stage"] == "xhs_note_analyzer"
    assert fallback.validation["llm_error"]["reason"] == "api_error"
    assert fallback.validation["llm_error"]["error_type"] == "RuntimeError"
