"""Class-owned package contract for CalendarPlannerAgent."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any

from nori.core import (
    AccountOperationProject,
    AgentInputPreparer,
    AgentPromptBuilder,
    ClientBrief,
    ContentCalendar,
    KPIPlan,
    OperationPlan,
)
from nori.shared.normalization import mapping
from nori.shared.prompting import json_prompt

from .policy import bounded_horizon, normalize_start_date


@dataclass(frozen=True)
class PreparedCalendarPlannerInput:
    operation_plan: OperationPlan
    kpi_plan: KPIPlan
    client_brief: ClientBrief
    inherited_calendar: ContentCalendar
    start_date: date
    horizon_days: int


class CalendarPlannerInputPreparer(AgentInputPreparer):
    """Restore calendar inputs, optional overrides, and run window."""

    def prepare(
        self,
        value: OperationPlan | AccountOperationProject | dict[str, Any] | None,
        *,
        kpi_plan: KPIPlan | dict[str, Any] | None = None,
        client_brief: ClientBrief | dict[str, Any] | None = None,
        start_date: str | date | None = None,
        horizon_days: int | None = None,
    ) -> PreparedCalendarPlannerInput:
        plan, kpi, brief, inherited_calendar = self.normalize_inputs(
            value,
            kpi_plan=kpi_plan,
            client_brief=client_brief,
        )
        start, days = self.normalize_run_window(
            start_date=start_date,
            horizon_days=horizon_days,
            plan=plan,
            inherited_calendar=inherited_calendar,
        )
        return PreparedCalendarPlannerInput(
            operation_plan=plan,
            kpi_plan=kpi,
            client_brief=brief,
            inherited_calendar=inherited_calendar,
            start_date=start,
            horizon_days=days,
        )

    def normalize_inputs(
        self,
        value: OperationPlan | AccountOperationProject | dict[str, Any] | None,
        *,
        kpi_plan: KPIPlan | dict[str, Any] | None = None,
        client_brief: ClientBrief | dict[str, Any] | None = None,
    ) -> tuple[OperationPlan, KPIPlan, ClientBrief, ContentCalendar]:
        if isinstance(value, AccountOperationProject):
            return (
                value.operation_plan,
                self.normalize_kpi(kpi_plan) if kpi_plan is not None else value.kpi_plan,
                self.normalize_brief(client_brief) if client_brief is not None else value.client_brief,
                value.content_calendar,
            )
        if isinstance(value, OperationPlan):
            return value, self.normalize_kpi(kpi_plan), self.normalize_brief(client_brief), ContentCalendar()
        data = mapping(value)
        if "operation_plan" in data and isinstance(data.get("operation_plan"), dict):
            return (
                OperationPlan.from_dict(data.get("operation_plan")),
                self.normalize_kpi(kpi_plan or data.get("kpi_plan")),
                self.normalize_brief(client_brief or data.get("client_brief")),
                ContentCalendar.from_dict(data.get("content_calendar")),
            )
        return OperationPlan.from_dict(data), self.normalize_kpi(kpi_plan), self.normalize_brief(client_brief), ContentCalendar()

    def normalize_kpi(self, value: KPIPlan | dict[str, Any] | None) -> KPIPlan:
        if isinstance(value, KPIPlan):
            return value
        return KPIPlan.from_dict(value if isinstance(value, dict) else {})

    def normalize_brief(self, value: ClientBrief | dict[str, Any] | None) -> ClientBrief:
        if isinstance(value, ClientBrief):
            return value
        return ClientBrief.from_dict(value if isinstance(value, dict) else {})

    def normalize_run_window(
        self,
        *,
        start_date: str | date | None,
        horizon_days: int | None,
        plan: OperationPlan,
        inherited_calendar: ContentCalendar,
    ) -> tuple[date, int]:
        days = bounded_horizon(horizon_days or plan.horizon_days)
        start = normalize_start_date(start_date or inherited_calendar.start_date)
        return start, days


class CalendarPlannerPromptBuilder(AgentPromptBuilder):
    system_prompt = "你是 Nori 的账号代运营排期规划器，只输出 JSON。"

    user_prompt_template = """\
根据运营计划、KPI 计划和客户上下文，生成可交给内容生产链路的内容排期。

运营计划：
{operation_plan}

KPI 计划：
{kpi_plan}

客户上下文：
{client_context}

计划要求：
- 只规划 {horizon_days} 天，从 {start_date} 开始。
- 不要安排真实发布、自动互动、自动抓取数据等未实现能力。
- 每个任务后续要能交给 ContentTask -> NoteMakerAgent -> CoverDirectorAgent。
- 任务状态必须保持 planned。
- 输出任务数量要服务 KPI，但不要超过 7 条。

输出 JSON，字段固定：
{{
  "themes": ["本周期主题，1-4 条"],
  "cadence": "制作/排期节奏",
  "tasks": [
    {{
      "title": "任务标题",
      "day": 1,
      "content_type": "note",
      "topic": "内容主题",
      "objective": "本条内容目标",
      "priority": 1,
      "brief": {{
        "cover_title": "封面标题建议",
        "content_pillar": "对应内容支柱",
        "angle": "切入角度"
      }},
      "required_assets": ["需要的素材类型"],
      "notes": ["制作注意事项"]
    }}
  ],
  "notes": ["排期说明，可为空"]
}}
"""

    def build_user_prompt(
        self,
        plan: OperationPlan,
        kpi: KPIPlan,
        brief: ClientBrief,
        *,
        start_date: date,
        horizon_days: int,
    ) -> str:
        return self.user_prompt_template.format(
            operation_plan=json_prompt(plan.to_dict()),
            kpi_plan=json_prompt(kpi.to_dict()),
            client_context=json_prompt(brief.to_dict()),
            start_date=start_date.isoformat(),
            horizon_days=horizon_days,
        )


__all__ = [
    "CalendarPlannerInputPreparer",
    "CalendarPlannerPromptBuilder",
    "PreparedCalendarPlannerInput",
]
