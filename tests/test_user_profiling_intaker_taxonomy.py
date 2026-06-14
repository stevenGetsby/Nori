"""Tests for Intake taxonomy and label-cleanup helpers."""

from __future__ import annotations

from nori.agents.user_profiling.intaker import taxonomy as intake_taxonomy


def test_rule_taxonomy_picks_goal_format_assets_and_guardrails():
    text = "小红书新品种草，要高级，不要硬广，参考 logo、品牌色和爆款案例"

    assert intake_taxonomy.pick_first(text, intake_taxonomy.GOAL_RULES) == "产品种草"
    assert intake_taxonomy.pick_first(text, intake_taxonomy.FORMAT_RULES) == "小红书图文"
    assert intake_taxonomy.pick_many(text, intake_taxonomy.TONE_RULES) == ["高级"]
    assert intake_taxonomy.creative_assets(text, ["assets/logo.png"]) == ["品牌标志", "品牌色", "图片资产"]
    assert intake_taxonomy.guardrails(text) == ["不要硬广"]
    assert intake_taxonomy.data_refs(text) == ["爆款案例"]


def test_label_normalization_maps_aliases_filters_unknowns_and_falls_back():
    assert intake_taxonomy.allowed_label("sales_conversion", intake_taxonomy.GOAL_RULES, "产品种草") == "销售转化"
    assert intake_taxonomy.allowed_label("unknown", intake_taxonomy.GOAL_RULES, "产品种草") == "产品种草"
    assert intake_taxonomy.allowed_list(
        ["friendly", "bad", "no_hard_sell", "亲和"],
        intake_taxonomy.allowed_values(intake_taxonomy.TONE_RULES) | intake_taxonomy.allowed_values(intake_taxonomy.ANTI_RULES),
        ["高级"],
        intake_taxonomy.label_aliases(intake_taxonomy.TONE_RULES) | intake_taxonomy.label_aliases(intake_taxonomy.ANTI_RULES),
    ) == ["亲和", "不要硬广"]


def test_missing_and_question_helpers_keep_required_fields_and_limit_questions():
    missing = intake_taxonomy.normalize_missing(
        ["bad", "goal"],
        text="",
        intention={"goal": ""},
    )
    questions = intake_taxonomy.normalize_questions(["自定义问题 1", "自定义问题 2", "自定义问题 3"], missing)

    assert missing == ["goal", "topic"]
    assert questions == ["自定义问题 1", "自定义问题 2"]
    assert intake_taxonomy.questions_for_missing(["topic"]) == ["这次要围绕什么主题、产品或活动来做？"]
