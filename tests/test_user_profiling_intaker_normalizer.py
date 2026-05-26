"""Tests for Intake text normalization helpers."""

from __future__ import annotations

from nori.user_profiling.models import IntakeResult, UserInput
from nori.user_profiling.intaker import normalizer as intake_normalizer


def _fallback() -> IntakeResult:
    return IntakeResult(
        intention={
            "goal": "产品种草",
            "format": "小红书图文",
            "tone": ["高级"],
            "anti": ["不要硬广"],
        },
        context={
            "creative_assets": ["品牌色"],
            "commercial_assets": [],
            "guardrails": ["不要硬广"],
            "data_refs": [],
            "images": [],
        },
        missing=[],
        questions=[],
        metadata={"source": "fallback"},
    )


def test_rule_intake_extracts_intention_context_and_missing_questions():
    result = intake_normalizer.rule_intake(
        UserInput(
            text="帮我做小红书图文，新品种草，要高级，不要硬广，参考 logo 和品牌色",
            images=["assets/logo.png"],
        )
    )

    assert result.ready
    assert result.intention["goal"] == "产品种草"
    assert result.intention["format"] == "小红书图文"
    assert result.intention["tone"] == ["高级"]
    assert result.intention["anti"] == ["不要硬广"]
    assert {"品牌标志", "品牌色", "图片资产"} <= set(result.context["creative_assets"])
    assert result.context["images"] == [{"path": "assets/logo.png", "kind": "png", "usage": "context"}]

    missing = intake_normalizer.rule_intake(UserInput(text="", images=[]))
    assert missing.missing == ["topic", "goal"]
    assert len(missing.questions) == 2


def test_normalize_llm_result_accepts_aliases_and_preserves_fallback_metadata():
    normalized = UserInput(text="帮我做一篇小红书，别硬广，要带商品链接转化", images=["assets/product.jpg"])
    data = {
        "intention": {
            "goal": "sales_conversion",
            "format": "xhs_note",
            "tone": ["friendly", "unknown"],
            "anti": ["no_hard_sell"],
        },
        "context": {
            "creative_assets": ["logo"],
            "commercial_assets": ["product_link"],
            "guardrails": ["no_hard_sell", "bad"],
            "data_refs": ["viral_examples"],
        },
        "missing": ["bad"],
        "questions": [],
    }

    result = intake_normalizer.normalize_llm_result(data, normalized, _fallback())

    assert result.metadata == {"source": "fallback"}
    assert result.intention == {
        "goal": "销售转化",
        "format": "小红书图文",
        "tone": ["亲和"],
        "anti": ["不要硬广"],
    }
    assert result.context["creative_assets"] == ["品牌标志", "图片资产"]
    assert result.context["commercial_assets"] == ["商品链接"]
    assert result.context["guardrails"] == ["不要硬广"]
    assert result.context["data_refs"] == ["爆款案例"]
    assert result.context["images"] == [{"path": "assets/product.jpg", "kind": "jpg", "usage": "context"}]
    assert result.missing == []


def test_normalize_llm_result_keeps_required_missing_fields_and_question_fallback():
    normalized = UserInput(text="", images=[])
    result = intake_normalizer.normalize_llm_result(
        {
            "intention": {"goal": "未知", "format": "bad", "tone": ["bad"], "anti": ["bad"]},
            "context": {},
            "missing": [],
            "questions": [],
        },
        normalized,
        _fallback(),
    )

    assert result.intention["goal"] == "产品种草"
    assert result.intention["format"] == "小红书图文"
    assert result.intention["tone"] == ["高级"]
    assert result.missing == ["topic"]
    assert result.questions == ["这次要围绕什么主题、产品或活动来做？"]
