"""Tests for OperationPlanner deterministic project builder."""

from __future__ import annotations

from nori.core import AccountOperationProject
from nori.core import ClientBrief

from datetime import date

from nori.user_profiling.models import AccountPlanResult
from nori.context_building.operation_planner import project_builder as operation_project_builder


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
        benchmark_accounts={"search_keywords": ["花艺", "节日花束", "社区花店"]},
        unique_selling_points=["本地配送快", "审美稳定"],
        ip_portrait_report={
            "content_pillars": [
                {"name": "花艺知识", "description": "花材养护和搭配"},
                {"name": "门店日常", "description": "真实经营细节"},
            ]
        },
    )


def test_fallback_project_builds_planning_project_calendar_tasks_and_kpi():
    project = operation_project_builder.fallback_project(
        _brief(),
        _account_plan(),
        project_id="ops_001",
        project_name="",
        start_date=date(2026, 5, 25),
        horizon_days=7,
    )

    assert isinstance(project, AccountOperationProject)
    assert project.project_id == "ops_001"
    assert project.name == "春日花房账号代运营"
    assert project.status == "planning"
    assert project.operation_plan.plan_id == "plan_7d"
    assert project.operation_plan.content_pillars[:2] == ["花艺知识", "门店日常"]
    assert "每条内容发布前做平台合规审核" in project.operation_plan.risk_controls
    assert project.kpi_plan.targets == {"content_tasks": 3, "review_pass_rate": ">= 90%"}
    assert project.content_calendar.calendar_id == "cal_2026-05-25_7d"
    assert project.content_calendar.tasks == project.content_tasks
    assert [task.scheduled_date for task in project.content_tasks] == [
        "2026-05-25",
        "2026-05-28",
        "2026-05-31",
    ]
    assert project.content_tasks[0].references[0] == {"source": "account_plan_keyword", "keyword": "花艺"}
    assert project.content_tasks[0].required_assets == ["product_photo"]
    assert project.metadata == {"planner": "rule_fallback"}


def test_fallback_project_uses_safe_defaults_without_account_plan_or_brand():
    brief = ClientBrief(client_name="", brand_name="", goals=[], positioning_notes=[], source_materials=[])

    project = operation_project_builder.fallback_project(
        brief,
        None,
        project_id="",
        project_name="Custom Project",
        start_date=date(2026, 5, 25),
        horizon_days=3,
    )

    assert project.project_id == "ops_local"
    assert project.name == "Custom Project"
    assert project.operation_plan.objectives == ["建立账号基础认知", "沉淀可复用内容方向"]
    assert project.operation_plan.content_pillars == ["账号定位", "产品价值", "用户场景"]
    assert len(project.content_tasks) == 1
    assert project.content_tasks[0].required_assets == ["品牌基础信息", "可用图片素材"]
    assert project.account_positioning.positioning_id == ""
