<!-- Last verified: 2026-05-24 | Current stage: P4 Review And Iteration | Status: implemented -->

# Spec: Package Review Gate

## Background

P3 can produce a draft `ContentPackage`. Before export, publishing, or strategy iteration, the package needs a deterministic review gate that can run in the default offline test suite. The first version should be text-only and rule-based, while preserving a contract that future LLM reviewers can reuse.

## Goal

Implement two P4 reviewers:

- `ComplianceReviewerAgent`: package text safety and publishing-readiness checks.
- `ConsistencyReviewerAgent`: task brief / package / cover prompt alignment checks.

Both return `ComplianceReview` because the existing ops model already stores review id, package id, task id, status, score, issues, suggestions, reviewer, and metadata.

## Non-Goals

- No live LLM call in this spec.
- No platform publishing.
- No automatic package rewriting.
- No metrics snapshot or strategy iteration generation.

## Public API

```python
ComplianceReviewerAgent().run(package, task=None, client_brief=None, project=None) -> ComplianceReview
ConsistencyReviewerAgent().run(package, task=None, client_brief=None, project=None) -> ComplianceReview
ReviewGateAgent().run(package, task=None, client_brief=None, project=None) -> list[ComplianceReview]
review_content_package(package, ...) -> list[ComplianceReview]
```

## Issue Schema

Each review issue is a dict:

```python
{
    "code": "non_empty_body",
    "severity": "low|medium|high",
    "field": "body",
    "message": "...",
    "evidence": "optional short evidence"
}
```

## Status And Score

| Status | Rule |
| --- | --- |
| `passed` | No high issue and score >= 85. |
| `needs_revision` | Medium issues exist or score is 60-84. |
| `blocked` | Any high issue or score < 60. |

Score starts at 100 and subtracts severity weights:

| Severity | Penalty |
| --- | --- |
| high | 40 |
| medium | 15 |
| low | 5 |

## Compliance Checks

| Check | Severity |
| --- | --- |
| Missing title or body. | high |
| Title/body contains client taboo terms. | high |
| Body contains unsupported absolute claims such as guaranteed effect or official certification. | high |
| Title is too long for XHS. | medium |
| Body is too long for current XHS note flow. | medium |
| NoteMaker validation marks `needs_human_review`. | medium |

## Consistency Checks

| Check | Severity |
| --- | --- |
| Package task id/platform conflicts with task. | high |
| Package title/body misses the task topic. | medium |
| Package body misses the task objective. | medium |
| Cover prompt misses the generated title or cover title. | medium |
| Required assets are not represented in `material_usage`. | low |
| Client brand is absent from package content when a brand name exists. | low |

## Project Attachment

If `project` is provided, reviewers append their `ComplianceReview` into `project.compliance_reviews` and leave package content unchanged.

## Verification

- Unit tests cover pass, compliance block, consistency needs-revision, and project attachment.
- Default suite remains `python -m pytest tests -q`.
