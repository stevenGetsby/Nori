"""Tests for shared structured LLM prompt builders."""

from __future__ import annotations

from llms import structured_prompts


def test_build_intent_system_prompt_includes_field_descriptions_and_enums():
    prompt = structured_prompts.build_intent_system_prompt(
        ["topic", "content_type"],
        {"content_type": ["图文", "视频"]},
        max_candidates=2,
    )

    assert "topic" in prompt
    assert "核心主题" in prompt
    assert "content_type" in prompt
    assert "[图文/视频]" in prompt
    assert "至多 2 个候选" in prompt


def test_build_intent_user_prompt_limits_schema_keys_to_requested_fields():
    prompt = structured_prompts.build_intent_user_prompt("写一篇春日花束图文", ["topic", "tone"])

    assert "写一篇春日花束图文" in prompt
    assert '{"topic", "tone"}' in prompt
    assert "content_type" not in prompt


def test_build_target_system_prompt_formats_and_truncates_option_catalog():
    long_summary = "第一行\n" + ("很长" * 50)
    prompt = structured_prompts.build_target_system_prompt(
        [
            {
                "selector": "cover#1",
                "role": "cover_image",
                "kind": "image",
                "summary": long_summary,
            }
        ],
        max_alternatives=1,
    )

    assert "selector=cover#1 | role=cover_image | kind=image | summary=第一行" in prompt
    assert "\n很长" not in prompt
    assert "alternatives 至多 1 个" in prompt
    assert "target_selector" in prompt


def test_build_target_user_prompt_preserves_history_order():
    prompt = structured_prompts.build_target_user_prompt(
        "封面画面亮一点",
        ["先改过标题", "用户现在说封面"],
    )

    assert "封面画面亮一点" in prompt
    assert "- 先改过标题" in prompt
    assert prompt.index("- 先改过标题") < prompt.index("- 用户现在说封面")
