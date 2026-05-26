from __future__ import annotations

from nori import config_models
from nori import nori_config


def test_config_model_dataclasses_live_in_dedicated_boundary():
    provider = config_models.ProviderConfig(
        id="openai",
        base_url="https://api.example.test/v1",
        api_key="test-key",
    )
    model = config_models.ModelConfig(
        key="openai::gpt-5-mini",
        provider_id="openai",
        model_id="gpt-5-mini",
        type="llm",
    )
    resolved = config_models.ResolvedModel(
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


def test_nori_config_reexports_config_model_identities_for_compatibility():
    assert nori_config.ProviderConfig is config_models.ProviderConfig
    assert nori_config.ModelConfig is config_models.ModelConfig
    assert nori_config.ResolvedModel is config_models.ResolvedModel
