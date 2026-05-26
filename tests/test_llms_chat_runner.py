from __future__ import annotations

import asyncio
from types import SimpleNamespace

import pytest

import llms.chat_runner as chat_runner
from llms import ChatCapabilityError, set_telemetry_sink


class FakeMessage:
    def __init__(self, content: str | None = " ok ") -> None:
        self.content = content


class FakeChoice:
    def __init__(self, content: str | None = " ok ") -> None:
        self.message = FakeMessage(content)


class FakeChatResponse:
    def __init__(self, content: str | None = " ok ") -> None:
        self.choices = [FakeChoice(content)]


class FakeCompletions:
    def __init__(self, content: str | None = " ok ") -> None:
        self.content = content
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return FakeChatResponse(self.content)


class AsyncFakeCompletions(FakeCompletions):
    async def create(self, **kwargs):
        return super().create(**kwargs)


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


def _bundle(model, completions):
    return SimpleNamespace(
        model=model,
        model_id=model.model_id,
        client=SimpleNamespace(chat=SimpleNamespace(completions=completions)),
    )


@pytest.fixture(autouse=True)
def _clear_telemetry_sink():
    set_telemetry_sink(None)
    yield
    set_telemetry_sink(None)


def test_chat_text_merges_params_calls_provider_and_emits_redacted_telemetry(monkeypatch):
    records = []
    model = _model()
    completions = FakeCompletions(" ok from runner ")
    monkeypatch.setattr(chat_runner, "get_client", lambda usage: _bundle(model, completions))
    set_telemetry_sink(records.append)

    result = chat_runner.chat_text(
        [{"role": "user", "content": "secret"}],
        usage="llm",
        extra_body={"trace": "caller"},
    )

    assert result == "ok from runner"
    assert completions.calls == [
        {
            "model": "gpt-5-mini",
            "messages": [{"role": "user", "content": "secret"}],
            "temperature": 0.2,
            "max_completion_tokens": 256,
            "extra_body": {"trace": "model"},
        }
    ]
    assert records[0]["operation"] == "chat"
    assert records[0]["success"] is True
    assert "messages" not in records[0]


def test_chat_text_checks_capability_before_provider_call_and_emits_error(monkeypatch):
    records = []
    model = _model(model_type="image")
    completions = FakeCompletions()
    monkeypatch.setattr(chat_runner, "get_client", lambda usage: _bundle(model, completions))
    set_telemetry_sink(records.append)

    with pytest.raises(ChatCapabilityError, match="expected type"):
        chat_runner.chat_text([{"role": "user", "content": "hello"}], usage="llm")

    assert completions.calls == []
    assert records[0]["operation"] == "chat"
    assert records[0]["success"] is False
    assert records[0]["error_type"] == "ChatCapabilityError"


def test_achat_text_uses_async_client_and_achat_telemetry(monkeypatch):
    records = []
    model = _model()
    completions = AsyncFakeCompletions(" async ok ")
    monkeypatch.setattr(chat_runner, "get_async_client", lambda usage: _bundle(model, completions))
    set_telemetry_sink(records.append)

    result = asyncio.run(chat_runner.achat_text([{"role": "user", "content": "hello"}], usage="llm"))

    assert result == "async ok"
    assert completions.calls[0]["model"] == "gpt-5-mini"
    assert records[0]["operation"] == "achat"
    assert records[0]["success"] is True
