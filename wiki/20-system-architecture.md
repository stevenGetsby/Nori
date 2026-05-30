<!-- Last verified: 2026-05-26 | Current stage: P1 Account-Ops Backend -->

# System Architecture

## Repository Shape

| Path | Role |
| --- | --- |
| `nori/` | Product workflow modules, shared contracts, runtime helpers, and config loader. |
| `nori/capabilities.py` | Public aggregate entrypoint for the current capability architecture: `build_capability_snapshot()` and `validate_capability_snapshot()`. |
| `nori/domain.py` | Legacy compatibility entrypoint that adapts capability snapshots to `DomainSnapshot` for older callers. |
| `nori/core/` | Shared capability contracts, runtime base classes, public LLM/config contracts, architecture registry, and package-root lazy-export helper for public module APIs. |
| `nori/agents/` | Business capability boundary for public agent groups: user profiling, planning, market analysis, content generation, and learning loop. |
| `nori/context/` | Runtime context assembly for one agent call. |
| `nori/memory/` | Stable/session/task memory contracts, retrieval, store, and promotion policy. |
| `nori/sessions/` | Session, turn, task-goal, and session-manager contracts. |
| `nori/workflows/` | Workflow run/stage contracts, runner, and `RuntimeRunRecorder` for session/context/workflow snapshots. |
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
  -> nori.core.IntentContract
  -> nori.content_generation.GenerationAgent
  -> nori.content_generation.ContentProducerAgent
  -> nori.content_generation.NoteMakerAgent
  -> nori.content_generation.CoverDirectorAgent
  -> nori.content_generation.models.ContentPackage
  -> nori.learning_loop.ReviewGateAgent
  -> nori.learning_loop.QualityReviewerAgent
  -> nori.learning_loop.{MetricsSnapshotAgent,StrategyIterationAgent}
  -> nori.learning_loop.models.ComplianceReview / MetricsSnapshot / StrategyIteration
```

## Capability Architecture

Nori's high-level product architecture is organized as one shared runtime layer plus five agent-owned capability groups. The canonical public surface is now `nori.capabilities` and `nori.agents.*`; the old agent/model roots have been removed and `nori.domain` is compatibility only.

```text
nori.core
  -> nori.sessions / nori.context / nori.memory / nori.workflows
  -> nori.agents.user_profiling
  -> nori.agents.market_analysis
  -> nori.agents.planning
  -> nori.agents.content_generation
  -> nori.agents.learning_loop
```

| Capability | Public contract | Current public agent surface | Backing implementation |
| --- | --- | --- | --- |
| Shared core/runtime | `UserProfile`, `UserAsset`, `ClientBrief`, `AccountOperationProject`, `ContextPack`, `CandidateSet`, `CapabilitySnapshot`, `Session`, `ContextBundle`, `WorkflowRun` | `nori.core`, `nori.sessions`, `nori.context`, `nori.memory`, `nori.workflows` | Provider-free dataclasses with `to_dict/from_dict`; `CapabilitySnapshot` is the current aggregate quality gate; `DomainSnapshot` remains legacy compatibility; `RuntimeRunRecorder` writes session/context/workflow snapshots for long live runs. |
| User profiling | Long-lived user/account/brand/preference profile | `nori.agents.user_profiling` | Backed by `nori.user_profiling` models and intaker/account planner stage packages. |
| Market analysis | Competitor samples, hot examples, trend/audience insights | `nori.agents.market_analysis` | Backed by `nori.market_analysis` models and `XHSNoteAnalyzer`; evidence can come from `DataCollector`. |
| Planning | Operation project assembly, KPI/calendar planning, and content task construction | `nori.agents.planning` | Backed by existing `nori.context_building` planner packages while system-level runtime context lives in `nori.context`. |
| Content generation | Routed text/image/package generation and candidate set before final human selection | `nori.agents.content_generation` | `NoteMakerAgent`, `CoverDirectorAgent`, and `ContentProducerAgent` remain specialized because text, image, and future video generation have different inputs and provider contracts. |
| Learning loop | Review gates, product-quality checks, monitoring snapshots, and preference/strategy update signals | `nori.agents.learning_loop` | Backed by `nori.learning_loop` review/strategy packages; `LearningLoopFacade.capability_snapshot_from_project()` builds the current aggregate view. |

Design rule: new cross-stage behavior should add a shared runtime contract or one of the five capability groups before adding another standalone agent.

Upper-layer rule: CLI/API/UI code should prefer `nori.capabilities.build_capability_snapshot()` and `nori.capabilities.validate_capability_snapshot()` when it needs the complete capability view. Use `nori.domain.*` only for legacy callers that still expect `DomainSnapshot`.

Projection bridge: the five domain facades can project an existing `AccountOperationProject` into the current architecture. `AccountOperationProject` lives in `nori.core.project`; `UserProfilingFacade` and `MarketAnalysisFacade` consume project-like dict/object shapes without importing context-building internals, keeping upstream modules independent from the context-building implementation.

| Projection | Purpose |
| --- | --- |
| `UserProfilingFacade.build_from_project(project)` | Converts client brief and account positioning into `UserProfile`. |
| `MarketAnalysisFacade.build_from_project(project)` | Converts competitor research into `MarketAnalysis`. |
| `ContextPackBuilder.build_from_project(project, task_id=...)` | Builds a task-level `ContextPack` from project profile, market, task, and assets. |
| `ContentGenerationFacade.candidate_set_from_project(project, task_id=...)` | Converts task packages into a `CandidateSet` linked to context trace input refs. |
| `LearningLoopFacade.performance_snapshots_from_project(project)` | Converts project metrics into `PerformanceSnapshot[]`. |
| `LearningLoopFacade.learning_signals_from_project(project, ...)` | Converts strategy iterations into `LearningSignal[]`. |
| `LearningLoopFacade.capability_snapshot_from_project(project, ...)` | Aggregates the full capability view into a round-trippable `CapabilitySnapshot`. |

`CapabilitySnapshot.validate()` currently guards required capability coverage, candidate-set/context alignment, and selected-candidate integrity. This is the shared quality gate for future CLI/API/UI consumers of the new architecture.

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
| `GenerationAgent` | `artifact_type` plus route-specific inputs | `ContentPackage` / `NoteDraft` / `CoverResult` | Coarse generation stage and router. It owns route selection and shared intent handoff, while preserving specialized child agents for text and image. |
| `IntakeAgent` | `UserInput(text, images)` | `IntakeResult(intention, context, missing, questions, assets)` | Only layer that performs image understanding / vision tagging. |
| `NoteMakerAgent` | `NoteSkill[]`, `UserAsset[]`, intent/context | `NoteDraft` | Only writes note copy/title/tags; does not read original image bytes. |
| `CoverDirectorAgent` | `NoteDraft`, selected skill, tagged assets | `CoverResult` | Only layer that calls image generation and reads reference image bytes. |
| `AccountPlannerAgent` | `AccountPlannerInput` or raw input/assets/links | `AccountPlanResult` | Produces account positioning and IP portrait; search provider is pluggable. |

`IntakeResult` and `AccountPlanResult` include optional `metadata` for non-contract control-plane facts such as LLM fallback errors. Empty metadata is omitted from `to_dict()` output to preserve compact fixtures.

Workflow stage package layout:

| Stage package | Implementation files |
| --- | --- |
| `nori/user_profiling/intaker/` | `intaker.py`, `package.py`, `normalizer.py`, `taxonomy.py`, `image_tagger.py` |
| `nori/user_profiling/account_planner/` | `account_planner.py`, `package.py`, `fallback.py`, `search.py`, `normalizer.py`, `portrait.py`, `keywords.py` |
| `nori/content_generation/note_maker/` | `note_maker.py`, `package.py` |
| `nori/content_generation/cover_director/` | `cover_director.py`, `package.py`, `output.py` |
| `nori/content_generation/content_producer/` | `content_producer.py`, `package.py`, `state.py` |
| `nori/context_building/operation_planner/` | `operation_planner.py`, `package.py`, `project_builder.py`, `project_policy.py`, `normalizer.py` |
| `nori/context_building/kpi_planner/` | `kpi_planner.py`, `package.py`, `normalizer.py` |
| `nori/context_building/calendar_planner/` | `calendar_planner.py`, `package.py`, `normalizer.py`, `policy.py`, `task_builder.py` |
| `nori/learning_loop/review/` | `review_gate.py`, `package.py`, `policy.py`, `scoring.py`, `state.py` |
| `nori/learning_loop/strategy/` | `strategy_iteration.py`, `package.py`, `policy.py`, `state.py` |
| `nori/market_analysis/xhs_note_analyzer/` | `xhs_note_analyzer.py`, `package.py`, `loader.py`, `rules.py`, `note_llm.py`, `session_clustering.py`, `session_llm.py`, `session_reporter.py`, `skill_builder.py` |

Flat helper module paths such as `nori.content_generation.skill_picker` and `nori.context_building.operation_planner_inputs` should not exist. Stage-local `schema.py` re-export files should not exist either; model contracts live in the owning business module `models.py` files or in `nori.core` for shared contracts. Stage-local `inputs.py`, `prompts.py`, and `refs.py` files have been consolidated into class-owned `package.py` contracts when they only supported a single agent. New implementation code and imports should live inside the owning stage package.

Shared generation utilities:

| Module | Role |
| --- | --- |
| `nori/core/contracts.py` | Public contract owner for runtime config models, LLM gateway errors, structured LLM helper result models, and model `from_dict()` coercion helpers. |
| `nori/core/llm.py` | `LLMFactory` is the injectable project LLM gateway used by agents instead of reaching directly into `llms` in constructors or orchestration code. |
| `nori/core/agent.py` | `AgentBase` standardizes `stage_name`, `use_llm`, `llm_factory`, and required/optional JSON helper methods while preserving each agent's domain-specific `run(...)` signature. `AgentInputPreparer` and `AgentPromptBuilder` give stage packages a shared class pattern for input and prompt contracts. |
| `nori/core/workflow.py` | `WorkflowBase` provides a small ordered-step runner for agents and domain facades that compose multiple substages; `named_workflow_steps(...)` lets facades declare readable no-op stage names when their public methods own execution. All five business facades expose this shared workflow contract through `workflow_name` and `step_names`. |
| `nori/core/artifacts.py` | `StableArtifactAssembler` provides shared slug/dedupe behavior for deterministic assemblers that produce stable local artifact IDs or media/reference lists. |
| `nori/core/artifacts.py` | `ArtifactStore` writes stage JSON checkpoints plus `manifest.json`, and exposes `get_or_build(...)` for resumable long-running flows. |
| `nori/core/models.py` | `IntentContract` freezes user intent before generation and exposes `missing_terms(...)` so generation/review stages can verify concrete acceptance requirements. |
| `nori/shared/llm_json.py` | `call_stage_json` wraps `llms.chat_json(json_mode=True)` for required generation stages and translates parse/provider errors into the caller's domain exception. |
| `nori/shared/llm_json.py` | `call_stage_messages_json` applies the same required-stage contract to pre-built messages, including multimodal vision messages. |
| `nori/shared/llm_json.py` | `try_stage_json` is the system/user convenience wrapper for optional JSON LLM stages, delegating to the same pre-built-message fallback path. |
| `nori/shared/llm_json.py` | `try_stage_messages_json` wraps optional pre-built-message JSON stages, returning `(data, error)` so planners can keep deterministic fallback; parse errors reuse `llms.structured_outputs.chat_json_error_reason`. |
| `nori/shared/llm_json.py` | `attach_llm_error` is the canonical formatter for redacted fallback errors: `{metadata|validation}.llm_error = {reason, error_type, stage, ...}` with caller stage kept authoritative. |
| `nori/user_profiling/intaker/normalizer.py` | Intake-owned text normalization boundary: owns deterministic text fallback, optional LLM output cleanup, image context construction, and metadata preservation while delegating taxonomy mechanics. |
| `nori/user_profiling/intaker/taxonomy.py` | Intake-owned taxonomy boundary: stores goal/format/tone/asset/guardrail/data vocabularies, alias maps, rule-based text classification, allowed-label cleanup, missing-field repair, and question fallback text. |
| `nori/user_profiling/intaker/image_tagger.py` | Intake-owned vision tagging boundary: builds multimodal per-image JSON messages, isolates per-image failures, filters tag vocabularies, and returns `UserAsset` records. `intaker.py` keeps compatibility facades for existing call sites. |
| `nori/market_analysis/note_skill_fixture.py` | Market-analysis-owned learned-skill fixture bridge: converts `SessionSkillReport` / `NoteSkill` objects to the skills-only JSON shape consumed by NoteMaker tests and smoke scripts. |
| `nori/content_generation/note_maker/package.py` | NoteMaker-owned package contract: `NoteSkillSelector`, `NoteAssetCurator`, and `NoteComposer` own prompt construction, asset curation, note field normalization, and domain error translation; `note_maker.py` stays focused on stage orchestration. |
| `nori/content_generation/cover_director/package.py` | CoverDirector-owned package contract: `CoverReferenceSelector` and `CoverPromptBuilder` own tagged/legacy reference selection, reference input conversion, prompt construction, and empty-prompt domain errors. |
| `nori/content_generation/cover_director/output.py` | CoverDirector-owned image output boundary: persists data-uri or remote image payloads, sanitizes cover filenames, and translates base64/download failures into the caller's domain error. |
| `nori/user_profiling/account_planner/package.py` | AccountPlanner-owned package contract: restores/merges `AccountPlannerInput`, extra images/links, platform defaults, per-image prompt context, and JSON-only account-planning prompt construction. |
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
| `nori/context_building/operation_planner/package.py` | OperationPlanner package contract: restores `ClientBrief`/`AccountPlanResult` inputs, normalizes planner start dates and horizons, and owns JSON-only SOP prompt construction. |
| `nori/context_building/operation_planner/project_builder.py` | OperationPlanner deterministic fallback assembly boundary: builds rule-based operation projects, tasks, calendars, and derived KPI snapshots while delegating pure fallback policy. |
| `nori/context_building/operation_planner/project_policy.py` | OperationPlanner pure policy boundary: derives account positioning, content pillars, objectives, risk controls, topic pools, references, milestones, project IDs/titles, and operation-derived KPI plans without constructing a project shell. |
| `nori/context_building/operation_planner/normalizer.py` | OperationPlanner-owned LLM output normalization boundary: merges operation plan/calendar JSON into a fallback project shell, normalizes LLM task rows, clamps milestone/task dates, and derives KPIPlan snapshots. |
| `nori/context_building/kpi_planner/kpi_planner.py` | `OperationPlan -> KPIPlan`. |
| `nori/context_building/kpi_planner/package.py` | KPIPlanner package contract: restores `OperationPlan` / `AccountOperationProject` / composite dict inputs, derives project context, and owns JSON-only KPI prompt construction. |
| `nori/context_building/kpi_planner/normalizer.py` | KPIPlanner-owned normalization boundary: builds deterministic KPI fallback, merges LLM KPI JSON, clamps KPI milestone days, preserves fallback measurement notes when LLM output is empty, and applies content-task target defaults. |
| `nori/context_building/calendar_planner/calendar_planner.py` | `OperationPlan + KPIPlan + ClientBrief -> ContentCalendar`. |
| `nori/context_building/calendar_planner/package.py` | CalendarPlanner package contract: restores `OperationPlan` / `AccountOperationProject` / composite dict inputs, normalizes KPI/brief overrides, derives run windows, and owns JSON-only calendar prompt construction. |
| `nori/context_building/calendar_planner/normalizer.py` | CalendarPlanner-owned normalization boundary: builds `ContentCalendar` shells, merges cadence/themes/notes, and delegates content-task row construction plus deterministic policy. |
| `nori/context_building/calendar_planner/policy.py` | CalendarPlanner pure policy boundary: clamps horizons and task days, derives target task counts and scheduled dates, formats calendar IDs/cadence/topics, and resolves required asset fallbacks without constructing `ContentCalendar`. |
| `nori/context_building/calendar_planner/task_builder.py` | CalendarPlanner content-task boundary: builds fallback `ContentTask` rows, normalizes LLM task rows, preserves invalid-row fallback, and applies task-level policy defaults. |
| `nori/context_building/planner_critics.py` | Shared planner critic policy boundary: evaluates Operation/KPI/Calendar fallback quality, structural completeness, task readiness, KPI alignment, and rule-fallback warnings without owning agent orchestration. |
| `nori/content_generation/content_producer/content_producer.py` | `ContentTask + NoteSkill + assets -> ContentPackage`; delegates note and cover generation. |
| `nori/content_generation/content_producer/package.py` | `ContentPackageAssembler` class: restores assets, builds production intent/context, selects the generated draft's skill, builds stable package IDs, material usage, source refs, and maps `NoteDraft` / `CoverResult` into `ContentPackage`. |
| `nori/content_generation/content_producer/state.py` | ContentProducer state boundary: formats production errors, classifies note/cover/production failures, and updates task/project success or failure metadata. |
| `nori/learning_loop/review/review_gate.py` | `ContentPackage + optional task/brief/project -> ComplianceReview[]`; rule-based review gate that delegates input restoration, policy, scoring, and project attachment. |
| `nori/learning_loop/review/package.py` | Review package contract: restores package/task/brief dict snapshots and derives missing client brief context from the project. |
| `nori/learning_loop/review/policy.py` | Review policy boundary: computes compliance and consistency issues from packages, tasks, and client briefs while delegating issue scoring and suggestions. |
| `nori/learning_loop/review/scoring.py` | Review scoring boundary: creates normalized issue rows, applies severity penalties, maps score/status, counts severities, and dedupes fix suggestions without reading package models. |
| `nori/learning_loop/review/state.py` | Review state boundary: attaches generated `ComplianceReview` rows to an optional project without owning reviewer policy. |
| `nori/learning_loop/strategy/strategy_iteration.py` | Manual `MetricsSnapshot` recording and rule-based `StrategyIteration` creation from reviews + metrics; delegates input restoration, policy, and project attachment. |
| `nori/learning_loop/strategy/package.py` | Strategy iteration package contract: restores review/metrics dict snapshots and derives default evidence lists from the project. |
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
