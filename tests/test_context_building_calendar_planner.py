from nori.core import AccountOperationProject
from nori.core import ContentCalendar, KPIPlan, OperationPlan, ClientBrief
import importlib

import llms

from nori.agents.planning import CalendarPlannerAgent, plan_calendar


calendar_module = importlib.import_module("nori.agents.planning.calendar_planner.calendar_planner")


def _brief():
    return ClientBrief(
        client_name="花店主理人",
        brand_name="春日花房",
        platform="xhs",
        goals=["建立本地认知", "提升到店咨询"],
        audience=["周边 3 公里年轻家庭"],
        positioning_notes=["社区花艺顾问"],
        constraints=["不夸大疗效"],
        taboos=["价格欺骗"],
        source_materials=[{"kind": "product_photo", "usage": "商品图"}],
    )


def _operation_plan():
    return OperationPlan(
        plan_id="plan_7d",
        horizon_days=7,
        objectives=["建立本地认知", "提升到店咨询"],
        content_pillars=["花艺知识", "门店日常"],
        cadence="7 天内规划 3 条内容任务",
        kpi_targets={"content_tasks": 3},
        milestones=[{"day": 7, "target": "完成首周复盘"}],
        risk_controls=["平台合规审核"],
    )


def _kpi_plan(content_tasks=3):
    return KPIPlan(
        plan_id="kpi_plan_7d",
        horizon_days=7,
        targets={"content_tasks": content_tasks, "review_pass_rate": ">= 90%"},
        milestones=[{"day": 7, "target": "核验内容产出"}],
        measurement_notes=["手动记录后台数据"],
    )


def test_calendar_planner_rule_fallback_builds_content_calendar():
    calendar = CalendarPlannerAgent(use_llm=False).run(
        _operation_plan(),
        kpi_plan=_kpi_plan(),
        client_brief=_brief(),
        start_date="2026-05-25",
    )

    assert isinstance(calendar, ContentCalendar)
    assert calendar.calendar_id == "cal_2026-05-25_7d"
    assert calendar.start_date == "2026-05-25"
    assert calendar.end_date == "2026-05-31"
    assert calendar.themes == ["花艺知识", "门店日常"]
    assert len(calendar.tasks) == 3
    assert [task.scheduled_date for task in calendar.tasks] == [
        "2026-05-25",
        "2026-05-28",
        "2026-05-31",
    ]
    assert all(task.platform == "xhs" for task in calendar.tasks)
    assert all(task.status == "planned" for task in calendar.tasks)
    assert calendar.tasks[0].brief["brand_name"] == "春日花房"
    assert calendar.metadata["planner"] == "rule_fallback"
    assert calendar.metadata["critic"]["status"] == "warn"
    assert "当前排期仍依赖规则兜底，应优先切换为 LLM 主线" in calendar.metadata["critic"]["issues"]


def test_calendar_planner_accepts_project_and_round_trips_calendar():
    project = AccountOperationProject(
        project_id="ops_001",
        name="春日花房账号代运营",
        client_brief=_brief(),
        operation_plan=_operation_plan(),
        kpi_plan=_kpi_plan(),
    )

    calendar = plan_calendar(project, use_llm=False, start_date="2026-05-25")
    restored = ContentCalendar.from_dict(calendar.to_dict())

    assert restored.to_dict() == calendar.to_dict()
    assert restored.tasks[0].brief["content_pillar"] == "花艺知识"
    assert restored.metadata["source_plan_id"] == "plan_7d"


def test_calendar_planner_accepts_dict_inputs():
    calendar = CalendarPlannerAgent(use_llm=False).run(
        {
            "operation_plan": _operation_plan().to_dict(),
            "kpi_plan": _kpi_plan(content_tasks=2).to_dict(),
            "client_brief": _brief().to_dict(),
        },
        start_date="2026-05-25",
    )

    assert len(calendar.tasks) == 2
    assert calendar.tasks[1].scheduled_date == "2026-05-31"
    assert calendar.metadata["source_kpi_plan_id"] == "kpi_plan_7d"


def test_calendar_planner_uses_llm_json_when_available(monkeypatch):
    def fake_chat(messages, *, usage="llm", **kwargs):
        assert usage == "llm"
        assert kwargs["response_format"] == {"type": "json_object"}
        assert "KPI 计划" in messages[1]["content"]
        return """
        {
          "themes": ["花艺知识", "节日场景"],
          "cadence": "7 天 2 条重点笔记",
          "tasks": [
            {
              "title": "母亲节花别乱买",
              "day": 2,
              "content_type": "note",
              "topic": "母亲节花束搭配",
              "objective": "提升咨询",
              "priority": 1,
              "brief": {
                "cover_title": "母亲节花别乱买",
                "content_pillar": "花艺知识",
                "angle": "送礼避坑"
              },
              "required_assets": ["product_photo"],
              "notes": ["封面大字要清晰"]
            },
            {
              "title": "社区花店的一天",
              "day": 7,
              "content_type": "note",
              "topic": "门店日常",
              "objective": "建立本地认知",
              "priority": 2,
              "brief": {
                "cover_title": "花店日常",
                "content_pillar": "门店日常",
                "angle": "真实经营"
              },
              "required_assets": ["product_photo"],
              "notes": ["保持生活化"]
            }
          ],
          "notes": ["等待内容生产桥接"]
        }
        """

    monkeypatch.setattr(llms, "chat", fake_chat)

    calendar = CalendarPlannerAgent(use_llm=True).run(
        _operation_plan(),
        kpi_plan=_kpi_plan(content_tasks=2),
        client_brief=_brief(),
        start_date="2026-05-25",
    )

    assert calendar.cadence == "7 天 2 条重点笔记"
    assert len(calendar.tasks) == 2
    assert calendar.tasks[0].scheduled_date == "2026-05-26"
    assert calendar.tasks[1].scheduled_date == "2026-05-31"
    assert calendar.tasks[0].brief["angle"] == "送礼避坑"
    assert calendar.metadata["planner"] == "llm_with_fallback"
    assert calendar.metadata["critic"]["status"] == "pass"
    assert not calendar.metadata["critic"]["issues"]


def test_calendar_planner_llm_failure_keeps_fallback(monkeypatch):
    def fake_chat(messages, *, usage="llm", **kwargs):
        return "not json"

    monkeypatch.setattr(llms, "chat", fake_chat)

    calendar = CalendarPlannerAgent(use_llm=True).run(
        _operation_plan(),
        kpi_plan=_kpi_plan(),
        client_brief=_brief(),
        start_date="2026-05-25",
    )

    assert calendar.metadata["planner"] == "rule_fallback"
    assert calendar.metadata["llm_error"]["stage"] == "calendar_planner"
    assert calendar.metadata["llm_error"]["reason"] == "parse_error"
    assert len(calendar.tasks) == 3
    assert calendar.metadata["critic"]["status"] == "warn"
