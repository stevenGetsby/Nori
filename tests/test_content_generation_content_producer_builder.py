from __future__ import annotations

from nori.core import AccountOperationProject
from nori.core import ContentTask, ClientBrief
from nori.content_generation.models import CandidateTitle, CoverResult, NoteDraft
from nori.core import UserAsset
from nori.content_generation.content_producer import builder as content_package_builder


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
        constraints=["不夸大疗效"],
        taboos=["不虚构价格"],
    )


def _draft() -> NoteDraft:
    return NoteDraft(
        skill_id="flower_skill",
        title="母亲节花别乱买",
        body="先看妈妈喜欢的颜色，再选花材。",
        tags=["花束", "母亲节"],
        comment_hook="你想送什么颜色？",
        cover_path="/tmp/ref.jpg",
        image_paths=["/tmp/body.jpg"],
        candidate_titles=[CandidateTitle(text="母亲节花别乱买")],
        asset_bundle={"text_points": ["母亲节花束搭配"]},
        validation={"status": "pass", "issues": []},
        llm_enhanced=True,
    )


def _cover() -> CoverResult:
    return CoverResult(
        cover_path="/tmp/generated-cover.png",
        prompt="cover prompt",
        size="1072x1440",
        reference_paths=["/tmp/ref.jpg"],
    )


def _skill() -> dict:
    return {"skill_id": "flower_skill", "label": "花店种草"}


def test_normalize_assets_adds_task_brief_text_when_missing():
    assets = content_package_builder.normalize_assets(
        [UserAsset(kind="image", path="/tmp/ref.jpg", usable_for=["cover"])],
        _task(),
        _brief(),
    )

    assert [asset.kind for asset in assets] == ["image", "text"]
    assert "任务标题：母亲节花束搭配" in assets[1].text
    assert "品牌：春日花房" in assets[1].text


def test_build_intent_context_and_selected_skill():
    project = AccountOperationProject(project_id="ops_001", name="春日花房代运营", client_brief=_brief())

    intent = content_package_builder.build_intent(_task(), _brief(), {"goal": "自定义目标"})
    context = content_package_builder.build_context(_task(), _brief(), project, {"extra": "value"})
    selected = content_package_builder.selected_skill([{"skill_id": "other"}, _skill()], "flower_skill")

    assert intent["goal"] == "自定义目标"
    assert intent["format"] == "小红书图文"
    assert context["project"]["project_id"] == "ops_001"
    assert context["extra"] == "value"
    assert selected == _skill()


def test_package_from_outputs_maps_prompts_material_usage_and_source_refs():
    task = _task()
    project = AccountOperationProject(project_id="ops_001", client_brief=_brief())
    assets = [UserAsset(kind="image", path="/tmp/ref.jpg", usable_for=["cover"])]

    package = content_package_builder.package_from_outputs(
        task,
        _draft(),
        _cover(),
        skills=[_skill()],
        assets=assets,
        brief=_brief(),
        project=project,
        status_before="planned",
        use_cover=True,
    )

    assert package.package_id == "pkg_task_001"
    assert package.cover_path == "/tmp/generated-cover.png"
    assert package.image_paths == ["/tmp/body.jpg", "/tmp/ref.jpg"]
    assert package.prompts["note_draft"]["title"] == "母亲节花别乱买"
    assert package.prompts["cover_result"]["prompt"] == "cover prompt"
    assert {"source": "task_required_asset", "kind": "product_photo"} in package.material_usage
    assert {"source": "note_skill", "skill_id": "flower_skill", "label": "花店种草"} in package.source_refs
    assert {"source": "account_operation_project", "project_id": "ops_001"} in package.source_refs
    assert package.metadata["production"]["task_status_before"] == "planned"
    assert package.metadata["production"]["cover_generated"] is True
