"""Tests for AccountPlanner input normalization helpers."""

from __future__ import annotations

from nori.user_profiling.models import AccountPlannerInput
from nori.user_profiling.account_planner import inputs as account_plan_inputs


def test_normalize_input_merges_existing_input_with_extra_images_and_links():
    source = AccountPlannerInput(
        text="原始内容",
        images=["a.png"],
        links=["https://old.example"],
        intention={"goal": "涨粉"},
        context={"tone": "轻松"},
        platform="",
        enable_search=True,
        search_limit=8,
    )

    normalized = account_plan_inputs.normalize_input(
        source,
        images=["b.webp"],
        links=["https://new.example"],
    )

    assert normalized.text == "原始内容"
    assert normalized.images == ["a.png", "b.webp"]
    assert normalized.links == ["https://old.example", "https://new.example"]
    assert normalized.intention == {"goal": "涨粉"}
    assert normalized.context == {"tone": "轻松"}
    assert normalized.platform == "xhs"
    assert normalized.enable_search is True
    assert normalized.search_limit == 8
    assert normalized is not source


def test_normalize_input_restores_plain_text_with_media_defaults():
    normalized = account_plan_inputs.normalize_input(
        "帮我做账号定位",
        images=["cover.jpg"],
        links=None,
    )

    assert normalized.text == "帮我做账号定位"
    assert normalized.images == ["cover.jpg"]
    assert normalized.links == []
    assert normalized.platform == "xhs"


def test_asset_context_uses_suffix_or_image_default():
    assert account_plan_inputs.asset_context("素材/cover.JPG") == {"path": "素材/cover.JPG", "kind": "jpg"}
    assert account_plan_inputs.asset_context("素材/no_suffix") == {"path": "素材/no_suffix", "kind": "image"}
