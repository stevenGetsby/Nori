from nori.core import ClientBrief
from nori.core import (
    AccountOperationProject,
    ContentCalendar,
    ContentTask,
    KPIPlan,
    OperationPlan,
)
from nori.agents.user_profiling.models import AccountPlanResult
from nori.agents.planning import planner_critics


def test_operation_project_critic_flags_missing_sections_and_fallback_source():
    project = AccountOperationProject(
        client_brief=ClientBrief(platform="dy"),
        operation_plan=OperationPlan(),
        content_calendar=ContentCalendar(),
        metadata={"planner": "rule_fallback"},
    )
    brief = ClientBrief(platform="xhs")
    account_plan = AccountPlanResult(
        tags={},
        recommended_positioning="社区花艺顾问",
        audience_profile=[],
        content_directions=[],
        benchmark_accounts={},
        unique_selling_points=[],
        ip_portrait_report={},
    )

    critic = planner_critics.critic_operation_project(project, brief, account_plan)

    assert critic["source"] == "rules"
    assert critic["status"] == "warn"
    assert critic["checks"]["objectives"] is False
    assert critic["checks"]["positioning_alignment"] is True
    assert "缺少运营目标" in critic["issues"]
    assert "平台与客户简报不一致" in critic["issues"]
    assert "当前结果仍依赖规则兜底，应优先切换为 LLM 主线" in critic["issues"]


def test_kpi_plan_critic_keeps_short_horizon_frequency_warning():
    plan = OperationPlan(horizon_days=7)
    kpi = KPIPlan(
        targets={"manual_metrics_check": "每周手动核验 1 次"},
        milestones=[{"day": 7, "target": "复盘"}],
        measurement_notes=["手动记录后台指标"],
        metadata={"planner": "rule_fallback"},
    )

    critic = planner_critics.critic_kpi_plan(kpi, plan)

    assert critic["status"] == "warn"
    assert critic["checks"] == {
        "targets": True,
        "milestones": True,
        "measurement_notes": True,
    }
    assert "7 天计划的核验频率过粗" in critic["issues"]
    assert "当前 KPI 仍依赖规则兜底，应优先切换为 LLM 主线" in critic["issues"]


def test_calendar_critic_checks_planned_status_briefs_and_kpi_task_count():
    plan = OperationPlan(horizon_days=7, content_pillars=["花艺知识"])
    kpi = KPIPlan(targets={"content_tasks": 2})
    calendar = ContentCalendar(
        start_date="2026-05-25",
        end_date="2026-05-31",
        themes=["门店日常"],
        tasks=[ContentTask(status="draft", brief={})],
        metadata={"planner": "rule_fallback"},
    )

    critic = planner_critics.critic_calendar(calendar, plan, kpi)

    assert critic["status"] == "warn"
    assert critic["checks"]["planned_status"] is False
    assert critic["checks"]["task_briefs"] is False
    assert "存在非 planned 状态任务" in critic["issues"]
    assert "存在缺少 brief 的任务" in critic["issues"]
    assert "任务数量少于 KPI 计划目标" in critic["issues"]
    assert "周期主题未覆盖运营计划内容支柱" in critic["issues"]
