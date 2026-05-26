# Spec: Ops Planner LLM Fallback Observability

## Problem

Operation, KPI, and calendar planners intentionally keep deterministic fallback when optional LLM calls fail. That behavior is correct for default reliability, but the failure reason was previously swallowed. A caller could see `planner=rule_fallback` without knowing whether the LLM was disabled, returned invalid JSON, or hit a provider/runtime error.

The three planners also duplicated optional JSON-call plumbing and did not consistently request gateway JSON mode.

## Decision

Add `nori.agent_utils.try_stage_json(...)` for optional JSON LLM stages.

The helper:

- calls `llms.chat_json(json_mode=True, _chat=llms.chat)`;
- returns `(data, None)` on success;
- returns `(None, error)` on parse/provider failure without raising;
- keeps error metadata redacted: stage callers add stage name, while the helper records reason, error type, preview/message only.

OperationPlanner, KPIPlanner, and CalendarPlanner now use this helper. On LLM failure they keep deterministic fallback and attach:

```python
metadata["llm_error"] = {
    "stage": "...",
    "reason": "parse_error|api_error",
    "error_type": "...",
    ...
}
```

## Acceptance

- `use_llm=True` success paths still produce `planner=llm_with_fallback`.
- Invalid LLM JSON still falls back instead of raising.
- Fallback artifacts record `metadata.llm_error.stage` and `metadata.llm_error.reason`.
- Mocked LLM tests verify JSON mode is requested.
- Default tests require no live LLM.

## Verification

- `tests/test_agent_utils.py`
- `tests/test_ops_agents_operation_planner.py`
- `tests/test_ops_agents_kpi_planner.py`
- `tests/test_ops_agents_calendar_planner.py`
- `python -m pytest tests -q`
