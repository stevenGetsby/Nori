from __future__ import annotations

import asyncio
from types import SimpleNamespace

import pytest

import nori.core.llms as llms
import nori.core.llms.capabilities as capabilities
import nori.core.llms.telemetry as telemetry_module
from nori.core.llms.imager import ImageClient
from nori.core.llms.lm import LanguageModelClient
from nori.core.llms import ChatCapabilityError, ChatResultError, ImageCapabilityError, set_telemetry_sink


class FakeMessage:
    def __init__(self, content: str | None = " ok ") -> None:
        self.content = content


class FakeChatModel:
    def __init__(
        self,
        error: Exception | None = None,
        content: str | None = " ok ",
        response=None,
    ) -> None:
        self.error = error
        self.content = content
        self.response = response
        self.invoke_calls = []
        self.ainvoke_calls = []

    def invoke(self, messages, **kwargs):
        self.invoke_calls.append({"messages": messages, "kwargs": kwargs})
        if self.error:
            raise self.error
        if self.response is not None:
            return self.response
        return FakeMessage(self.content)

    async def ainvoke(self, messages, **kwargs):
        self.ainvoke_calls.append({"messages": messages, "kwargs": kwargs})
        if self.error:
            raise self.error
        if self.response is not None:
            return self.response
        return FakeMessage(self.content)


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
    chat_model: FakeChatModel | None = None,
    content: str | None = " ok ",
    response=None,
):
    model = model or _model(model_type="llm")
    chat_model = chat_model or FakeChatModel(error, content=content, response=response)
    return SimpleNamespace(
        model=model,
        model_id=model.model_id,
        client=chat_model,
    )


def _image_bundle(model, images: FakeImages):
    return SimpleNamespace(
        model=model,
        model_id=model.model_id,
        client=SimpleNamespace(images=images),
    )


def _lm_client(bundle) -> LanguageModelClient:
    return LanguageModelClient(
        chat_model_factory=lambda usage: bundle,
        async_chat_model_factory=lambda usage: bundle,
    )


def _image_client(model, images: FakeImages) -> ImageClient:
    return ImageClient(
        active_model_factory=lambda usage: model,
        client_bundle_factory=lambda model_arg, usage: _image_bundle(model_arg, images),
    )


@pytest.fixture(autouse=True)
def _clear_telemetry_sink():
    set_telemetry_sink(None)
    yield
    set_telemetry_sink(None)


def test_telemetry_setter_identity_is_stable():
    assert llms.set_telemetry_sink is telemetry_module.set_telemetry_sink


def test_chat_normalizes_langchain_message_content():
    response = FakeMessage("  ok from langchain message  ")
    client = _lm_client(_chat_bundle(response=response))

    assert client.chat([{"role": "user", "content": "hello"}]) == "ok from langchain message"


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


def test_chat_emits_redacted_telemetry_on_success():
    records = []
    client = _lm_client(_chat_bundle())
    set_telemetry_sink(records.append)

    result = client.chat([{"role": "user", "content": "secret prompt"}], usage="llm")

    assert result == "ok"
    assert records[0]["operation"] == "chat"
    assert records[0]["usage"] == "llm"
    assert records[0]["model_key"] == "openai::gpt-5-mini"
    assert records[0]["success"] is True
    assert "error_type" not in records[0]
    assert "prompt" not in records[0]
    assert "messages" not in records[0]


def test_chat_emits_telemetry_on_error_and_preserves_exception():
    records = []
    client = _lm_client(_chat_bundle(RuntimeError("provider down")))
    set_telemetry_sink(records.append)

    with pytest.raises(RuntimeError, match="provider down"):
        client.chat([{"role": "user", "content": "hello"}], usage="llm")

    assert records[0]["operation"] == "chat"
    assert records[0]["success"] is False
    assert records[0]["error_type"] == "RuntimeError"


def test_chat_empty_provider_content_raises_result_error():
    records = []
    client = _lm_client(_chat_bundle(content="   "))
    set_telemetry_sink(records.append)

    with pytest.raises(ChatResultError, match="未返回可用文本"):
        client.chat([{"role": "user", "content": "hello"}], usage="llm")

    assert records[0]["operation"] == "chat"
    assert records[0]["success"] is False
    assert records[0]["error_type"] == "ChatResultError"


def test_chat_missing_langchain_content_raises_result_error():
    records = []
    client = _lm_client(_chat_bundle(response=object()))
    set_telemetry_sink(records.append)

    with pytest.raises(ChatResultError, match="未返回可用文本"):
        client.chat([{"role": "user", "content": "hello"}], usage="llm")

    assert records[0]["operation"] == "chat"
    assert records[0]["success"] is False
    assert records[0]["error_type"] == "ChatResultError"


def test_achat_missing_langchain_content_raises_result_error():
    records = []
    client = _lm_client(_chat_bundle(response=object()))
    set_telemetry_sink(records.append)

    with pytest.raises(ChatResultError, match="未返回可用文本"):
        asyncio.run(client.achat([{"role": "user", "content": "hello"}], usage="llm"))

    assert records[0]["operation"] == "achat"
    assert records[0]["success"] is False
    assert records[0]["error_type"] == "ChatResultError"


def test_telemetry_sink_failure_does_not_break_call():
    client = _lm_client(_chat_bundle())

    def broken_sink(record):
        raise AssertionError("sink down")

    set_telemetry_sink(broken_sink)

    assert client.chat([{"role": "user", "content": "hello"}], usage="llm") == "ok"


def test_image_emits_telemetry_on_success():
    records = []
    model = _model(model_type="image")
    images = FakeImages()
    client = _image_client(model, images)
    set_telemetry_sink(records.append)

    result = client.image("secret prompt", usage="image")

    assert result == ["https://example.test/image.png"]
    assert records[0]["operation"] == "image"
    assert records[0]["usage"] == "image"
    assert records[0]["success"] is True
    assert "prompt" not in records[0]


def test_image_emits_telemetry_on_capability_error():
    records = []
    model = _model(model_type="image")
    images = FakeImages()
    client = _image_client(model, images)
    set_telemetry_sink(records.append)

    with pytest.raises(ImageCapabilityError):
        client.image("edit", usage="image", reference_images=[b"\x89PNG\r\n\x1a\nfake"])

    assert records[0]["operation"] == "image"
    assert records[0]["success"] is False
    assert records[0]["error_type"] == "ImageCapabilityError"


def test_chat_rejects_non_chat_model_before_provider():
    records = []
    chat_model = FakeChatModel()
    model = _model(model_type="image")
    client = _lm_client(_chat_bundle(model=model, chat_model=chat_model))
    set_telemetry_sink(records.append)

    with pytest.raises(ChatCapabilityError, match="expected type"):
        client.chat([{"role": "user", "content": "hello"}], usage="llm")

    assert chat_model.invoke_calls == []
    assert records[0]["operation"] == "chat"
    assert records[0]["success"] is False
    assert records[0]["error_type"] == "ChatCapabilityError"


def test_chat_vision_usage_requires_vision_capability():
    chat_model = FakeChatModel()
    model = _model(model_type="llm", supports_vision=False)
    client = _lm_client(_chat_bundle(model=model, chat_model=chat_model))

    with pytest.raises(ChatCapabilityError, match="support vision"):
        client.chat([{"role": "user", "content": "describe this"}], usage="vision")

    assert chat_model.invoke_calls == []


def test_chat_multimodal_message_requires_vision_capability():
    chat_model = FakeChatModel()
    model = _model(model_type="llm", supports_vision=False)
    client = _lm_client(_chat_bundle(model=model, chat_model=chat_model))
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
        client.chat(messages, usage="llm")

    assert chat_model.invoke_calls == []


def test_chat_multimodal_message_allows_vision_model():
    chat_model = FakeChatModel()
    model = _model(model_type="vision", supports_vision=True)
    client = _lm_client(_chat_bundle(model=model, chat_model=chat_model))
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "describe"},
                {"type": "image_url", "image_url": {"url": "data:image/png;base64,ZmFrZQ=="}},
            ],
        }
    ]

    assert client.chat(messages, usage="llm") == "ok"
    assert chat_model.invoke_calls[0]["messages"] == messages
