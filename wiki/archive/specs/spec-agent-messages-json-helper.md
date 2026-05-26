# Agent Messages JSON Helper

## Background

`call_stage_json` covered required JSON stages that can be expressed as simple `system` + `user` text prompts. Intake vision tagging already builds OpenAI-style multimodal messages with text and `image_url` parts, so it still called `llms.chat_json` directly. That left JSON mode and domain-error translation outside the shared agent utility contract.

## Decision

Add `nori.agent_utils.call_stage_messages_json(...)` for required JSON stages with pre-built messages:

- accepts `messages`, `usage`, `timeout`, `error_type`, `chat_func`, and `chat_json_func`;
- calls `llms.chat_json(..., json_mode=True, _chat=chat_func)`;
- translates parse/provider failures into the supplied domain error type;
- is exported from `nori.agent_utils`.

`call_stage_json(...)` now delegates to `call_stage_messages_json(...)`, and Intake vision tagging uses it with `usage="vision"` and `IntakeVisionLLMError`.

## Acceptance

- Text and multimodal required JSON stages share the same JSON-mode contract.
- Intake vision still isolates per-image failures and returns empty image tags for failed images.
- Tests cover helper export, pre-built multimodal messages, and Intake vision `json_mode=True` routing.

## Verification

- `python -m pytest tests/test_agent_utils.py tests/test_gen_agents_intaker.py -q`
- `rg -n "llms\\.chat_json\\(" nori/gen_agents/intaker.py nori/ana_agents/xhs_note_analyzer.py`
