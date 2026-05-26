<!-- Last verified: 2026-05-24 | Current stage: P1 Account-Ops Backend -->

# Stage 60: Generation Core

## Goal

Stabilize the executable XHS generation chain:

```text
UserInput(text/images)
-> IntakeResult(intention/context/assets)
-> NoteDraft(title/body/tags/asset bundle)
-> CoverResult(cover image path/prompt/reference paths)
```

## Current Flow

| Step | Module | Status | Output |
| --- | --- | --- | --- |
| 1. Input orchestration | `nori/user_profiling/intaker/intaker.py` | Implemented | `IntakeResult` |
| 2. Text intake normalization | `nori/user_profiling/intaker/normalizer.py` | Implemented | intention/context/missing/questions |
| 3. Vision tagging | `nori/user_profiling/intaker/image_tagger.py` | Implemented | `UserAsset` with `vision_*` fields |
| 4. Skill selection | `nori/content_generation/note_maker/skill_picker.py` | Implemented | chosen `NoteSkill` |
| 5. Asset curation | `nori/content_generation/note_maker/asset_curator.py` | Implemented | `AssetBundle` |
| 6. Note composition | `nori/content_generation/note_maker/note_composer.py` | Implemented | `NoteDraft` |
| 7. Cover reference selection | `nori/content_generation/cover_director/refs.py` | Implemented | reference image paths |
| 8. Cover prompt writing | `nori/content_generation/cover_director/prompts.py` | Implemented | image prompt |
| 9. Cover image call | `CoverDirectorAgent` | Implemented | image payload |
| 10. Cover image output | `nori/content_generation/cover_director/output.py` | Implemented | `CoverResult.cover_path` |

## Contracts

| Contract | Source |
| --- | --- |
| `UserInput`, `IntakeResult` | `nori/user_profiling/models.py`; front-pipeline inputs/results support `to_dict()` / `from_dict()` round trips. |
| `UserAsset` | `nori/core/models.py`; cross-stage asset contract produced by Intake and consumed by NoteMaker/CoverDirector/ContentProducer. `nori.content_generation.models` re-exports the same class for existing generation call sites. |
| `AssetBundle`, `CandidateTitle`, `NoteDraft` | `nori/content_generation/models.py`; generation artifacts support `to_dict()` / `from_dict()` round trips, and `UserAsset.from_dict()` is the canonical dict-asset normalization path for NoteMaker/ContentProducer. |
| `CoverResult` | `nori/content_generation/models.py`; cover artifacts support `to_dict()` / `from_dict()` round trips. |
| `NoteSkill` | `nori/market_analysis/models.py` |
| `load_note_skills`, `write_note_skill_fixture` | `nori/market_analysis/note_skill_fixture.py` |

## Agent Boundaries

| Agent | Owns | Must not own |
| --- | --- | --- |
| Intake | Text normalization, image vision tags, missing questions. | Account strategy, note copy, image generation. |
| NoteMaker | Skill pick, asset bundle, title/body/tags. | Raw image reading, cover rendering, account planning. |
| CoverDirector | Reference selection for cover, prompt writing, image generation. | Body copy, skill learning, platform publishing. |

## LLM Failure Policy

| Component | Failure behavior |
| --- | --- |
| Intake text LLM | Rule fallback. |
| Intake per-image vision | Warn/skip image tag; do not abort whole intake. |
| NoteMaker LLM stages | Raise `NoteMakerLLMError`. |
| CoverDirector LLM/image stages | Raise `CoverDirectorError`. |
| AccountPlanner | Structural fallback. |

## LLM Helper Contracts

| Helper | Contract |
| --- | --- |
| `llms.chat(...)` / `llms.achat(...)` | Public facades over `llms.chat_runner.chat_text` / `achat_text`, which check active model type through `llms.capabilities.ensure_chat_capability` before provider dispatch. Text chat accepts `type=llm` or `type=vision`; `usage="vision"` and multimodal message parts require `supports_vision=true`, otherwise `ChatCapabilityError`. Provider response text normalization lives in `llms.results.extract_chat_text`; empty text content, empty `choices`, or missing `message.content` raise `ChatResultError` instead of leaking empty success or low-level shape errors. |
| `llms.chat_json(..., json_mode=True)` | Requests JSON object mode but retries once without `response_format` when a provider rejects JSON mode. Retry classification is limited to `response_format`, `json_object`, or JSON-specific unsupported errors so unrelated provider failures are not hidden. Default `json_mode=False` remains unchanged for broad provider compatibility. |
| `llms.chat_json_with_raw(...)` | Uses the same JSON-mode retry contract as `chat_json`, and returns `(data, raw)` so structured helpers can retain original model text without duplicating `chat` wrappers. |
| `llms.json_calls.*` | Canonical JSON-mode raw-call and retry plumbing. It owns `response_format` fallback classification and copies request params before retrying. |
| `llms.parse_json_object(...)` | Accepts whole-object, fenced, and embedded JSON. Embedded parsing scans for the first valid JSON object instead of using greedy brace matching, so extra prose or later objects do not invalidate an otherwise usable first object. Implementation lives in `llms.json_parser`, while package and `llms.call` imports keep the same function identity. |
| `llms.current_mode()` / `llms.set_mode(...)` / `llms.ensure_ready(...)` | Use a trimmed runtime mode value so `NORI_MODE=" ghc "` selects the same active block and readiness probe path as `NoriConfig`. |
| `nori.shared.call_stage_json(...)` | Shared generation-stage wrapper around `llms.chat_json(json_mode=True)` that preserves injected chat functions and raises the caller's domain exception type. |
| `nori.shared.call_stage_messages_json(...)` | Shared required-stage wrapper for pre-built messages, including Intake vision's multimodal `usage="vision"` JSON tagging call. |
| `nori.shared.try_stage_messages_json(...)` | Shared optional-stage wrapper for pre-built messages, including future multimodal/custom-message fallback paths. It returns `(data, error)` instead of raising so deterministic fallbacks can continue. Parse failures reuse the same `empty_response` / `parse_error` classification as optional `llms` structured helpers. |
| `nori.shared.try_stage_json(...)` | System/user convenience wrapper over `try_stage_messages_json(...)` for optional-stage JSON stages. |
| `nori.shared.attach_llm_error(...)` | Shared formatter for optional fallback `llm_error` fields, used by Intake, AccountPlanner, ops planners, and analyzer fallbacks to avoid local shape drift. |
| `nori.user_profiling.intaker.normalizer.*` | Intake text boundary. It owns deterministic text fallback, optional text-LLM output normalization, allowed vocabulary/alias mapping, image context construction, and missing/question repair; `IntakeAgent` only decides whether to call text LLM and vision tagging. |
| `nori.user_profiling.intaker.image_tagger.*` | Intake vision boundary. It owns per-image multimodal JSON prompt construction, parallel dispatch, per-image failure isolation, and tag vocabulary filtering; `IntakeAgent` only decides when to use vision tagging. |
| `nori.content_generation.note_maker.skill_picker.*` | NoteMaker skill-selection boundary. It owns compact candidate summary construction, the skill-picker JSON prompt, and unknown-skill error translation; `NoteMakerAgent` only decides whether a picker call is needed. |
| `nori.content_generation.note_maker.asset_curator.*` | NoteMaker asset boundary. It owns asset-curation JSON prompt construction, selected-index normalization, text bucket cleanup, and cover/gallery path selection; `NoteMakerAgent` only orchestrates skill pick -> asset bundle -> note composition. |
| `nori.content_generation.note_maker.note_composer.*` | NoteMaker composition boundary. It owns note-composition JSON prompt construction, candidate title/tag/validation normalization, and missing title/body domain-error translation; `NoteMakerAgent` only turns composed fields into `NoteDraft`. |
| `nori.content_generation.cover_director.refs.*` | CoverDirector reference boundary. It owns tagged-asset prompt construction, chosen-index normalization, existing-image filtering, dedupe/cap policy, and legacy draft/reference-asset path collection; `CoverDirectorAgent` keeps the wrapper for domain error translation and image-stage orchestration. |
| `nori.content_generation.cover_director.prompts.*` | CoverDirector prompt boundary. It owns image-prompt JSON construction from draft asset facts, skill rules, intent, and selected reference count; `CoverDirectorAgent` only injects the JSON stage and passes the resulting prompt to image generation. |
| `nori.content_generation.cover_director.output.*` | CoverDirector output boundary. It owns data-uri decoding, remote image download, filename sanitization, and persistence errors; `CoverDirectorAgent` only passes the first image payload and records the resulting path. |
| `llms.request_params.merge_chat_kwargs(...)` | Canonical chat gateway merge for model constraints. It copies caller `extra_body` before applying model-level defaults and always normalizes token-limit kwargs so each model sends only its expected parameter, even when no `max_output` default is configured. |
| `llms.request_params.merge_image_kwargs(...)` | Canonical image request merge for model-level `extra_body` without inheriting chat-only token/temperature fields. |
| `llms.image(..., reference_images=...)` | Checks active model type and reference-image capability through `llms.capabilities.ensure_image_capability`; invalid image usage raises `ImageCapabilityError`. OpenAI-compatible image requests also merge model-level `extra_body` without mutating caller kwargs, but do not inherit chat-only token/temperature fields. Provider response normalization lives in `llms.results.collect_image_results`; responses with no usable URL/base64 image raise `ImageResultError` instead of returning an empty success. |
| `llms.image_inputs.*` | Canonical reference-image input helpers. `load_image_bytes(...)` normalizes bytes, data-uri, local path, and base64 string inputs while returning empty bytes for invalid/remote values; `sniff_mime(...)` and `bytes_to_data_uri(...)` build provider payloads. |
| `llms.image_providers.*` | Canonical provider-specific image helpers. OpenAI-compatible edit, relay reference-payload retry, and Google native image generation live here. |
| `llms.structured_outputs.*` | Canonical cleanup and parse-error classification for optional structured LLM helpers. |
| `llms.set_telemetry_sink(...)` | Emits redacted metadata for `chat` / `achat` / `image`; prompt, messages, keys, image bytes, and response text are excluded. Implementation lives in `llms.telemetry`, while package and `llms.call` imports keep the same function identity. |
| `llms.extract_intent(...)` | Returns `IntentLLMResult` with filtered fields/candidates and structured `error`; no live failure should escape to callers. |
| `llms.select_edit_target(...)` | Returns `TargetSelectionResult`, validates selector whitelist, and filters alternatives to known selectors. |

Fallback metadata:

| Result | Contract |
| --- | --- |
| `IntakeResult.metadata.llm_error` | Present when optional text-intake LLM fails and rule fallback is used. |
| `AccountPlanResult.metadata.llm_error` | Present when optional account-planning LLM fails and structural fallback is used. |
| `XHSSeedSkillDraft.validation.llm_error` | Present when optional single-note analyzer LLM enhancement fails and rule fallback is used. |
| `*.metadata.llm_enhanced` | Present on successful optional LLM enhancement for intake/account planning. |

## Verification

| Test | Purpose |
| --- | --- |
| `tests/test_user_profiling_intaker_normalizer.py` | Deterministic text fallback, optional LLM output alias normalization, image context repair, missing/question fallback, and metadata preservation. |
| `tests/test_user_profiling_intaker.py` | Text/image intake, fallback metadata, mocked vision, and multimodal JSON helper routing through the image-tagger boundary. |
| `tests/test_user_profiling_intaker_image_tagger.py` | Vision tag filtering, no-vision asset construction, and single-image multimodal JSON helper routing. |
| `tests/test_content_generation_note_maker_skill_picker.py` | Compact skill-summary prompt contract and unknown skill-id domain error translation. |
| `tests/test_content_generation_note_maker_asset_curator.py` | Asset-curation prompt contract, selected-index normalization, empty-asset skip, and cover/gallery path selection. |
| `tests/test_content_generation_note_maker_note_composer.py` | Note-composition prompt contract, field normalization, fallback candidate title, and missing title/body domain error translation. |
| `tests/test_content_generation_note_maker.py` | Skill selection, asset curation, note composition behavior. |
| `tests/test_shared_utils.py` | Shared `call_stage_json` / `call_stage_messages_json` / `try_stage_messages_json` / `try_stage_json` routing, error translation/classification, and utility exports. |
| `tests/test_note_skill_fixture.py` | Learned skill fixture loading into NoteMaker-compatible `NoteSkill` objects. |
| `tests/test_content_generation_cover_director_refs.py` | Cover reference path collection, tagged-asset prompt contract, selected-index normalization, missing-path filtering, dedupe, and reference caps. |
| `tests/test_content_generation_cover_director_prompt.py` | Cover prompt JSON-call contract, asset fact/text-point summarization, reference-count context, and empty prompt domain errors. |
| `tests/test_content_generation_cover_director_output.py` | Cover output persistence for data-uri/http payloads, safe filename construction, user-agent download requests, and output domain errors. |
| `tests/test_content_generation_cover_director.py` | Reference selection, shared JSON prompt routing, prompt generation, image output path handling. |
| `tests/test_domain_model_contracts.py` | Front-pipeline and generation artifact serialization plus `from_dict()` restoration for intake/account-plan/note/cover snapshots. |
| `tests/test_llms_call_json.py` | JSON parser and request-param helper import identity, embedded first-object extraction, raw capture, usage/kwargs propagation, JSON-mode retry behavior and retry classification, side-effect-free model kwargs merging, and token-limit parameter normalization. |
| `tests/test_llms_mode.py` | Runtime mode normalization, config validation reuse, and offline `ghc` readiness probing. |
| `tests/test_llms_intent_target_helpers.py` | Intent extraction, edit-target selector, and shared structured-output helper contracts without live LLM. |
| `tests/test_llms_image_capabilities.py` | Image reference capability guard, image result normalization, image input/provider helper aliases, provider helper behavior, and image request kwargs merging without live image calls. |
| `tests/test_llms_telemetry.py` | Redacted telemetry module exports, capability/result helper identity, sink isolation, model-call success/failure records, and chat/vision capability guard behavior. |
| `scripts/smoke_note_maker.py` | Live optional Holly path: intake -> note -> cover. Requires config/assets. |

## Open Decisions

| Decision | Current default |
| --- | --- |
| Whether `IntentLLMResult` should replace parts of `IntakeAgent` | Not yet; helper exists but current Intake is stable. |
| Where generated artifacts should persist | Local paths for now; future `ContentPackage` bridge should own final artifact index. |
| Whether NoteMaker should have rule fallback | No; current design treats it as LLM-required. |
