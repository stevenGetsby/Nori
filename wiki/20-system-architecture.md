<!-- Last verified: 2026-06-01 | Current stage: P1 Account-Ops Backend -->

# System Architecture

## Repository Shape

| Path | Role |
| --- | --- |
| `backend/` | FastAPI product-service boundary for web/CLI/local-server adapters. It owns request/response shapes, session routes, session image uploads, workflow catalog/resolve routes, content-generation option/action catalogs, backend experiment run APIs, and experiment readiness/run-summary observability without owning agent logic. |
| `nori/` | Product workflow modules, shared contracts, runtime helpers, and config loader. |
| `nori/core/` | Shared capability contracts, runtime base classes, public LLM/config contracts, architecture registry, and package-root lazy-export helper for public module APIs. |
| `nori/agents/` | Agent boundary for the user-facing supervisor plus public business capability groups: user profiling, planning, market analysis, content generation, and learning loop. |
| `nori/context/` | Context orchestration layer: compiles business `ContextPack` / `ContextView`, resolves runtime `ContextBundle`, and bridges business context into one agent call. |
| `nori/memory/` | Stable/session/task memory contracts, retrieval, LangGraph store subclass, and promotion policy. |
| `nori/sessions/` | Session, turn, task-goal, and session-manager contracts. |
| `nori/workflows/` | Workflow run/stage contracts, LangGraph-backed runner, and `RuntimeRunRecorder` for session/context/workflow snapshots. |
| `nori/agents/user_profiling/` | `facade.py` for long-lived user/account/brand/preference profile construction; package `__init__` keeps lightweight model exports eager and routes stage/facade exports through `nori.core.lazy_exports`. |
| `nori/agents/market_analysis/` | `facade.py` for competitor/hot-example/trend evidence as market analysis; package `__init__` keeps lightweight model exports eager and routes analyzer/facade exports through `nori.core.lazy_exports`. |
| `nori/agents/planning/` | Operation/KPI/calendar planning, planner critics, and content task construction. Context compilation lives only in `nori.context`. |
| `nori/agents/content_generation/` | Canonical content-generation module: content production bridge, package input/builder/provenance/state helpers, candidate sets, and lazy public stage exports. |
| `nori/agents/learning_loop/` | Canonical learning-loop module: review gates, review policy/scoring/state, metrics snapshots, strategy iteration, capability snapshots, and lazy public stage exports. |
| `nori/agents/supervisor/` | User-facing main-chat supervisor. It routes a chat turn into injected subagent/subworkflow tools and does not import workflow runtime modules directly. |
| `nori/core/llms/` | Core infra gateway for language, vision, and image-model calls. This is the only LLM gateway import root; the old top-level `llms/` compatibility package has been removed. |
| `nori/_compat.py` | Small runtime compatibility layer for dataclass features used by shared models and LLM result objects. |
| `nori/config_normalization.py` | Pure runtime-config normalization helpers for provider/model keys, env names, mode names, core section shapes, and active model maps. |
| `data_collect/` | Unified crawler/sign/downloader integration layer. |
| `tests/` | Unit and mocked integration tests. Live tests should be opt-in. |
| `scripts/` | Thin adapters for live/session-level workflows. Product workflow definitions belong in `nori/workflows/*`, not in scripts. |
| `web/` | Product frontend boundary and frontend prototypes. Backend-integrated production workbench is not implemented yet. |
| `wiki/archive/legacy-docs/` | Historical design notes and project-specific skill source. Wiki root remains the canonical project map. |
| `wiki/visuals/` | Static architecture visualization and documentation artifacts only; product UI belongs in `web/`. |

## Frameworks

Nori uses LangGraph and LangChain Core at the runtime orchestration boundary:

| Framework | Where | Role |
| --- | --- | --- |
| LangGraph | `nori.workflows.WorkflowRunner` | Compiles `WorkflowSpec` into a `StateGraph`, executes coarse workflow nodes through `START -> ... -> END`, and records `WorkflowRun` / `StageRun` status. |
| LangChain Core | `nori.workflows.WorkflowRunner` | Wraps each stage handler as a `RunnableLambda`, keeping workflow stages compatible with LangChain runnable semantics. |
| LangGraph checkpoint memory | `nori.workflows.WorkflowRunner` | Does not enable LangGraph checkpointing by default because workflow state carries runtime-only objects such as `LLMFactory`; callers can inject a checkpointer only for serializable state. |
| LangGraph memory store | `nori.memory.InMemoryMemoryStore` | Subclasses `langgraph.store.memory.InMemoryStore` and adds Nori typed profile/session/task helpers instead of keeping a bespoke dict store. |
| Nori Human Gate | `nori.workflows.HumanGateSpec` | Declares human review control points before selected stages. Default `human_gate_mode="skip"` keeps tests automated; `pause` records `waiting_for_human` for product surfaces. |

`nori/workflows/content_production` is the first product-level workflow package. It depends on public agent boundaries and owns the ordered content-production stages; `scripts/run_holly_live_case.py` only adapts Holly-specific inputs, model config, and XHS collection into that workflow.

Business agents still own Nori-specific behavior under `nori.agents.*`; LangGraph owns cross-stage execution, not domain logic.

`NoriSupervisorAgent` is the main-chat orchestration agent above the business
capability layer. It can plan or execute injected `SupervisorTool` handlers such
as `content_production`, `content_design_spec`, `artifact_generation`,
`market_analysis`, `review_content_package`, and `session_memory`. The default
catalog describes these tools without handlers; backend/workflow adapters bind
real subworkflow handlers at the product boundary.

## Runtime Layers

```text
Input / assets
  -> backend upload/run routes / scripts
  -> nori.agents.supervisor.NoriSupervisorAgent
  -> nori.sessions.SessionManager
  -> nori.agents.user_profiling.IntakeAgent
  -> nori.agents.user_profiling.AccountPlannerAgent
  -> nori.agents.planning.{OperationPlanner,KPIPlanner,CalendarPlanner}
  -> nori.context.{ContextCompiler,ContextResolver}
  -> nori.core.IntentContract
  -> nori.agents.content_generation.ContentSpecAgent
  -> nori.agents.content_generation.ArtifactGenerationAgent
  -> nori.agents.content_generation.ContentProducerAgent
  -> nori.agents.content_generation.NoteMakerAgent
  -> nori.agents.content_generation.CoverDirectorAgent
  -> nori.agents.content_generation.schemas.generation.ContentPackage
  -> nori.agents.learning_loop.ReviewGateAgent
  -> nori.agents.learning_loop.QualityReviewerAgent
  -> nori.agents.learning_loop.{MetricsSnapshotAgent,StrategyIterationAgent}
  -> nori.agents.learning_loop.schemas.learning.ComplianceReview / MetricsSnapshot / StrategyIteration
```

## Capability Architecture

Nori's high-level product architecture is organized as one shared runtime layer, one user-facing supervisor, and five agent-owned business capability groups. The canonical public surface is now the owning modules: `nori.core` for capability registry metadata, `nori.agents.supervisor` for main-chat tool routing, `nori.agents.learning_loop` for aggregate capability snapshots, and `nori.agents.*` for business behavior. The old top-level business roots, `nori.domain`, and `nori.capabilities` compatibility layers have been removed.

```text
nori.core
  -> nori.sessions / nori.context / nori.memory / nori.workflows
  -> nori.agents.supervisor
  -> nori.agents.user_profiling
  -> nori.agents.market_analysis
  -> nori.agents.planning
  -> nori.agents.content_generation
  -> nori.agents.learning_loop
```

| Capability | Public contract | Current public agent surface | Backing implementation |
| --- | --- | --- | --- |
| Shared core/runtime | `UserProfile`, `UserAsset`, `ClientBrief`, `AccountOperationProject`, `ContextPack`, `ContextSlice`, `ContextView`, `CandidateSet`, `CapabilitySnapshot`, `Session`, `ContextBundle`, `WorkflowRun`, `HumanGateSpec` | `nori.core`, `nori.sessions`, `nori.context`, `nori.memory`, `nori.workflows` | Provider-free dataclasses with `to_dict/from_dict`; `CapabilitySnapshot` is the current aggregate quality gate; `ContextCompiler` compiles platform, market, skill, strategy, asset, and constraint slices into `ContextPack`; `ContextResolver.for_agent(...)` projects a `ContextView`; `ContextBundle` remains the runtime envelope for one agent call. |
| Main-chat supervisor | `SupervisorIntent`, `SupervisorTool`, `SupervisorToolRequest`, `SupervisorToolResult`, `SupervisorTurnResult` | `nori.agents.supervisor` | `NoriSupervisorAgent` routes a user chat turn to a tool. It supports LLM structured routing, deterministic keyword fallback, plan-only mode, injected tool handlers, and clarification when no tool matches. It is intentionally not part of `CAPABILITY_MODULES`. |
| User profiling | Long-lived user/account/brand/preference profile | `nori.agents.user_profiling` | Backed by `nori.agents.user_profiling` models and intaker/account planner stage packages. |
| Market analysis | Competitor samples, hot examples, trend/audience insights | `nori.agents.market_analysis` | Backed by `nori.agents.market_analysis` models and `XHSNoteAnalyzer`; evidence can come from `DataCollector`. |
| Planning | Operation project assembly, KPI/calendar planning, and content task construction | `nori.agents.planning` | Backed by existing `nori.agents.planning` planner packages; context-pack compilation and agent-specific context views live in `nori.context`. |
| Content generation | Spec-driven package generation and candidate set before final human selection | `nori.agents.content_generation` | `ContentSpecAgent` turns task/skills/assets into an inspectable `ContentDesignSpec`; `ArtifactGenerationAgent` executes the spec through specialized generators. `NoteMakerAgent`, `CoverDirectorAgent`, and `ContentProducerAgent` remain specialized implementation details behind the executor. |
| Learning loop | Review gates, product-quality checks, monitoring snapshots, and preference/strategy update signals | `nori.agents.learning_loop` | Backed by `nori.agents.learning_loop` review/strategy packages; `LearningLoopFacade.capability_snapshot_from_project()` builds the current aggregate view. |

Design rule: new business behavior should add a shared runtime contract or one of the five capability groups before adding another standalone agent. The supervisor is the exception reserved for user-facing orchestration; it should call injected tools rather than import concrete workflow runtimes.

Upper-layer rule: CLI/API/UI code should use `nori.core.capability_registry_snapshot()` for architecture metadata and `nori.agents.learning_loop.build_capability_snapshot()` / `validate_capability_snapshot()` when it needs the complete capability view.

Projection bridge: the five domain facades can project an existing `AccountOperationProject` into the current architecture. `AccountOperationProject` lives in `nori.core.project`; `UserProfilingFacade` and `MarketAnalysisFacade` consume project-like dict/object shapes without importing planning internals, keeping upstream modules independent from the planning implementation.

| Projection | Purpose |
| --- | --- |
| `UserProfilingFacade.build_from_project(project)` | Converts client brief and account positioning into `UserProfile`. |
| `MarketAnalysisFacade.build_from_project(project)` | Converts competitor research into `MarketAnalysis`. |
| `nori.context.ContextPackBuilder.build_from_project(project, task_id=...)` | Builds a task-level `ContextPack` from project profile, platform strategy, market, task, skills, content strategy, assets, and constraints. |
| `ContentGenerationFacade.candidate_set_from_project(project, task_id=...)` | Converts task packages into a `CandidateSet` linked to context trace input refs. |
| `LearningLoopFacade.performance_snapshots_from_project(project)` | Converts project metrics into `PerformanceSnapshot[]`. |
| `LearningLoopFacade.learning_signals_from_project(project, ...)` | Converts strategy iterations into `LearningSignal[]`. |
| `LearningLoopFacade.capability_snapshot_from_project(project, ...)` | Aggregates the full capability view into a round-trippable `CapabilitySnapshot`. |

`CapabilitySnapshot.validate()` currently guards required capability coverage, candidate-set/context alignment, and selected-candidate integrity. This is the shared quality gate for future CLI/API/UI consumers of the new architecture.

## LLM Gateway

| Module | Responsibility |
| --- | --- |
| `nori/core/contracts.py` | Public runtime contract boundary shared by Nori core and the LLM gateway: provider/model config rows, resolved active models, gateway exception classes, and provider-free model coercion helpers. |
| `nori/nori_config.py` | Locate `api_config.yaml`, parse providers/models/active usages, coerce model scalar fields, resolve `api_key_env`, apply `NORI_MODE`, and assemble config model contracts. |
| `nori/config_normalization.py` | Pure config normalization boundary shared by `nori.nori_config` and `nori.core.llms.client`: canonical provider/model keys, env names, mode keys, section-shape validation, and nested/flat `active_models` selection. |
| `nori/core/llms/telemetry.py` | Process-local redacted telemetry sink and emit helper. The public setter is exposed from `nori.core.llms`; gateway call sites import the telemetry boundary directly. |
| `nori/core/llms/lm.py` | `LanguageModelClient` for sync/async LangChain chat execution, request-parameter merging, chat result normalization, LangChain structured-output JSON calls, and chat telemetry. |
| `nori/core/llms/imager.py` | `ImageClient` for active image-model resolution, reference input filtering, capability guards, image provider dispatch, result validation, and image telemetry. |
| `nori/core/llms/capabilities.py` | Shared capability guards for chat model type, vision usage, multimodal messages, image model type, and reference-image support. |
| `nori/core/llms/image_inputs.py` | Shared image input normalization for bytes, data-uri, local path, base64 strings, MIME sniffing, and data-uri construction. |
| `nori/core/llms/image_providers.py` | `ImageProviders` class for OpenAI-compatible edit, relay reference-payload retry, Google native image generation, and image response extraction. |
| `nori/core/llms/client.py` | Own the LLM runtime config singleton, switch `direct`/`ghc`, preflight local proxy `/models`, build LangChain chat adapters through `init_chat_model` for text/vision chat, build OpenAI-compatible SDK clients for image providers, and expose `NoriAIClient` as the aggregate gateway. |

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
| `ContentSpecAgent` | `ContextView` from `nori.context`, or explicit task/skills/assets inputs for focused tests | `ContentDesignSpec` | Strategy/spec stage. It selects skill refs, freezes structure, media plan, copy/visual rules, constraints, and acceptance checks. For XHS hotspot image posts it also freezes the page rhythm, hotspot strategy metadata, and human review checklist. It does not write final copy or generate media. |
| `ArtifactGenerationAgent` | `ContentDesignSpec` plus task, skills, assets, and output path | `ContentPackage` | Execution stage. It filters skills by the spec and passes the spec into intent/context before delegating to `ContentProducerAgent`. It should not re-decide strategy. |
| `IntakeAgent` | `UserInput(text, images)` | `IntakeResult(intention, context, missing, questions, assets)` | Only layer that performs image understanding / vision tagging. |
| `NoteMakerAgent` | `NoteSkill[]`, `UserAsset[]`, intent/context | `NoteDraft` | Only writes note copy/title/tags; its prompt owns hotspot evidence assumptions, account credibility, title/body constraints, and authenticity boundaries. It does not read original image bytes. |
| `CoverDirectorAgent` | `NoteDraft`, selected skill, tagged assets | `CoverResult` | Only layer that calls image generation and reads reference image bytes; its prompt owns one-glance cover clarity, visual composition, and fake-evidence bans. |
| `AccountPlannerAgent` | `AccountPlannerInput` or raw input/assets/links | `AccountPlanResult` | Produces account positioning and IP portrait; search provider is pluggable. |

`IntakeResult` and `AccountPlanResult` include optional `metadata` for non-contract control-plane facts such as LLM fallback errors. Empty metadata is omitted from `to_dict()` output to preserve compact fixtures.

Implementation ownership is stage-local: each runtime stage keeps its orchestrator,
input restoration, deterministic fallback, prompt construction, and output
normalization inside the owning capability package. Flat helper modules,
stage-local `schema.py` re-export files, and old top-level business roots should
not come back.

Detailed package maps and helper-module ownership live in
[Module Map](./refs/module-map.md). Keep this page focused on runtime layers and
architectural boundaries.

## Account-Ops Backend

The backend is organized around the core project aggregate plus stage-owned
capability packages:

```text
ClientBrief + AccountPlanResult
  -> AccountOperationProject
  -> OperationPlan / KPIPlan / ContentCalendar / ContentTask
  -> ContentPackage
  -> ComplianceReview / MetricsSnapshot / StrategyIteration
```

Cross-stage workflow contracts are now owned by focused core modules:
`nori.core.asset_models`, `nori.core.planning_models`,
`nori.core.profile_models`, and `nori.core.capability_models`.
The historical `nori.core.models` single-module facade has been removed; import
from `nori.core` or the narrower owner module. The detailed module inventory is in
[Module Map](./refs/module-map.md).

Planning stages support deterministic fallback and LLM paths. Production/review
stages are dependency-injected or rule-based so default tests avoid live calls.

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

`XHSNoteAnalyzer.collect_for_session` uses `nori.agents.market_analysis.xhs_note_analyzer.session_llm` for required keyword generation and note-labeling JSON stages. These stages route through `call_stage_json` and fail fast with `XHSNoteAnalyzerLLMError` / existing session validation errors instead of emitting partial learned skills.

Market-analysis helpers:

| Module | Role |
| --- | --- |
| `nori/agents/market_analysis/xhs_note_analyzer/loader.py` | XHS local metadata loader boundary: reads note/author `meta.json`, restores `XHSNoteSample`, parses `万`/comma metric counts, extracts tags, and leaves analyzer orchestration out of file IO details. |
| `nori/agents/market_analysis/xhs_note_analyzer/rules.py` | XHS single-note rule boundary: derives single-note seed drafts, scenes, goals, title/opening/body/interaction/visual rules, CTA evidence, and draft confidence without owning LLM enhancement or session collection. |
| `nori/agents/market_analysis/xhs_note_analyzer/note_llm.py` | XHS single-note optional LLM enhancement boundary: owns prompt text, optional JSON routing, LLM output normalization, and fallback `llm_error` attachment for seed drafts. |
| `nori/agents/market_analysis/xhs_note_analyzer/session_clustering.py` | XHS session clustering boundary: classifies rule goals, applies required LLM labels, validates missing labels, keeps the top four goal buckets, and records leftover note ids. |
| `nori/agents/market_analysis/xhs_note_analyzer/session_llm.py` | XHS session LLM boundary: generates search keywords and normalizes per-note goal/tone labels through the shared JSON helper with fail-fast domain errors. |
| `nori/agents/market_analysis/xhs_note_analyzer/session_reporter.py` | XHS session reporter boundary: derives stable report stamps and writes full session reports plus skills-only guide JSON artifacts. |
| `nori/agents/market_analysis/xhs_note_analyzer/skill_builder.py` | XHS session skill builder boundary: converts clustered hot notes into `NoteSkill` rows with merged rules, evidence notes, cover rules, metric percentiles, note-type majority, and cluster signals. |

## Test Architecture

| Test group | Coverage |
| --- | --- |
| `tests/test_llms_call_json.py` | LangChain structured-output JSON routing, schema/method passthrough, structured parse-error wrapping, non-object rejection, and legacy raw-chat injection isolation. |
| `tests/test_llms_client.py` | Client factory validation for OpenAI-compatible `api_key` / `base_url` before SDK construction. |
| `tests/test_llms_errors.py` | Public gateway exception identity across `nori.core.contracts`, package exports, call, and client modules. |
| `tests/test_llms_mode.py` | `ensure_ready` config validation reuse and offline `ghc` proxy probe behavior. |
| `tests/test_llms_structured_models.py` | Structured helper result dataclass defaults and identity across core contracts, package exports, intent, target, and call modules. |
| `tests/test_llms_intent_target_helpers.py` | Intent extraction, edit-target selector, and shared structured-output helper contracts without live LLM. |
| `tests/test_llms_image_capabilities.py` | Image gateway capability checks, image result normalization, reference-image requests, image input normalization boundaries, and provider-specific image helper behavior. |
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
| `tests/test_user_profiling_account_positioning.py` | Account positioning extraction, legacy dict compatibility, and planner integration. |
| `tests/test_market_analysis_asset_research.py` | Asset library and competitor research evidence contracts. |
| `tests/test_planning_* / test_content_generation_* / test_learning_loop_*` | Operation/KPI/calendar planner fallback, shared planner critic policy, and mocked LLM paths. |
| `tests/test_content_generation_content_producer.py` | ContentTask production bridge success, cover skip, and failure metadata. |
| `tests/test_learning_loop_review.py` | Compliance/consistency review gate and project attachment behavior. |
| `tests/test_learning_loop_strategy.py` | Metrics snapshot recording and strategy iteration from review/metric evidence. |
| `tests/test_data_collect_top_notes.py` | Top-notes collection contract. |
| `tests/test_note_skill_fixture.py` | Learned skill fixture loading and NoteMaker handoff. |

## Runtime Compatibility

| Concern | Decision |
| --- | --- |
| Python dataclass slots | Shared model/result files import `dataclass` / `field` from `nori._compat`. Python 3.10+ keeps `slots=True`; Python 3.9 drops the unsupported keyword so imports and tests remain executable. |
| Schema input coercion | Owner-local `schemas/` packages use `nori.core.contracts` for mapping/list/string/int/bool normalization instead of carrying local copies. |
| Dependency direction | `nori.core.llms` is infrastructure. Product-specific intent extraction or edit-target routing should live in the owning agent/supervisor package, not in the core LLM gateway. |

## Non-Goals In Current Architecture

| Non-goal | Constraint |
| --- | --- |
| Production web server runtime | `backend/` provides a lightweight FastAPI/uvicorn service for local/product integration with local experiment uploads and synchronous workflow runs, but no production deployment stack, auth, streaming, async job queue, or persistent DB is implemented yet. |
| Production frontend workbench | `web/` is now the boundary for product UI and prototypes, but no backend-integrated workbench app is implemented yet. |
| Persistent DB | Current ops contracts are dataclasses and local JSON/file artifacts first. |
| Live platform publishing | Keep as reserved adapter until review/package loop is implemented. |
