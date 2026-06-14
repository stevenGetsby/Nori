from nori.core import AccountOperationProject
from nori.core import ContentTask, KPIPlan, OperationPlan, ClientBrief
import importlib
import json

import nori.core.llms as llms

from nori.agents.planning import KPIPlannerAgent, plan_kpi


kpi_module = importlib.import_module("nori.agents.planning.kpi_planner.kpi_planner")


def _operation_plan():
    return OperationPlan(
        plan_id="plan_7d",
        horizon_days=7,
        objectives=["建立本地认知"],
        content_pillars=["花艺知识"],
        cadence="7 天内规划 3 条内容任务",
        kpi_targets={"followers": 50},
        milestones=[{"day": 7, "target": "完成首周复盘"}],
    )


def test_kpi_planner_rule_fallback_from_operation_plan():
    kpi = KPIPlannerAgent(use_llm=False).run(_operation_plan())

    assert isinstance(kpi, KPIPlan)
    assert kpi.plan_id == "kpi_plan_7d"
    assert kpi.horizon_days == 7
    assert kpi.targets["followers"] == 50
    assert kpi.targets["content_tasks"] == 3
    assert kpi.targets["review_pass_rate"] == ">= 90%"
    assert kpi.milestones == [{"day": 7, "target": "完成首周复盘"}]
    assert kpi.metadata["planner"] == "rule_fallback"
    assert kpi.metadata["critic"]["status"] == "warn"
    assert "当前 KPI 仍依赖规则兜底，应优先切换为 LLM 主线" in kpi.metadata["critic"]["issues"]


def test_kpi_planner_uses_project_task_count_as_target():
    project = AccountOperationProject(
        project_id="ops_001",
        name="春日花房账号代运营",
        client_brief=ClientBrief(brand_name="春日花房"),
        operation_plan=_operation_plan(),
        content_tasks=[
            ContentTask(task_id="task_1"),
            ContentTask(task_id="task_2"),
            ContentTask(task_id="task_3"),
            ContentTask(task_id="task_4"),
        ],
    )

    kpi = plan_kpi(project, use_llm=False)

    assert kpi.targets["content_tasks"] == 4
    assert kpi.metadata["source_plan_id"] == "plan_7d"
    assert kpi.metadata["critic"]["status"] == "warn"
    assert "当前 KPI 仍依赖规则兜底，应优先切换为 LLM 主线" in kpi.metadata["critic"]["issues"]


def test_kpi_planner_accepts_dict_inputs():
    kpi = KPIPlannerAgent(use_llm=False).run({"operation_plan": _operation_plan().to_dict(), "project_id": "ops_001"})

    restored = KPIPlan.from_dict(kpi.to_dict())

    assert restored.to_dict() == kpi.to_dict()
    assert restored.plan_id == "kpi_plan_7d"


def test_kpi_planner_uses_llm_json_when_available(monkeypatch):
    def fake_chat_json(messages, *, usage="llm", **kwargs):
        assert usage == "llm"
        assert kwargs["json_mode"] is True
        assert "运营计划" in messages[1]["content"]
        return json.loads("""
        {
          "targets": {
            "content_tasks": 4,
            "profile_visits": 120,
            "manual_metrics_check": "第 7 天核验"
          },
          "milestones": [
            {"day": 1, "target": "记录账号当前粉丝基线"},
            {"day": 7, "target": "核验主页访问和咨询"}
          ],
          "measurement_notes": ["手动记录小红书后台数据", "不做自动抓取"]
        }
        """)

    monkeypatch.setattr(llms, "chat_json", fake_chat_json)

    kpi = KPIPlannerAgent(use_llm=True).run(_operation_plan())

    assert kpi.targets["profile_visits"] == 120
    assert kpi.targets["content_tasks"] == 4
    assert kpi.milestones[-1] == {"day": 7, "target": "核验主页访问和咨询"}
    assert kpi.measurement_notes == ["手动记录小红书后台数据", "不做自动抓取"]
    assert kpi.metadata["planner"] == "llm_with_fallback"
    assert kpi.metadata["critic"]["status"] == "pass"


def test_kpi_planner_llm_failure_keeps_fallback(monkeypatch):
    def fake_chat_json(messages, *, usage="llm", **kwargs):
        raise llms.ChatJSONError("bad json", "not json")

    monkeypatch.setattr(llms, "chat_json", fake_chat_json)

    kpi = KPIPlannerAgent(use_llm=True).run(_operation_plan())

    assert kpi.metadata["planner"] == "rule_fallback"
    assert kpi.metadata["llm_error"]["stage"] == "kpi_planner"
    assert kpi.metadata["llm_error"]["reason"] == "parse_error"
    assert kpi.targets["content_tasks"] == 3
    assert kpi.metadata["critic"]["status"] == "warn"
