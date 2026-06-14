"""Tests for AccountPlanner prompt construction helpers."""

from __future__ import annotations

from nori.agents.user_profiling.schemas import AccountPlannerInput
from nori.agents.user_profiling.account_planner.package import AccountPlannerPromptBuilder


account_plan_prompts = AccountPlannerPromptBuilder()


def test_account_plan_user_prompt_serializes_input_evidence_and_search_results():
    normalized = AccountPlannerInput(
        text="  花店账号需要做母亲节内容  ",
        images=["/tmp/cover.JPG"],
        links=["https://example.com/brand"],
        intention={"goal": "获客"},
        context={"audience": ["本地家庭"]},
    )

    prompt = account_plan_prompts.build_user_prompt(
        normalized,
        [{"title": "母亲节花束爆款", "author": "花艺博主"}],
    )

    assert "原始文字证据" in prompt
    assert "花店账号需要做母亲节内容" in prompt
    assert '{"path": "/tmp/cover.JPG", "kind": "jpg"}' in prompt
    assert '"https://example.com/brand"' in prompt
    assert '"goal": "获客"' in prompt
    assert '"audience": ["本地家庭"]' in prompt
    assert '"title": "母亲节花束爆款"' in prompt
    assert "{text}" not in prompt
    assert "{search_results}" not in prompt


def test_account_plan_user_prompt_uses_empty_text_fallback():
    normalized = AccountPlannerInput(text="  ", images=[], links=[])

    prompt = account_plan_prompts.build_user_prompt(normalized, [])

    assert "原始文字证据：\n无" in prompt
    assert "原始图片证据：\n[]" in prompt
    assert "搜索结果：\n[]" in prompt


def test_account_plan_prompt_constants_keep_json_only_contract():
    assert "只输出 JSON" in account_plan_prompts.system_prompt
    assert "输出 JSON，字段固定" in account_plan_prompts.user_prompt_template
