import json
import importlib
from pathlib import Path

import pytest

from nori.ana_agents import XHSNoteAnalyzer
from nori.agent_models import XHSNoteSample, XHSSeedSkillDraft
from data_collect import HotNote, TopNotesResult


analyzer_module = importlib.import_module("nori.ana_agents.xhs_note_analyzer")


def _sample_meta_path(tmp_path: Path):
    author_dir = tmp_path / "cold_start_data" / "xhs" / "设计" / "author_1"
    note_dir = author_dir / "posts" / "6984106b000000000a02aeaf"
    note_dir.mkdir(parents=True)
    (author_dir / "meta.json").write_text(
        json.dumps({"user_id": "author_1", "nickname": "测试作者"}, ensure_ascii=False),
        encoding="utf-8",
    )
    meta_path = note_dir / "meta.json"
    meta_path.write_text(
        json.dumps(
            {
                "note_id": "6984106b000000000a02aeaf",
                "title": "报告！ 年夜饭薯该宠幸谁？",
                "desc": (
                    "年夜饭的仪式感固然很多，但是在吃这件事情上更有话语权。\n"
                    "火锅涮一切，年糕炒一切，饺子包一切。\n"
                    "什么？你问这些邪门搭配中不中？\n"
                    "在搜索框输入答案之书，一起看看结果。"
                ),
                "user_id": "author_1",
                "liked_count": "102",
                "collected_count": "22",
                "comment_count": "20",
                "share_count": "6",
                "tag_list": "#新年答案之书 #小红书答案之书",
                "image_count": 3,
                "note_type": "normal",
                "note_url": "https://www.xiaohongshu.com/explore/6984106b000000000a02aeaf",
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    return meta_path


def test_xhs_note_analyzer_extracts_single_note_seed_skill_without_llm(tmp_path):
    analyzer = XHSNoteAnalyzer("cold_start_data/xhs", use_llm=False)
    note = analyzer.load_note(_sample_meta_path(tmp_path))
    skill = analyzer.analyze_note(note)
    data = skill.to_dict()

    assert isinstance(note, XHSNoteSample)
    assert isinstance(skill, XHSSeedSkillDraft)
    assert data["type"] == "xhs_note_seed_skill"
    assert data["status"] == "single_note_draft"
    assert data["platform"] == "小红书"
    assert data["category"] == "设计"
    assert data["match"]["scene"]
    assert data["craft"]["title_rules"]
    assert data["craft"]["body_structure"]
    assert data["evidence"]["source_note"]["note_id"] == "6984106b000000000a02aeaf"
    assert data["validation"]["result"] == "draft_only"
    assert data["validation"]["llm_enhanced"] is False
    assert data["validation"]["pipeline"] == ["rule_analyzer"]


def test_xhs_note_analyzer_enhances_rule_draft_with_llm(monkeypatch, tmp_path):
        def fake_chat(messages, *, usage="llm", **kwargs):
                assert usage == "llm"
                assert "规则草案" in messages[1]["content"]
                return """
                {
                    "match": {
                        "scene": "问题悬念活动型 note",
                        "goals": ["互动", "活动参与"],
                        "note_type": "图文/视频"
                    },
                    "craft": {
                        "creative_goal": "用一个问题把用户带入场景，再把活动入口自然交代清楚。",
                        "title_rules": [
                            {"name": "问题钩子", "rule": "标题先抛一个用户会想回答的问题。", "evidence": "报告！ 年夜饭薯该宠幸谁？"}
                        ],
                        "opening_rules": [
                            {"name": "场景开场", "rule": "开头先确认共同场景，再进入具体玩法。", "evidence": "年夜饭的仪式感固然很多"}
                        ],
                        "body_structure": [
                            {"name": "场景共识", "rule": "先说共同场景。", "evidence": "年夜饭"},
                            {"name": "连续追问", "rule": "用多个问题推动互动。", "evidence": "行不行"}
                        ],
                        "interaction_rules": [
                            {"name": "搜索入口", "rule": "把搜索动作包装成答案入口。", "evidence": "在搜索框输入"}
                        ],
                        "visual_rules": [
                            {"name": "封面设问", "rule": "封面优先呈现问题和答案感。", "evidence": "cover.jpg"}
                        ],
                        "avoid_rules": ["不要把活动入口写成硬广口令。"]
                    },
                    "evidence": {
                        "llm_observations": ["这篇 note 的核心是用问题降低活动参与门槛。"]
                    },
                    "validation": {
                        "llm_notes": ["需要在更多活动型笔记中验证问题钩子是否高频。"]
                    }
                }
                """

        monkeypatch.setattr(analyzer_module.llms, "chat", fake_chat)
        analyzer = XHSNoteAnalyzer("cold_start_data/xhs", use_llm=True)
        note = analyzer.load_note(_sample_meta_path(tmp_path))
        skill = analyzer.analyze_note(note)
        data = skill.to_dict()

        assert data["match"]["scene"] == "问题悬念活动型 note"
        assert data["craft"]["creative_goal"] == "用一个问题把用户带入场景，再把活动入口自然交代清楚。"
        assert data["craft"]["title_rules"][0]["name"] == "问题钩子"
        assert data["evidence"]["source_note"]["note_id"] == "6984106b000000000a02aeaf"
        assert data["evidence"]["llm_observations"] == ["这篇 note 的核心是用问题降低活动参与门槛。"]
        assert data["validation"]["llm_enhanced"] is True
        assert data["validation"]["pipeline"] == ["rule_analyzer", "llm_enhancer", "format_normalizer"]


def test_xhs_note_analyzer_routes_json_calls_through_llms_chat_json(monkeypatch, tmp_path):
    calls: list[dict] = []

    def fake_chat_json(messages, *, usage="llm", _chat=None, **kwargs):
        calls.append({"messages": messages, "usage": usage, "chat": _chat, "kwargs": kwargs})
        return {
            "match": {"scene": "chat_json 场景", "goals": ["收藏"], "note_type": "图文"},
            "craft": {"creative_goal": "通过统一 JSON helper 增强规则。"},
            "evidence": {"llm_observations": ["已路由到 llms.chat_json"]},
            "validation": {"llm_notes": ["保持 analyzer 降级语义不变。"]},
        }

    monkeypatch.setattr(analyzer_module.llms, "chat_json", fake_chat_json)
    analyzer = XHSNoteAnalyzer("cold_start_data/xhs", use_llm=True)
    note = analyzer.load_note(_sample_meta_path(tmp_path))
    skill = analyzer.analyze_note(note)

    assert calls
    assert calls[0]["usage"] == "llm"
    assert calls[0]["chat"] is analyzer_module.llms.chat
    assert calls[0]["kwargs"]["timeout"] == 60
    assert skill.match["scene"] == "chat_json 场景"


def test_xhs_note_analyzer_falls_back_when_llm_fails(monkeypatch, tmp_path):
    def broken_chat(*args, **kwargs):
        raise RuntimeError("llm down")

    monkeypatch.setattr(analyzer_module.llms, "chat", broken_chat)
    analyzer = XHSNoteAnalyzer("cold_start_data/xhs", use_llm=True)
    note = analyzer.load_note(_sample_meta_path(tmp_path))
    skill = analyzer.analyze_note(note)
    data = skill.to_dict()

    assert data["validation"]["llm_enhanced"] is False
    assert data["validation"]["pipeline"] == ["rule_analyzer", "llm_enhancer_failed", "format_normalizer"]
    assert "llm down" in data["validation"]["llm_error"]
    assert data["craft"]["title_rules"]


class FakeSessionCollector:
    def __init__(self, data_dir: Path, insufficient=None):
        self.data_dir = data_dir
        self.insufficient = insufficient or []
        self.last_rule = None

    def start_sign_server(self):
        return None

    def collect_top_notes(self, rule):
        self.last_rule = rule
        keyword_dir = self.data_dir / "20260515_000000_测试关键词"
        keyword_dir.mkdir(parents=True, exist_ok=True)
        notes = [
            HotNote(
                note_id="note_1",
                keyword="测试关键词",
                title="3 个方法做出有点击欲的封面",
                desc="先给结果，再展示封面案例。评论区告诉我你喜欢哪版。",
                author_id="author_1",
                author_name="作者一",
                liked=100,
                collected=20,
                comment=5,
                share=1,
                tags=["封面设计", "小红书运营"],
                image_count=4,
                note_type="normal",
                note_url="https://www.xiaohongshu.com/explore/note_1",
                time_ms=1778000000000,
                cover_path=str(keyword_dir / "note_1" / "images" / "cover.jpg"),
                image_paths=[str(keyword_dir / "note_1" / "images" / "image_0.jpg")],
            ),
            HotNote(
                note_id="note_2",
                keyword="测试关键词",
                title="这类种草封面为什么更想点",
                desc="用真实场景承接产品价值，最后给收藏理由。",
                author_id="author_2",
                author_name="作者二",
                liked=80,
                collected=18,
                comment=2,
                share=1,
                tags=["种草", "封面"],
                image_count=2,
                note_type="normal",
                note_url="https://www.xiaohongshu.com/explore/note_2",
                time_ms=1778000000000,
                cover_path=str(keyword_dir / "note_2" / "images" / "cover.jpg"),
                image_paths=[str(keyword_dir / "note_2" / "images" / "image_0.jpg")],
            ),
        ]
        return TopNotesResult(
            platform="xhs",
            queries=list(rule.keywords),
            hot_notes=notes,
            insufficient=list(self.insufficient),
            source_data_dir=str(self.data_dir),
            source_keyword_dirs={"测试关键词": str(keyword_dir)},
        )


def test_collect_for_session_requires_llm_and_writes_skill_only_json(monkeypatch, tmp_path):
    def fake_chat(messages, *, usage="llm", **kwargs):
        assert usage == "llm"
        assert "笔记列表" in messages[1]["content"]
        return """
        {"labels": [
            {"note_id": "note_1", "goal": "planting", "tone": "朋友安利"},
            {"note_id": "note_2", "goal": "planting", "tone": "朋友安利"}
        ]}
        """

    monkeypatch.setattr(analyzer_module.llms, "chat", fake_chat)
    analyzer = XHSNoteAnalyzer(use_llm=True)
    report = analyzer.collect_for_session(
        {"platform": "xhs", "keywords": ["测试关键词"], "data_dir": str(tmp_path)},
        dc=FakeSessionCollector(tmp_path),
    )

    assert report.llm_enhanced is True
    skill = report.skills[0].to_dict()
    assert skill["skill_id"] == "种草推荐·朋友安利笔记制作指南"
    assert skill["cover_rules"]
    assert "session.xhs" not in skill["skill_id"]

    skill_path = tmp_path / "20260515_000000_note_skill_guides.json"
    skill_output = __import__("json").loads(skill_path.read_text(encoding="utf-8"))
    assert set(skill_output) == {"skills"}
    assert "context" not in skill_output
    assert skill_output["skills"][0]["skill_id"] == "种草推荐·朋友安利笔记制作指南"


def test_collect_for_session_uses_fixed_search_standard(monkeypatch, tmp_path):
    monkeypatch.setattr(analyzer_module.llms, "chat", lambda *args, **kwargs: """
        {"labels": [
            {"note_id": "note_1", "goal": "planting", "tone": "朋友安利"},
            {"note_id": "note_2", "goal": "planting", "tone": "朋友安利"}
        ]}
        """)
    collector = FakeSessionCollector(tmp_path)
    analyzer = XHSNoteAnalyzer(use_llm=True)

    analyzer.collect_for_session(
        {"platform": "xhs", "keywords": ["测试关键词"], "data_dir": str(tmp_path)},
        dc=collector,
    )

    assert collector.last_rule.days == 30
    assert collector.last_rule.top_k_per_keyword == 5
    assert collector.last_rule.min_liked == 500
    assert collector.last_rule.pool_size == 20


def test_collect_for_session_stops_without_llm(tmp_path):
    analyzer = XHSNoteAnalyzer(use_llm=False)
    with pytest.raises(ValueError, match="必须启用 LLM"):
        analyzer.collect_for_session(
            {"platform": "xhs", "keywords": ["测试关键词"], "data_dir": str(tmp_path)},
            dc=FakeSessionCollector(tmp_path),
        )


def test_collect_for_session_stops_when_llm_labels_are_empty(monkeypatch, tmp_path):
    monkeypatch.setattr(analyzer_module.llms, "chat", lambda *args, **kwargs: '{"labels": []}')
    analyzer = XHSNoteAnalyzer(use_llm=True)
    with pytest.raises(RuntimeError, match="LLM 标签结果为空"):
        analyzer.collect_for_session(
            {"platform": "xhs", "keywords": ["测试关键词"], "data_dir": str(tmp_path)},
            dc=FakeSessionCollector(tmp_path),
        )


def test_collect_for_session_stops_when_collection_is_insufficient(monkeypatch, tmp_path):
    monkeypatch.setattr(analyzer_module.llms, "chat", lambda *args, **kwargs: '{"labels": []}')
    analyzer = XHSNoteAnalyzer(use_llm=True)
    with pytest.raises(RuntimeError, match="高赞采集不足"):
        analyzer.collect_for_session(
            {"platform": "xhs", "keywords": ["测试关键词"], "data_dir": str(tmp_path)},
            dc=FakeSessionCollector(tmp_path, insufficient=[{"keyword": "测试关键词", "got": 1, "need": 5}]),
        )
