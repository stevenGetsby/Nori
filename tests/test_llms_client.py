from __future__ import annotations

from types import SimpleNamespace

import pytest

import nori.core.llms.client as client_module
from nori.core.llms import LLMClientConfigError


def _model(*, api_key: str = " test-key ", base_url: str = " https://api.test/v1 "):
    return SimpleNamespace(
        key="openai::gpt-5-mini",
        provider_id="openai",
        api_key=api_key,
        base_url=base_url,
        model_id="gpt-5-mini",
    )


class FakeOpenAI:
    def __init__(self, **kwargs):
        self.kwargs = kwargs


class FakeAsyncOpenAI(FakeOpenAI):
    pass


def test_get_client_validates_and_trims_openai_config(monkeypatch):
    monkeypatch.setattr(client_module, "get_active", lambda usage: _model())
    monkeypatch.setattr(client_module, "OpenAI", FakeOpenAI)

    bundle = client_module.get_client("llm")

    assert bundle.model_id == "gpt-5-mini"
    assert bundle.client.kwargs == {
        "api_key": "test-key",
        "base_url": "https://api.test/v1",
    }


def test_build_client_bundle_reuses_resolved_model(monkeypatch):
    model = _model()
    monkeypatch.setattr(client_module, "OpenAI", FakeOpenAI)

    bundle = client_module.build_client_bundle(model, "image")

    assert bundle.model is model
    assert bundle.model_id == "gpt-5-mini"
    assert bundle.client.kwargs == {
        "api_key": "test-key",
        "base_url": "https://api.test/v1",
    }


def test_build_chat_model_bundle_uses_langchain_init_chat_model(monkeypatch):
    model = _model()
    calls: list[dict] = []

    def fake_init_chat_model(model_name, *, model_provider=None, **kwargs):
        calls.append(
            {
                "model": model_name,
                "model_provider": model_provider,
                "kwargs": kwargs,
            }
        )
        return FakeOpenAI(model=model_name, model_provider=model_provider, **kwargs)

    monkeypatch.setattr(client_module, "init_chat_model", fake_init_chat_model, raising=False)

    bundle = client_module.build_chat_model_bundle(model, "llm")

    assert bundle.model is model
    assert bundle.model_id == "gpt-5-mini"
    assert calls == [
        {
            "model": "gpt-5-mini",
            "model_provider": "openai",
            "kwargs": {
                "api_key": "test-key",
                "base_url": "https://api.test/v1",
            },
        }
    ]
    assert bundle.client.kwargs == {
        "model": "gpt-5-mini",
        "model_provider": "openai",
        "api_key": "test-key",
        "base_url": "https://api.test/v1",
    }


def test_build_async_client_bundle_reuses_resolved_model(monkeypatch):
    model = _model()
    monkeypatch.setattr(client_module, "AsyncOpenAI", FakeAsyncOpenAI)

    bundle = client_module.build_async_client_bundle(model, "llm")

    assert bundle.model is model
    assert bundle.client.kwargs == {
        "api_key": "test-key",
        "base_url": "https://api.test/v1",
    }


def test_validate_api_key_returns_trimmed_key():
    assert client_module.validate_api_key(_model(), "llm") == "test-key"


def test_validate_api_key_fails_for_blank_key():
    with pytest.raises(LLMClientConfigError, match="api_key 为空"):
        client_module.validate_api_key(_model(api_key=" "), "llm")


def test_get_async_client_uses_same_config_validation(monkeypatch):
    monkeypatch.setattr(client_module, "get_active", lambda usage: _model())
    monkeypatch.setattr(client_module, "AsyncOpenAI", FakeAsyncOpenAI)

    bundle = client_module.get_async_client("vision")

    assert bundle.client.kwargs == {
        "api_key": "test-key",
        "base_url": "https://api.test/v1",
    }


def test_get_client_fails_before_sdk_when_api_key_is_blank(monkeypatch):
    calls = []
    monkeypatch.setattr(client_module, "get_active", lambda usage: _model(api_key=" "))
    monkeypatch.setattr(client_module, "OpenAI", lambda **kwargs: calls.append(kwargs))

    with pytest.raises(LLMClientConfigError, match="api_key 为空"):
        client_module.get_client("llm")

    assert calls == []


def test_get_client_fails_before_sdk_when_base_url_is_blank(monkeypatch):
    calls = []
    monkeypatch.setattr(client_module, "get_active", lambda usage: _model(base_url=""))
    monkeypatch.setattr(client_module, "OpenAI", lambda **kwargs: calls.append(kwargs))

    with pytest.raises(LLMClientConfigError, match="base_url 为空"):
        client_module.get_client("image")

    assert calls == []
