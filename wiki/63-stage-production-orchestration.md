<!-- Last verified: 2026-05-24 | Current stage: P3 Production Orchestration -->

# Stage 63: Production Orchestration

## Goal

Bridge account-ops plans into generated content artifacts:

```text
ContentTask
  -> ContentProducerAgent
  -> NoteMakerAgent
  -> CoverDirectorAgent
  -> ContentPackage
```

The stage connects P1 planning contracts with P0 generation agents. It does not publish content or run compliance review.

## Implemented Modules

| Module | Status | Notes |
| --- | --- | --- |
| `nori/content_generation/content_producer/content_producer.py` | Implemented | Produces `ContentPackage` from a planned `ContentTask`. |
| `nori/content_generation/content_producer/builder.py` | Implemented | Builds production intent/context, restores assets, adds task/brief text context, selects note skill, and maps draft/cover outputs into package fields. |
| `tests/test_content_generation_content_producer_builder.py` | Implemented | Package mapping, material usage, source refs, intent/context construction, skill selection, and text-context fallback. |
| `tests/test_content_generation_content_producer.py` | Implemented | Uses fake NoteMaker/CoverDirector; no live LLM or image calls. |

## Core Contract

| API | Contract |
| --- | --- |
| `ContentProducerAgent().run(task, skills, assets, out_dir, client_brief=None, project=None, intent=None, context=None, use_cover=True)` | Normalize task/brief/assets, produce note draft, optionally produce cover, return `ContentPackage`. |
| `content_package_builder.normalize_assets(assets, task, brief)` | Restore `UserAsset` inputs and add task/brief text context when no text asset exists. |
| `content_package_builder.package_from_outputs(task, draft, cover, ...)` | Map `NoteDraft` / `CoverResult` into `ContentPackage` fields, material usage, source refs, prompts, and production metadata. |
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

Asset inputs:

| Input shape | Normalization |
| --- | --- |
| `UserAsset` | Passed through unchanged. |
| `dict` | Restored through `UserAsset.from_dict(...)` before NoteMaker handoff. |
| Missing text asset | Producer appends a task/brief text asset so NoteMaker always has text context. |

The concrete asset restoration and text-context fallback live in `content_package_builder`; `ContentProducerAgent` only decides when production runs.

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
| `tests/test_content_generation_content_producer_builder.py` | Package mapping, material usage, source refs, intent/context construction, skill selection, and text-context fallback. |
| `tests/test_content_generation_content_producer.py` | Success package mapping, cover skip path, structured failure metadata. |
| `python -m pytest tests/test_content_generation_content_producer_builder.py tests/test_content_generation_content_producer.py -q` | Fast focused check. |
| `python -m pytest tests -q` | Default offline suite. |

## Next Exit Criteria

| Criteria | Owner |
| --- | --- |
| Add text-only compliance reviewer. | [Stage 64 Review And Iteration](./64-stage-review-and-iteration.md) |
| Add consistency reviewer for task brief vs generated title/body/cover prompt. | [Stage 64 Review And Iteration](./64-stage-review-and-iteration.md) |
| Add durable artifact workspace layout if packages need file indexes beyond cover output. | Future spec. |
