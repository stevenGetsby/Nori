from nori.core import AccountOperationProject
from nori.core import ClientBrief
import importlib

import llms

from nori.user_profiling.models import AccountPlanResult
from nori.context_building import OperationPlannerAgent, plan_operation


planner_module = importlib.import_module("nori.context_building.operation_planner.operation_planner")


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


def _account_plan():
    return AccountPlanResult(
        tags={
            "track": "花艺",
            "goal": "获客",
            "platform": "小红书",
            "product": "花束",
            "positioning": "社区花艺",
        },
        recommended_positioning="懂生活的社区花艺顾问",
        audience_profile=["周边 3 公里年轻家庭"],
        content_directions=["节日花束搭配", "门店日常", "花材养护"],
        benchmark_accounts={
            "search_keywords": ["花艺", "节日花束", "社区花店"],
            "keyword_levels": [],
            "accounts": [],
            "search_results": [],
        },
        unique_selling_points=["本地配送快", "审美稳定"],
        ip_portrait_report={
            "content_pillars": [
                {"name": "花艺知识", "description": "花材养护和搭配"},
                {"name": "门店日常", "description": "真实经营细节"},
            ],
            "account_keywords": ["花艺", "本地生活"],
        },
    )


def test_operation_planner_rule_fallback_builds_project_calendar_and_tasks():
    project = OperationPlannerAgent(use_llm=False).run(
        _brief(),
        _account_plan(),
        project_id="ops_001",
        start_date="2026-05-25",
        horizon_days=7,
    )

    assert isinstance(project, AccountOperationProject)
    assert project.project_id == "ops_001"
    assert project.status == "planning"
    assert project.client_brief.brand_name == "春日花房"
    assert project.operation_plan.horizon_days == 7
    assert "花艺知识" in project.operation_plan.content_pillars
    assert "每条内容发布前做平台合规审核" in project.operation_plan.risk_controls
    assert project.content_calendar.start_date == "2026-05-25"
    assert project.content_calendar.end_date == "2026-05-31"
    assert len(project.content_tasks) == 3
    assert project.content_calendar.tasks == project.content_tasks
    assert [task.scheduled_date for task in project.content_tasks] == [
        "2026-05-25",
        "2026-05-28",
        "2026-05-31",
    ]
    assert all(task.platform == "xhs" for task in project.content_tasks)
    assert project.content_tasks[0].references[0]["keyword"] == "花艺"
    assert project.metadata["critic"]["status"] == "warn"
    assert project.metadata["critic"]["source"] == "rules"
    assert project.metadata["planner"] == "rule_fallback"
    assert "当前结果仍依赖规则兜底，应优先切换为 LLM 主线" in project.metadata["critic"]["issues"]


def test_operation_planner_accepts_dict_inputs_and_round_trips_project():
    project = plan_operation(
        _brief().to_dict(),
        _account_plan().to_dict(),
        start_date="2026-05-25",
        horizon_days=3,
        use_llm=False,
    )

    restored = AccountOperationProject.from_dict(project.to_dict())

    assert restored.to_dict() == project.to_dict()
    assert restored.operation_plan.horizon_days == 3
    assert len(restored.content_tasks) == 1
    assert restored.content_tasks[0].brief["brand_name"] == "春日花房"


def test_operation_planner_uses_llm_json_when_available(monkeypatch):
    def fake_chat(messages, *, usage="llm", **kwargs):
        assert usage == "llm"
        assert kwargs["response_format"] == {"type": "json_object"}
        assert "客户简报" in messages[1]["content"]
        return """
        {
          "operation_plan": {
            "objectives": ["验证社区花艺定位"],
            "content_pillars": ["节日场景", "花材养护"],
            "cadence": "7 天 2 条重点笔记",
            "kpi_targets": {"inquiries": 20},
            "milestones": [{"day": 3, "target": "完成第一条内容审核"}],
            "risk_controls": ["不承诺治疗效果"],
            "notes": ["先验证内容方向"]
          },
          "content_calendar": {
            "themes": ["母亲节预热"],
            "tasks": [
              {
                "title": "母亲节花别乱买",
                "day": 2,
                "content_type": "note",
                "topic": "母亲节花束搭配",
                "objective": "提升咨询",
                "priority": 1,
                "brief": {"cover_title": "母亲节花别乱买"},
                "required_assets": ["product_photo"],
                "notes": ["封面大字要清晰"]
              }
            ],
            "notes": ["任务等待内容生产桥接"]
          }
        }
        """

    monkeypatch.setattr(llms, "chat", fake_chat)

    project = OperationPlannerAgent(use_llm=True).run(
        _brief(),
        _account_plan(),
        start_date="2026-05-25",
        horizon_days=7,
    )

    assert project.operation_plan.objectives == ["验证社区花艺定位"]
    assert project.operation_plan.kpi_targets == {"inquiries": 20}
    assert project.operation_plan.milestones == [{"day": 3, "target": "完成第一条内容审核"}]
    assert project.content_calendar.themes == ["母亲节预热"]
    assert len(project.content_tasks) == 1
    assert project.content_tasks[0].scheduled_date == "2026-05-26"
    assert project.content_tasks[0].brief["cover_title"] == "母亲节花别乱买"
    assert project.metadata["planner"] == "llm_with_fallback"
    assert project.metadata["critic"]["status"] == "pass"
    assert not project.metadata["critic"]["issues"]


def test_operation_planner_llm_failure_keeps_fallback(monkeypatch):
    def fake_chat(messages, *, usage="llm", **kwargs):
        return "not json"

    monkeypatch.setattr(llms, "chat", fake_chat)

    project = OperationPlannerAgent(use_llm=True).run(
        _brief(),
        _account_plan(),
        start_date="2026-05-25",
        horizon_days=7,
    )

    assert project.metadata["planner"] == "rule_fallback"
    assert project.metadata["llm_error"]["stage"] == "operation_planner"
    assert project.metadata["llm_error"]["reason"] == "parse_error"
    assert len(project.content_tasks) == 3
    assert project.metadata["critic"]["status"] == "warn"
    assert "当前结果仍依赖规则兜底，应优先切换为 LLM 主线" in project.metadata["critic"]["issues"]
