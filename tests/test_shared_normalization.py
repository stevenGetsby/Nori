"""Tests for shared runtime normalization helpers."""
from __future__ import annotations

from nori.shared.normalization import (
    bounded_int,
    dedupe_preserve_order,
    int_value,
    mapping,
    milestone_rows,
    string_list,
)


def test_mapping_accepts_dict_only_and_returns_copy():
    source = {"a": 1}

    result = mapping(source)

    assert result == {"a": 1}
    assert result is not source
    assert mapping([("a", 1)]) == {}
    assert mapping(None) == {}


def test_string_list_normalizes_scalar_lists_fallback_and_limits():
    assert string_list(" 花束 ") == ["花束"]
    assert string_list([" a ", None, "", 3]) == ["a", "3"]
    assert string_list(None, ["fallback"], limit=1) == ["fallback"]
    assert string_list(["", "  "], ["fallback"]) == ["fallback"]
    assert string_list(["a", "b", "c"], limit=2) == ["a", "b"]


def test_dedupe_preserve_order_skips_repeated_items():
    assert dedupe_preserve_order(["a", "b", "a", "", "b", "c"]) == ["a", "b", "", "c"]


def test_int_helpers_reject_bool_and_apply_bounds():
    assert int_value("3", default=1) == 3
    assert int_value(True, default=1) == 1
    assert int_value("bad", default=7) == 7
    assert bounded_int("10", default=1, minimum=1, maximum=5) == 5
    assert bounded_int("-1", default=1, minimum=1, maximum=5) == 1


def test_milestone_rows_normalizes_days_targets_and_falls_back():
    fallback = [{"day": 1, "target": "fallback"}]

    assert milestone_rows(
        [
            {"day": 0, "target": " start "},
            {"day": 99, "name": "end"},
            {"day": 2, "target": ""},
            "bad",
        ],
        fallback,
        horizon_days=7,
    ) == [{"day": 1, "target": "start"}, {"day": 7, "target": "end"}]
    assert milestone_rows([], fallback, horizon_days=7) == fallback
