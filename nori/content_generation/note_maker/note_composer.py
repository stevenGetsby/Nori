"""Note composition helpers for NoteMakerAgent."""
from __future__ import annotations

from typing import Any, Callable

from nori.content_generation.models import AssetBundle, CandidateTitle
from nori.shared.prompting import json_block, json_prompt
from . import prompts as _prompts


JsonCall = Callable[..., dict[str, Any]]


def compose_note_llm(
    skill: dict[str, Any],
    bundle: AssetBundle,
    intent: dict[str, Any],
    *,
    json_call: JsonCall,
    error_type=RuntimeError,
) -> dict[str, Any]:
    """Compose note fields from selected skill and curated assets."""
    data = json_call(
        system=_prompts.NOTE_COMPOSER_SYSTEM_PROMPT,
        user=(
            f"创作目标：{skill.get('creative_goal', '')}\n"
            f"语气：{skill.get('tone', '')}；类型：{skill.get('note_type', '')}\n"
            f"用户意图：{json_prompt(intent)}\n\n"
            f"素材卖点：{json_prompt(bundle.text_points)}\n"
            f"品牌信息：{json_prompt(bundle.brand_facts)}\n"
            f"数据点：{json_prompt(bundle.data_points)}\n\n"
            f"标题规则：\n{json_block(skill.get('title_rules') or [])}\n\n"
            f"开场规则：\n{json_block(skill.get('opening_rules') or [])}\n\n"
            f"正文结构：\n{json_block(skill.get('body_structure') or [])}\n\n"
            f"互动规则：\n{json_block(skill.get('interaction_rules') or [])}\n\n"
            f"禁止项：{json_prompt(skill.get('avoid_rules') or [])}\n\n"
            "按规则写一篇可发布的小红书 note：\n"
            "  - title：推荐标题，<=24 字\n"
            "  - candidate_titles：3-5 个候选，每个含 text / rule_name（命中的 title_rules.name）/ rationale\n"
            "  - body：开场 → 主体段落 → 互动钩子，<=300 字\n"
            "  - tags：3-5 个，每个 <=8 字\n"
            "  - comment_hook：评论引导一句话\n"
            "  - validation：{status: pass|needs_human_review, issues: [...]}"
            "，命中禁止项时 status=needs_human_review\n\n"
            '输出 JSON：{"title":"","candidate_titles":[],'
            '"body":"","tags":[],"comment_hook":"","validation":{"status":"","issues":[]}}'
        ),
        timeout=90,
    )
    return normalize_composed_note(data, error_type=error_type)


def normalize_composed_note(
    data: dict[str, Any],
    *,
    error_type=RuntimeError,
) -> dict[str, Any]:
    """Normalize composer JSON into NoteDraft constructor-ready fields."""
    title = str(data.get("title") or "").strip()
    body = str(data.get("body") or "").strip()
    if not title or not body:
        raise error_type("NoteComposer 缺 title 或 body")

    candidates: list[CandidateTitle] = []
    for item in data.get("candidate_titles") or []:
        if isinstance(item, dict) and item.get("text"):
            candidates.append(CandidateTitle(
                text=str(item["text"]).strip()[:30],
                rule_name=str(item.get("rule_name") or "").strip(),
                rationale=str(item.get("rationale") or "").strip(),
            ))
    if not candidates:
        candidates.append(CandidateTitle(text=title, rule_name="", rationale=""))

    tags = [str(tag).strip() for tag in (data.get("tags") or []) if str(tag).strip()][:5]
    hook = str(data.get("comment_hook") or "").strip()

    validation = data.get("validation") if isinstance(data.get("validation"), dict) else {}
    status = str(validation.get("status") or "pass").strip() or "pass"
    issues = [str(item).strip() for item in (validation.get("issues") or []) if str(item).strip()]

    return {
        "title": title,
        "body": body,
        "tags": tags,
        "comment_hook": hook,
        "candidate_titles": candidates,
        "validation": {"status": status, "issues": issues},
    }


__all__ = ["compose_note_llm", "normalize_composed_note"]
