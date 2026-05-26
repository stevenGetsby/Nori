import json

import llms.call as call_module
import llms.intent_extractor as intent_module
import llms.structured_calls as structured_calls
import llms.structured_outputs as structured_outputs
import llms.target_selector as target_module
from llms import ChatJSONError
from llms import extract_intent, select_edit_target


def test_structured_output_helpers_are_shared_by_intent_and_target_modules():
    assert intent_module._clean_str is structured_outputs.clean_str
    assert target_module._clean_str is structured_outputs.clean_str
    assert intent_module._chat_json_error_reason is structured_outputs.chat_json_error_reason
    assert target_module._chat_json_error_reason is structured_outputs.chat_json_error_reason
    assert intent_module._normalize_field_value is structured_outputs.normalize_field_value
    assert target_module._normalize_options is structured_outputs.normalize_selector_options


def test_structured_output_helpers_clean_values_and_classify_parse_errors():
    assert structured_outputs.clean_str("  '春日花束'  ") == "春日花束"
    assert structured_outputs.clean_str(123) == "123"
    assert structured_outputs.clean_str("未知") is None
    assert structured_outputs.clean_str(" null ") is None
    assert structured_outputs.clean_str("") is None
    assert structured_outputs.chat_json_error_reason(ChatJSONError("empty", "  ")) == "empty_response"
    assert structured_outputs.chat_json_error_reason(ChatJSONError("bad", "{bad")) == "parse_error"


def test_structured_call_helper_returns_data_raw_and_classified_errors():
    def ok_call(messages, *, usage="llm", timeout=6.0, json_mode=True):  # noqa: ARG001
        return {"topic": "通勤香薰"}, '{"topic": "通勤香薰"}'

    def parse_error_call(messages, *, usage="llm", timeout=6.0, json_mode=True):  # noqa: ARG001
        raise ChatJSONError("bad", "{bad")

    def api_error_call(messages, *, usage="llm", timeout=6.0, json_mode=True):  # noqa: ARG001
        raise RuntimeError("boom")

    ok = structured_calls.call_structured_json(
        [{"role": "user", "content": "x"}],
        chat_json_with_raw_func=ok_call,
    )
    parse_error = structured_calls.call_structured_json(
        [{"role": "user", "content": "x"}],
        chat_json_with_raw_func=parse_error_call,
    )
    api_error = structured_calls.call_structured_json(
        [{"role": "user", "content": "x"}],
        chat_json_with_raw_func=api_error_call,
    )

    assert ok.data == {"topic": "通勤香薰"}
    assert ok.raw == '{"topic": "通勤香薰"}'
    assert ok.error is None
    assert parse_error.raw == "{bad"
    assert parse_error.error == "parse_error"
    assert api_error.raw == ""
    assert api_error.error == "api_error:RuntimeError"


def test_structured_output_helpers_normalize_fields_and_selectors():
    value, candidates = structured_outputs.normalize_field_value(
        {"value": "视频", "candidates": ["图文", "视频", "直播"]},
        allowed=["图文", "直播"],
        max_candidates=2,
    )

    assert value is None
    assert candidates == ["图文", "直播"]

    options = structured_outputs.normalize_selector_options([
        {"selector": " cover#1 ", "role": "cover_image", "kind": "image", "summary": "  封面图  "},
        {"selector": "cover#1", "role": "duplicate"},
        {"selector": ""},
        "bad",
    ])

    assert options == [{
        "selector": "cover#1",
        "role": "cover_image",
        "kind": "image",
        "summary": "封面图",
    }]
    assert structured_outputs.normalize_confidence("certain") == "low"
    assert structured_outputs.normalize_selector_alternatives(
        ["copy#1", "cover#1", "missing", "copy#2"],
        selector_set={"cover#1", "copy#1", "copy#2"},
        target="cover#1",
        max_alternatives=1,
    ) == ["copy#1"]


def test_extract_intent_uses_json_mode_and_filters_enums(monkeypatch):
    calls: list[dict] = []

    def fake_chat(messages, *, usage="llm", **kwargs):  # noqa: ARG001
        calls.append({"usage": usage, "kwargs": kwargs})
        return json.dumps({
            "topic": {"value": "春日花束", "candidates": ["母亲节花束"]},
            "content_type": {"value": "视频", "candidates": ["图文"]},
            "tone": ["生活化", "专业克制"],
        })

    monkeypatch.setattr(call_module, "chat", fake_chat)

    result = extract_intent(
        "写一篇春日花束小红书图文，语气生活化",
        needed_fields=["topic", "content_type", "tone"],
        enum_constraints={"content_type": ["图文"]},
    )

    assert result.ok
    assert result.fields == {"topic": "春日花束", "tone": "生活化"}
    assert result.candidates["topic"] == ["母亲节花束"]
    assert result.candidates["content_type"] == ["图文"]
    assert calls[0]["kwargs"]["response_format"] == {"type": "json_object"}


def test_extract_intent_retries_when_json_mode_is_rejected(monkeypatch):
    calls: list[dict] = []

    def fake_chat(messages, *, usage="llm", **kwargs):  # noqa: ARG001
        calls.append(dict(kwargs))
        if len(calls) == 1:
            raise RuntimeError("response_format unsupported")
        return '{"topic": "通勤香薰"}'

    monkeypatch.setattr(call_module, "chat", fake_chat)

    result = extract_intent("通勤香薰选题", needed_fields=["topic"])

    assert result.fields == {"topic": "通勤香薰"}
    assert "response_format" in calls[0]
    assert "response_format" not in calls[1]


def test_select_edit_target_validates_selector_and_alternatives(monkeypatch):
    def fake_chat(messages, *, usage="llm", **kwargs):  # noqa: ARG001
        return json.dumps({
            "target_selector": "cover#1",
            "refined_instruction": "增加更明亮的花束主视觉",
            "alternatives": ["copy#1", "missing#1"],
            "confidence": "high",
            "reason": "用户提到画面",
        })

    monkeypatch.setattr(call_module, "chat", fake_chat)

    result = select_edit_target(
        "封面画面亮一点",
        [
            {"selector": "cover#1", "role": "cover_image", "summary": "封面图"},
            {"selector": "copy#1", "role": "copy_text", "summary": "正文"},
        ],
    )

    assert result.ok
    assert result.target_selector == "cover#1"
    assert result.refined_instruction == "增加更明亮的花束主视觉"
    assert result.alternatives == ["copy#1"]
    assert result.confidence == "high"


def test_select_edit_target_returns_error_for_invalid_selector(monkeypatch):
    monkeypatch.setattr(
        call_module,
        "chat",
        lambda *args, **kwargs: '{"target_selector": "not_allowed", "confidence": "high"}',
    )

    result = select_edit_target(
        "改封面",
        [
            {"selector": "cover#1", "role": "cover_image"},
            {"selector": "copy#1", "role": "copy_text"},
        ],
    )

    assert not result.ok
    assert result.error == "invalid_selector"
