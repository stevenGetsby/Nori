"""Optional LLM enhancement helpers for single XHS note seed drafts."""
from __future__ import annotations

from typing import Any

from nori.core import LLMFactory
from nori.agents.market_analysis.schemas import XHSNoteSample, XHSSeedSkillDraft
from nori.shared.llm_json import attach_llm_error, try_stage_json
from nori.shared.normalization import dedupe_preserve_order, string_list as _shared_string_list
from .package import XHSNoteEnhancementPromptBuilder


_PROMPT_BUILDER = XHSNoteEnhancementPromptBuilder()
SYSTEM_PROMPT = _PROMPT_BUILDER.system_prompt
USER_PROMPT = _PROMPT_BUILDER.user_prompt_template


def enhance_note(
    note: XHSNoteSample,
    rule_draft: XHSSeedSkillDraft,
    *,
    chat_json_func=None,
) -> XHSSeedSkillDraft:
    llm_factory = LLMFactory(chat_json_func=chat_json_func)
    data, error = try_stage_json(
        system=_PROMPT_BUILDER.system_prompt,
        user=_PROMPT_BUILDER.build_user_prompt(note, rule_draft),
        timeout=60,
        chat_json_func=llm_factory.chat_json_func,
    )
    if data is None:
        fallback = mark_llm_fallback(rule_draft)
        if error:
            attach_llm_error(fallback.validation, "xhs_note_analyzer", error)
        return fallback
    return normalize_llm_draft(data, rule_draft)


def normalize_llm_draft(data: dict[str, Any], fallback: XHSSeedSkillDraft) -> XHSSeedSkillDraft:
    match_data = data.get("match") if isinstance(data.get("match"), dict) else {}
    craft_data = data.get("craft") if isinstance(data.get("craft"), dict) else {}
    evidence_data = data.get("evidence") if isinstance(data.get("evidence"), dict) else {}
    validation_data = data.get("validation") if isinstance(data.get("validation"), dict) else {}

    match = dict(fallback.match)
    match["scene"] = text(match_data.get("scene"), fallback.match.get("scene", ""), limit=30)
    match["goals"] = string_list(match_data.get("goals"), fallback.match.get("goals", []), limit=3)
    match["note_type"] = text(match_data.get("note_type"), fallback.match.get("note_type", "图文"), limit=20)

    craft = dict(fallback.craft)
    craft["creative_goal"] = text(
        craft_data.get("creative_goal"),
        fallback.craft.get("creative_goal", ""),
        limit=120,
    )
    for key in ("title_rules", "opening_rules", "body_structure", "interaction_rules", "visual_rules"):
        craft[key] = rule_items(craft_data.get(key), fallback.craft.get(key, []), limit=6)
    craft["avoid_rules"] = string_list(craft_data.get("avoid_rules"), fallback.craft.get("avoid_rules", []), limit=8)

    evidence = dict(fallback.evidence)
    llm_observations = string_list(evidence_data.get("llm_observations"), [], limit=5)
    if llm_observations:
        evidence["llm_observations"] = llm_observations

    validation = dict(fallback.validation)
    validation["result"] = "draft_only"
    validation["llm_enhanced"] = True
    validation["pipeline"] = ["rule_analyzer", "llm_enhancer", "format_normalizer"]
    validation["llm_notes"] = string_list(validation_data.get("llm_notes"), [], limit=3)

    return XHSSeedSkillDraft(
        skill_id=fallback.skill_id,
        category=fallback.category,
        match=match,
        craft=craft,
        evidence=evidence,
        validation=validation,
        type=fallback.type,
        status=fallback.status,
        platform=fallback.platform,
        source_scope=fallback.source_scope,
    )


def mark_llm_fallback(draft: XHSSeedSkillDraft) -> XHSSeedSkillDraft:
    validation = dict(draft.validation)
    validation["result"] = "draft_only"
    validation["llm_enhanced"] = False
    validation["pipeline"] = ["rule_analyzer", "llm_enhancer_failed", "format_normalizer"]
    return XHSSeedSkillDraft(
        skill_id=draft.skill_id,
        category=draft.category,
        match=dict(draft.match),
        craft=dict(draft.craft),
        evidence=dict(draft.evidence),
        validation=validation,
        type=draft.type,
        status=draft.status,
        platform=draft.platform,
        source_scope=draft.source_scope,
    )


def text(value: Any, fallback: str, *, limit: int) -> str:
    text_value = str(value or "").strip()
    if not text_value:
        text_value = str(fallback or "").strip()
    return text_value[:limit]


def string_list(value: Any, fallback: list[Any], *, limit: int) -> list[str]:
    return dedupe(_shared_string_list(value, (str(item) for item in fallback)))[:limit]


def rule_items(value: Any, fallback: list[dict[str, Any]], *, limit: int) -> list[dict[str, str]]:
    if not isinstance(value, list):
        value = []
    items: list[dict[str, str]] = []
    for item in value:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name") or "").strip()
        rule = str(item.get("rule") or item.get("description") or "").strip()
        evidence = str(item.get("evidence") or "").strip()
        if name and rule:
            items.append({"name": name[:30], "rule": rule[:180], "evidence": evidence[:220]})
    if not items:
        for item in fallback:
            if not isinstance(item, dict):
                continue
            name = str(item.get("name") or "").strip()
            rule = str(item.get("rule") or "").strip()
            evidence = str(item.get("evidence") or "").strip()
            if name and rule:
                items.append({"name": name[:30], "rule": rule[:180], "evidence": evidence[:220]})
    return items[:limit]


def dedupe(items: list[str]) -> list[str]:
    return dedupe_preserve_order(items)


__all__ = [
    "SYSTEM_PROMPT",
    "USER_PROMPT",
    "dedupe",
    "enhance_note",
    "mark_llm_fallback",
    "normalize_llm_draft",
    "rule_items",
    "string_list",
    "text",
]
