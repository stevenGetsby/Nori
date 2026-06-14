import importlib
import json
from pathlib import Path

import nori.core.llms as llms

from nori.agents.user_profiling import AccountPlannerAgent, AccountPlannerInput, IntakeAgent, UserInput


planner_module = importlib.import_module("nori.agents.user_profiling.account_planner.account_planner")


def _holly_input(enable_search=False):
    holly_dir = Path("cases/Holly/showcase")
    text = (holly_dir / "brief.md").read_text(encoding="utf-8")
    images = sorted(
        str(path)
        for path in (holly_dir / "assets").iterdir()
        if path.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
    )
    return AccountPlannerInput(text=text, images=images, platform="xhs", enable_search=enable_search)


def _fake_llm_response():
    return """
    {
      "tags": {
        "track": "怪趣文创",
        "goal": "涨粉带货",
        "platform": "小红书",
        "product": "文创周边",
        "positioning": "反焦虑主理人"
      },
      "recommended_positioning": "做一个用怪趣表达反焦虑的文创主理人账号。",
      "audience_profile": ["高压打工人", "喜欢怪趣审美的年轻消费者"],
      "content_directions": ["厕所哲学短故事", "产品设计幕后", "打工人情绪段子"],
      "benchmark_accounts": {
        "keyword_levels": [
          {"level": 1, "role": "赛道", "keyword": "文创", "reason": "看文创大盘"},
          {"level": 2, "role": "主题", "keyword": "反焦虑 文创 小红书", "reason": "看产品和情绪切口"},
          {"level": 3, "role": "内容点", "keyword": "怪趣 主理人 xhs", "reason": "看账号表达调性"}
        ],
        "search_keywords": ["文创", "反焦虑 文创 小红书", "怪趣 主理人 xhs"],
        "accounts": [
          {"name": "搜索：反焦虑 文创", "platform": "小红书", "reason": "找相似表达", "keyword": "反焦虑 文创"}
        ],
        "search_results": []
      },
      "unique_selling_points": ["粗俗语言包装体面诉求", "IP 和产品天然统一"],
      "ip_portrait_report": {
        "account_name_suggestions": ["便便精神合作社", "厕所时间研究所"],
        "account_keywords": ["反焦虑", "怪趣文创", "打工人嘴替"],
        "content_pillars": [
          {"name": "厕所哲学", "description": "用轻观点表达反焦虑"}
        ],
        "benchmark_creators": [
          {"name": "搜索：反焦虑 文创", "platform": "小红书", "reason": "找相似表达", "keyword": "反焦虑 文创"}
        ],
        "cover_design_formats": [
          {"name": "大字观点封面", "ratio": "3:4", "layout": "大字加IP", "reason": "强化记忆点"}
        ]
      }
    }
    """


def test_account_planner_no_llm_does_not_infer_holly_keywords():
    result = AccountPlannerAgent(use_llm=False).run(_holly_input())

    assert result.tags == {
        "track": "待判断",
        "goal": "待判断",
        "platform": "小红书",
        "product": "待判断",
        "positioning": "待判断",
    }
    assert result.benchmark_accounts["keyword_levels"] == []
    assert result.benchmark_accounts["search_keywords"] == []
    assert result.ip_portrait_report["account_name_suggestions"] == []


def test_account_planner_consumes_intaker_result_without_rule_inference():
    holly_dir = Path("cases/Holly/showcase")
    text = (holly_dir / "brief.md").read_text(encoding="utf-8")
    images = sorted(
        str(path)
        for path in (holly_dir / "assets").iterdir()
        if path.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
    )
    intaker_result = IntakeAgent(use_llm=False).run(UserInput(text=text, images=images))
    planner_input = AccountPlannerInput.from_intaker(intaker_result, text=text, platform="xhs")

    result = AccountPlannerAgent(use_llm=False).run(planner_input)

    assert planner_input.intention["goal"] == "涨粉"
    assert "图片资产" in planner_input.context["creative_assets"]
    assert len(planner_input.images) == len(images)
    assert result.tags["goal"] == "涨粉"
    assert result.tags["track"] == "待判断"
    assert result.benchmark_accounts["search_keywords"] == []


def test_account_planner_uses_llm_for_keywords(monkeypatch):
    def fake_chat_json(messages, *, usage="llm", **kwargs):
        assert usage == "llm"
        assert "_chat" not in kwargs
        assert kwargs["json_mode"] is True
        assert "搜索结果" in messages[1]["content"]
        return json.loads(_fake_llm_response())

    monkeypatch.setattr(llms, "chat_json", fake_chat_json)
    result = AccountPlannerAgent(use_llm=True).run(_holly_input())

    assert result.tags["track"] == "怪趣文创"
    assert result.tags["positioning"] == "反焦虑主理人"
    assert result.metadata["llm_enhanced"] is True
    assert result.benchmark_accounts["search_keywords"] == ["文创", "反焦虑文创", "怪趣主理人"]
    assert result.benchmark_accounts["keyword_levels"][0]["reason"] == "看文创大盘"
    assert [item["role"] for item in result.benchmark_accounts["keyword_levels"]] == ["赛道", "主题", "内容点"]
    assert result.ip_portrait_report["account_name_suggestions"] == ["便便精神合作社", "厕所时间研究所"]
    assert result.ip_portrait_report["cover_design_formats"][0]["ratio"] == "3:4"


def test_account_planner_invalid_llm_json_falls_back(monkeypatch):
    def fake_chat_json(messages, *, usage="llm", **kwargs):  # noqa: ARG001
        raise llms.ChatJSONError("bad json", "not json")

    monkeypatch.setattr(llms, "chat_json", fake_chat_json)
    result = AccountPlannerAgent(use_llm=True).run(_holly_input())

    assert result.tags["track"] == "待判断"
    assert result.tags["platform"] == "小红书"
    assert result.benchmark_accounts["search_keywords"] == []
    assert result.metadata["llm_error"]["stage"] == "account_planner"
    assert result.metadata["llm_error"]["reason"] == "parse_error"


def test_account_planner_search_uses_llm_keywords(monkeypatch):
    def fake_chat_json(messages, *, usage="llm", **kwargs):
        return json.loads(_fake_llm_response())

    class FakeSearchProvider:
        def __init__(self):
            self.calls = []

        def search(self, *, platform, keyword, limit):
            self.calls.append({"platform": platform, "keyword": keyword, "limit": limit})
            return [
                {
                    "author": "便便精神研究所",
                    "title": "反焦虑文创账号",
                    "summary": "怪趣表达和文创周边结合。",
                }
            ]

    monkeypatch.setattr(llms, "chat_json", fake_chat_json)
    provider = FakeSearchProvider()
    result = AccountPlannerAgent(use_llm=True, search_provider=provider).run(_holly_input(enable_search=True))

    assert [item["keyword"] for item in provider.calls] == ["文创", "反焦虑文创", "怪趣主理人"]
    assert all(item["platform"] == "xhs" for item in provider.calls)
    assert result.benchmark_accounts["search_results"]
