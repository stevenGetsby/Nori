<!-- Last verified: 2026-05-24 | Current stage: P3 Production Orchestration -->

# Stage 63: Production Orchestration

## Goal

Bridge account-ops plans into generated content artifacts:

```text
ContentTask
  -> ContextCompiler / ContextResolver
  -> ContextView(ContentSpecAgent)
  -> IntentContract
  -> ContentSpecAgent
  -> ArtifactGenerationAgent
  -> ContentProducerAgent
  -> NoteMakerAgent
  -> CoverDirectorAgent
  -> ContentPackage
```

The stage connects P1 planning contracts with P0 generation agents. It does not publish content or run compliance review.

## Implemented Modules

| Module | Status | Notes |
| --- | --- | --- |
| `nori/context/compiler.py` | Implemented | Compiles platform strategy, market hotspots, learned skills, content strategy, assets, and constraints into a sliced `ContextPack`. |
| `nori/context/resolver.py` | Implemented | Projects `ContextPack` into the `ContextView` consumed by `ContentSpecAgent`. |
| `nori/agents/content_generation/social_card_guides.py` | Implemented | Distills Guizang social-card design practice into reusable XHS/WeChat platform profiles, page plans, style identity rules, and QA checks consumed by specs and cover prompts. |
| `nori/agents/content_generation/spec_designer/spec_designer.py` | Implemented | Builds `ContentDesignSpec` from task, brief, intent contract, assets, and skill evidence before generation. |
| `nori/agents/content_generation/artifact_generator/artifact_generator.py` | Implemented | Executes a `ContentDesignSpec` by filtering selected skills, injecting the spec into intent/context, and delegating to `ContentProducerAgent`. |
| `nori/agents/content_generation/content_producer/content_producer.py` | Implemented | Produces `ContentPackage` from a planned `ContentTask`. |
| `nori/agents/content_generation/content_producer/package.py` | Implemented | `ContentPackageAssembler` prepares deterministic production inputs and maps draft/cover outputs into package fields. |
| `tests/test_content_generation_content_producer_package.py` | Implemented | Class-based package assembly, material usage, source refs, intent/context construction, skill selection, and text-context fallback. |
| `tests/test_content_generation_content_producer.py` | Implemented | Uses fake NoteMaker/CoverDirector; no live LLM or image calls. |

## Core Contract

| API | Contract |
| --- | --- |
| `ContextPackBuilder().build(...)` / `.build_from_project(...)` | Build the task-level context pack used by production orchestration. Canonical owner is `nori.context`; planning only re-exports it. |
| `ContextResolver().for_agent("ContentSpecAgent", pack) -> ContextView` | Select only the slices needed for spec design. |
| `ContentSpecAgent().run(context_view=...) -> ContentDesignSpec` | Preferred production path. Produce an inspectable generation blueprint from platform, market, skill, content strategy, asset, and constraint context slices. |
| `ContentSpecAgent().run(task, skills, assets=None, client_brief=None, project=None, intent_contract=None, intent=None, context=None) -> ContentDesignSpec` | Direct-input path for focused tests and manual calls when a compiled context view is not available. |
| `nori.agents.content_generation.social_card_guides.social_card_profile(...)` | Build reusable social-card platform profiles for XHS image-text posts and WeChat cover pairs. These are spec inputs, not a separate generator. |
| `ArtifactGenerationAgent().run(spec, task, skills, assets, out_dir, ...) -> ContentPackage` | Instantiate a spec through the current package generator; it passes `content_design_spec` into both intent and context so lower-level generators can obey the plan without owning it. |
| `ContentProducerAgent().run(task, skills, assets, out_dir, client_brief=None, project=None, intent=None, context=None, intent_contract=None, use_cover=True)` | Normalize task/brief/assets, pass optional `IntentContract` into generation context/metadata, produce note draft, optionally produce cover, return `ContentPackage`. |
| `ContentPackageAssembler.prepare(task, brief, ...)` | Restore `UserAsset` inputs, add task/brief text context when no text asset exists, and build production intent/context. |
| `ContentPackageAssembler.build(task, draft, cover, ...)` | Map `NoteDraft` / `CoverResult` into `ContentPackage` fields, material usage, source refs, prompts, and production metadata. |
| `produce_content_package(task, **kwargs)` | Convenience wrapper with optional dependency injection for tests. |
| `ContentProductionError` | Raised on note/cover/production failure after attaching structured metadata to task/project. |

## Output Mapping

| `ContentPackage` field | Source |
| --- | --- |
| `title`, `body`, `tags` | `NoteDraft`. |
| `cover_path` | `CoverResult.cover_path` if cover is enabled; otherwise `NoteDraft.cover_path`. |
| `image_paths` | `NoteDraft.image_paths` plus cover reference paths, deduped. |
| `prompts.note_draft` | Full `NoteDraft.to_dict()` snapshot; restorable with `NoteDraft.from_dict(...)`. |
| `prompts.cover_result` | Full `CoverResult.to_dict()` snapshot or `None` when cover is skipped; restorable with `CoverResult.from_dict(...)`. |
| `material_usage` | Input assets plus `ContentTask.required_assets`. |
| `source_refs` | Task references, note skill ids, client brief, and project id. |
| `metadata.production` | Producer version, prior task status, cover flags. |
| `metadata.intent_contract` | Optional frozen intent contract snapshot used by generation and quality review. |

Asset inputs:

| Input shape | Normalization |
| --- | --- |
| `UserAsset` | Passed through unchanged. |
| `dict` | Restored through `UserAsset.from_dict(...)` before NoteMaker handoff. |
| Missing text asset | Producer appends a task/brief text asset so NoteMaker always has text context. |

Concrete asset restoration, text-context fallback, stable IDs, provenance rows, and package field mapping live in `ContentPackageAssembler`; `ContentProducerAgent` only decides when production runs.

`ContentSpecAgent` and `ArtifactGenerationAgent` are the public production path. There is no compatibility router for text/image/package routes: skill/spec decisions happen before execution, and `NoteMakerAgent`, `CoverDirectorAgent`, and `ContentProducerAgent` remain specialized child agents because text, image, and future video/article artifacts have different provider contracts and failure modes.

## Failure Policy

| Failure | Behavior |
| --- | --- |
| Note generation fails | Raise `ContentProductionError`, set `task.status="failed"`, write `task.metadata.production_error`, append project metadata if provided. |
| Cover generation fails | Same failure contract; no partial `ContentPackage` is returned. |
| Cover disabled | Still produces a `ContentPackage`; `cover_result` prompt snapshot is `None`. |

## Current Constraints

| Constraint | Reason |
| --- | --- |
| No DB persistence | Existing ops contracts are JSON round-trip first. |
| No automatic compliance review | P4 owns `ComplianceReview` and consistency review. |
| No real publishing | Publishing remains deferred until review/package safety is stable. |
| Skills required | NoteMaker remains LLM-required and skill-driven. |

## Verification

| Test | Coverage |
| --- | --- |
| `tests/test_content_generation_content_producer_package.py` | Package mapping, material usage, source refs, intent/context construction, skill selection, and text-context fallback. |
| `tests/test_content_generation_content_producer.py` | Success package mapping, cover skip path, structured failure metadata. |
| `tests/test_content_generation_entrypoints.py` | Removed-router guard and live workflow spec-before-execution checks. |
| `tests/test_content_generation_spec_pipeline.py` | Spec -> executor composition and skill/spec decoupling behavior. |
| `python -m pytest tests/test_content_generation_content_producer_package.py tests/test_content_generation_content_producer.py -q` | Fast focused check. |
| `python -m pytest tests -q` | Default offline suite. |

## Next Exit Criteria

| Criteria | Owner |
| --- | --- |
| Add text-only compliance reviewer. | [Stage 64 Review And Iteration](./64-stage-review-and-iteration.md) |
| Add consistency reviewer for task brief vs generated title/body/cover prompt. | [Stage 64 Review And Iteration](./64-stage-review-and-iteration.md) |
| Add durable artifact workspace layout if packages need file indexes beyond cover output. | Future spec. |
