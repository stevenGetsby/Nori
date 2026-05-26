from __future__ import annotations

from nori.core import AccountOperationProject
from nori.core import ContentTask, ClientBrief
import pytest

from nori.content_generation.models import CandidateTitle, CoverResult, NoteDraft
from nori.core import UserAsset
from nori.content_generation import ContentProducerAgent, ContentProductionError, produce_content_package


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


def _skill() -> dict:
    return {
        "skill_id": "flower_skill",
        "label": "花店种草",
        "goal": "planting",
        "note_type": "图文",
        "tone": "亲和",
        "creative_goal": "把花束搭配讲得具体、可信。",
    }


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


class FakeNoteMaker:
    def __init__(self, draft=None, error: Exception | None = None) -> None:
        self.draft = draft or _draft()
        self.error = error
        self.calls = []

    def run(self, skills, assets, *, intent=None, context=None):
        self.calls.append({"skills": skills, "assets": assets, "intent": intent, "context": context})
        if self.error:
            raise self.error
        return self.draft


class FakeCoverDirector:
    def __init__(self, cover=None, error: Exception | None = None) -> None:
        self.cover = cover or CoverResult(
            cover_path="/tmp/generated-cover.png",
            prompt="cover prompt",
            size="1072x1440",
            reference_paths=["/tmp/ref.jpg"],
        )
        self.error = error
        self.calls = []

    def run(self, draft, skill, *, reference_assets=None, out_dir=None, intent=None, tagged_assets=None):
        self.calls.append({
            "draft": draft,
            "skill": skill,
            "reference_assets": reference_assets,
            "out_dir": out_dir,
            "intent": intent,
            "tagged_assets": tagged_assets,
        })
        if self.error:
            raise self.error
        return self.cover


def test_content_producer_builds_package_and_attaches_to_project(tmp_path):
    task = _task()
    project = AccountOperationProject(
        project_id="ops_001",
        name="春日花房代运营",
        client_brief=_brief(),
        content_tasks=[task],
    )
    note_maker = FakeNoteMaker()
    cover_director = FakeCoverDirector()

    package = ContentProducerAgent(
        note_maker=note_maker,
        cover_director=cover_director,
    ).run(
        task,
        skills=[_skill()],
        assets=[UserAsset(kind="image", path="/tmp/ref.jpg", usable_for=["cover"])],
        out_dir=tmp_path,
        project=project,
    )

    assert package.package_id == "pkg_task_001"
    assert package.task_id == "task_001"
    assert package.title == "母亲节花别乱买"
    assert package.cover_path == "/tmp/generated-cover.png"
    assert package.image_paths == ["/tmp/body.jpg", "/tmp/ref.jpg"]
    assert package.prompts["note_draft"]["title"] == "母亲节花别乱买"
    assert package.prompts["cover_result"]["prompt"] == "cover prompt"
    assert package.material_usage[0]["source"] == "input_asset"
    assert {"source": "task_required_asset", "kind": "product_photo"} in package.material_usage
    assert {"source": "note_skill", "skill_id": "flower_skill", "label": "花店种草"} in package.source_refs
    assert {"source": "account_operation_project", "project_id": "ops_001"} in package.source_refs
    assert task.package_id == package.package_id
    assert task.status == "drafted"
    assert project.content_packages == [package]
    assert project.metadata["last_produced_package_id"] == package.package_id
    assert note_maker.calls[0]["intent"]["topic"] == "母亲节花束"
    assert any(asset.kind == "text" for asset in note_maker.calls[0]["assets"])
    assert cover_director.calls[0]["skill"]["skill_id"] == "flower_skill"


def test_content_producer_can_skip_cover_generation(tmp_path):
    note_maker = FakeNoteMaker()
    cover_director = FakeCoverDirector()

    package = produce_content_package(
        _task().to_dict(),
        skills=[_skill()],
        assets=[{"kind": "text", "text": "用户补充卖点"}],
        out_dir=tmp_path,
        client_brief=_brief().to_dict(),
        note_maker=note_maker,
        cover_director=cover_director,
        use_cover=False,
    )

    assert package.cover_path == "/tmp/ref.jpg"
    assert package.prompts["cover_result"] is None
    assert package.metadata["production"]["cover_enabled"] is False
    assert cover_director.calls == []


def test_content_producer_failure_attaches_structured_error_to_task_and_project(tmp_path):
    task = _task()
    project = AccountOperationProject(project_id="ops_001", client_brief=_brief(), content_tasks=[task])
    agent = ContentProducerAgent(note_maker=FakeNoteMaker(error=RuntimeError("llm down")))

    with pytest.raises(ContentProductionError) as excinfo:
        agent.run(task, skills=[_skill()], assets=[], out_dir=tmp_path, project=project)

    assert task.status == "failed"
    assert task.metadata["production_error"]["task_id"] == "task_001"
    assert task.metadata["production_error"]["error_type"] == "RuntimeError"
    assert "llm down" in task.metadata["production_error"]["message"]
    assert project.metadata["production_errors"] == [task.metadata["production_error"]]
    assert project.content_packages == []
    assert excinfo.value.error == task.metadata["production_error"]
