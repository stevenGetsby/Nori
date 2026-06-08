from __future__ import annotations

import asyncio
from types import SimpleNamespace

import pytest

import nori.core.llms.lm as lm_module
from nori.core.llms import ChatCapabilityError, set_telemetry_sink


class FakeMessage:
    def __init__(self, content: str | None = " ok ") -> None:
        self.content = content


class FakeLangChainChatModel:
    def __init__(self, content: str = " ok from langchain ") -> None:
        self.content = content
        self.invoke_calls = []
        self.ainvoke_calls = []

    def invoke(self, messages, **kwargs):
        self.invoke_calls.append({"messages": messages, "kwargs": kwargs})
        return FakeMessage(self.content)

    async def ainvoke(self, messages, **kwargs):
        self.ainvoke_calls.append({"messages": messages, "kwargs": kwargs})
        return FakeMessage(self.content)


def _model(*, model_type: str = "llm", supports_vision: bool = False):
    return SimpleNamespace(
        key="openai::gpt-5-mini",
        provider_id="openai",
        model_id="gpt-5-mini",
        type=model_type,
        max_output=256,
        temperature_fixed=0.2,
        extra_body={"trace": "model"},
        supports_vision=supports_vision,
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


def test_chat_text_merges_params_calls_langchain_and_emits_redacted_telemetry():
    records = []
    model = _model()
    chat_model = FakeLangChainChatModel(" ok from runner ")
    client = lm_module.LanguageModelClient(
        chat_model_factory=lambda usage: _chat_model_bundle(model, chat_model),
    )
    set_telemetry_sink(records.append)

    result = client.chat(
        [{"role": "user", "content": "secret"}],
        usage="llm",
        extra_body={"trace": "caller"},
    )

    assert result == "ok from runner"
    assert chat_model.invoke_calls == [
        {
            "messages": [{"role": "user", "content": "secret"}],
            "kwargs": {
                "temperature": 0.2,
                "max_completion_tokens": 256,
                "extra_body": {"trace": "model"},
            },
        }
    ]
    assert records[0]["operation"] == "chat"
    assert records[0]["success"] is True
    assert "messages" not in records[0]


def test_chat_text_uses_langchain_invoke():
    model = _model()
    chat_model = FakeLangChainChatModel()
    client = lm_module.LanguageModelClient(
        chat_model_factory=lambda usage: _chat_model_bundle(model, chat_model),
    )

    result = client.chat([{"role": "user", "content": "secret"}], usage="llm")

    assert result == "ok from langchain"
    assert chat_model.invoke_calls[0]["messages"] == [{"role": "user", "content": "secret"}]
    assert chat_model.invoke_calls[0]["kwargs"] == {
        "temperature": 0.2,
        "max_completion_tokens": 256,
        "extra_body": {"trace": "model"},
    }


def test_chat_text_checks_capability_before_provider_call_and_emits_error():
    records = []
    model = _model(model_type="image")
    chat_model = FakeLangChainChatModel()
    client = lm_module.LanguageModelClient(
        chat_model_factory=lambda usage: _chat_model_bundle(model, chat_model),
    )
    set_telemetry_sink(records.append)

    with pytest.raises(ChatCapabilityError, match="expected type"):
        client.chat([{"role": "user", "content": "hello"}], usage="llm")

    assert chat_model.invoke_calls == []
    assert records[0]["operation"] == "chat"
    assert records[0]["success"] is False
    assert records[0]["error_type"] == "ChatCapabilityError"


def test_achat_text_uses_langchain_ainvoke_and_achat_telemetry():
    records = []
    model = _model()
    chat_model = FakeLangChainChatModel(" async ok ")
    client = lm_module.LanguageModelClient(
        async_chat_model_factory=lambda usage: _chat_model_bundle(model, chat_model),
    )
    set_telemetry_sink(records.append)

    result = asyncio.run(client.achat([{"role": "user", "content": "hello"}], usage="llm"))

    assert result == "async ok"
    assert chat_model.ainvoke_calls[0]["messages"] == [{"role": "user", "content": "hello"}]
    assert records[0]["operation"] == "achat"
    assert records[0]["success"] is True
