from __future__ import annotations

from nori.core import KPIPlan, OperationPlan, ClientBrief
import os

import pytest

import llms
from nori.agents.user_profiling.models import AccountPlanResult
from nori.agents.planning import CalendarPlannerAgent, KPIPlannerAgent, OperationPlannerAgent


LIVE_GHC = os.getenv("NORI_LIVE_GHC") == "1"
pytestmark = pytest.mark.skipif(not LIVE_GHC, reason="live ghc smoke disabled")


def _brief() -> ClientBrief:
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


def _account_plan() -> AccountPlanResult:
    return AccountPlanResult(
        tags={"track": "花艺", "goal": "获客", "platform": "小红书", "product": "花束", "positioning": "社区花艺"},
        recommended_positioning="懂生活的社区花艺顾问",
        audience_profile=["周边 3 公里年轻家庭"],
        content_directions=["节日花束搭配", "门店日常"],
        benchmark_accounts={"search_keywords": ["花艺", "花束"], "keyword_levels": [], "accounts": [], "search_results": []},
        unique_selling_points=["本地配送快"],
        ip_portrait_report={"content_pillars": [{"name": "花艺知识", "description": "花材养护"}]},
    )


def _operation_plan() -> OperationPlan:
    return OperationPlan(
        plan_id="plan_7d",
        horizon_days=7,
        objectives=["建立本地认知"],
        content_pillars=["花艺知识"],
        cadence="7 天内规划 3 条内容任务",
        kpi_targets={"followers": 50},
        milestones=[{"day": 7, "target": "完成首周复盘"}],
        risk_controls=["平台合规审核"],
    )


def _kpi_plan() -> KPIPlan:
    return KPIPlan(
        plan_id="kpi_plan_7d",
        horizon_days=7,
        targets={"content_tasks": 2, "review_pass_rate": ">= 90%"},
        milestones=[{"day": 7, "target": "核验首周内容产出"}],
        measurement_notes=["手动记录平台后台数据"],
    )


def test_operation_planner_ghc_smoke():
    llms.set_mode("ghc")
    llms.ensure_ready("llm", timeout=10)

    project = OperationPlannerAgent(use_llm=True).run(
        _brief(),
        _account_plan(),
        project_id="ops_live",
        start_date="2026-05-25",
        horizon_days=7,
    )

    assert project.operation_plan.objectives
    assert project.content_tasks
    assert project.metadata["critic"]["source"] == "rules"


def test_kpi_planner_ghc_smoke():
    llms.set_mode("ghc")
    llms.ensure_ready("llm", timeout=10)

    kpi = KPIPlannerAgent(use_llm=True).run(_operation_plan())

    assert kpi.targets
    assert kpi.metadata["critic"]["source"] == "rules"


def test_calendar_planner_ghc_smoke():
    llms.set_mode("ghc")
    llms.ensure_ready("llm", timeout=10)

    calendar = CalendarPlannerAgent(use_llm=True).run(
        _operation_plan(),
        kpi_plan=_kpi_plan(),
        client_brief=_brief(),
        start_date="2026-05-25",
    )

    assert calendar.tasks
    assert calendar.metadata["critic"]["source"] == "rules"
