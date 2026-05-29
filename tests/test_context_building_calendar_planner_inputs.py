"""Tests for CalendarPlanner input normalization helpers."""

from __future__ import annotations

from nori.core import AccountOperationProject
from nori.core import ContentCalendar, KPIPlan, OperationPlan, ClientBrief

from datetime import date

from nori.context_building.calendar_planner.package import CalendarPlannerInputPreparer


calendar_planner_inputs = CalendarPlannerInputPreparer()


def _brief() -> ClientBrief:
    return ClientBrief(client_name="花店主理人", brand_name="春日花房", goals=["建立本地认知"])


def _operation_plan() -> OperationPlan:
    return OperationPlan(
        plan_id="plan_7d",
        horizon_days=7,
        objectives=["建立本地认知"],
        content_pillars=["花艺知识"],
        kpi_targets={"content_tasks": 3},
    )


def _kpi_plan(content_tasks: int = 3) -> KPIPlan:
    return KPIPlan(plan_id="kpi_plan_7d", horizon_days=7, targets={"content_tasks": content_tasks})


def _calendar() -> ContentCalendar:
    return ContentCalendar(calendar_id="cal_existing", start_date="2026-05-25")


def test_normalize_inputs_accepts_project_and_preserves_embedded_models():
    project = AccountOperationProject(
        project_id="ops_001",
        client_brief=_brief(),
        operation_plan=_operation_plan(),
        kpi_plan=_kpi_plan(),
        content_calendar=_calendar(),
    )

    plan, kpi, brief, calendar = calendar_planner_inputs.normalize_inputs(project)

    assert plan is project.operation_plan
    assert kpi is project.kpi_plan
    assert brief is project.client_brief
    assert calendar is project.content_calendar


def test_normalize_inputs_accepts_project_with_explicit_overrides():
    project = AccountOperationProject(
        operation_plan=_operation_plan(),
        kpi_plan=_kpi_plan(),
        client_brief=_brief(),
        content_calendar=_calendar(),
    )
    override_kpi = _kpi_plan(content_tasks=2).to_dict()
    override_brief = ClientBrief(brand_name="夏日花房", goals=["预约咨询"]).to_dict()

    _, kpi, brief, calendar = calendar_planner_inputs.normalize_inputs(
        project,
        kpi_plan=override_kpi,
        client_brief=override_brief,
    )

    assert kpi.targets["content_tasks"] == 2
    assert brief.brand_name == "夏日花房"
    assert calendar is project.content_calendar


def test_normalize_inputs_restores_composite_dict_payloads():
    plan, kpi, brief, calendar = calendar_planner_inputs.normalize_inputs(
        {
            "operation_plan": _operation_plan().to_dict(),
            "kpi_plan": _kpi_plan(content_tasks=2).to_dict(),
            "client_brief": _brief().to_dict(),
            "content_calendar": _calendar().to_dict(),
        }
    )

    assert plan.plan_id == "plan_7d"
    assert kpi.targets["content_tasks"] == 2
    assert brief.brand_name == "春日花房"
    assert calendar.calendar_id == "cal_existing"
    assert calendar.start_date == "2026-05-25"


def test_normalize_model_helpers_restore_dicts_and_preserve_instances():
    kpi = _kpi_plan()
    brief = _brief()

    assert calendar_planner_inputs.normalize_kpi(kpi) is kpi
    assert calendar_planner_inputs.normalize_brief(brief) is brief
    assert calendar_planner_inputs.normalize_kpi(kpi.to_dict()).plan_id == "kpi_plan_7d"
    assert calendar_planner_inputs.normalize_brief(brief.to_dict()).brand_name == "春日花房"


def test_normalize_run_window_prefers_explicit_values_then_inherited_calendar():
    plan = _operation_plan()
    inherited = _calendar()

    start, days = calendar_planner_inputs.normalize_run_window(
        start_date=None,
        horizon_days=None,
        plan=plan,
        inherited_calendar=inherited,
    )

    assert start == date(2026, 5, 25)
    assert days == 7

    start, days = calendar_planner_inputs.normalize_run_window(
        start_date="2026-06-01",
        horizon_days=120,
        plan=plan,
        inherited_calendar=inherited,
    )

    assert start == date(2026, 6, 1)
    assert days == 90
