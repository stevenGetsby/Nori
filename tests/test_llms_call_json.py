from __future__ import annotations

from types import SimpleNamespace

import inspect

import pytest

import nori.core.llms.lm as lm_module
from nori.core.llms import ChatJSONError, set_telemetry_sink


class FakeStructuredRunnable:
    def __init__(self, response):
        self.response = response
        self.invoke_calls = []

    def invoke(self, messages):
        self.invoke_calls.append(messages)
        if isinstance(self.response, Exception):
            raise self.response
        return self.response


class FakeLangChainChatModel:
    def __init__(self, response=None, structured_output_error=None):
        self.response = response if response is not None else {"raw": None, "parsed": {"ok": True}, "parsing_error": None}
        self.structured_output_error = structured_output_error
        self.with_structured_output_calls = []
        self.invoke_calls = []
        self.structured = FakeStructuredRunnable(self.response)

    def with_structured_output(self, schema=None, **kwargs):
        self.with_structured_output_calls.append({"schema": schema, "kwargs": kwargs})
        if self.structured_output_error is not None:
            raise self.structured_output_error
        return self.structured

    def invoke(self, messages, **kwargs):
        self.invoke_calls.append({"messages": messages, "kwargs": kwargs})
        return SimpleNamespace(content='{"ok": true, "source": "plain"}')


class FakeDirectChatCompletions:
    def __init__(self):
        self.create_calls = []

    def create(self, **kwargs):
        self.create_calls.append(kwargs)
        return SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(content='{"ok": true, "source": "direct"}')
                )
            ]
        )


class FakeDirectOpenAIClient:
    def __init__(self):
        self.completions = FakeDirectChatCompletions()
        self.chat = SimpleNamespace(completions=self.completions)


def _model(*, max_output: int = 256, temperature_fixed: float | None = 0.2):
    return SimpleNamespace(
        key="openai::gpt-5-mini",
        provider_id="openai",
        model_id="gpt-5-mini",
        type="llm",
        max_output=max_output,
        temperature_fixed=temperature_fixed,
        extra_body={"trace": "model"},
        supports_vision=False,
    )


def _chat_model_bundle(model, chat_model):
    return SimpleNamespace(
        model=model,
        model_id=model.model_id,
        client=chat_model,
    )


@pytest.fixture(autouse=True)
def _clear_telemetry_sink():
    set_telemetry_sink(None)
    yield
    set_telemetry_sink(None)


def test_chat_json_uses_langchain_structured_output_and_returns_parsed_dict():
    model = _model()
    chat_model = FakeLangChainChatModel(
        {"raw": "raw-message", "parsed": {"ok": True, "count": 2}, "parsing_error": None}
    )
    client = lm_module.LanguageModelClient(
        chat_model_factory=lambda usage: _chat_model_bundle(model, chat_model),
    )

    data = client.chat_json(
        [{"role": "user", "content": "json only"}],
        usage="llm",
        timeout=12,
        response_format={"type": "json_object"},
        extra_body={"trace": "caller"},
    )

    assert data == {"ok": True, "count": 2}
    assert chat_model.with_structured_output_calls == [
        {
            "schema": None,
            "kwargs": {
                "method": "json_mode",
                "include_raw": True,
                "temperature": 0.2,
                "max_completion_tokens": 256,
                "timeout": 12,
                "extra_body": {"trace": "model"},
            },
        }
    ]
    assert chat_model.structured.invoke_calls == [[{"role": "user", "content": "json only"}]]


def test_chat_json_exposes_only_structured_output_parameters():
    signature = inspect.signature(lm_module.LanguageModelClient.chat_json)

    assert "_chat" not in signature.parameters
    assert "chat_func" not in signature.parameters
    assert "retry_without_response_format" not in signature.parameters


@pytest.mark.parametrize("legacy_kwarg", ["_chat", "chat_func", "retry_without_response_format"])
def test_chat_json_rejects_removed_legacy_kwargs(legacy_kwarg):
    client = lm_module.LanguageModelClient(
        chat_model_factory=lambda usage: _chat_model_bundle(_model(), FakeLangChainChatModel()),
    )

    with pytest.raises(TypeError, match=legacy_kwarg):
        client.chat_json(
            [{"role": "user", "content": "json only"}],
            **{legacy_kwarg: object()},
        )


def test_chat_json_accepts_explicit_schema_and_method():
    schema = {
        "name": "Answer",
        "description": "Answer payload",
        "parameters": {
            "type": "object",
            "properties": {"answer": {"type": "string"}},
            "required": ["answer"],
        },
    }
    chat_model = FakeLangChainChatModel(
        {"raw": "raw-message", "parsed": {"answer": "yes"}, "parsing_error": None}
    )
    client = lm_module.LanguageModelClient(
        chat_model_factory=lambda usage: _chat_model_bundle(_model(), chat_model),
    )

    data = client.chat_json(
        [{"role": "user", "content": "json only"}],
        schema=schema,
        structured_method="function_calling",
    )

    assert data == {"answer": "yes"}
    assert chat_model.with_structured_output_calls[0]["schema"] == schema
    assert chat_model.with_structured_output_calls[0]["kwargs"]["method"] == "function_calling"


def test_chat_json_wraps_langchain_parsing_error_as_chat_json_error():
    parsing_error = ValueError("bad structured output")
    chat_model = FakeLangChainChatModel(
        {"raw": SimpleNamespace(content="not json"), "parsed": None, "parsing_error": parsing_error}
    )
    client = lm_module.LanguageModelClient(
        chat_model_factory=lambda usage: _chat_model_bundle(_model(), chat_model),
    )

    with pytest.raises(ChatJSONError) as exc:
        client.chat_json([{"role": "user", "content": "json only"}])

    assert "无法解析为 JSON object" in str(exc.value)
    assert exc.value.raw == "not json"


def test_chat_json_rejects_non_object_structured_output():
    chat_model = FakeLangChainChatModel(
        {"raw": SimpleNamespace(content='["not", "object"]'), "parsed": ["not", "object"], "parsing_error": None}
    )
    client = lm_module.LanguageModelClient(
        chat_model_factory=lambda usage: _chat_model_bundle(_model(), chat_model),
    )

    with pytest.raises(ChatJSONError) as exc:
        client.chat_json([{"role": "user", "content": "json only"}])

    assert "不是 object" in str(exc.value)
    assert exc.value.raw == '["not", "object"]'


def test_chat_json_does_not_fall_back_to_plain_chat_when_structured_output_raises():
    chat_model = FakeLangChainChatModel(RuntimeError("structured down"))
    client = lm_module.LanguageModelClient(
        chat_model_factory=lambda usage: _chat_model_bundle(_model(), chat_model),
    )

    with pytest.raises(RuntimeError, match="structured down"):
        client.chat_json([{"role": "user", "content": "json only"}])

    assert chat_model.invoke_calls == []


def test_chat_json_falls_back_for_openai_raw_response_parse_adapter_error():
    chat_model = FakeLangChainChatModel(
        AttributeError("'CompletionsWithRawResponse' object has no attribute 'parse'")
    )
    direct_client = FakeDirectOpenAIClient()
    client = lm_module.LanguageModelClient(
        chat_model_factory=lambda usage: _chat_model_bundle(_model(), chat_model),
        chat_completion_client_factory=lambda model, usage: _chat_model_bundle(model, direct_client),
    )

    data = client.chat_json([{"role": "user", "content": "json only"}])

    assert data == {"ok": True, "source": "direct"}
    assert chat_model.invoke_calls == []
    assert direct_client.completions.create_calls == [
        {
            "messages": [{"role": "user", "content": "json only"}],
            "model": "gpt-5-mini",
            "temperature": 0.2,
            "max_completion_tokens": 256,
            "extra_body": {"trace": "model"},
            "response_format": {"type": "json_object"},
        }
    ]


def test_chat_json_falls_back_when_structured_output_creation_hits_openai_parse_adapter_error():
    chat_model = FakeLangChainChatModel(
        structured_output_error=AttributeError(
            "'CompletionsWithRawResponse' object has no attribute 'parse'"
        )
    )
    direct_client = FakeDirectOpenAIClient()
    client = lm_module.LanguageModelClient(
        chat_model_factory=lambda usage: _chat_model_bundle(_model(), chat_model),
        chat_completion_client_factory=lambda model, usage: _chat_model_bundle(model, direct_client),
    )

    data = client.chat_json([{"role": "user", "content": "json only"}])

    assert data == {"ok": True, "source": "direct"}
    assert len(chat_model.with_structured_output_calls) == 1
    assert chat_model.invoke_calls == []
    assert len(direct_client.completions.create_calls) == 1
