# Token Kwargs Normalization

## Background

`llms._merge_kwargs` maps model-level `max_output` into provider request parameters. GPT-5 models use `max_completion_tokens`, while older OpenAI-compatible chat models use `max_tokens`.

Mixed caller params can create avoidable provider errors:

```python
{"max_tokens": 123, "max_completion_tokens": 456}
```

The gateway should normalize this before provider dispatch, regardless of whether a model-level `max_output` default is configured.

## Decision

For GPT-5 models under `openai` or `ghc` providers:

- caller `max_completion_tokens` is authoritative;
- legacy `max_tokens` is removed when both are present;
- legacy `max_tokens` is converted when it is the only caller token limit;
- model `max_output` fills `max_completion_tokens` when neither caller param is present.

For other chat models:

- caller `max_tokens` is authoritative;
- `max_completion_tokens` is removed when both are present;
- `max_completion_tokens` is converted to `max_tokens` when it is the only caller token limit;
- model `max_output` fills `max_tokens` when neither caller param is present.

## Acceptance

- Chat request params never contain both `max_tokens` and `max_completion_tokens`.
- Explicit model-native token params are preserved.
- Opposite/legacy token params remain accepted by callers and are converted before dispatch.
- Normalization runs even when `model.max_output` is unset or zero.
- Full default suite passes.

## Verification

- `python -m pytest tests/test_llms_call_json.py tests/test_llms_telemetry.py tests/test_llms_image_capabilities.py tests/test_nori_config.py -q`
- `python -m pytest tests -q`
