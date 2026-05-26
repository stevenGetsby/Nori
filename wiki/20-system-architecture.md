<!-- Last verified: 2026-05-26 | Current stage: P1 Account-Ops Backend -->

# System Architecture

## Repository Shape

| Path | Role |
| --- | --- |
| `nori/` | Product workflow modules, shared contracts, runtime helpers, and config loader. |
| `nori/domain.py` | Public aggregate entrypoint for the domain architecture: `build_domain_snapshot()` and `validate_domain_snapshot()`. |
| `nori/core/` | Shared domain contracts, runtime base classes, public LLM/config contracts, architecture registry, and package-root lazy-export helper for public module APIs. |
| `nori/user_profiling/` | `facade.py` for long-lived user/account/brand/preference profile construction; package `__init__` keeps lightweight model exports eager and routes stage/facade exports through `nori.core.lazy_exports`. |
| `nori/market_analysis/` | `facade.py` for competitor/hot-example/trend evidence as market analysis; package `__init__` keeps lightweight model exports eager and routes analyzer/facade exports through `nori.core.lazy_exports`. |
| `nori/context_building/` | Canonical context-building module: operation/KPI/calendar planning, planner critics, content task construction, and unified `ContextPack` assembly. |
| `nori/content_generation/` | Canonical content-generation module: content production bridge, package input/builder/provenance/state helpers, candidate sets, and lazy public stage exports. |
| `nori/learning_loop/` | Canonical learning-loop module: review gates, review policy/scoring/state, metrics snapshots, strategy iteration, domain snapshots, and lazy public stage exports. |
| `llms/` | Project-level LLM gateway and utilities. |
| `nori/_compat.py` | Small runtime compatibility layer for dataclass features used by shared models and LLM result objects. |
| `nori/config_normalization.py` | Pure runtime-config normalization helpers for provider/model keys, env names, mode names, core section shapes, and active model maps. |
| `data_collect/` | Unified crawler/sign/downloader integration layer. |
| `tests/` | Unit and mocked integration tests. Live tests should be opt-in. |
| `scripts/` | Smoke scripts for live/session-level workflows. |
| `文档/` | Historical design notes and project-specific skill source. Wiki is now the canonical project map. |
| `view/` | Static demo artifact; not current product architecture. |

## Runtime Layers

```text
Input / assets
  -> nori.user_profiling.IntakeAgent
  -> nori.user_profiling.AccountPlannerAgent
  -> nori.context_building.{OperationPlanner,KPIPlanner,CalendarPlanner}
  -> nori.content_generation.ContentProducerAgent
  -> nori.content_generation.NoteMakerAgent
  -> nori.content_generation.CoverDirectorAgent
  -> nori.content_generation.models.ContentPackage
  -> nori.learning_loop.ReviewGateAgent
  -> nori.learning_loop.{MetricsSnapshotAgent,StrategyIterationAgent}
  -> nori.learning_loop.models.ComplianceReview / MetricsSnapshot / StrategyIteration
```

## Domain Architecture

Nori's high-level product architecture is organized as one shared layer plus five business modules. The canonical implementation now lives in these five packages; the old agent/model roots have been removed.

```text
nori.core
  -> nori.user_profiling
  -> nori.market_analysis
  -> nori.context_building
  -> nori.content_generation
  -> nori.learning_loop
```

| Domain module | Public contract | Current facade | Backing implementation |
| --- | --- | --- | --- |
| Shared core | `UserProfile`, `UserAsset`, `AssetRecord`, `AssetLibrary`, `ClientBrief`, `OperationPlan`, `KPIPlan`, `ContentTask`, `ContentCalendar`, `AccountOperationProject`, `MarketAnalysis`, `ContextPack`, `DecisionPoint`, `ExplanationTrace`, `CandidateSet`, `PerformanceSnapshot`, `LearningSignal`, `DomainSnapshot` | `nori.core` | Provider-free dataclasses with `to_dict/from_dict`; `UserAsset`, asset library, brief, plan, KPI, task, calendar, and account-operation project contracts are cross-stage contracts; `ExplanationTrace` writes `stage_steps` and only reads legacy `agent_steps`; `DomainSnapshot` includes `validate()` / `is_valid()` quality gates; `nori.core.architecture` exposes `DOMAIN_MODULES`, `DomainModule`, `domain_module_names()`, and `get_domain_module()`. |
| User profiling | Long-lived user/account/brand/preference profile | `nori.user_profiling.facade.UserProfilingFacade` | `nori.user_profiling.models` owns `UserInput`, `IntakeResult`, `AccountPlannerInput`, `AccountPlanResult`, and `AccountPositioning`. Image tagging returns `nori.core.UserAsset` without importing content generation. |
| Market analysis | Competitor samples, hot examples, trend/audience insights | `nori.market_analysis.facade.MarketAnalysisFacade` | `nori.market_analysis.models` owns `CompetitorResearch`, `CompetitorSample`, `XHSNoteSample`, `XHSSeedSkillDraft`, `NoteEvidence`, `NoteSkill`, and `SessionSkillReport`; evidence can come from `DataCollector` and `XHSNoteAnalyzer`. |
| Context building | Operation project assembly, KPI/calendar planning, unified generation context, and xAI evidence trace | `nori.context_building.{OperationPlannerAgent,KPIPlannerAgent,CalendarPlannerAgent,ContextPackBuilder}` | Context-building stages import cross-stage contracts directly from `nori.core`; shared `ContextPack` also lives in `nori.core`. |
| Content generation | Content package production and candidate set before final human selection | `nori.content_generation.{ContentProducerAgent,ContentGenerationFacade}` | `nori.content_generation.models` owns `AssetBundle`, `CandidateTitle`, `NoteDraft`, `CoverResult`, and `ContentPackage`. Shared assets/tasks come from `nori.core.UserAsset` and `nori.core.ContentTask`. |
| Learning loop | Review gates, monitoring snapshots, and preference/strategy update signals | `nori.learning_loop.{ReviewGateAgent,MetricsSnapshotAgent,StrategyIterationAgent,LearningLoopFacade}` | `nori.learning_loop.models` owns `ComplianceReview`, `MetricsSnapshot`, `StrategyIteration`; review/metric evidence feeds `nori.core` learning contracts. |

Design rule: new cross-stage behavior should add a shared `nori.core` contract or one of the five domain facades before adding another standalone agent.

Upper-layer rule: CLI/API/UI code should prefer `nori.domain.build_domain_snapshot()` and `nori.domain.validate_domain_snapshot()` when it needs the complete five-module view. Use individual facades only when the caller is intentionally working inside one domain module.

Projection bridge: the five domain facades can project an existing `AccountOperationProject` into the current architecture. `AccountOperationProject` lives in `nori.core.project`; `UserProfilingFacade` and `MarketAnalysisFacade` consume project-like dict/object shapes without importing context-building internals, keeping upstream modules independent from the context-building implementation.

| Projection | Purpose |
| --- | --- |
| `UserProfilingFacade.build_from_project(project)` | Converts client brief and account positioning into `UserProfile`. |
| `MarketAnalysisFacade.build_from_project(project)` | Converts competitor research into `MarketAnalysis`. |
| `ContextPackBuilder.build_from_project(project, task_id=...)` | Builds a task-level `ContextPack` from project profile, market, task, and assets. |
| `ContentGenerationFacade.candidate_set_from_project(project, task_id=...)` | Converts task packages into a `CandidateSet` linked to context trace input refs. |
| `LearningLoopFacade.performance_snapshots_from_project(project)` | Converts project metrics into `PerformanceSnapshot[]`. |
| `LearningLoopFacade.learning_signals_from_project(project, ...)` | Converts strategy iterations into `LearningSignal[]`. |
| `LearningLoopFacade.domain_snapshot_from_project(project, ...)` | Aggregates the full five-module projected view into a round-trippable `DomainSnapshot`. |

`DomainSnapshot.validate()` currently guards required module coverage, candidate-set/context alignment, and selected-candidate integrity. This is the shared quality gate for future CLI/API/UI consumers of the new architecture.

## LLM Gateway

| Module | Responsibility |
| --- | --- |
| `nori/core/contracts.py` | Public runtime contract boundary shared by Nori core and the LLM gateway: provider/model config rows, resolved active models, gateway exception classes, structured-helper result dataclasses, and provider-free model coercion helpers. |
| `nori/nori_config.py` | Locate `api_config.yaml`, parse providers/models/active usages, coerce model scalar fields, resolve `api_key_env`, apply `NORI_MODE`, and assemble config model contracts. |
| `nori/config_normalization.py` | Pure config normalization boundary shared by `nori.nori_config` and `llms.mode`: canonical provider/model keys, env names, mode keys, section-shape validation, and nested/flat `active_models` selection. |
| `llms/config.py` | Singleton bridge to `NoriConfig`. |
| `llms/telemetry.py` | Process-local redacted telemetry sink and emit helper. Public imports from `llms` and `llms.call` re-export the same `set_telemetry_sink` function. |
| `llms/chat_runner.py` | Sync/async chat execution boundary: resolves clients, merges chat kwargs, applies chat/vision capability guards, extracts provider text, and emits redacted telemetry for `chat` / `achat`. |
| `llms/json_parser.py` | Shared parser for full, fenced, and embedded JSON object responses. Public imports from `llms` and `llms.call` re-export the same `parse_json_object` function. |
| `llms/json_calls.py` | Shared JSON-mode raw chat-call helper, `response_format` fallback, and retry classification. |
| `llms/request_params.py` | Shared request-parameter merger for chat/image calls, including token-limit normalization and side-effect-free `extra_body` merging. |
| `llms/capabilities.py` | Shared capability guards for chat model type, vision usage, multimodal messages, image model type, and reference-image support. |
| `llms/results.py` | Shared provider-response normalization for chat text and image URL/data-uri extraction, including stable empty-result errors. |
| `llms/image_inputs.py` | Shared image input normalization for bytes, data-uri, local path, base64 strings, MIME sniffing, and data-uri construction. |
| `llms/image_providers.py` | Provider-specific image request helpers for OpenAI-compatible edit, relay reference-payload retry, and Google native image generation. |
| `llms/image_runner.py` | Image execution boundary: resolves active image model, normalizes reference inputs, applies image capability guards, dispatches Google/relay/OpenAI-compatible providers, validates result emptiness, and emits redacted telemetry for `image`. |
| `llms/structured_outputs.py` | Shared string cleanup, parse-error classification, intent field-node normalization, selector-option cleanup, confidence normalization, and alternative-selector filtering for structured LLM utilities. |
| `llms/structured_calls.py` | Shared non-throwing JSON call boundary for structured LLM utilities: returns `data/raw/error`, classifies parse failures, and wraps provider exceptions for intent/target helpers. |
| `llms/structured_prompts.py` | Shared prompt-construction boundary for structured LLM utilities: owns intent field descriptions, enum/candidate instructions, target-selector catalogs, history formatting, and summary truncation. Legacy module-private prompt-builder wrappers stay stable. |
| `llms/client.py` | Build sync/async OpenAI-compatible clients, including builders for already-resolved models, and provide shared `api_key` / `base_url` validation before provider SDK construction. |
| `llms/call.py` | Public facade for `chat`, `achat`, `chat_json`, `chat_json_with_raw`, and `image`. It delegates chat execution, image execution, parsing, JSON-call retry plumbing, telemetry, errors, request-parameter merging, capability policy, result normalization, image input normalization, and image provider dispatch to dedicated gateway modules. |
| `llms/mode.py` | Switch `direct`/`ghc`; reuse shared mode normalization and client config validation, then preflight local proxy `/models` in `ghc` mode. |
| `llms/intent_extractor.py` | Optional P1 intent extraction helper; fails as structured result, not exception, and reuses shared structured prompt, output-normalization, and call-error boundaries. |
| `llms/target_selector.py` | Optional edit-target selector; consumes candidate selectors, returns confidence, and reuses shared structured prompt, output-normalization, and call-error boundaries. |

Config lookup order:

```text
NORI_CONFIG
-> ./api_config.yaml
-> nori/api_config.yaml
-> repo_root/api_config.yaml
```

Known current state: local root `api_config.yaml` exists. Status scripts should report only redacted active model names, not provider secrets.

Committed config artifacts:

| Path | Role |
| --- | --- |
| `api_config.example.yaml` | Redacted provider/model/active model template. |
| `wiki/refs/api-config.md` | Config contract, lookup order, secret rules, and validation commands. |

## Generation Core

| Agent | Input | Output | Boundary |
| --- | --- | --- | --- |
| `IntakeAgent` | `UserInput(text, images)` | `IntakeResult(intention, context, missing, questions, assets)` | Only layer that performs image understanding / vision tagging. |
| `NoteMakerAgent` | `NoteSkill[]`, `UserAsset[]`, intent/context | `NoteDraft` | Only writes note copy/title/tags; does not read original image bytes. |
| `CoverDirectorAgent` | `NoteDraft`, selected skill, tagged assets | `CoverResult` | Only layer that calls image generation and reads reference image bytes. |
| `AccountPlannerAgent` | `AccountPlannerInput` or raw input/assets/links | `AccountPlanResult` | Produces account positioning and IP portrait; search provider is pluggable. |

`IntakeResult` and `AccountPlanResult` include optional `metadata` for non-contract control-plane facts such as LLM fallback errors. Empty metadata is omitted from `to_dict()` output to preserve compact fixtures.

Workflow stage package layout:

| Stage package | Implementation files |
| --- | --- |
| `nori/user_profiling/intaker/` | `intaker.py`, `prompts.py`, `schema.py`, `normalizer.py`, `taxonomy.py`, `image_tagger.py` |
| `nori/user_profiling/account_planner/` | `account_planner.py`, `prompts.py`, `schema.py`, `inputs.py`, `fallback.py`, `search.py`, `normalizer.py`, `portrait.py`, `keywords.py` |
| `nori/content_generation/note_maker/` | `note_maker.py`, `prompts.py`, `schema.py`, `skill_picker.py`, `asset_curator.py`, `note_composer.py` |
| `nori/content_generation/cover_director/` | `cover_director.py`, `prompts.py`, `schema.py`, `refs.py`, `output.py` |
| `nori/content_generation/content_producer/` | `content_producer.py`, `prompts.py`, `schema.py`, `inputs.py`, `builder.py`, `refs.py`, `state.py` |
| `nori/context_building/operation_planner/` | `operation_planner.py`, `prompts.py`, `schema.py`, `inputs.py`, `project_builder.py`, `project_policy.py`, `normalizer.py` |
| `nori/context_building/kpi_planner/` | `kpi_planner.py`, `prompts.py`, `schema.py`, `inputs.py`, `normalizer.py` |
| `nori/context_building/calendar_planner/` | `calendar_planner.py`, `prompts.py`, `schema.py`, `inputs.py`, `normalizer.py`, `policy.py`, `task_builder.py` |
| `nori/learning_loop/review/` | `review_gate.py`, `prompts.py`, `schema.py`, `inputs.py`, `policy.py`, `scoring.py`, `state.py` |
| `nori/learning_loop/strategy/` | `strategy_iteration.py`, `prompts.py`, `schema.py`, `inputs.py`, `policy.py`, `state.py` |
| `nori/market_analysis/xhs_note_analyzer/` | `xhs_note_analyzer.py`, `prompts.py`, `schema.py`, `loader.py`, `rules.py`, `note_llm.py`, `session_clustering.py`, `session_llm.py`, `session_reporter.py`, `skill_builder.py` |

Flat helper module paths such as `nori.content_generation.skill_picker` and `nori.context_building.operation_planner_inputs` should not exist. New implementation code and imports should live inside the owning stage package.

Shared generation utilities:

| Module | Role |
| --- | --- |
| `nori/core/contracts.py` | Public contract owner for runtime config models, LLM gateway errors, structured LLM helper result models, and model `from_dict()` coercion helpers. |
| `nori/core/llm.py` | `LLMFactory` is the injectable project LLM gateway used by agents instead of reaching directly into `llms` in constructors or orchestration code. |
| `nori/core/agent.py` | `AgentBase` standardizes `stage_name`, `use_llm`, `llm_factory`, and required/optional JSON helper methods while preserving each agent's domain-specific `run(...)` signature. |
| `nori/core/workflow.py` | `WorkflowBase` provides a small ordered-step runner for agents and domain facades that compose multiple substages; `named_workflow_steps(...)` lets facades declare readable no-op stage names when their public methods own execution. All five business facades expose this shared workflow contract through `workflow_name` and `step_names`. |
| `nori/shared/llm_json.py` | `call_stage_json` wraps `llms.chat_json(json_mode=True)` for required generation stages and translates parse/provider errors into the caller's domain exception. |
| `nori/shared/llm_json.py` | `call_stage_messages_json` applies the same required-stage contract to pre-built messages, including multimodal vision messages. |
| `nori/shared/llm_json.py` | `try_stage_json` is the system/user convenience wrapper for optional JSON LLM stages, delegating to the same pre-built-message fallback path. |
| `nori/shared/llm_json.py` | `try_stage_messages_json` wraps optional pre-built-message JSON stages, returning `(data, error)` so planners can keep deterministic fallback; parse errors reuse `llms.structured_outputs.chat_json_error_reason`. |
| `nori/shared/llm_json.py` | `attach_llm_error` is the canonical formatter for redacted fallback errors: `{metadata|validation}.llm_error = {reason, error_type, stage, ...}` with caller stage kept authoritative. |
| `nori/user_profiling/intaker/normalizer.py` | Intake-owned text normalization boundary: owns deterministic text fallback, optional LLM output cleanup, image context construction, and metadata preservation while delegating taxonomy mechanics. |
| `nori/user_profiling/intaker/taxonomy.py` | Intake-owned taxonomy boundary: stores goal/format/tone/asset/guardrail/data vocabularies, alias maps, rule-based text classification, allowed-label cleanup, missing-field repair, and question fallback text. |
| `nori/user_profiling/intaker/image_tagger.py` | Intake-owned vision tagging boundary: builds multimodal per-image JSON messages, isolates per-image failures, filters tag vocabularies, and returns `UserAsset` records. `intaker.py` keeps compatibility facades for existing call sites. |
| `nori/market_analysis/note_skill_fixture.py` | Market-analysis-owned learned-skill fixture bridge: converts `SessionSkillReport` / `NoteSkill` objects to the skills-only JSON shape consumed by NoteMaker tests and smoke scripts. |
| `nori/content_generation/note_maker/skill_picker.py` | NoteMaker-owned skill selection boundary: builds compact candidate summaries, routes the required JSON call through the injected stage helper, and translates unknown `skill_id` into the caller's domain error. |
| `nori/content_generation/note_maker/asset_curator.py` | NoteMaker-owned asset curation boundary: builds asset-curation JSON prompts, normalizes selected asset indices into `AssetBundle`, caps gallery paths, and keeps `note_maker.py` focused on stage orchestration and note composition. |
| `nori/content_generation/note_maker/note_composer.py` | NoteMaker-owned composition boundary: builds note-composition JSON prompts, normalizes candidate titles/tags/validation, and translates missing title/body into the caller's domain error. |
| `nori/content_generation/cover_director/refs.py` | CoverDirector-owned reference selection boundary: preserves legacy draft/reference-asset path collection and tagged-assets LLM selection while keeping `cover_director.py` focused on orchestration, prompt writing, and image output. |
| `nori/content_generation/cover_director/prompts.py` | CoverDirector-owned prompt-writing boundary: builds the image-generation prompt JSON call from `NoteDraft`, skill rules, intent, and selected reference count, and translates empty prompt responses into the caller's domain error. |
| `nori/content_generation/cover_director/output.py` | CoverDirector-owned image output boundary: persists data-uri or remote image payloads, sanitizes cover filenames, and translates base64/download failures into the caller's domain error. |
| `nori/user_profiling/account_planner/inputs.py` | AccountPlanner-owned input boundary: restores/merges `AccountPlannerInput`, extra images/links, platform defaults, and per-image prompt context. |
| `nori/user_profiling/account_planner/prompts.py` | AccountPlanner-owned prompt boundary: stores the JSON-only account-planning prompt contract and serializes normalized text, image/link evidence, intention/context, and optional search results for LLM drafting. |
| `nori/user_profiling/account_planner/fallback.py` | AccountPlanner-owned deterministic fallback boundary: builds the non-inferential `AccountPlanResult` shell with platform/goal tags and empty benchmark/IP portrait sections. |
| `nori/user_profiling/account_planner/search.py` | AccountPlanner-owned search boundary: defines search provider protocol/fallback, cleans and dedupes planner keywords, isolates provider errors, and normalizes search result defaults. |
| `nori/user_profiling/account_planner/normalizer.py` | AccountPlanner-owned result normalization boundary: converts LLM JSON/search evidence into `AccountPlanResult`, delegates keyword and portrait mechanics, and preserves fallback metadata. |
| `nori/user_profiling/account_planner/portrait.py` | AccountPlanner-owned IP portrait boundary: normalizes benchmark account rows, account keywords, content pillars, benchmark creators, and cover design formats for LLM and search-only planner output. |
| `nori/user_profiling/account_planner/keywords.py` | AccountPlanner-owned keyword normalization boundary: strips platform tokens, normalizes three-level keyword rows, applies reason fallbacks, derives search-keyword fallbacks, and dedupes keyword output. |

## Account-Ops Backend

| Module | Role |
| --- | --- |
| `nori/user_profiling/models.py` | Canonical user/account profile models: `AccountPositioning`, `UserInput`, `IntakeResult`, `AccountPlannerInput`, and `AccountPlanResult`. |
| `nori/market_analysis/models.py` | Canonical market evidence models: `CompetitorSample`, `CompetitorResearch`. |
| `nori/content_generation/models.py` | Canonical generated artifact model: `ContentPackage`. |
| `nori/learning_loop/models.py` | Canonical review/monitoring/evolution models: `ComplianceReview`, `MetricsSnapshot`, `StrategyIteration`. |
| `nori/core/models.py` | Canonical owner for cross-stage workflow contracts: `AssetRecord`, `AssetLibrary`, `ClientBrief`, `OperationPlan`, `KPIPlan`, `ContentCalendar`, and `ContentTask`. |
| `nori/core/project.py` | Canonical owner for the cross-module `AccountOperationProject` aggregate, with lazy coercion into each business module's concrete nested models. |
| `nori/context_building/operation_planner/operation_planner.py` | `ClientBrief + AccountPlanResult -> AccountOperationProject`; owns orchestration, LLM request, fallback selection, and critic attachment. |
| `nori/context_building/operation_planner/inputs.py` | OperationPlanner input boundary: restores `ClientBrief`/`AccountPlanResult` inputs from dicts, normalizes planner start dates and horizons, and serializes optional account plans for prompts. |
| `nori/context_building/operation_planner/prompts.py` | OperationPlanner prompt boundary: stores the JSON-only SOP planning prompt contract and serializes normalized client briefs, optional account plans, and bounded horizons for LLM drafting. |
| `nori/context_building/operation_planner/project_builder.py` | OperationPlanner deterministic fallback assembly boundary: builds rule-based operation projects, tasks, calendars, and derived KPI snapshots while delegating pure fallback policy. |
| `nori/context_building/operation_planner/project_policy.py` | OperationPlanner pure policy boundary: derives account positioning, content pillars, objectives, risk controls, topic pools, references, milestones, project IDs/titles, and operation-derived KPI plans without constructing a project shell. |
| `nori/context_building/operation_planner/normalizer.py` | OperationPlanner-owned LLM output normalization boundary: merges operation plan/calendar JSON into a fallback project shell, normalizes LLM task rows, clamps milestone/task dates, and derives KPIPlan snapshots. |
| `nori/context_building/kpi_planner/kpi_planner.py` | `OperationPlan -> KPIPlan`. |
| `nori/context_building/kpi_planner/inputs.py` | KPIPlanner input boundary: restores `OperationPlan` / `AccountOperationProject` / composite dict inputs and derives project context such as project id, client brief, and content task count. |
| `nori/context_building/kpi_planner/prompts.py` | KPIPlanner prompt boundary: stores the JSON-only KPI planning prompt contract and serializes normalized operation plans plus project context for LLM drafting. |
| `nori/context_building/kpi_planner/normalizer.py` | KPIPlanner-owned normalization boundary: builds deterministic KPI fallback, merges LLM KPI JSON, clamps KPI milestone days, preserves fallback measurement notes when LLM output is empty, and applies content-task target defaults. |
| `nori/context_building/calendar_planner/calendar_planner.py` | `OperationPlan + KPIPlan + ClientBrief -> ContentCalendar`. |
| `nori/context_building/calendar_planner/inputs.py` | CalendarPlanner input boundary: restores `OperationPlan` / `AccountOperationProject` / composite dict inputs, normalizes KPI and brief overrides, and derives run start/horizon from explicit args, inherited calendars, and operation plans. |
| `nori/context_building/calendar_planner/prompts.py` | CalendarPlanner prompt boundary: stores the JSON-only content-calendar prompt contract and serializes normalized operation plans, KPI plans, client briefs, and run windows for LLM drafting. |
| `nori/context_building/calendar_planner/normalizer.py` | CalendarPlanner-owned normalization boundary: builds `ContentCalendar` shells, merges cadence/themes/notes, and delegates content-task row construction plus deterministic policy. |
| `nori/context_building/calendar_planner/policy.py` | CalendarPlanner pure policy boundary: clamps horizons and task days, derives target task counts and scheduled dates, formats calendar IDs/cadence/topics, and resolves required asset fallbacks without constructing `ContentCalendar`. |
| `nori/context_building/calendar_planner/task_builder.py` | CalendarPlanner content-task boundary: builds fallback `ContentTask` rows, normalizes LLM task rows, preserves invalid-row fallback, and applies task-level policy defaults. |
| `nori/context_building/planner_critics.py` | Shared planner critic policy boundary: evaluates Operation/KPI/Calendar fallback quality, structural completeness, task readiness, KPI alignment, and rule-fallback warnings without owning agent orchestration. |
| `nori/content_generation/content_producer/content_producer.py` | `ContentTask + NoteSkill + assets -> ContentPackage`; delegates note and cover generation. |
| `nori/content_generation/content_producer/inputs.py` | ContentProducer input boundary: restores `UserAsset` rows, adds task/brief text fallback, builds note/cover intent and context, and selects the generated draft's skill. |
| `nori/content_generation/content_producer/builder.py` | ContentProducer-owned package construction boundary: maps `NoteDraft` / `CoverResult` outputs into `ContentPackage` fields while delegating input preparation and provenance rows. |
| `nori/content_generation/content_producer/refs.py` | ContentPackage provenance boundary: builds material-usage rows, source refs, stable package IDs, slugs, and deduped media/reference paths without reading draft orchestration state. |
| `nori/content_generation/content_producer/state.py` | ContentProducer state boundary: formats production errors, classifies note/cover/production failures, and updates task/project success or failure metadata. |
| `nori/learning_loop/review/review_gate.py` | `ContentPackage + optional task/brief/project -> ComplianceReview[]`; rule-based review gate that delegates input restoration, policy, scoring, and project attachment. |
| `nori/learning_loop/review/inputs.py` | Review input boundary: restores package/task/brief dict snapshots and derives missing client brief context from the project. |
| `nori/learning_loop/review/policy.py` | Review policy boundary: computes compliance and consistency issues from packages, tasks, and client briefs while delegating issue scoring and suggestions. |
| `nori/learning_loop/review/scoring.py` | Review scoring boundary: creates normalized issue rows, applies severity penalties, maps score/status, counts severities, and dedupes fix suggestions without reading package models. |
| `nori/learning_loop/review/state.py` | Review state boundary: attaches generated `ComplianceReview` rows to an optional project without owning reviewer policy. |
| `nori/learning_loop/strategy/strategy_iteration.py` | Manual `MetricsSnapshot` recording and rule-based `StrategyIteration` creation from reviews + metrics; delegates input restoration, policy, and project attachment. |
| `nori/learning_loop/strategy/inputs.py` | Strategy iteration input boundary: restores review/metrics dict snapshots and derives default evidence lists from the project. |
| `nori/learning_loop/strategy/policy.py` | Strategy-iteration policy boundary: normalizes metric snapshots, summarizes review/metric evidence, and derives diagnosis, decisions, and next actions without mutating projects. |
| `nori/learning_loop/strategy/state.py` | Strategy iteration state boundary: attaches metrics snapshots and strategy iterations to an optional project without owning policy. |

Removed roots: `nori/gen_agents`, `nori/ops_agents`, `nori/ana_agents`, `nori/ops_models`, `nori/agent_models`, and `nori/agent_utils`. Canonical model ownership is split across the five business modules above, shared runtime helpers live in `nori/shared`, and tests enforce that those legacy roots are not importable.

Planning stages support deterministic fallback and LLM paths. Production/review stages are dependency-injected or rule-based so default tests avoid live calls.

## Data Collection Layer

| Subpath | Responsibility |
| --- | --- |
| `data_collect/adapter.py` | Public facade: `DataCollector`, rules, result models. |
| `data_collect/crawler/` | Multi-platform crawler core. |
| `data_collect/sign/` | XHS/Douyin signing service, default port `8989`. |
| `data_collect/downloader/` | Media downloader service, default port `8990`. |

High-level XHS skill collection:

```text
TopNotesRule
-> DataCollector.collect_top_notes
-> popular search pages
-> selected notes JSON / optional media
-> XHSNoteAnalyzer.collect_for_session
-> SessionSkillReport / NoteSkill list
```

`XHSNoteAnalyzer.collect_for_session` uses `nori.market_analysis.xhs_note_analyzer.session_llm` for required keyword generation and note-labeling JSON stages. These stages route through `call_stage_json` and fail fast with `XHSNoteAnalyzerLLMError` / existing session validation errors instead of emitting partial learned skills.

Market-analysis helpers:

| Module | Role |
| --- | --- |
| `nori/market_analysis/xhs_note_analyzer/loader.py` | XHS local metadata loader boundary: reads note/author `meta.json`, restores `XHSNoteSample`, parses `万`/comma metric counts, extracts tags, and leaves analyzer orchestration out of file IO details. |
| `nori/market_analysis/xhs_note_analyzer/rules.py` | XHS single-note rule boundary: derives single-note seed drafts, scenes, goals, title/opening/body/interaction/visual rules, CTA evidence, and draft confidence without owning LLM enhancement or session collection. |
| `nori/market_analysis/xhs_note_analyzer/note_llm.py` | XHS single-note optional LLM enhancement boundary: owns prompt text, optional JSON routing, LLM output normalization, and fallback `llm_error` attachment for seed drafts. |
| `nori/market_analysis/xhs_note_analyzer/session_clustering.py` | XHS session clustering boundary: classifies rule goals, applies required LLM labels, validates missing labels, keeps the top four goal buckets, and records leftover note ids. |
| `nori/market_analysis/xhs_note_analyzer/session_llm.py` | XHS session LLM boundary: generates search keywords and normalizes per-note goal/tone labels through the shared JSON helper with fail-fast domain errors. |
| `nori/market_analysis/xhs_note_analyzer/session_reporter.py` | XHS session reporter boundary: derives stable report stamps and writes full session reports plus skills-only guide JSON artifacts. |
| `nori/market_analysis/xhs_note_analyzer/skill_builder.py` | XHS session skill builder boundary: converts clustered hot notes into `NoteSkill` rows with merged rules, evidence notes, cover rules, metric percentiles, note-type majority, and cluster signals. |

## Test Architecture

| Test group | Coverage |
| --- | --- |
| `tests/test_llms_call_json.py` | JSON parser and request-param helper import identity, parsing helper behavior, raw capture, JSON-mode retry, and usage/kwargs propagation. |
| `tests/test_llms_client.py` | Client factory validation for OpenAI-compatible `api_key` / `base_url` before SDK construction. |
| `tests/test_llms_errors.py` | Public gateway exception identity across `nori.core.contracts`, package exports, call, and client modules. |
| `tests/test_llms_mode.py` | `ensure_ready` config validation reuse and offline `ghc` proxy probe behavior. |
| `tests/test_llms_structured_models.py` | Structured helper result dataclass defaults and identity across core contracts, package exports, intent, target, and call modules. |
| `tests/test_llms_intent_target_helpers.py` | Intent extraction, edit-target selector, and shared structured-output helper contracts without live LLM. |
| `tests/test_llms_image_capabilities.py` | Image gateway capability checks, image result normalization, reference-image requests, image input normalization helper aliases, and provider-specific image helper behavior. |
| `tests/test_llms_telemetry.py` | Redacted model-call telemetry module exports, capability/result helper identity, sink isolation, success/error behavior, plus chat/vision capability checks. |
| `tests/test_shared_utils.py` | Shared utility exports, case logging, strict JSON wrapper behavior, required/optional pre-built messages JSON routing, optional fallback JSON wrapper behavior, and fallback error field shape. |
| `tests/test_config_models.py` | Runtime-config dataclass defaults and identity between `nori.core.contracts`, core package exports, and `nori.nori_config` imports. |
| `tests/test_nori_config.py` | Config parsing, `api_key_env`, `${ENV_VAR}`, `NORI_MODE`, flat/nested active models, missing env path errors. |
| `tests/test_config_normalization.py` | Pure runtime-config normalization coverage for canonical model/provider keys, section-shape validation, mode/env cleanup, API key resolution, and active model selection. |
| `tests/test_user_profiling_* / test_content_generation_*` | Legacy compatibility coverage for Intake, IntakeTaxonomy, ImageTagger, SkillPicker, AssetCurator, NoteComposer, NoteMaker, CoverRefs, CoverPrompt, CoverOutput, CoverDirector, AccountPlanSearch, AccountPlanKeywords, AccountPlanNormalizer, AccountPlanner module aliases. |
| `tests/test_market_analysis_xhs_note_loader.py` | Canonical XHS metadata loader coverage for author/note restoration, count/tag parsing, and non-object JSON rejection. |
| `tests/test_market_analysis_xhs_note_rules.py` | Canonical XHS single-note rule coverage for seed draft structure, design-case detection, content-line cleanup, and title rule extraction. |
| `tests/test_market_analysis_xhs_note_llm.py` | Canonical single-note LLM enhancement coverage for optional JSON routing, output normalization caps/fallbacks, and fallback `llm_error` metadata. |
| `tests/test_market_analysis_xhs_session_clustering.py` | Canonical session clustering coverage for rule-goal classification, LLM-label grouping, top-four bucket selection, leftovers, and missing-label failures. |
| `tests/test_market_analysis_xhs_session_llm.py` | Canonical session LLM coverage for keyword JSON routing, context cleanup, hot-note prompt truncation, label normalization, and stage-specific errors. |
| `tests/test_market_analysis_xhs_session_reporter.py` | Canonical session reporter coverage for timestamp derivation, skills-only fixture shape, report JSON writing, and no-source-dir behavior. |
| `tests/test_market_analysis_xhs_skill_builder.py` | Canonical session skill-builder coverage for `NoteSkill` aggregation, evidence notes, cover rules, metric percentiles, and note-type majority behavior. |
| `tests/test_market_analysis_xhs_note_analyzer.py` | Legacy compatibility coverage for XHS note analysis module alias and analyzer fallback/session routing. |
| `tests/test_workflow_models.py` | Dataclass defaults and round-trip serialization. |
| `tests/test_context_building_account_positioning.py` | Account positioning extraction, legacy dict compatibility, and planner integration. |
| `tests/test_context_building_asset_research.py` | Asset library and competitor research evidence contracts. |
| `tests/test_context_building_* / test_content_generation_* / test_learning_loop_*` | Operation/KPI/calendar planner fallback, shared planner critic policy, and mocked LLM paths. |
| `tests/test_content_generation_content_producer.py` | ContentTask production bridge success, cover skip, and failure metadata. |
| `tests/test_learning_loop_review.py` | Compliance/consistency review gate and project attachment behavior. |
| `tests/test_learning_loop_strategy.py` | Metrics snapshot recording and strategy iteration from review/metric evidence. |
| `tests/test_data_collect_top_notes.py` | Top-notes collection contract. |
| `tests/test_note_skill_fixture.py` | Learned skill fixture loading and NoteMaker handoff. |

## Runtime Compatibility

| Concern | Decision |
| --- | --- |
| Python dataclass slots | Shared model/result files import `dataclass` / `field` from `nori._compat`. Python 3.10+ keeps `slots=True`; Python 3.9 drops the unsupported keyword so imports and tests remain executable. |
| Model input coercion | The five business-module `models.py` files use `nori.core.contracts` for mapping/list/string/int/bool normalization instead of carrying local copies. |
| Dependency direction | `llms.intent_extractor` and `llms.target_selector` may use `nori._compat` because `llms` already depends on `nori.nori_config` for model resolution. |

## Non-Goals In Current Architecture

| Non-goal | Constraint |
| --- | --- |
| Web server runtime | `main.py` tries `nori.nori.server`, but that module is not present in this scan. Treat server startup as stale until implemented. |
| Persistent DB | Current ops contracts are dataclasses and local JSON/file artifacts first. |
| Live platform publishing | Keep as reserved adapter until review/package loop is implemented. |
