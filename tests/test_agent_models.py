from pathlib import Path

from nori.agent_models import AccountPlannerInput, IntakeResult, UserInput, XHSNoteSample, XHSSeedSkillDraft
from nori.agent_models.account_planner import AccountPlannerInput as DirectAccountPlannerInput
from nori.agent_models.intake import UserInput as DirectUserInput
from nori.agent_models.xhs_note import XHSNoteSample as DirectXHSNoteSample
from nori.agent_models.xhs_note import XHSSeedSkillDraft as DirectXHSSeedSkillDraft
from nori.gen_agents import AccountPlannerInput as ExportedAccountPlannerInput
from nori.gen_agents import UserInput as ExportedUserInput


def test_user_input_model_serializes():
    user_input = UserInput(text="做一篇小红书", images=["a.png"])

    assert user_input.to_dict() == {"text": "做一篇小红书", "images": ["a.png"]}


def test_account_planner_input_from_intaker_model():
    intaker_result = IntakeResult(
        intention={"goal": "涨粉"},
        context={"images": [{"path": "a.png", "kind": "png"}]},
        missing=[],
        questions=[],
    )

    planner_input = AccountPlannerInput.from_intaker(intaker_result, text="品牌理念", platform="xhs")

    assert planner_input.intention == {"goal": "涨粉"}
    assert planner_input.context["images"][0]["path"] == "a.png"
    assert planner_input.images == ["a.png"]
    assert planner_input.to_dict()["platform"] == "xhs"


def test_gen_agents_reexport_shared_models():
    assert ExportedUserInput is UserInput
    assert ExportedAccountPlannerInput is AccountPlannerInput


def test_models_are_defined_in_dedicated_modules():
    assert UserInput is DirectUserInput
    assert AccountPlannerInput is DirectAccountPlannerInput
    assert XHSNoteSample is DirectXHSNoteSample
    assert XHSSeedSkillDraft is DirectXHSSeedSkillDraft
    assert UserInput.__module__ == "nori.agent_models.intake"
    assert AccountPlannerInput.__module__ == "nori.agent_models.account_planner"
    assert XHSNoteSample.__module__ == "nori.agent_models.xhs_note"
    assert XHSSeedSkillDraft.__module__ == "nori.agent_models.xhs_note"


def test_xhs_note_models_serialize():
    note = XHSNoteSample(
        meta_path=Path("cold_start_data/xhs/设计/a/posts/b/meta.json"),
        category="设计",
        author_id="a",
        author_name="设计作者",
        note_id="b",
        title="设计案例｜测试",
        desc="项目说明",
        tags=["#设计"],
        metrics={"liked": 1},
        image_count=3,
        note_type="图文",
        note_url="https://example.com",
    )
    draft = XHSSeedSkillDraft(
        skill_id="seed.xhs.test",
        category="设计",
        match={"scene": "设计案例解析型 note"},
        craft={"title_rules": []},
        evidence={"source_note": note.to_dict()},
        validation={"result": "draft_only"},
    )

    assert note.to_dict()["meta_path"] == "cold_start_data/xhs/设计/a/posts/b/meta.json"
    assert draft.to_dict()["id"] == "seed.xhs.test"
    assert draft.to_dict()["evidence"]["source_note"]["note_id"] == "b"
