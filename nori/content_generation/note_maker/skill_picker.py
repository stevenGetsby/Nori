"""Skill selection helpers for NoteMakerAgent."""
from __future__ import annotations

from typing import Any, Callable

from nori.shared.prompting import json_block, json_prompt


JsonCall = Callable[..., dict[str, Any]]


def pick_skill_llm(
    skills: list[dict[str, Any]],
    intent: dict[str, Any],
    context: dict[str, Any],
    *,
    json_call: JsonCall,
    error_type=RuntimeError,
) -> dict[str, Any]:
    """Pick one skill by sending a compact candidate summary to the JSON LLM stage."""
    summary = [
        {
            "skill_id": skill.get("skill_id"),
            "label": skill.get("label"),
            "goal": skill.get("goal"),
            "tone": skill.get("tone"),
            "note_type": skill.get("note_type"),
            "creative_goal": skill.get("creative_goal"),
            "metrics_summary": skill.get("metrics_summary"),
        }
        for skill in skills
    ]
    data = json_call(
        system="你是 Nori 的 Skill 选择器，只输出 JSON。",
        user=(
            f"用户意图：\n{json_prompt(intent)}\n\n"
            f"上下文：\n{json_prompt(context)}\n\n"
            f"候选 skill：\n{json_block(summary)}\n\n"
            '选 1 个最契合用户意图的 skill。输出 {"skill_id": "..."}。'
        ),
        timeout=30,
    )
    chosen_id = str(data.get("skill_id") or "").strip()
    for skill in skills:
        if skill.get("skill_id") == chosen_id:
            return skill
    raise error_type(f"SkillPicker 返回未知 skill_id: {chosen_id!r}")


__all__ = ["pick_skill_llm"]
