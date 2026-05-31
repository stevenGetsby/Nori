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
| `nori.context` | `ContextCompiler`, `ContextPackBuilder`, `ContextView`, `ContextBundle`, `ContextSource`, `ContextResolver`, `attach_context_pack(...)`. |
| `nori.memory` | `StableProfile`, `SessionMemory`, `TaskMemory`, stores, retrieval, promotion. |
| `nori.workflows` | `WorkflowRun`, `StageRun`, `WorkflowRunner`, `RuntimeRunRecorder`, human gates, and artifact-ref recording. |

`WorkflowRunner` is backed by LangGraph. It compiles `WorkflowSpec` into a `StateGraph`, wraps each coarse-grained `StageSpec.handler` with LangChain Core `RunnableLambda`, and records stage status plus artifact references into `WorkflowRun`.

`StageSpec` can declare a `HumanGateSpec`. The default `human_gate_mode` is `skip`, so tests and automated live runs do not block. Product-facing runs can switch to `pause`; the workflow then records `waiting_for_human` without marking the run as failed.

`nori.core.WorkflowBase` is the backend-free base abstraction for capability facades. It owns `workflow_name`, ordered step metadata, and simple in-process `run_steps(...)`. Runtime execution is separate: `nori.workflows.workflow_spec_from_base(...)` converts a `WorkflowBase` into `WorkflowSpec`, and `WorkflowRunner` executes that spec through the configured backend.

`ContextPack` and `ContextBundle` are different layers. `ContextPack` is a business-generation input compiled by `nori.context.ContextCompiler` from profile, task, market, skills, strategy, and assets. `ContextResolver.for_agent(...)` projects it into a `ContextView` for a specific agent. `ContextBundle` is the runtime envelope for one agent call. Use `nori.context.attach_context_pack(...)` to attach the business pack into the runtime bundle as a source and payload entry.

`ArtifactStore` and `WorkflowRun.artifact_refs` are also bridged explicitly. Stage handlers can return `StoredArtifact`, `_artifact_ref`, or `_artifact_refs`; the LangGraph runner records normalized paths into `StageRun.output_ref` and `WorkflowRun.artifact_refs`.

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
| Core/runtime split | `nori.core.WorkflowBase` defines workflow shape; `nori.workflows` owns runtime specs, execution, human gates, and run records. |
| Context bridge | `ContextPack` stays in business/core contracts; `ContextBundle` stays in runtime context; `attach_context_pack(...)` is the bridge. |
| Context compiler owner | `ContextCompiler` / `ContextPackBuilder` belongs to `nori.context`; planning can re-export it but should not own context compilation. |
| Artifact bridge | Long-running stages write artifacts through `ArtifactStore`; workflow runtime records the returned refs instead of duplicating artifact persistence. |
| Graph execution | Multi-stage workflows should enter through `WorkflowSpec` + `WorkflowRunner`; do not recreate manual stage loops in scripts. |
| Coarse graph nodes | LangGraph nodes should represent checkpoint/retry/human-gate boundaries, not every helper or normalizer. |
| Human gate mode | Human gates default to `skip` for tests; use `pause` only when a product surface can resume after human review. |
| Agents own business behavior | Business entrypoints go through `nori.agents.*`; avoid adding a separate `domains/` package. |
| Context is separate from planning | System-level context assembly belongs in `nori.context`; planning agents remain under the planning capability. |
| Memory is separate from context | Durable facts and promotion policy belong in `nori.memory`; context only assembles what a specific call needs. |
| No legacy compatibility layer | `nori.domain`, `DomainSnapshot`, and the old top-level business roots are removed before launch. |
