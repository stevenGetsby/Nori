"""Class-owned package contract for OperationPlannerAgent."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any

from nori.core import AgentInputPreparer, AgentPromptBuilder, ClientBrief
from nori.shared.normalization import bounded_int, mapping, string_list
from nori.shared.prompting import json_prompt
from nori.agents.user_profiling.schemas import AccountPlanResult


@dataclass(frozen=True)
class PreparedOperationPlannerInput:
    brief: ClientBrief
    account_plan: AccountPlanResult | None
    start_date: date
    horizon_days: int


class OperationPlannerInputPreparer(AgentInputPreparer):
    """Restore and bound OperationPlanner runtime inputs."""

    def prepare(
        self,
        client_brief: ClientBrief | dict[str, Any] | None,
        account_plan: AccountPlanResult | dict[str, Any] | None = None,
        *,
        start_date: str | date | None = None,
        horizon_days: int = 7,
    ) -> PreparedOperationPlannerInput:
        return PreparedOperationPlannerInput(
            brief=self.normalize_client_brief(client_brief),
            account_plan=self.normalize_account_plan(account_plan),
            start_date=self.normalize_start_date(start_date),
            horizon_days=self.bounded_horizon(horizon_days),
        )

    def normalize_client_brief(self, value: ClientBrief | dict[str, Any] | None) -> ClientBrief:
        if isinstance(value, ClientBrief):
            return value
        return ClientBrief.from_dict(value if isinstance(value, dict) else {})

    def normalize_account_plan(self, value: AccountPlanResult | dict[str, Any] | None) -> AccountPlanResult | None:
        if isinstance(value, AccountPlanResult):
            return value
        if not isinstance(value, dict):
            return None
        return AccountPlanResult(
            tags=mapping(value.get("tags")),
            recommended_positioning=str(value.get("recommended_positioning") or ""),
            audience_profile=string_list(value.get("audience_profile"), []),
            content_directions=string_list(value.get("content_directions"), []),
            benchmark_accounts=mapping(value.get("benchmark_accounts")),
            unique_selling_points=string_list(value.get("unique_selling_points"), []),
            ip_portrait_report=mapping(value.get("ip_portrait_report")),
        )

    def account_plan_dict(self, value: AccountPlanResult | None) -> dict[str, Any]:
        return value.to_dict() if isinstance(value, AccountPlanResult) else {}

    def normalize_start_date(self, value: str | date | None) -> date:
        if isinstance(value, date):
            return value
        if isinstance(value, str) and value:
            try:
                return date.fromisoformat(value)
            except ValueError:
                pass
        return date.today()

    def bounded_horizon(self, value: Any) -> int:
        return bounded_int(value, default=7, minimum=1, maximum=90)


class OperationPlannerPromptBuilder(AgentPromptBuilder):
    system_prompt = "你是 Nori 的账号代运营 SOP 运营计划助手。只输出 JSON。"

    user_prompt_template = """\
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

    def __init__(self, input_preparer: OperationPlannerInputPreparer | None = None) -> None:
        self.input_preparer = input_preparer or OperationPlannerInputPreparer()

    def build_user_prompt(
        self,
        brief: ClientBrief,
        account_plan: AccountPlanResult | None,
        *,
        horizon_days: int,
    ) -> str:
        return self.user_prompt_template.format(
            client_brief=json_prompt(brief.to_dict()),
            account_plan=json_prompt(self.input_preparer.account_plan_dict(account_plan)),
            horizon_days=horizon_days,
        )


__all__ = [
    "OperationPlannerInputPreparer",
    "OperationPlannerPromptBuilder",
    "PreparedOperationPlannerInput",
]
