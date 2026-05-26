"""Tests for CalendarPlanner pure policy helpers."""

from __future__ import annotations

from nori.core import KPIPlan, OperationPlan, ClientBrief

from datetime import date

from nori.context_building.calendar_planner import policy as calendar_plan_policy


def _operation_plan(horizon_days: int = 14, content_tasks: object = 0) -> OperationPlan:
    return OperationPlan(
        plan_id="plan_policy",
        horizon_days=horizon_days,
        objectives=["建立认知", "提升咨询"],
        content_pillars=["知识科普", "门店日常"],
        cadence="",
        kpi_targets={"content_tasks": content_tasks},
    )


def _kpi_plan(content_tasks: object = 0) -> KPIPlan:
    return KPIPlan(plan_id="kpi_policy", targets={"content_tasks": content_tasks})


def test_bounded_horizon_defaults_and_clamps_invalid_values():
    assert calendar_plan_policy.bounded_horizon(None) == 7
    assert calendar_plan_policy.bounded_horizon(True) == 7
    assert calendar_plan_policy.bounded_horizon(0) == 1
    assert calendar_plan_policy.bounded_horizon(120) == 90


def test_scheduled_dates_evenly_span_horizon_and_day_values_are_clamped():
    start = date(2026, 5, 25)

    dates = calendar_plan_policy.scheduled_dates(start, horizon_days=7, count=3)

    assert dates == [date(2026, 5, 25), date(2026, 5, 28), date(2026, 5, 31)]
    assert calendar_plan_policy.date_from_day(-5, start, horizon_days=7) == date(2026, 5, 25)
    assert calendar_plan_policy.date_from_day(99, start, horizon_days=7) == date(2026, 5, 31)


def test_task_count_prefers_kpi_then_operation_then_horizon_defaults():
    assert calendar_plan_policy.task_count_from_targets(_operation_plan(), _kpi_plan(5), 14) == 5
    assert calendar_plan_policy.task_count_from_targets(_operation_plan(content_tasks="4"), _kpi_plan(), 14) == 4
    assert calendar_plan_policy.task_count_from_targets(_operation_plan(content_tasks=12), _kpi_plan(), 14) == 7
    assert calendar_plan_policy.task_count_from_targets(_operation_plan(content_tasks=0), _kpi_plan(), 21) == 7
    assert calendar_plan_policy.task_count_from_targets(_operation_plan(content_tasks=0), _kpi_plan(), 7) == 3


def test_required_assets_prefers_deduped_material_types_with_safe_default():
    brief = ClientBrief(
        client_name="花店主理人",
        source_materials=[
            {"kind": "product_photo", "usage": "商品图"},
            {"type": "product_photo"},
            {"usage": "store_scene"},
            "bad",
        ],
    )

    assert calendar_plan_policy.required_assets(brief) == ["product_photo", "store_scene"]
    assert calendar_plan_policy.required_assets(ClientBrief()) == ["品牌基础信息", "可用图片素材"]


def test_topic_and_cadence_policy_use_brief_and_horizon_context():
    brief = ClientBrief(client_name="花店主理人", brand_name="春日花房")

    assert calendar_plan_policy.normalize_start_date("2026-05-25") == date(2026, 5, 25)
    assert calendar_plan_policy.calendar_id(date(2026, 5, 25), 14) == "cal_2026-05-25_14d"
    assert calendar_plan_policy.cadence_for_horizon(7) == "7 天内规划 3 条内容任务"
    assert calendar_plan_policy.cadence_for_horizon(30) == "每周 3 条内容任务"
    assert calendar_plan_policy.cadence_for_horizon(31) == "每周 3-5 条内容任务"
    assert calendar_plan_policy.topic_for_task("花艺知识", "建立认知", brief) == "春日花房花艺知识"
    assert calendar_plan_policy.objective_for_index(_operation_plan(), 3) == "提升咨询"
    assert calendar_plan_policy.short_brand(brief) == "春日花房"
