# Analyzer Session JSON Helper Routing

## Background

`XHSNoteAnalyzer.collect_for_session` intentionally fails fast for session-level skill learning. It should not emit partial `NoteSkill` records when keyword generation or note labeling fails. Before this change, the keyword and label stages called `llms.chat_json` directly, so they did not share the same JSON-mode and error-translation contract used by required generation-agent stages.

## Decision

Route the required session LLM stages through `nori.agent_utils.call_stage_json(...)`:

- `_llm_generate_keywords(...)` uses `call_stage_json(..., timeout=30, error_type=XHSNoteAnalyzerLLMError)`.
- `_llm_label_notes(...)` uses `call_stage_json(..., timeout=120, error_type=XHSNoteAnalyzerLLMError)`.
- Both preserve package-level monkeypatching by passing `chat_func=llms.chat` and `chat_json_func=llms.chat_json`.
- Empty or incomplete label results remain explicit session validation errors.

## Acceptance

- Analyzer source has no direct `llms.chat_json(...)` calls.
- Required session JSON calls request `json_mode=True`.
- Keyword generation and label recognition keep their fail-fast behavior.
- Default tests remain offline and mocked.

## Verification

- `python -m pytest tests/test_ana_agents_xhs_note_analyzer.py tests/test_agent_utils.py -q`
- `rg -n "llms\\.chat_json\\(" nori/ana_agents/xhs_note_analyzer.py`
