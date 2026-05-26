from __future__ import annotations

import pytest

from nori import config_normalization


def test_model_and_provider_keys_are_canonicalized():
    assert config_normalization.parse_model_key(" openai :: gpt-5-mini ") == ("openai", "gpt-5-mini")
    assert config_normalization.format_model_key(" openai ", " gpt-5-mini ") == "openai::gpt-5-mini"
    assert config_normalization.format_provider_id(" openai ") == "openai"

    with pytest.raises(ValueError, match="无效模型键"):
        config_normalization.parse_model_key("openai::")
    with pytest.raises(ValueError, match="无效服务商 id"):
        config_normalization.format_provider_id(" ")


def test_config_sections_reject_malformed_core_shapes():
    assert config_normalization.config_section_mapping(None, "providers") == {}
    assert config_normalization.config_section_mapping({"openai": {}}, "providers") == {"openai": {}}
    assert config_normalization.config_entry_mapping({"base_url": "x"}, "providers", "openai") == {"base_url": "x"}

    with pytest.raises(config_normalization.NoriConfigError, match="api_config.yaml.providers"):
        config_normalization.config_section_mapping(["openai"], "providers")
    with pytest.raises(config_normalization.NoriConfigError, match="api_config.yaml.models.openai::gpt-5-mini"):
        config_normalization.config_entry_mapping([], "models", "openai::gpt-5-mini")


def test_active_model_selection_supports_flat_and_mode_blocks():
    nested = {
        " direct ": {" llm ": " openai :: gpt-5-mini ", "image": "relay::gpt-image-2"},
        "ghc": {"llm": "ghc::gpt-5-mini"},
    }
    flat = {" llm ": " openai :: gpt-5-mini "}

    assert config_normalization.select_active_models(nested, " direct ", fallback_mode="direct") == {
        "llm": "openai::gpt-5-mini",
        "image": "relay::gpt-image-2",
    }
    assert config_normalization.select_active_models(nested, "missing", fallback_mode="direct") == {
        "llm": "openai::gpt-5-mini",
        "image": "relay::gpt-image-2",
    }
    assert config_normalization.select_active_models(nested, "missing", fallback_mode=None) == {}
    assert config_normalization.select_active_models(flat, "direct", fallback_mode="direct") == {
        "llm": "openai::gpt-5-mini",
    }


def test_env_name_mode_key_and_api_key_resolution_are_canonical(monkeypatch):
    monkeypatch.setenv("NORI_TEST_KEY", "env-key")

    assert config_normalization.mode_key(" direct ", default="ghc") == "direct"
    assert config_normalization.mode_key("", default="direct") == "direct"
    assert config_normalization.env_name(" NORI_TEST_KEY ") == "NORI_TEST_KEY"
    assert config_normalization.resolve_api_key("", " NORI_TEST_KEY ") == "env-key"
    assert config_normalization.resolve_api_key("${ NORI_TEST_KEY }") == "env-key"
    assert config_normalization.resolve_api_key(" literal-key ") == " literal-key "
