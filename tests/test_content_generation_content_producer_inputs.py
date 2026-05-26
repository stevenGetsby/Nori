"""Tests for ContentProducer input and context helpers."""

from __future__ import annotations

from nori.core import AccountOperationProject
from nori.core import ContentTask, ClientBrief

from nori.content_generation.models import UserAsset
from nori.content_generation.content_producer import inputs as content_package_inputs


def _task() -> ContentTask:
    return ContentTask(
        task_id="task_001",
        title="母亲节花束搭配",
        platform="xhs",
        content_type="note",
        topic="母亲节花束",
        objective="提升咨询",
        brief={"cover_title": "母亲节花别乱买"},
    )


def _brief() -> ClientBrief:
    return ClientBrief(
        brand_name="春日花房",
        goals=["建立本地认知"],
        audience=["周边家庭"],
        constraints=["不夸大疗效"],
        taboos=["不虚构价格"],
    )


def test_normalize_assets_restores_dicts_and_adds_task_brief_text_fallback():
    assets = content_package_inputs.normalize_assets(
        [{"kind": "image", "path": "/tmp/ref.jpg", "usable_for": ["cover"]}],
        _task(),
        _brief(),
    )

    assert [asset.kind for asset in assets] == ["image", "text"]
    assert assets[0].path == "/tmp/ref.jpg"
    assert "任务标题：母亲节花束搭配" in assets[1].text
    assert "品牌：春日花房" in assets[1].text


def test_build_intent_and_context_apply_overrides_after_defaults():
    project = AccountOperationProject(project_id="ops_001", name="春日花房代运营", client_brief=_brief())

    intent = content_package_inputs.build_intent(_task(), _brief(), {"goal": "自定义目标"})
    context = content_package_inputs.build_context(_task(), _brief(), project, {"extra": "value"})

    assert intent == {
        "goal": "自定义目标",
        "format": "小红书图文",
        "topic": "母亲节花束",
        "platform": "xhs",
        "content_type": "note",
    }
    assert context["task"]["task_id"] == "task_001"
    assert context["client_brief"]["brand_name"] == "春日花房"
    assert context["project"]["project_id"] == "ops_001"
    assert context["extra"] == "value"


def test_selected_skill_prefers_matching_skill_id_and_falls_back_to_first():
    first = {"skill_id": "default", "label": "默认"}
    match = {"skill_id": "flower_skill", "label": "花店种草"}

    assert content_package_inputs.selected_skill([first, match], "flower_skill") == match
    assert content_package_inputs.selected_skill([first, match], "missing") == first
