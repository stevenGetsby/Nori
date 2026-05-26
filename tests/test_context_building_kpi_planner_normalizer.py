"""Tests for KPIPlanner normalization helpers."""

from __future__ import annotations

from nori.core import KPIPlan, OperationPlan

from nori.context_building.kpi_planner import normalizer as kpi_plan_normalizer


def _operation_plan(horizon_days: int = 7) -> OperationPlan:
    return OperationPlan(
        plan_id="plan_7d",
        horizon_days=horizon_days,
        objectives=["建立本地认知"],
        content_pillars=["花艺知识"],
        cadence="7 天内规划 3 条内容任务",
        kpi_targets={"followers": 50},
        milestones=[{"day": horizon_days, "target": "完成周期复盘"}],
    )


def test_fallback_kpi_plan_uses_operation_targets_and_project_task_count():
    plan = _operation_plan()

    kpi = kpi_plan_normalizer.fallback_kpi_plan(plan, {"content_task_count": 4})

    assert kpi.plan_id == "kpi_plan_7d"
    assert kpi.horizon_days == 7
    assert kpi.targets["followers"] == 50
    assert kpi.targets["content_tasks"] == 4
    assert kpi.targets["review_pass_rate"] == ">= 90%"
    assert kpi.targets["manual_metrics_check"] == "周期结束手动核验 1 次"
    assert kpi.targets["cycle_review"] == "完成 1 次周期复盘"
    assert kpi.milestones == [{"day": 7, "target": "完成周期复盘"}]
    assert kpi.metadata == {"planner": "rule_fallback", "source_plan_id": "plan_7d"}


def test_merge_llm_kpi_plan_normalizes_targets_milestones_notes_and_metadata():
    fallback = KPIPlan(
        plan_id="kpi_plan_7d",
        horizon_days=7,
        targets={"content_tasks": 3},
        milestones=[{"day": 7, "target": "fallback"}],
        measurement_notes=["fallback note"],
        metadata={"planner": "rule_fallback", "source_plan_id": "plan_7d"},
    )
    data = {
        "targets": {"content_tasks": 4, "profile_visits": 120},
        "milestones": [{"day": 99, "target": "核验主页访问"}],
        "measurement_notes": ["手动记录后台数据", "不做自动抓取", "多余1", "多余2", "多余3", "多余4"],
    }

    kpi = kpi_plan_normalizer.merge_llm_kpi_plan(data, fallback, _operation_plan())

    assert kpi.targets == {"content_tasks": 4, "profile_visits": 120}
    assert kpi.milestones == [{"day": 7, "target": "核验主页访问"}]
    assert kpi.measurement_notes == ["手动记录后台数据", "不做自动抓取", "多余1", "多余2", "多余3"]
    assert kpi.metadata == {"planner": "llm_with_fallback", "source_plan_id": "plan_7d"}


def test_merge_llm_kpi_plan_falls_back_for_invalid_sections():
    fallback = kpi_plan_normalizer.fallback_kpi_plan(_operation_plan(), {})

    kpi = kpi_plan_normalizer.merge_llm_kpi_plan(
        {"targets": "bad", "milestones": "bad", "measurement_notes": []},
        fallback,
        _operation_plan(),
    )

    assert kpi.targets == fallback.targets
    assert kpi.milestones == fallback.milestones
    assert kpi.measurement_notes == fallback.measurement_notes
