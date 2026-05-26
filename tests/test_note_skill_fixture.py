import json

import llms

from nori.market_analysis.models import NoteEvidence, NoteSkill, SessionSkillReport
from nori.market_analysis import load_note_skills, note_skill_fixture, write_note_skill_fixture
from nori.market_analysis.note_skill_fixture import load_note_skills as direct_load_note_skills
from nori.core import UserAsset
from nori.content_generation import NoteMakerAgent


def _skill() -> NoteSkill:
    return NoteSkill(
        skill_id="种草推荐·朋友安利笔记制作指南",
        label="种草推荐·朋友安利",
        goal="planting",
        note_type="图文",
        tone="朋友安利",
        creative_goal="把产品放进真实生活场景里讲清楚。",
        title_rules=[{"name": "场景钩子", "rule": "标题先给具体场景。", "evidence": "通勤包"}],
        opening_rules=[{"name": "首句定场", "rule": "第一句说明使用场景。", "evidence": "下班路上"}],
        body_structure=[{"name": "三段式", "rule": "场景、体验、建议。", "evidence": ""}],
        interaction_rules=[{"name": "提问", "rule": "结尾给可回答问题。", "evidence": ""}],
        avoid_rules=["不要硬广"],
        metrics_summary={"liked_p50": 1200, "collected_p50": 300, "sample": 2},
        evidence_notes=[
            NoteEvidence(
                note_id="note_1",
                note_url="https://example.com/note",
                title="通勤包里这个最实用",
                liked=1200,
                collected=300,
            )
        ],
    )


def test_note_skill_fixture_round_trips_report_and_skills_only_json(tmp_path):
    report = SessionSkillReport(
        context={"topic": "通勤好物"},
        keywords=["通勤"],
        skills=[_skill()],
        coverage={"total_notes": 2},
        llm_enhanced=True,
    )

    fixture = note_skill_fixture(report)
    path = write_note_skill_fixture(report, tmp_path / "note_skill_guides.json")
    loaded_from_fixture = load_note_skills(path)
    loaded_from_report = load_note_skills(report.to_dict())

    assert set(fixture) == {"skills"}
    assert fixture["skills"][0]["skill_id"] == "种草推荐·朋友安利笔记制作指南"
    assert loaded_from_fixture[0].to_dict() == _skill().to_dict()
    assert loaded_from_report[0].evidence_notes[0].note_id == "note_1"


def test_note_skill_fixture_helpers_are_owned_by_market_analysis():
    assert load_note_skills is direct_load_note_skills
    assert load_note_skills.__module__ == "nori.market_analysis.note_skill_fixture"


def test_session_skill_report_from_dict_parses_string_booleans():
    restored = SessionSkillReport.from_dict({"llm_enhanced": "false"})

    assert restored.llm_enhanced is False


def test_load_note_skills_accepts_legacy_dicts():
    loaded = load_note_skills({
        "skills": [
            {
                "id": "legacy_skill",
                "label": "旧技能",
                "goal": "planting",
                "note_type": "图文",
                "tone": "朋友安利",
                "creative_goal": "旧格式也能恢复。",
            }
        ]
    })

    assert loaded[0].skill_id == "legacy_skill"
    assert loaded[0].label == "旧技能"
    assert loaded[0].evidence_notes == []


def test_loaded_note_skill_fixture_can_feed_note_maker(monkeypatch, tmp_path):
    calls = []

    def fake_chat_json(messages, *, usage="llm", **kwargs):
        calls.append(messages)
        if len(calls) == 1:
            return {
                "main_image_indices": [],
                "aux_image_indices": [],
                "text_points": ["通勤包轻便"],
                "brand_facts": ["小众设计师品牌"],
                "data_points": [],
            }
        return {
            "title": "通勤包｜轻便不乱",
            "candidate_titles": [{"text": "通勤包｜轻便不乱", "rule_name": "场景钩子", "rationale": "命中场景"}],
            "body": "下班路上最怕包太乱。这只通勤包分区清楚，也不压肩。",
            "tags": ["通勤包", "好物"],
            "comment_hook": "你通勤包里最离不开什么？",
            "validation": {"status": "pass", "issues": []},
        }

    monkeypatch.setattr("llms.chat_json", fake_chat_json)
    path = write_note_skill_fixture([_skill()], tmp_path / "fixture.json")
    skills = load_note_skills(json.loads(path.read_text(encoding="utf-8")))

    draft = NoteMakerAgent().run(
        skills,
        [UserAsset(kind="text", text="通勤包轻便，分区清楚")],
        intent={"goal": "产品种草"},
    )

    assert draft.skill_id == "种草推荐·朋友安利笔记制作指南"
    assert draft.title == "通勤包｜轻便不乱"
    assert draft.metrics_target["liked_target"] == 1200
