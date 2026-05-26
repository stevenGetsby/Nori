import pytest

from nori.content_generation.models import AssetBundle, CandidateTitle
from nori.content_generation.note_maker import note_composer


class NoteComposerTestError(RuntimeError):
    pass


def _skill() -> dict:
    return {
        "creative_goal": "像朋友推荐一样讲清楚。",
        "tone": "朋友安利",
        "note_type": "图文",
        "title_rules": [{"name": "观点标题", "rule": "用一句观点承题。"}],
        "opening_rules": [{"name": "首句定场", "rule": "先给场景。"}],
        "body_structure": [{"name": "模块分段", "rule": "用小标题承载。"}],
        "interaction_rules": [{"name": "评论触发", "rule": "正文留问题。"}],
        "avoid_rules": ["不要硬广"],
    }


def test_note_composer_prompts_json_call_and_normalizes_output():
    bundle = AssetBundle(
        text_points=["通勤香薰很治愈"],
        brand_facts=["小众设计师品牌"],
        data_points=["复购率 60%"],
    )
    calls: list[dict] = []

    def fake_json_call(*, system: str, user: str, timeout: int):
        calls.append({"system": system, "user": user, "timeout": timeout})
        return {
            "title": " 通勤香薰｜复购的小确幸 ",
            "candidate_titles": [
                {"text": "通勤香薰｜复购的小确幸", "rule_name": "观点标题", "rationale": "贴合语气"},
                {"text": "x" * 80, "rule_name": "长标题", "rationale": "会被截断"},
            ],
            "body": " 下班路上被它治愈。 ",
            "tags": [" 香薰 ", "", "通勤好物", "朋友安利", "治愈", "多余"],
            "comment_hook": " 评论区告诉我你的心头好 ",
            "validation": {"status": "needs_human_review", "issues": [" 命中禁止项 "]},
        }

    composed = note_composer.compose_note_llm(
        _skill(),
        bundle,
        {"goal": "产品种草"},
        json_call=fake_json_call,
        error_type=NoteComposerTestError,
    )

    assert composed["title"] == "通勤香薰｜复购的小确幸"
    assert composed["body"] == "下班路上被它治愈。"
    assert composed["tags"] == ["香薰", "通勤好物", "朋友安利", "治愈", "多余"]
    assert composed["comment_hook"] == "评论区告诉我你的心头好"
    assert composed["validation"] == {"status": "needs_human_review", "issues": ["命中禁止项"]}
    assert all(isinstance(item, CandidateTitle) for item in composed["candidate_titles"])
    assert composed["candidate_titles"][1].text == "x" * 30
    assert calls[0]["timeout"] == 90
    assert "素材卖点" in calls[0]["user"]
    assert "通勤香薰很治愈" in calls[0]["user"]
    assert "不要硬广" in calls[0]["user"]


def test_note_composer_adds_fallback_candidate_title():
    def fake_json_call(*, system: str, user: str, timeout: int):
        return {
            "title": "好物分享",
            "body": "正文",
            "candidate_titles": [],
            "validation": {},
        }

    composed = note_composer.compose_note_llm(
        _skill(),
        AssetBundle(),
        {},
        json_call=fake_json_call,
        error_type=NoteComposerTestError,
    )

    assert composed["candidate_titles"] == [CandidateTitle(text="好物分享", rule_name="", rationale="")]
    assert composed["validation"] == {"status": "pass", "issues": []}


def test_note_composer_raises_domain_error_when_title_or_body_missing():
    def fake_json_call(*, system: str, user: str, timeout: int):
        return {"title": "", "body": "正文"}

    with pytest.raises(NoteComposerTestError, match="缺 title 或 body"):
        note_composer.compose_note_llm(
            _skill(),
            AssetBundle(),
            {},
            json_call=fake_json_call,
            error_type=NoteComposerTestError,
        )
