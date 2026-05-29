"""Required session-level LLM stages for XHS hot-note analysis."""
from __future__ import annotations

from typing import Any

from nori.core import LLMFactory
from nori.shared.llm_json import call_stage_json
from .session_clustering import GOAL_KEYWORDS
from .package import XHSKeywordPromptBuilder, XHSLabelPromptBuilder


class XHSSessionLLMError(RuntimeError):
    """Raised when required session-level XHS LLM stages fail."""


_KEYWORD_PROMPT_BUILDER = XHSKeywordPromptBuilder()
_LABEL_PROMPT_BUILDER = XHSLabelPromptBuilder()
KEYWORD_SYSTEM_PROMPT = _KEYWORD_PROMPT_BUILDER.system_prompt
KEYWORD_USER_PROMPT = _KEYWORD_PROMPT_BUILDER.user_prompt_template
LABEL_SYSTEM_PROMPT = _LABEL_PROMPT_BUILDER.system_prompt
LABEL_USER_PROMPT = _LABEL_PROMPT_BUILDER.user_prompt_template


def generate_keywords(
    context: dict[str, Any],
    *,
    max_n: int = 3,
    error_type: type[Exception] = XHSSessionLLMError,
    llm_factory: LLMFactory | None = None,
) -> list[str]:
    llm_gateway = llm_factory or LLMFactory()
    data = call_stage_json(
        system=_KEYWORD_PROMPT_BUILDER.system_prompt,
        user=_KEYWORD_PROMPT_BUILDER.build_user_prompt(context, max_n=max_n),
        timeout=30,
        error_type=error_type,
        chat_func=llm_gateway.chat_func,
        chat_json_func=llm_gateway.chat_json_func,
    )
    items = data.get("keywords") if isinstance(data, dict) else None
    if not isinstance(items, list):
        return []
    out: list[str] = []
    for item in items:
        text = str(item or "").strip()
        if text and text not in out:
            out.append(text[:20])
        if len(out) >= max_n:
            break
    return out


def label_notes(
    hot_notes: list[Any],
    *,
    error_type: type[Exception] = XHSSessionLLMError,
    llm_factory: LLMFactory | None = None,
) -> dict[str, dict[str, str]]:
    if not hot_notes:
        return {}
    items = [
        {
            "note_id": note.note_id,
            "title": note.title,
            "desc": (note.desc or "")[:200],
            "tags": list(note.tags)[:5],
            "metrics": {"liked": note.liked, "collected": note.collected},
        }
        for note in hot_notes
    ]
    llm_gateway = llm_factory or LLMFactory()
    data = call_stage_json(
        system=_LABEL_PROMPT_BUILDER.system_prompt,
        user=_LABEL_PROMPT_BUILDER.build_user_prompt(items),
        timeout=120,
        error_type=error_type,
        chat_func=llm_gateway.chat_func,
        chat_json_func=llm_gateway.chat_json_func,
    )
    out: dict[str, dict[str, str]] = {}
    if not isinstance(data, dict):
        return out
    labels = data.get("labels")
    if not isinstance(labels, list):
        return out
    valid_goals = set(GOAL_KEYWORDS) | {"general"}
    for item in labels:
        if not isinstance(item, dict):
            continue
        note_id = str(item.get("note_id") or "").strip()
        if not note_id:
            continue
        goal = str(item.get("goal") or "").strip().lower()
        if goal not in valid_goals:
            goal = "general"
        tone = str(item.get("tone") or "").strip()[:20]
        out[note_id] = {"goal": goal, "tone": tone}
    return out


__all__ = [
    "KEYWORD_SYSTEM_PROMPT",
    "KEYWORD_USER_PROMPT",
    "LABEL_SYSTEM_PROMPT",
    "LABEL_USER_PROMPT",
    "XHSSessionLLMError",
    "generate_keywords",
    "label_notes",
]
