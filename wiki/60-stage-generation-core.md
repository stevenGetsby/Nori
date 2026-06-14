<!-- Last verified: 2026-06-01 | Current stage: P1 Account-Ops Backend -->

# Stage 60: Generation Core

## Goal

Stabilize the executable XHS generation chain:

```text
UserInput(text/images)
-> IntakeResult(intention/context/assets)
-> ContextPack / ContextView(platform, market, skills, content strategy, assets, constraints)
-> ContentDesignSpec(structure/rules/media plan/acceptance checks)
-> NoteDraft(title/body/tags/asset bundle)
-> CoverResult(cover image path/prompt/reference paths)
```

## Current Flow

| Step | Module | Status | Output |
| --- | --- | --- | --- |
| 1. Input orchestration | `nori/agents/user_profiling/intaker/intaker.py` | Implemented | `IntakeResult` |
| 2. Text intake normalization | `nori/agents/user_profiling/intaker/normalizer.py` | Implemented | intention/context/missing/questions |
| 3. Vision tagging | `nori/agents/user_profiling/intaker/image_tagger.py` | Implemented | `UserAsset` with `vision_*` fields |
| 4. Context compilation | `nori/context/compiler.py::ContextCompiler` + `nori/context/resolver.py::ContextResolver` | Implemented | `ContextPack` / `ContextView` |
| 5. Content design spec | `nori/agents/content_generation/spec_designer/spec_designer.py::ContentSpecAgent` | Implemented | `ContentDesignSpec` |
| 6. Artifact execution | `nori/agents/content_generation/artifact_generator/artifact_generator.py::ArtifactGenerationAgent` | Implemented | routes spec to concrete generator |
| 6. Skill selection | `nori/agents/content_generation/note_maker/package.py::NoteSkillSelector` | Implemented | chosen `NoteSkill` when executor needs note copy |
| 7. Asset curation | `nori/agents/content_generation/note_maker/package.py::NoteAssetCurator` | Implemented | `AssetBundle` |
| 8. Note composition | `nori/agents/content_generation/note_maker/package.py::NoteComposer` | Implemented | `NoteDraft` |
| 9. Cover reference selection | `nori/agents/content_generation/cover_director/package.py::CoverReferenceSelector` | Implemented | reference image paths |
| 10. Cover prompt writing | `nori/agents/content_generation/cover_director/package.py::CoverPromptBuilder` | Implemented | image prompt |
| 11. Cover image call | `CoverDirectorAgent` | Implemented | image payload |
| 12. Cover image output | `nori/agents/content_generation/cover_director/output.py` | Implemented | `CoverResult.cover_path` |

## Contracts

| Contract | Source |
| --- | --- |
| `UserInput`, `IntakeResult` | `nori/agents/user_profiling/schemas/profile.py`; front-pipeline inputs/results support `to_dict()` / `from_dict()` round trips. |
| `UserAsset` | `nori/core/asset_models.py`; cross-stage asset contract produced by Intake and consumed by NoteMaker/CoverDirector/ContentProducer. `nori.agents.content_generation.schemas` re-exports the same class for existing generation call sites. |
| `AssetBundle`, `CandidateTitle`, `NoteDraft` | `nori/agents/content_generation/schemas/generation.py`; generation artifacts support `to_dict()` / `from_dict()` round trips, and `UserAsset.from_dict()` is the canonical dict-asset normalization path for NoteMaker/ContentProducer. |
| `ContextSlice`, `ContextView` | `nori/context/schemas/context.py`; agent-facing context projections for platform strategy, market hotspots, learned skills, content strategy, asset context, and constraints. |
| `ContentDesignSpec` | `nori/agents/content_generation/schemas/generation.py`; bridge contract between skill/context decisions and artifact execution. It stores selected skill refs, evidence refs, structure, media plan, copy/visual rules, constraints, and acceptance checks. |
| `CoverResult` | `nori/agents/content_generation/schemas/generation.py`; cover artifacts support `to_dict()` / `from_dict()` round trips. |
| `NoteSkill` | `nori/agents/market_analysis/schemas/market.py` |
| `load_note_skills`, `write_note_skill_fixture` | `nori/agents/market_analysis/note_skill_fixture.py` |

## Agent Boundaries

| Agent | Owns | Must not own |
| --- | --- | --- |
| Intake | Text normalization, image vision tags, missing questions. | Account strategy, note copy, image generation. |
| ContextCompiler/Resolver | Platform, market, skill, content-strategy, asset, and constraint context assembly; agent-specific context projection. | Writing final generation specs or artifact copy. |
| ContentSpec | Artifact type, selected skill refs, structure, media plan, copy/visual rules, acceptance checks from `ContextView`. | Final copy, image generation, package persistence. |
| ArtifactGeneration | Instantiating a spec into concrete artifacts and passing spec context to executors. | Re-selecting strategy or rewriting the spec. |
| NoteMaker | Skill pick, asset bundle, title/body/tags. | Raw image reading, cover rendering, account planning. |
| CoverDirector | Reference selection for cover, prompt writing, image generation. | Body copy, skill learning, platform publishing. |

## XHS Hotspot Prompt Ownership

The external `xhs-hotspot-image-post-generator` skill maps into Nori through existing agents instead of becoming a separate generator. Its prompt responsibilities are split this way:

| Skill requirement | Nori owner | Implementation |
| --- | --- | --- |
| Hotspot evidence, account fit, content gap, imageability, and risk scoring | `NoteSkillSelector` | The skill-selection prompt now chooses a learned skill using hotspot evidence, account credibility, audience fit, content gap, visualizability, and risk. |
| Design spec / page rhythm | `ContentSpecAgent` | XHS image-post specs produce a six-part page sequence: cover, hotspot bridge, account fit, proof/example, method/choice, save/comment CTA. |
| Copy, title, tags, and authenticity boundaries | `NoteComposer` | The copy prompt now asks for source-aware hotspot assumptions, account credibility, one-glance first-image support, <=20-character titles, <=1000-character body, and no fake experience/screenshots/endorsement. |
| Cover direction and image-generation prompt | `CoverPromptBuilder` | The cover prompt now enforces one-glance clarity, hotspot/account fit, 6-14 character cover text, and bans fake UI, official notices, testimonials, and medical/financial proof. |
| Human review checklist | `ContentDesignSpec.metadata.human_review_checklist` | Hotspot image-post specs include checks for evidence traceability, credible account angle, first-image clarity, and no fabricated claims. |

Market-analysis agents still collect and distill XHS evidence. Generation agents consume that evidence; they should not pretend to know live hotspots unless a collector, user brief, or other source has supplied the evidence.

## Guizang Social Card Design Profile

The external `guizang-social-card-skill` is distilled into Nori as a design profile, not vendored as templates. The owner is `nori.agents.content_generation.social_card_guides`; `ContentSpecAgent` injects the profile into `ContentDesignSpec.media_plan`, `visual_rules`, `acceptance_checks`, and `metadata`.

| External principle | Nori placement |
| --- | --- |
| XHS cards should be a visual argument, not an article pasted into posters | `media_plan.social_card.compression_ladder` and acceptance checks. |
| XHS output defaults to `1080 x 1440`, `3:4`, phone-safe margins, 5-9 pages | `media_plan.social_card.canvas` and `page_count`. |
| Page 1 is cover hook; pages 2-N carry one idea each | `media_plan.social_card.page_plan` and enriched `ContentDesignSpec.structure[*].page_role`. |
| Editorial and Swiss modes are visual stances, not content-type categories | `visual_rules.social_card.style_modes`. |
| QA should check thumbnail legibility, safe area, density, style identity, screenshot readability, and no fake evidence | `ContentDesignSpec.acceptance_checks`; `CoverPromptBuilder` also reads `intent.content_design_spec` and repeats first-cover constraints. |
| WeChat cover output is a 21:9 + 1:1 pair, not a hard crop | `media_plan.wechat_cover_pair` for `platform=wechat` article tasks. |

This keeps skill strategy decoupled from concrete execution: future HTML/card renderers can consume the same spec, while the current `CoverDirector` already gets the cover-relevant parts through `intent.content_design_spec`.

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
| `nori.core.llms.chat(...)` / `nori.core.llms.achat(...)` | Execute through `nori.core.llms.lm.LanguageModelClient`, which uses LangChain chat adapters from `init_chat_model`, checks active model type through `nori.core.llms.capabilities.ensure_chat_capability` before provider dispatch, and preserves Nori's active-model config. Text chat accepts `type=llm` or `type=vision`; `usage="vision"` and multimodal message parts require `supports_vision=true`, otherwise `ChatCapabilityError`. Chat text comes from the LangChain message `content`; empty or missing content raises `ChatResultError` instead of leaking empty success. |
| `nori.core.llms.chat_json(...)` | Executes through LangChain `with_structured_output(..., include_raw=True)`. Without a schema it binds `method="json_mode"`; with a schema it defaults to `json_schema` unless `structured_method` is provided. The gateway returns only JSON objects and wraps LangChain parse failures as `ChatJSONError`. |
| `nori.core.llms.current_mode()` / `nori.core.llms.set_mode(...)` / `nori.core.llms.ensure_ready(...)` | Use a trimmed runtime mode value so `NORI_MODE=" ghc "` selects the same active block and readiness probe path as `NoriConfig`. |
| `nori.shared.call_stage_json(...)` | Shared generation-stage wrapper around `nori.core.llms.chat_json(json_mode=True)` that raises the caller's domain exception type. |
| `nori.shared.call_stage_messages_json(...)` | Shared required-stage wrapper for pre-built messages, including Intake vision's multimodal `usage="vision"` JSON tagging call. |
| `nori.shared.try_stage_messages_json(...)` | Shared optional-stage wrapper for pre-built messages, including future multimodal/custom-message fallback paths. It returns `(data, error)` instead of raising so deterministic fallbacks can continue. Parse failures reuse the same `empty_response` / `parse_error` classification as optional `nori.core.llms` structured helpers. |
| `nori.shared.try_stage_json(...)` | System/user convenience wrapper over `try_stage_messages_json(...)` for optional-stage JSON stages. |
| `nori.shared.attach_llm_error(...)` | Shared formatter for optional fallback `llm_error` fields, used by Intake, AccountPlanner, ops planners, and analyzer fallbacks to avoid local shape drift. |
| `nori.agents.user_profiling.intaker.normalizer.*` | Intake text boundary. It owns deterministic text fallback, optional text-LLM output normalization, allowed vocabulary/alias mapping, image context construction, and missing/question repair; `IntakeAgent` only decides whether to call text LLM and vision tagging. |
| `nori.agents.user_profiling.intaker.image_tagger.*` | Intake vision boundary. It owns per-image multimodal JSON prompt construction, parallel dispatch, per-image failure isolation, and tag vocabulary filtering; `IntakeAgent` only decides when to use vision tagging. |
| `nori.agents.content_generation.note_maker.package.*` | NoteMaker package boundary. `NoteSkillSelector`, `NoteAssetCurator`, and `NoteComposer` own prompt construction, selected-index normalization, text bucket cleanup, cover/gallery path selection, candidate title/tag/validation normalization, and domain-error translation; `NoteMakerAgent` only orchestrates skill pick -> asset bundle -> note draft. |
| `nori.agents.content_generation.cover_director.package.CoverReferenceSelector` | CoverDirector reference boundary. It owns tagged-asset prompt construction, chosen-index normalization, existing-image filtering, dedupe/cap policy, reference input conversion, and legacy draft/reference-asset path collection; `CoverDirectorAgent` keeps the wrapper for image-stage orchestration. |
| `nori.agents.content_generation.cover_director.package.CoverPromptBuilder` | CoverDirector prompt boundary. It owns image-prompt JSON construction from draft asset facts, skill rules, intent, and selected reference count; `CoverDirectorAgent` only injects the JSON stage and passes the resulting prompt to image generation. |
| `nori.agents.content_generation.cover_director.output.*` | CoverDirector output boundary. It owns data-uri decoding, remote image download, filename sanitization, and persistence errors; `CoverDirectorAgent` only passes the first image payload and records the resulting path. |
| `nori.agents.content_generation.spec_designer.ContentSpecAgent` | Spec boundary. Skills, platform rules, task intent, assets, and acceptance checks are resolved into `ContentDesignSpec` before execution. This keeps reusable skills decoupled from concrete generators. |
| `nori.agents.content_generation.artifact_generator.ArtifactGenerationAgent` | Execution boundary. It consumes `ContentDesignSpec`, filters skill inputs to `selected_skill_refs`, injects the spec into intent/context, and delegates to concrete generators. |
| `nori.core.llms.chat(...)` request kwargs | `LanguageModelClient` owns model-constraint merging. It copies caller `extra_body` before applying model-level defaults and always normalizes token-limit kwargs so each model sends only its expected parameter, even when no `max_output` default is configured. |
| `nori.core.llms.image(..., reference_images=...)` | `ImageClient` checks active model type and reference-image capability through `nori.core.llms.capabilities.ensure_image_capability`; invalid image usage raises `ImageCapabilityError`. OpenAI-compatible image requests also merge model-level `extra_body` without mutating caller kwargs, but do not inherit chat-only token/temperature fields. Image response normalization lives with `ImageProviders`; responses with no usable URL/base64 image raise `ImageResultError` instead of returning an empty success. |
| `nori.core.llms.image_inputs.*` | Canonical reference-image input helpers. `load_image_bytes(...)` normalizes bytes, data-uri, local path, and base64 string inputs while returning empty bytes for invalid/remote values; `sniff_mime(...)` and `bytes_to_data_uri(...)` build provider payloads. |
| `nori.core.llms.image_providers.ImageProviders` | Canonical provider-specific image adapter. OpenAI-compatible edit, relay reference-payload retry, and Google native image generation live here. |
| `nori.core.llms.set_telemetry_sink(...)` | Emits redacted metadata for `chat` / `achat` / `image`; prompt, messages, keys, image bytes, and response text are excluded. Implementation lives in `nori.core.llms.telemetry`. |

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
| `tests/test_content_generation_note_maker_skill_picker.py` | Compact skill-summary prompt contract, hotspot-fit skill-selection rubric, and unknown skill-id domain error translation. |
| `tests/test_content_generation_note_maker_asset_curator.py` | Asset-curation prompt contract, selected-index normalization, empty-asset skip, and cover/gallery path selection. |
| `tests/test_content_generation_note_maker_note_composer.py` | Note-composition prompt contract, XHS hotspot/authenticity guidance, field normalization, fallback candidate title, and missing title/body domain error translation. |
| `tests/test_content_generation_note_maker.py` | Skill selection, asset curation, note composition behavior. |
| `tests/test_content_generation_spec_pipeline.py` | Spec-agent contract, hotspot image-post strategy/page rhythm, artifact-executor skill filtering/spec injection, and explicit spec -> executor composition. |
| `tests/test_content_generation_entrypoints.py` | Guards the removal of the old `GenerationAgent` router and verifies live Holly workflows create a design spec before artifact execution. |
| `tests/test_shared_utils.py` | Shared `call_stage_json` / `call_stage_messages_json` / `try_stage_messages_json` / `try_stage_json` routing, error translation/classification, and utility exports. |
| `tests/test_note_skill_fixture.py` | Learned skill fixture loading into NoteMaker-compatible `NoteSkill` objects. |
| `tests/test_content_generation_cover_director_refs.py` | Cover reference path collection, tagged-asset prompt contract, selected-index normalization, missing-path filtering, dedupe, and reference caps. |
| `tests/test_content_generation_cover_director_prompt.py` | Cover prompt JSON-call contract, one-glance XHS cover constraints, asset fact/text-point summarization, reference-count context, and empty prompt domain errors. |
| `tests/test_content_generation_cover_director_output.py` | Cover output persistence for data-uri/http payloads, safe filename construction, user-agent download requests, and output domain errors. |
| `tests/test_content_generation_cover_director.py` | Reference selection, shared JSON prompt routing, prompt generation, image output path handling. |
| `tests/test_domain_model_contracts.py` | Front-pipeline and generation artifact serialization plus `from_dict()` restoration for intake/account-plan/note/cover snapshots. |
| `tests/test_llms_call_json.py` | LangChain structured-output JSON routing, schema/method passthrough, parse-error wrapping, non-object rejection, and proof that legacy raw-chat injection no longer drives `chat_json`. |
| `tests/test_llms_mode.py` | Runtime mode normalization, config validation reuse, and offline `ghc` readiness probing. |
| `tests/test_llms_intent_target_helpers.py` | Intent extraction, edit-target selector, and shared structured-output helper contracts without live LLM. |
| `tests/test_llms_image_capabilities.py` | Image reference capability guard, image result normalization, image input/provider helper aliases, provider helper behavior, and image request kwargs merging without live image calls. |
| `tests/test_llms_telemetry.py` | Redacted telemetry module exports, capability/result helper identity, sink isolation, model-call success/failure records, and chat/vision capability guard behavior. |
| `scripts/smoke_note_maker.py` | Live optional Holly path: intake -> note -> cover. Requires config/assets. |

## Open Decisions

| Decision | Current default |
| --- | --- |
| Where generated artifacts should persist | Local paths for now; future `ContentPackage` bridge should own final artifact index. |
| Whether NoteMaker should have rule fallback | No; current design treats it as LLM-required. |
