# LLM Kwargs Merge Immutability

## Background

`llms._merge_kwargs` injects model-level constraints into each request, including `temperature_fixed`, `max_output`, and provider-specific `extra_body`. The previous `extra_body` merge used `out.setdefault("extra_body", {}).update(...)`, which could mutate a caller-provided nested dict because `dict(kwargs)` only makes a shallow copy.

Hidden mutation at the gateway boundary is risky: retry logic, tests, or calling agents can reuse a kwargs dict and see provider-specific fields that were not present before the call.

## Decision

When model-level `extra_body` exists:

```python
caller_extra_body = out.get("extra_body") if isinstance(out.get("extra_body"), dict) else {}
extra_body = dict(caller_extra_body)
extra_body.update(model.extra_body)
out["extra_body"] = extra_body
```

This preserves the existing precedence where model-level fields override caller `extra_body`, but avoids mutating the caller's dict.

## Acceptance

- `_merge_kwargs` does not mutate caller-provided `extra_body`.
- Merged params receive model-level `extra_body`.
- Existing chat, JSON, image, capability, and telemetry tests continue to pass.

## Verification

- `python -m pytest tests/test_llms_call_json.py tests/test_llms_telemetry.py tests/test_llms_image_capabilities.py -q`
- `python -m pytest tests -q`
