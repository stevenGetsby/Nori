from __future__ import annotations

from nori.agents.learning_loop.strategy import policy as strategy_iteration_policy
from nori.agents.learning_loop.models import ComplianceReview, MetricsSnapshot


def _passed_review() -> ComplianceReview:
    return ComplianceReview(review_id="review_passed", status="passed", score=95)


def _blocked_review() -> ComplianceReview:
    return ComplianceReview(
        review_id="review_blocked",
        status="blocked",
        score=40,
        issues=[{"code": "unsupported_absolute_claim", "severity": "high"}],
    )


def _weak_snapshot() -> MetricsSnapshot:
    return MetricsSnapshot(
        snapshot_id="metric_weak",
        ref_id="pkg_001",
        metrics={"views": 1000, "likes": 10, "collections": 5, "comments": 1},
    )


def _strong_snapshot() -> MetricsSnapshot:
    return MetricsSnapshot(
        snapshot_id="metric_strong",
        ref_id="pkg_002",
        metrics={"views": 1000, "likes": 60, "collected": 20, "comments": 5, "shares": 5, "inquiries": 3},
    )


def test_metric_summary_and_metrics_summary_normalize_aliases_and_rates():
    summary = strategy_iteration_policy.metric_summary(_strong_snapshot().metrics)
    aggregate = strategy_iteration_policy.metrics_summary([_weak_snapshot(), _strong_snapshot()])

    assert summary == {"views": 1000.0, "engagement": 90.0, "engagement_rate": 0.09, "inquiries": 3.0}
    assert aggregate == {"total": 2, "views": 2000, "engagement": 106, "engagement_rate": 0.053, "inquiries": 3}


def test_review_summary_counts_statuses_and_top_issue_codes():
    summary = strategy_iteration_policy.review_summary([_blocked_review(), _passed_review()])

    assert summary["total"] == 2
    assert summary["by_status"]["blocked"] == 1
    assert summary["by_status"]["passed"] == 1
    assert summary["high_issue_count"] == 1
    assert summary["top_issue_codes"] == ["unsupported_absolute_claim"]


def test_strategy_recommendations_cover_blocked_weak_and_strong_cases():
    blocked_review_summary = strategy_iteration_policy.review_summary([_blocked_review()])
    no_metrics_summary = strategy_iteration_policy.metrics_summary([])

    assert any("blocked" in item for item in strategy_iteration_policy.diagnosis(blocked_review_summary, no_metrics_summary))
    assert any("阻断级审核问题" in item for item in strategy_iteration_policy.decisions(blocked_review_summary, no_metrics_summary))
    assert any("high severity" in item for item in strategy_iteration_policy.next_actions(blocked_review_summary, no_metrics_summary))

    passed_review_summary = strategy_iteration_policy.review_summary([_passed_review()])
    weak_metrics_summary = strategy_iteration_policy.metrics_summary([_weak_snapshot()])
    strong_metrics_summary = strategy_iteration_policy.metrics_summary([_strong_snapshot()])

    assert any("互动率低于 3%" in item for item in strategy_iteration_policy.diagnosis(passed_review_summary, weak_metrics_summary))
    assert any("痛点标题" in item for item in strategy_iteration_policy.next_actions(passed_review_summary, weak_metrics_summary))
    assert any("8% 以上" in item for item in strategy_iteration_policy.diagnosis(passed_review_summary, strong_metrics_summary))
    assert any("高互动内容" in item for item in strategy_iteration_policy.next_actions(passed_review_summary, strong_metrics_summary))


def test_ref_identity_date_and_slug_helpers_are_stable():
    assert strategy_iteration_policy.ref_identity("cycle_001") == ("cycle_001", "manual_ref")
    assert strategy_iteration_policy.ref_identity({"task_id": "task_001"}) == ("task_001", "content_task")
    assert strategy_iteration_policy.date_text("2026-05-24") == "2026-05-24"
    assert strategy_iteration_policy.slug("pkg 001!") == "pkg_001"
