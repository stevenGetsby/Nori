<!-- Last verified: 2026-05-24 | Current stage: P0 Generation Core -->

# Spec: LLM Telemetry Hook

## Background

Model-call failures were visible only through caller-specific exceptions and scattered logs. The gateway needed a small, redacted telemetry seam without coupling `llms` to a logging backend.

## Goal

Add a process-local telemetry hook that:

- records `chat`, `achat`, and `image` success/failure metadata;
- excludes prompts, messages, response text, API keys, image bytes, and provider payloads;
- preserves existing exception behavior;
- ignores telemetry sink failures.

## Contract

Public API:

```python
from llms import set_telemetry_sink

set_telemetry_sink(lambda record: ...)
set_telemetry_sink(None)
```

Record fields:

- `operation`
- `usage`
- `model_key`
- `provider_id`
- `model_id`
- `duration_ms`
- `success`
- `error_type` only on failure

## Acceptance

- Successful chat calls emit redacted metadata.
- Failed chat calls emit `success=false` and `error_type`, then re-raise the original exception.
- A broken telemetry sink does not break the model call.
- Image calls use the same metadata shape.

## Implemented Files

- `llms/call.py`
- `llms/__init__.py`
- `tests/test_llms_telemetry.py`
- `llms/README.md`
- `wiki/30-api-reference.md`
- `wiki/60-stage-generation-core.md`
- `wiki/85-backlog.md`
