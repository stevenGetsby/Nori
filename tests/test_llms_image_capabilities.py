from __future__ import annotations

import base64
from types import SimpleNamespace

import pytest

import llms.call as call_module
import llms.image_inputs as image_inputs
import llms.image_providers as image_providers
import llms.image_runner as image_runner
import llms.results as results_module
from llms import ImageCapabilityError, ImageResultError, LLMClientConfigError, set_telemetry_sink


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


class EmptyImages(FakeImages):
    def generate(self, **kwargs):
        self.generate_calls.append(kwargs)
        return FakeImageResponse(FakeImageItem())


@pytest.fixture(autouse=True)
def _clear_telemetry_sink():
    set_telemetry_sink(None)
    yield
    set_telemetry_sink(None)


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


def test_image_input_helpers_normalize_supported_sources(tmp_path):
    image_path = tmp_path / "source.png"
    image_path.write_bytes(PNG_BYTES)
    encoded = base64.b64encode(PNG_BYTES).decode()

    assert image_inputs.load_image_bytes(PNG_BYTES) == PNG_BYTES
    assert image_inputs.load_image_bytes(bytearray(PNG_BYTES)) == PNG_BYTES
    assert image_inputs.load_image_bytes(f"data:image/png;base64,{encoded}") == PNG_BYTES
    assert image_inputs.load_image_bytes(image_path) == PNG_BYTES
    assert image_inputs.load_image_bytes(str(image_path)) == PNG_BYTES
    assert image_inputs.load_image_bytes(encoded) == PNG_BYTES
    assert image_inputs.load_image_bytes("https://example.test/source.png") == b""
    assert image_inputs.load_image_bytes("not valid base64") == b""
    assert image_inputs.load_image_bytes(None) == b""


def test_image_input_helpers_sniff_mime_and_build_data_uri():
    webp = b"RIFFxxxxWEBPpayload"
    data_uri = image_inputs.bytes_to_data_uri(PNG_BYTES)
    _, _, payload = data_uri.partition(",")

    assert image_inputs.sniff_mime(PNG_BYTES) == "image/png"
    assert image_inputs.sniff_mime(b"\xff\xd8\xffjpeg") == "image/jpeg"
    assert image_inputs.sniff_mime(b"GIF89aimage") == "image/gif"
    assert image_inputs.sniff_mime(webp) == "image/webp"
    assert image_inputs.sniff_mime(b"unknown") == "image/png"
    assert data_uri.startswith("data:image/png;base64,")
    assert base64.b64decode(payload) == PNG_BYTES


def test_openai_image_edit_provider_wraps_reference_bytes_as_named_files():
    model = _model(supports_reference_image=True)
    images = FakeImages()

    result = image_providers.image_openai_edit(
        _bundle(model, images),
        "edit this",
        [PNG_BYTES, b"\xff\xd8\xfffake"],
        "1024x1024",
        {"extra_body": {"quality": "high"}},
    )

    assert result == ["data:image/png;base64,ZmFrZQ=="]
    assert images.generate_calls == []
    call = images.edit_calls[0]
    image_arg = call["image"]
    assert call["model"] == "image-model"
    assert call["prompt"] == "edit this"
    assert call["size"] == "1024x1024"
    assert isinstance(image_arg, list)
    assert [item.name for item in image_arg] == ["input_0.png", "input_1.png"]
    assert [item.getvalue() for item in image_arg] == [PNG_BYTES, b"\xff\xd8\xfffake"]


def test_relay_image_provider_retries_reference_payload_variants_without_mutating_kwargs():
    class RetryRelayImages(FakeImages):
        def generate(self, **kwargs):
            self.generate_calls.append(kwargs)
            if len(self.generate_calls) == 1:
                raise RuntimeError("unsupported image_urls")
            return FakeImageResponse(FakeImageItem(url="https://example.test/relay.png"))

    model = _model(supports_reference_image=True, provider_id="relay")
    images = RetryRelayImages()
    request_kwargs = {"extra_body": {"trace": "caller"}, "response_format": "b64_json"}

    result = image_providers.image_relay_generate_with_references(
        _bundle(model, images),
        "edit this",
        [PNG_BYTES],
        "1024x1024",
        request_kwargs,
    )

    assert result == ["https://example.test/relay.png"]
    assert request_kwargs == {"extra_body": {"trace": "caller"}, "response_format": "b64_json"}
    assert len(images.generate_calls) == 2
    assert images.generate_calls[0]["extra_body"]["trace"] == "caller"
    assert images.generate_calls[0]["extra_body"]["image_urls"][0].startswith("data:image/png;base64,")
    assert "images" not in images.generate_calls[0]["extra_body"]
    assert images.generate_calls[1]["extra_body"]["trace"] == "caller"
    assert images.generate_calls[1]["extra_body"]["images"][0].startswith("data:image/png;base64,")
    assert "image_urls" not in images.generate_calls[1]["extra_body"]
    assert images.generate_calls[1]["size"] == "1024x1024"


def test_image_text_generation_does_not_require_reference_capability(monkeypatch):
    model = _model(supports_reference_image=False)
    images = FakeImages()
    monkeypatch.setattr(call_module, "get_active", lambda usage: model)
    monkeypatch.setattr(call_module, "build_client_bundle", lambda model_arg, usage: _bundle(model_arg, images))

    result = call_module.image("draw a flower", usage="image")

    assert result == ["https://example.test/generated.png"]
    assert images.generate_calls[0]["size"] == "1024x1024"
    assert images.edit_calls == []


def test_image_generation_merges_model_extra_body_without_mutating_caller(monkeypatch):
    model = _model(
        supports_reference_image=False,
        extra_body={"quality": "high", "metadata": {"source": "model"}},
    )
    images = FakeImages()
    caller_extra_body = {"metadata": {"source": "caller"}, "trace": "local"}
    monkeypatch.setattr(call_module, "get_active", lambda usage: model)
    monkeypatch.setattr(call_module, "build_client_bundle", lambda model_arg, usage: _bundle(model_arg, images))

    result = call_module.image("draw a flower", usage="image", extra_body=caller_extra_body)

    assert result == ["https://example.test/generated.png"]
    assert caller_extra_body == {"metadata": {"source": "caller"}, "trace": "local"}
    assert images.generate_calls[0]["extra_body"] == {
        "metadata": {"source": "model"},
        "trace": "local",
        "quality": "high",
    }
    assert images.generate_calls[0]["extra_body"] is not caller_extra_body


def test_image_generation_fails_when_provider_returns_no_results(monkeypatch):
    records = []
    model = _model(supports_reference_image=False)
    images = EmptyImages()
    monkeypatch.setattr(call_module, "get_active", lambda usage: model)
    monkeypatch.setattr(call_module, "build_client_bundle", lambda model_arg, usage: _bundle(model_arg, images))
    set_telemetry_sink(records.append)

    with pytest.raises(ImageResultError, match="未返回可用图片"):
        call_module.image("draw a flower", usage="image")

    assert images.generate_calls
    assert records[0]["operation"] == "image"
    assert records[0]["success"] is False
    assert records[0]["error_type"] == "ImageResultError"


def test_collect_image_results_accepts_url_and_b64_items():
    response = SimpleNamespace(
        data=[
            SimpleNamespace(url="https://example.test/a.png", b64_json=""),
            SimpleNamespace(url="", b64_json="ZmFrZQ=="),
        ]
    )

    assert results_module.collect_image_results(response) == [
        "https://example.test/a.png",
        "data:image/png;base64,ZmFrZQ==",
    ]


def test_image_reference_request_fails_before_provider_when_capability_disabled(monkeypatch):
    model = _model(supports_reference_image=False)
    images = FakeImages()
    monkeypatch.setattr(call_module, "get_active", lambda usage: model)
    monkeypatch.setattr(call_module, "build_client_bundle", lambda model_arg, usage: _bundle(model_arg, images))

    with pytest.raises(ImageCapabilityError, match="supports_reference_image"):
        call_module.image("edit this", usage="image", reference_images=[PNG_BYTES])

    assert images.generate_calls == []
    assert images.edit_calls == []


def test_image_reference_request_uses_edit_when_capability_enabled(monkeypatch):
    model = _model(supports_reference_image=True)
    images = FakeImages()
    monkeypatch.setattr(call_module, "get_active", lambda usage: model)
    monkeypatch.setattr(call_module, "build_client_bundle", lambda model_arg, usage: _bundle(model_arg, images))

    result = call_module.image("edit this", usage="image", reference_images=[PNG_BYTES], size="1024x1024")

    assert result == ["data:image/png;base64,ZmFrZQ=="]
    assert images.generate_calls == []
    assert images.edit_calls[0]["prompt"] == "edit this"
    assert images.edit_calls[0]["size"] == "1024x1024"


def test_image_rejects_non_image_active_model_before_provider(monkeypatch):
    model = _model(supports_reference_image=False)
    model.type = "llm"
    images = FakeImages()
    monkeypatch.setattr(call_module, "get_active", lambda usage: model)
    monkeypatch.setattr(call_module, "build_client_bundle", lambda model_arg, usage: _bundle(model_arg, images))

    with pytest.raises(ImageCapabilityError, match="expected type='image'"):
        call_module.image("draw", usage="image")

    assert images.generate_calls == []
    assert images.edit_calls == []


def test_image_uses_single_resolved_model_for_capability_and_client(monkeypatch):
    model = _model(supports_reference_image=True)
    images = FakeImages()
    active_calls = []
    bundle_models = []

    def fake_get_active(usage):
        active_calls.append(usage)
        return model

    def fake_build_client_bundle(model_arg, usage):
        bundle_models.append(model_arg)
        return _bundle(model_arg, images)

    monkeypatch.setattr(call_module, "get_active", fake_get_active)
    monkeypatch.setattr(call_module, "build_client_bundle", fake_build_client_bundle)

    result = call_module.image("edit this", usage="image", reference_images=[PNG_BYTES])

    assert result == ["data:image/png;base64,ZmFrZQ=="]
    assert active_calls == ["image"]
    assert bundle_models == [model]


def test_google_image_fails_before_provider_when_api_key_is_blank(monkeypatch):
    records = []
    model = _model(
        supports_reference_image=False,
        provider_id="google",
        api_key=" ",
    )
    monkeypatch.setattr(call_module, "get_active", lambda usage: model)
    set_telemetry_sink(records.append)

    with pytest.raises(LLMClientConfigError, match="api_key 为空"):
        call_module.image("draw", usage="image")

    assert records[0]["operation"] == "image"
    assert records[0]["success"] is False
    assert records[0]["error_type"] == "LLMClientConfigError"


def test_google_image_uses_trimmed_api_key(monkeypatch):
    captured = {}
    model = _model(
        supports_reference_image=False,
        provider_id="google",
        api_key=" test-google-key ",
    )
    monkeypatch.setattr(call_module, "get_active", lambda usage: model)

    def fake_google(prompt, model_arg, size, ref_bytes_list=None, *, api_key):
        captured["prompt"] = prompt
        captured["model"] = model_arg
        captured["size"] = size
        captured["refs"] = ref_bytes_list
        captured["api_key"] = api_key
        return ["data:image/png;base64,ZmFrZQ=="]

    monkeypatch.setattr(image_runner, "image_google", fake_google)

    result = call_module.image("draw", usage="image", size="1024x1024")

    assert result == ["data:image/png;base64,ZmFrZQ=="]
    assert captured["api_key"] == "test-google-key"
    assert captured["model"] is model


def test_google_image_empty_results_raise_result_error(monkeypatch):
    model = _model(
        supports_reference_image=False,
        provider_id="google",
        api_key="test-google-key",
    )
    monkeypatch.setattr(call_module, "get_active", lambda usage: model)
    monkeypatch.setattr(image_runner, "image_google", lambda *args, **kwargs: [])

    with pytest.raises(ImageResultError, match="未返回可用图片"):
        call_module.image("draw", usage="image", size="1024x1024")
