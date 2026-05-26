"""Offline review gate for generated content packages."""
from __future__ import annotations

from nori.core import AccountOperationProject
from typing import Any

from nori.core import AgentBase, WorkflowBase
from nori.content_generation.models import ContentPackage
from nori.core import ClientBrief, ContentTask

from . import inputs as _inputs
from . import policy as _policy
from . import state as _state
from ..models import ComplianceReview


class ComplianceReviewerAgent(AgentBase):
    """Text-only compliance reviewer for generated packages."""

    stage_name = "compliance_reviewer"
    reviewer = "compliance"

    def __init__(self) -> None:
        super().__init__(stage_name=self.stage_name, use_llm=False)

    def run(
        self,
        package: ContentPackage | dict[str, Any],
        *,
        task: ContentTask | dict[str, Any] | None = None,
        client_brief: ClientBrief | dict[str, Any] | None = None,
        project: AccountOperationProject | None = None,
    ) -> ComplianceReview:
        pkg = _inputs.normalize_package(package)
        normalized_task = _inputs.normalize_task(task)
        brief = _inputs.normalize_client_brief(client_brief, project)

        review = _policy.build_review(
            package=pkg,
            task=normalized_task,
            reviewer=self.reviewer,
            issues=_policy.compliance_issues(pkg, brief),
            metadata={
                "review_type": "rule_based_text_compliance",
                "checks": [
                    "required_title_body",
                    "xhs_length",
                    "client_taboos",
                    "absolute_claims",
                    "note_maker_validation",
                ],
            },
        )
        _state.attach_review(project, review)
        return review


class ConsistencyReviewerAgent(AgentBase):
    """Rule-based alignment reviewer for task, package, and cover prompt."""

    stage_name = "consistency_reviewer"
    reviewer = "consistency"

    def __init__(self) -> None:
        super().__init__(stage_name=self.stage_name, use_llm=False)

    def run(
        self,
        package: ContentPackage | dict[str, Any],
        *,
        task: ContentTask | dict[str, Any] | None = None,
        client_brief: ClientBrief | dict[str, Any] | None = None,
        project: AccountOperationProject | None = None,
    ) -> ComplianceReview:
        pkg = _inputs.normalize_package(package)
        normalized_task = _inputs.normalize_task(task)
        brief = _inputs.normalize_client_brief(client_brief, project)

        review = _policy.build_review(
            package=pkg,
            task=normalized_task,
            reviewer=self.reviewer,
            issues=_policy.consistency_issues(pkg, normalized_task, brief),
            metadata={
                "review_type": "rule_based_package_consistency",
                "checks": [
                    "task_identity",
                    "topic_objective",
                    "cover_prompt",
                    "required_assets",
                    "brand_presence",
                ],
            },
        )
        _state.attach_review(project, review)
        return review


class ReviewGateAgent(AgentBase, WorkflowBase):
    """Run the default package review gate."""

    def __init__(
        self,
        *,
        compliance_reviewer: ComplianceReviewerAgent | None = None,
        consistency_reviewer: ConsistencyReviewerAgent | None = None,
    ) -> None:
        AgentBase.__init__(self, stage_name="review_gate", use_llm=False)
        self.compliance_reviewer = compliance_reviewer or ComplianceReviewerAgent()
        self.consistency_reviewer = consistency_reviewer or ConsistencyReviewerAgent()
        WorkflowBase.__init__(
            self,
            workflow_name="review_gate",
            steps=[
                ("compliance", self.compliance_reviewer.run),
                ("consistency", self.consistency_reviewer.run),
            ],
        )

    def run(
        self,
        package: ContentPackage | dict[str, Any],
        *,
        task: ContentTask | dict[str, Any] | None = None,
        client_brief: ClientBrief | dict[str, Any] | None = None,
        project: AccountOperationProject | None = None,
    ) -> list[ComplianceReview]:
        return [
            self.compliance_reviewer.run(
                package,
                task=task,
                client_brief=client_brief,
                project=project,
            ),
            self.consistency_reviewer.run(
                package,
                task=task,
                client_brief=client_brief,
                project=project,
            ),
        ]


def review_content_package(
    package: ContentPackage | dict[str, Any],
    **kwargs: Any,
) -> list[ComplianceReview]:
    """Convenience wrapper for the default package review gate."""

    return ReviewGateAgent().run(package, **kwargs)


__all__ = [
    "ComplianceReviewerAgent",
    "ConsistencyReviewerAgent",
    "ReviewGateAgent",
    "review_content_package",
]
