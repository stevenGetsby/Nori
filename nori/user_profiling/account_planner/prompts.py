"""AccountPlanner prompt construction helpers."""
from __future__ import annotations

from typing import Any

from nori.shared.prompting import json_prompt
from nori.user_profiling.models import AccountPlannerInput

from .inputs import asset_context


SYSTEM_PROMPT = "你是 Nori 的 Account Planner Agent。只输出 JSON。"

USER_PROMPT_TEMPLATE = """\
根据 Intaker 输出做账号规划。

业务流程：
1. 基于 Intention + Context 推理账号赛道、内容主题、具体内容点。
2. 基于推理结果生成账号定位、内容方向、差异化卖点和三层搜索关键词。
3. 如果有真实搜索结果，只把它作为对标与样本依据，不覆盖用户事实。

优先级：
Intention + Context 是主输入。
原始文字、图片、链接只作为证据，不重新覆盖 Intaker 的结论。

原始文字证据：
{text}

原始图片证据：
{images}

链接证据：
{links}

Intention：
{intention}

Context：
{context}

搜索结果：
{search_results}

输出 JSON，字段固定：
{{
  "tags": {{
	"track": "五个字以内的赛道",
	"goal": "五个字以内的目标",
	"platform": "平台",
	"product": "五个字以内的产品",
	"positioning": "十个字以内的定位"
  }},
  "recommended_positioning": "一句推荐账号定位",
  "audience_profile": ["目标受众画像，3-5条"],
  "content_directions": ["内容方向建议，3-5条"],
  "benchmark_accounts": {{
	"keyword_levels": [
	  {{"level": 1, "role": "赛道", "keyword": "从输入推理出的赛道关键词", "reason": "为什么这个词能覆盖本次创作赛道"}},
	  {{"level": 2, "role": "主题", "keyword": "从输入推理出的主题关键词", "reason": "为什么这个词能聚焦本次创作主题"}},
	  {{"level": 3, "role": "内容点", "keyword": "从输入推理出的内容点关键词", "reason": "为什么这个词能贴近本次具体内容点"}}
	],
	"search_keywords": ["从 keyword_levels 提取的关键词，保持同顺序"],
	"accounts": [
	  {{"name": "账号名或搜索方向", "platform": "平台", "reason": "推荐原因", "keyword": "对应关键词"}}
	],
	"search_results": []
  }},
	"unique_selling_points": ["差异化卖点，3-5条"],
  "ip_portrait_report": {{
	"account_name_suggestions": ["账号名建议，5个以内"],
	"account_keywords": ["账号关键词，5个以内"],
	"content_pillars": [
	  {{"name": "内容支柱名称", "description": "这类内容主要讲什么"}}
	],
	"benchmark_creators": [
	  {{"name": "对标博主或搜索方向", "platform": "平台", "reason": "为什么对标", "keyword": "对应搜索关键词"}}
	],
	"cover_design_formats": [
	  {{"name": "封面格式名称", "ratio": "3:4", "layout": "画面结构", "reason": "为什么推荐"}}
	]
  }}
}}

要求：
- 五个小标签必须短。
- 账号规划必须基于 Intention + Context 推理，不要照抄上面的占位说明。
- 不要编造用户没有提供的确定事实。
- 搜索关键词必须固定 3 个层级：第 1 层是本次内容创作的赛道，第 2 层是本次内容创作的主题，第 3 层是本次内容创作的具体内容点；每层 reason 必须不同。
- keyword 不能包含空格，不能包含平台名，例如不要写“小红书”“xhs”“抖音”。
- 如果没有真实搜索结果，对标账号可以给搜索方向，但不要假装已经搜索到具体账号。
- 输出适合后续生成账号内容策略使用。
"""


def build_user_prompt(normalized: AccountPlannerInput, search_results: list[dict[str, Any]]) -> str:
	return USER_PROMPT_TEMPLATE.format(
		text=normalized.text.strip() or "无",
		images=json_prompt([asset_context(path) for path in normalized.images]),
		links=json_prompt(normalized.links),
		intention=json_prompt(normalized.intention),
		context=json_prompt(normalized.context),
		search_results=json_prompt(search_results),
	)
