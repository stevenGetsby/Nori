# Spec: Chat And Vision Capability Guard

## Problem

`llms.chat` could route requests to any active model returned by config. A misconfigured `active_models.llm` or `active_models.vision` could send text chat to an image model, or send multimodal messages to a text-only model, leaving provider SDKs to fail with inconsistent errors.

## Decision

Move chat capability enforcement into the `llms` gateway:

- text chat accepts active models with `type=llm` or `type=vision`;
- `usage="vision"` requires `supports_vision=true`;
- multimodal message parts require `supports_vision=true`;
- invalid requests raise `ChatCapabilityError` before provider SDK dispatch;
- failed capability checks still emit redacted telemetry if a sink is registered.

## Acceptance

- `llms.chat(...)` rejects active models whose resolved `type` is not `llm` or `vision`.
- `llms.chat(..., usage="vision")` rejects models without `supports_vision`.
- `llms.chat(...)` rejects messages containing `image_url`, `input_image`, or `image` parts when the model lacks `supports_vision`.
- Valid vision models still dispatch through the normal chat completion path.
- Telemetry failure records include `error_type=ChatCapabilityError` and no prompt/message payload.

## Verification

- `tests/test_llms_telemetry.py`
- `python -m pytest tests -q`
