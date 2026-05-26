"""Tests for shared prompt serialization helpers."""
from __future__ import annotations

from nori.shared.prompting import json_block, json_inline, json_prompt, render_prompt


def test_json_inline_preserves_chinese_without_extra_spaces():
    assert json_inline({"brand": "春日花房", "n": 1}) == '{"brand":"春日花房","n":1}'


def test_json_block_pretty_prints_chinese_payloads():
    assert json_block({"brand": "春日花房"}) == '{\n  "brand": "春日花房"\n}'


def test_json_prompt_keeps_default_readable_spacing():
    assert json_prompt({"brand": "春日花房", "n": 1}) == '{"brand": "春日花房", "n": 1}'


def test_render_prompt_serializes_mapping_values():
    prompt = render_prompt(
        "用户：{intent}\n素材：{assets}",
        intent={"goal": "获客"},
        assets=[{"path": "/tmp/a.png"}],
    )

    assert '用户：{"goal":"获客"}' in prompt
    assert '素材：[{"path":"/tmp/a.png"}]' in prompt
