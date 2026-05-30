"""Tests for CoverDirector cover prompt helper."""

from __future__ import annotations

import pytest

from nori.agents.content_generation.models import CandidateTitle, NoteDraft
from nori.agents.content_generation.cover_director.package import CoverPromptBuilder


cover_prompt = CoverPromptBuilder()


class _PromptError(RuntimeError):
    pass


def _draft() -> NoteDraft:
    return NoteDraft(
        skill_id="planting",
        title="通勤香薰｜复购的小确幸",
        body="正文",
        tags=["香薰"],
        comment_hook="评论区告诉我",
        cover_path="",
        image_paths=[],
        candidate_titles=[CandidateTitle(text="通勤香薰｜复购的小确幸")],
        metrics_target={},
        asset_bundle={
            "brand_facts": ["小众设计师品牌", "手工调香"],
            "text_points": ["下班通勤香气治愈", "扩香稳定", "瓶身好看", "第四个卖点不进入 prompt"],
        },
        validation={"status": "pass", "issues": []},
        llm_enhanced=True,
    )


def _skill() -> dict:
    return {
        "tone": "朋友安利",
        "note_type": "图文",
        "creative_goal": "真实讲清楚使用感。",
        "cover_rules": [{"name": "一句话钩子", "rule": "封面 6-14 字钩子"}],
        "visual_rules": [{"name": "封面承担点击", "rule": "主体清晰"}],
        "avoid_rules": ["不要硬广价格"],
    }


def test_design_prompt_llm_builds_cover_prompt_contract():
    calls: list[dict] = []

    def fake_json_call(**kwargs):
        calls.append(kwargs)
        return {"prompt": "A vertical 3:4 cover with warm light and Chinese title text."}

    prompt = cover_prompt.design_with_llm(
        _draft(),
        _skill(),
        ["/tmp/ref-a.png", "/tmp/ref-b.png"],
        {"user_text": "突出通勤治愈感"},
        json_call=fake_json_call,
        error_type=_PromptError,
    )

    assert prompt.startswith("A vertical 3:4 cover")
    assert len(calls) == 1
    assert calls[0]["system"] == "你是 Nori 的封面 prompt 工序，只输出 JSON。"
    assert calls[0]["timeout"] == 60
    user_prompt = calls[0]["user"]
    assert "通勤香薰｜复购的小确幸" in user_prompt
    assert "小众设计师品牌" in user_prompt
    assert "下班通勤香气治愈" in user_prompt
    assert "第四个卖点不进入 prompt" not in user_prompt
    assert "参考图数量：2" in user_prompt
    assert "只输出 JSON" in user_prompt


def test_design_prompt_llm_raises_domain_error_for_empty_prompt():
    def fake_json_call(**kwargs):  # noqa: ARG001
        return {"prompt": "  "}

    with pytest.raises(_PromptError, match="返回空 prompt"):
        cover_prompt.design_with_llm(
            _draft(),
            _skill(),
            [],
            {},
            json_call=fake_json_call,
            error_type=_PromptError,
        )
