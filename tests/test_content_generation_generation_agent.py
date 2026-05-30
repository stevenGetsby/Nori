from __future__ import annotations

from nori.agents.content_generation import GenerationAgent
from nori.agents.content_generation.models import ContentPackage, CoverResult, NoteDraft
from nori.core import ContentTask, IntentContract, UserAsset
from nori.agents.market_analysis.models import NoteSkill


class FakeContentProducer:
    def __init__(self):
        self.calls = []

    def run(self, task, **kwargs):
        self.calls.append({"task": task, "kwargs": kwargs})
        return ContentPackage(package_id="pkg_1", task_id=task.task_id, title="note", body="body")


class FakeNoteMaker:
    def __init__(self):
        self.calls = []

    def run(self, skills, assets, **kwargs):
        self.calls.append({"skills": skills, "assets": assets, "kwargs": kwargs})
        return NoteDraft(skill_id="skill_1", title="title", body="body")


class FakeCoverDirector:
    def __init__(self):
        self.calls = []

    def run(self, draft, skill, **kwargs):
        self.calls.append({"draft": draft, "skill": skill, "kwargs": kwargs})
        return CoverResult(cover_path="/tmp/cover.png", prompt="prompt")


def _skill() -> NoteSkill:
    return NoteSkill(
        skill_id="skill_1",
        label="种草",
        goal="planting",
        note_type="图文",
        tone="朋友安利",
        creative_goal="自然种草",
    )


def test_generation_agent_routes_note_package_to_content_producer():
    producer = FakeContentProducer()
    agent = GenerationAgent(content_producer=producer)
    task = ContentTask(task_id="task_1", content_type="note")
    contract = IntentContract(contract_id="intent_task_1", brand_name="Holly")

    result = agent.run(
        "note_package",
        task=task,
        skills=[_skill()],
        assets=[UserAsset(kind="text", text="brief")],
        out_dir="/tmp/out",
        intent_contract=contract,
    )

    assert isinstance(result, ContentPackage)
    assert producer.calls[0]["kwargs"]["intent_contract"] is contract


def test_generation_agent_keeps_specialized_text_and_image_routes():
    note_maker = FakeNoteMaker()
    cover_director = FakeCoverDirector()
    agent = GenerationAgent(note_maker=note_maker, cover_director=cover_director)
    skill = _skill()
    asset = UserAsset(kind="text", text="brief")

    draft = agent.run("text", skills=[skill], assets=[asset], intent={"goal": "涨粉"})
    cover = agent.run("image", draft=draft, skill=skill, out_dir="/tmp/out")

    assert isinstance(draft, NoteDraft)
    assert isinstance(cover, CoverResult)
    assert note_maker.calls[0]["kwargs"]["intent"] == {"goal": "涨粉"}
    assert cover_director.calls[0]["draft"] is draft
