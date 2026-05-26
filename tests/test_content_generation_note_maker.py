"""Tests for NoteMakerAgent (skill + assets → NoteDraft, 全程 LLM)."""

from __future__ import annotations

import importlib
import json

import llms
import pytest

from nori.market_analysis.models import NoteSkill
from nori.content_generation.models import UserAsset
from nori.content_generation import NoteMakerAgent
from nori.content_generation.note_maker import NoteMakerLLMError

note_maker_module = importlib.import_module("nori.content_generation.note_maker.note_maker")


def _planting_skill() -> dict:
    return {
        "skill_id": "种草推荐·朋友安利笔记制作指南",
        "label": "种草推荐·朋友安利",
        "goal": "planting",
        "note_type": "图文",
        "tone": "朋友安利",
        "creative_goal": "像朋友推荐一样把真实使用感讲清楚。",
        "title_rules": [
            {"name": "数字钩子", "rule": "用数字暗示步骤或结果。", "evidence": "3 个让我回购的理由"},
            {"name": "观点标题", "rule": "用一句明确观点承载主题。", "evidence": "这款真的不踩雷"},
        ],
        "opening_rules": [{"name": "首句定场", "rule": "第一句先给场景。", "evidence": "下班通勤"}],
        "body_structure": [{"name": "模块分段", "rule": "用小标题承载。", "evidence": ""}],
        "interaction_rules": [{"name": "评论触发", "rule": "正文留可回答的问题。", "evidence": ""}],
        "avoid_rules": ["不要硬广", "不要照搬原话"],
        "metrics_summary": {"liked_p50": 1200, "collected_p50": 600, "sample": 4},
    }


def _debrief_skill() -> dict:
    skill = _planting_skill()
    skill.update({
        "skill_id": "经验复盘·个人经验笔记制作指南",
        "label": "经验复盘·个人经验",
        "goal": "debrief",
        "tone": "个人经验",
        "creative_goal": "用真实经历换一份可执行清单。",
    })
    return skill


def _stub_chat(call_log: list[dict], responses: list[str]):
    """按顺序返回 responses，每次调用记录到 call_log。"""
    it = iter(responses)

    def fake_chat(messages, *, usage="llm", **kwargs):
        call_log.append({"messages": messages, "usage": usage, "kwargs": kwargs})
        try:
            return next(it)
        except StopIteration as exc:
            raise AssertionError("LLM 被调用次数超过预设") from exc

    return fake_chat


def test_note_maker_routes_json_calls_through_llms_chat_json(monkeypatch):
    skills = [_planting_skill()]
    assets = [UserAsset(kind="text", text="香薰好物")]
    calls: list[dict] = []
    sentinel_chat = object()

    def fake_chat_json(messages, *, usage="llm", _chat=None, **kwargs):
        calls.append({"messages": messages, "usage": usage, "_chat": _chat, "kwargs": kwargs})
        assert _chat is sentinel_chat
        assert kwargs["json_mode"] is True
        return json.loads(_CURATE_JSON) if len(calls) == 1 else json.loads(_COMPOSE_JSON)

    monkeypatch.setattr(llms, "chat", sentinel_chat)
    monkeypatch.setattr(llms, "chat_json", fake_chat_json)

    draft = NoteMakerAgent().run(skills, assets, intent={"goal": "产品种草"})

    assert draft.title == "通勤香薰｜复购的小确幸"
    assert len(calls) == 2
    assert all(call["usage"] == "llm" for call in calls)


_CURATE_JSON = json.dumps({
    "main_image_indices": [1],
    "aux_image_indices": [2],
    "text_points": ["3 个让我回购的随身香薰", "下班通勤香气治愈了一天疲惫"],
    "brand_facts": ["小众设计师品牌"],
    "data_points": ["复购率 60%"],
})

_COMPOSE_JSON = json.dumps({
    "title": "通勤香薰｜复购的小确幸",
    "candidate_titles": [
        {"text": "通勤香薰｜复购的小确幸", "rule_name": "观点标题", "rationale": "贴合朋友安利语气"},
        {"text": "3 款让我回购的香薰", "rule_name": "数字钩子", "rationale": "用数字承题"},
    ],
    "body": "下班通勤路上，是这瓶香薰把我从疲惫里捞起来。\n\n复购了 3 次，分享给同样需要治愈的你。",
    "tags": ["香薰", "通勤好物", "朋友安利"],
    "comment_hook": "评论区告诉我你的香薰心头好 👇",
    "validation": {"status": "pass", "issues": []},
})


def test_note_maker_single_skill_skips_picker(monkeypatch):
    skills = [_planting_skill()]
    assets = [
        UserAsset(kind="image", path="/tmp/main.jpg"),
        UserAsset(kind="image", path="/tmp/aux.jpg"),
        UserAsset(kind="text", text="3 个让我回购的随身香薰"),
    ]
    log: list[dict] = []
    monkeypatch.setattr(llms, "chat", _stub_chat(log, [_CURATE_JSON, _COMPOSE_JSON]))

    draft = NoteMakerAgent().run(skills, assets, intent={"goal": "产品种草"})

    assert len(log) == 2  # 只跑了 curate + compose，没跑 picker
    assert draft.skill_id == "种草推荐·朋友安利笔记制作指南"
    assert draft.title == "通勤香薰｜复购的小确幸"
    assert draft.body.startswith("下班通勤")
    assert draft.tags == ["香薰", "通勤好物", "朋友安利"]
    assert draft.comment_hook.startswith("评论区")
    assert draft.metrics_target == {"liked_target": 1200, "collected_target": 600, "sample": 4}
    assert draft.validation == {"status": "pass", "issues": []}
    assert draft.llm_enhanced is True
    assert len(draft.candidate_titles) == 2


def test_note_maker_multi_skill_invokes_picker(monkeypatch):
    skills = [_debrief_skill(), _planting_skill()]
    assets = [UserAsset(kind="text", text="香薰好物")]
    pick_json = json.dumps({"skill_id": "种草推荐·朋友安利笔记制作指南"})
    log: list[dict] = []
    monkeypatch.setattr(
        llms, "chat",
        _stub_chat(log, [pick_json, _CURATE_JSON, _COMPOSE_JSON]),
    )

    draft = NoteMakerAgent().run(skills, assets, intent={"goal": "产品种草", "tone": ["朋友安利"]})

    assert len(log) == 3
    assert draft.skill_id == "种草推荐·朋友安利笔记制作指南"


def test_note_maker_uses_main_image_as_cover(monkeypatch):
    skills = [_planting_skill()]
    assets = [
        UserAsset(kind="image", path="/tmp/a.jpg"),
        UserAsset(kind="image", path="/tmp/b.jpg"),
        UserAsset(kind="image", path="/tmp/c.jpg"),
    ]
    curate_json = json.dumps({
        "main_image_indices": [1],
        "aux_image_indices": [0, 2],
        "text_points": [], "brand_facts": [], "data_points": [],
    })
    monkeypatch.setattr(llms, "chat", _stub_chat([], [curate_json, _COMPOSE_JSON]))

    draft = NoteMakerAgent().run(skills, assets)

    assert draft.cover_path == "/tmp/b.jpg"
    assert draft.image_paths == ["/tmp/a.jpg", "/tmp/c.jpg"]


def test_note_maker_falls_back_first_image_when_llm_returns_no_main(monkeypatch):
    skills = [_planting_skill()]
    assets = [UserAsset(kind="image", path="/tmp/only.jpg")]
    curate_json = json.dumps({
        "main_image_indices": [],
        "aux_image_indices": [],
        "text_points": [], "brand_facts": [], "data_points": [],
    })
    monkeypatch.setattr(llms, "chat", _stub_chat([], [curate_json, _COMPOSE_JSON]))

    draft = NoteMakerAgent().run(skills, assets)

    assert draft.cover_path == "/tmp/only.jpg"


def test_note_maker_caps_image_paths_to_eight(monkeypatch):
    skills = [_planting_skill()]
    assets = [UserAsset(kind="image", path=f"/tmp/{i}.jpg") for i in range(12)]
    curate_json = json.dumps({
        "main_image_indices": [0],
        "aux_image_indices": list(range(1, 12)),
        "text_points": [], "brand_facts": [], "data_points": [],
    })
    monkeypatch.setattr(llms, "chat", _stub_chat([], [curate_json, _COMPOSE_JSON]))

    draft = NoteMakerAgent().run(skills, assets)

    assert len(draft.image_paths) == 8


def test_note_maker_propagates_validation_from_llm(monkeypatch):
    skills = [_planting_skill()]
    assets = [UserAsset(kind="text", text="硬广")]
    compose_json = json.dumps({
        "title": "好物分享",
        "candidate_titles": [{"text": "好物分享"}],
        "body": "正文",
        "tags": [],
        "comment_hook": "",
        "validation": {"status": "needs_human_review", "issues": ["命中禁止项：硬广"]},
    })
    monkeypatch.setattr(llms, "chat", _stub_chat([], [_CURATE_JSON, compose_json]))

    draft = NoteMakerAgent().run(skills, assets)

    assert draft.validation["status"] == "needs_human_review"
    assert "硬广" in draft.validation["issues"][0]


def test_note_maker_raises_when_compose_missing_title(monkeypatch):
    skills = [_planting_skill()]
    assets = [UserAsset(kind="text", text="x")]
    bad_compose = json.dumps({"title": "", "body": "x"})
    monkeypatch.setattr(llms, "chat", _stub_chat([], [_CURATE_JSON, bad_compose]))

    with pytest.raises(NoteMakerLLMError, match="缺 title 或 body"):
        NoteMakerAgent().run(skills, assets)


def test_note_maker_raises_when_picker_returns_unknown_id(monkeypatch):
    skills = [_planting_skill(), _debrief_skill()]
    assets = [UserAsset(kind="text", text="x")]
    pick_json = json.dumps({"skill_id": "不存在的 skill"})
    monkeypatch.setattr(llms, "chat", _stub_chat([], [pick_json]))

    with pytest.raises(NoteMakerLLMError, match="未知 skill_id"):
        NoteMakerAgent().run(skills, assets)


def test_note_maker_raises_when_llm_chat_throws(monkeypatch):
    skills = [_planting_skill()]
    assets = [UserAsset(kind="text", text="x")]

    def boom(messages, *, usage="llm", **kwargs):
        raise RuntimeError("llm down")

    monkeypatch.setattr(llms, "chat", boom)
    with pytest.raises(NoteMakerLLMError, match="llms.chat 失败"):
        NoteMakerAgent().run(skills, assets)


def test_note_maker_raises_when_llm_returns_non_json(monkeypatch):
    skills = [_planting_skill()]
    assets = [UserAsset(kind="text", text="x")]
    monkeypatch.setattr(llms, "chat", _stub_chat([], ["this is not json"]))

    with pytest.raises(NoteMakerLLMError, match="无法解析为 JSON"):
        NoteMakerAgent().run(skills, assets)


def test_note_maker_accepts_note_skill_dataclass(monkeypatch):
    skill = NoteSkill(
        skill_id="x",
        label="测评·专业",
        goal="general",
        note_type="图文",
        tone="专业",
        creative_goal="把测评讲清楚。",
        title_rules=[{"name": "短标题", "rule": "短句承题。", "evidence": "AI 实测"}],
        avoid_rules=["不要硬广"],
        metrics_summary={"liked_p50": 500, "sample": 2},
    )
    monkeypatch.setattr(llms, "chat", _stub_chat([], [_CURATE_JSON, _COMPOSE_JSON]))

    draft = NoteMakerAgent().run([skill], [UserAsset(kind="text", text="测评要点")])

    assert draft.skill_id == "x"
    assert draft.title


def test_note_maker_accepts_path_strings_and_dict_assets(monkeypatch):
    skills = [_planting_skill()]
    assets = ["/tmp/main.jpg", {"kind": "text", "text": "随手好物"}]
    monkeypatch.setattr(llms, "chat", _stub_chat([], [_CURATE_JSON, _COMPOSE_JSON]))

    draft = NoteMakerAgent().run(skills, assets)

    # _CURATE_JSON 主图 index=1（文本）越界 → fallback 第一张图片
    assert draft.cover_path == "/tmp/main.jpg"


def test_note_maker_raises_when_skills_empty():
    with pytest.raises(ValueError):
        NoteMakerAgent().run([], [UserAsset(kind="text", text="x")])
