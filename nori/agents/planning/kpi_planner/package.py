"""Class-owned package contract for KPIPlannerAgent."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from nori.core import AccountOperationProject, AgentInputPreparer, AgentPromptBuilder, OperationPlan
from nori.shared.normalization import mapping
from nori.shared.prompting import json_prompt


@dataclass(frozen=True)
class PreparedKPIPlannerInput:
    operation_plan: OperationPlan
    project_context: dict[str, Any]


class KPIPlannerInputPreparer(AgentInputPreparer):
    """Restore operation-plan inputs and derived project context."""

    def prepare(
        self,
        value: OperationPlan | AccountOperationProject | dict[str, Any] | None,
        project_context: dict[str, Any] | None,
    ) -> PreparedKPIPlannerInput:
        plan, context = self.normalize_plan_and_context(value, project_context)
        return PreparedKPIPlannerInput(operation_plan=plan, project_context=context)

    def normalize_plan_and_context(
        self,
        value: OperationPlan | AccountOperationProject | dict[str, Any] | None,
        project_context: dict[str, Any] | None,
    ) -> tuple[OperationPlan, dict[str, Any]]:
        if isinstance(value, AccountOperationProject):
            context = {
                "project_id": value.project_id,
                "project_name": value.name,
                "client_brief": value.client_brief.to_dict(),
                "content_task_count": len(value.content_tasks),
                **dict(project_context or {}),
            }
            return value.operation_plan, context
        if isinstance(value, OperationPlan):
            return value, dict(project_context or {})
        data = mapping(value)
        if "operation_plan" in data and isinstance(data.get("operation_plan"), dict):
            context = {key: data[key] for key in ("project_id", "name", "client_brief") if key in data}
            context.update(project_context or {})
            return OperationPlan.from_dict(data.get("operation_plan")), context
        return OperationPlan.from_dict(data), dict(project_context or {})


class KPIPlannerPromptBuilder(AgentPromptBuilder):
    system_prompt = "你是 Nori 的账号代运营 KPI 规划器，只输出 JSON。"

    user_prompt_template = """\
根据运营计划生成可人工核验的 KPI 计划。

运营计划：
{operation_plan}

项目上下文：
{project_context}

要求：
- 不要假设已经有自动数据抓取能力。
- 指标必须能人工记录或从平台后台读取。
- 不做真实发布承诺，只做目标和核验方法。

输出 JSON，字段固定：
{{
  "targets": {{
    "content_tasks": 3,
    "review_pass_rate": ">= 90%",
    "manual_metrics_check": "每周 1 次"
  }},
  "milestones": [
    {{"day": 1, "target": "确认基线指标"}},
    {{"day": 7, "target": "完成本周期复盘"}}
  ],
  "measurement_notes": ["如何核验指标，2-5 条"]
}}
"""

    def build_user_prompt(self, plan: OperationPlan, context: dict[str, Any]) -> str:
        return self.user_prompt_template.format(
            operation_plan=json_prompt(plan.to_dict()),
            project_context=json_prompt(context),
        )


__all__ = [
    "KPIPlannerInputPreparer",
    "KPIPlannerPromptBuilder",
    "PreparedKPIPlannerInput",
]
