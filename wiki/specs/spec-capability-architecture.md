# Spec: Capability and Runtime Architecture

## Goal

Nori is organized around explicit runtime state plus agent-owned business capabilities:

```text
nori.core
  -> nori.sessions
  -> nori.context
  -> nori.memory
  -> nori.workflows
  -> nori.agents.user_profiling
  -> nori.agents.market_analysis
  -> nori.agents.planning
  -> nori.agents.content_generation
  -> nori.agents.learning_loop
```

The goal is to keep session state, memory, context assembly, workflow execution, and business agents separate enough to test and evolve independently.

## Public Entrypoints

| API | Purpose |
| --- | --- |
| `nori.capabilities.capability_registry_snapshot()` | JSON-serializable registry for the five agent-owned capability groups. |
| `nori.capabilities.build_capability_snapshot(project, ...)` | Builds a complete `CapabilitySnapshot` from an `AccountOperationProject` or persisted project dict. |
| `nori.capabilities.validate_capability_snapshot(snapshot)` | Validates a `CapabilitySnapshot` object or persisted snapshot dict. |
| `nori.workflows.RuntimeRunRecorder` | Creates session/context/workflow snapshots for scripts, CLI, API, and future UI runs. |

There is no `nori.domain` compatibility layer; the product has not shipped yet, so new code uses the capability architecture directly.

## Capability Groups

| Capability | Public package | Responsibility |
| --- | --- | --- |
| User profiling | `nori.agents.user_profiling` | Intake, asset tagging, user/account/brand understanding. |
| Market analysis | `nori.agents.market_analysis` | XHS evidence collection, note skill extraction, market summaries. |
| Planning | `nori.agents.planning` | Operation project, KPI, calendar, and task planning. |
| Content generation | `nori.agents.content_generation` | Note copy, cover generation, and content package assembly. |
| Learning loop | `nori.agents.learning_loop` | Review gates, metrics snapshots, strategy iteration, and aggregate capability snapshots. |

## Runtime State

| Package | Owns |
| --- | --- |
| `nori.sessions` | `Session`, `Turn`, `TaskGoal`, `SessionManager`. |
| `nori.context` | `ContextBundle`, `ContextSource`, `ContextResolver`. |
| `nori.memory` | `StableProfile`, `SessionMemory`, `TaskMemory`, stores, retrieval, promotion. |
| `nori.workflows` | `WorkflowRun`, `StageRun`, `WorkflowRunner`, `RuntimeRunRecorder`. |

## Snapshot Quality Gates

`CapabilitySnapshot.validate()` returns structured issue dictionaries with `code`, `path`, `message`, `severity`, and `metadata`.

Current gates catch:

| Issue code | Meaning |
| --- | --- |
| `missing_required_capability` | `capability_names` does not include all five capability groups. |
| `candidate_set_without_context` | A candidate set references a task that has no matching `ContextPack`. |
| `selected_candidate_missing` | `selected_candidate_id` does not exist in that candidate set's candidate rows. |

## Design Rules

| Rule | Meaning |
| --- | --- |
| Runtime first | New scripts/apps should create session/context/workflow state through `RuntimeRunRecorder`. |
| Agents own business behavior | Business entrypoints go through `nori.agents.*`; avoid adding a separate `domains/` package. |
| Context is separate from planning | System-level context assembly belongs in `nori.context`; planning agents remain under the planning capability. |
| Memory is separate from context | Durable facts and promotion policy belong in `nori.memory`; context only assembles what a specific call needs. |
| No legacy compatibility layer | `nori.domain`, `DomainSnapshot`, and the old top-level business roots are removed before launch. |
