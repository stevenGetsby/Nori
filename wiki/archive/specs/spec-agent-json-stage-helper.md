# Spec: Agent JSON Stage Helper

## Problem

Generation agents had repeated local wrappers around `llms.chat_json`:

- each agent rebuilt the same system/user message list;
- each agent manually translated `ChatJSONError` into its domain exception;
- JSON-producing stages did not consistently opt into gateway JSON mode;
- tests depended on package-level `llms.chat` monkeypatching, so any shared helper had to preserve that seam.

## Decision

Add `nori.agent_utils.call_stage_json(...)` as the shared helper for generation-agent JSON stages.

The helper:

- calls `llms.chat_json(..., json_mode=True, _chat=llms.chat)` by default;
- accepts injected `chat_func` / `chat_json_func` for module-level monkeypatching and focused tests;
- translates parse failures into `error_type("LLM 输出无法解析为 JSON: ...")`;
- translates provider failures into `error_type("llms.chat 失败: ...")`;
- keeps caller modules responsible for stage-specific validation after JSON parsing.

`NoteMakerAgent` and `CoverDirectorAgent` now use the helper while preserving their existing domain exception classes.

## Acceptance

- `NoteMakerAgent` JSON stages route through the shared helper and still raise `NoteMakerLLMError`.
- `CoverDirectorAgent` JSON stages route through the shared helper and still raise `CoverDirectorError`.
- Tests can still monkeypatch each agent module's `llms.chat` / `llms.chat_json`.
- Default tests require no live LLM or image calls.

## Verification

- `tests/test_agent_utils.py`
- `tests/test_gen_agents_note_maker.py`
- `tests/test_gen_agents_cover_director.py`
- `python -m pytest tests -q`
