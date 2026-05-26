# Spec: Analyzer Fallback Observability

## Problem

`XHSNoteAnalyzer.analyze_note` intentionally keeps a rule-based seed-skill draft when optional LLM enhancement fails. Before this change, the fallback stored `validation["llm_error"]` as a raw exception string, which mixed provider messages with validation data and did not align with the structured `try_stage_json` fallback contract used elsewhere.

## Decision

Route single-note LLM enhancement through `nori.agent_utils.try_stage_json(...)`.

On failure, keep the existing rule fallback and attach:

```python
validation["llm_error"] = {
    "stage": "xhs_note_analyzer",
    "reason": "parse_error|api_error",
    "error_type": "...",
    ...
}
```

Session-level skill learning still remains fail-fast because clustering and labels require LLM output by design.

## Acceptance

- Single-note analyzer LLM success still produces `validation.llm_enhanced=true`.
- Single-note analyzer LLM failure returns a rule draft with `llm_enhanced=false`.
- Failure metadata is structured and redacted enough for logs/docs.
- Session skill learning behavior is unchanged.
- Default tests require no live LLM.

## Verification

- `tests/test_ana_agents_xhs_note_analyzer.py`
- `python -m pytest tests -q`
