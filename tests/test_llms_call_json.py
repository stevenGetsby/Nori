from __future__ import annotations

from types import SimpleNamespace

import pytest

import llms
import llms.call as call_module
import llms.json_calls as json_calls
import llms.json_parser as json_parser
import llms.request_params as request_params
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


def test_merge_kwargs_does_not_mutate_caller_extra_body():
    model = SimpleNamespace(
        provider_id="openai",
        model_id="gpt-5-mini",
        max_output=0,
        temperature_fixed=None,
        extra_body={"reasoning": {"effort": "low"}, "trace": "model"},
    )
    caller_extra_body = {"trace": "caller", "metadata": {"request_id": "local"}}

    merged = request_params.merge_chat_kwargs(model, {"extra_body": caller_extra_body})

    assert caller_extra_body == {"trace": "caller", "metadata": {"request_id": "local"}}
    assert merged["extra_body"] == {
        "trace": "model",
        "metadata": {"request_id": "local"},
        "reasoning": {"effort": "low"},
    }
    assert merged["extra_body"] is not caller_extra_body


def test_merge_kwargs_prefers_max_completion_tokens_for_gpt5():
    model = SimpleNamespace(
        provider_id="openai",
        model_id="gpt-5-mini",
        max_output=4096,
        temperature_fixed=None,
        extra_body={},
    )

    converted = request_params.merge_chat_kwargs(model, {"max_tokens": 123})
    explicit = request_params.merge_chat_kwargs(
        model,
        {"max_tokens": 123, "max_completion_tokens": 456},
    )
    defaulted = request_params.merge_chat_kwargs(model, {})

    assert converted == {"max_completion_tokens": 123}
    assert explicit == {"max_completion_tokens": 456}
    assert defaulted == {"max_completion_tokens": 4096}


def test_merge_kwargs_prefers_max_completion_tokens_for_openai_compatible_gpt5_providers():
    model = SimpleNamespace(
        provider_id="lumina",
        model_id="gpt-5.5",
        max_output=128,
        temperature_fixed=None,
        extra_body={},
    )

    assert request_params.merge_chat_kwargs(model, {"max_tokens": 32}) == {"max_completion_tokens": 32}
    assert request_params.merge_chat_kwargs(model, {}) == {"max_completion_tokens": 128}


def test_merge_kwargs_prefers_max_tokens_for_non_gpt5():
    model = SimpleNamespace(
        provider_id="openai",
        model_id="gpt-4.1-mini",
        max_output=2048,
        temperature_fixed=None,
        extra_body={},
    )

    converted = request_params.merge_chat_kwargs(model, {"max_completion_tokens": 123})
    explicit = request_params.merge_chat_kwargs(
        model,
        {"max_tokens": 456, "max_completion_tokens": 123},
    )
    defaulted = request_params.merge_chat_kwargs(model, {})

    assert converted == {"max_tokens": 123}
    assert explicit == {"max_tokens": 456}
    assert defaulted == {"max_tokens": 2048}


def test_merge_kwargs_normalizes_token_kwargs_without_model_default():
    gpt5 = SimpleNamespace(
        provider_id="openai",
        model_id="gpt-5-mini",
        max_output=0,
        temperature_fixed=None,
        extra_body={},
    )
    non_gpt5 = SimpleNamespace(
        provider_id="openai",
        model_id="gpt-4.1-mini",
        max_output=0,
        temperature_fixed=None,
        extra_body={},
    )

    assert request_params.merge_chat_kwargs(
        gpt5,
        {"max_tokens": 123, "max_completion_tokens": 456},
    ) == {"max_completion_tokens": 456}
    assert request_params.merge_chat_kwargs(
        non_gpt5,
        {"max_tokens": 456, "max_completion_tokens": 123},
    ) == {"max_tokens": 456}
    assert request_params.merge_chat_kwargs(gpt5, {}) == {}
    assert request_params.merge_chat_kwargs(non_gpt5, {}) == {}


def test_chat_json_accepts_injected_chat_function():
    def fake_chat(messages, *, usage="llm", **kwargs):  # noqa: ARG001
        return '{"source": "injected"}'

    data = call_module.chat_json(
        [{"role": "user", "content": "json only"}],
        _chat=fake_chat,
    )

    assert data == {"source": "injected"}


def test_parse_json_object_identity_is_stable_across_import_paths():
    assert llms.parse_json_object is json_parser.parse_json_object
    assert call_module.parse_json_object is json_parser.parse_json_object


def test_chat_json_with_raw_returns_parsed_data_and_raw_text():
    def fake_chat(messages, *, usage="llm", **kwargs):  # noqa: ARG001
        return '```json\n{"source": "raw-helper"}\n```'

    data, raw = call_module.chat_json_with_raw(
        [{"role": "user", "content": "json only"}],
        _chat=fake_chat,
    )

    assert data == {"source": "raw-helper"}
    assert raw == '```json\n{"source": "raw-helper"}\n```'


def test_json_call_raw_retries_without_mutating_params():
    calls: list[dict] = []
    params = {"timeout": 6, "extra_body": {"trace": "caller"}}

    def fake_chat(messages, *, usage="llm", **kwargs):  # noqa: ARG001
        calls.append({"usage": usage, "kwargs": kwargs})
        if len(calls) == 1:
            raise RuntimeError("provider says response_format json_object unsupported")
        return '{"ok": true}'

    raw = json_calls.chat_json_raw(
        [{"role": "user", "content": "json only"}],
        usage="vision",
        json_mode=True,
        retry_without_response_format=True,
        chat_func=fake_chat,
        params=params,
    )

    assert raw == '{"ok": true}'
    assert params == {"timeout": 6, "extra_body": {"trace": "caller"}}
    assert calls[0]["usage"] == "vision"
    assert calls[0]["kwargs"]["response_format"] == {"type": "json_object"}
    assert calls[0]["kwargs"]["timeout"] == 6
    assert "response_format" not in calls[1]["kwargs"]
    assert calls[1]["kwargs"]["extra_body"] == {"trace": "caller"}


def test_chat_json_json_mode_retries_without_response_format():
    calls: list[dict] = []

    def fake_chat(messages, *, usage="llm", **kwargs):  # noqa: ARG001
        calls.append({"usage": usage, "kwargs": kwargs})
        if len(calls) == 1:
            raise RuntimeError("provider says response_format json_object unsupported")
        return '{"ok": true}'

    data = call_module.chat_json(
        [{"role": "user", "content": "json only"}],
        usage="llm",
        json_mode=True,
        timeout=6,
        _chat=fake_chat,
    )

    assert data == {"ok": True}
    assert calls[0]["kwargs"]["response_format"] == {"type": "json_object"}
    assert "response_format" not in calls[1]["kwargs"]
    assert calls[1]["kwargs"]["timeout"] == 6


def test_chat_json_json_mode_retries_type_error_from_response_format_kwarg():
    calls: list[dict] = []

    def fake_chat(messages, *, usage="llm", **kwargs):  # noqa: ARG001
        calls.append(dict(kwargs))
        if len(calls) == 1:
            raise TypeError(
                "Completions.create() got an unexpected keyword argument 'response_format'"
            )
        return '{"ok": true}'

    data = call_module.chat_json(
        [{"role": "user", "content": "json only"}],
        json_mode=True,
        _chat=fake_chat,
    )

    assert data == {"ok": True}
    assert "response_format" in calls[0]
    assert "response_format" not in calls[1]


def test_chat_json_json_mode_does_not_retry_unrelated_type_error():
    calls = 0

    def fake_chat(messages, *, usage="llm", **kwargs):  # noqa: ARG001
        nonlocal calls
        calls += 1
        raise TypeError("object of type int has no len()")

    with pytest.raises(TypeError, match="object of type int"):
        call_module.chat_json(
            [{"role": "user", "content": "json only"}],
            json_mode=True,
            _chat=fake_chat,
        )

    assert calls == 1


def test_chat_json_with_raw_preserves_raw_from_retry_success():
    calls: list[dict] = []

    def fake_chat(messages, *, usage="llm", **kwargs):  # noqa: ARG001
        calls.append(dict(kwargs))
        if len(calls) == 1:
            raise RuntimeError("provider says response_format unsupported")
        return '{"retry": true}'

    data, raw = call_module.chat_json_with_raw(
        [{"role": "user", "content": "json only"}],
        json_mode=True,
        _chat=fake_chat,
    )

    assert data == {"retry": True}
    assert raw == '{"retry": true}'
    assert "response_format" in calls[0]
    assert "response_format" not in calls[1]


def test_chat_json_json_mode_can_disable_retry():
    def fake_chat(messages, *, usage="llm", **kwargs):  # noqa: ARG001
        raise RuntimeError("response_format unsupported")

    with pytest.raises(RuntimeError, match="response_format"):
        call_module.chat_json(
            [{"role": "user", "content": "json only"}],
            json_mode=True,
            retry_without_response_format=False,
            _chat=fake_chat,
        )


def test_chat_json_json_mode_does_not_retry_unrelated_unsupported_errors():
    calls = 0

    def fake_chat(messages, *, usage="llm", **kwargs):  # noqa: ARG001
        nonlocal calls
        calls += 1
        raise RuntimeError("model family unsupported for this account")

    with pytest.raises(RuntimeError, match="model family unsupported"):
        call_module.chat_json(
            [{"role": "user", "content": "json only"}],
            json_mode=True,
            _chat=fake_chat,
        )

    assert calls == 1


def test_parse_json_object_accepts_fenced_and_embedded_json():
    assert parse_json_object('```json\n{"a": 1}\n```') == {"a": 1}
    assert parse_json_object('Here is the JSON:\n{"b": {"nested": true}}\nDone.') == {
        "b": {"nested": True}
    }


def test_parse_json_object_uses_first_valid_embedded_object():
    assert parse_json_object('Draft {placeholder}\n{"ok": true}\nDone.') == {"ok": True}
    assert parse_json_object('First: {"a": 1}\nSecond: {"b": 2}') == {"a": 1}


def test_parse_json_object_rejects_invalid_or_non_object_json():
    with pytest.raises(ChatJSONError, match="无法解析"):
        parse_json_object("not json")

    with pytest.raises(ChatJSONError, match="不是 object"):
        parse_json_object('["not", "an", "object"]')


def test_chat_json_with_raw_attaches_raw_to_parse_error():
    def fake_chat(messages, *, usage="llm", **kwargs):  # noqa: ARG001
        return "not json"

    with pytest.raises(ChatJSONError) as exc:
        call_module.chat_json_with_raw(
            [{"role": "user", "content": "json only"}],
            _chat=fake_chat,
        )

    assert exc.value.raw == "not json"
