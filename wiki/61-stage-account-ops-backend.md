<!-- Last verified: 2026-05-24 | Current stage: P1 Account-Ops Backend -->

# Stage 61: Account-Ops Backend

## Goal

Turn Nori from one-shot generation into an account-operations backend with stable project, planning, KPI, calendar, task, package, review, metrics, and iteration contracts.

## Implemented Modules

| Module | Status | Notes |
| --- | --- | --- |
| `nori/agents/planning/models.py` | Implemented | Provider-free account-operation dataclasses with serialization; `from_dict()` input cleanup uses shared `nori.core.contracts` helpers. |
| `nori/agents/planning/operation_planner/operation_planner.py` | Implemented | LLM JSON path + deterministic fallback + critic metadata + fallback `llm_error` metadata. |
| `nori/agents/planning/operation_planner/project_builder.py` | Implemented | Builds OperationPlanner deterministic fallback projects, including rule-based tasks, calendars, derived KPI snapshots, positioning, asset requirements, and benchmark references. |
| `nori/agents/planning/operation_planner/normalizer.py` | Implemented | Normalizes OperationPlanner LLM operation-plan/calendar output into a fallback project shell, including tasks, date clamps, metadata, and derived KPI snapshot. |
| `nori/agents/planning/kpi_planner/kpi_planner.py` | Implemented | Builds measurable targets; can read project task count; records optional LLM failure metadata on fallback. |
| `nori/agents/planning/kpi_planner/normalizer.py` | Implemented | Normalizes KPIPlanner fallback and LLM output, including task-count defaults, milestone day clamps, and measurement-note fallback preservation. |
| `nori/agents/planning/calendar_planner/calendar_planner.py` | Implemented | Builds scheduled content tasks; records optional LLM failure metadata on fallback. |
| `nori/agents/planning/calendar_planner/normalizer.py` | Implemented | Normalizes CalendarPlanner fallback and LLM output, including task-count caps, scheduled-day clamps, content-pillar repair, and empty-list fallback preservation. |
| `nori/agents/user_profiling/account_planner/account_planner.py` | Implemented | Account positioning and IP portrait. |
| `nori/agents/user_profiling/account_planner/normalizer.py` | Implemented | Normalizes AccountPlanner LLM/search output into stable `AccountPlanResult` fields, including keyword levels, benchmark creators, and fallback metadata. |

## Core Data Model

```text
AccountOperationProject
  client_brief: ClientBrief
  account_positioning: AccountPositioning
  asset_library: AssetLibrary
  competitor_research: CompetitorResearch
  operation_plan: OperationPlan
  kpi_plan: KPIPlan
  content_calendar: ContentCalendar
  content_tasks: list[ContentTask]
  content_packages: list[ContentPackage]
  compliance_reviews: list[ComplianceReview]
  metrics_snapshots: list[MetricsSnapshot]
  strategy_iterations: list[StrategyIteration]
```

## Planning Chain

| Step | Input | Output |
| --- | --- | --- |
| Account planning | User/account context | `AccountPlanResult` |
| Operation planning | `ClientBrief + AccountPlanResult` | `AccountOperationProject` with plan/calendar/tasks |
| KPI planning | `OperationPlan` or project | `KPIPlan` |
| Calendar planning | `OperationPlan + KPIPlan + ClientBrief` | `ContentCalendar` |

## Evidence Models

| Model | Role |
| --- | --- |
| `AccountPositioning` | Typed account positioning result derived from `AccountPlanResult`; preserves legacy dict fields and supports `dict(project.account_positioning)`. |
| `AssetRecord` | One client or generated asset reference with id, kind, usage, status, tags, source, and metadata. |
| `AssetLibrary` | Project-level typed asset index; supports `get(asset_id)` and `usable_assets(usage)`. |
| `CompetitorSample` | One benchmark content sample with title, note id, URL, keyword, metrics, content angles, and provenance. |
| `CompetitorResearch` | Project-level competitor evidence set; supports top-sample ranking and task-reference conversion. |

## Current Constraints

| Constraint | Reason |
| --- | --- |
| No DB persistence | Contracts are still evolving; round-trip JSON is enough. |
| No real publishing | Review/package handoff is not complete. |
| Manual metrics first | Avoid platform scraping dependency until strategy iteration contract is stable. |
| Fallback allowed | Ops planning can produce useful structure without live LLM. |
| Fallback observability | Optional LLM failures must not abort planning, but fallback artifacts should keep redacted `metadata.llm_error` with stage, reason, and error type through `attach_llm_error`. |
| Result normalization boundary | AccountPlanner output-shape cleanup, platform-token stripping, three-level keyword fallback, search-only merge behavior, and IP portrait benchmark derivation live in `account_plan_normalizer`; the agent owns orchestration only. |
| Operation fallback builder boundary | OperationPlanner deterministic fallback construction lives in `operation_project_builder`; the agent owns input normalization, LLM invocation, and critic attachment. |
| Operation plan normalization boundary | OperationPlanner LLM operation/calendar/task output cleanup lives in `operation_plan_normalizer`; the agent owns input normalization, LLM invocation, and critic attachment. |
| KPI normalization boundary | KPIPlanner target defaults, LLM KPI merge, milestone clamping, and measurement-note fallback preservation live in `kpi_plan_normalizer`; the agent owns LLM invocation and critic attachment. |
| Calendar normalization boundary | CalendarPlanner fallback construction, LLM task-row cleanup, scheduled-day clamping, empty-list fallback preservation, and task-count caps live in `calendar_plan_normalizer`; the agent owns input normalization, LLM invocation, and critic attachment. |

## Verification

| Test | Coverage |
| --- | --- |
| `tests/test_workflow_models.py` | Defaults, deep-copy behavior, project round trips, package exports. |
| `tests/test_context_building_operation_planner_project_builder.py` | OperationPlanner deterministic fallback project, calendar, tasks, derived KPI snapshot, safe defaults, asset requirements, and benchmark references. |
| `tests/test_context_building_operation_planner_normalizer.py` | OperationPlanner LLM output merge, task-row normalization, date clamping, fallback-task preservation, and derived KPI snapshot behavior. |
| `tests/test_context_building_operation_planner.py` | Fallback, dict input, mocked LLM JSON, JSON-mode routing, failure fallback metadata. |
| `tests/test_context_building_kpi_planner_normalizer.py` | KPI fallback defaults, LLM KPI merge, milestone clamping, measurement-note fallback, and metadata behavior. |
| `tests/test_context_building_kpi_planner.py` | Operation plan/project inputs, mocked LLM JSON, JSON-mode routing, critic and fallback metadata. |
| `tests/test_context_building_calendar_planner_normalizer.py` | Calendar fallback scheduling, LLM task-row normalization, scheduled-day clamping, content-pillar repair, empty-list fallback, and metadata behavior. |
| `tests/test_context_building_calendar_planner.py` | Calendar task scheduling, project/dict inputs, mocked LLM JSON, JSON-mode routing, failure fallback metadata. |
| `tests/test_context_building_asset_research.py` | Asset/competitor model round trips, helper behavior, and project nesting. |
| `tests/test_context_building_account_positioning.py` | Account positioning extraction, legacy dict compatibility, and planner integration. |
| `tests/test_user_profiling_account_planner_normalizer.py` | AccountPlanner LLM result normalization, keyword cleaning, benchmark creator derivation, and fallback preservation. |
| `tests/test_model_coercion.py` | Shared model coercion defaults used by ops and agent model `from_dict()` methods. |
| `tests/test_domain_model_contracts.py` | `AccountPlannerInput` / `AccountPlanResult` serialization and restoration used before ops handoff. |

## Handed Off To P3

| Criteria | Backlog link |
| --- | --- |
| `ContentTask -> ContentPackage` bridge implemented. | [Stage 63 Production Orchestration](./63-stage-production-orchestration.md) |
| Generated package can reference `NoteDraft` and `CoverResult`. | [Stage 63 Production Orchestration](./63-stage-production-orchestration.md) |
| Review agent can attach `ComplianceReview`. | [P4 Review and Iteration](./85-backlog.md#p4-review-and-iteration) |
