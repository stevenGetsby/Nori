<!-- Last verified: 2026-05-24 | Current stage: P0 Documentation Hygiene -->

# Spec: Embedded JSON Object Parsing

## Background

`llms.parse_json_object` accepts model responses that contain a JSON object inside prose. The old embedded fallback used a greedy brace regex, so text like `Draft {placeholder}\n{"ok": true}` or `{"a": 1}\n{"b": 2}` could be rejected even though the response contained a usable object.

## Goal

Make embedded JSON parsing deterministic and tolerant of common LLM output noise:

- keep accepting complete JSON object responses;
- keep accepting fenced JSON blocks;
- parse the first valid embedded JSON object;
- ignore invalid brace spans before the first valid object;
- preserve `ChatJSONError.raw` behavior on failure.

## Non-Goals

- Do not accept non-object JSON as a successful result.
- Do not change JSON-mode request or retry behavior.
- Do not add provider-specific parsing branches.

## Acceptance

- `parse_json_object('Draft {placeholder}\n{"ok": true}\nDone.') == {"ok": True}`.
- `parse_json_object('First: {"a": 1}\nSecond: {"b": 2}') == {"a": 1}`.
- Existing fenced, embedded, invalid, and non-object tests still pass.

## Verification

- `python -m pytest tests/test_llms_call_json.py -q`
