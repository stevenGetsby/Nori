# Spec: Front Pipeline Fallback Metadata

## Problem

Intake and account planning intentionally keep rule/structural fallback when optional LLM calls fail. Before this change, callers could not distinguish a deliberate no-LLM fallback from a failed LLM attempt, and the two agents still duplicated optional JSON-call behavior instead of using the shared fallback helper.

## Decision

Add optional metadata to front-pipeline result models:

- `IntakeResult.metadata`
- `AccountPlanResult.metadata`

Empty metadata is omitted from `to_dict()` to preserve existing compact fixtures. Optional LLM failure paths attach redacted metadata:

```python
metadata["llm_error"] = {
    "stage": "intake_text|account_planner",
    "reason": "parse_error|api_error",
    "error_type": "...",
    ...
}
```

Successful optional LLM enhancement records `metadata["llm_enhanced"] = True`.

Both Intake and AccountPlanner now route optional JSON stages through `nori.agent_utils.try_stage_json(...)`, so they request JSON mode consistently and share parse/provider failure handling.

## Acceptance

- Rule-only intake and account planning remain compact and do not serialize empty metadata.
- Intake LLM failure returns rule fallback with `metadata.llm_error`.
- AccountPlanner LLM failure returns structural fallback with `metadata.llm_error`.
- Successful optional LLM paths mark `metadata.llm_enhanced`.
- Default tests require no live LLM calls.

## Verification

- `tests/test_agent_models.py`
- `tests/test_gen_agents_intaker.py`
- `tests/test_gen_agents_account_planner.py`
- `python -m pytest tests -q`
