"""Offline review gate for generated content packages."""
from __future__ import annotations

from nori.core import AccountOperationProject
from typing import Any

from nori.core import AgentBase, WorkflowBase
from nori.agents.content_generation.models import ContentPackage
from nori.core import ClientBrief, ContentTask, IntentContract

from .package import ReviewInputPreparer
from . import policy as _policy
from . import state as _state
from ..models import ComplianceReview


_INPUT_PREPARER = ReviewInputPreparer()


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
        pkg = _INPUT_PREPARER.normalize_package(package)
        normalized_task = _INPUT_PREPARER.normalize_task(task)
        brief = _INPUT_PREPARER.normalize_client_brief(client_brief, project)

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
        pkg = _INPUT_PREPARER.normalize_package(package)
        normalized_task = _INPUT_PREPARER.normalize_task(task)
        brief = _INPUT_PREPARER.normalize_client_brief(client_brief, project)

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


class QualityReviewerAgent(AgentBase):
    """Rule-based product-quality reviewer against the frozen intent contract."""

    stage_name = "quality_reviewer"
    reviewer = "quality"

    def __init__(self) -> None:
        super().__init__(stage_name=self.stage_name, use_llm=False)

    def run(
        self,
        package: ContentPackage | dict[str, Any],
        *,
        intent_contract: IntentContract | dict[str, Any] | None = None,
        task: ContentTask | dict[str, Any] | None = None,
        client_brief: ClientBrief | dict[str, Any] | None = None,
        project: AccountOperationProject | None = None,
    ) -> ComplianceReview:
        pkg = _INPUT_PREPARER.normalize_package(package)
        contract = intent_contract if isinstance(intent_contract, IntentContract) else IntentContract.from_dict(intent_contract)
        issues = _quality_issues(pkg, contract)
        review = _policy.build_review(
            package=pkg,
            task=_INPUT_PREPARER.normalize_task(task),
            reviewer=self.reviewer,
            issues=issues,
            metadata={
                "review_type": "rule_based_intent_quality",
                "checks": [
                    "intent_contract_present",
                    "must_include_terms",
                    "brand_presence",
                    "business_goal_alignment",
                ],
                "intent_contract": contract.to_dict() if contract.contract_id else {},
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
        quality_reviewer: QualityReviewerAgent | None = None,
    ) -> None:
        AgentBase.__init__(self, stage_name="review_gate", use_llm=False)
        self.compliance_reviewer = compliance_reviewer or ComplianceReviewerAgent()
        self.consistency_reviewer = consistency_reviewer or ConsistencyReviewerAgent()
        self.quality_reviewer = quality_reviewer or QualityReviewerAgent()
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
        intent_contract: IntentContract | dict[str, Any] | None = None,
        project: AccountOperationProject | None = None,
    ) -> list[ComplianceReview]:
        reviews = [
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
        if intent_contract:
            reviews.append(
                self.quality_reviewer.run(
                    package,
                    intent_contract=intent_contract,
                    task=task,
                    client_brief=client_brief,
                    project=project,
                )
            )
        return reviews


def review_content_package(
    package: ContentPackage | dict[str, Any],
    **kwargs: Any,
) -> list[ComplianceReview]:
    """Convenience wrapper for the default package review gate."""

    return ReviewGateAgent().run(package, **kwargs)


__all__ = [
    "ComplianceReviewerAgent",
    "ConsistencyReviewerAgent",
    "QualityReviewerAgent",
    "ReviewGateAgent",
    "review_content_package",
]


def _quality_issues(pkg: ContentPackage, contract: IntentContract) -> list[dict[str, Any]]:
    if not contract.contract_id and not contract.must_include:
        return [{
            "code": "missing_intent_contract",
            "severity": "medium",
            "message": "No IntentContract was provided, so product quality cannot be verified against user intent.",
        }]

    text = "\n".join([pkg.title, pkg.body, " ".join(pkg.tags)])
    issues: list[dict[str, Any]] = []
    missing = contract.missing_terms(text)
    if missing:
        issues.append({
            "code": "missing_must_include",
            "severity": "medium",
            "message": "Generated content misses required intent terms.",
            "terms": missing,
        })
    if contract.brand_name and contract.brand_name not in text:
        issues.append({
            "code": "brand_not_present",
            "severity": "medium",
            "message": f"Generated content does not mention brand '{contract.brand_name}'.",
            "terms": [contract.brand_name],
        })
    if any("卖" in goal or "产品" in goal for goal in contract.business_goals):
        if not any(term in text for term in ["产品", "杯", "包", "挂件", "贴纸", "冰箱贴", "手机支架"]):
            issues.append({
                "code": "product_goal_not_reflected",
                "severity": "medium",
                "message": "Business goal includes product conversion, but the content does not naturally surface products.",
            })
    return issues
