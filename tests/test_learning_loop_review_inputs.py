"""Tests for content review input normalization helpers."""

from __future__ import annotations

from nori.core import AccountOperationProject
from nori.core import ContentTask, ClientBrief

from nori.agents.learning_loop.review.package import ReviewInputPreparer
from nori.agents.content_generation.schemas import ContentPackage


content_review_inputs = ReviewInputPreparer()


def test_normalize_package_restores_dicts_and_preserves_instances():
    package = ContentPackage(package_id="pkg_001", task_id="task_001", title="标题")

    assert content_review_inputs.normalize_package(package) is package
    assert content_review_inputs.normalize_package(package.to_dict()).package_id == "pkg_001"


def test_normalize_task_restores_optional_dicts():
    task = ContentTask(task_id="task_001", title="任务")

    assert content_review_inputs.normalize_task(task) is task
    assert content_review_inputs.normalize_task(task.to_dict()).task_id == "task_001"
    assert content_review_inputs.normalize_task(None) is None


def test_normalize_client_brief_prefers_explicit_value_then_project_brief():
    project = AccountOperationProject(client_brief=ClientBrief(brand_name="春日花房"))
    explicit = ClientBrief(brand_name="夏日花房")

    assert content_review_inputs.normalize_client_brief(explicit, project) is explicit
    assert content_review_inputs.normalize_client_brief({"brand_name": "秋日花房"}, project).brand_name == "秋日花房"
    assert content_review_inputs.normalize_client_brief(None, project).brand_name == "春日花房"
    assert content_review_inputs.normalize_client_brief(None, None).brand_name == ""
