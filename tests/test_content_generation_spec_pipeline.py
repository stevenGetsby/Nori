from __future__ import annotations

from nori.agents.content_generation import ArtifactGenerationAgent, ContentSpecAgent
from nori.agents.content_generation.models import ContentDesignSpec, ContentPackage
from nori.agents.market_analysis.models import NoteSkill
from nori.core import ClientBrief, ContentTask, IntentContract, UserAsset


def _task(content_type: str = "note") -> ContentTask:
    return ContentTask(
        task_id="task_001",
        title="母亲节花束搭配",
        platform="xhs",
        content_type=content_type,
        topic="母亲节花束",
        objective="提升到店咨询",
        brief={"cover_title": "母亲节花别乱买"},
        references=[{"source": "benchmark_note", "note_id": "xhs_001"}],
    )


def _brief() -> ClientBrief:
    return ClientBrief(
        client_name="花店主理人",
        brand_name="春日花房",
        goals=["建立本地认知"],
        audience=["周边 3 公里年轻家庭"],
        constraints=["温暖但专业"],
        taboos=["不虚构价格"],
    )


def _skill(skill_id: str = "flower_skill") -> NoteSkill:
    return NoteSkill(
        skill_id=skill_id,
        label="节日花束种草",
        goal="planting",
        note_type="图文",
        tone="朋友安利",
        creative_goal="把花束放进节日送礼场景里自然种草。",
        title_rules=[{"name": "场景避坑", "rule": "标题先点出送礼场景和常见误区。"}],
        opening_rules=[{"name": "场景开场", "rule": "第一句先说用户正在面对的送礼难题。"}],
        body_structure=[{"name": "三段式", "rule": "场景 -> 选择理由 -> 到店动作。"}],
        visual_rules=[{"name": "主体突出", "rule": "花束主体占画面 60%-75%。"}],
        cover_rules=[{"name": "封面一句话", "rule": "封面文字 6-14 字。"}],
        avoid_rules=["不要虚构价格。"],
    )


class FakeContentProducer:
    def __init__(self):
        self.calls = []

    def run(self, task, **kwargs):
        self.calls.append({"task": task, "kwargs": kwargs})
        return ContentPackage(package_id="pkg_001", task_id=task.task_id, title="母亲节花别乱买", body="body")


def test_content_spec_agent_turns_task_skills_and_brief_into_a_design_spec():
    contract = IntentContract(
        contract_id="intent_task_001",
        brand_name="春日花房",
        must_include=["母亲节花束"],
        taboos=["不虚构价格"],
    )

    spec = ContentSpecAgent().run(
        task=_task(),
        skills=[_skill()],
        client_brief=_brief(),
        assets=[UserAsset(kind="image", path="/tmp/flower.jpg", usable_for=["cover"])],
        intent_contract=contract,
    )

    assert spec.spec_id == "spec_task_001"
    assert spec.platform == "xhs"
    assert spec.artifact_type == "note"
    assert spec.goal == "提升到店咨询"
    assert spec.selected_skill_refs == [{"skill_id": "flower_skill", "label": "节日花束种草"}]
    assert {"slot": "title", "purpose": "标题先点出送礼场景和常见误区。"} in spec.structure
    assert spec.media_plan["cover"]["required"] is True
    assert spec.copy_rules["opening_rules"] == [{"name": "场景开场", "rule": "第一句先说用户正在面对的送礼难题。"}]
    assert "必须包含：母亲节花束" in spec.acceptance_checks
    assert "避免：不虚构价格" in spec.acceptance_checks


def test_artifact_generation_agent_executes_from_spec_without_exposing_all_skills():
    producer = FakeContentProducer()
    spec = ContentDesignSpec(
        spec_id="spec_task_001",
        task_id="task_001",
        platform="xhs",
        artifact_type="note",
        selected_skill_refs=[{"skill_id": "flower_skill"}],
    )
    other_skill = _skill("other_skill")

    package = ArtifactGenerationAgent(content_producer=producer).run(
        spec=spec,
        task=_task(),
        skills=[other_skill, _skill()],
        assets=[UserAsset(kind="text", text="brief")],
        out_dir="/tmp/out",
    )

    assert package.package_id == "pkg_001"
    assert [skill.skill_id for skill in producer.calls[0]["kwargs"]["skills"]] == ["flower_skill"]
    assert producer.calls[0]["kwargs"]["intent"]["content_design_spec"]["spec_id"] == "spec_task_001"
    assert producer.calls[0]["kwargs"]["context"]["content_design_spec"]["selected_skill_refs"] == [{"skill_id": "flower_skill"}]


def test_spec_and_artifact_agents_are_the_explicit_generation_pipeline():
    producer = FakeContentProducer()
    spec = ContentSpecAgent().run(
        task=_task(),
        skills=[_skill()],
        assets=[UserAsset(kind="text", text="brief")],
        client_brief=_brief(),
    )

    result = ArtifactGenerationAgent(content_producer=producer).run(
        spec=spec,
        task=_task(),
        skills=[_skill()],
        assets=[UserAsset(kind="text", text="brief")],
        out_dir="/tmp/out",
    )

    assert result.package_id == "pkg_001"
    assert spec.spec_id == "spec_task_001"
    assert producer.calls[0]["kwargs"]["context"]["content_design_spec"]["spec_id"] == "spec_task_001"
