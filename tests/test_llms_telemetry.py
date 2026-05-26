from __future__ import annotations

import asyncio
from types import SimpleNamespace

import pytest

import llms
import llms.capabilities as capabilities
import llms.call as call_module
import llms.results as results_module
import llms.telemetry as telemetry_module
from llms import ChatCapabilityError, ChatResultError, ImageCapabilityError, set_telemetry_sink


class FakeMessage:
    def __init__(self, content: str | None = " ok ") -> None:
        self.content = content


class FakeChoice:
    def __init__(self, content: str | None = " ok ") -> None:
        self.message = FakeMessage(content)


class FakeChatResponse:
    def __init__(self, content: str | None = " ok ", choices=None) -> None:
        self.choices = [FakeChoice(content)] if choices is None else choices


class FakeCompletions:
    def __init__(
        self,
        error: Exception | None = None,
        content: str | None = " ok ",
        response=None,
    ) -> None:
        self.error = error
        self.content = content
        self.response = response
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        if self.error:
            raise self.error
        if self.response is not None:
            return self.response
        return FakeChatResponse(self.content)


class AsyncFakeCompletions(FakeCompletions):
    async def create(self, **kwargs):
        return super().create(**kwargs)


class FakeImageItem:
    url = "https://example.test/image.png"
    b64_json = ""


class FakeImageResponse:
    data = [FakeImageItem()]


class FakeImages:
    def __init__(self) -> None:
        self.generate_calls = []

    def generate(self, **kwargs):
        self.generate_calls.append(kwargs)
        return FakeImageResponse()


def _model(
    *,
    model_type: str = "llm",
    supports_vision: bool = False,
    supports_reference_image: bool = False,
):
    return SimpleNamespace(
        key="openai::gpt-5-mini",
        provider_id="openai",
        model_id="gpt-5-mini",
        type=model_type,
        max_output=4096,
        temperature_fixed=None,
        extra_body={},
        resolution_options=[],
        supports_vision=supports_vision,
        supports_reference_image=supports_reference_image,
    )


def _chat_bundle(
    error: Exception | None = None,
    *,
    model=None,
    completions: FakeCompletions | None = None,
    content: str | None = " ok ",
):
    model = model or _model(model_type="llm")
    completions = completions or FakeCompletions(error, content=content)
    return SimpleNamespace(
        model=model,
        model_id=model.model_id,
        client=SimpleNamespace(chat=SimpleNamespace(completions=completions)),
    )


def _async_chat_bundle(
    *,
    model=None,
    completions: AsyncFakeCompletions | None = None,
):
    model = model or _model(model_type="llm")
    completions = completions or AsyncFakeCompletions()
    return SimpleNamespace(
        model=model,
        model_id=model.model_id,
        client=SimpleNamespace(chat=SimpleNamespace(completions=completions)),
    )


def _image_bundle(model, images: FakeImages):
    return SimpleNamespace(
        model=model,
        model_id=model.model_id,
        client=SimpleNamespace(images=images),
    )


@pytest.fixture(autouse=True)
def _clear_telemetry_sink():
    set_telemetry_sink(None)
    yield
    set_telemetry_sink(None)


def test_telemetry_setter_identity_is_stable():
    assert llms.set_telemetry_sink is telemetry_module.set_telemetry_sink
    assert call_module.set_telemetry_sink is telemetry_module.set_telemetry_sink


def test_extract_chat_text_accepts_dict_shaped_provider_response():
    response = {
        "choices": [
            {
                "message": {
                    "content": "  ok from dict  ",
                }
            }
        ]
    }

    assert results_module.extract_chat_text(response, _model()) == "ok from dict"


def test_messages_need_vision_detects_multimodal_parts():
    assert capabilities.messages_need_vision([{"role": "user", "content": "text only"}]) is False
    assert (
        capabilities.messages_need_vision(
            [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "describe"},
                        {"image_url": {"url": "data:image/png;base64,ZmFrZQ=="}},
                    ],
                }
            ]
        )
        is True
    )


def test_emit_telemetry_redacts_payload_and_survives_sink_error():
    records = []
    set_telemetry_sink(records.append)

    telemetry_module.emit_telemetry(
        "chat",
        "llm",
        _model(),
        0,
        error=RuntimeError("provider down"),
    )

    assert records[0]["operation"] == "chat"
    assert records[0]["usage"] == "llm"
    assert records[0]["model_key"] == "openai::gpt-5-mini"
    assert records[0]["success"] is False
    assert records[0]["error_type"] == "RuntimeError"
    assert "prompt" not in records[0]
    assert "messages" not in records[0]
    assert "api_key" not in records[0]

    def broken_sink(record):
        raise AssertionError("sink down")

    set_telemetry_sink(broken_sink)
    telemetry_module.emit_telemetry("chat", "llm", _model(), 0)


def test_chat_emits_redacted_telemetry_on_success(monkeypatch):
    records = []
    monkeypatch.setattr(call_module, "get_client", lambda usage: _chat_bundle())
    set_telemetry_sink(records.append)

    result = call_module.chat([{"role": "user", "content": "secret prompt"}], usage="llm")

    assert result == "ok"
    assert records[0]["operation"] == "chat"
    assert records[0]["usage"] == "llm"
    assert records[0]["model_key"] == "openai::gpt-5-mini"
    assert records[0]["success"] is True
    assert "error_type" not in records[0]
    assert "prompt" not in records[0]
    assert "messages" not in records[0]


def test_chat_emits_telemetry_on_error_and_preserves_exception(monkeypatch):
    records = []
    monkeypatch.setattr(call_module, "get_client", lambda usage: _chat_bundle(RuntimeError("provider down")))
    set_telemetry_sink(records.append)

    with pytest.raises(RuntimeError, match="provider down"):
        call_module.chat([{"role": "user", "content": "hello"}], usage="llm")

    assert records[0]["operation"] == "chat"
    assert records[0]["success"] is False
    assert records[0]["error_type"] == "RuntimeError"


def test_chat_empty_provider_content_raises_result_error(monkeypatch):
    records = []
    monkeypatch.setattr(call_module, "get_client", lambda usage: _chat_bundle(content="   "))
    set_telemetry_sink(records.append)

    with pytest.raises(ChatResultError, match="未返回可用文本"):
        call_module.chat([{"role": "user", "content": "hello"}], usage="llm")

    assert records[0]["operation"] == "chat"
    assert records[0]["success"] is False
    assert records[0]["error_type"] == "ChatResultError"


def test_chat_empty_provider_choices_raise_result_error(monkeypatch):
    records = []
    empty_response = FakeChatResponse(choices=[])
    completions = FakeCompletions(response=empty_response)
    monkeypatch.setattr(call_module, "get_client", lambda usage: _chat_bundle(completions=completions))
    set_telemetry_sink(records.append)

    with pytest.raises(ChatResultError, match="未返回可用文本"):
        call_module.chat([{"role": "user", "content": "hello"}], usage="llm")

    assert records[0]["operation"] == "chat"
    assert records[0]["success"] is False
    assert records[0]["error_type"] == "ChatResultError"


def test_achat_missing_provider_content_raises_result_error(monkeypatch):
    records = []
    response = FakeChatResponse(choices=[SimpleNamespace(message=SimpleNamespace())])
    completions = AsyncFakeCompletions(response=response)
    monkeypatch.setattr(
        call_module,
        "get_async_client",
        lambda usage: _async_chat_bundle(completions=completions),
    )
    set_telemetry_sink(records.append)

    with pytest.raises(ChatResultError, match="未返回可用文本"):
        asyncio.run(call_module.achat([{"role": "user", "content": "hello"}], usage="llm"))

    assert records[0]["operation"] == "achat"
    assert records[0]["success"] is False
    assert records[0]["error_type"] == "ChatResultError"


def test_telemetry_sink_failure_does_not_break_call(monkeypatch):
    monkeypatch.setattr(call_module, "get_client", lambda usage: _chat_bundle())

    def broken_sink(record):
        raise AssertionError("sink down")

    set_telemetry_sink(broken_sink)

    assert call_module.chat([{"role": "user", "content": "hello"}], usage="llm") == "ok"


def test_image_emits_telemetry_on_success(monkeypatch):
    records = []
    model = _model(model_type="image")
    images = FakeImages()
    monkeypatch.setattr(call_module, "get_active", lambda usage: model)
    monkeypatch.setattr(
        call_module,
        "build_client_bundle",
        lambda model_arg, usage: _image_bundle(model_arg, images),
    )
    set_telemetry_sink(records.append)

    result = call_module.image("secret prompt", usage="image")

    assert result == ["https://example.test/image.png"]
    assert records[0]["operation"] == "image"
    assert records[0]["usage"] == "image"
    assert records[0]["success"] is True
    assert "prompt" not in records[0]


def test_image_emits_telemetry_on_capability_error(monkeypatch):
    records = []
    model = _model(model_type="image")
    monkeypatch.setattr(call_module, "get_active", lambda usage: model)
    set_telemetry_sink(records.append)

    with pytest.raises(ImageCapabilityError):
        call_module.image("edit", usage="image", reference_images=[b"\x89PNG\r\n\x1a\nfake"])

    assert records[0]["operation"] == "image"
    assert records[0]["success"] is False
    assert records[0]["error_type"] == "ImageCapabilityError"


def test_chat_rejects_non_chat_model_before_provider(monkeypatch):
    records = []
    completions = FakeCompletions()
    model = _model(model_type="image")
    monkeypatch.setattr(
        call_module,
        "get_client",
        lambda usage: _chat_bundle(model=model, completions=completions),
    )
    set_telemetry_sink(records.append)

    with pytest.raises(ChatCapabilityError, match="expected type"):
        call_module.chat([{"role": "user", "content": "hello"}], usage="llm")

    assert completions.calls == []
    assert records[0]["operation"] == "chat"
    assert records[0]["success"] is False
    assert records[0]["error_type"] == "ChatCapabilityError"


def test_chat_vision_usage_requires_vision_capability(monkeypatch):
    completions = FakeCompletions()
    model = _model(model_type="llm", supports_vision=False)
    monkeypatch.setattr(
        call_module,
        "get_client",
        lambda usage: _chat_bundle(model=model, completions=completions),
    )

    with pytest.raises(ChatCapabilityError, match="support vision"):
        call_module.chat([{"role": "user", "content": "describe this"}], usage="vision")

    assert completions.calls == []


def test_chat_multimodal_message_requires_vision_capability(monkeypatch):
    completions = FakeCompletions()
    model = _model(model_type="llm", supports_vision=False)
    monkeypatch.setattr(
        call_module,
        "get_client",
        lambda usage: _chat_bundle(model=model, completions=completions),
    )
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "describe"},
                {"type": "image_url", "image_url": {"url": "data:image/png;base64,ZmFrZQ=="}},
            ],
        }
    ]

    with pytest.raises(ChatCapabilityError, match="support vision"):
        call_module.chat(messages, usage="llm")

    assert completions.calls == []


def test_chat_multimodal_message_allows_vision_model(monkeypatch):
    completions = FakeCompletions()
    model = _model(model_type="vision", supports_vision=True)
    monkeypatch.setattr(
        call_module,
        "get_client",
        lambda usage: _chat_bundle(model=model, completions=completions),
    )
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "describe"},
                {"type": "image_url", "image_url": {"url": "data:image/png;base64,ZmFrZQ=="}},
            ],
        }
    ]

    assert call_module.chat(messages, usage="llm") == "ok"
    assert completions.calls[0]["messages"] == messages
