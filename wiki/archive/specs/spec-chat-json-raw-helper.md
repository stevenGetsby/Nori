# Spec: Chat JSON Raw Helper

## Problem

Structured LLM helpers such as intent extraction and edit-target selection need both parsed JSON and the original model text for debug and structured error reporting. Before this change, each helper wrapped `chat` locally just to capture raw text, duplicating retry-sensitive plumbing around `chat_json`.

## Decision

Add a first-class gateway helper:

```python
llms.chat_json_with_raw(...) -> tuple[dict[str, Any], str]
```

It shares `chat_json` semantics:

- default behavior does not inject `response_format`;
- `json_mode=True` requests JSON object mode;
- provider rejection of JSON mode retries once without `response_format` by default;
- parse failures raise `ChatJSONError` with the raw model text attached.

`llms.chat_json(...)` now delegates to this helper and returns only the parsed data.

## Acceptance

- Existing `chat_json` callers keep the same public return value.
- `chat_json_with_raw` returns parsed data and the exact successful raw text.
- JSON-mode retry behavior is shared between both helpers.
- `IntentLLMResult.raw` and `TargetSelectionResult.raw` are populated through the shared helper.
- No live LLM calls are required for default tests.

## Verification

- `tests/test_llms_call_json.py`
- `tests/test_llms_intent_target_helpers.py`
- `python -m pytest tests -q`
