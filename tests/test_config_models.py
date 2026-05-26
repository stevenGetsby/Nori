from __future__ import annotations

from nori import config_models
from nori.core import ProviderConfig, ModelConfig, ResolvedModel
from nori.core import contracts
from nori import nori_config


def test_config_model_dataclasses_live_in_core_contracts_boundary():
    provider = ProviderConfig(
        id="openai",
        base_url="https://api.example.test/v1",
        api_key="test-key",
    )
    model = ModelConfig(
        key="openai::gpt-5-mini",
        provider_id="openai",
        model_id="gpt-5-mini",
        type="llm",
    )
    resolved = ResolvedModel(
        key="openai::gpt-5-mini",
        provider_id="openai",
        model_id="gpt-5-mini",
        type="llm",
        name="GPT-5 Mini",
        api_key="test-key",
        base_url="https://api.example.test/v1",
    )

    assert provider.api_key_env == ""
    assert model.max_output == 4096
    assert model.extra_body == {}
    assert resolved.resolution_options == []
    assert resolved.duration_options == []
    assert resolved.supports_audio is False


def test_config_model_import_identities_stay_compatible():
    assert contracts.ProviderConfig is ProviderConfig
    assert contracts.ModelConfig is ModelConfig
    assert contracts.ResolvedModel is ResolvedModel
    assert config_models.ProviderConfig is ProviderConfig
    assert config_models.ModelConfig is ModelConfig
    assert config_models.ResolvedModel is ResolvedModel
    assert nori_config.ProviderConfig is ProviderConfig
    assert nori_config.ModelConfig is ModelConfig
    assert nori_config.ResolvedModel is ResolvedModel
