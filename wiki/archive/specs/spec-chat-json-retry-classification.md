<!-- Last verified: 2026-05-24 | Current stage: P0 Documentation Hygiene -->

# Spec: Chat JSON Retry Classification

## Background

`chat_json(json_mode=True)` may retry once without `response_format` for providers that reject OpenAI-style JSON object mode. The fallback should not hide unrelated provider failures such as unsupported model access, account restrictions, or non-JSON capability errors.

## Goal

Keep JSON-mode fallback narrow and explainable:

- retry when the error mentions `response_format`;
- retry when the error mentions `json_object`;
- retry when the error is an unsupported JSON-mode error;
- do not retry unrelated `unsupported` errors.
- do not retry unrelated `TypeError` failures from caller/SDK internals.

## Non-Goals

- Do not remove JSON-mode fallback.
- Do not add provider-specific exception classes.
- Do not change the default `json_mode=False` behavior.

## Acceptance

- A response-format rejection retries once without `response_format`.
- A TypeError caused by an unexpected `response_format` kwarg retries once.
- `RuntimeError("model family unsupported for this account")` does not retry.
- `TypeError("object of type int has no len()")` does not retry.
- Retry behavior remains covered without live provider calls.

## Verification

- `python -m pytest tests/test_llms_call_json.py -q`
