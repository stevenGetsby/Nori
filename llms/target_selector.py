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

import json
import re
from dataclasses import dataclass, field
from typing import Any

from .call import chat


@dataclass(slots=True)
class TargetSelectionResult:
    """LLM 选 target 产物。

    target_selector:    最终选中的 selector（必须在输入 options 内）
    refined_instruction: LLM 帮忙规整后的指令（去除"封面"等指代词，保留语义）
                         可能与原指令一致；调用方可视情况采用
    alternatives:        次选 selector 列表（不含主选自身）
    confidence:          high / medium / low；low 表示模型自己也不确定
    reason:              一句话说明，供日志/UI 用
    raw:                 原始字符串，仅 debug
    model:               模型 key
    error:               非空表示降级原因
    """

    target_selector: str | None = None
    refined_instruction: str | None = None
    alternatives: list[str] = field(default_factory=list)
    confidence: str = "low"
    reason: str | None = None
    raw: str = ""
    model: str | None = None
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.error is None and self.target_selector is not None


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

    raw = ""
    try:
        kwargs: dict[str, Any] = {
            "usage": usage,
            "timeout": timeout,
        }
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
            raw = chat(
                [
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg},
                ],
                **kwargs,
            )
        except Exception as inner:  # noqa: BLE001
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
        return TargetSelectionResult(raw=raw, error=f"api_error:{type(exc).__name__}")

    if not raw or not raw.strip():
        return TargetSelectionResult(raw=raw, error="empty_response")

    parsed = _safe_json_loads(raw)
    if parsed is None or not isinstance(parsed, dict):
        return TargetSelectionResult(raw=raw, error="parse_error")

    target = _clean_str(parsed.get("target_selector"))
    if target is None or target not in selector_set:
        return TargetSelectionResult(
            raw=raw,
            error="invalid_selector" if target else "missing_selector",
        )

    refined_raw = parsed.get("refined_instruction")
    refined = _clean_str(refined_raw) or text
    confidence = _clean_str(parsed.get("confidence")) or "low"
    if confidence not in ("high", "medium", "low"):
        confidence = "low"
    reason = _clean_str(parsed.get("reason"))

    alts_raw = parsed.get("alternatives") or []
    alts: list[str] = []
    if isinstance(alts_raw, list):
        for x in alts_raw:
            s = _clean_str(x)
            if s and s in selector_set and s != target and s not in alts:
                alts.append(s)
            if len(alts) >= max_alternatives:
                break

    return TargetSelectionResult(
        target_selector=target,
        refined_instruction=refined,
        alternatives=alts,
        confidence=confidence,
        reason=reason,
        raw=raw,
        model=model_hint,
    )


# ----------------------------------------------------------------------
# Prompt 构造
# ----------------------------------------------------------------------


def _build_system_prompt(options: list[dict[str, Any]], max_alternatives: int) -> str:
    catalog_lines: list[str] = []
    for opt in options:
        sel = opt["selector"]
        role = opt.get("role") or ""
        kind = opt.get("kind") or ""
        summary = (opt.get("summary") or "").strip()
        if summary:
            summary = summary.replace("\n", " ")
            if len(summary) > 80:
                summary = summary[:77] + "..."
        bits = [f"selector={sel}"]
        if role:
            bits.append(f"role={role}")
        if kind:
            bits.append(f"kind={kind}")
        if summary:
            bits.append(f"summary={summary}")
        catalog_lines.append("- " + " | ".join(bits))

    catalog_block = "\n".join(catalog_lines)

    return (
        "你是一个对话编辑路由器。\n"
        "任务：用户对一份已生成的小红书内容提出了一条编辑指令；"
        "请从候选资产里挑出一个最适合被这条指令改写的 target selector，"
        "并把指令改写成无歧义、面向该资产的版本。\n\n"
        "可选资产：\n"
        f"{catalog_block}\n\n"
        "硬性规则：\n"
        "1. target_selector 必须是上面列出的 selector 字符串之一，不要发明新值。\n"
        "2. 如果用户指令里明显涉及画面/封面/视觉/构图 → 选 role=cover_image；\n"
        "   如果指令涉及标题/正文/文案/口吻/标签 → 选 role=copy_text；\n"
        "   不要去选 role=package / role=review / role=scratch（这些不允许编辑）。\n"
        "3. refined_instruction 中不要再用'封面'/'图'/'文案'这种指代词，"
        "要写成对该资产可直接执行的祈使句；语义不能改变。\n"
        f"4. alternatives 至多 {max_alternatives} 个；只能从候选里选；不要重复主选。\n"
        "5. confidence 取 high/medium/low 之一。\n"
        "6. 输出严格 JSON：{\"target_selector\": str, \"refined_instruction\": str,"
        " \"alternatives\": [str], \"confidence\": \"high|medium|low\","
        " \"reason\": str}。不要解释，不要前后缀。"
    )


def _build_user_prompt(instruction: str, history: list[str]) -> str:
    parts = [
        "用户编辑指令：",
        f"<<<\n{instruction}\n>>>",
    ]
    if history:
        parts.append("")
        parts.append("最近对话摘要（最旧 → 最新）：")
        for line in history:
            parts.append(f"- {line}")
    return "\n".join(parts)


# ----------------------------------------------------------------------
# 输入/输出归一化
# ----------------------------------------------------------------------


def _normalize_options(options: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    cleaned: list[dict[str, Any]] = []
    for raw in options or []:
        if not isinstance(raw, dict):
            continue
        sel = _clean_str(raw.get("selector"))
        if not sel or sel in seen:
            continue
        seen.add(sel)
        cleaned.append(
            {
                "selector": sel,
                "role": _clean_str(raw.get("role")) or "",
                "kind": _clean_str(raw.get("kind")) or "",
                "summary": _clean_str(raw.get("summary")) or "",
            }
        )
    return cleaned


def _safe_json_loads(raw: str) -> Any | None:
    text = raw.strip()
    try:
        return json.loads(text)
    except Exception:  # noqa: BLE001
        pass
    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL | re.IGNORECASE)
    if fence:
        try:
            return json.loads(fence.group(1))
        except Exception:  # noqa: BLE001
            pass
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start : end + 1])
        except Exception:  # noqa: BLE001
            return None
    return None


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
    "TargetSelectionResult",
    "select_edit_target",
]
