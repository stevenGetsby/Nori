# Shared LLM Error Metadata Helper

## Background

Optional LLM stages now return redacted failure metadata through `try_stage_json`, but each fallback agent had its own local `_attach_llm_error` helper. The duplicated helpers used the same shape today, but future changes could drift across Intake, AccountPlanner, and ops planners.

## Decision

Add `nori.agent_utils.attach_llm_error(target, stage, error)` as the canonical formatter:

```python
target["llm_error"] = {
    **dict(error),
    "stage": stage,
}
```

`target` can be an agent result `metadata` dict or an analyzer `validation` dict. The caller-provided `stage` is written last so malformed error metadata cannot override the authoritative stage.

## Acceptance

- `attach_llm_error` is exported from `nori.agent_utils`.
- Intake, AccountPlanner, OperationPlanner, KPIPlanner, CalendarPlanner, and `XHSNoteAnalyzer.analyze_note` fallback use the shared helper.
- No local `_attach_llm_error` helper remains in `nori/`.
- Existing fallback tests keep passing, and `tests/test_agent_utils.py` covers the shared field shape plus stage authority.

## Verification

- `rg -n "def _attach_llm_error|_attach_llm_error\\(" nori tests`
- `python -m pytest tests/test_agent_utils.py tests/test_gen_agents_intaker.py tests/test_gen_agents_account_planner.py tests/test_ops_agents_operation_planner.py tests/test_ops_agents_kpi_planner.py tests/test_ops_agents_calendar_planner.py -q`
