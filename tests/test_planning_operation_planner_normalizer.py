"""Tests for OperationPlanner LLM output normalization helpers."""

from __future__ import annotations

from nori.core import ClientBrief

from datetime import date

from nori.agents.planning.operation_planner import normalizer as operation_plan_normalizer
from nori.agents.planning.operation_planner.project_builder import fallback_project


def _brief() -> ClientBrief:
    return ClientBrief(
        client_name="花店主理人",
        brand_name="春日花房",
        platform="xhs",
        goals=["建立本地认知"],
        audience=["周边年轻家庭"],
        positioning_notes=["社区花艺顾问"],
        source_materials=[{"kind": "product_photo", "usage": "商品图"}],
    )


def _fallback():
    return fallback_project(
        _brief(),
        None,
        project_id="ops_001",
        project_name="",
        start_date=date(2026, 5, 25),
        horizon_days=7,
    )


def test_merge_llm_project_normalizes_plan_calendar_tasks_and_metadata():
    data = {
        "operation_plan": {
            "objectives": ["验证社区花艺定位"],
            "content_pillars": ["节日场景", "花材养护"],
            "cadence": "7 天 2 条重点笔记",
            "kpi_targets": {"inquiries": 20},
            "milestones": [{"day": 99, "target": "完成内容审核"}],
            "risk_controls": ["不承诺治疗效果"],
            "notes": ["先验证内容方向"],
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
                    "priority": "3",
                    "brief": {"cover_title": "母亲节花别乱买"},
                    "required_assets": ["product_photo"],
                    "notes": ["封面大字要清晰"],
                }
            ],
            "notes": ["任务等待内容生产桥接"],
        },
    }

    project = operation_plan_normalizer.merge_llm_project(
        data,
        _fallback(),
        start_date=date(2026, 5, 25),
        horizon_days=7,
    )

    assert project.project_id == "ops_001"
    assert project.operation_plan.objectives == ["验证社区花艺定位"]
    assert project.operation_plan.kpi_targets == {"inquiries": 20}
    assert project.operation_plan.milestones == [{"day": 7, "target": "完成内容审核"}]
    assert project.kpi_plan.targets == {"inquiries": 20}
    assert project.content_calendar.themes == ["母亲节预热"]
    assert project.content_calendar.cadence == "7 天 2 条重点笔记"
    assert project.content_tasks[0].task_id == "task_d02_01"
    assert project.content_tasks[0].scheduled_date == "2026-05-26"
    assert project.content_tasks[0].priority == 3
    assert project.content_tasks[0].metadata == {"source": "operation_planner_llm"}
    assert project.metadata["planner"] == "llm_with_fallback"


def test_merge_llm_project_falls_back_to_existing_tasks_when_llm_tasks_invalid():
    data = {
        "operation_plan": {"objectives": ["新目标"]},
        "content_calendar": {"tasks": [{"title": "", "topic": ""}, "bad"]},
    }
    fallback = _fallback()

    project = operation_plan_normalizer.merge_llm_project(
        data,
        fallback,
        start_date=date(2026, 5, 25),
        horizon_days=7,
    )

    assert project.operation_plan.objectives == ["新目标"]
    assert project.content_tasks == fallback.content_tasks
    assert project.content_calendar.tasks == fallback.content_tasks
