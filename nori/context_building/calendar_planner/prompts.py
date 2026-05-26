"""CalendarPlanner prompt construction helpers."""
from __future__ import annotations

from datetime import date

from nori.core import ClientBrief
from nori.shared.prompting import json_prompt

from ..models import KPIPlan, OperationPlan


SYSTEM_PROMPT = "你是 Nori 的账号代运营排期规划器，只输出 JSON。"

USER_PROMPT_TEMPLATE = """\
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
    plan: OperationPlan,
    kpi: KPIPlan,
    brief: ClientBrief,
    *,
    start_date: date,
    horizon_days: int,
) -> str:
    return USER_PROMPT_TEMPLATE.format(
        operation_plan=json_prompt(plan.to_dict()),
        kpi_plan=json_prompt(kpi.to_dict()),
        client_context=json_prompt(brief.to_dict()),
        start_date=start_date.isoformat(),
        horizon_days=horizon_days,
    )
