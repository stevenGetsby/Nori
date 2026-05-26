from __future__ import annotations

from types import SimpleNamespace

import pytest

import llms.image_runner as image_runner
from llms import ImageCapabilityError, LLMClientConfigError, set_telemetry_sink


PNG_BYTES = b"\x89PNG\r\n\x1a\nfake"


class FakeImageItem:
    def __init__(self, *, url: str = "", b64_json: str = "") -> None:
        self.url = url
        self.b64_json = b64_json


class FakeImageResponse:
    def __init__(self, item: FakeImageItem) -> None:
        self.data = [item]


class FakeImages:
    def __init__(self) -> None:
        self.generate_calls = []
        self.edit_calls = []

    def generate(self, **kwargs):
        self.generate_calls.append(kwargs)
        return FakeImageResponse(FakeImageItem(url="https://example.test/generated.png"))

    def edit(self, **kwargs):
        self.edit_calls.append(kwargs)
        return FakeImageResponse(FakeImageItem(b64_json="ZmFrZQ=="))


def _model(
    *,
    supports_reference_image: bool,
    provider_id: str = "openai",
    api_key: str = "test-key",
    extra_body: dict | None = None,
):
    return SimpleNamespace(
        key=f"{provider_id}::image-model",
        provider_id=provider_id,
        model_id="image-model",
        type="image",
        api_key=api_key,
        supports_reference_image=supports_reference_image,
        resolution_options=["1024x1024"],
        extra_body=extra_body or {},
    )


def _bundle(model, images: FakeImages):
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


def test_image_outputs_generates_text_image_with_defaults_and_telemetry():
    records = []
    model = _model(supports_reference_image=False)
    images = FakeImages()
    set_telemetry_sink(records.append)

    result = image_runner.image_outputs(
        "draw a flower",
        usage="image",
        _get_active=lambda usage: model,
        _build_client_bundle=lambda model_arg, usage: _bundle(model_arg, images),
    )

    assert result == ["https://example.test/generated.png"]
    assert images.generate_calls == [
        {"model": "image-model", "prompt": "draw a flower", "size": "1024x1024"}
    ]
    assert images.edit_calls == []
    assert records[0]["operation"] == "image"
    assert records[0]["success"] is True
    assert "prompt" not in records[0]


def test_image_outputs_rejects_reference_before_provider_when_capability_disabled():
    records = []
    model = _model(supports_reference_image=False)
    images = FakeImages()
    set_telemetry_sink(records.append)

    with pytest.raises(ImageCapabilityError, match="supports_reference_image"):
        image_runner.image_outputs(
            "edit",
            usage="image",
            reference_images=[PNG_BYTES],
            _get_active=lambda usage: model,
            _build_client_bundle=lambda model_arg, usage: _bundle(model_arg, images),
        )

    assert images.generate_calls == []
    assert images.edit_calls == []
    assert records[0]["success"] is False
    assert records[0]["error_type"] == "ImageCapabilityError"


def test_image_outputs_google_path_validates_api_key_and_uses_injected_provider():
    captured = {}
    model = _model(
        supports_reference_image=False,
        provider_id="google",
        api_key=" test-google-key ",
    )

    def fake_google(prompt, model_arg, size, ref_bytes_list=None, *, api_key):
        captured["prompt"] = prompt
        captured["model"] = model_arg
        captured["size"] = size
        captured["refs"] = ref_bytes_list
        captured["api_key"] = api_key
        return ["data:image/png;base64,ZmFrZQ=="]

    result = image_runner.image_outputs(
        "draw",
        usage="image",
        size="1024x1024",
        _get_active=lambda usage: model,
        _image_google_func=fake_google,
    )

    assert result == ["data:image/png;base64,ZmFrZQ=="]
    assert captured == {
        "prompt": "draw",
        "model": model,
        "size": "1024x1024",
        "refs": [],
        "api_key": "test-google-key",
    }


def test_image_outputs_google_blank_key_fails_before_provider():
    model = _model(supports_reference_image=False, provider_id="google", api_key=" ")

    with pytest.raises(LLMClientConfigError, match="api_key 为空"):
        image_runner.image_outputs("draw", usage="image", _get_active=lambda usage: model)
