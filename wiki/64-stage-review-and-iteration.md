<!-- Last verified: 2026-05-24 | Current stage: P4 Review And Iteration -->

# Stage 64: Review And Iteration

## Goal

Create a review gate between generated packages and any export, publish, or strategy iteration workflow:

```text
ContentPackage
  -> ReviewGateAgent
  -> ComplianceReview(compliance)
  -> ComplianceReview(consistency)
  -> MetricsSnapshot(manual)
  -> StrategyIteration
```

The first implementation is deterministic and text-only so it can run in the default offline suite.

## Implemented Modules

| Module | Status | Notes |
| --- | --- | --- |
| `nori/learning_loop/review/review_gate.py` | Implemented | Rule-based compliance and consistency reviewers. |
| `nori/learning_loop/review/policy.py` | Implemented | Pure review policy boundary for compliance/consistency issue calculation, score/status mapping, severity counts, and fix suggestions. |
| `nori/learning_loop/strategy/strategy_iteration.py` | Implemented | Manual metrics snapshot recorder and rule-based strategy iteration. |
| `nori/learning_loop/strategy/policy.py` | Implemented | Pure strategy policy boundary for metric summary, review summary, diagnosis, decisions, and next actions. |
| `tests/test_learning_loop_review_policy.py` | Implemented | Policy-level compliance issues, consistency issues, score/status/severity, and suggestions. |
| `tests/test_learning_loop_review.py` | Implemented | Pass, blocked compliance, needs-revision consistency, and project attachment. |
| `tests/test_learning_loop_strategy_policy.py` | Implemented | Metric aliases/rates, review summaries, weak/strong engagement strategy rules, ref identity, date, and slug helpers. |
| `tests/test_learning_loop_strategy.py` | Implemented | Metrics attachment, blocked review actions, weak/strong engagement diagnosis. |

## Core Contract

| API | Contract |
| --- | --- |
| `ComplianceReviewerAgent().run(package, task=None, client_brief=None, project=None) -> ComplianceReview` | Checks text safety, length, client taboos, absolute claims, and NoteMaker validation. |
| `ConsistencyReviewerAgent().run(package, task=None, client_brief=None, project=None) -> ComplianceReview` | Checks task/package identity, topic/objective alignment, cover prompt alignment, required asset tracking, and brand presence. |
| `content_review_policy.compliance_issues(package, brief) -> list[dict]` | Calculates compliance issue rows only; no mutation. |
| `content_review_policy.consistency_issues(package, task, brief) -> list[dict]` | Calculates consistency issue rows only; no mutation. |
| `content_review_policy.build_review(...) -> ComplianceReview` | Builds review id, score, status, severity metadata, and fix suggestions from issues. |
| `ReviewGateAgent().run(package, task=None, client_brief=None, project=None) -> list[ComplianceReview]` | Runs compliance then consistency. |
| `review_content_package(package, **kwargs) -> list[ComplianceReview]` | Convenience wrapper for the default gate. |
| `MetricsSnapshotAgent().run(ref, metrics, captured_at=None, source="manual", notes=None, project=None) -> MetricsSnapshot` | Records raw manual metrics and normalized summary metadata. |
| `record_metrics_snapshot(ref, metrics, **kwargs) -> MetricsSnapshot` | Convenience wrapper for manual metrics. |
| `strategy_iteration_policy.metric_summary(metrics) -> dict` | Normalizes raw metrics aliases and computes engagement rate. |
| `strategy_iteration_policy.review_summary(reviews) -> dict` | Counts review statuses, issue severities, and top issue codes. |
| `strategy_iteration_policy.{diagnosis,decisions,next_actions}(...) -> list[str]` | Converts evidence summaries into strategy outputs. |
| `StrategyIterationAgent().run(project=None, reviews=None, metrics_snapshots=None, project_id="") -> StrategyIteration` | Turns review and metrics evidence into diagnosis, decisions, and next actions. |
| `create_strategy_iteration(**kwargs) -> StrategyIteration` | Convenience wrapper for strategy iteration. |

## Review Issue Schema

```python
{
    "code": "topic_not_reflected",
    "severity": "low|medium|high",
    "field": "title/body",
    "message": "...",
    "evidence": "optional short evidence",
}
```

## Status And Score

| Status | Rule |
| --- | --- |
| `passed` | No high issue and score >= 85. |
| `needs_revision` | Medium/low issues exist or score is 60-84. |
| `blocked` | Any high issue or score < 60. |

Score starts at 100. High issues subtract 40, medium subtract 15, low subtract 5.

## Current Checks

| Reviewer | Checks |
| --- | --- |
| Compliance | Required title/body, XHS title/body length, client taboo terms, unsupported absolute claims, NoteMaker validation. |
| Consistency | Task id/platform match, task topic/objective reflected in title/body, cover prompt contains title/cover-title terms, required assets represented in `material_usage`, brand reflected when provided. |

## Metrics And Iteration Rules

| Evidence | Rule |
| --- | --- |
| Blocked review | Fix blocking review issues before export/publish/reuse. |
| Needs-revision review | Revise package and rerun review gate. |
| No metrics | Record manual `MetricsSnapshot` before drawing strategic conclusions. |
| Engagement rate < 3% | Diagnose weak engagement; next action should test stronger hook/topic. |
| Engagement rate >= 8% | Diagnose reusable angle; next action should carry topic/title/material pattern forward. |
| Inquiries > 0 | Preserve conversion CTA/source refs for the next task brief. |

## Project Attachment

When `project` is provided, each reviewer appends the returned `ComplianceReview` into `project.compliance_reviews`. Reviewers never mutate package title/body/cover.

Policy helpers never attach to projects. Project mutation stays in `content_reviewer.py`, so policy functions can be tested as pure review rules.

Strategy policy helpers also never attach to projects. Project mutation stays in `strategy_iteration.py`, so metric and iteration rules can be tested independently from agent orchestration.

## Current Constraints

| Constraint | Reason |
| --- | --- |
| Text-only first | Keeps default tests offline and avoids live LLM dependencies. |
| No package rewriting | Review gate should be auditable; rewrite agents can be added later. |
| Manual metrics first | Platform metrics ingestion stays deferred until the manual workflow proves the model. |
| Strategy suggestions only | `StrategyIterationAgent` does not mutate calendars or tasks. |

## Verification

| Test | Coverage |
| --- | --- |
| `tests/test_learning_loop_review_policy.py` | Compliance/consistency issue calculation, score/status/severity metadata, and fix suggestions. |
| `tests/test_learning_loop_review.py` | Compliance pass/block, consistency needs-revision, gate attachment to project. |
| `tests/test_learning_loop_strategy_policy.py` | Metric summary aliases, review summary counts, strategy rules, ref identity, date, and slug behavior. |
| `tests/test_learning_loop_strategy.py` | Manual metrics, project attachment, blocked review actions, weak/strong metrics iteration. |
| `python -m pytest tests/test_learning_loop_review_policy.py tests/test_learning_loop_review.py tests/test_learning_loop_strategy_policy.py tests/test_learning_loop_strategy.py -q` | Fast focused check. |
| `python -m pytest tests -q` | Default offline suite. |

## Next Exit Criteria

| Criteria | Backlog link |
| --- | --- |
| Redacted config/runbook makes live LLM and live crawler setup reproducible without secrets. | [85-backlog.md](./85-backlog.md#p0--documentation-hygiene) |
| Future automatic metrics ingestion can produce the same `MetricsSnapshot` contract. | [85-backlog.md](./85-backlog.md#deferred) |
