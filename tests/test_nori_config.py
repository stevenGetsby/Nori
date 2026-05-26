from __future__ import annotations

import os
from pathlib import Path

import pytest
import yaml

from nori.nori_config import (
    NoriConfigError,
    NoriConfig,
    format_model_key,
    format_provider_id,
    parse_model_key,
)


def _write_config(path: Path) -> Path:
    data = {
        "mode": "direct",
        "providers": {
            "openai": {
                "base_url": "https://api.openai.com/v1",
                "api_key_env": "NORI_TEST_OPENAI_KEY",
            },
            "ghc": {
                "base_url": "http://localhost:8313/v1",
                "api_key": "${NORI_TEST_GHC_KEY}",
            },
            "relay": {
                "base_url": "https://relay.example.test/v1",
                "api_key": "literal-relay-key",
            },
        },
        "models": {
            "openai::gpt-5-mini": {
                "type": "llm",
                "name": "GPT-5 Mini",
                "max_output": 2048,
                "supports_vision": True,
                "temperature_fixed": 1,
            },
            "ghc::gpt-5-mini": {"type": "llm", "name": "GHC GPT-5 Mini"},
            "relay::gpt-image-2": {
                "type": "image",
                "resolution_options": ["1072x1440"],
                "supports_reference_image": True,
            },
            "relay::video-gen": {
                "type": "video",
                "duration_options": [5, 10],
                "supports_audio": True,
            },
        },
        "active_models": {
            "direct": {"llm": "openai::gpt-5-mini", "image": "relay::gpt-image-2"},
            "ghc": {"llm": "ghc::gpt-5-mini", "image": "relay::gpt-image-2"},
        },
        "evolution": {"sample": 3},
    }
    path.write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")
    return path


def test_parse_model_key_requires_provider_separator():
    assert parse_model_key("openai::gpt-5-mini") == ("openai", "gpt-5-mini")
    with pytest.raises(ValueError, match="无效模型键"):
        parse_model_key("gpt-5-mini")
    with pytest.raises(ValueError, match="无效模型键"):
        parse_model_key("openai::")
    with pytest.raises(ValueError, match="无效模型键"):
        parse_model_key("::gpt-5-mini")


def test_parse_model_key_strips_outer_segments():
    assert parse_model_key(" openai :: gpt-5-mini ") == ("openai", "gpt-5-mini")


def test_format_model_key_canonicalizes_segments():
    assert format_model_key(" openai ", " gpt-5-mini ") == "openai::gpt-5-mini"


def test_format_provider_id_requires_nonblank_id():
    assert format_provider_id(" openai ") == "openai"
    with pytest.raises(ValueError, match="无效服务商 id"):
        format_provider_id(" ")


def test_nori_config_loads_env_keys_and_mode_specific_active_models(tmp_path, monkeypatch):
    config_path = _write_config(tmp_path / "api_config.yaml")
    monkeypatch.setenv("NORI_TEST_OPENAI_KEY", "env-openai-key")
    monkeypatch.setenv("NORI_TEST_GHC_KEY", "env-ghc-key")
    monkeypatch.delenv("NORI_MODE", raising=False)

    cfg = NoriConfig(config_path)
    llm = cfg.get_active("llm")
    image = cfg.get_active("image")

    assert cfg.config_path == str(config_path)
    assert cfg.mode == "direct"
    assert cfg.active_summary == {"llm": "openai::gpt-5-mini", "image": "relay::gpt-image-2"}
    assert llm.api_key == "env-openai-key"
    assert llm.base_url == "https://api.openai.com/v1"
    assert llm.max_output == 2048
    assert llm.supports_vision is True
    assert llm.temperature_fixed == 1
    assert image.api_key == "literal-relay-key"
    assert image.resolution_options == ["1072x1440"]
    assert image.supports_reference_image is True
    video = cfg.resolve("relay::video-gen")
    assert video.duration_options == [5, 10]
    assert video.supports_audio is True
    assert cfg.evolution_param("sample") == 3


def test_api_key_env_name_is_canonicalized(tmp_path, monkeypatch):
    config_path = _write_config(tmp_path / "api_config.yaml")
    data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    data["providers"]["openai"]["api_key_env"] = " NORI_TEST_OPENAI_KEY "
    config_path.write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")
    monkeypatch.setenv("NORI_TEST_OPENAI_KEY", "env-openai-key")
    monkeypatch.delenv("NORI_MODE", raising=False)

    cfg = NoriConfig(config_path)

    assert cfg.get_provider("openai").api_key_env == "NORI_TEST_OPENAI_KEY"
    assert cfg.get_active("llm").api_key == "env-openai-key"


def test_api_key_env_placeholder_name_is_canonicalized(tmp_path, monkeypatch):
    config_path = _write_config(tmp_path / "api_config.yaml")
    data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    data["providers"]["ghc"]["api_key"] = "${ NORI_TEST_GHC_KEY }"
    config_path.write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")
    monkeypatch.setenv("NORI_TEST_GHC_KEY", "env-ghc-key")
    monkeypatch.setenv("NORI_MODE", "ghc")

    cfg = NoriConfig(config_path)

    assert cfg.get_active("llm").api_key == "env-ghc-key"


def test_nori_mode_env_selects_matching_active_models(tmp_path, monkeypatch):
    config_path = _write_config(tmp_path / "api_config.yaml")
    monkeypatch.setenv("NORI_TEST_GHC_KEY", "env-ghc-key")
    monkeypatch.setenv("NORI_MODE", "ghc")

    cfg = NoriConfig(config_path)
    llm = cfg.get_active("llm")

    assert cfg.mode == "ghc"
    assert cfg.active_summary["llm"] == "ghc::gpt-5-mini"
    assert llm.provider_id == "ghc"
    assert llm.api_key == "env-ghc-key"


def test_flat_active_models_shape_still_works(tmp_path, monkeypatch):
    config_path = _write_config(tmp_path / "api_config.yaml")
    data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    data["active_models"] = {"llm": "openai::gpt-5-mini"}
    config_path.write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")
    monkeypatch.setenv("NORI_TEST_OPENAI_KEY", "env-openai-key")
    monkeypatch.delenv("NORI_MODE", raising=False)

    cfg = NoriConfig(config_path)

    assert cfg.active_summary == {"llm": "openai::gpt-5-mini"}
    assert cfg.get_active("llm").api_key == "env-openai-key"


def test_model_keys_are_canonicalized_before_model_lookup(tmp_path, monkeypatch):
    config_path = _write_config(tmp_path / "api_config.yaml")
    data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    data["models"][" openai :: gpt-5-mini "] = data["models"].pop("openai::gpt-5-mini")
    data["active_models"]["direct"]["llm"] = " openai :: gpt-5-mini "
    config_path.write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")
    monkeypatch.setenv("NORI_TEST_OPENAI_KEY", "env-openai-key")
    monkeypatch.delenv("NORI_MODE", raising=False)

    cfg = NoriConfig(config_path)
    llm = cfg.get_active("llm")

    assert cfg.active_summary["llm"] == "openai::gpt-5-mini"
    assert llm.key == "openai::gpt-5-mini"
    assert llm.name == "GPT-5 Mini"
    assert llm.max_output == 2048
    assert llm.supports_vision is True


def test_provider_keys_are_canonicalized_before_resolve(tmp_path, monkeypatch):
    config_path = _write_config(tmp_path / "api_config.yaml")
    data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    data["providers"][" openai "] = data["providers"].pop("openai")
    config_path.write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")
    monkeypatch.setenv("NORI_TEST_OPENAI_KEY", "env-openai-key")
    monkeypatch.delenv("NORI_MODE", raising=False)

    cfg = NoriConfig(config_path)
    llm = cfg.get_active("llm")

    assert cfg.get_provider(" openai ").id == "openai"
    assert llm.provider_id == "openai"
    assert llm.api_key == "env-openai-key"


def test_mode_and_mode_blocks_are_canonicalized(tmp_path, monkeypatch):
    config_path = _write_config(tmp_path / "api_config.yaml")
    data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    data["mode"] = " direct "
    data["active_models"][" direct "] = data["active_models"].pop("direct")
    config_path.write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")
    monkeypatch.setenv("NORI_TEST_OPENAI_KEY", "env-openai-key")
    monkeypatch.delenv("NORI_MODE", raising=False)

    cfg = NoriConfig(config_path)

    assert cfg.mode == "direct"
    assert cfg.active_summary["llm"] == "openai::gpt-5-mini"
    assert cfg.get_active("llm").api_key == "env-openai-key"


def test_nori_mode_env_is_canonicalized(tmp_path, monkeypatch):
    config_path = _write_config(tmp_path / "api_config.yaml")
    monkeypatch.setenv("NORI_TEST_GHC_KEY", "env-ghc-key")
    monkeypatch.setenv("NORI_MODE", " ghc ")

    cfg = NoriConfig(config_path)

    assert cfg.mode == "ghc"
    assert cfg.active_summary["llm"] == "ghc::gpt-5-mini"
    assert cfg.get_active("llm").api_key == "env-ghc-key"


def test_malformed_active_models_shape_becomes_missing_usage_error(tmp_path, monkeypatch):
    config_path = _write_config(tmp_path / "api_config.yaml")
    data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    data["active_models"] = ["llm", "openai::gpt-5-mini"]
    config_path.write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")
    monkeypatch.delenv("NORI_MODE", raising=False)

    cfg = NoriConfig(config_path)

    assert cfg.active_summary == {}
    with pytest.raises(KeyError, match="active_models.llm"):
        cfg.get_active("llm")


def test_blank_active_model_values_are_ignored(tmp_path, monkeypatch):
    config_path = _write_config(tmp_path / "api_config.yaml")
    data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    data["active_models"]["direct"]["llm"] = "   "
    config_path.write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")
    monkeypatch.delenv("NORI_MODE", raising=False)

    cfg = NoriConfig(config_path)

    assert "llm" not in cfg.active_summary
    with pytest.raises(KeyError, match="active_models.llm"):
        cfg.get_active("llm")


def test_get_active_canonicalizes_usage_key(tmp_path, monkeypatch):
    config_path = _write_config(tmp_path / "api_config.yaml")
    monkeypatch.setenv("NORI_TEST_OPENAI_KEY", "env-openai-key")
    monkeypatch.delenv("NORI_MODE", raising=False)

    model = NoriConfig(config_path).get_active(" llm ")

    assert model.key == "openai::gpt-5-mini"
    assert model.api_key == "env-openai-key"


def test_non_string_active_model_values_raise_invalid_model_key(tmp_path, monkeypatch):
    config_path = _write_config(tmp_path / "api_config.yaml")
    data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    data["active_models"]["direct"]["llm"] = 123
    config_path.write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")
    monkeypatch.delenv("NORI_MODE", raising=False)

    cfg = NoriConfig(config_path)

    assert cfg.active_summary["llm"] == "123"
    with pytest.raises(ValueError, match="无效模型键"):
        cfg.get_active("llm")


def test_blank_model_id_in_active_model_key_raises_invalid_model_key(
    tmp_path, monkeypatch
):
    config_path = _write_config(tmp_path / "api_config.yaml")
    data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    data["active_models"]["direct"]["llm"] = "openai::"
    config_path.write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")
    monkeypatch.delenv("NORI_MODE", raising=False)

    cfg = NoriConfig(config_path)

    with pytest.raises(ValueError, match="无效模型键"):
        cfg.get_active("llm")


def test_nori_mode_env_without_matching_block_clears_nested_active_models(
    tmp_path, monkeypatch
):
    config_path = _write_config(tmp_path / "api_config.yaml")
    monkeypatch.setenv("NORI_MODE", "missing-mode")

    cfg = NoriConfig(config_path)

    assert cfg.mode == "missing-mode"
    assert cfg.active_summary == {}
    with pytest.raises(KeyError, match="active_models.llm"):
        cfg.get_active("llm")


def test_nori_config_env_path_fails_fast_when_missing(monkeypatch, tmp_path):
    missing = tmp_path / "missing.yaml"
    monkeypatch.setenv("NORI_CONFIG", str(missing))

    with pytest.raises(FileNotFoundError, match="NORI_CONFIG"):
        NoriConfig()


@pytest.mark.parametrize(
    ("section", "value"),
    [
        ("providers", ["openai"]),
        ("models", ["openai::gpt-5-mini"]),
    ],
)
def test_nori_config_rejects_non_mapping_core_sections(
    tmp_path, monkeypatch, section, value
):
    config_path = _write_config(tmp_path / "api_config.yaml")
    data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    data[section] = value
    config_path.write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")
    monkeypatch.delenv("NORI_MODE", raising=False)

    with pytest.raises(NoriConfigError, match=f"api_config.yaml.{section}"):
        NoriConfig(config_path)


@pytest.mark.parametrize(
    ("section", "key", "value"),
    [
        ("providers", "openai", "not-a-provider-map"),
        ("models", "openai::gpt-5-mini", ["not-a-model-map"]),
    ],
)
def test_nori_config_rejects_non_mapping_core_section_entries(
    tmp_path, monkeypatch, section, key, value
):
    config_path = _write_config(tmp_path / "api_config.yaml")
    data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    data[section][key] = value
    config_path.write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")
    monkeypatch.delenv("NORI_MODE", raising=False)

    with pytest.raises(NoriConfigError, match=f"api_config.yaml.{section}.{key}"):
        NoriConfig(config_path)


def test_nori_config_rejects_non_mapping_top_level(tmp_path, monkeypatch):
    config_path = tmp_path / "api_config.yaml"
    config_path.write_text("- not\n- a\n- mapping\n", encoding="utf-8")
    monkeypatch.delenv("NORI_MODE", raising=False)

    with pytest.raises(NoriConfigError, match="api_config.yaml 顶层"):
        NoriConfig(config_path)


def test_missing_active_usage_and_provider_errors_are_explicit(tmp_path):
    config_path = _write_config(tmp_path / "api_config.yaml")
    cfg = NoriConfig(config_path)

    with pytest.raises(KeyError, match="active_models.vision"):
        cfg.get_active("vision")
    with pytest.raises(KeyError, match="未配置服务商"):
        cfg.resolve("missing::model")


def test_resolve_unknown_model_key_fails_instead_of_defaulting(tmp_path):
    config_path = _write_config(tmp_path / "api_config.yaml")
    cfg = NoriConfig(config_path)

    with pytest.raises(KeyError, match="未配置模型"):
        cfg.resolve("openai::not-in-config")


def test_active_model_pointing_to_unknown_model_fails_explicitly(
    tmp_path, monkeypatch
):
    config_path = _write_config(tmp_path / "api_config.yaml")
    data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    data["active_models"]["direct"]["llm"] = "openai::not-in-config"
    config_path.write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")
    monkeypatch.setenv("NORI_TEST_OPENAI_KEY", "env-openai-key")
    monkeypatch.delenv("NORI_MODE", raising=False)

    cfg = NoriConfig(config_path)

    with pytest.raises(KeyError, match="未配置模型"):
        cfg.get_active("llm")


def test_model_config_coerces_string_scalars_and_booleans(tmp_path, monkeypatch):
    config_path = _write_config(tmp_path / "api_config.yaml")
    data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    data["models"]["openai::gpt-5-mini"].update(
        {
            "context_window": "128000",
            "max_output": "8192",
            "supports_vision": "false",
            "supports_thinking": "true",
            "temperature_fixed": "0.5",
            "resolution_options": "1024x1024",
            "supports_reference_image": "false",
            "duration_options": ["5", True, "bad", 10],
            "supports_audio": "yes",
            "extra_body": "not-a-dict",
        }
    )
    config_path.write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")
    monkeypatch.setenv("NORI_TEST_OPENAI_KEY", "env-openai-key")
    monkeypatch.delenv("NORI_MODE", raising=False)

    model = NoriConfig(config_path).get_active("llm")

    assert model.context_window == 128000
    assert model.max_output == 8192
    assert model.supports_vision is False
    assert model.supports_thinking is True
    assert model.temperature_fixed == 0.5
    assert model.resolution_options == ["1024x1024"]
    assert model.supports_reference_image is False
    assert model.duration_options == [5, 10]
    assert model.supports_audio is True
    assert model.extra_body == {}


def test_model_config_coerces_scalar_duration_option(tmp_path, monkeypatch):
    config_path = _write_config(tmp_path / "api_config.yaml")
    data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    data["models"]["relay::video-gen"]["duration_options"] = "10"
    config_path.write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")
    monkeypatch.delenv("NORI_MODE", raising=False)

    model = NoriConfig(config_path).resolve("relay::video-gen")

    assert model.duration_options == [10]
