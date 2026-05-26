<!-- Last verified: 2026-05-24 | Current stage: P0 Generation Core -->

# Spec: LLM JSON Helper Contract

## Background

`llms.intent_extractor` and `llms.target_selector` each carried their own response-format retry and JSON parsing logic. That duplicated gateway behavior and made provider compatibility harder to reason about.

## Goal

Move JSON-mode retry behavior into `llms.call.chat_json` while preserving the current default behavior:

- default `chat_json(...)` does not inject `response_format`;
- callers can request `json_mode=True`;
- when JSON mode is rejected because of `response_format` / `json_object` / unsupported provider behavior, retry once without `response_format`;
- intent and target helpers use the shared parser and keep structured-result failure semantics.

## Acceptance

- `chat_json(json_mode=True)` passes `response_format={"type": "json_object"}` on the first call.
- Provider rejection of JSON mode triggers a second call without `response_format`.
- Retry can be disabled with `retry_without_response_format=False`.
- `extract_intent()` filters unsupported fields/enums and returns `IntentLLMResult.error` instead of throwing.
- `select_edit_target()` validates the selector whitelist and filters alternatives.
- All behavior is covered by offline tests.

## Implemented Files

- `llms/call.py`
- `llms/intent_extractor.py`
- `llms/target_selector.py`
- `tests/test_llms_call_json.py`
- `tests/test_llms_intent_target_helpers.py`
- `llms/README.md`
- `wiki/30-api-reference.md`
- `wiki/60-stage-generation-core.md`
- `wiki/85-backlog.md`
