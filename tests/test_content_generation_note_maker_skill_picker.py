import pytest

from nori.content_generation.note_maker import skill_picker


class SkillPickerTestError(RuntimeError):
    pass


def _skills() -> list[dict]:
    return [
        {
            "skill_id": "debrief",
            "label": "经验复盘",
            "goal": "debrief",
            "tone": "个人经验",
            "note_type": "图文",
            "creative_goal": "用真实经历换一份清单。",
            "metrics_summary": {"sample": 3},
            "title_rules": [{"name": "large field should not enter summary"}],
        },
        {
            "skill_id": "planting",
            "label": "种草推荐",
            "goal": "planting",
            "tone": "朋友安利",
            "note_type": "图文",
            "creative_goal": "像朋友推荐一样讲清楚。",
            "metrics_summary": {"sample": 4},
        },
    ]


def test_skill_picker_uses_compact_summary_and_json_call():
    calls: list[dict] = []

    def fake_json_call(*, system: str, user: str, timeout: int):
        calls.append({"system": system, "user": user, "timeout": timeout})
        return {"skill_id": "planting"}

    selected = skill_picker.pick_skill_llm(
        _skills(),
        {"goal": "产品种草"},
        {"platform": "xhs"},
        json_call=fake_json_call,
        error_type=SkillPickerTestError,
    )

    assert selected["skill_id"] == "planting"
    assert calls[0]["timeout"] == 30
    assert "候选 skill" in calls[0]["user"]
    assert "产品种草" in calls[0]["user"]
    assert "planting" in calls[0]["user"]
    assert "large field should not enter summary" not in calls[0]["user"]


def test_skill_picker_raises_domain_error_for_unknown_skill_id():
    def fake_json_call(*, system: str, user: str, timeout: int):
        return {"skill_id": "missing"}

    with pytest.raises(SkillPickerTestError, match="未知 skill_id"):
        skill_picker.pick_skill_llm(
            _skills(),
            {},
            {},
            json_call=fake_json_call,
            error_type=SkillPickerTestError,
        )
