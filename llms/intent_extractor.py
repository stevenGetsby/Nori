"""LLM-based intent extractor (P1 升级位).

岗位分工：
  - 输入：已 normalize 的 prompt 文本 + 需要抽取的字段清单 + 可选的枚举白名单
  - 输出：IntentLLMResult，只填能稳定抽到的字段，未抽到一律置空
  - 不依赖 nori_app，由调用方负责把结果 merge 回 IntentDraft

设计约束：
  - 严格 JSON 输出；解析失败、枚举越界、空串一律视为"未抽到"
  - 仅抽 needed_fields，省 token
  - 失败/超时不抛出，返回 error 字段，由上游决定降级
  - 不覆盖正则已经命中的字段（这一职责由调用方 merge 时负责）

接口：
  - extract_intent(normalized_prompt, *, needed_fields, enum_constraints=None,
                   usage="llm", timeout=6.0, max_candidates=3) -> IntentLLMResult

字段约定（与 nori_app.intent / nori_app.clarification 对齐）：
  - topic / content_type / audience / goal / tone / scene_hint / style_reference
"""
from __future__ import annotations

from typing import Any

from .call import chat_json_with_raw
from .errors import ChatJSONError
from .structured_calls import call_structured_json as _call_structured_json
from .structured_models import IntentLLMResult
from .structured_prompts import INTENT_FIELD_DESCRIPTIONS as _FIELD_DESCRIPTIONS
from .structured_prompts import build_intent_system_prompt as _build_intent_system_prompt
from .structured_prompts import build_intent_user_prompt as _build_intent_user_prompt
from .structured_outputs import chat_json_error_reason as _chat_json_error_reason
from .structured_outputs import clean_str as _clean_str
from .structured_outputs import normalize_field_value as _normalize_field_value


SUPPORTED_FIELDS = (
    "topic",
    "content_type",
    "audience",
    "goal",
    "tone",
    "scene_hint",
    "style_reference",
)

def extract_intent(
    normalized_prompt: str,
    *,
    needed_fields: list[str] | None = None,
    enum_constraints: dict[str, list[str]] | None = None,
    usage: str = "llm",
    timeout: float = 6.0,
    max_candidates: int = 3,
    model_hint: str | None = None,
) -> IntentLLMResult:
    """调用 LLM 从 prompt 中抽取意图字段。

    任何异常都吞掉，转成 result.error 返回，调用方按需降级。
    """
    # ---- 入参清洗 ----
    text = (normalized_prompt or "").strip()
    if not text:
        return IntentLLMResult(error="empty_prompt")

    fields = list(needed_fields) if needed_fields else list(SUPPORTED_FIELDS)
    fields = [f for f in fields if f in SUPPORTED_FIELDS]
    if not fields:
        return IntentLLMResult(error="no_supported_fields")

    enum_constraints = enum_constraints or {}

    # ---- 构造 prompt ----
    system_msg = _build_system_prompt(fields, enum_constraints, max_candidates)
    user_msg = _build_user_prompt(text, fields)

    # ---- 调用 LLM ----
    call_result = _call_structured_json(
        [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
        ],
        usage=usage,
        timeout=timeout,
        chat_json_with_raw_func=chat_json_with_raw,
    )
    if call_result.error:
        return IntentLLMResult(raw=call_result.raw, error=call_result.error)
    parsed = call_result.data or {}

    # ---- 字段收敛 ----
    final_fields: dict[str, str] = {}
    final_candidates: dict[str, list[str]] = {}

    for f in fields:
        node = parsed.get(f)
        value, candidates = _normalize_field_value(
            node,
            allowed=enum_constraints.get(f),
            max_candidates=max_candidates,
        )
        if value is not None:
            final_fields[f] = value
        if candidates:
            final_candidates[f] = candidates

    return IntentLLMResult(
        fields=final_fields,
        candidates=final_candidates,
        raw=call_result.raw,
        model=model_hint,
    )


# ----------------------------------------------------------------------
# Prompt 构造
# ----------------------------------------------------------------------


def _build_system_prompt(
    fields: list[str],
    enum_constraints: dict[str, list[str]],
    max_candidates: int,
) -> str:
    return _build_intent_system_prompt(fields, enum_constraints, max_candidates)


def _build_user_prompt(text: str, fields: list[str]) -> str:
    return _build_intent_user_prompt(text, fields)


__all__ = [
    "SUPPORTED_FIELDS",
    "IntentLLMResult",
    "extract_intent",
]
