"""Tests for XHS session report artifact helpers."""

from __future__ import annotations

import json

from nori.market_analysis.models import NoteSkill, SessionSkillReport
from nori.market_analysis.xhs_note_analyzer import session_reporter as xhs_session_reporter


def _skill() -> NoteSkill:
    return NoteSkill(
        skill_id="种草推荐·朋友安利笔记制作指南",
        label="种草推荐·朋友安利",
        goal="planting",
        note_type="图文",
        tone="朋友安利",
        creative_goal="把对象放进真实生活场景里讲清楚。",
    )


def test_report_stamp_uses_first_keyword_dir_timestamp():
    assert (
        xhs_session_reporter.report_stamp(
            {
                "封面": "/tmp/nori/20260515_000000_封面",
                "运营": "/tmp/nori/20260516_010203_运营",
            }
        )
        == "20260515_000000"
    )
    assert xhs_session_reporter.report_stamp({}) == "session"
    assert xhs_session_reporter.report_stamp({"bad": "/tmp/no-timestamp"}) == "session"


def test_skills_output_is_skills_only_fixture():
    report = SessionSkillReport(
        context={"topic": "封面设计"},
        keywords=["封面"],
        skills=[_skill()],
        coverage={"total_notes": 2},
        llm_enhanced=True,
    )

    output = xhs_session_reporter.skills_output(report)

    assert set(output) == {"skills"}
    assert output["skills"][0]["skill_id"] == "种草推荐·朋友安利笔记制作指南"


def test_write_session_outputs_writes_report_and_skills_only_json(tmp_path):
    keyword_dir = tmp_path / "20260515_000000_封面"
    report = SessionSkillReport(
        context={"topic": "封面设计"},
        keywords=["封面"],
        skills=[_skill()],
        coverage={"total_notes": 2},
        source_data_dir=str(tmp_path),
        source_keyword_dirs={"封面": str(keyword_dir)},
        llm_enhanced=True,
    )

    paths = xhs_session_reporter.write_session_outputs(report)

    assert set(paths) == {"report", "skills"}
    report_data = json.loads(paths["report"].read_text(encoding="utf-8"))
    skills_data = json.loads(paths["skills"].read_text(encoding="utf-8"))
    assert paths["report"].name == "20260515_000000_session_skill_report.json"
    assert paths["skills"].name == "20260515_000000_note_skill_guides.json"
    assert report_data["context"] == {"topic": "封面设计"}
    assert set(skills_data) == {"skills"}
    assert "context" not in skills_data


def test_write_session_outputs_returns_empty_without_source_dir():
    report = SessionSkillReport(
        context={},
        keywords=[],
        skills=[_skill()],
        llm_enhanced=True,
    )

    assert xhs_session_reporter.write_session_outputs(report) == {}
