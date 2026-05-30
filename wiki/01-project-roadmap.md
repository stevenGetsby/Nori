<!-- Last verified: 2026-05-25 | Current stage: P1 Account-Ops Backend -->

# Nori Project Roadmap

## Stage Overview

| Stage | Status | File | Goal |
| --- | --- | --- | --- |
| P0 Generation Core | Active / mostly implemented | [60-stage-generation-core.md](./60-stage-generation-core.md) | Stabilize prompt/assets -> note draft -> cover generation. |
| P1 Account-Ops Backend | Active | [61-stage-account-ops-backend.md](./61-stage-account-ops-backend.md) | Represent account-ops projects, plans, KPIs, calendars, tasks, packages, reviews, metrics, and iterations. |
| P2 Data Collection + Skill Learning | Partial | [62-stage-data-collection-and-skill-learning.md](./62-stage-data-collection-and-skill-learning.md) | Collect high-performing notes and turn evidence into reusable NoteSkills. |
| P3 Production Orchestration | Active / bridge implemented | [63-stage-production-orchestration.md](./63-stage-production-orchestration.md) | Bridge `ContentTask -> NoteMaker -> CoverDirector -> ContentPackage`. |
| P4 Review + Iteration | Active / offline loop implemented | [64-stage-review-and-iteration.md](./64-stage-review-and-iteration.md) | Add compliance, consistency, review analysis, and strategy optimization. |
| Later Platform / UI | Deferred | [85-backlog.md](./85-backlog.md#deferred) | Publishing, community ops, metrics ingestion, multi-platform UI/workbench. |
| Capability/Runtime Architecture Refactor | Active / Holly runtime verified | [spec-capability-architecture.md](./specs/spec-capability-architecture.md) | Organize Nori around shared runtime contracts, sessions, context, memory, workflows, and agent-owned capability groups. |

## Feature Index

| Feature | Status | Owner module | Stage |
| --- | --- | --- | --- |
| Model config loader | Done | `nori/nori_config.py` | [60](./60-stage-generation-core.md) |
| LLM client factory | Done | `llms/client.py` | [60](./60-stage-generation-core.md) |
| JSON chat helper | Done, includes raw capture contract | `llms/call.py` | [60](./60-stage-generation-core.md) |
| Intent extractor utility | Implemented, not fully wired | `llms/intent_extractor.py` | [60](./60-stage-generation-core.md) |
| Edit target selector utility | Implemented, upgrade slot | `llms/target_selector.py` | [60](./60-stage-generation-core.md) |
| Intake text + image tagging | Done with mocked tests; live smoke optional | `nori/user_profiling/intaker.py` | [60](./60-stage-generation-core.md) |
| Note draft generation | Done with mocked tests; live smoke optional | `nori/content_generation/note_maker.py` | [60](./60-stage-generation-core.md) |
| Cover image generation | Done with mocked tests; live smoke optional | `nori/content_generation/cover_director.py` | [60](./60-stage-generation-core.md) |
| Account positioning | Done with fallback/search provider seam | `nori/user_profiling/account_planner.py` | [61](./61-stage-account-ops-backend.md) |
| Ops dataclasses | Done | `nori/core/project.py` + owning business model modules | [61](./61-stage-account-ops-backend.md) |
| Operation planner | Done / exposed through planning capability | `nori/agents/planning` | [61](./61-stage-account-ops-backend.md) |
| KPI planner | Done / exposed through planning capability | `nori/agents/planning` | [61](./61-stage-account-ops-backend.md) |
| Calendar planner | Done / exposed through planning capability | `nori/agents/planning` | [61](./61-stage-account-ops-backend.md) |
| DataCollector top notes | Partial / external-service dependent | `data_collect/adapter.py` | [62](./62-stage-data-collection-and-skill-learning.md) |
| XHS note analyzer | Done for single/session skill extraction | `nori/market_analysis/xhs_note_analyzer.py` | [62](./62-stage-data-collection-and-skill-learning.md) |
| ContentTask production bridge | Done / exposed through content-generation capability | `nori/agents/content_generation` | [63](./63-stage-production-orchestration.md) |
| Compliance review agent | Done / exposed through learning-loop capability | `nori/agents/learning_loop` | [64](./64-stage-review-and-iteration.md) |
| Consistency review agent | Done / exposed through learning-loop capability | `nori/agents/learning_loop` | [64](./64-stage-review-and-iteration.md) |
| Manual metrics snapshot workflow | Done / exposed through learning-loop capability | `nori/agents/learning_loop` | [64](./64-stage-review-and-iteration.md) |
| Strategy iteration agent | Done / exposed through learning-loop capability | `nori/agents/learning_loop` | [64](./64-stage-review-and-iteration.md) |
| Automatic metrics ingestion | Deferred | TBD | [85](./85-backlog.md#deferred) |
| Shared capability/runtime contracts | Done | `nori/core/models.py`, `nori/sessions`, `nori/context`, `nori/memory`, `nori/workflows` | [spec](./specs/spec-capability-architecture.md) |
| Capability architecture registry | Done | `nori/core/architecture.py`, `nori/capabilities.py` | [spec](./specs/spec-capability-architecture.md) |
| User profiling facade | Done | `nori/user_profiling/facade.py` | [spec](./specs/spec-domain-architecture.md) |
| Market analysis facade | Done | `nori/market_analysis/facade.py` | [spec](./specs/spec-domain-architecture.md) |
| ContextPack builder | Done | `nori/context_building/facade.py` | [spec](./specs/spec-domain-architecture.md) |
| CandidateSet generation facade | Done | `nori/content_generation/facade.py` | [spec](./specs/spec-domain-architecture.md) |
| Learning loop facade | Done | `nori/learning_loop/facade.py` | [spec](./specs/spec-domain-architecture.md) |
| AccountOperationProject capability projection | Done | `LearningLoopFacade.capability_snapshot_from_project()` | [spec](./specs/spec-capability-architecture.md) |
| CapabilitySnapshot aggregation | Done | `nori/learning_loop/facade.py` | [spec](./specs/spec-capability-architecture.md) |
| CapabilitySnapshot validation | Done | `nori/core/models.py` | [spec](./specs/spec-capability-architecture.md) |
| Public capability entrypoint | Done | `nori/capabilities.py` | [spec](./specs/spec-capability-architecture.md) |

## Milestones

| Milestone | Exit criteria |
| --- | --- |
| M0: Executable core stable | `python -m pytest tests -q` passes; no live LLM/crawler/image required for default suite. |
| M1: Account ops contract stable | `AccountOperationProject` can round-trip from brief -> plan -> KPI -> calendar -> tasks. |
| M2: Task production bridge | A planned `ContentTask` can produce a `ContentPackage` with note text, cover path, prompt snapshots, material usage, and source refs. |
| M3: Review gate | Generated packages receive structured compliance/consistency review before export. |
| M4: Iteration loop | Manual metrics snapshots can create `StrategyIteration` and update the next calendar. |

## Current Operating Rule

Before implementing a task:

```text
1. Read this roadmap.
2. Read the relevant stage file only.
3. Check [85-backlog.md](./85-backlog.md) for the smallest unfinished item.
4. Keep live LLM/crawler/image calls out of normal tests.
5. Update stage/backlog/changelog when a node-level capability changes.
```
