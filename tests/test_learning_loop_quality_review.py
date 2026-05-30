from __future__ import annotations

from nori.agents.content_generation.models import ContentPackage
from nori.core import IntentContract
from nori.agents.learning_loop.review import QualityReviewerAgent


def test_quality_reviewer_passes_when_package_satisfies_intent_contract():
    contract = IntentContract(
        contract_id="intent_task_1",
        brand_name="Holly Shit开心拉屎",
        primary_goal="让用户理解反焦虑并自然种草产品",
        must_include=["杯子", "贴纸"],
        business_goals=["涨粉", "卖文创产品"],
        tone=["搞怪"],
    )
    package = ContentPackage(
        package_id="pkg_1",
        task_id="task_1",
        title="别再为休息羞耻了",
        body="Holly Shit开心拉屎把杯子和贴纸做成厕所快乐哲学的小提醒。",
        tags=["反焦虑", "文创品牌"],
    )

    review = QualityReviewerAgent().run(package, intent_contract=contract)

    assert review.status == "passed"
    assert review.reviewer == "quality"
    assert review.score == 100
    assert review.issues == []


def test_quality_reviewer_flags_missing_intent_requirements():
    contract = IntentContract(
        contract_id="intent_task_1",
        brand_name="Holly Shit开心拉屎",
        primary_goal="卖产品",
        must_include=["杯子", "贴纸"],
        business_goals=["卖文创产品"],
    )
    package = ContentPackage(
        package_id="pkg_1",
        task_id="task_1",
        title="别再为休息羞耻了",
        body="这篇只讲反焦虑理念，没有带出产品。",
        tags=["反焦虑"],
    )

    review = QualityReviewerAgent().run(package, intent_contract=contract)

    assert review.status == "needs_revision"
    assert review.reviewer == "quality"
    assert review.score < 100
    assert {issue["code"] for issue in review.issues} == {"missing_must_include", "brand_not_present"}
    missing_issue = next(issue for issue in review.issues if issue["code"] == "missing_must_include")
    assert missing_issue["terms"] == ["杯子", "贴纸"]
