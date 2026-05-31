<!-- Last verified: 2026-06-01 | Current stage: P1 Account-Ops Backend -->

# Changelog

## 2026-06-01

| Change | Notes |
| --- | --- |
| Repaired runtime entrypoints | `main.py` now reports supported CLI/workflow entrypoints and can dispatch the Holly live workflow instead of importing the missing `nori.nori.server`. |
| Repaired live smoke imports | `scripts/smoke_note_maker.py` and `scripts/smoke_session_skill.py` now bootstrap the repo root and import canonical `nori.agents.*` / `nori.core` modules. |
| Added runtime entrypoint guards | Added subprocess tests for `main.py` and smoke-script `--help`, plus a stale-root scan covering removed legacy imports. |
| Renamed planning tests | Renamed `tests/test_context_building_*` files to current `planning_*`, `user_profiling_*`, and `market_analysis_*` names and added a guard against reintroducing the stale prefix. |
| Split core model ownership | Replaced the large `nori.core.models` implementation with focused owner modules: `profile_models`, `asset_models`, `planning_models`, and `capability_models`; `nori.core.models` is now a compatibility facade. |
| Moved module inventory to reference docs | Reduced `wiki/20-system-architecture.md` to runtime-layer decisions and moved detailed package/helper maps to `wiki/refs/module-map.md`. |
| Updated verification baseline | `python -m pytest tests -q` reports `503 passed, 3 skipped`. |

## 2026-05-26

| Change | Notes |
| --- | --- |
| Removed legacy contract compatibility modules | Deleted `nori.config_models`, `nori._model_coercion`, `nori.agents.planning.models`, `llms.errors`, and `llms.structured_models`; tests now assert these old import roots are absent. |
| Promoted LLM public contracts to core | Added `nori.core.contracts` as the owner for runtime config dataclasses, gateway errors, structured LLM result dataclasses, and shared model coercion helpers. |
| Made core exports lazy | `nori.core` now lazy-loads public contracts, domain models, runtime bases, workflow helpers, and architecture metadata, reducing import side effects while keeping existing public imports stable. |
| Guarded private contract imports | Added architecture coverage so runtime code imports public contracts from `nori.core` / `nori.core.contracts` instead of private compatibility modules. |
| Added core runtime bases | Added `nori.core.LLMFactory`, `AgentBase`, and `WorkflowBase`; concrete runtime agents now inherit `AgentBase`, and orchestration agents can share the same injectable LLM gateway. |
| Standardized domain facades as workflows | `UserProfilingFacade`, `MarketAnalysisFacade`, `ContextPackBuilder`, `ContentGenerationFacade`, and `LearningLoopFacade` now inherit `WorkflowBase` and expose stable `workflow_name` / `step_names` values. |
| Enforced core LLM injection boundary | Removed direct `llms` imports from workflow runtime stages; tests now patch the project gateway or inject factories, and architecture guards require stage code to route LLM access through `nori.core.LLMFactory`. |
| Promoted shared workflow contracts to core | Moved `AssetRecord`, `AssetLibrary`, `ClientBrief`, `OperationPlan`, `KPIPlan`, `ContentTask`, and `ContentCalendar` to `nori.core.models`; runtime code imports them from core. |
| Promoted project aggregate to core | Moved `AccountOperationProject` to `nori.core.project`; planning stages import it from core and no longer carry a model re-export layer. |
| Standardized stage package contracts | Stage-local `inputs.py`, `prompts.py`, and `refs.py` support files are now consolidated into class-owned `package.py` contracts where they only serve one agent; model contracts stay in canonical `models.py` files or `nori.core`. |
| Updated verification baseline | `python -m pytest tests -q` now reports `448 passed, 3 skipped` after adding core runtime abstraction tests, stage-support-module guards, the no-direct-`llms` runtime guard, shared workflow-contract ownership guards, project-aggregate ownership guards, and domain-facade workflow guards. |
| Removed legacy agent/model roots | Deleted `nori/gen_agents`, `nori/ops_agents`, `nori/ana_agents`, `nori/ops_models`, `nori/agent_models`, and `nori/agent_utils`; tests now assert those import roots are absent. |
| Removed canonical-package flat aliases | Removed flat helper aliases from workflow package roots and updated tests/docs to import each helper from its owning stage folder. |
| Tightened stage package roots | Replaced `import *` package re-exports with explicit public exports and moved monkeypatch tests to real entry modules. |
| Trimmed XHS analyzer orchestration file | Removed private pass-through helpers from the main analyzer file so rule, loader, LLM, clustering, reporting, and skill-building logic stay in their owning modules. |
| Trimmed agent entry orchestration wrappers | Removed no-value private pass-through helpers from generation, profiling, planning, review, strategy, and analyzer entry modules so orchestration calls owning helper modules directly. |
| Moved user-profiling model ownership | Moved `UserInput`, `IntakeResult`, `AccountPlannerInput`, and `AccountPlanResult` to `nori.agents.user_profiling.models`; added an architecture guard against imports from the removed old owner path. |
| Moved content-generation model ownership | Moved `AssetBundle`, `CandidateTitle`, `NoteDraft`, and `CoverResult` to `nori.agents.content_generation.models`; added an architecture guard against imports from the removed old owner path. |
| Promoted UserAsset to shared core contract | Moved `UserAsset` to `nori.core.models` because it is produced by Intake and consumed by generation; `nori.agents.content_generation.models` re-exports the same class for existing generation call sites. |
| Moved market-analysis model ownership | Moved `XHSNoteSample`, `XHSSeedSkillDraft`, `NoteEvidence`, `NoteSkill`, and `SessionSkillReport` to `nori.agents.market_analysis.models`; added an architecture guard against imports from the removed old owner path. |
| Removed agent model compatibility root | Deleted `nori/agent_models` and renamed model contract tests to `tests/test_domain_model_contracts.py`. |
| Moved shared runtime utilities | Moved case logging, image IO, and JSON LLM helpers to `nori/shared`; deleted `nori/agent_utils` and renamed utility tests to `tests/test_shared_utils.py`. |
| Moved NoteSkill fixture helper to market analysis | Moved `load_note_skills`, `note_skill_fixture`, and `write_note_skill_fixture` from `nori.shared` to `nori.agents.market_analysis.note_skill_fixture`; added a guard that `nori/shared` must not import business modules. |
| Renamed shared runtime helper surface | Replaced historical `call_agent_*`, `try_agent_*`, and `write_agent_log` names with stage-oriented `call_stage_*`, `try_stage_*`, and `write_stage_log`; renamed the architecture guard to `tests/test_workflow_folder_architecture.py`. |
| Centralized package-root lazy exports | Added `nori.core.lazy_exports.lazy_export` and routed five business package roots through one shared helper for facade/stage exports, preserving public imports without reintroducing domain-module cycles. |
| Renamed trace stage history field | `ExplanationTrace` now writes `stage_steps` and normalizes legacy `agent_steps` / row-level `agent` keys to `stage` during `from_dict()`. |
| Decoupled upstream facades from project aggregate internals | `UserProfilingFacade` and `MarketAnalysisFacade` now consume project-like dict/object shapes instead of importing `AccountOperationProject`; added dependency-direction guards. |
| Updated legacy-cleanup verification baseline | `python -m pytest tests -q` reported `434 passed, 3 skipped` after deleting legacy compatibility tests and adding export-boundary/lazy-export/trace-field/shared-boundary/dependency-direction/core-asset guards. |

## 2026-05-24

| Change | Notes |
| --- | --- |
| Migrated ops/analysis agent implementations | Moved concrete implementations into the five workflow modules. Superseded on 2026-05-26 by removal of the legacy roots. |
| Grouped stage files by owning stage package | Moved each concrete runtime stage into a folder with a specifically named entry module plus local helper modules and added `tests/test_workflow_folder_architecture.py` to prevent regression. |
| Initialized canonical wiki | Added product proposal, roadmap, glossary, architecture, design principles, API reference, conventions, stage docs, pitfalls, backlog, and changelog. |
| Captured current architecture | Documented LLM gateway, generation chain, account-ops backend, data collection, and live dependency boundaries. |
| Added wiki maintenance rules | Created `CLAUDE.md` with wiki synchronization guidance. |
| Restored default test baseline | Added Python 3.9 dataclass compatibility, restored Holly showcase fixture, and verified `python -m pytest tests -q` now passes. |
| Updated README canonical entry | README now points to `wiki/` as the source of truth and treats historical `文档/` notes as reference material. |
| Added P3 production bridge | Implemented `ContentProducerAgent` / `produce_content_package` for `ContentTask -> ContentPackage`, with prompt snapshots, material usage, source refs, and structured failure metadata. |
| Consolidated content package assembly | Replaced tiny `inputs` / `builder` / `refs` helper modules with class-based `ContentPackageAssembler` in `nori.agents.content_generation.content_producer.package`, inheriting shared stable artifact slug/dedupe behavior. |
| Extracted content production state boundary | Moved production error formatting, stage classification, and task/project success/failure metadata updates into `nori.agents.content_generation.content_producer.state`, with focused state tests. |
| Added P4 review gate | Implemented rule-based compliance and consistency reviewers returning `ComplianceReview`, with project attachment and offline tests. |
| Consolidated review package contract | Moved package/task/client-brief restoration and project-derived brief fallback into class-owned `nori.agents.learning_loop.review.package`, with focused package tests. |
| Extracted review policy boundary | Moved compliance/consistency issue calculation, score/status mapping, severity metadata, and fix suggestions into `nori.agents.learning_loop.review.policy`, with focused policy tests. |
| Extracted review scoring boundary | Moved issue-row construction, severity penalties, score/status mapping, severity counts, and deduped fix suggestions into `nori.agents.learning_loop.review.scoring`, with focused scoring tests. |
| Extracted review state boundary | Moved optional project compliance-review attachment into `nori.agents.learning_loop.review.state`, with focused state tests. |
| Consolidated XHS analyzer package contract | Moved note enhancement, keyword generation, and label prompt text into class-owned `nori.agents.market_analysis.xhs_note_analyzer.package`; `note_llm` and `session_llm` now use prompt builders instead of a shared `prompts.py` constants module. |
| Added P4 iteration loop | Implemented manual `MetricsSnapshot` recording and rule-based `StrategyIteration` creation from reviews + metrics. |
| Consolidated strategy iteration package contract | Moved review/metrics snapshot restoration and project-derived evidence fallback into class-owned `nori.agents.learning_loop.strategy.package`, with focused package tests. |
| Extracted strategy iteration policy boundary | Moved metric alias normalization, review/metric summaries, diagnosis, decisions, and next-action rules into `nori.agents.learning_loop.strategy.policy`, with focused policy tests. |
| Extracted strategy iteration state boundary | Moved metrics snapshot and strategy iteration project attachment into `nori.agents.learning_loop.strategy.state`, with focused state tests. |
| Consolidated OperationPlanner package contract | Moved `ClientBrief` / `AccountPlanResult` restoration, run-window normalization, and JSON-only SOP prompt construction into class-owned `nori.agents.planning.operation_planner.package`, with focused package tests. |
| Extracted OperationPlanner fallback builder boundary | Moved deterministic project fallback construction, rule-based tasks, calendar/KPI derivation, asset requirements, and benchmark references into `nori.agents.planning.operation_planner.project_builder`, with focused module tests. |
| Extracted OperationPlanner fallback policy boundary | Moved content-pillar/objective/topic/risk/reference derivation, default milestones, project labels, shared calendar policy reuse, and operation-derived KPI policy into `nori.agents.planning.operation_planner.project_policy`, with focused policy tests. |
| Extracted OperationPlanner LLM normalizer boundary | Moved operation-plan/calendar JSON merging, task-row normalization, date clamping, and derived KPI snapshot creation into `nori.agents.planning.operation_planner.normalizer`, with focused module tests. |
| Consolidated KPIPlanner package contract | Moved operation/project/composite-dict restoration, project-context derivation, and JSON-only KPI prompt construction into class-owned `nori.agents.planning.kpi_planner.package`, with focused package tests. |
| Extracted KPIPlanner normalizer boundary | Moved KPI fallback defaults, LLM KPI merge, milestone clamping, and empty measurement-note fallback preservation into `nori.agents.planning.kpi_planner.normalizer`, with focused module tests. |
| Consolidated CalendarPlanner package contract | Moved operation/project/composite-dict restoration, KPI/brief override normalization, run-window selection, and JSON-only calendar prompt construction into class-owned `nori.agents.planning.calendar_planner.package`, with focused package tests. |
| Extracted CalendarPlanner normalizer boundary | Moved calendar fallback construction, LLM task-row merge, scheduled-day clamping, empty-list fallback preservation, and task-count caps into `nori.agents.planning.calendar_planner.normalizer`, with focused module tests. |
| Extracted CalendarPlanner policy boundary | Moved bounded horizon/start-date rules, task-count limits, scheduled-date/day clamping, cadence/topic labels, and required asset fallback into `nori.agents.planning.calendar_planner.policy`, with focused policy tests. |
| Extracted CalendarPlanner task builder boundary | Moved fallback `ContentTask` row construction and LLM task-row cleanup into `nori.agents.planning.calendar_planner.task_builder`, with focused task-builder tests. |
| Extracted shared planner critic policy | Moved Operation/KPI/Calendar structural completeness checks, fallback warnings, task readiness checks, and KPI/calendar alignment into `nori.agents.planning.planner_critics`, with focused policy tests. |
| Added redacted LLM config contract | Added `api_config.example.yaml`, `wiki/refs/api-config.md`, `api_key_env` support, `NORI_CONFIG` fail-fast behavior, and config tests. |
| Added P1 evidence models | Implemented `AssetLibrary` and `CompetitorResearch` models with project nesting and serialization tests. |
| Added typed account positioning | Replaced loose project positioning dict with `AccountPositioning`, preserving legacy dict round trips and planner context compatibility. |
| Added NoteSkill fixture bridge | Added `NoteSkill` / `SessionSkillReport` deserialization plus `load_note_skills` and `write_note_skill_fixture` helpers for learned-skill reuse. |
| Added redacted data-collection runbook | Documented CookieBridge/sign/downloader health checks, live top-notes smoke, session-skill smoke, and stop conditions without secrets. |
| Extracted XHS note loader boundary | Moved local note/author `meta.json` restoration, tag extraction, and platform metric count parsing into `nori.agents.market_analysis.xhs_note_loader`, with focused loader tests. |
| Extracted XHS single-note rule boundary | Moved rule-only seed draft construction, scene/goal classification, content rule extraction, CTA evidence, and confidence scoring into `nori.agents.market_analysis.xhs_note_rules`, with focused rule tests. |
| Extracted XHS single-note LLM enhancement boundary | Moved optional single-note prompt text, JSON routing, model-output normalization, fallback draft marking, and `validation.llm_error` attachment into `nori.agents.market_analysis.xhs_note_llm`, with focused optional-stage tests. |
| Extracted XHS session clustering boundary | Moved rule-goal classification, required LLM-label validation, top-four bucket selection, tone majority, and leftover note tracking into `nori.agents.market_analysis.xhs_session_clustering`, with focused clustering tests. |
| Extracted XHS session LLM boundary | Moved keyword generation, hot-note prompt shaping, goal/tone label normalization, and fail-fast JSON helper routing into `nori.agents.market_analysis.xhs_session_llm`, with focused session LLM tests. |
| Extracted XHS session reporter boundary | Moved report timestamping, full session report writing, and skills-only guide JSON writing into `nori.agents.market_analysis.xhs_session_reporter`, with focused reporter tests. |
| Extracted XHS session skill-builder boundary | Moved session `NoteSkill` construction, merged rules, evidence-note mapping, cover rules, metric percentiles, note-type majority, and cluster signals into `nori.agents.market_analysis.xhs_skill_builder`, with focused builder tests. |
| Extracted LLM gateway errors | Added stable gateway exception classes and preserved package, call-module, and client-module imports as the same class identities. Superseded by core-contract ownership above. |
| Extracted LLM telemetry boundary | Moved redacted telemetry state and emit logic into `llms.telemetry`, keeping public `set_telemetry_sink` imports compatible. |
| Extracted LLM chat runner boundary | Moved sync/async chat client resolution, kwargs merge, capability guard, provider text extraction, and chat telemetry into `llms.chat_runner`, keeping `llms.call.chat` / `achat` as public facades. |
| Extracted LLM JSON parser boundary | Moved JSON object parsing into `llms.json_parser`, keeping package and call-module `parse_json_object` imports compatible. |
| Extracted LLM JSON-call boundary | Moved JSON-mode raw chat calls, response-format fallback, and retry classification into `llms.json_calls`, keeping legacy call-module helper aliases compatible. |
| Extracted LLM request-param boundary | Moved chat/image kwargs merging and token-limit normalization into `llms.request_params`, keeping legacy call-module helper aliases compatible. |
| Extracted LLM capability boundary | Moved chat/vision/image-reference capability guards into `llms.capabilities`, keeping legacy call-module helper aliases compatible. |
| Extracted LLM result boundary | Moved chat text and image URL/data-uri normalization into `llms.results`, keeping legacy call-module helper aliases compatible. |
| Extracted LLM image-input boundary | Moved reference-image bytes/data-uri/path/base64 normalization and MIME/data-uri helpers into `llms.image_inputs`, keeping legacy call-module helper aliases compatible. |
| Extracted LLM image-provider boundary | Moved OpenAI-compatible edit, relay reference-payload retry, and Google native image generation into `llms.image_providers`, keeping legacy call-module helper aliases compatible. |
| Extracted LLM image runner boundary | Moved active image-model resolution, reference input filtering, image capability guards, provider dispatch, result validation, and image telemetry into `llms.image_runner`, keeping `llms.call.image` as the public facade. |
| Extracted runtime config model boundary | Moved `ProviderConfig`, `ModelConfig`, and `ResolvedModel` behind a shared contract boundary, with `nori_config`, `llms.config`, and `llms.client` sharing the same dataclass contracts. |
| Extracted runtime config normalization boundary | Moved provider/model key parsing, env-name cleanup, mode normalization, section-shape validation, and active-model selection into `nori.config_normalization`, shared by `nori_config` and `llms.mode`. |
| Extracted structured LLM result model boundary | Moved `StructuredCallResult`, `IntentLLMResult`, and `TargetSelectionResult` behind a shared structured-model boundary, keeping package and legacy module import identities compatible. |
| Extracted structured LLM-output normalization | Moved shared string cleanup, parse-error reason classification, intent field-node normalization, selector option cleanup, confidence fallback, and alternative filtering for intent/target helpers into `llms.structured_outputs`, keeping legacy module-private helper aliases compatible. |
| Extracted structured LLM-call boundary | Moved non-throwing JSON-mode call handling, raw capture, parse-error classification, and provider-exception wrapping for intent/target helpers into `llms.structured_calls`, with focused helper tests. |
| Extracted structured LLM-prompt boundary | Moved intent field descriptions, enum/candidate prompt text, target selector catalogs, history formatting, and summary truncation into `llms.structured_prompts`, with focused prompt tests. |
| Hardened LLM helper JSON contracts | Added `chat_json(json_mode=True)` response-format fallback and refactored intent/target helpers onto the shared parser with offline tests. |
| Retired root progress tracker | Marked `进度.md` as historical and updated project-operator instructions to write current status into wiki/backlog. |
| Added chat result error contract | `llms.chat` / `achat` now raise `ChatResultError` and emit failure telemetry when provider responses contain no usable text content. |
| Normalized malformed chat results | Empty `choices` and missing `message.content` now raise `ChatResultError` for sync and async chat calls instead of leaking low-level response-shape errors. |
| Guarded image reference capability | Added `ImageCapabilityError` and tests so unsupported reference-image requests fail before provider SDK dispatch. |
| Added image result error contract | `llms.image` now raises `ImageResultError` and emits failure telemetry when provider responses contain no usable URL/base64 image. |
| Added redacted LLM telemetry hook | Added `set_telemetry_sink` with prompt-free model call metadata for chat, async chat, and image calls. |
| Made LLM kwargs merge side-effect-free | `_merge_kwargs` now copies caller `extra_body` before applying model-level fields, preventing hidden mutation of request kwargs. |
| Merged image model extra_body safely | OpenAI-compatible `llms.image` requests now apply model-level `extra_body` through an image-specific kwargs path without mutating caller kwargs or adding chat-only token/temperature fields. |
| Normalized token limit kwargs | `_merge_kwargs` now emits only the active model's expected token-limit parameter: `max_completion_tokens` for GPT-5 and `max_tokens` for other chat models, independent of whether a model-level `max_output` default exists. |
| Hardened embedded JSON parsing | `parse_json_object` now scans for the first valid embedded JSON object instead of greedily matching the first-to-last brace span, preventing extra prose or later objects from breaking valid LLM output. |
| Narrowed JSON-mode retry classification | `chat_json(json_mode=True)` no longer retries unrelated `unsupported` provider errors; fallback is limited to response-format or JSON-mode compatibility failures. |
| Narrowed JSON-mode TypeError retry classification | `chat_json(json_mode=True)` now retries TypeError only when it indicates `response_format` / JSON-mode incompatibility, preserving compatibility with older SDKs without hiding unrelated TypeErrors. |
| Aligned model capability metadata | Preserved video/audio fields on `ResolvedModel` and added active image model type validation. |
| Guarded chat/vision capability | Added `ChatCapabilityError` and tests so non-chat models, vision usage on non-vision models, and multimodal messages on non-vision models fail before provider SDK dispatch. |
| Centralized JSON raw capture | Added `chat_json_with_raw` and refactored intent/target helpers to retain original model text without duplicating `chat` wrapper logic. |
| Shared generation JSON wrapper | Added `nori.shared.call_stage_json` and routed NoteMaker/CoverDirector JSON stages through it with domain-specific error translation. |
| Shared pre-built messages JSON wrapper | Added `nori.shared.call_stage_messages_json` and routed Intake vision tagging through it so multimodal JSON stages also request JSON mode consistently. |
| Shared optional pre-built messages JSON wrapper | Added `nori.shared.try_stage_messages_json` and made `try_stage_json` delegate to it so optional custom/multimodal JSON stages share one fallback metadata contract. |
| Extracted Intake text-normalizer boundary | Moved deterministic text fallback, optional text-LLM output cleanup, alias mapping, image context construction, and missing/question fallback into `nori.agents.user_profiling.intaker.normalizer`, with focused module tests. |
| Extracted Intake taxonomy boundary | Moved goal/format/tone/asset/guardrail/data vocabularies, alias mapping, allowed-label cleanup, rule-based classification, and missing/question fallback text into `nori.agents.user_profiling.intaker.taxonomy`, with focused taxonomy tests. |
| Extracted Intake image tagger boundary | Moved per-image vision prompt construction, parallel dispatch, failure isolation, and tag filtering into `nori.agents.user_profiling.intaker.image_tagger`, with focused module tests. |
| Consolidated NoteMaker package contract | Moved skill selection, asset curation, note composition, prompt construction, selected-index normalization, and note-field cleanup into class-owned `nori.agents.content_generation.note_maker.package`, with focused package tests. |
| Consolidated CoverDirector package contract | Moved tagged-asset reference selection, legacy draft/reference collection, reference input conversion, and cover prompt construction into class-owned `nori.agents.content_generation.cover_director.package`, with focused package tests. |
| Extracted CoverDirector output boundary | Moved data-uri/http image persistence and output error translation into `nori.agents.content_generation.cover_director.output`, with focused module tests. |
| Consolidated AccountPlanner package contract | Moved `AccountPlannerInput` restoration, image/link evidence merging, asset prompt context, and JSON-only account prompt construction into class-owned `nori.agents.user_profiling.account_planner.package`, with focused package tests. |
| Extracted AccountPlanner fallback boundary | Moved deterministic no-inference fallback result construction into `nori.agents.user_profiling.account_planner.fallback`, with focused fallback tests. |
| Extracted AccountPlanner search boundary | Moved search provider protocol/fallback, keyword cleanup/dedupe, platform id normalization, provider-error isolation, and search row defaulting into `nori.agents.user_profiling.account_planner.search`, with focused search tests. |
| Extracted AccountPlanner result-normalizer boundary | Moved AccountPlanner output cleanup, keyword normalization, search-only merge behavior, and IP portrait benchmark derivation into `nori.agents.user_profiling.account_planner.normalizer`, with focused module tests. |
| Extracted AccountPlanner portrait boundary | Moved benchmark-account cleanup, IP portrait account names/keywords/pillars/creators/cover formats, and search-only benchmark creator refresh into `nori.agents.user_profiling.account_planner.portrait`, with focused portrait tests. |
| Extracted AccountPlanner keyword normalizer boundary | Moved platform-token stripping, keyword-level normalization, reason fallback, search-keyword fallback, and dedupe into `nori.agents.user_profiling.account_planner.keywords`, with focused keyword tests. |
| Centralized fallback error formatter | Added `nori.shared.attach_llm_error`, removed duplicate per-agent `llm_error` formatter helpers, routed analyzer fallback through the same helper, and made caller stage authoritative. |
| Refined optional JSON fallback reasons | `try_stage_json` now reuses `llms.structured_outputs.chat_json_error_reason`, so fallback metadata distinguishes empty model responses from malformed JSON. |
| Added ops planner fallback observability | Added `try_stage_json` and routed Operation/KPI/Calendar optional LLM stages through it so fallback artifacts retain redacted `llm_error` metadata. |
| Added front-pipeline fallback metadata | Added optional metadata on `IntakeResult` and `AccountPlanResult`, and routed Intake/AccountPlanner optional JSON stages through `try_stage_json`. |
| Added analyzer fallback observability | Routed `XHSNoteAnalyzer.analyze_note` optional LLM enhancement through `try_stage_json` and replaced raw exception strings with structured `validation.llm_error`. |
| Routed analyzer session JSON stages through shared helper | `collect_for_session` keyword generation and note labeling now use `call_stage_json(json_mode=True)` and fail fast through `XHSNoteAnalyzerLLMError` / session validation checks. |
| Shared model coercion helpers | Added shared model coercion helpers and routed ops/skill model `from_dict()` normalization through them to avoid drift between duplicated private helpers. |
| Added generation artifact restoration | Added `from_dict()` round trips for `UserAsset`, `AssetBundle`, `CandidateTitle`, `NoteDraft`, and `CoverResult` so package prompt snapshots can be restored without ad hoc parsing. |
| Added front-pipeline restoration | Added `from_dict()` round trips for `UserInput`, `IntakeResult`, `AccountPlannerInput`, and `AccountPlanResult` so intake and account-planning snapshots can be restored before ops handoff. |
| Canonicalized asset dict normalization | Routed NoteMaker and ContentProducer dict assets through `UserAsset.from_dict()` instead of local reconstruction helpers. |
| Added XHS evidence restoration | Added `from_dict()` round trips for `XHSNoteSample` and `XHSSeedSkillDraft` so collected evidence and seed drafts can be restored without ad hoc parsing. |
| Added boolean model coercion | Added shared `bool_value` and routed persisted model booleans through it so string values like `"false"` restore correctly. |
| Hardened config model coercion | `NoriConfig` now coerces model scalar/list/dict fields from YAML before they reach LLM capability guards and kwargs merging. |
| Added explicit config structure errors | Non-mapping YAML top level, `providers`, `models`, and individual provider/model entries now raise `NoriConfigError`, and active usage lookup trims the queried usage key before resolution. |
| Hardened duration option coercion | Added shared `int_list` coercion so scalar config values such as `duration_options: "10"` become `[10]`. |
| Normalized active model selection | `NoriConfig` now normalizes selected `active_models` blocks and reports malformed shapes, blank active keys, invalid scalar keys, and missing `NORI_MODE` blocks through explicit config errors. |
| Aligned runtime mode normalization | `llms.current_mode`, `set_mode`, and `ensure_ready` now trim mode values so environment whitespace cannot make readiness checks diverge from `NoriConfig` active model selection. |
| Rejected half-empty model keys | `parse_model_key` now requires non-blank provider and model ids after trimming, so malformed keys such as `openai::` and `::model` fail at the config boundary. |
| Canonicalized model key lookup | `NoriConfig` now stores and resolves model keys as canonical `provider::model`, preventing segment whitespace from dropping configured model capability fields. |
| Required declared model configs | `NoriConfig.resolve` now raises `KeyError: 未配置模型` for provider-backed but undeclared model keys instead of constructing a default `ResolvedModel`. |
| Canonicalized provider and mode keys | Provider ids, `mode`, `NORI_MODE`, and mode block keys are now trimmed before lookup, and blank provider ids fail fast. |
| Canonicalized API key env names | `api_key_env` and `${ENV_VAR}` placeholders now trim environment variable names before lookup and store provider `api_key_env` canonically. |
| Validated OpenAI-compatible client config | `llms.get_client` and `get_async_client` now raise `LLMClientConfigError` before SDK construction when active provider `api_key` or `base_url` is blank. |
| Shared readiness/client config validation | `llms.ensure_ready` now reuses `validate_client_config`, so readiness checks and actual OpenAI-compatible client construction agree on blank `api_key` / `base_url` failures. |
| Validated Google image API key before SDK dispatch | Google native image generation now reuses shared `validate_api_key`, so blank API keys fail with `LLMClientConfigError` and redacted telemetry before `google-genai` construction. |
| Eliminated image active-model double resolution | `llms.image` now constructs OpenAI-compatible image clients from the already-resolved model, keeping capability checks and provider dispatch bound to the same model. |
