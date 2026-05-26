<!-- Last verified: 2026-05-24 | Current stage: P4 Review And Iteration | Status: implemented -->

# Spec: Metrics And Strategy Iteration

## Background

P4 now has a deterministic review gate. The remaining loop is to attach manual metrics to a package/task/project and turn reviews plus metrics into next-cycle strategy actions. This must work without live platform scraping.

## Goal

Implement:

- `MetricsSnapshotAgent`: normalize manual metrics into `MetricsSnapshot` and optionally attach to a project.
- `StrategyIterationAgent`: turn `ComplianceReview[] + MetricsSnapshot[]` into `StrategyIteration`.

## Non-Goals

- No automatic metrics ingestion from XHS or other platforms.
- No LLM diagnosis in this spec.
- No mutation of calendars or content tasks.
- No rewriting generated content.

## Public API

```python
MetricsSnapshotAgent().run(ref, metrics, captured_at=None, source="manual", notes=None, project=None) -> MetricsSnapshot
record_metrics_snapshot(ref, metrics, ...) -> MetricsSnapshot

StrategyIterationAgent().run(project=None, reviews=None, metrics_snapshots=None, project_id="") -> StrategyIteration
create_strategy_iteration(project=None, reviews=None, metrics_snapshots=None, project_id="") -> StrategyIteration
```

## Metrics Contract

`metrics` is a dict of observed values. Common keys:

| Key | Meaning |
| --- | --- |
| `views` | Exposure / impressions / reads. |
| `likes` | Likes. |
| `collections` or `collected` | Collections / saves. |
| `comments` | Comments. |
| `shares` | Shares. |
| `followers_delta` | Follower delta after the package/cycle. |
| `inquiries` | Manual lead or inquiry count. |

The agent stores the raw metric dict unchanged and adds normalized summary metadata.

## Strategy Rules

| Evidence | Diagnosis / action |
| --- | --- |
| Any blocked review | Next action must fix blocking review issues before export/publish. |
| Any needs-revision review | Next action should revise package and rerun review gate. |
| No metrics snapshots | Next action should record manual metrics before strategic conclusions. |
| Engagement rate < 3% when views exist | Diagnose weak engagement and suggest testing stronger hook/topic. |
| Engagement rate >= 8% when views exist | Diagnose strong engagement and suggest reusing angle/pillar. |
| Inquiries > 0 | Suggest preserving conversion angle and source refs. |

## Project Attachment

If `project` is provided:

- `MetricsSnapshotAgent` appends to `project.metrics_snapshots`.
- `StrategyIterationAgent` defaults to project reviews/snapshots and appends to `project.strategy_iterations`.

## Verification

- Unit tests cover package/task/string refs, project attachment, blocked review actions, weak/strong metrics, and no-metrics guidance.
- Default suite remains `python -m pytest tests -q`.
