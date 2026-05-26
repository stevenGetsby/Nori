<!-- Last verified: 2026-05-25 | Current stage: Architecture Refactor -->

# Spec: Domain Architecture Refactor

## Goal

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
| `shared` | `nori/core/models.py`, `nori/core/architecture.py` | Common contract types, canonical domain registry, context packs, decision traces, evidence references, learning signals. |
| `user profiling` | `nori/user_profiling/facade.py` | Long-lived user/account/brand/preferences/constraints profiles. |
| `market analysis` | `nori/market_analysis/facade.py` | Benchmark samples, market snapshots, trend insights, audience insights. |
| `context building` | `nori/context_building/facade.py`, operation/KPI/calendar planner modules, planner critics | Build operation project context, KPI plans, content calendars, `ContentTask` rows, and `ContextPack` from profile + task + market + assets + history. |
| `content generation` | `nori/content_generation/facade.py`, `content_producer/*`, `note_maker/*`, `cover_director/*` | Produce content packages, manage production state/provenance, group candidates, and expose final deliverables. |
| `learning loop` | `nori/learning_loop/facade.py`, `review/*`, `strategy/*` | Review gates, monitoring snapshots, analytics, feedback signals, preference updates, strategy iteration. |

## Public Entrypoint

`nori.domain` is the recommended stable import path for upper layers that need the complete projected architecture:

| API | Purpose |
| --- | --- |
| `build_domain_snapshot(project, ...)` | Builds a full `DomainSnapshot` from an `AccountOperationProject` or persisted project dict. |
| `validate_domain_snapshot(snapshot)` | Validates a `DomainSnapshot` object or persisted snapshot dict and returns structured issues. |

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
| `DomainSnapshot` | Full projected view of one project/workflow across the five domain modules; includes `validate()` / `is_valid()` structural quality gates. |

## Architecture Registry

`nori.core.architecture` exposes the canonical module map for orchestration, docs, and future CLI/UI inspection:

| API | Purpose |
| --- | --- |
| `DomainModule` | Metadata for one domain module: name, package, facade, responsibility, contracts, dependencies. |
| `DOMAIN_MODULES` | Ordered tuple of the five business modules. |
| `domain_module_names()` | Returns the canonical module order. |
| `get_domain_module(name)` | Looks up a module by canonical name, returning `None` for unknown names. |

## Project Projection API

The first compatibility bridge from the existing ops world into the new domain architecture is `AccountOperationProject` projection. This lets current account-ops artifacts enter the five-module architecture without forcing a wholesale file migration.

| Module | Projection API | Output |
| --- | --- | --- |
| `user_profiling` | `UserProfilingFacade.build_from_project(project)` | `UserProfile` with project metadata and profile source refs. |
| `market_analysis` | `MarketAnalysisFacade.build_from_project(project)` | `MarketAnalysis` with competitor evidence and project metadata. |
| `context_building` | `ContextPackBuilder.build_from_project(project, task_id=...)` | `ContextPack` assembled from project profile, market evidence, task, assets, and decisions. |
| `content_generation` | `ContentGenerationFacade.candidate_set_from_project(project, task_id=...)` | `CandidateSet` filtered to the task and linked back to the `ContextPack` trace. |
| `learning_loop` | `LearningLoopFacade.performance_snapshots_from_project(project)` / `learning_signals_from_project(project, ...)` | Normalized monitoring snapshots and learning signals. |
| `learning_loop` | `LearningLoopFacade.domain_snapshot_from_project(project, ...)` | `DomainSnapshot` containing profile, market, context packs, candidate sets, monitoring snapshots, and learning signals. |

## Snapshot Quality Gates

`DomainSnapshot.validate()` returns structured issue dictionaries with `code`, `path`, `message`, `severity`, and `metadata`. Current gates catch:

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
| Canonical imports only | Agent/model code imports from `nori.user_profiling`, `nori.market_analysis`, `nori.context_building`, `nori.content_generation`, or `nori.learning_loop`; legacy roots are not importable. |

## Migration Strategy

| Phase | Change |
| --- | --- |
| P0 | Add shared `nori/core` contracts and facades that wrap existing models. |
| P1 | Add `user_profiling`, `market_analysis`, `context_building`, `content_generation`, `learning_loop` packages as thin orchestrators. |
| P2 | Move review/monitoring/strategy implementation into `nori.learning_loop`. |
| P3 | Move content producer/package helpers into `nori.content_generation`. |
| P4 | Move intake/account planning and XHS analyzer implementation into `nori.user_profiling` and `nori.market_analysis`. |
| P5 | Move NoteMaker/CoverDirector generation chain into `nori.content_generation`. |
| P6 | Remove legacy roots `nori/gen_agents`, `nori/ops_agents`, `nori/ana_agents`, `nori/ops_models`, `nori/agent_models`, and `nori/agent_utils`; keep tests enforcing canonical-only imports. |

Current implementation note: each domain package owns both facade-level orchestration and its internal implementation modules. Legacy package roots are gone.
