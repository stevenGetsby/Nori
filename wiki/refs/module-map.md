<!-- Last verified: 2026-06-01 -->

# Module Map Reference

This reference holds detailed file-level ownership maps. Keep high-level runtime
architecture in [System Architecture](../20-system-architecture.md).

## Core Model Ownership

| Contract group | Owner module | Public facade |
| --- | --- | --- |
| User/account profile | `nori/core/profile_models.py` | `nori.core` |
| User/source/generated assets | `nori/core/asset_models.py` | `nori.core` |
| Planning and task contracts | `nori/core/planning_models.py` | `nori.core` |
| Capability evidence, context, candidates, learning | `nori/core/capability_models.py` | `nori.core` |
| Cross-module project aggregate | `nori/core/project.py` | `nori.core` |
| Config/runtime/LLM helper contracts | `nori/core/contracts.py` | `nori.core` |

The historical `nori.core.models` facade has been removed. New code should
import from `nori.core` or the narrower owner module when owner clarity matters.

## Workflow Stage Packages

| Stage package | Implementation files |
| --- | --- |
| `nori/agents/user_profiling/intaker/` | `intaker.py`, `package.py`, `normalizer.py`, `taxonomy.py`, `image_tagger.py` |
| `nori/agents/user_profiling/account_planner/` | `account_planner.py`, `package.py`, `fallback.py`, `search.py`, `normalizer.py`, `portrait.py`, `keywords.py` |
| `nori/agents/market_analysis/xhs_note_analyzer/` | `xhs_note_analyzer.py`, `package.py`, `loader.py`, `rules.py`, `note_llm.py`, `session_clustering.py`, `session_llm.py`, `session_reporter.py`, `skill_builder.py` |
| `nori/agents/planning/operation_planner/` | `operation_planner.py`, `package.py`, `project_builder.py`, `project_policy.py`, `normalizer.py` |
| `nori/agents/planning/kpi_planner/` | `kpi_planner.py`, `package.py`, `normalizer.py` |
| `nori/agents/planning/calendar_planner/` | `calendar_planner.py`, `package.py`, `normalizer.py`, `policy.py`, `task_builder.py` |
| `nori/agents/content_generation/spec_designer/` | `spec_designer.py` |
| `nori/agents/content_generation/artifact_generator/` | `artifact_generator.py` |
| `nori/agents/content_generation/note_maker/` | `note_maker.py`, `package.py` |
| `nori/agents/content_generation/cover_director/` | `cover_director.py`, `package.py`, `output.py` |
| `nori/agents/content_generation/content_producer/` | `content_producer.py`, `package.py`, `state.py` |
| `nori/agents/learning_loop/review/` | `review_gate.py`, `package.py`, `policy.py`, `scoring.py`, `state.py` |
| `nori/agents/learning_loop/strategy/` | `strategy_iteration.py`, `package.py`, `policy.py`, `state.py` |

`nori/agents/supervisor/` is not a workflow stage package. It owns the
user-facing main-chat routing agent and exposes subagents/subworkflows through
injected `SupervisorTool` handlers.

Flat helper module paths such as `nori.agents.content_generation.skill_picker`
and `nori.agents.planning.operation_planner_inputs` should not exist.
Stage-local `schema.py` re-export files should not exist either.

## Shared Runtime Utilities

| Module | Role |
| --- | --- |
| `backend/` | FastAPI product-service boundary for request/response shaping, session routes, local session image uploads/downloads, workflow catalog/resolve routes, content-generation option/action catalogs, backend content-production experiment runs, experiment readiness/run-summary APIs, whitelisted run artifact serving, Swagger/OpenAPI docs, and local uvicorn serving. It calls stable Nori contracts and must not own prompt or agent policy logic. |
| `nori/core/llm.py` | Injectable project LLM gateway used by agents instead of reaching directly into provider globals. |
| `nori/core/agent.py` | Shared agent base and input/prompt builder patterns. |
| `nori/core/workflow.py` | Backend-free workflow abstraction for agents and capability facades. |
| `nori/workflows/adapters.py` | Bridges `WorkflowBase` into runtime `WorkflowSpec` for LangGraph-backed execution and run recording. |
| `nori/workflows/content_production/` | Product-level content production workflow. `stages.py` owns ordered agent-stage orchestration and artifact checkpoints; `stage_support.py` owns pure market/context/summary builders; the package also owns content production state, artifact refs, and the Human Gate before final package generation. |
| `nori/context/compiler.py` | Compiles profile, task, market, skill, strategy, asset, and constraint slices into `ContextPack`. |
| `nori/context/resolver.py` | Builds runtime `ContextBundle` rows and projects task `ContextPack` into agent-specific `ContextView`. |
| `nori/context/adapters.py` | Bridges business `ContextPack` into the runtime `ContextBundle` used for one agent call. |
| `nori/core/artifacts.py` | Stable artifact IDs, stage JSON checkpoints, manifests, and resumable artifact lookup. |
| `nori/shared/llm_json.py` | Required/optional JSON LLM helpers and redacted fallback error formatting. |

## Frontend And Visualization Boundaries

| Path | Role |
| --- | --- |
| `backend/` | Product backend/API adapter boundary. Web clients should call this layer instead of importing Python agent internals. |
| `web/` | Product frontend boundary. Future workbench code and backend-integrated UI should live here. |
| `web/prototypes/` | Static frontend prototypes and product UI experiments. These may use fake/static data. |
| `wiki/visuals/` | Architecture diagrams and documentation visualization only. |
| `hyperframes/` | Promotional video compositions and renders. |

## Account-Ops Modules

| Module | Role |
| --- | --- |
| `nori/agents/user_profiling/schemas/profile.py` | User/account profile schemas: `AccountPositioning`, `UserInput`, `IntakeResult`, `AccountPlannerInput`, `AccountPlanResult`. |
| `nori/agents/market_analysis/schemas/market.py` | Market evidence and learned-skill schemas. |
| `nori/agents/content_generation/schemas/generation.py` | Generated artifact/spec schemas: `ContentDesignSpec`, `ContentPackage`, `NoteDraft`, `CoverResult`, and helper schemas. |
| `nori/agents/learning_loop/schemas/learning.py` | Review, monitoring, and evolution schemas. |
| `nori/agents/supervisor/schemas/supervisor.py` | Main-chat routing contracts: `SupervisorIntent`, `SupervisorTool`, `SupervisorToolRequest`, `SupervisorToolResult`, and `SupervisorTurnResult`. |

Each owner-local `schemas/__init__.py` is a public export surface only; schema implementations live in named modules such as `profile.py`, `market.py`, `generation.py`, and `workflow.py`.

| Module | Role |
| --- | --- |
| `nori/agents/supervisor/supervisor.py` | `NoriSupervisorAgent` plus default tool catalog. It plans or invokes injected handlers and stays independent from `nori.workflows`. |
| `nori/agents/planning/operation_planner/operation_planner.py` | `ClientBrief + AccountPlanResult -> AccountOperationProject`; owns orchestration, LLM request, fallback selection, and critic attachment. |
| `nori/agents/planning/operation_planner/package.py` | Restores operation-planner inputs, normalizes start dates/horizons, and builds JSON-only SOP prompts. |
| `nori/agents/planning/operation_planner/project_builder.py` | Builds deterministic operation projects, tasks, calendars, and derived KPI snapshots. |
| `nori/agents/planning/operation_planner/project_policy.py` | Pure operation-planning fallback policy. |
| `nori/agents/planning/operation_planner/normalizer.py` | Merges LLM operation/calendar JSON into fallback project shells. |
| `nori/agents/planning/kpi_planner/kpi_planner.py` | `OperationPlan -> KPIPlan`. |
| `nori/agents/planning/kpi_planner/package.py` | Restores KPI planner inputs and builds JSON-only KPI prompts. |
| `nori/agents/planning/kpi_planner/normalizer.py` | Builds deterministic KPI fallback and merges LLM KPI JSON. |
| `nori/agents/planning/calendar_planner/calendar_planner.py` | `OperationPlan + KPIPlan + ClientBrief -> ContentCalendar`. |
| `nori/agents/planning/calendar_planner/package.py` | Restores calendar planner inputs and builds JSON-only calendar prompts. |
| `nori/agents/planning/calendar_planner/normalizer.py` | Builds and merges `ContentCalendar` shells. |
| `nori/agents/planning/calendar_planner/policy.py` | Pure calendar fallback policy. |
| `nori/agents/planning/calendar_planner/task_builder.py` | Builds fallback and normalized LLM `ContentTask` rows. |
| `nori/agents/planning/planner_critics.py` | Shared planner critic policy. |
| `nori/agents/content_generation/social_card_guides.py` | Social-card platform profiles, page plans, style identity rules, and QA checks distilled from Guizang social-card practice. |
| `nori/agents/content_generation/spec_designer/spec_designer.py` | Converts tasks, briefs, intent contracts, assets, and learned skills into `ContentDesignSpec`. |
| `nori/agents/content_generation/artifact_generator/artifact_generator.py` | Executes a frozen `ContentDesignSpec` through concrete generators. |
| `nori/agents/content_generation/note_maker/package.py` | Note skill selection, asset curation, note prompt construction, and note field normalization. |
| `nori/agents/content_generation/cover_director/package.py` | Cover reference selection and cover prompt construction. |
| `nori/agents/content_generation/cover_director/output.py` | Cover image persistence and output error translation. |
| `nori/agents/content_generation/content_producer/content_producer.py` | `ContentTask + NoteSkill + assets -> ContentPackage`. |
| `nori/agents/content_generation/content_producer/package.py` | Content package preparation, stable IDs, provenance, and package assembly. |
| `nori/agents/content_generation/content_producer/state.py` | Production error classification and project/task status updates. |
| `nori/agents/learning_loop/review/review_gate.py` | `ContentPackage + optional task/brief/project -> ComplianceReview[]`. |
| `nori/agents/learning_loop/review/package.py` | Restores review inputs and derives missing client brief context. |
| `nori/agents/learning_loop/review/policy.py` | Compliance and consistency issue policy. |
| `nori/agents/learning_loop/review/scoring.py` | Review issue rows, severity penalties, score/status mapping, and fix suggestions. |
| `nori/agents/learning_loop/review/state.py` | Attaches compliance reviews to optional projects. |
| `nori/agents/learning_loop/strategy/strategy_iteration.py` | Records metrics and creates strategy iterations. |
| `nori/agents/learning_loop/strategy/package.py` | Restores strategy inputs and derives default evidence lists. |
| `nori/agents/learning_loop/strategy/policy.py` | Metric normalization, evidence summary, diagnosis, decisions, and next actions. |
| `nori/agents/learning_loop/strategy/state.py` | Attaches metrics snapshots and strategy iterations to optional projects. |

Removed roots: `nori/gen_agents`, `nori/ops_agents`, `nori/ana_agents`,
`nori/ops_models`, `nori/agent_models`, and `nori/agent_utils`.
