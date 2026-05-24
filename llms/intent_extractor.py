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

import json
import re
from dataclasses import dataclass, field
from typing import Any

from .call import chat


SUPPORTED_FIELDS = (
    "topic",
    "content_type",
    "audience",
    "goal",
    "tone",
    "scene_hint",
    "style_reference",
)

_FIELD_DESCRIPTIONS: dict[str, str] = {
    "topic": "本次内容的核心主题（1 句话以内，不要包含'分享'/'今天'这类无信息词）。",
    "content_type": "小红书内容形态枚举，只能从 enum 里选一个。",
    "audience": "主要受众画像（如：新手宝妈、职场新人、健身入门者）。",
    "goal": "本条内容期望达成的目标（如：收藏、转发、获客、表达观点）。",
    "tone": "整体语气调性（如：清晰自然、专业克制、生活化、犀利直接、温柔陪伴）。",
    "scene_hint": "封面期望的场景倾向（如：桌面静物、人像特写、对比拼图）。",
    "style_reference": "用户提到的视觉/文案参考（作品、博主、风格关键词）。",
}


@dataclass(slots=True)
class IntentLLMResult:
    """LLM 抽取产物.

    fields:        最终落定的 (field -> value)，已通过空串/枚举白名单过滤
    candidates:    每个字段的候选列表（含主选），可投喂给 ClarificationQuestion.options
    raw:           LLM 原始字符串，仅用于 debug
    model:         实际调用的模型 key
    error:         非空表示降级原因（timeout / parse_error / empty / api_error 等）
    """

    fields: dict[str, str] = field(default_factory=dict)
    candidates: dict[str, list[str]] = field(default_factory=dict)
    raw: str = ""
    model: str | None = None
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.error is None and bool(self.fields)


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
    raw = ""
    try:
        kwargs: dict[str, Any] = {
            "usage": usage,
            "timeout": timeout,
        }
        # 优先尝试 JSON object 强约束；失败再回退一次纯文本
        try:
            raw = chat(
                [
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg},
                ],
                response_format={"type": "json_object"},
                **kwargs,
            )
        except TypeError:
            # provider/SDK 不接受 response_format
            raw = chat(
                [
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg},
                ],
                **kwargs,
            )
        except Exception as inner:  # noqa: BLE001
            # response_format 被 provider 拒绝（部分中转走 4xx）→ 退到纯文本
            if _is_response_format_error(inner):
                raw = chat(
                    [
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": user_msg},
                    ],
                    **kwargs,
                )
            else:
                raise
    except Exception as exc:  # noqa: BLE001
        return IntentLLMResult(raw=raw, error=f"api_error:{type(exc).__name__}")

    if not raw or not raw.strip():
        return IntentLLMResult(raw=raw, error="empty_response")

    # ---- 解析 JSON ----
    parsed = _safe_json_loads(raw)
    if parsed is None or not isinstance(parsed, dict):
        return IntentLLMResult(raw=raw, error="parse_error")

    # ---- 字段收敛 ----
    final_fields: dict[str, str] = {}
    final_candidates: dict[str, list[str]] = {}

    for f in fields:
        node = parsed.get(f)
        value, candidates = _normalize_field_value(
            field_name=f,
            node=node,
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
        raw=raw,
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
    field_lines: list[str] = []
    for f in fields:
        desc = _FIELD_DESCRIPTIONS.get(f, "")
        if f in enum_constraints:
            allowed = "/".join(enum_constraints[f])
            field_lines.append(f"- {f}: {desc} 只能从枚举中选：[{allowed}]")
        else:
            field_lines.append(f"- {f}: {desc}")

    field_block = "\n".join(field_lines)

    return (
        "你是小红书内容意图抽取器。\n"
        "任务：从用户的需求文本中抽取下列字段，只输出 JSON 对象，不要解释、不要前后缀。\n\n"
        f"需要抽取的字段：\n{field_block}\n\n"
        "硬性规则：\n"
        "1. 抽不到、不确定、用户没明确写的字段，对应 value 必须为 null。\n"
        "2. 不要编造内容，不要把'分享'/'今天'这类无意义词当 topic。\n"
        "3. 枚举字段必须严格落在给定枚举内，不在则返回 null。\n"
        f"4. 每个字段可以额外提供至多 {max_candidates} 个候选，"
        "格式：{\"value\": <主选>, \"candidates\": [<可选>, ...]}；"
        "若只有一个候选，直接给字符串即可。\n"
        "5. 输出必须是合法 JSON，键名严格使用上面给出的英文字段名。"
    )


def _build_user_prompt(text: str, fields: list[str]) -> str:
    schema_keys = ", ".join(f'"{f}"' for f in fields)
    return (
        "用户需求文本：\n"
        f"<<<\n{text}\n>>>\n\n"
        f"请输出 JSON，仅包含 keys: {{{schema_keys}}}。"
    )


# ----------------------------------------------------------------------
# 解析与收敛
# ----------------------------------------------------------------------


def _safe_json_loads(raw: str) -> Any | None:
    text = raw.strip()
    # 直接尝试
    try:
        return json.loads(text)
    except Exception:  # noqa: BLE001
        pass
    # 从 ```json ... ``` 抠
    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL | re.IGNORECASE)
    if fence:
        try:
            return json.loads(fence.group(1))
        except Exception:  # noqa: BLE001
            pass
    # 抠第一个 { 到最后一个 }
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start : end + 1])
        except Exception:  # noqa: BLE001
            return None
    return None


def _normalize_field_value(
    *,
    field_name: str,
    node: Any,
    allowed: list[str] | None,
    max_candidates: int,
) -> tuple[str | None, list[str]]:
    """把 LLM 返回的单字段节点收敛为 (value, candidates)。

    支持三种节点形态：
      - 字符串（直接当 value，candidates 为空）
      - {"value": str, "candidates": [str, ...]}
      - 列表（首项当 value，其余进 candidates）
    """
    value: str | None = None
    candidates: list[str] = []

    if node is None:
        return None, []

    if isinstance(node, str):
        value = node
    elif isinstance(node, dict):
        v = node.get("value")
        if isinstance(v, str):
            value = v
        elif isinstance(v, list) and v:
            value = str(v[0]) if v[0] is not None else None
            candidates.extend(str(x) for x in v[1:] if x)
        cand = node.get("candidates")
        if isinstance(cand, list):
            candidates.extend(str(x) for x in cand if x)
    elif isinstance(node, list):
        items = [str(x) for x in node if x]
        if items:
            value = items[0]
            candidates.extend(items[1:])

    value = _clean_str(value)
    candidates = [c for c in (_clean_str(x) or "" for x in candidates) if c]

    if allowed is not None:
        allowed_set = set(allowed)
        if value is not None and value not in allowed_set:
            value = None
        candidates = [c for c in candidates if c in allowed_set]

    # 去重 + 截断
    seen: set[str] = set()
    deduped: list[str] = []
    if value:
        seen.add(value)
        deduped.append(value)
    for c in candidates:
        if c in seen:
            continue
        seen.add(c)
        deduped.append(c)
        if len(deduped) - (1 if value else 0) >= max_candidates:
            break

    # candidates 不含主选本身，方便上游直接当 options 用
    final_candidates = [c for c in deduped if c != value]
    return value, final_candidates


def _clean_str(v: Any) -> str | None:
    if v is None:
        return None
    if not isinstance(v, str):
        v = str(v)
    s = v.strip().strip("'\"").strip()
    if not s:
        return None
    if s.lower() in {"null", "none", "n/a", "未知"}:
        return None
    return s


def _is_response_format_error(exc: Exception) -> bool:
    msg = str(exc).lower()
    return any(k in msg for k in ("response_format", "json_object", "unsupported"))


__all__ = [
    "SUPPORTED_FIELDS",
    "IntentLLMResult",
    "extract_intent",
]
