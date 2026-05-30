"""Tests for content review state helpers."""

from __future__ import annotations

from nori.core import AccountOperationProject
from nori.agents.learning_loop.review import state as content_review_state
from nori.agents.learning_loop.models import ComplianceReview


def test_attach_review_appends_to_project_when_present():
    project = AccountOperationProject(project_id="ops_001")
    review = ComplianceReview(review_id="rev_001", package_id="pkg_001")

    content_review_state.attach_review(project, review)

    assert project.compliance_reviews == [review]


def test_attach_review_ignores_missing_project():
    review = ComplianceReview(review_id="rev_001", package_id="pkg_001")

    assert content_review_state.attach_review(None, review) is None


def test_attach_review_preserves_existing_reviews_and_appends():
    first = ComplianceReview(review_id="rev_001", package_id="pkg_001")
    second = ComplianceReview(review_id="rev_002", package_id="pkg_002")
    project = AccountOperationProject(project_id="ops_001", compliance_reviews=[first])

    content_review_state.attach_review(project, second)

    assert project.compliance_reviews == [first, second]
