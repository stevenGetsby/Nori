"""OperationPlanner prompt construction helpers."""
from __future__ import annotations

from nori.core import ClientBrief
from nori.shared.prompting import json_prompt
from nori.user_profiling.models import AccountPlanResult

from .inputs import account_plan_dict


SYSTEM_PROMPT = "你是 Nori 的账号代运营 SOP 运营计划助手。只输出 JSON。"

USER_PROMPT_TEMPLATE = """\
根据客户简报和账号定位结果，生成一个可执行的账号代运营计划。

客户简报：
{client_brief}

账号定位结果：
{account_plan}

计划要求：
- 只规划 {horizon_days} 天。
- 默认平台是客户简报中的 platform。
- 不要设计真实发布、自动互动、自动抓取数据等未实现能力。
- 内容任务要能后续交给 ContentTask -> NoteMakerAgent -> CoverDirectorAgent。

输出 JSON，字段固定：
{{
  "operation_plan": {{
    "objectives": ["运营目标，2-4 条"],
    "content_pillars": ["内容支柱，2-5 条"],
    "cadence": "发布/制作节奏",
    "kpi_targets": {{"metric": "target"}},
    "milestones": [
      {{"day": 1, "target": "阶段目标"}}
    ],
    "risk_controls": ["风险控制，2-4 条"],
    "notes": ["补充说明，可为空"]
  }},
  "content_calendar": {{
    "themes": ["本周期主题，1-4 条"],
    "tasks": [
      {{
        "title": "任务标题",
        "day": 1,
        "content_type": "note",
        "topic": "内容主题",
        "objective": "本条内容目标",
        "priority": 1,
        "brief": {{"cover_title": "封面标题建议"}},
        "required_assets": ["需要的素材类型"],
        "notes": ["制作注意事项"]
      }}
    ],
    "notes": ["排期说明，可为空"]
  }}
}}
"""


def build_user_prompt(
    brief: ClientBrief,
    account_plan: AccountPlanResult | None,
    *,
    horizon_days: int,
) -> str:
    return USER_PROMPT_TEMPLATE.format(
        client_brief=json_prompt(brief.to_dict()),
        account_plan=json_prompt(account_plan_dict(account_plan)),
        horizon_days=horizon_days,
    )
