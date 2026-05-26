"""KPIPlanner prompt construction helpers."""
from __future__ import annotations

from typing import Any

from nori.shared.prompting import json_prompt

from ..models import OperationPlan


SYSTEM_PROMPT = "你是 Nori 的账号代运营 KPI 规划器，只输出 JSON。"

USER_PROMPT_TEMPLATE = """\
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


def build_user_prompt(plan: OperationPlan, context: dict[str, Any]) -> str:
    return USER_PROMPT_TEMPLATE.format(
        operation_plan=json_prompt(plan.to_dict()),
        project_context=json_prompt(context),
    )
