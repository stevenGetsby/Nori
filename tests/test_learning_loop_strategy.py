from __future__ import annotations

from nori.core import AccountOperationProject
from nori.core import ContentTask, ClientBrief
from nori.agents.learning_loop import (
    MetricsSnapshotAgent,
    StrategyIterationAgent,
    create_strategy_iteration,
    record_metrics_snapshot,
)
from nori.agents.content_generation.models import ContentPackage
from nori.agents.learning_loop.models import ComplianceReview


def _package() -> ContentPackage:
    return ContentPackage(
        package_id="pkg_001",
        task_id="task_001",
        title="母亲节花别乱买",
        body="正文",
    )


def _task() -> ContentTask:
    return ContentTask(task_id="task_001", package_id="pkg_001", title="母亲节任务")


def _passed_review() -> ComplianceReview:
    return ComplianceReview(
        review_id="review_passed",
        package_id="pkg_001",
        task_id="task_001",
        status="passed",
        score=95,
        reviewer="compliance",
    )


def _blocked_review() -> ComplianceReview:
    return ComplianceReview(
        review_id="review_blocked",
        package_id="pkg_001",
        task_id="task_001",
        status="blocked",
        score=40,
        reviewer="compliance",
        issues=[
            {
                "code": "unsupported_absolute_claim",
                "severity": "high",
                "field": "body",
                "message": "高风险承诺",
            }
        ],
    )


def _needs_revision_review() -> ComplianceReview:
    return ComplianceReview(
        review_id="review_revision",
        package_id="pkg_001",
        task_id="task_001",
        status="needs_revision",
        score=75,
        reviewer="consistency",
        issues=[
            {
                "code": "cover_prompt_not_aligned",
                "severity": "medium",
                "field": "prompt",
                "message": "封面不一致",
            }
        ],
    )


def test_metrics_snapshot_agent_records_package_metrics_and_attaches_to_project():
    project = AccountOperationProject(project_id="ops_001", client_brief=ClientBrief(brand_name="春日花房"))

    snapshot = MetricsSnapshotAgent().run(
        _package(),
        {"views": 1000, "likes": 50, "collections": 20, "comments": 10, "shares": 5, "inquiries": 2},
        captured_at="2026-05-24",
        project=project,
        notes=["上线 24 小时"],
    )

    assert snapshot.snapshot_id == "metric_pkg_001_20260524"
    assert snapshot.ref_id == "pkg_001"
    assert snapshot.source == "manual"
    assert snapshot.metadata["ref_type"] == "content_package"
    assert snapshot.metadata["summary"]["engagement"] == 85
    assert snapshot.metadata["summary"]["engagement_rate"] == 0.085
    assert project.metrics_snapshots == [snapshot]


def test_record_metrics_snapshot_accepts_task_dict_and_string_refs():
    task_snapshot = record_metrics_snapshot(
        _task().to_dict(),
        {"views": "100", "likes": "3"},
        captured_at="2026-05-24",
    )
    manual_snapshot = record_metrics_snapshot(
        "cycle_001",
        {"views": 0, "likes": 0},
        captured_at="2026-05-24",
    )

    assert task_snapshot.ref_id == "pkg_001"
    assert task_snapshot.metadata["ref_type"] == "content_package"
    assert manual_snapshot.ref_id == "cycle_001"
    assert manual_snapshot.metadata["ref_type"] == "manual_ref"


def test_strategy_iteration_blocks_on_high_review_without_metrics():
    iteration = StrategyIterationAgent().run(
        project_id="ops_001",
        reviews=[_blocked_review(), _needs_revision_review()],
        metrics_snapshots=[],
    )

    assert iteration.project_id == "ops_001"
    assert "review_blocked" in iteration.input_refs
    assert any("blocked" in item for item in iteration.diagnosis)
    assert any("阻断级审核问题" in item for item in iteration.decisions)
    assert any("high severity" in item for item in iteration.next_actions)
    assert any("manual MetricsSnapshot" in item for item in iteration.next_actions)
    assert iteration.metadata["review_summary"]["high_issue_count"] == 1


def test_strategy_iteration_detects_weak_engagement_and_attaches_to_project():
    project = AccountOperationProject(project_id="ops_001")
    project.compliance_reviews.append(_passed_review())
    snapshot = record_metrics_snapshot(
        _package(),
        {"views": 1000, "likes": 10, "collections": 5, "comments": 1},
        captured_at="2026-05-24",
        project=project,
    )

    iteration = create_strategy_iteration(project=project)

    assert iteration in project.strategy_iterations
    assert snapshot.snapshot_id in iteration.input_refs
    assert iteration.metadata["metrics_summary"]["engagement_rate"] == 0.016
    assert any("互动率低于 3%" in item for item in iteration.diagnosis)
    assert any("痛点标题" in item for item in iteration.next_actions)


def test_strategy_iteration_detects_strong_engagement_and_inquiries_from_dict_inputs():
    review = _passed_review().to_dict()
    snapshot = record_metrics_snapshot(
        "pkg_001",
        {"views": 1000, "likes": 60, "collected": 20, "comments": 5, "shares": 5, "inquiries": 3},
        captured_at="2026-05-24",
    ).to_dict()

    iteration = StrategyIterationAgent().run(
        project_id="ops_001",
        reviews=[review],
        metrics_snapshots=[snapshot],
    )

    assert iteration.metadata["metrics_summary"]["engagement_rate"] == 0.09
    assert iteration.metadata["metrics_summary"]["inquiries"] == 3
    assert any("8% 以上" in item for item in iteration.diagnosis)
    assert any("转化角度" in item for item in iteration.diagnosis)
    assert any("高互动内容" in item for item in iteration.next_actions)

