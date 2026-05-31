"""Tests for CalendarPlanner normalization helpers."""

from __future__ import annotations

from nori.core import ContentCalendar, ContentTask, KPIPlan, OperationPlan, ClientBrief

from datetime import date

from nori.agents.planning.calendar_planner import normalizer as calendar_plan_normalizer


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


def _operation_plan(horizon_days: int = 7) -> OperationPlan:
    return OperationPlan(
        plan_id="plan_7d",
        horizon_days=horizon_days,
        objectives=["建立本地认知", "提升到店咨询"],
        content_pillars=["花艺知识", "门店日常"],
        cadence="7 天内规划 3 条内容任务",
        kpi_targets={"content_tasks": 3},
        milestones=[{"day": 7, "target": "完成首周复盘"}],
    )


def _kpi_plan(content_tasks: int = 3) -> KPIPlan:
    return KPIPlan(
        plan_id="kpi_plan_7d",
        horizon_days=7,
        targets={"content_tasks": content_tasks, "review_pass_rate": ">= 90%"},
        milestones=[{"day": 7, "target": "核验内容产出"}],
        measurement_notes=["手动记录后台数据"],
    )


def test_fallback_calendar_builds_scheduled_planned_tasks():
    calendar = calendar_plan_normalizer.fallback_calendar(
        _operation_plan(),
        _kpi_plan(),
        _brief(),
        start_date=date(2026, 5, 25),
        horizon_days=7,
    )

    assert calendar.calendar_id == "cal_2026-05-25_7d"
    assert calendar.start_date == "2026-05-25"
    assert calendar.end_date == "2026-05-31"
    assert calendar.themes == ["花艺知识", "门店日常"]
    assert [task.scheduled_date for task in calendar.tasks] == [
        "2026-05-25",
        "2026-05-28",
        "2026-05-31",
    ]
    assert all(task.status == "planned" for task in calendar.tasks)
    assert calendar.tasks[0].brief["brand_name"] == "春日花房"
    assert calendar.tasks[0].required_assets == ["product_photo"]
    assert calendar.metadata["planner"] == "rule_fallback"
    assert calendar.metadata["source_plan_id"] == "plan_7d"
    assert calendar.metadata["source_kpi_plan_id"] == "kpi_plan_7d"


def test_merge_llm_calendar_normalizes_tasks_dates_and_metadata():
    fallback = calendar_plan_normalizer.fallback_calendar(
        _operation_plan(),
        _kpi_plan(),
        _brief(),
        start_date=date(2026, 5, 25),
        horizon_days=7,
    )
    data = {
        "themes": ["花艺知识", "节日场景", "   "],
        "cadence": "7 天 2 条重点笔记",
        "tasks": [
            {
                "title": "母亲节花别乱买",
                "day": 99,
                "content_type": "note",
                "topic": "母亲节花束搭配",
                "objective": "提升咨询",
                "priority": "2",
                "brief": {"cover_title": "母亲节花别乱买", "angle": "送礼避坑"},
                "required_assets": ["product_photo"],
                "notes": ["封面大字要清晰"],
            }
        ],
        "notes": ["等待内容生产桥接"],
    }

    calendar = calendar_plan_normalizer.merge_llm_calendar(
        data,
        fallback,
        _operation_plan(),
        _brief(),
        start_date=date(2026, 5, 25),
        horizon_days=7,
    )

    assert calendar.cadence == "7 天 2 条重点笔记"
    assert calendar.themes == ["花艺知识", "节日场景"]
    assert len(calendar.tasks) == 1
    assert calendar.tasks[0].scheduled_date == "2026-05-31"
    assert calendar.tasks[0].priority == 2
    assert calendar.tasks[0].brief["angle"] == "送礼避坑"
    assert calendar.tasks[0].brief["content_pillar"] == "花艺知识"
    assert calendar.notes == ["等待内容生产桥接"]
    assert calendar.metadata == {
        "planner": "llm_with_fallback",
        "source_plan_id": "plan_7d",
        "source_kpi_plan_id": "kpi_plan_7d",
        "horizon_days": 7,
        "theme_count": 2,
    }


def test_merge_llm_calendar_falls_back_for_invalid_tasks_and_empty_lists():
    fallback = ContentCalendar(
        calendar_id="cal_2026-05-25_7d",
        start_date="2026-05-25",
        end_date="2026-05-31",
        cadence="fallback cadence",
        themes=["fallback theme"],
        tasks=[
            ContentTask(
                task_id="task_d01_01",
                title="fallback task",
                scheduled_date="2026-05-25",
                status="planned",
                brief={"content_pillar": "fallback"},
            )
        ],
        notes=["fallback note"],
        metadata={"planner": "rule_fallback"},
    )

    calendar = calendar_plan_normalizer.merge_llm_calendar(
        {"themes": [], "tasks": ["bad"], "notes": []},
        fallback,
        _operation_plan(),
        _brief(),
        start_date=date(2026, 5, 25),
        horizon_days=7,
    )

    assert calendar.themes == fallback.themes
    assert calendar.tasks == fallback.tasks
    assert calendar.notes == fallback.notes
