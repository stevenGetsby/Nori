<!-- Last verified: 2026-05-24 | Current stage: P0 Generation Core -->

# Spec: Image Reference Capability Guard

## Background

`ModelConfig` already had `supports_reference_image`, but `llms.image(reference_images=...)` did not enforce it. Unsupported reference-image requests could reach provider SDKs and fail with provider-specific errors after partial request construction.

## Goal

Move capability enforcement into the `llms` gateway:

- text-to-image requests should not require reference-image capability;
- reference-image requests should be allowed only when the active image model has `supports_reference_image=true`;
- unsupported requests should fail with a stable `ImageCapabilityError` before provider dispatch;
- behavior should be covered by offline tests.

## Acceptance

- `llms.image(prompt)` still calls `images.generate` when no valid reference bytes are present.
- `llms.image(prompt)` rejects active models whose resolved `type` is not `image`.
- `llms.image(prompt, reference_images=[...])` raises `ImageCapabilityError` when the model lacks `supports_reference_image`.
- Supported reference-image requests still route to provider-specific edit/generate path.
- `api_config.example.yaml` and `wiki/refs/api-config.md` document the flag.

## Implemented Files

- `llms/call.py`
- `llms/__init__.py`
- `tests/test_llms_image_capabilities.py`
- `api_config.example.yaml`
- `llms/README.md`
- `wiki/refs/api-config.md`
- `wiki/30-api-reference.md`
- `wiki/60-stage-generation-core.md`
- `wiki/85-backlog.md`
