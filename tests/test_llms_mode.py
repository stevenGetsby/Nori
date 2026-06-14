from __future__ import annotations

from types import SimpleNamespace

import pytest

import nori.core.llms.client as client_module
from nori.core.llms import LLMClientConfigError


def _model(
    *,
    api_key: str = " test-key ",
    base_url: str = " http://localhost:8313/v1 ",
):
    return SimpleNamespace(
        key="ghc::gpt-5-mini",
        api_key=api_key,
        base_url=base_url,
    )


def test_ensure_ready_direct_validates_config_without_http_probe(monkeypatch):
    calls = []
    monkeypatch.setenv("NORI_MODE", "direct")
    monkeypatch.setattr(client_module, "get_active", lambda usage: _model())
    monkeypatch.setattr(client_module.httpx, "get", lambda *args, **kwargs: calls.append((args, kwargs)))

    client_module.ensure_ready("llm")

    assert calls == []


def test_ensure_ready_raises_client_config_error_for_blank_api_key(monkeypatch):
    monkeypatch.setenv("NORI_MODE", "direct")
    monkeypatch.setattr(client_module, "get_active", lambda usage: _model(api_key=" "))

    with pytest.raises(LLMClientConfigError, match="api_key 为空"):
        client_module.ensure_ready("llm")


def test_ensure_ready_raises_client_config_error_for_blank_base_url(monkeypatch):
    monkeypatch.setenv("NORI_MODE", "direct")
    monkeypatch.setattr(client_module, "get_active", lambda usage: _model(base_url=" "))

    with pytest.raises(LLMClientConfigError, match="base_url 为空"):
        client_module.ensure_ready("llm")


def test_ensure_ready_ghc_probes_models_with_trimmed_config(monkeypatch):
    calls = []
    monkeypatch.setenv("NORI_MODE", "ghc")
    monkeypatch.setattr(client_module, "get_active", lambda usage: _model())

    class Response:
        def raise_for_status(self):
            return None

    def fake_get(url, *, headers, timeout):
        calls.append({"url": url, "headers": headers, "timeout": timeout})
        return Response()

    monkeypatch.setattr(client_module.httpx, "get", fake_get)

    client_module.ensure_ready("llm", timeout=9)

    assert calls == [
        {
            "url": "http://localhost:8313/v1/models",
            "headers": {"Authorization": "Bearer test-key"},
            "timeout": 9,
        }
    ]


def test_current_mode_strips_environment_override(monkeypatch):
    monkeypatch.setenv("NORI_MODE", " ghc ")

    assert client_module.current_mode() == "ghc"


def test_set_mode_strips_runtime_input_before_reload(monkeypatch):
    reload_calls = []
    monkeypatch.delenv("NORI_MODE", raising=False)
    monkeypatch.setattr(client_module, "_reload_config", lambda: reload_calls.append(True))

    assert client_module.set_mode(" ghc ") == "ghc"
    assert reload_calls == [True]
    assert client_module.os.getenv("NORI_MODE") == "ghc"


def test_ensure_ready_ghc_with_whitespace_mode_still_probes_proxy(monkeypatch):
    calls = []
    monkeypatch.setenv("NORI_MODE", " ghc ")
    monkeypatch.setattr(client_module, "get_active", lambda usage: _model())

    class Response:
        def raise_for_status(self):
            return None

    def fake_get(url, *, headers, timeout):
        calls.append({"url": url, "headers": headers, "timeout": timeout})
        return Response()

    monkeypatch.setattr(client_module.httpx, "get", fake_get)

    client_module.ensure_ready("llm", timeout=5)

    assert calls == [
        {
            "url": "http://localhost:8313/v1/models",
            "headers": {"Authorization": "Bearer test-key"},
            "timeout": 5,
        }
    ]


def test_ensure_ready_ghc_proxy_failure_preserves_startup_hint(monkeypatch):
    monkeypatch.setenv("NORI_MODE", "ghc")
    monkeypatch.setattr(client_module, "get_active", lambda usage: _model())

    def fake_get(*args, **kwargs):
        raise RuntimeError("connection refused")

    monkeypatch.setattr(client_module.httpx, "get", fake_get)

    with pytest.raises(RuntimeError, match="ghc 代理不可用"):
        client_module.ensure_ready("llm")
