"""Account Planner Agent: turn user context into account strategy."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Protocol

import llms
from nori.agent_models import AccountPlanResult, AccountPlannerInput


class SearchProvider(Protocol):
	def search(self, *, platform: str, keyword: str, limit: int) -> list[dict[str, Any]]:
		"""Search social platform content by keyword."""


class EmptySearchProvider:
	def search(self, *, platform: str, keyword: str, limit: int) -> list[dict[str, Any]]:
		return []


class AccountPlannerAgent:
	"""LLM-first account planner with a minimal structural fallback."""

	def __init__(self, *, use_llm: bool = True, search_provider: SearchProvider | None = None) -> None:
		self.use_llm = use_llm
		self.search_provider = search_provider or EmptySearchProvider()

	def run(
		self,
		user_input: AccountPlannerInput | str,
		images: list[str] | None = None,
		links: list[str] | None = None,
		*,
		use_llm: bool | None = None,
		enable_search: bool | None = None,
	) -> AccountPlanResult:
		normalized = _normalize_input(user_input, images, links)
		if enable_search is not None:
			normalized.enable_search = enable_search

		fallback = _fallback_plan(normalized)
		should_use_llm = self.use_llm if use_llm is None else use_llm
		result = self._draft_plan(normalized, fallback, should_use_llm)

		if normalized.enable_search:
			result = self._enrich_with_search(normalized, result, should_use_llm)

		return result

	def _draft_plan(
		self,
		normalized: AccountPlannerInput,
		fallback: AccountPlanResult,
		should_use_llm: bool,
	) -> AccountPlanResult:
		if not should_use_llm:
			return fallback
		return _llm_plan(normalized, fallback, []) or fallback

	def _enrich_with_search(
		self,
		normalized: AccountPlannerInput,
		result: AccountPlanResult,
		should_use_llm: bool,
	) -> AccountPlanResult:
		search_results = _run_search(self.search_provider, normalized, result)
		if not search_results:
			return result
		if should_use_llm:
			refined = _llm_plan(normalized, result, search_results)
			if refined:
				return refined
		return _merge_search_results(result, search_results)


account_plan = AccountPlannerAgent().run


SYSTEM_PROMPT = "你是 Nori 的 Account Planner Agent。只输出 JSON。"

USER_PROMPT = """\
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


TAG_KEYS = ("track", "goal", "platform", "product", "positioning")
KEYWORD_ROLES = {1: "赛道", 2: "主题", 3: "内容点"}
KEYWORD_REASON_FALLBACKS = {
	1: "用于覆盖本次内容创作所在赛道。",
	2: "用于聚焦本次内容创作主题。",
	3: "用于贴近本次内容创作的具体内容点。",
}
PLATFORM_KEYWORD_TOKENS = ("小红书", "xhs", "xiaohongshu", "抖音", "douyin", "dy", "视频号", "B站", "bilibili")


def _normalize_input(
	user_input: AccountPlannerInput | str,
	images: list[str] | None,
	links: list[str] | None,
) -> AccountPlannerInput:
	if isinstance(user_input, AccountPlannerInput):
		return AccountPlannerInput(
			text=user_input.text,
			images=[*user_input.images, *(images or [])],
			links=[*user_input.links, *(links or [])],
			intention=dict(user_input.intention),
			context=dict(user_input.context),
			platform=user_input.platform or "xhs",
			enable_search=user_input.enable_search,
			search_limit=user_input.search_limit,
		)
	return AccountPlannerInput(text=str(user_input or ""), images=list(images or []), links=list(links or []))


def _llm_plan(
	normalized: AccountPlannerInput,
	fallback: AccountPlanResult,
	search_results: list[dict[str, Any]],
) -> AccountPlanResult | None:
	try:
		data = llms.chat_json(
			[
				{"role": "system", "content": SYSTEM_PROMPT},
				{
					"role": "user",
					"content": USER_PROMPT.format(
						text=normalized.text.strip() or "无",
						images=json.dumps([_asset_context(path) for path in normalized.images], ensure_ascii=False),
						links=json.dumps(normalized.links, ensure_ascii=False),
						intention=json.dumps(normalized.intention, ensure_ascii=False),
						context=json.dumps(normalized.context, ensure_ascii=False),
						search_results=json.dumps(search_results, ensure_ascii=False),
					),
				},
			],
			usage="llm",
			_chat=llms.chat,
		)
		return _normalize_llm_result(data, fallback, search_results)
	except Exception:  # noqa: BLE001 - Planner must keep a usable fallback.
		return None


def _fallback_plan(normalized: AccountPlannerInput) -> AccountPlanResult:
	platform = _platform_label(normalized.platform)
	goal = _short_text(normalized.intention.get("goal"), "待判断")
	tags = {
		"track": "待判断",
		"goal": goal,
		"platform": platform,
		"product": "待判断",
		"positioning": "待判断",
	}
	benchmark_accounts = {"keyword_levels": [], "search_keywords": [], "accounts": [], "search_results": []}
	return AccountPlanResult(
		tags=tags,
		recommended_positioning="需要 LLM 根据 Intention + Context 推理账号定位。",
		audience_profile=[],
		content_directions=[],
		benchmark_accounts=benchmark_accounts,
		unique_selling_points=[],
		ip_portrait_report={
			"account_name_suggestions": [],
			"account_keywords": [],
			"content_pillars": [],
			"benchmark_creators": [],
			"cover_design_formats": [],
		},
	)


def _normalize_llm_result(
	data: dict[str, Any],
	fallback: AccountPlanResult,
	search_results: list[dict[str, Any]],
) -> AccountPlanResult:
	tags_data = data.get("tags") if isinstance(data.get("tags"), dict) else {}
	tags = {key: _short_text(tags_data.get(key), fallback.tags.get(key, "")) for key in TAG_KEYS}
	benchmark_data = data.get("benchmark_accounts") if isinstance(data.get("benchmark_accounts"), dict) else {}
	search_keyword_sources = _string_list(
		benchmark_data.get("search_keywords"),
		fallback.benchmark_accounts.get("search_keywords", []),
		limit=3,
	)
	keyword_levels = _normalize_keyword_levels(
		benchmark_data.get("keyword_levels"),
		fallback.benchmark_accounts.get("keyword_levels", []),
		search_keyword_sources,
	)
	benchmark_accounts = {
		"keyword_levels": keyword_levels,
		"search_keywords": _keywords_from_levels(keyword_levels),
		"accounts": _account_list(
			benchmark_data.get("accounts"),
			fallback.benchmark_accounts.get("accounts", []),
		),
		"search_results": list(search_results or benchmark_data.get("search_results") or []),
	}
	ip_portrait_report = _normalize_ip_portrait_report(
		data.get("ip_portrait_report"),
		fallback.ip_portrait_report,
		benchmark_accounts,
	)
	return AccountPlanResult(
		tags=tags,
		recommended_positioning=_text(data.get("recommended_positioning"), fallback.recommended_positioning),
		audience_profile=_string_list(data.get("audience_profile"), fallback.audience_profile, limit=5),
		content_directions=_string_list(data.get("content_directions"), fallback.content_directions, limit=5),
		benchmark_accounts=benchmark_accounts,
		unique_selling_points=_string_list(data.get("unique_selling_points"), fallback.unique_selling_points, limit=5),
		ip_portrait_report=ip_portrait_report,
	)


def _run_search(
	search_provider: SearchProvider,
	normalized: AccountPlannerInput,
	result: AccountPlanResult,
) -> list[dict[str, Any]]:
	platform = _platform_id(result.tags.get("platform") or normalized.platform)
	keywords = result.benchmark_accounts.get("search_keywords") or []
	output: list[dict[str, Any]] = []
	for keyword in _dedupe([_clean_keyword(keyword) for keyword in keywords if _clean_keyword(keyword)])[:3]:
		try:
			rows = search_provider.search(platform=platform, keyword=keyword, limit=normalized.search_limit)
		except Exception:  # noqa: BLE001
			rows = []
		for row in rows[: normalized.search_limit]:
			item = dict(row)
			item.setdefault("platform", platform)
			item.setdefault("keyword", keyword)
			output.append(item)
	return output


def _merge_search_results(result: AccountPlanResult, search_results: list[dict[str, Any]]) -> AccountPlanResult:
	benchmark_accounts = dict(result.benchmark_accounts)
	benchmark_accounts["search_results"] = search_results
	if search_results:
		benchmark_accounts["accounts"] = [
			{
				"name": str(item.get("author") or item.get("nickname") or item.get("title") or "搜索结果"),
				"platform": str(item.get("platform") or "xhs"),
				"reason": str(item.get("summary") or item.get("desc") or item.get("title") or "搜索命中结果。"),
				"keyword": _clean_keyword(item.get("keyword") or ""),
			}
			for item in search_results[:5]
		]
	return AccountPlanResult(
		tags=result.tags,
		recommended_positioning=result.recommended_positioning,
		audience_profile=result.audience_profile,
		content_directions=result.content_directions,
		benchmark_accounts=benchmark_accounts,
		unique_selling_points=result.unique_selling_points,
		ip_portrait_report=_merge_report_benchmarks(result.ip_portrait_report, benchmark_accounts),
	)


def _asset_context(path: str) -> dict[str, str]:
	suffix = Path(path).suffix.lower().lstrip(".")
	return {"path": path, "kind": suffix or "image"}


def _platform_label(platform: str) -> str:
	value = str(platform or "xhs").lower()
	if value in {"xhs", "xiaohongshu", "小红书"}:
		return "小红书"
	if value in {"dy", "douyin", "抖音"}:
		return "抖音"
	if value in {"bili", "bilibili", "b站"}:
		return "B站"
	if value in {"wechat", "视频号"}:
		return "视频号"
	return str(platform or "xhs")


def _platform_id(platform: str) -> str:
	if platform in {"小红书", "xhs", "xiaohongshu"}:
		return "xhs"
	if platform in {"抖音", "dy", "douyin"}:
		return "dy"
	if platform in {"B站", "bili", "bilibili"}:
		return "bili"
	if platform in {"视频号", "wechat"}:
		return "wechat"
	return platform or "xhs"


def _normalize_keyword_levels(
	value: Any,
	fallback: list[dict[str, Any]],
	search_keywords: list[str],
) -> list[dict[str, Any]]:
	sources = _keyword_sources(value, search_keywords, fallback)
	levels: list[dict[str, Any]] = []
	used_keywords: set[str] = set()
	used_reasons: set[str] = set()
	for index, source in enumerate(sources[:3], start=1):
		level = _level_number(source.get("level"), index)
		keyword = _clean_keyword(source.get("keyword") or "")
		if not keyword or keyword in used_keywords:
			continue
		reason = _text(source.get("reason"), KEYWORD_REASON_FALLBACKS.get(level, "用于本次账号规划搜索。"))
		if reason in used_reasons:
			reason = KEYWORD_REASON_FALLBACKS.get(level, "用于本次账号规划搜索。")
		used_keywords.add(keyword)
		used_reasons.add(reason)
		levels.append(
			{
				"level": level,
				"role": str(source.get("role") or KEYWORD_ROLES.get(level, "")),
				"keyword": keyword,
				"reason": reason,
			}
		)
	return sorted(levels, key=lambda item: int(item.get("level") or 0))


def _keyword_sources(value: Any, search_keywords: list[str], fallback: list[dict[str, Any]]) -> list[dict[str, Any]]:
	if isinstance(value, list):
		sources = [item for item in value if isinstance(item, dict)]
		if sources:
			return sources
	if search_keywords:
		return [{"level": index, "keyword": keyword} for index, keyword in enumerate(search_keywords[:3], start=1)]
	return [item for item in fallback[:3] if isinstance(item, dict)]


def _level_number(value: Any, fallback: int) -> int:
	try:
		level = int(value)
	except (TypeError, ValueError):
		level = fallback
	return level if level in KEYWORD_ROLES else fallback


def _keywords_from_levels(keyword_levels: list[dict[str, Any]]) -> list[str]:
	return _dedupe([
		_clean_keyword(item.get("keyword") or "")
		for item in keyword_levels
		if isinstance(item, dict) and _clean_keyword(item.get("keyword") or "")
	])


def _clean_keyword(value: Any) -> str:
	keyword = str(value or "").strip()
	for token in PLATFORM_KEYWORD_TOKENS:
		keyword = re.sub(re.escape(token), "", keyword, flags=re.I)
	keyword = re.sub(r"\s+", "", keyword)
	return keyword.strip("：:，,、；;|/\\")


def _normalize_ip_portrait_report(
	value: Any,
	fallback: dict[str, Any],
	benchmark_accounts: dict[str, Any],
) -> dict[str, Any]:
	data = value if isinstance(value, dict) else {}
	benchmark_creators = _creator_list(data.get("benchmark_creators"), fallback.get("benchmark_creators", []))
	if not benchmark_creators:
		benchmark_creators = _report_benchmark_creators(benchmark_accounts)
	return {
		"account_name_suggestions": _string_list(
			data.get("account_name_suggestions"),
			fallback.get("account_name_suggestions", []),
			limit=5,
		),
		"account_keywords": _string_list(data.get("account_keywords"), fallback.get("account_keywords", []), limit=5),
		"content_pillars": _content_pillar_list(data.get("content_pillars"), fallback.get("content_pillars", [])),
		"benchmark_creators": benchmark_creators[:5],
		"cover_design_formats": _cover_format_list(
			data.get("cover_design_formats"),
			fallback.get("cover_design_formats", []),
		),
	}


def _merge_report_benchmarks(report: dict[str, Any], benchmark_accounts: dict[str, Any]) -> dict[str, Any]:
	merged = dict(report)
	merged["benchmark_creators"] = _report_benchmark_creators(benchmark_accounts)
	return merged


def _report_benchmark_creators(benchmark_accounts: dict[str, Any]) -> list[dict[str, str]]:
	return [
		{
			"name": str(item.get("name") or "").strip(),
			"platform": str(item.get("platform") or "").strip(),
			"reason": str(item.get("reason") or "").strip(),
			"keyword": _clean_keyword(item.get("keyword") or ""),
		}
		for item in benchmark_accounts.get("accounts", [])[:5]
		if isinstance(item, dict)
	]


def _content_pillar_list(value: Any, fallback: list[dict[str, Any]]) -> list[dict[str, str]]:
	items = _dict_list(value, keys=("name", "description"), fallback=fallback)
	return [
		{"name": item.get("name") or item.get("description", "")[:12], "description": item.get("description") or item.get("name", "")}
		for item in items
		if item.get("name") or item.get("description")
	][:5]


def _creator_list(value: Any, fallback: list[dict[str, Any]]) -> list[dict[str, str]]:
	items = _dict_list(value, keys=("name", "platform", "reason", "keyword"), fallback=fallback)
	return [
		{
			"name": item.get("name", ""),
			"platform": item.get("platform", ""),
			"reason": item.get("reason", ""),
			"keyword": _clean_keyword(item.get("keyword") or ""),
		}
		for item in items
	][:5]


def _cover_format_list(value: Any, fallback: list[dict[str, Any]]) -> list[dict[str, str]]:
	items = _dict_list(value, keys=("name", "ratio", "layout", "reason"), fallback=fallback)
	return [
		{
			"name": item.get("name", ""),
			"ratio": item.get("ratio") or "3:4",
			"layout": item.get("layout", ""),
			"reason": item.get("reason", ""),
		}
		for item in items
	][:5]


def _account_list(value: Any, fallback: list[dict[str, Any]]) -> list[dict[str, str]]:
	items = _dict_list(value, keys=("name", "platform", "reason", "keyword"), fallback=fallback)
	return [
		{
			"name": item.get("name", ""),
			"platform": item.get("platform", ""),
			"reason": item.get("reason", ""),
			"keyword": _clean_keyword(item.get("keyword") or ""),
		}
		for item in items
	][:5]


def _dict_list(value: Any, *, keys: tuple[str, ...], fallback: list[dict[str, Any]]) -> list[dict[str, str]]:
	rows = value if isinstance(value, list) else fallback
	items: list[dict[str, str]] = []
	for row in rows:
		if not isinstance(row, dict):
			continue
		item = {key: str(row.get(key) or "").strip() for key in keys}
		if any(item.values()):
			items.append(item)
	return items


def _short_text(value: Any, fallback: str) -> str:
	text = _text(value, fallback)
	return text[:20]


def _text(value: Any, fallback: str) -> str:
	text = str(value or "").strip()
	return text or fallback


def _string_list(value: Any, fallback: list[str], *, limit: int) -> list[str]:
	if isinstance(value, str):
		items = [value]
	elif isinstance(value, list):
		items = [str(item).strip() for item in value if str(item).strip()]
	else:
		items = []
	return _dedupe(items or list(fallback))[:limit]


def _dedupe(items: list[str]) -> list[str]:
	seen: set[str] = set()
	result: list[str] = []
	for item in items:
		if item in seen:
			continue
		seen.add(item)
		result.append(item)
	return result
