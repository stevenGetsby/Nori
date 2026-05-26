<!-- Last verified: 2026-05-24 | Current stage: P3 Production Orchestration | Status: implemented -->

# Spec: ContentTask Production Bridge

## Background

P1 can plan `ContentTask` objects, and P0 can generate `NoteDraft` and `CoverResult`. The missing P3 boundary is a small orchestration layer that turns a planned task into a durable `ContentPackage` without adding persistence, publishing, or live-service assumptions to ops models.

## Goal

Implement `ContentTask -> NoteMakerAgent -> CoverDirectorAgent -> ContentPackage` as a testable Python API.

## Non-Goals

- No real publishing adapter.
- No DB or filesystem artifact registry beyond the cover path returned by `CoverDirectorAgent`.
- No compliance review in this spec; P4 owns `ComplianceReview`.
- No automatic fallback note writing if `NoteMakerAgent` fails.

## Contract

Public API:

```python
ContentProducerAgent().run(
    task,
    skills=[...],
    assets=[...],
    out_dir=...,
    client_brief=None,
    project=None,
    intent=None,
    context=None,
    use_cover=True,
) -> ContentPackage
```

Convenience API:

```python
produce_content_package(task, skills=[...], assets=[...], out_dir=...)
```

## Input Normalization

| Input | Rule |
| --- | --- |
| `task` | Accept `ContentTask` or dict; normalize through `ContentTask.from_dict`. |
| `skills` | Pass through to `NoteMakerAgent`; at least one skill is required by NoteMaker. |
| `assets` | Accept `UserAsset` or dict. If no text asset is present, add one synthesized task brief text asset. |
| `client_brief` | Optional `ClientBrief` or dict; contributes brand, audience, goals, constraints, taboos, source materials. |
| `project` | Optional `AccountOperationProject`; receives the package and error metadata. |

## Output Mapping

| `ContentPackage` field | Source |
| --- | --- |
| `package_id` | `pkg_{task_id}` or stable fallback from title/topic. |
| `task_id` | `ContentTask.task_id`. |
| `platform` | `ContentTask.platform`. |
| `title` / `body` / `tags` | `NoteDraft`. |
| `cover_path` | `CoverResult.cover_path` when cover generation is enabled; otherwise `NoteDraft.cover_path`. |
| `image_paths` | `NoteDraft.image_paths` plus cover reference paths excluding duplicates. |
| `prompts.note_draft` | `NoteDraft.to_dict()`. |
| `prompts.cover_result` | `CoverResult.to_dict()` when present. |
| `material_usage` | Normalized input assets and task required assets. |
| `source_refs` | `ContentTask.references` plus skill id and project/client refs. |
| `status` | `draft` on success. |
| `metadata.production` | Producer version, cover enabled flag, task status before production. |

## Failure Contract

If `NoteMakerAgent` or `CoverDirectorAgent` fails:

- Raise `ContentProductionError`.
- Set `task.status = "failed"`.
- Add a structured error to `task.metadata["production_error"]`.
- If `project` is provided, append the same error to `project.metadata["production_errors"]`.
- Do not create a partial `ContentPackage`.

## Verification

- Unit tests use fake NoteMaker/CoverDirector implementations, no live LLM or image call.
- Default suite remains `python -m pytest tests -q`.
