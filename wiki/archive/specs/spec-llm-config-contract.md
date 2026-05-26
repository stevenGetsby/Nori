<!-- Last verified: 2026-05-24 | Current stage: P0 Documentation Hygiene | Status: implemented -->

# Spec: LLM Config Contract

## Background

The status script repeatedly reports no `api_config.yaml`. Live LLM/image workflows require a local config, but secrets must not be committed. The config shape should be documented, example-driven, and covered by tests.

## Goal

Implement a redacted config contract for `nori.nori_config` and `llms`:

- Commit `api_config.example.yaml`.
- Keep `api_config.yaml` ignored.
- Support `api_key_env` and `${ENV_VAR}` so private keys can live in environment variables.
- Fail fast when explicit `NORI_CONFIG` points to a missing file.
- Test mode-specific `active_models`.
- Coerce model scalar fields from YAML before they reach `ResolvedModel`, including string booleans such as `"false"`.

## Contract

Provider shape:

```yaml
providers:
  openai:
    base_url: https://api.openai.com/v1
    api_key_env: OPENAI_API_KEY
```

Model key shape:

```yaml
models:
  openai::gpt-5-mini:
    type: llm
```

Mode-specific active models:

```yaml
active_models:
  direct:
    llm: openai::gpt-5-mini
  ghc:
    llm: ghc::gpt-5-mini
```

## Verification

- `tests/test_nori_config.py`
- `python -m pytest tests/test_nori_config.py -q`
- `python -m pytest tests -q`

## Follow-Up

Model parsing now uses shared coercion for booleans, integers, floats, lists, and dicts. This keeps config strings like `supports_vision: "false"` from enabling capabilities accidentally and protects `llms` guards from malformed option shapes. Numeric option fields also use shared integer-list coercion so scalar values such as `duration_options: "10"` restore as `[10]`.

Config structure validation now fails fast with `NoriConfigError` for non-mapping YAML top level, `providers`, `models`, and individual provider/model entries. This keeps malformed private configs from surfacing as generic loader `AttributeError`s or silently becoming empty provider/model config.

Active model selection now normalizes the selected `active_models` block before it reaches `resolve()`. Non-dict shapes and blank values become explicit missing-usage errors, scalar malformed keys become `ValueError: 无效模型键`, and a `NORI_MODE` override with no matching mode block clears the active map instead of silently using `direct`.

Active usage lookup now applies the same trimming rule to the queried usage key as it applies to configured usage keys, so `get_active(" llm ")` resolves `active_models.llm`.

Model key parsing now also requires both sides of `provider_id::model_id` to be non-blank after trimming. Keys such as `openai::` and `::gpt-5-mini` fail at config-parse time with `ValueError: 无效模型键` instead of leaking blank provider/model ids into client construction.

Model keys are now stored and resolved in canonical `provider::model` form. This prevents segment whitespace in YAML, such as `openai :: gpt-5-mini`, from making `resolve()` parse the provider successfully but miss the corresponding `ModelConfig` and fall back to default model fields.

Model resolution is now strict: `resolve()` requires the canonical key to exist in `models`. A configured provider without a matching model entry raises `KeyError: 未配置模型` instead of constructing a default `ResolvedModel` with implicit capabilities.

Provider ids and mode keys now follow the same canonicalization rule: provider ids are trimmed before storage/lookup, blank provider ids are rejected, and `mode`, `NORI_MODE`, and mode-block keys are trimmed before active model selection.

Provider API key environment variable names are also canonicalized. `api_key_env` is trimmed before lookup and stored in canonical form, and `${ ENV_VAR }` placeholders trim the inner variable name before calling `os.getenv`.

`llms.current_mode()`, `llms.set_mode(...)`, and `llms.ensure_ready(...)` now use the same trimmed runtime mode semantics. This keeps `NORI_MODE=" ghc "` from selecting the `ghc` active model block while skipping the `ghc` readiness proxy probe.

Model-level `extra_body` now has explicit runtime semantics across gateway paths: chat requests merge it through the chat kwargs helper, while OpenAI-compatible image requests merge it through an image-specific helper so image provider extensions do not inherit chat-only token/temperature arguments. Both paths copy caller `extra_body` before applying model fields.
