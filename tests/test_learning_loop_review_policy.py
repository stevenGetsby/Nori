from __future__ import annotations

from nori.core import ContentTask, ClientBrief
from nori.agents.learning_loop.review import policy as content_review_policy
from nori.agents.content_generation.schemas import ContentPackage


def _task() -> ContentTask:
    return ContentTask(
        task_id="task_001",
        title="母亲节花束搭配",
        platform="xhs",
        topic="母亲节花束",
        objective="提升到店咨询",
        brief={"cover_title": "母亲节花别乱买"},
        required_assets=["product_photo"],
    )


def _brief() -> ClientBrief:
    return ClientBrief(brand_name="春日花房", taboos=["虚假折扣"])


def _package() -> ContentPackage:
    return ContentPackage(
        package_id="pkg_task_001",
        task_id="task_001",
        platform="xhs",
        title="母亲节花别乱买｜春日花房",
        body="春日花房这次按母亲节花束场景做搭配，帮你提升到店咨询前的选择效率。",
        prompts={
            "note_draft": {"validation": {"status": "pass", "issues": []}},
            "cover_result": {"prompt": "cover title 母亲节花别乱买 春日花房"},
        },
        material_usage=[{"source": "task_required_asset", "kind": "product_photo"}],
    )


def test_compliance_policy_flags_required_fields_taboo_claims_and_validation():
    package = _package()
    package.title = ""
    package.body = "虚假折扣保证立刻见效。"
    package.prompts["note_draft"]["validation"] = {
        "status": "needs_human_review",
        "issues": ["命中禁止项"],
    }

    issues = content_review_policy.compliance_issues(package, _brief())

    codes = {issue["code"] for issue in issues}
    assert "missing_title" in codes
    assert "client_taboo_term" in codes
    assert "unsupported_absolute_claim" in codes
    assert "note_maker_needs_human_review" in codes


def test_consistency_policy_flags_alignment_and_asset_gaps():
    package = _package()
    package.title = "今日灵感"
    package.body = "春日花房分享轻松选花思路。"
    package.prompts["cover_result"]["prompt"] = "minimal flower cover"
    package.material_usage = [{"source": "input_asset", "kind": "text"}]

    issues = content_review_policy.consistency_issues(package, _task(), _brief())

    codes = {issue["code"] for issue in issues}
    assert "topic_not_reflected" in codes
    assert "objective_not_reflected" in codes
    assert "cover_prompt_not_aligned" in codes
    assert "required_asset_not_tracked" in codes


def test_build_review_scores_status_and_suggestions():
    issues = [
        content_review_policy.issue("client_taboo_term", "high", "body", "bad"),
        content_review_policy.issue("cover_prompt_not_aligned", "medium", "prompt", "bad"),
    ]

    review = content_review_policy.build_review(
        package=_package(),
        task=_task(),
        reviewer="compliance",
        issues=issues,
        metadata={"review_type": "unit"},
    )

    assert review.review_id == "review_compliance_pkg_task_001"
    assert review.status == "blocked"
    assert review.score == 45
    assert review.metadata["issue_count"] == 2
    assert review.metadata["severity_counts"] == {"high": 1, "medium": 1, "low": 0}
    assert any("禁用" in suggestion for suggestion in review.fix_suggestions)
