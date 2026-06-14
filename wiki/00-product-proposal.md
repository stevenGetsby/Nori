<!-- Last verified: 2026-05-24 | Current stage: P1 Account-Ops Backend -->

# Nori Product Proposal

## Product Position

| Item | Decision |
| --- | --- |
| One-liner | Nori is an AI content-operations Agent system for Xiaohongshu-first account planning, content production, review, and iteration. |
| Current wedge | Turn a user's prompt and assets into an executable XHS note draft plus cover, with account-planning context. |
| Direction | Move from one-shot content generation to account-operations SOP: plan account -> produce content -> review -> measure -> iterate. |
| Primary platform | Xiaohongshu (`xhs`) first. Douyin/Kuaishou/Weibo exist in collection infrastructure, not the product surface yet. |
| User mode | Local personal backend first: Python API, CLI/smoke scripts, local files, tests. No full frontend in current stage. |

## Target Users

| User | Job |
| --- | --- |
| Creator/operator | Convert messy brand/product/material inputs into structured note briefs, copy, cover, and task packages. |
| Account-ops service provider | Plan a client account, calendar, KPI, and content tasks before manual publishing. |
| Agent developer | Extend the pipeline safely by reading stable contracts, stages, and backlog instead of scattered notes. |

## Core Loop

```text
Client / creator input
-> Intake: normalize intention + assets
-> Account planning: positioning, IP portrait, benchmarks
-> Operation planning: plan, KPI, calendar, content tasks
-> Content production: note draft + cover image
-> Review: compliance / consistency / quality
-> Package: export-ready artifact and version trail
-> Metrics / strategy iteration
```

## What Exists Now

| Area | Status | Canonical source |
| --- | --- | --- |
| LLM gateway | Implemented: config loader, LangChain chat adapter, OpenAI-compatible image clients, chat/image helpers, JSON parsing helper, mode switch. | [20-system-architecture.md](./20-system-architecture.md#llm-gateway) |
| Generation chain | Implemented: `IntakeAgent -> NoteMakerAgent -> CoverDirectorAgent`. | [60-stage-generation-core.md](./60-stage-generation-core.md) |
| Analysis / skill learning | Implemented: XHS note analyzer and session-level skill reports; crawler integration is partly operational. | [62-stage-data-collection-and-skill-learning.md](./62-stage-data-collection-and-skill-learning.md) |
| Account planning | Implemented: `AccountPlannerAgent` plus ops models/agents for operation plan, KPI, calendar. | [61-stage-account-ops-backend.md](./61-stage-account-ops-backend.md) |
| Production bridge | Implemented: `ContentProducerAgent` turns planned tasks into draft `ContentPackage` artifacts. | [63-stage-production-orchestration.md](./63-stage-production-orchestration.md) |
| Test baseline | Existing unit/mocked tests cover agents, ops models, production bridge, LLM JSON helper, and data collection top-notes path. | [85-backlog.md](./85-backlog.md#verification-baseline) |

## What Nori Does Not Do Yet

| Not doing | Reason |
| --- | --- |
| Real publishing | Backend production/review loop is not stable enough; publish adapter should remain reserved. |
| Automated comment/DM operations | Needs risk controls, account safety, and metrics loop first. |
| Full frontend workbench | `web/` is reserved for product UI/prototypes and `backend/` now provides a lightweight service adapter, but the current stage still validates most generation contracts via Python API, CLI, smoke scripts, and local artifacts. |
| Multi-platform product parity | `data_collect` supports more platforms, but Nori product logic is XHS-first. |
| Unbounded live LLM/crawler/image runs in tests | Tests should stay mocked by default; live runs belong to explicit smoke scripts. |

## Product Principles

| Principle | Meaning |
| --- | --- |
| Asset-aware | User images and text are first-class inputs, not decoration. |
| Contract-first | Agent handoff goes through dataclasses/JSON contracts before UI or orchestration. |
| One owner per decision | Intake owns image understanding; CoverDirector owns image generation; ops agents own planning artifacts. |
| Local-first validation | Every stage should be testable without live platform or model calls unless a smoke script explicitly opts in. |
| Skill is internal | Users should not need to understand internal skill routing; Nori selects or derives skills from intent/context. |

## Source Map

| Existing source | Role after wiki |
| --- | --- |
| `README.md` | Lightweight project entry; should point to wiki as canonical docs. |
| `wiki/archive/进度.md` | Historical P0 backend tracker; current status must live in roadmap/backlog. |
| `wiki/archive/legacy-docs/Nori总设计.md` | Historical design note; current pipeline facts are mirrored in stage docs. |
| `wiki/archive/legacy-docs/Agent-*.md` | Agent-specific reference material; keep as supporting docs until migrated. |
| `wiki/archive/legacy-docs/Codex自动化推进计划.md` | Automation log and project-skill context; durable roadmap should live in [01-project-roadmap.md](./01-project-roadmap.md). |
