"""LLM-based edit target selector (E2 升级位).

岗位分工：
  - 输入：用户的自由编辑指令文本 + 候选 selectors（带 role / summary）
         + 最近 N 轮对话意图摘要
  - 输出：TargetSelectionResult，给出主选 selector + 规整后的 instruction
         + 可选备选 + 置信度
  - 不依赖 nori_app.Conversation 类型；调用方只递 list[dict] 即可
  - 失败/超时不抛出，返回 error 字段，由上游决定降级（回退启发式）

接口：
  - select_edit_target(instruction, options, *, history=None, usage="llm",
                       timeout=6.0, max_alternatives=2,
                       model_hint=None) -> TargetSelectionResult

option 项约定：
  {"selector": "cover_image#abc123", "role": "cover_image",
   "summary": "封面图主选...", "kind": "image"}
  selector 是必填，其余都是可选辅料。

LLM 必须只能选 options 列出的 selector；不在白名单 → 视作未抽到（None）。
"""
from __future__ import annotations

from typing import Any

from .call import chat_json_with_raw
from .structured_calls import call_structured_json as _call_structured_json
from .structured_prompts import build_target_system_prompt as _build_target_system_prompt
from .structured_prompts import build_target_user_prompt as _build_target_user_prompt
from .structured_outputs import chat_json_error_reason as _chat_json_error_reason
from .structured_outputs import clean_str as _clean_str
from .structured_outputs import normalize_confidence as _normalize_confidence
from .structured_outputs import normalize_selector_alternatives as _normalize_selector_alternatives
from .structured_outputs import normalize_selector_options as _normalize_options
from nori.core.contracts import ChatJSONError, TargetSelectionResult


def select_edit_target(
    instruction: str,
    options: list[dict[str, Any]],
    *,
    history: list[str] | None = None,
    usage: str = "llm",
    timeout: float = 6.0,
    max_alternatives: int = 2,
    model_hint: str | None = None,
) -> TargetSelectionResult:
    """让 LLM 从 options 里挑一个 selector。

    任何异常都吞掉，转 result.error 返回。
    """
    text = (instruction or "").strip()
    if not text:
        return TargetSelectionResult(error="empty_instruction")

    valid_options = _normalize_options(options)
    if not valid_options:
        return TargetSelectionResult(error="empty_options")
    if len(valid_options) == 1:
        # 只有一个候选无须调 LLM
        only = valid_options[0]
        return TargetSelectionResult(
            target_selector=only["selector"],
            refined_instruction=text,
            confidence="high",
            reason="only_one_option",
        )

    selector_set = {opt["selector"] for opt in valid_options}

    system_msg = _build_system_prompt(valid_options, max_alternatives)
    user_msg = _build_user_prompt(text, history or [])

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
        return TargetSelectionResult(raw=call_result.raw, error=call_result.error)
    parsed = call_result.data or {}

    target = _clean_str(parsed.get("target_selector"))
    if target is None or target not in selector_set:
        return TargetSelectionResult(
            raw=call_result.raw,
            error="invalid_selector" if target else "missing_selector",
        )

    refined_raw = parsed.get("refined_instruction")
    refined = _clean_str(refined_raw) or text
    confidence = _normalize_confidence(parsed.get("confidence"))
    reason = _clean_str(parsed.get("reason"))

    alts = _normalize_selector_alternatives(
        parsed.get("alternatives"),
        selector_set=selector_set,
        target=target,
        max_alternatives=max_alternatives,
    )

    return TargetSelectionResult(
        target_selector=target,
        refined_instruction=refined,
        alternatives=alts,
        confidence=confidence,
        reason=reason,
        raw=call_result.raw,
        model=model_hint,
    )


# ----------------------------------------------------------------------
# Prompt 构造
# ----------------------------------------------------------------------


def _build_system_prompt(options: list[dict[str, Any]], max_alternatives: int) -> str:
    return _build_target_system_prompt(options, max_alternatives)


def _build_user_prompt(instruction: str, history: list[str]) -> str:
    return _build_target_user_prompt(instruction, history)


__all__ = [
    "TargetSelectionResult",
    "select_edit_target",
]
