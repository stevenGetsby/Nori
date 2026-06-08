<!-- Last verified: 2026-06-01 | Current stage: Architecture Refactor -->

# Historical Spec: Domain Architecture Refactor

This document is retained as historical context for the earlier domain-module refactor. The current canonical architecture is capability/runtime based; see `spec-capability-architecture.md`.

## Original Goal

Refactor Nori into one shared layer plus five stable domain modules:

```text
shared
  -> user profiling
  -> market analysis
  -> context building
  -> content generation
  -> learning loop
```

The purpose is to make the shared layer and five domain modules the canonical implementation surface. Legacy agent/model roots have been removed; new code imports from the owning workflow module directly.

## Non-Goals

| Non-goal | Reason |
| --- | --- |
| Support legacy import paths | Legacy wrappers are intentionally removed to keep the architecture unambiguous. |
| Add another top-level agent bucket | New behavior should land in one of the five domain modules unless a shared core contract is needed first. |
| Add new business behavior | This refactor is about structure, contracts, and module boundaries. |
| Replace current dataclasses with a DB or ORM | Current contracts are JSON-first and local-file-first. |

## Target Module Map

| Layer | Modules | Responsibility |
| --- | --- | --- |
| `shared` | `nori/core/{profile_models,asset_models,planning_models,capability_models}.py`, `nori/core/architecture.py` | Common contract owners, canonical registry, context packs, decision traces, evidence references, learning signals. |
| `user profiling` | `nori/agents/user_profiling/facade.py` | Long-lived user/account/brand/preferences/constraints profiles. |
| `market analysis` | `nori/agents/market_analysis/facade.py` | Benchmark samples, market snapshots, trend insights, audience insights. |
| `context building` | `nori/context`, operation/KPI/calendar planner modules, planner critics | Build operation project context, KPI plans, content calendars, `ContentTask` rows, and `ContextPack` from profile + task + market + assets + history. |
| `content generation` | `nori/agents/content_generation/facade.py`, `content_producer/*`, `note_maker/*`, `cover_director/*` | Produce content packages, manage production state/provenance, group candidates, and expose final deliverables. |
| `learning loop` | `nori/agents/learning_loop/facade.py`, `review/*`, `strategy/*` | Review gates, monitoring snapshots, analytics, feedback signals, preference updates, strategy iteration. |

## Public Entrypoint

At the time of this historical refactor, `nori.domain` was proposed as the stable import path for upper layers that needed the complete projected architecture. Current pre-launch code removed that compatibility layer and the later `nori.capabilities` facade; use the owning modules directly:

| API | Purpose |
| --- | --- |
| `nori.core.capability_registry_snapshot()` | Returns the five agent-owned capability groups. |
| `nori.agents.learning_loop.build_capability_snapshot(project, ...)` | Builds a full `CapabilitySnapshot` from an `AccountOperationProject` or persisted project dict. |
| `nori.agents.learning_loop.validate_capability_snapshot(snapshot)` | Validates a `CapabilitySnapshot` object or persisted snapshot dict and returns structured issues. |

## Shared Contracts

| Contract | Purpose |
| --- | --- |
| `UserProfile` | Stable user/account/brand identity. |
| `MarketAnalysis` | Stable market/competitor evidence snapshot. |
| `ContextPack` | Unified input bundle for all generation decisions. |
| `DecisionPoint` | One human or system decision with options, evidence, and rationale. |
| `CandidateSet` | Multiple generated candidates before final selection. |
| `ExplanationTrace` | xAI trace that explains why a candidate or decision exists; serialized stage history uses `stage_steps`, while old `agent_steps` payloads are accepted only as read-time compatibility input. |
| `LearningSignal` | Observation that updates profile, market memory, or strategy. |
| `PerformanceSnapshot` | Post-publish or post-review measured result. |
| `CapabilitySnapshot` | Full projected view of one project/workflow across the five agent-owned capability groups; includes `validate()` / `is_valid()` structural quality gates. |

## Architecture Registry

`nori.core.architecture` exposes the canonical capability map for orchestration, docs, and future CLI/UI inspection:

| API | Purpose |
| --- | --- |
| `CapabilityModule` | Metadata for one capability group: name, package, responsibility, agents, contracts, dependencies. |
| `CAPABILITY_MODULES` | Ordered tuple of the five capability groups. |
| `capability_module_names()` | Returns the canonical capability order. |
| `get_capability_module(name)` | Looks up a capability by canonical name, returning `None` for unknown names. |

## Project Projection API

The first compatibility bridge from the existing ops world into the new domain architecture is `AccountOperationProject` projection. This lets current account-ops artifacts enter the five-module architecture without forcing a wholesale file migration.

| Module | Projection API | Output |
| --- | --- | --- |
| `user_profiling` | `UserProfilingFacade.build_from_project(project)` | `UserProfile` with project metadata and profile source refs. |
| `market_analysis` | `MarketAnalysisFacade.build_from_project(project)` | `MarketAnalysis` with competitor evidence and project metadata. |
| `context` | `ContextPackBuilder.build_from_project(project, task_id=...)` | `ContextPack` assembled from project profile, platform strategy, market evidence, task, skills, content strategy, assets, and decisions. |
| `content_generation` | `ContentGenerationFacade.candidate_set_from_project(project, task_id=...)` | `CandidateSet` filtered to the task and linked back to the `ContextPack` trace. |
| `learning_loop` | `LearningLoopFacade.performance_snapshots_from_project(project)` / `learning_signals_from_project(project, ...)` | Normalized monitoring snapshots and learning signals. |
| `learning_loop` | `LearningLoopFacade.capability_snapshot_from_project(project, ...)` | `CapabilitySnapshot` containing profile, market, context packs, candidate sets, monitoring snapshots, and learning signals. |

## Snapshot Quality Gates

`CapabilitySnapshot.validate()` returns structured issue dictionaries with `code`, `path`, `message`, `severity`, and `metadata`. Current gates catch:

| Issue code | Meaning |
| --- | --- |
| `missing_required_module` | `module_names` does not include all five domain modules. |
| `candidate_set_without_context` | A candidate set references a task that has no matching `ContextPack`. |
| `selected_candidate_missing` | `selected_candidate_id` does not exist in that candidate set's candidate rows. |

## Design Rules

| Rule | Meaning |
| --- | --- |
| Shared first | New modules must consume shared contracts, not ad hoc dicts. |
| Facade over implementation | Top-level module packages should expose stable orchestration APIs and keep implementation details underneath. |
| Evidence everywhere | Every decision and candidate should retain source refs / evidence refs. |
| Human decision is explicit | Human choices are modeled, not hidden in free-text comments. |
| Learning is separate from generation | Generated content should not mutate preference/market state directly. |
| Canonical imports only | Agent/model code imports from `nori.agents.user_profiling`, `nori.agents.market_analysis`, `nori.agents.planning`, `nori.agents.content_generation`, or `nori.agents.learning_loop`; legacy roots are not importable. |

## Migration Strategy

| Phase | Change |
| --- | --- |
| P0 | Add shared `nori/core` contracts and facades that wrap existing models. |
| P1 | Add `user_profiling`, `market_analysis`, `planning`, `content_generation`, `learning_loop` packages as thin orchestrators. |
| P2 | Move review/monitoring/strategy implementation into `nori.agents.learning_loop`. |
| P3 | Move content producer/package helpers into `nori.agents.content_generation`. |
| P4 | Move intake/account planning and XHS analyzer implementation into `nori.agents.user_profiling` and `nori.agents.market_analysis`. |
| P5 | Move NoteMaker/CoverDirector generation chain into `nori.agents.content_generation`. |
| P6 | Remove legacy roots `nori/gen_agents`, `nori/ops_agents`, `nori/ana_agents`, `nori/ops_models`, `nori/agent_models`, and `nori/agent_utils`; keep tests enforcing canonical-only imports. |

Current implementation note: each domain package owns both facade-level orchestration and its internal implementation modules. Legacy package roots are gone.
