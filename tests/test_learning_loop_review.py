from __future__ import annotations

from nori.core import AccountOperationProject
from nori.core import ContentTask, ClientBrief
from nori.learning_loop import (
    ComplianceReviewerAgent,
    ConsistencyReviewerAgent,
    ReviewGateAgent,
    review_content_package,
)
from nori.content_generation.models import ContentPackage


def _task() -> ContentTask:
    return ContentTask(
        task_id="task_001",
        title="母亲节花束搭配",
        platform="xhs",
        content_type="note",
        topic="母亲节花束",
        objective="提升到店咨询",
        brief={"cover_title": "母亲节花别乱买", "content_pillar": "节日节点"},
        required_assets=["product_photo"],
        references=[{"source": "benchmark_note", "note_id": "xhs_001"}],
    )


def _brief() -> ClientBrief:
    return ClientBrief(
        client_name="花店主理人",
        brand_name="春日花房",
        goals=["建立本地认知"],
        audience=["周边 3 公里年轻家庭"],
        taboos=["虚假折扣"],
    )


def _package() -> ContentPackage:
    return ContentPackage(
        package_id="pkg_task_001",
        task_id="task_001",
        platform="xhs",
        title="母亲节花别乱买｜春日花房",
        body="春日花房这次按母亲节花束场景做搭配，帮你提升到店咨询前的选择效率。",
        tags=["花束", "母亲节"],
        cover_path="/tmp/cover.png",
        prompts={
            "note_draft": {"validation": {"status": "pass", "issues": []}},
            "cover_result": {"prompt": "3:4 cover with Chinese title 母亲节花别乱买 and 春日花房 bouquet"},
        },
        material_usage=[
            {"source": "input_asset", "kind": "image", "path": "/tmp/product.jpg", "usable_for": ["cover"]},
            {"source": "task_required_asset", "kind": "product_photo"},
        ],
        source_refs=[{"source": "benchmark_note", "note_id": "xhs_001"}],
    )


def test_compliance_reviewer_passes_clean_text_package():
    review = ComplianceReviewerAgent().run(_package(), task=_task(), client_brief=_brief())

    assert review.reviewer == "compliance"
    assert review.status == "passed"
    assert review.score == 100
    assert review.issues == []
    assert review.package_id == "pkg_task_001"
    assert review.task_id == "task_001"


def test_compliance_reviewer_blocks_taboo_and_absolute_claims():
    package = _package()
    package.body = "虚假折扣保证立刻见效，100% 到店。"
    package.prompts["note_draft"]["validation"] = {
        "status": "needs_human_review",
        "issues": ["命中禁止项"],
    }

    review = ComplianceReviewerAgent().run(package, task=_task(), client_brief=_brief())

    codes = {issue["code"] for issue in review.issues}
    assert review.status == "blocked"
    assert review.score < 60
    assert "client_taboo_term" in codes
    assert "unsupported_absolute_claim" in codes
    assert "note_maker_needs_human_review" in codes
    assert any("绝对化" in suggestion for suggestion in review.fix_suggestions)


def test_consistency_reviewer_flags_alignment_gaps_without_blocking():
    package = _package()
    package.title = "今日灵感"
    package.body = "春日花房分享一个轻松选花思路，用来提升到店咨询前的选择效率。"
    package.prompts["cover_result"]["prompt"] = "minimal flower cover without title text"
    package.material_usage = [{"source": "input_asset", "kind": "text", "text_preview": "brief"}]

    review = ConsistencyReviewerAgent().run(package, task=_task(), client_brief=_brief())

    codes = {issue["code"] for issue in review.issues}
    assert review.reviewer == "consistency"
    assert review.status == "needs_revision"
    assert "topic_not_reflected" in codes
    assert "cover_prompt_not_aligned" in codes
    assert "required_asset_not_tracked" in codes
    assert all(issue["severity"] != "high" for issue in review.issues)


def test_review_gate_appends_both_reviews_to_project_and_accepts_dict_package():
    project = AccountOperationProject(
        project_id="ops_001",
        client_brief=_brief(),
    )

    reviews = review_content_package(
        _package().to_dict(),
        task=_task().to_dict(),
        project=project,
    )

    assert len(reviews) == 2
    assert [review.reviewer for review in reviews] == ["compliance", "consistency"]
    assert project.compliance_reviews == reviews
    assert all(review.status == "passed" for review in reviews)
    assert isinstance(ReviewGateAgent().run(_package(), task=_task(), client_brief=_brief()), list)

