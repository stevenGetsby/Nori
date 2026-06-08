"""State mutation helpers for content review workflows."""
from __future__ import annotations


from nori.core import AccountOperationProject
from ..schemas import ComplianceReview


def attach_review(project: AccountOperationProject | None, review: ComplianceReview) -> None:
    """Attach a review to a project when project context is available."""

    if project is not None:
        project.compliance_reviews.append(review)


__all__ = ["attach_review"]
