from __future__ import annotations

from nori.content_generation.content_producer.package import ContentPackageAssembler, PreparedContentPackageInput
from nori.content_generation.models import CandidateTitle, CoverResult, NoteDraft
from nori.core import AccountOperationProject, ClientBrief, ContentTask, StableArtifactAssembler, UserAsset


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


def test_content_package_assembler_prepares_agent_inputs_and_context() -> None:
    assembler = ContentPackageAssembler()
    project = AccountOperationProject(project_id="ops_001", name="春日花房代运营", client_brief=_brief())

    prepared = assembler.prepare(
        _task(),
        _brief(),
        assets=[{"kind": "image", "path": "/tmp/ref.jpg", "usable_for": ["cover"]}],
        project=project,
        intent_override={"goal": "自定义目标"},
        context_override={"extra": "value"},
    )

    assert isinstance(assembler, StableArtifactAssembler)
    assert isinstance(prepared, PreparedContentPackageInput)
    assert [asset.kind for asset in prepared.assets] == ["image", "text"]
    assert prepared.assets[0].path == "/tmp/ref.jpg"
    assert "任务标题：母亲节花束搭配" in prepared.assets[1].text
    assert "品牌：春日花房" in prepared.assets[1].text
    assert prepared.intent == {
        "goal": "自定义目标",
        "format": "小红书图文",
        "topic": "母亲节花束",
        "platform": "xhs",
        "content_type": "note",
    }
    assert prepared.context["task"]["task_id"] == "task_001"
    assert prepared.context["client_brief"]["brand_name"] == "春日花房"
    assert prepared.context["project"]["project_id"] == "ops_001"
    assert prepared.context["extra"] == "value"


def test_content_package_assembler_selects_skill_and_builds_package() -> None:
    assembler = ContentPackageAssembler()
    project = AccountOperationProject(project_id="ops_001", client_brief=_brief())
    assets = [UserAsset(kind="image", path="/tmp/ref.jpg", usable_for=["cover"])]

    selected = assembler.selected_skill([{"skill_id": "other"}, _skill()], "flower_skill")
    package = assembler.build(
        _task(),
        _draft(),
        _cover(),
        skills=[_skill()],
        assets=assets,
        brief=_brief(),
        project=project,
        status_before="planned",
        use_cover=True,
    )

    assert selected == _skill()
    assert package.package_id == "pkg_task_001"
    assert package.cover_path == "/tmp/generated-cover.png"
    assert package.image_paths == ["/tmp/body.jpg", "/tmp/ref.jpg"]
    assert package.prompts["note_draft"]["title"] == "母亲节花别乱买"
    assert package.prompts["cover_result"]["prompt"] == "cover prompt"
    assert {"source": "input_asset", "index": 0, "kind": "image", "path": "/tmp/ref.jpg", "text_preview": "", "usable_for": ["cover"]} in package.material_usage
    assert {"source": "task_required_asset", "kind": "product_photo"} in package.material_usage
    assert {"source": "benchmark_note", "note_id": "xhs_001"} in package.source_refs
    assert {"source": "note_skill", "skill_id": "flower_skill", "label": "花店种草"} in package.source_refs
    assert {"source": "client_brief", "client_name": "花店主理人", "brand_name": "春日花房"} in package.source_refs
    assert {"source": "account_operation_project", "project_id": "ops_001"} in package.source_refs
    assert package.metadata["production"]["task_status_before"] == "planned"
    assert package.metadata["production"]["cover_generated"] is True


def test_content_package_assembler_stable_ids_and_media_paths_are_deduped() -> None:
    assembler = ContentPackageAssembler()

    assert assembler.package_id_for_task(_task()) == "pkg_task_001"
    assert assembler.slug(" 母亲节 花束! ") == "母亲节_花束"
    assert assembler.dedupe(["/tmp/a.jpg", "", "/tmp/a.jpg", "/tmp/b.jpg"]) == ["/tmp/a.jpg", "/tmp/b.jpg"]
