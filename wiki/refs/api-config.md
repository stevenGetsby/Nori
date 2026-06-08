<!-- Last verified: 2026-05-24 | Current stage: P0 Documentation Hygiene -->

# API Config Reference

## Purpose

`api_config.yaml` is the private runtime config for `nori.nori_config` and `nori.core.llms`. It selects providers and active models for LLM, vision, and image usage. The repository should only commit redacted examples such as `api_config.example.yaml`. Import the runtime gateway through `nori.core.llms`; the old top-level `llms/` compatibility package has been removed.

## Files

| File | Commit? | Purpose |
| --- | --- | --- |
| `api_config.example.yaml` | Yes | Redacted template with provider/model/active model shape. |
| `api_config.yaml` | No | Local private runtime config. Ignored by `.gitignore`. |
| External config via `NORI_CONFIG` | No | Preferred for machine-specific or secret-managed configs. |

## Lookup Order

```text
NORI_CONFIG
-> ./api_config.yaml
-> nori/api_config.yaml
-> repo_root/api_config.yaml
```

If `NORI_CONFIG` is set and points to a missing file, `NoriConfig` fails fast instead of silently falling back to another config.

The YAML top level must be a mapping. Core `providers` and `models` sections, when present, must also be mappings, and each `providers.<id>` / `models.<key>` entry must be a mapping. Invalid structural shapes raise `NoriConfigError` instead of leaking generic Python errors such as `AttributeError` or silently becoming empty config.

## Provider Shape

```yaml
providers:
  openai:
    base_url: https://api.openai.com/v1
    api_key_env: OPENAI_API_KEY
```

Rules:

- Provider ids are trimmed and stored canonically. Blank provider ids are rejected with `ValueError: 无效服务商 id`.
- Prefer `api_key_env` so the YAML contains no secrets. The environment variable name is trimmed before lookup and stored canonically.
- `api_key: ${OPENAI_API_KEY}` is also supported for compatibility; whitespace inside `${ ... }` is ignored when resolving the environment variable name.
- Literal `api_key` works but should only appear in ignored local files.
- `api_key` and `base_url` must resolve to non-blank strings before `nori.core.llms.client` constructs an OpenAI-compatible SDK client.
- `base_url` should be OpenAI-compatible for `nori.core.llms.client`.
- Live image generation uses the active `image` model's provider. If `active_models.direct.image` points at `relay::gpt-image-2`, the `relay` provider must resolve a real key and base URL; leaving the example `https://your-relay.example.com/v1` or an unset `RELAY_API_KEY` will fail before provider dispatch.

## Model Shape

```yaml
models:
  openai::gpt-5-mini:
    type: llm
    name: GPT-5 Mini
    max_output: 4096
    supports_vision: true
    temperature_fixed: 1
```

Model keys must use `provider_id::model_id`; both sides must be non-blank after trimming. Nori stores model keys in canonical `provider::model` form after parsing, so YAML such as `openai :: gpt-5-mini` still resolves to `openai::gpt-5-mini` and retains its `ModelConfig`. `resolve()` requires both a matching `providers.<provider_id>` and a matching `models.<provider_id::model_id>` entry; missing providers or models raise explicit `KeyError`s instead of constructing a default model.

Scalar cleanup:

| Field kind | Contract |
| --- | --- |
| Numeric fields such as `context_window`, `max_output`, `temperature_fixed`, and `duration_options` | String numbers are accepted and coerced; scalar option values are treated as single-item lists; invalid option values are dropped. |
| Boolean capability flags such as `supports_vision`, `supports_reference_image`, and `supports_audio` | YAML booleans and common strings such as `"true"` / `"false"` are parsed through shared coercion, so `"false"` does not become truthy. |
| List/dict fields such as `resolution_options` and `extra_body` | Non-list or non-dict values are normalized to the safe default shape. |

Runtime merge rule:

- Chat requests merge model-level `extra_body` through the chat kwargs path, together with token/temperature normalization.
- OpenAI-compatible image requests merge model-level `extra_body` through an image-specific kwargs path, so image adapters can receive provider extensions without inheriting chat-only token/temperature fields.
- Caller-provided `extra_body` is copied before model-level fields are applied; the caller's dict is not mutated.

Image model capability flags:

```yaml
models:
  relay::gpt-image-2:
    type: image
    resolution_options: ["1072x1440", "1024x1024"]
    supports_reference_image: true
```

`nori.core.llms.image(reference_images=...)` checks `supports_reference_image` before calling the provider SDK. If the active image model does not support reference images, it raises `ImageCapabilityError` instead of failing later inside provider-specific code.

Video/audio capability flags are preserved on resolved models for future adapters:

```yaml
models:
  relay::video-gen:
    type: video
    duration_options: [5, 10]
    supports_audio: true
```

`nori.core.llms.image(...)` requires the active model to have `type: image`; using an LLM/video model for image usage raises `ImageCapabilityError` before provider dispatch.

## Active Models

Flat shape is supported for one mode:

```yaml
active_models:
  llm: openai::gpt-5-mini
  image: relay::gpt-image-2
```

Mode-specific shape is preferred:

```yaml
mode: direct
active_models:
  direct:
    llm: openai::gpt-5-mini
    image: relay::gpt-image-2
  ghc:
    llm: ghc::gpt-5-mini
    image: relay::gpt-image-2
```

`mode`, `NORI_MODE`, and mode block keys are trimmed before lookup. `NORI_MODE` overrides `mode` and selects the matching `active_models.<mode>` block. `nori.core.llms.current_mode()`, `nori.core.llms.set_mode(...)`, and `nori.core.llms.ensure_ready(...)` use the same trimmed mode value, so readiness checks and active model selection do not diverge when environment variables contain surrounding whitespace.

Active model values are normalized before resolution:

- Usage keys and model keys are trimmed strings.
- `get_active(usage)` trims the queried usage key before lookup, matching the normalization applied to configured usage keys.
- Valid model keys are canonicalized to `provider::model` before `active_summary` and `resolve()`.
- Active model values must point to declared `models.<provider::model>` entries. Unknown model keys raise `KeyError: 未配置模型`.
- Blank model keys are ignored, so `get_active("llm")` raises `KeyError: active_models.llm` instead of resolving an empty model.
- Non-dict `active_models` shapes normalize to an empty map and produce the same missing-usage error.
- Non-blank scalar model keys such as `123` are stringified, then rejected by `parse_model_key()` with `ValueError: 无效模型键`.
- Half-empty model keys such as `openai::` and `::gpt-5-mini` are rejected by `parse_model_key()` with `ValueError: 无效模型键`.
- If `NORI_MODE` selects a mode that has no block in a mode-specific config, the active map is empty; the loader does not silently reuse `direct`.

## Validation Commands

```bash
python -m pytest tests/test_nori_config.py -q
python - <<'PY'
from nori.nori_config import NoriConfig
cfg = NoriConfig()
print(cfg.config_path)
print(cfg.mode)
print(cfg.active_summary)
PY
```

`nori.core.llms.validate_api_key(...)` is the shared runtime validator for provider API keys, including native Google image calls. `nori.core.llms.validate_client_config(...)` extends it for OpenAI-compatible clients by also requiring `base_url`. `nori.core.llms.ensure_ready("llm")`, `nori.core.llms.get_client(...)`, and `nori.core.llms.get_async_client(...)` all fail with `LLMClientConfigError` when required config is blank. In trimmed `ghc` mode, `ensure_ready(...)` also probes `{base_url}/models`.

Minimal live smoke commands:

```bash
python -m pip install 'socksio>=1.0.0'  # only needed when the local proxy is SOCKS-backed

python - <<'PY'
import nori.core.llms as llms
print(llms.chat([
    {"role": "system", "content": "Reply with exactly: Nori live check OK"},
    {"role": "user", "content": "Run a minimal live connectivity check."},
], usage="llm", timeout=30))
PY

python - <<'PY'
import nori.core.llms as llms
images = llms.image(
    "Nori image API smoke test: a white flower on a clean table, no text.",
    usage="image",
    size="1024x1024",
)
print(len(images), str(images[0])[:30])
PY
```
