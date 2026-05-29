<!-- Last verified: 2026-05-26 | Current stage: P1 Account-Ops Backend -->

# Backlog

## Verification Baseline

| Baseline | Command |
| --- | --- |
| Default suite | `python -m pytest tests -q` |
| Project status | `python 文档/codex-skills/nori-project-operator/scripts/nori_status.py .` |

Latest default test run on 2026-05-26: `python -m pytest tests -q` -> 448 passed, 3 skipped. Project skill exists; canonical workflow stages and models are split across the five business modules; concrete stages own package folders with prompt files only when they own prompt text/construction and explicit public exports; model contracts live in business-module `models.py` files or `nori.core`; runtime stages use `nori.core.LLMFactory` instead of direct `llms` imports; domain facades inherit `nori.core.WorkflowBase` and declare readable `step_names`; cross-stage workflow contracts and asset library contracts live in `nori.core.models`, and `AccountOperationProject` lives in `nori.core.project`; `ops_models`, `ops_agents`, `gen_agents`, `ana_agents`, `agent_models`, and `agent_utils` legacy packages have been removed; local `api_config.yaml` exists and status output redacts it to active model names.

## Domain Architecture Refactor

| Task | Status | Notes |
| --- | --- | --- |
| Define shared + five-module architecture | Done | Spec written at `wiki/specs/spec-domain-architecture.md`. |
| Add domain architecture registry | Done | `nori/core/architecture.py` exposes `DomainModule`, `DOMAIN_MODULES`, `domain_module_names()`, and `get_domain_module()`. |
| Add shared domain contracts | Done | `nori/core/models.py` defines `UserProfile`, `UserAsset`, `AssetRecord`, `AssetLibrary`, `ClientBrief`, `OperationPlan`, `KPIPlan`, `ContentTask`, `ContentCalendar`, `MarketAnalysis`, `ContextPack`, `DecisionPoint`, `ExplanationTrace`, `CandidateSet`, `PerformanceSnapshot`, `LearningSignal`, and `DomainSnapshot`. |
| Add user profiling facade | Done | `nori/user_profiling/facade.py` maps `ClientBrief` + `AccountPositioning` into `UserProfile`. |
| Add market analysis facade | Done | `nori/market_analysis/facade.py` maps `CompetitorResearch` into `MarketAnalysis`. |
| Add context-building facade | Done | `nori/context_building/facade.py` combines profile, task, market evidence, assets, and decisions. |
| Add content-generation facade | Done | `nori/content_generation/facade.py` groups generated packages into `CandidateSet`. |
| Add learning-loop facade | Done | `nori/learning_loop/facade.py` maps metrics/strategy artifacts into monitoring and learning contracts. |
| Keep package `__init__` files as public exports | Done | Five domain packages now keep orchestration logic in `facade.py` and use package roots as stable import surfaces. |
| Project old ops artifacts into new domain modules | Done | `AccountOperationProject` can now feed profile, market, context, candidate, snapshot, and learning-signal contracts through the five facades. |
| Add full domain snapshot aggregation | Done | `LearningLoopFacade.domain_snapshot_from_project()` returns a round-trippable `DomainSnapshot` across all five modules. |
| Add DomainSnapshot structural validation | Done | `DomainSnapshot.validate()` / `is_valid()` guard module coverage, candidate/context alignment, and selected-candidate integrity. |
| Add public domain entrypoint | Done | `nori/domain.py` exposes `build_domain_snapshot()` and `validate_domain_snapshot()` for upper-layer CLI/API/UI consumers. |
| Centralize business-module lazy exports | Done | Added `nori.core.lazy_exports.lazy_export`; five business package roots now use one shared lazy-export helper for facade/stage public APIs while keeping lightweight model exports eager. |
| Rename explanation trace stage history | Done | `ExplanationTrace` now serializes workflow history as `stage_steps`; legacy `agent_steps` payloads still read in and normalize row key `agent` to `stage`. |
| Decouple upstream facades from context-building models | Done | `UserProfilingFacade` and `MarketAnalysisFacade` now consume persisted project dict/object shapes without importing `AccountOperationProject`; architecture tests guard the upstream dependency direction. |
| PR1 learning-loop module migration | Done | Review gate, review policy/scoring/state, metrics snapshot, and strategy iteration implementations now live under `nori/learning_loop`. |
| PR2 content-generation module migration | Done | Content producer, package input/builder/provenance helpers, and production state now live under `nori/content_generation`. |
| PR3 context-building module migration | Done | Operation/KPI/calendar planners, planner prompts/normalizers/policies/task builders, and planner critics now live under `nori/context_building`. |
| PR4 user-profiling and market-analysis migration | Done | Intake, image tagging, account planning, and XHS note analysis implementations now live under `nori/user_profiling` and `nori/market_analysis`. |
| PR5 content-generation consolidation | Done | NoteMaker and CoverDirector implementations now live under `nori/content_generation`. |
| Migrate new feature entrypoints to five modules | Done | New product features now enter `nori/user_profiling`, `nori/market_analysis`, `nori/context_building`, `nori/content_generation`, or `nori/learning_loop`. |
| Split account-ops models by business module | Done | Canonical models now live in each owning module's `models.py`; the old account-ops model root was removed. |
| Group workflow stage implementation files by owning package | Done | Intaker, AccountPlanner, NoteMaker, CoverDirector, ContentProducer, OperationPlanner, KPIPlanner, CalendarPlanner, Review, Strategy, and XHSNoteAnalyzer now each own a package folder with a specifically named entry module plus local helper modules. |
| Remove legacy agent/model roots | Done | Deleted `nori/gen_agents`, `nori/ops_agents`, `nori/ana_agents`, `nori/ops_models`, `nori/agent_models`, and `nori/agent_utils`; tests now assert these import roots are absent. |
| Tighten stage package public exports | Done | Stage package roots now use explicit `__all__` exports and no longer re-export implementation internals such as `llms`; tests monkeypatch entry modules directly. |
| Trim XHS analyzer orchestration file | Done | Removed private pass-through helper functions from `xhs_note_analyzer.py`; the file now orchestrates loader/rules/LLM/session modules directly. |
| Trim stage entry orchestration wrappers | Done | Removed no-value private pass-through helpers from NoteMaker, CoverDirector, Intaker, AccountPlanner, ContentProducer, ReviewGate, StrategyIteration, Operation/KPI/Calendar planners, and XHS analyzer entry modules. |
| Move user-profiling model ownership | Done | `UserInput`, `IntakeResult`, `AccountPlannerInput`, and `AccountPlanResult` now live in `nori.user_profiling.models`; architecture tests block imports from the removed old owner path. |
| Move content-generation model ownership | Done | `AssetBundle`, `CandidateTitle`, `NoteDraft`, and `CoverResult` now live in `nori.content_generation.models`; architecture tests block imports from the removed old owner path. `UserAsset` was later promoted to `nori.core.models` as a cross-stage asset contract. |
| Promote UserAsset to shared core contract | Done | `UserAsset` now lives in `nori.core.models`; `user_profiling` no longer imports `content_generation`, and `nori.content_generation.models` re-exports the same class for existing generation call sites. |
| Move market-analysis model ownership | Done | `XHSNoteSample`, `XHSSeedSkillDraft`, `NoteEvidence`, `NoteSkill`, and `SessionSkillReport` now live in `nori.market_analysis.models`; architecture tests block imports from the removed old owner path. |
| Remove agent model compatibility root | Done | Removed `nori/agent_models` after all model owners moved to business modules; `tests/test_domain_model_contracts.py` now covers canonical model serialization. |
| Move shared runtime utilities | Done | Moved case logging, image IO, and JSON LLM helpers from `nori/agent_utils` to `nori/shared`; `tests/test_shared_utils.py` covers the canonical utility surface. |
| Move NoteSkill fixture helper to market analysis | Done | `load_note_skills`, `note_skill_fixture`, and `write_note_skill_fixture` now live under `nori.market_analysis.note_skill_fixture`; `nori/shared` no longer imports business modules. |

## P0 / Documentation Hygiene

| Task | Status | Notes |
| --- | --- | --- |
| Make wiki canonical entry | Done | This wiki now captures roadmap, architecture, stages, backlog, and maintenance rules. |
| Update README to point at wiki | Done | README is now a compact project entry that treats `wiki/` as canonical and `文档/` as historical reference. |
| Decide fate of `进度.md` | Done | Marked root `进度.md` as a historical archive and updated the project operator skill to use wiki/backlog as the canonical status source. |
| Add root project config docs without secrets | Done | Added `api_config.example.yaml`, `wiki/refs/api-config.md`, and config contract tests. |
| Keep Python 3.9 import compatibility | Done | Shared dataclass model/result classes now route through `nori._compat`. |
| Extract LLM gateway error boundary | Done | Gateway error classes are owned by `nori.core.contracts` and exposed through the public `llms` package, call, and client modules. |
| Extract LLM telemetry boundary | Done | Moved sink state and emit logic into `llms.telemetry` while preserving `llms.set_telemetry_sink` and `llms.call.set_telemetry_sink` identity. |
| Extract LLM chat runner boundary | Done | Moved sync/async chat client resolution, kwargs merge, capability guard, provider text extraction, and chat telemetry into `llms.chat_runner`. |
| Extract LLM JSON parser boundary | Done | Moved JSON object parsing into `llms.json_parser` while preserving `llms.parse_json_object` and `llms.call.parse_json_object` identity. |
| Extract LLM JSON-call boundary | Done | Moved JSON-mode raw call, response-format fallback, and retry classification into `llms.json_calls` while preserving legacy `llms.call._chat_json_raw` helper identity. |
| Extract LLM request-param boundary | Done | Moved chat/image kwargs merge and token-limit normalization into `llms.request_params` while preserving legacy `llms.call._merge_*` helper identity. |
| Extract LLM capability boundary | Done | Moved chat/vision/image-reference guard policy into `llms.capabilities` while preserving legacy `llms.call._ensure_*` helper identity. |
| Extract LLM result boundary | Done | Moved chat text and image result normalization into `llms.results` while preserving legacy `llms.call._extract_chat_text` / `_collect_image_results` helper identity. |
| Extract LLM image-input boundary | Done | Moved reference-image bytes/data-uri/path/base64 normalization and MIME/data-uri helpers into `llms.image_inputs` while preserving legacy `llms.call._load_image_bytes` / `_bytes_to_data_uri` / `_sniff_mime` helper identity. |
| Extract LLM image-provider boundary | Done | Moved OpenAI-compatible edit, relay reference payload retry, and Google native image generation into `llms.image_providers` while preserving legacy `llms.call._image_*` helper identity. |
| Extract LLM image runner boundary | Done | Moved active image-model resolution, reference input filtering, image capability guards, provider dispatch, result validation, and image telemetry into `llms.image_runner`. |
| Extract structured LLM-output normalization | Done | Moved shared string cleanup, `ChatJSONError` reason classification, intent field-node normalization, selector option cleanup, confidence fallback, and alternative filtering for intent/target helpers into `llms.structured_outputs` while preserving legacy module-private helper identity. |
| Extract structured LLM-call boundary | Done | Moved non-throwing JSON-mode call handling, raw capture, parse-error classification, and provider-exception wrapping for intent/target helpers into `llms.structured_calls`. |
| Extract structured LLM-prompt boundary | Done | Moved intent field descriptions, enum/candidate prompt text, target selector catalogs, history formatting, and summary truncation into `llms.structured_prompts`. |
| Restore Holly fixture-dependent tests | Done | Added lightweight `SHOWCASE/Holly` fixture used by Intaker and AccountPlanner tests. |
| Harden LLM JSON helper contract | Done | `chat_json(json_mode=True)` now retries without `response_format`; intent/target helpers reuse it and have offline tests. |
| Fail fast on empty chat provider content | Done | `llms.chat` / `achat` now raise `ChatResultError` when provider responses contain no usable text, and telemetry records the call as failed. |
| Normalize malformed chat provider results | Done | Empty `choices` and missing `message.content` now raise `ChatResultError` for both `chat` and `achat`, with telemetry marked as failed. |
| Guard image reference capability | Done | `llms.image(reference_images=...)` now raises `ImageCapabilityError` when the active image model lacks `supports_reference_image`. |
| Fail fast on empty image provider results | Done | `llms.image` now raises `ImageResultError` when provider responses contain no usable URL/base64 image, and telemetry records the call as failed. |
| Add redacted LLM telemetry hook | Done | Added `set_telemetry_sink` for prompt-free success/error metadata on `chat`, `achat`, and `image`. |
| Make LLM kwargs merge side-effect-free | Done | `_merge_kwargs` now copies caller `extra_body` before applying model-level `extra_body`, with regression coverage. |
| Merge image model extra_body safely | Done | OpenAI-compatible `llms.image` requests now apply model-level `extra_body` without mutating caller kwargs or inheriting chat-only token/temperature fields. |
| Normalize token limit kwargs | Done | `_merge_kwargs` now emits `max_completion_tokens` for GPT-5 and `max_tokens` for other chat models, converting legacy/opposite caller params without sending both, even when `max_output` is unset. |
| Harden embedded JSON object parsing | Done | `parse_json_object` now scans for the first valid embedded JSON object instead of greedily matching all braces, with regression coverage for placeholder braces and multiple objects. |
| Narrow JSON-mode retry classification | Done | `chat_json(json_mode=True)` now retries only response-format/JSON-mode compatibility failures and does not retry unrelated unsupported provider errors. |
| Narrow JSON-mode TypeError retry classification | Done | TypeError fallback now only retries when the error itself indicates `response_format` / JSON-mode incompatibility, so unrelated caller or SDK TypeErrors surface directly. |
| Align resolved model capabilities | Done | `ResolvedModel` now preserves video/audio capability fields and `llms.image` rejects non-image active models early. |
| Guard chat/vision capability | Done | `llms.chat` / `llms.achat` now reject non-chat models and require `supports_vision=true` for vision usage or multimodal message parts. |
| Centralize JSON raw capture | Done | Added `llms.chat_json_with_raw` and routed intent/target helpers through it instead of duplicate chat wrappers. |
| Extract structured LLM result model boundary | Done | `StructuredCallResult`, `IntentLLMResult`, and `TargetSelectionResult` are owned by `nori.core.contracts` and exposed through the public helper modules. |
| Share required stage JSON wrapper | Done | Added `nori.shared.call_stage_json` and routed NoteMaker/CoverDirector JSON stages through it with JSON mode enabled. |
| Share pre-built messages JSON wrapper | Done | Added `call_stage_messages_json` and routed Intake vision JSON tagging through it with JSON mode enabled. |
| Share optional pre-built JSON wrapper | Done | Added `try_stage_messages_json` so optional custom/multimodal message stages can reuse the same deterministic fallback metadata contract as `try_stage_json`. |
| Extract Intake text-normalizer boundary | Done | Moved deterministic text fallback, optional text-LLM output cleanup, label alias mapping, image context construction, and missing/question fallback into `nori.user_profiling.intaker.normalizer`. |
| Extract Intake taxonomy boundary | Done | Moved goal/format/tone/asset/guardrail/data vocabularies, alias mapping, allowed-label cleanup, rule-based classification, and missing/question fallback text into `nori.user_profiling.intaker.taxonomy`. |
| Extract Intake image tagger boundary | Done | Moved per-image vision prompt construction, parallel dispatch, failure isolation, and tag filtering into `nori.user_profiling.intaker.image_tagger`, leaving `intaker.py` focused on text intake and flow orchestration. |
| Consolidate NoteMaker package contract | Done | Moved skill selection, asset curation, note composition, prompt construction, selected-index normalization, and note-field cleanup into class-owned `nori.content_generation.note_maker.package`. |
| Consolidate CoverDirector package contract | Done | Moved tagged-asset selection, draft/reference path collection, reference input conversion, prompt construction, and reference caps into class-owned `nori.content_generation.cover_director.package`. |
| Extract CoverDirector output boundary | Done | Moved data-uri decoding, remote image download, safe filename construction, and output error translation into `nori.content_generation.cover_director.output`. |
| Consolidate AccountPlanner package contract | Done | Moved `AccountPlannerInput` restoration, evidence merging, asset prompt context, and JSON-only prompt construction into class-owned `nori.user_profiling.account_planner.package`. |
| Extract AccountPlanner fallback boundary | Done | Moved deterministic no-inference fallback result construction into `nori.user_profiling.account_planner.fallback`. |
| Extract AccountPlanner search boundary | Done | Moved search provider protocol/fallback, keyword cleanup/dedupe, platform id normalization, provider-error isolation, and search row defaulting into `nori.user_profiling.account_planner.search`. |
| Extract AccountPlanner result-normalizer boundary | Done | Moved AccountPlanner LLM result cleanup, keyword-level normalization, platform-token stripping, search-only merge behavior, and IP portrait benchmark derivation into `nori.user_profiling.account_planner.normalizer`. |
| Extract AccountPlanner portrait boundary | Done | Moved benchmark-account cleanup, IP portrait account names/keywords/pillars/creators/cover formats, and search-only benchmark creator refresh into `nori.user_profiling.account_planner.portrait`. |
| Extract AccountPlanner keyword normalizer boundary | Done | Moved platform-token stripping, keyword-level normalization, reason fallback, search-keyword fallback, and dedupe into `nori.user_profiling.account_planner.keywords`. |
| Centralize LLM fallback error formatter | Done | Added `nori.shared.attach_llm_error` and routed Intake, AccountPlanner, ops planners, and analyzer fallback through it. |
| Refine optional JSON fallback reasons | Done | `try_stage_json` now reuses `llms.structured_outputs.chat_json_error_reason`, preserving `empty_response` versus `parse_error` in fallback metadata. |
| Add front-pipeline fallback metadata | Done | `IntakeResult` and `AccountPlanResult` now support optional metadata; Intake/AccountPlanner route optional JSON stages through `try_stage_json` and record redacted `llm_error` on fallback. |
| Share model coercion helpers | Done | Added shared coercion helpers under `nori.core.contracts` and migrated model `from_dict()` cleanup onto them. |
| Add model boolean coercion | Done | Added shared `bool_value()` and migrated persisted booleans such as `enable_search` / `llm_enhanced` off plain `bool(...)`. |
| Extract runtime config model boundary | Done | Moved `ProviderConfig`, `ModelConfig`, and `ResolvedModel` behind a shared boundary; canonical ownership later moved to `nori.core.contracts`, while `nori_config`, `llms.config`, and `llms.client` preserve class identities. |
| Extract runtime config normalization boundary | Done | Moved provider/model key parsing, env-name cleanup, mode normalization, core section validation, and flat/nested active-model selection into `nori.config_normalization`; `nori_config` and `llms.mode` now reuse it. |
| Harden model config scalar coercion | Done | `NoriConfig` now normalizes model booleans, ints, floats, list options, and dict options before constructing `ModelConfig` / `ResolvedModel`. |
| Fail fast on malformed config sections | Done | Non-mapping YAML top level, `providers`, `models`, and individual provider/model entries now raise `NoriConfigError` instead of generic Python errors or silent empty defaults. |
| Harden scalar duration option parsing | Done | `duration_options: "10"` now restores as `[10]` instead of iterating the string character-by-character. |
| Normalize active model selection | Done | `active_models` now normalizes selected mode blocks, turns malformed shapes into explicit missing-usage errors, and prevents `NORI_MODE` from silently reusing `direct` when a mode block is absent. |
| Canonicalize active usage lookup | Done | `get_active(" llm ")` now trims the queried usage key before resolving the active model. |
| Align runtime mode normalization | Done | `llms.current_mode`, `set_mode`, and `ensure_ready` now trim mode values so readiness probes and `NoriConfig` active selection agree. |
| Reject half-empty model keys | Done | `parse_model_key` now requires non-blank provider and model ids, so `openai::` / `::model` fail before client construction. |
| Canonicalize model key lookup | Done | `NoriConfig` now stores and resolves model keys as canonical `provider::model`, so segment whitespace cannot drop `ModelConfig` fields. |
| Require declared model configs | Done | `NoriConfig.resolve` now raises `KeyError: 未配置模型` when a provider exists but `models.<provider::model>` is missing, preventing silent default `ResolvedModel` construction. |
| Canonicalize provider and mode keys | Done | Provider ids, `mode`, `NORI_MODE`, and mode block keys are now trimmed before lookup; blank provider ids fail fast. |
| Canonicalize API key env names | Done | `api_key_env` and `${ENV_VAR}` placeholders now trim environment variable names before lookup and store `api_key_env` canonically. |
| Validate OpenAI-compatible client config | Done | `llms.get_client` / `get_async_client` now raise `LLMClientConfigError` before SDK construction when active `api_key` or `base_url` is blank. |
| Share readiness/client config validation | Done | `ensure_ready` now reuses the same `validate_client_config` path as client factories, including `base_url` validation before ghc proxy probing. |
| Validate Google image API key before SDK dispatch | Done | Google native image generation now reuses shared `validate_api_key`, raising `LLMClientConfigError` and telemetry before `google-genai` construction when key is blank. |
| Eliminate image active-model double resolution | Done | `llms.image` now uses `build_client_bundle` with the already-resolved model so capability checks and provider dispatch cannot drift across two active-model lookups. |
| Add generation artifact from_dict contracts | Done | `UserAsset`, `AssetBundle`, `CandidateTitle`, `NoteDraft`, and `CoverResult` now restore from persisted dict snapshots with regression coverage. |
| Add front-pipeline from_dict contracts | Done | `UserInput`, `IntakeResult`, `AccountPlannerInput`, and `AccountPlanResult` now restore from persisted dict snapshots with regression coverage. |
| Canonicalize UserAsset dict normalization | Done | NoteMaker and ContentProducer now delegate dict asset restoration to `UserAsset.from_dict()` instead of duplicating normalization logic. |
| Add XHS evidence from_dict contracts | Done | `XHSNoteSample` and `XHSSeedSkillDraft` now restore from persisted dict snapshots, including metric coercion for note samples. |

## P1 Account-Ops Backend

| Task | Status | Notes |
| --- | --- | --- |
| Ops dataclasses | Done | `AccountOperationProject` is the core project aggregate; `ClientBrief`, `OperationPlan`, `KPIPlan`, `ContentCalendar`, and `ContentTask` are core workflow contracts; `ContentPackage`, `ComplianceReview`, `MetricsSnapshot`, and `StrategyIteration` stay in their owning business modules. |
| Consolidate OperationPlanner package contract | Done | Canonical path is class-owned `nori.context_building.operation_planner.package`. |
| Extract OperationPlanner fallback builder boundary | Done | Canonical path is `nori.context_building.operation_planner.project_builder`. |
| Extract OperationPlanner fallback policy boundary | Done | Canonical path is `nori.context_building.operation_planner.project_policy`. |
| Extract OperationPlanner LLM normalizer boundary | Done | Canonical path is `nori.context_building.operation_planner.normalizer`. |
| Consolidate KPIPlanner package contract | Done | Canonical path is class-owned `nori.context_building.kpi_planner.package`. |
| Extract KPIPlanner normalizer boundary | Done | Canonical path is `nori.context_building.kpi_planner.normalizer`. |
| Consolidate CalendarPlanner package contract | Done | Canonical path is class-owned `nori.context_building.calendar_planner.package`. |
| Extract CalendarPlanner normalizer boundary | Done | Canonical path is `nori.context_building.calendar_planner.normalizer`. |
| Extract CalendarPlanner policy boundary | Done | Canonical path is `nori.context_building.calendar_planner.policy`. |
| Extract CalendarPlanner task builder boundary | Done | Canonical path is `nori.context_building.calendar_planner.task_builder`. |
| Operation/KPI/Calendar agents | Done | LLM path + fallback path covered by tests. |
| Ops planner fallback observability | Done | Operation/KPI/Calendar optional LLM calls now route through `try_stage_json`, request JSON mode, and record redacted `metadata.llm_error` on fallback. |
| Extract shared planner critic policy | Done | Canonical path is `nori.context_building.planner_critics`. |
| Asset library model | Done | `AssetRecord` / `AssetLibrary` now live in `nori.core.models`; context-building code imports them from core. |
| Competitor research model | Done | Added `CompetitorSample` / `CompetitorResearch` with top-sample and task-reference helpers. |
| Account positioning model | Done | Added typed `AccountPositioning` with legacy dict compatibility and planner integration. |

## P3 Production Orchestration

| Task | Status | Acceptance |
| --- | --- | --- |
| Content task generation bridge | Done | `ContentTask -> NoteMakerAgent -> CoverDirectorAgent -> ContentPackage` covered by mocked tests. |
| Consolidate content package assembly | Done | Canonical path is `nori.content_generation.content_producer.package.ContentPackageAssembler`. |
| Extract content production state boundary | Done | Canonical path is `nori.content_generation.content_producer.state`. |
| Artifact index | Done | Package records note draft, cover result, prompts, material usage, and source refs. |
| Retry/error contract | Done | Generation failures attach structured error to task/project metadata before raising `ContentProductionError`. |

## P4 Review And Iteration

| Task | Status | Acceptance |
| --- | --- | --- |
| Compliance reviewer | Done | Produces `ComplianceReview` from `ContentPackage`, text-only first. |
| Consolidate review package contract | Done | Canonical path is class-owned `nori.learning_loop.review.package`. |
| Extract review policy boundary | Done | Canonical path is `nori.learning_loop.review.policy`. |
| Extract review scoring boundary | Done | Canonical path is `nori.learning_loop.review.scoring`. |
| Extract review state boundary | Done | Canonical path is `nori.learning_loop.review.state`. |
| Consistency reviewer | Done | Checks brief/title/body/cover prompt alignment. |
| Metrics snapshot workflow | Done | Manual metrics entry can attach to package/task/project. |
| Consolidate strategy iteration package contract | Done | Canonical path is class-owned `nori.learning_loop.strategy.package`. |
| Extract strategy iteration policy boundary | Done | Canonical path is `nori.learning_loop.strategy.policy`. |
| Extract strategy iteration state boundary | Done | Canonical path is `nori.learning_loop.strategy.state`. |
| Strategy iteration agent | Done | Metrics + reviews -> `StrategyIteration.next_actions`. |

## Data Collection / Skill Learning

| Task | Status | Notes |
| --- | --- | --- |
| Stable mocked top-notes tests | Done | Covered by `tests/test_data_collect_top_notes.py`. |
| Redacted live runbook | Done | Added `wiki/refs/data-collection-live-runbook.md` for health checks, smoke commands, troubleshooting, and secret rules. |
| Skill report -> NoteMaker fixture bridge | Done | Added `load_note_skills`, `note_skill_fixture`, `write_note_skill_fixture`, and model `from_dict()` support. |
| Extract XHS note loader boundary | Done | Moved local note/author `meta.json` restoration, tag extraction, and platform metric count parsing into `nori.market_analysis.xhs_note_analyzer.loader`. |
| Extract XHS single-note rule boundary | Done | Moved rule-only seed draft construction, scene/goal classification, content rule extraction, CTA evidence, and confidence scoring into `nori.market_analysis.xhs_note_analyzer.rules`. |
| Consolidate XHS analyzer package contract | Done | Moved note enhancement, keyword, and label prompt contracts into class-owned `nori.market_analysis.xhs_note_analyzer.package`; `note_llm` and `session_llm` now own call orchestration and output normalization only. |
| Extract XHS single-note LLM enhancement boundary | Done | Moved optional JSON routing, LLM output normalization, fallback draft marking, and `validation.llm_error` attachment into `nori.market_analysis.xhs_note_analyzer.note_llm`. |
| Extract XHS session clustering boundary | Done | Moved rule-goal classification, required LLM-label validation, top-four bucket selection, tone majority, and leftover note tracking into `nori.market_analysis.xhs_note_analyzer.session_clustering`. |
| Extract XHS session LLM boundary | Done | Moved keyword generation, hot-note prompt shaping, goal/tone label normalization, and fail-fast JSON helper routing into `nori.market_analysis.xhs_note_analyzer.session_llm`. |
| Extract XHS session reporter boundary | Done | Moved report timestamping, full session report writing, and skills-only guide JSON writing into `nori.market_analysis.xhs_note_analyzer.session_reporter`. |
| Extract XHS session skill-builder boundary | Done | Moved session `NoteSkill` construction, merged rules, evidence-note mapping, cover rules, metric percentiles, note-type majority, and cluster signals into `nori.market_analysis.xhs_note_analyzer.skill_builder`. |
| Analyzer fallback observability | Done | `XHSNoteAnalyzer.analyze_note` optional LLM enhancement now uses `try_stage_json` and shared `attach_llm_error` for structured `validation.llm_error`. |
| Analyzer session JSON helper routing | Done | `collect_for_session` keyword and label stages now use `call_stage_json(json_mode=True)` with fail-fast domain errors. |
| Shared model coercion helpers | Done | `NoteSkill` / `SessionSkillReport` and ops model `from_dict()` paths now share `nori.core.contracts` coercion helpers. |
| XHS evidence from_dict contracts | Done | `XHSNoteSample` and `XHSSeedSkillDraft` now round-trip through `from_dict()` for analyzer evidence artifacts. |

## Deferred

| Task | Reason |
| --- | --- |
| Real publish adapter | Needs review/package safety first. |
| Automatic community operations | Account-safety and compliance risk. |
| Automatic metrics ingestion | Manual `MetricsSnapshot` workflow validates the contract first. |
| Multi-platform parity | XHS-first loop is not complete. |
| Full frontend workbench | Backend contracts and artifact inspection should stabilize first. |
