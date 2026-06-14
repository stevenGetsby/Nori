"""Tests for OperationPlanner deterministic policy helpers."""

from __future__ import annotations

from nori.core import OperationPlan, ClientBrief

from nori.agents.user_profiling.schemas import AccountPlanResult
from nori.agents.planning.operation_planner import project_policy as operation_project_policy


def _brief() -> ClientBrief:
    return ClientBrief(
        client_name="花店主理人",
        brand_name="春日花房",
        goals=["建立本地认知", "提升到店咨询"],
        positioning_notes=["社区花艺顾问"],
        constraints=["不夸大疗效"],
        taboos=["价格欺骗", "虚构库存"],
        source_materials=[{"kind": "product_photo"}, {"usage": "store_scene"}],
    )


def _account_plan() -> AccountPlanResult:
    return AccountPlanResult(
        tags={"track": "花艺", "goal": "获客", "platform": "小红书", "product": "花束", "positioning": "社区花艺"},
        recommended_positioning="懂生活的社区花艺顾问",
        audience_profile=["周边 3 公里年轻家庭"],
        content_directions=["节日花束搭配", "门店日常", "花材养护"],
        unique_selling_points=["本地配送快", "审美稳定"],
        benchmark_accounts={"search_keywords": ["花艺", "节日花束", "社区花店", "多余"]},
        ip_portrait_report={
            "content_pillars": [
                {"name": "花艺知识", "description": "花材养护和搭配"},
                {"description": "真实经营细节"},
            ]
        },
    )


def test_content_pillars_objectives_and_topics_prefer_account_plan_context():
    pillars = operation_project_policy.content_pillars(_brief(), _account_plan())
    objectives = operation_project_policy.objectives_for_plan(_brief(), _account_plan())
    topics = operation_project_policy.topic_pool(_brief(), _account_plan(), pillars)

    assert pillars[:4] == ["花艺知识", "真实经营细节", "节日花束搭配", "门店日常"]
    assert objectives == ["建立本地认知", "提升到店咨询", "验证定位：懂生活的社区花艺顾问", "本地配送快"]
    assert topics[:4] == ["节日花束搭配", "门店日常", "花材养护", "本地配送快"]
    assert topics[-1] == "春日花房账号定位"


def test_policy_defaults_are_safe_without_account_plan_or_brand():
    brief = ClientBrief(client_name="", brand_name="", goals=[], positioning_notes=[])

    assert operation_project_policy.content_pillars(brief, None) == ["账号定位", "产品价值", "用户场景"]
    assert operation_project_policy.objectives_for_plan(brief, None) == ["建立账号基础认知", "沉淀可复用内容方向"]
    assert operation_project_policy.topic_pool(brief, None, []) == ["账号定位", "用户痛点", "产品价值"]
    assert operation_project_policy.project_title(brief) == "Nori账号代运营"
    assert operation_project_policy.stable_id("ops", "!!!") == "ops_local"


def test_risk_controls_references_and_required_assets_are_bounded():
    controls = operation_project_policy.risk_controls_for_brief(_brief())
    references = operation_project_policy.task_references(_account_plan())

    assert controls == [
        "每条内容发布前做平台合规审核",
        "封面和正文保持同一主题",
        "避免：价格欺骗",
        "避免：虚构库存",
        "不夸大疗效",
    ]
    assert references == [
        {"source": "account_plan_keyword", "keyword": "花艺"},
        {"source": "account_plan_keyword", "keyword": "节日花束"},
        {"source": "account_plan_keyword", "keyword": "社区花店"},
    ]
    assert operation_project_policy.required_assets(_brief()) == ["product_photo", "store_scene"]


def test_default_milestones_and_derived_kpi_plan_follow_operation_plan():
    operation_plan = OperationPlan(
        plan_id="plan_14d",
        horizon_days=14,
        kpi_targets={"content_tasks": 3},
        milestones=[{"day": 14, "target": "复盘"}],
    )

    assert operation_project_policy.default_milestones(14) == [
        {"day": 1, "target": "确认账号定位与本周期内容支柱"},
        {"day": 7, "target": "完成首批内容任务制作与审核"},
        {"day": 14, "target": "复盘本周期内容产出并准备下一轮选题"},
    ]
    kpi = operation_project_policy.kpi_plan_from_operation(operation_plan)
    assert kpi.plan_id == "kpi_plan_14d"
    assert kpi.targets == {"content_tasks": 3}
    assert kpi.milestones == [{"day": 14, "target": "复盘"}]
    assert kpi.metadata == {"source": "operation_plan"}
