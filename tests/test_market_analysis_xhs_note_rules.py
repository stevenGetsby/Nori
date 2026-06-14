"""Tests for single-note XHS rule analysis helpers."""

from __future__ import annotations

from pathlib import Path

from nori.agents.market_analysis.schemas import XHSSeedSkillDraft, XHSNoteSample
from nori.agents.market_analysis.xhs_note_analyzer import rules as xhs_note_rules


def _sample_note(**overrides) -> XHSNoteSample:
    data = {
        "meta_path": Path("cold_start_data/xhs/设计/author_1/posts/note_001/meta.json"),
        "category": "设计",
        "author_id": "author_1",
        "author_name": "测试作者",
        "note_id": "note_001",
        "title": "报告！ 年夜饭薯该宠幸谁？",
        "desc": (
            "年夜饭的仪式感固然很多，但是在吃这件事情上更有话语权。\n"
            "什么？你问这些邪门搭配中不中？\n"
            "在搜索框输入答案之书，一起看看结果。\n"
            "#新年答案之书"
        ),
        "tags": ["#新年答案之书"],
        "metrics": {"liked": 102, "collected": 22, "commented": 20, "shared": 6},
        "image_count": 3,
        "note_type": "normal",
        "note_url": "https://www.xiaohongshu.com/explore/note_001",
    }
    data.update(overrides)
    return XHSNoteSample(**data)


def test_rule_analyze_note_builds_single_note_seed_skill_draft():
    draft = xhs_note_rules.rule_analyze_note(_sample_note())

    assert isinstance(draft, XHSSeedSkillDraft)
    assert draft.skill_id == "seed.xhs.设计.note.single.note_001"
    assert draft.match["scene"] == "问题悬念型 note"
    assert draft.match["goals"] == ["平台搜索"]
    assert draft.craft["title_rules"]
    assert draft.craft["body_structure"]
    assert draft.evidence["source_note"]["note_id"] == "note_001"
    assert draft.evidence["text_evidence"]["cta_lines"] == ["在搜索框输入答案之书，一起看看结果。"]
    assert draft.validation["pipeline"] == ["rule_analyzer"]


def test_rule_analyze_note_detects_design_case_scene_and_goals():
    note = _sample_note(
        title="品牌视觉设计项目复盘",
        desc=(
            "项目起点来自一次社区品牌升级。\n"
            "我们通过海报和字体结构建立视觉系统。\n"
            "不只是好看，也要让品牌意义被看见。\n"
            "项目时间：2026"
        ),
        metrics={},
    )

    draft = xhs_note_rules.rule_analyze_note(note)

    assert draft.match["scene"] == "设计案例解析型 note"
    assert draft.match["goals"] == ["作品展示", "设计灵感", "品牌表达"]
    assert [item["name"] for item in draft.craft["body_structure"]] == [
        "项目缘起",
        "场景展开",
        "视觉方法",
        "概念升华",
        "项目信息",
    ]


def test_title_rules_and_content_lines_are_exposed_for_compatibility():
    assert xhs_note_rules.content_lines("第一行\n\n第二行") == ["第一行", "第二行"]
    assert [item["name"] for item in xhs_note_rules.title_rules("3 个方法！")] == [
        "口播感标题",
        "数字钩子",
        "短标题",
    ]
