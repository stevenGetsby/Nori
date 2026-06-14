<!-- Last verified: 2026-06-01 | Current stage: P1 Account-Ops Backend -->

# Backlog

## Verification Baseline

| Baseline | Command |
| --- | --- |
| Default suite | `python -m pytest tests -q` |
| Project status | `python wiki/archive/legacy-docs/codex-skills/nori-project-operator/scripts/nori_status.py .` |

Latest default test run on 2026-06-01: `python -m pytest tests -q` -> 503 passed, 3 skipped. Project skill exists; public capability entrypoints now live under owning modules: `nori.core` for registry metadata and `nori.agents.learning_loop` for aggregate snapshots; runtime state lives under `nori.sessions`, `nori.context`, `nori.memory`, and `nori.workflows`; `WorkflowRunner` now executes `WorkflowSpec` through LangGraph, wraps coarse stage handlers with LangChain Core `RunnableLambda`, and supports default-skipped `HumanGateSpec` approval points; `main.py` reports real CLI/workflow entrypoints instead of importing a missing web server; live smoke scripts import only canonical module roots; `LearningLoopFacade.capability_snapshot_from_project()` builds the current aggregate view. The pre-launch codebase no longer keeps `nori.domain`, `nori.capabilities`, `DomainSnapshot`, or old top-level business roots. Concrete stages own package folders with prompt files only when they own prompt text/construction and explicit public exports; runtime stages use `nori.core.LLMFactory` instead of direct `llms` imports; local `api_config.yaml` exists and status output redacts it to active model names.

## Capability / Runtime Architecture Refactor

| Task | Status | Notes |
| --- | --- | --- |
| Define capability/runtime architecture | Done | Spec written at `wiki/specs/spec-capability-architecture.md`; old domain spec retained as historical compatibility background. |
| Add capability architecture registry | Done | `nori/core/architecture.py` exposes `CapabilityModule`, `CAPABILITY_MODULES`, `capability_module_names()`, and `get_capability_module()`. |
| Add shared capability/runtime contracts | Done | Focused core model owners now live in `nori/core/{profile_models,asset_models,planning_models,capability_models}.py`; runtime contracts live in `nori/sessions`, `nori/context`, `nori/memory`, and `nori/workflows`. |
| Add user profiling facade | Done | `nori/agents/user_profiling/facade.py` maps `ClientBrief` + `AccountPositioning` into `UserProfile`. |
| Add market analysis facade | Done | `nori/agents/market_analysis/facade.py` maps `CompetitorResearch` into `MarketAnalysis`. |
| Add context orchestration layer | Done | `nori/context/compiler.py` compiles profile, task, market evidence, assets, skills, platform rules, and constraints; the old `nori/agents/planning/facade.py` builder re-export has been removed. |
| Add content-generation facade | Done | `nori/agents/content_generation/facade.py` groups generated packages into `CandidateSet`. |
| Add learning-loop facade | Done | `nori/agents/learning_loop/facade.py` maps metrics/strategy artifacts into monitoring and learning contracts. |
| Keep package `__init__` files as public exports | Done | `nori.agents.*` exposes capability-level public agent groups. |
| Project old ops artifacts into capability view | Done | `AccountOperationProject` can now feed profile, market, context, candidate, snapshot, and learning-signal contracts into `CapabilitySnapshot`. |
| Add full capability snapshot aggregation | Done | `LearningLoopFacade.capability_snapshot_from_project()` returns a round-trippable `CapabilitySnapshot` across all five capability groups. |
| Add CapabilitySnapshot structural validation | Done | `CapabilitySnapshot.validate()` / `is_valid()` guard capability coverage, candidate/context alignment, and selected-candidate integrity. |
| Add public capability entrypoints | Done | Registry metadata is exposed by `nori.core.capability_registry_snapshot()`; aggregate build/validate is exposed by `nori.agents.learning_loop`. The legacy `nori/capabilities/` facade has been removed. |
| Promote LLM gateway to core infra | Done | Canonical language/vision/image gateway implementation now lives in `nori.core.llms`; the old top-level `llms/` compatibility package has been removed. |
| Simplify LangGraph workflow runner | Done | `WorkflowRunner` directly compiles `WorkflowSpec` into a LangGraph `StateGraph`, supports `HumanGateSpec` with default skip mode, and records stage status/artifact refs without a separate runner wrapper. |
| Introduce LangChain Core stage runnable boundary | Done | Each `StageSpec.handler` is wrapped with `RunnableLambda`, keeping workflow stages compatible with LangChain runnable semantics. |
| Centralize business-module lazy exports | Done | Added `nori.core.lazy_exports.lazy_export`; five business package roots now use one shared lazy-export helper for facade/stage public APIs while keeping lightweight model exports eager. |
| Rename explanation trace stage history | Done | `ExplanationTrace` now serializes workflow history as `stage_steps`; legacy `agent_steps` payloads still read in and normalize row key `agent` to `stage`. |
| Decouple upstream facades from project aggregate internals | Done | `UserProfilingFacade` and `MarketAnalysisFacade` now consume persisted project dict/object shapes without importing `AccountOperationProject`; architecture tests guard the upstream dependency direction. |
| PR1 learning-loop module migration | Done | Review gate, review policy/scoring/state, metrics snapshot, and strategy iteration implementations now live under `nori/agents/learning_loop`. |
| PR2 content-generation module migration | Done | Content producer, package input/builder/provenance helpers, and production state now live under `nori/agents/content_generation`. |
| PR3 planning module migration | Done | Operation/KPI/calendar planners, planner prompts/normalizers/policies/task builders, and planner critics now live under `nori/agents/planning`. |
| PR4 user-profiling and market-analysis migration | Done | Intake, image tagging, account planning, and XHS note analysis implementations now live under `nori/agents/user_profiling` and `nori/agents/market_analysis`. |
| PR5 content-generation consolidation | Done | NoteMaker and CoverDirector implementations now live under `nori/agents/content_generation`. |
| Migrate new feature entrypoints to five modules | Done | New product features now enter `nori/agents/user_profiling`, `nori/agents/market_analysis`, `nori/agents/planning`, `nori/agents/content_generation`, or `nori/agents/learning_loop`. |
| Split account-ops models by business module | Done | Canonical models now live in each owning module schemas; the old account-ops model root was removed. |
| Group workflow stage implementation files by owning package | Done | Intaker, AccountPlanner, NoteMaker, CoverDirector, ContentProducer, OperationPlanner, KPIPlanner, CalendarPlanner, Review, Strategy, and XHSNoteAnalyzer now each own a package folder with a specifically named entry module plus local helper modules. |
| Remove legacy agent/model roots | Done | Deleted `nori/gen_agents`, `nori/ops_agents`, `nori/ana_agents`, `nori/ops_models`, `nori/agent_models`, and `nori/agent_utils`; tests now assert these import roots are absent. |
| Tighten stage package public exports | Done | Stage package roots now use explicit `__all__` exports and no longer re-export implementation internals such as `llms`; tests monkeypatch entry modules directly. |
| Trim XHS analyzer orchestration file | Done | Removed private pass-through helper functions from `xhs_note_analyzer.py`; the file now orchestrates loader/rules/LLM/session modules directly. |
| Trim stage entry orchestration wrappers | Done | Removed no-value private pass-through helpers from NoteMaker, CoverDirector, Intaker, AccountPlanner, ContentProducer, ReviewGate, StrategyIteration, Operation/KPI/Calendar planners, and XHS analyzer entry modules. |
| Move user-profiling model ownership | Done | `UserInput`, `IntakeResult`, `AccountPlannerInput`, and `AccountPlanResult` now live in `nori.agents.user_profiling.schemas`; architecture tests block imports from the removed old owner path. |
| Move content-generation model ownership | Done | `AssetBundle`, `CandidateTitle`, `NoteDraft`, and `CoverResult` now live in `nori.agents.content_generation.schemas`; architecture tests block imports from the removed old owner path. `UserAsset` was later promoted to `nori.core.asset_models` as a cross-stage asset contract. |
| Promote UserAsset to shared core contract | Done | `UserAsset` now lives in `nori.core.asset_models`; `user_profiling` no longer imports `content_generation`, and `nori.agents.content_generation.schemas` re-exports the same class for existing generation call sites. |
| Move market-analysis model ownership | Done | `XHSNoteSample`, `XHSSeedSkillDraft`, `NoteEvidence`, `NoteSkill`, and `SessionSkillReport` now live in `nori.agents.market_analysis.schemas`; architecture tests block imports from the removed old owner path. |
| Remove agent model compatibility root | Done | Removed `nori/agent_models` after all model owners moved to business modules; `tests/test_domain_model_contracts.py` now covers canonical model serialization. |
| Move shared runtime utilities | Done | Moved case logging, image IO, and JSON LLM helpers from `nori/agent_utils` to `nori/shared`; `tests/test_shared_utils.py` covers the canonical utility surface. |
| Move NoteSkill fixture helper to market analysis | Done | `load_note_skills`, `note_skill_fixture`, and `write_note_skill_fixture` now live under `nori.agents.market_analysis.note_skill_fixture`; `nori/shared` no longer imports business modules. |

## P0 / Documentation Hygiene

| Task | Status | Notes |
| --- | --- | --- |
| Make wiki canonical entry | Done | This wiki now captures roadmap, architecture, stages, backlog, and maintenance rules. |
| Update README to point at wiki | Done | README is now a compact project entry that treats `wiki/` as canonical and `wiki/archive/legacy-docs/` as historical reference. |
| Archive root progress tracker | Done | Moved root `进度.md` to `wiki/archive/进度.md`; current status belongs in roadmap/backlog. |
| Add root project config docs without secrets | Done | Added `api_config.example.yaml`, `wiki/refs/api-config.md`, and config contract tests. |
| Keep Python 3.9 import compatibility | Done | Shared dataclass model/result classes now route through `nori._compat`. |
| Extract LLM gateway error boundary | Done | Gateway error classes are owned by `nori.core.contracts` and exposed through the public `nori.core.llms` package root. |
| Extract LLM telemetry boundary | Done | Moved sink state and emit logic into `nori.core.llms.telemetry`; the public setter is exposed from `nori.core.llms`. |
| Move LLM chat execution into client class | Done | Sync/async chat adapter resolution, kwargs merge, capability guard, LangChain message content extraction, and chat telemetry now live in `LanguageModelClient`. |
| Route text chat through LangChain init API | Done | `nori.core.llms.chat` / `achat` now execute through chat adapters built by LangChain `init_chat_model` while preserving Nori active-model config, request-param merging, capability guards, result errors, and telemetry. OpenAI SDK clients remain for image provider paths. |
| Route LLM JSON through LangChain structured output | Done | `nori.core.llms.chat_json` now executes through `with_structured_output(..., include_raw=True)` and returns parsed JSON objects instead of hand-parsing model text. |
| Remove raw-chat JSON retry path | Done | `chat_json` no longer calls `_chat` / `chat_func`, no longer injects `response_format` by hand, and no longer retries into a private text parser. |
| Move request kwargs policy into client classes | Done | Chat kwargs live in `LanguageModelClient`; image kwargs live in `ImageClient`; both paths keep caller dictionaries immutable. |
| Extract LLM capability boundary | Done | Moved chat/vision/image-reference guard policy into `nori.core.llms.capabilities`; capability checks stay behind named internal boundaries. |
| Move provider output normalization into client/provider classes | Done | Chat text normalization lives privately in `LanguageModelClient`; image URL/data-uri extraction lives with `ImageProviders`. |
| Remove legacy OpenAI chat response parsing | Done | Text chat now consumes LangChain message `content` only; old SDK-shaped compatibility parsing was removed. |
| Extract LLM image-input boundary | Done | Moved reference-image bytes/data-uri/path/base64 normalization and MIME/data-uri helpers into `nori.core.llms.image_inputs`. |
| Extract LLM image-provider boundary | Done | Moved OpenAI-compatible edit, relay reference payload retry, and Google native image generation into `ImageProviders`. |
| Move LLM image execution into client class | Done | Active image-model resolution, reference input filtering, image capability guards, provider dispatch, result validation, and image telemetry now live in `ImageClient`. |
| Remove unused structured LLM helper modules | Done | Removed the unconnected intent/target helper prompts, normalization module, structured result models, and non-throwing structured call wrapper from `nori.core.llms`; product-specific structured helpers belong in the owning agent/supervisor package. |
| Move structured JSON-call behavior into shared helper/client | Done | Required/optional stage wrappers stay in `nori.shared.llm_json`; actual JSON execution is owned by `LanguageModelClient` through LangChain structured output. |
| Keep JSON fallback reason local to shared helper | Done | `try_stage_json` now classifies empty vs malformed JSON inside `nori.shared.llm_json`, without depending on a core LLM structured-output module. |
| Move Holly fixture-dependent tests to case workspace | Done | Intaker and AccountPlanner tests now read the curated fixture from `cases/Holly/showcase`. |
| Harden LLM JSON helper contract | Done | `chat_json` now uses LangChain structured output and raises `ChatJSONError` for parser failures or non-object structured outputs; tests mock `llms.chat_json` directly. |
| Fail fast on empty chat provider content | Done | `nori.core.llms.chat` / `achat` now raise `ChatResultError` when provider responses contain no usable text, and telemetry records the call as failed. |
| Normalize malformed chat provider results | Done | Empty or missing LangChain message `content` now raises `ChatResultError` for both `chat` and `achat`, with telemetry marked as failed. |
| Guard image reference capability | Done | `nori.core.llms.image(reference_images=...)` now raises `ImageCapabilityError` when the active image model lacks `supports_reference_image`. |
| Fail fast on empty image provider results | Done | `nori.core.llms.image` now raises `ImageResultError` when provider responses contain no usable URL/base64 image, and telemetry records the call as failed. |
| Add redacted LLM telemetry hook | Done | Added `set_telemetry_sink` for prompt-free success/error metadata on `chat`, `achat`, and `image`. |
| Make LLM kwargs merge side-effect-free | Done | Chat/image gateway calls now copy caller `extra_body` before applying model-level `extra_body`, with regression coverage. |
| Merge image model extra_body safely | Done | OpenAI-compatible `nori.core.llms.image` requests now apply model-level `extra_body` without mutating caller kwargs or inheriting chat-only token/temperature fields. |
| Normalize token limit kwargs | Done | Chat gateway kwargs now emit `max_completion_tokens` for GPT-5 and `max_tokens` for other chat models, converting opposite caller params without sending both, even when `max_output` is unset. |
| Remove embedded JSON parser dependency | Done | `LanguageModelClient` no longer owns fenced/embedded JSON text parsing; LangChain structured output is the JSON boundary. |
| Remove JSON-mode retry classification | Done | `chat_json` no longer carries response-format retry classifiers because structured output binding is delegated to LangChain. |
| Remove JSON-mode TypeError retry classification | Done | TypeError compatibility retry was removed with the raw-chat JSON fallback path; provider/SDK errors now surface directly unless LangChain returns a structured parsing error payload. |
| Align resolved model capabilities | Done | `ResolvedModel` now preserves video/audio capability fields and `nori.core.llms.image` rejects non-image active models early. |
| Guard chat/vision capability | Done | `nori.core.llms.chat` / `nori.core.llms.achat` now reject non-chat models and require `supports_vision=true` for vision usage or multimodal message parts. |
| Remove public JSON raw-capture helper | Done | `chat_json` owns retry and parse behavior; raw-capture plumbing is private to `LanguageModelClient`, and package root no longer exposes `chat_json_with_raw`. |
| Remove unused structured LLM result contracts | Done | Deleted `StructuredCallResult`, `IntentLLMResult`, and `TargetSelectionResult` from `nori.core.contracts` because the helper modules they served were not connected to production code. |
| Share required stage JSON wrapper | Done | Added `nori.shared.call_stage_json` and routed NoteMaker/CoverDirector JSON stages through it with JSON mode enabled. |
| Share pre-built messages JSON wrapper | Done | Added `call_stage_messages_json` and routed Intake vision JSON tagging through it with JSON mode enabled. |
| Share optional pre-built JSON wrapper | Done | Added `try_stage_messages_json` so optional custom/multimodal message stages can reuse the same deterministic fallback metadata contract as `try_stage_json`. |
| Extract Intake text-normalizer boundary | Done | Moved deterministic text fallback, optional text-LLM output cleanup, label alias mapping, image context construction, and missing/question fallback into `nori.agents.user_profiling.intaker.normalizer`. |
| Extract Intake taxonomy boundary | Done | Moved goal/format/tone/asset/guardrail/data vocabularies, alias mapping, allowed-label cleanup, rule-based classification, and missing/question fallback text into `nori.agents.user_profiling.intaker.taxonomy`. |
| Extract Intake image tagger boundary | Done | Moved per-image vision prompt construction, parallel dispatch, failure isolation, and tag filtering into `nori.agents.user_profiling.intaker.image_tagger`, leaving `intaker.py` focused on text intake and flow orchestration. |
| Consolidate NoteMaker package contract | Done | Moved skill selection, asset curation, note composition, prompt construction, selected-index normalization, and note-field cleanup into class-owned `nori.agents.content_generation.note_maker.package`. |
| Consolidate CoverDirector package contract | Done | Moved tagged-asset selection, draft/reference path collection, reference input conversion, prompt construction, and reference caps into class-owned `nori.agents.content_generation.cover_director.package`. |
| Extract CoverDirector output boundary | Done | Moved data-uri decoding, remote image download, safe filename construction, and output error translation into `nori.agents.content_generation.cover_director.output`. |
| Consolidate AccountPlanner package contract | Done | Moved `AccountPlannerInput` restoration, evidence merging, asset prompt context, and JSON-only prompt construction into class-owned `nori.agents.user_profiling.account_planner.package`. |
| Extract AccountPlanner fallback boundary | Done | Moved deterministic no-inference fallback result construction into `nori.agents.user_profiling.account_planner.fallback`. |
| Extract AccountPlanner search boundary | Done | Moved search provider protocol/fallback, keyword cleanup/dedupe, platform id normalization, provider-error isolation, and search row defaulting into `nori.agents.user_profiling.account_planner.search`. |
| Extract AccountPlanner result-normalizer boundary | Done | Moved AccountPlanner LLM result cleanup, keyword-level normalization, platform-token stripping, search-only merge behavior, and IP portrait benchmark derivation into `nori.agents.user_profiling.account_planner.normalizer`. |
| Extract AccountPlanner portrait boundary | Done | Moved benchmark-account cleanup, IP portrait account names/keywords/pillars/creators/cover formats, and search-only benchmark creator refresh into `nori.agents.user_profiling.account_planner.portrait`. |
| Extract AccountPlanner keyword normalizer boundary | Done | Moved platform-token stripping, keyword-level normalization, reason fallback, search-keyword fallback, and dedupe into `nori.agents.user_profiling.account_planner.keywords`. |
| Centralize LLM fallback error formatter | Done | Added `nori.shared.attach_llm_error` and routed Intake, AccountPlanner, ops planners, and analyzer fallback through it. |
| Refine optional JSON fallback reasons | Done | `try_stage_json` preserves `empty_response` versus `parse_error` in fallback metadata with local shared-helper logic. |
| Add front-pipeline fallback metadata | Done | `IntakeResult` and `AccountPlanResult` now support optional metadata; Intake/AccountPlanner route optional JSON stages through `try_stage_json` and record redacted `llm_error` on fallback. |
| Share model coercion helpers | Done | Added shared coercion helpers under `nori.core.contracts` and migrated model `from_dict()` cleanup onto them. |
| Add model boolean coercion | Done | Added shared `bool_value()` and migrated persisted booleans such as `enable_search` / `llm_enhanced` off plain `bool(...)`. |
| Fold LLM runtime config/mode bridges into client core | Done | `ProviderConfig`, `ModelConfig`, and `ResolvedModel` are owned by `nori.core.contracts`; `nori.core.llms.client` owns the LLM config singleton, active-model access, direct/ghc mode switching, readiness checks, and client factories. The intermediate `config.py` and `mode.py` splits have been removed. |
| Extract runtime config normalization boundary | Done | Moved provider/model key parsing, env-name cleanup, mode normalization, core section validation, and flat/nested active-model selection into `nori.config_normalization`; `nori_config` and `nori.core.llms.client` reuse it. |
| Harden model config scalar coercion | Done | `NoriConfig` now normalizes model booleans, ints, floats, list options, and dict options before constructing `ModelConfig` / `ResolvedModel`. |
| Fail fast on malformed config sections | Done | Non-mapping YAML top level, `providers`, `models`, and individual provider/model entries now raise `NoriConfigError` instead of generic Python errors or silent empty defaults. |
| Harden scalar duration option parsing | Done | `duration_options: "10"` now restores as `[10]` instead of iterating the string character-by-character. |
| Normalize active model selection | Done | `active_models` now normalizes selected mode blocks, turns malformed shapes into explicit missing-usage errors, and prevents `NORI_MODE` from silently reusing `direct` when a mode block is absent. |
| Canonicalize active usage lookup | Done | `get_active(" llm ")` now trims the queried usage key before resolving the active model. |
| Align runtime mode normalization | Done | `nori.core.llms.current_mode`, `set_mode`, and `ensure_ready` now trim mode values so readiness probes and `NoriConfig` active selection agree. |
| Reject half-empty model keys | Done | `parse_model_key` now requires non-blank provider and model ids, so `openai::` / `::model` fail before client construction. |
| Canonicalize model key lookup | Done | `NoriConfig` now stores and resolves model keys as canonical `provider::model`, so segment whitespace cannot drop `ModelConfig` fields. |
| Require declared model configs | Done | `NoriConfig.resolve` now raises `KeyError: 未配置模型` when a provider exists but `models.<provider::model>` is missing, preventing silent default `ResolvedModel` construction. |
| Canonicalize provider and mode keys | Done | Provider ids, `mode`, `NORI_MODE`, and mode block keys are now trimmed before lookup; blank provider ids fail fast. |
| Canonicalize API key env names | Done | `api_key_env` and `${ENV_VAR}` placeholders now trim environment variable names before lookup and store `api_key_env` canonically. |
| Validate OpenAI-compatible client config | Done | Internal `nori.core.llms.client.get_client` / `get_async_client` raise `LLMClientConfigError` before SDK construction when active `api_key` or `base_url` is blank. |
| Share readiness/client config validation | Done | `ensure_ready` now reuses the same `validate_client_config` path as client factories, including `base_url` validation before ghc proxy probing. |
| Validate Google image API key before SDK dispatch | Done | Google native image generation now reuses shared `validate_api_key`, raising `LLMClientConfigError` and telemetry before `google-genai` construction when key is blank. |
| Eliminate image active-model double resolution | Done | `nori.core.llms.image` now uses `build_client_bundle` with the already-resolved model so capability checks and provider dispatch cannot drift across two active-model lookups. |
| Add generation artifact from_dict contracts | Done | `UserAsset`, `AssetBundle`, `CandidateTitle`, `NoteDraft`, and `CoverResult` now restore from persisted dict snapshots with regression coverage. |
| Add front-pipeline from_dict contracts | Done | `UserInput`, `IntakeResult`, `AccountPlannerInput`, and `AccountPlanResult` now restore from persisted dict snapshots with regression coverage. |
| Canonicalize UserAsset dict normalization | Done | NoteMaker and ContentProducer now delegate dict asset restoration to `UserAsset.from_dict()` instead of duplicating normalization logic. |
| Add XHS evidence from_dict contracts | Done | `XHSNoteSample` and `XHSSeedSkillDraft` now restore from persisted dict snapshots, including metric coercion for note samples. |

## P1 Account-Ops Backend

| Task | Status | Notes |
| --- | --- | --- |
| Ops dataclasses | Done | `AccountOperationProject` is the core project aggregate; `ClientBrief`, `OperationPlan`, `KPIPlan`, `ContentCalendar`, and `ContentTask` are core workflow contracts; `ContentPackage`, `ComplianceReview`, `MetricsSnapshot`, and `StrategyIteration` stay in their owning business modules. |
| Consolidate OperationPlanner package contract | Done | Canonical path is class-owned `nori.agents.planning.operation_planner.package`. |
| Extract OperationPlanner fallback builder boundary | Done | Canonical path is `nori.agents.planning.operation_planner.project_builder`. |
| Extract OperationPlanner fallback policy boundary | Done | Canonical path is `nori.agents.planning.operation_planner.project_policy`. |
| Extract OperationPlanner LLM normalizer boundary | Done | Canonical path is `nori.agents.planning.operation_planner.normalizer`. |
| Consolidate KPIPlanner package contract | Done | Canonical path is class-owned `nori.agents.planning.kpi_planner.package`. |
| Extract KPIPlanner normalizer boundary | Done | Canonical path is `nori.agents.planning.kpi_planner.normalizer`. |
| Consolidate CalendarPlanner package contract | Done | Canonical path is class-owned `nori.agents.planning.calendar_planner.package`. |
| Extract CalendarPlanner normalizer boundary | Done | Canonical path is `nori.agents.planning.calendar_planner.normalizer`. |
| Extract CalendarPlanner policy boundary | Done | Canonical path is `nori.agents.planning.calendar_planner.policy`. |
| Extract CalendarPlanner task builder boundary | Done | Canonical path is `nori.agents.planning.calendar_planner.task_builder`. |
| Operation/KPI/Calendar agents | Done | LLM path + fallback path covered by tests. |
| Ops planner fallback observability | Done | Operation/KPI/Calendar optional LLM calls now route through `try_stage_json`, request JSON mode, and record redacted `metadata.llm_error` on fallback. |
| Extract shared planner critic policy | Done | Canonical path is `nori.agents.planning.planner_critics`. |
| Asset library model | Done | `AssetRecord` / `AssetLibrary` now live in `nori.core.asset_models`; planning and context code import them from core. |
| Competitor research model | Done | Added `CompetitorSample` / `CompetitorResearch` with top-sample and task-reference helpers. |
| Account positioning model | Done | Added typed `AccountPositioning` with legacy dict compatibility and planner integration. |

## P3 Production Orchestration

| Task | Status | Acceptance |
| --- | --- | --- |
| Content task generation bridge | Done | `ContentTask -> NoteMakerAgent -> CoverDirectorAgent -> ContentPackage` covered by mocked tests. |
| Consolidate content package assembly | Done | Canonical path is `nori.agents.content_generation.content_producer.package.ContentPackageAssembler`. |
| Extract content production state boundary | Done | Canonical path is `nori.agents.content_generation.content_producer.state`. |
| Artifact index | Done | Package records note draft, cover result, prompts, material usage, and source refs. |
| Retry/error contract | Done | Generation failures attach structured error to task/project metadata before raising `ContentProductionError`. |

## P4 Review And Iteration

| Task | Status | Acceptance |
| --- | --- | --- |
| Compliance reviewer | Done | Produces `ComplianceReview` from `ContentPackage`, text-only first. |
| Consolidate review package contract | Done | Canonical path is class-owned `nori.agents.learning_loop.review.package`. |
| Extract review policy boundary | Done | Canonical path is `nori.agents.learning_loop.review.policy`. |
| Extract review scoring boundary | Done | Canonical path is `nori.agents.learning_loop.review.scoring`. |
| Extract review state boundary | Done | Canonical path is `nori.agents.learning_loop.review.state`. |
| Consistency reviewer | Done | Checks brief/title/body/cover prompt alignment. |
| Metrics snapshot workflow | Done | Manual metrics entry can attach to package/task/project. |
| Consolidate strategy iteration package contract | Done | Canonical path is class-owned `nori.agents.learning_loop.strategy.package`. |
| Extract strategy iteration policy boundary | Done | Canonical path is `nori.agents.learning_loop.strategy.policy`. |
| Extract strategy iteration state boundary | Done | Canonical path is `nori.agents.learning_loop.strategy.state`. |
| Strategy iteration agent | Done | Metrics + reviews -> `StrategyIteration.next_actions`. |

## Data Collection / Skill Learning

| Task | Status | Notes |
| --- | --- | --- |
| Stable mocked top-notes tests | Done | Covered by `tests/test_data_collect_top_notes.py`. |
| Redacted live runbook | Done | Added `wiki/refs/data-collection-live-runbook.md` for health checks, smoke commands, troubleshooting, and secret rules. |
| Skill report -> NoteMaker fixture bridge | Done | Added `load_note_skills`, `note_skill_fixture`, `write_note_skill_fixture`, and model `from_dict()` support. |
| Extract XHS note loader boundary | Done | Moved local note/author `meta.json` restoration, tag extraction, and platform metric count parsing into `nori.agents.market_analysis.xhs_note_analyzer.loader`. |
| Extract XHS single-note rule boundary | Done | Moved rule-only seed draft construction, scene/goal classification, content rule extraction, CTA evidence, and confidence scoring into `nori.agents.market_analysis.xhs_note_analyzer.rules`. |
| Consolidate XHS analyzer package contract | Done | Moved note enhancement, keyword, and label prompt contracts into class-owned `nori.agents.market_analysis.xhs_note_analyzer.package`; `note_llm` and `session_llm` now own call orchestration and output normalization only. |
| Extract XHS single-note LLM enhancement boundary | Done | Moved optional JSON routing, LLM output normalization, fallback draft marking, and `validation.llm_error` attachment into `nori.agents.market_analysis.xhs_note_analyzer.note_llm`. |
| Extract XHS session clustering boundary | Done | Moved rule-goal classification, required LLM-label validation, top-four bucket selection, tone majority, and leftover note tracking into `nori.agents.market_analysis.xhs_note_analyzer.session_clustering`. |
| Extract XHS session LLM boundary | Done | Moved keyword generation, hot-note prompt shaping, goal/tone label normalization, and fail-fast JSON helper routing into `nori.agents.market_analysis.xhs_note_analyzer.session_llm`. |
| Extract XHS session reporter boundary | Done | Moved report timestamping, full session report writing, and skills-only guide JSON writing into `nori.agents.market_analysis.xhs_note_analyzer.session_reporter`. |
| Extract XHS session skill-builder boundary | Done | Moved session `NoteSkill` construction, merged rules, evidence-note mapping, cover rules, metric percentiles, note-type majority, and cluster signals into `nori.agents.market_analysis.xhs_note_analyzer.skill_builder`. |
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
| Full frontend workbench | Backend case workbench data is now stable enough for UI integration: `workbench?case_id=...` returns diagnostics, case actions, `case_compare`, `case_delivery`, `active_run_artifacts`, and case-level launch/review links; `/experiments/content-production/cases` exposes case-level launch/review/replay/delivery/timeline/export links for selectors; `run_first_experiment` routes through the backend run-template; run-template, preflight, run results, failed-run payloads, and background jobs expose method/href/payload action contracts; `cases/{case_id}/replay` handles selected/best run reruns; `cases/{case_id}/evaluations/draft` and `/evaluations` handle case review writes; and `cases/{case_id}/delivery/export` provides the gated handoff zip. Remaining work is the actual frontend implementation under `web/`. |
