"""Tests for KPIPlanner input normalization helpers."""

from __future__ import annotations

from nori.core import AccountOperationProject
from nori.core import ContentTask, OperationPlan, ClientBrief

from nori.context_building.kpi_planner.package import KPIPlannerInputPreparer


kpi_planner_inputs = KPIPlannerInputPreparer()


def _operation_plan() -> OperationPlan:
    return OperationPlan(plan_id="plan_7d", horizon_days=7, objectives=["建立认知"])


def test_normalize_plan_and_context_accepts_project_and_merges_overrides():
    project = AccountOperationProject(
        project_id="ops_001",
        name="春日花房代运营",
        client_brief=ClientBrief(brand_name="春日花房"),
        operation_plan=_operation_plan(),
        content_tasks=[ContentTask(task_id="task_1"), ContentTask(task_id="task_2")],
    )

    plan, context = kpi_planner_inputs.normalize_plan_and_context(
        project,
        {"content_task_count": 4, "extra": "value"},
    )

    assert plan is project.operation_plan
    assert context["project_id"] == "ops_001"
    assert context["project_name"] == "春日花房代运营"
    assert context["client_brief"]["brand_name"] == "春日花房"
    assert context["content_task_count"] == 4
    assert context["extra"] == "value"


def test_normalize_plan_and_context_accepts_operation_plan_instance():
    plan = _operation_plan()

    restored, context = kpi_planner_inputs.normalize_plan_and_context(plan, {"project_id": "ops_002"})

    assert restored is plan
    assert context == {"project_id": "ops_002"}


def test_normalize_plan_and_context_restores_composite_dict_payload():
    plan, context = kpi_planner_inputs.normalize_plan_and_context(
        {
            "operation_plan": _operation_plan().to_dict(),
            "project_id": "ops_003",
            "name": "项目名称",
            "client_brief": {"brand_name": "春日花房"},
        },
        {"extra": "value"},
    )

    assert plan.plan_id == "plan_7d"
    assert context == {
        "project_id": "ops_003",
        "name": "项目名称",
        "client_brief": {"brand_name": "春日花房"},
        "extra": "value",
    }
