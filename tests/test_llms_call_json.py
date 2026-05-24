from __future__ import annotations

import pytest

import llms.call as call_module
from llms import ChatJSONError, parse_json_object


def test_chat_json_routes_usage_and_kwargs(monkeypatch):
    captured: dict = {}

    def fake_chat(messages, *, usage="llm", **kwargs):
        captured["messages"] = messages
        captured["usage"] = usage
        captured["kwargs"] = kwargs
        return '{"ok": true, "count": 2}'

    monkeypatch.setattr(call_module, "chat", fake_chat)

    data = call_module.chat_json(
        [{"role": "user", "content": "json only"}],
        usage="vision",
        timeout=12,
    )

    assert data == {"ok": True, "count": 2}
    assert captured["usage"] == "vision"
    assert captured["kwargs"] == {"timeout": 12}
    assert "response_format" not in captured["kwargs"]


def test_chat_json_accepts_injected_chat_function():
    def fake_chat(messages, *, usage="llm", **kwargs):  # noqa: ARG001
        return '{"source": "injected"}'

    data = call_module.chat_json(
        [{"role": "user", "content": "json only"}],
        _chat=fake_chat,
    )

    assert data == {"source": "injected"}


def test_parse_json_object_accepts_fenced_and_embedded_json():
    assert parse_json_object('```json\n{"a": 1}\n```') == {"a": 1}
    assert parse_json_object('Here is the JSON:\n{"b": {"nested": true}}\nDone.') == {
        "b": {"nested": True}
    }


def test_parse_json_object_rejects_invalid_or_non_object_json():
    with pytest.raises(ChatJSONError, match="无法解析"):
        parse_json_object("not json")

    with pytest.raises(ChatJSONError, match="不是 object"):
        parse_json_object('["not", "an", "object"]')
