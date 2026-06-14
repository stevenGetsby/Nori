"""Tests for CalendarPlanner content-task construction helpers."""

from __future__ import annotations

from nori.core import ContentTask, KPIPlan, OperationPlan, ClientBrief

from datetime import date

from nori.agents.planning.calendar_planner import task_builder as calendar_task_builder


def _brief() -> ClientBrief:
    return ClientBrief(
        client_name="花店主理人",
        brand_name="春日花房",
        platform="xhs",
        goals=["建立本地认知", "提升到店咨询"],
        audience=["周边 3 公里年轻家庭"],
        positioning_notes=["社区花艺顾问"],
        source_materials=[{"kind": "product_photo", "usage": "商品图"}],
    )


def _operation_plan() -> OperationPlan:
    return OperationPlan(
        plan_id="plan_7d",
        horizon_days=7,
        objectives=["建立本地认知", "提升到店咨询"],
        content_pillars=["花艺知识", "门店日常"],
        cadence="7 天内规划 3 条内容任务",
        kpi_targets={"content_tasks": 3},
    )


def _kpi_plan(content_tasks: int = 3) -> KPIPlan:
    return KPIPlan(plan_id="kpi_plan_7d", targets={"content_tasks": content_tasks})


def test_fallback_tasks_build_scheduled_content_tasks():
    tasks = calendar_task_builder.fallback_tasks(
        _operation_plan(),
        _kpi_plan(),
        _brief(),
        start_date=date(2026, 5, 25),
        horizon_days=7,
    )

    assert [task.task_id for task in tasks] == ["task_d01_01", "task_d04_02", "task_d07_03"]
    assert [task.scheduled_date for task in tasks] == ["2026-05-25", "2026-05-28", "2026-05-31"]
    assert tasks[0].title == "春日花房花艺知识｜春日花房"
    assert tasks[0].brief["brand_name"] == "春日花房"
    assert tasks[0].brief["content_pillar"] == "花艺知识"
    assert tasks[0].required_assets == ["product_photo"]
    assert all(task.metadata["source"] == "calendar_planner_fallback" for task in tasks)


def test_tasks_from_llm_normalizes_rows_and_adds_missing_content_pillar():
    tasks = calendar_task_builder.tasks_from_llm(
        [
            {
                "title": "母亲节花别乱买",
                "day": 99,
                "content_type": "note",
                "topic": "母亲节花束搭配",
                "priority": "2",
                "brief": {"cover_title": "母亲节花别乱买", "angle": "送礼避坑"},
                "required_assets": ["product_photo", ""],
                "notes": ["封面大字要清晰"],
            }
        ],
        [],
        _operation_plan(),
        _brief(),
        start_date=date(2026, 5, 25),
        horizon_days=7,
    )

    assert len(tasks) == 1
    assert tasks[0].task_id == "task_d07_01"
    assert tasks[0].scheduled_date == "2026-05-31"
    assert tasks[0].priority == 2
    assert tasks[0].topic == "母亲节花束搭配"
    assert tasks[0].objective == "建立本地认知"
    assert tasks[0].brief["angle"] == "送礼避坑"
    assert tasks[0].brief["content_pillar"] == "花艺知识"
    assert tasks[0].required_assets == ["product_photo"]
    assert tasks[0].metadata["source"] == "calendar_planner_llm"


def test_tasks_from_llm_falls_back_when_rows_are_invalid():
    fallback = [ContentTask(task_id="task_d01_01", title="fallback task")]

    assert (
        calendar_task_builder.tasks_from_llm(
            ["bad", {"title": "   ", "topic": ""}],
            fallback,
            _operation_plan(),
            _brief(),
            start_date=date(2026, 5, 25),
            horizon_days=7,
        )
        == fallback
    )
