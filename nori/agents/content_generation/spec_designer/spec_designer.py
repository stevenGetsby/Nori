"""Design-spec stage for content generation."""
from __future__ import annotations

from typing import Any

from nori.agents.content_generation.models import ContentDesignSpec
from nori.agents.content_generation.social_card_guides import (
    social_card_acceptance_checks,
    social_card_profile,
    social_card_visual_rules,
)
from nori.agents.market_analysis.models import NoteSkill
from nori.context import ContextView
from nori.core import AccountOperationProject, AgentBase, ClientBrief, ContentTask, IntentContract, LLMFactory, UserAsset


class ContentSpecAgent(AgentBase):
    """Convert task, brief, assets, and skills into an inspectable generation spec.

    This stage decides structure, rules, media intent, and acceptance checks.
    It intentionally does not write final copy or call image generation.
    """

    stage_name = "content_spec"

    def __init__(self, *, llm_factory: LLMFactory | None = None) -> None:
        super().__init__(stage_name=self.stage_name, use_llm=False, llm_factory=llm_factory)

    def run(
        self,
        *,
        task: ContentTask | dict[str, Any] | None = None,
        skills: list[NoteSkill | dict[str, Any]] | None = None,
        assets: list[UserAsset | dict[str, Any]] | None = None,
        client_brief: ClientBrief | dict[str, Any] | None = None,
        project: AccountOperationProject | None = None,
        intent_contract: IntentContract | dict[str, Any] | None = None,
        intent: dict[str, Any] | None = None,
        context: dict[str, Any] | None = None,
        context_view: ContextView | dict[str, Any] | None = None,
    ) -> ContentDesignSpec:
        view = _normalize_context_view(context_view)
        if view is not None:
            payload = view.payload
            task = task or payload.get("task_intent")
            skills = skills or payload.get("learned_skills", {}).get("skills")
            assets = assets or payload.get("asset_context", {}).get("assets")
            intent = {**payload.get("content_strategy", {}), **dict(intent or {})}
            context = {
                **payload,
                "constraints": [
                    *payload.get("constraints", {}).get("constraints", []),
                    *payload.get("constraints", {}).get("task_notes", []),
                    *list((context or {}).get("constraints", []) if isinstance(context, dict) else []),
                ],
            }
        normalized_task = _normalize_task(task)
        brief = _normalize_brief(client_brief or (project.client_brief if project else None))
        contract = _normalize_contract(intent_contract)
        normalized_skills = [_normalize_skill(skill) for skill in (skills or []) if skill]
        selected = _select_skills(normalized_skills, normalized_task)
        selected_refs = [_skill_ref(skill) for skill in selected]
        artifact_type = _artifact_type(normalized_task)
        normalized_assets = _normalize_assets(assets)
        social_profile = social_card_profile(normalized_task, artifact_type=artifact_type, assets=normalized_assets)
        hotspot_strategy = _hotspot_strategy(context, normalized_task)
        acceptance_checks = _acceptance_checks(contract, brief, selected)
        if social_profile:
            acceptance_checks = _dedupe([*acceptance_checks, *social_card_acceptance_checks(social_profile)])
        if hotspot_strategy:
            acceptance_checks = _dedupe([
                *acceptance_checks,
                "校验热点证据来源或明确标注假设",
                "确认账号参与角度可信，不硬蹭热点",
                "首图必须一眼看懂，不只做氛围图",
                "避免伪造体验、截图、官方背书或夸大承诺",
            ])
        metadata = {
            "designer": self.__class__.__name__,
            "skill_count": len(normalized_skills),
            "selected_skill_count": len(selected),
            **({"context_view": {"agent_name": view.agent_name, "slice_kinds": view.kinds}} if view else {}),
        }
        if social_profile:
            metadata["social_card_profile"] = {
                "source": social_profile.get("source", ""),
                "platform": social_profile.get("platform", ""),
                "artifact": social_profile.get("artifact", ""),
            }
        if hotspot_strategy:
            metadata["hotspot_strategy"] = hotspot_strategy
            metadata["human_review_checklist"] = [
                "热点证据可追溯或已明确标注假设",
                "账号参与角度可信，不显得硬蹭",
                "首图能在一眼内说明利益点",
                "没有伪造体验、截图、官方背书或夸大承诺",
            ]

        return ContentDesignSpec(
            spec_id=f"spec_{normalized_task.task_id or 'default'}",
            task_id=normalized_task.task_id,
            platform=normalized_task.platform or brief.platform,
            artifact_type=artifact_type,
            content_type=normalized_task.content_type,
            goal=normalized_task.objective or (brief.goals[0] if brief.goals else ""),
            audience=list(brief.audience),
            creative_angle=_creative_angle(selected, normalized_task, intent),
            selected_skill_refs=selected_refs,
            evidence_refs=_evidence_refs(normalized_task, selected),
            structure=_structure(selected, normalized_task, context, social_profile),
            media_plan=_media_plan(selected, normalized_task, normalized_assets, social_profile),
            copy_rules=_copy_rules(selected),
            visual_rules=_visual_rules(selected, social_profile),
            constraints=_constraints(brief, normalized_task, context),
            acceptance_checks=acceptance_checks,
            metadata=metadata,
        )


def _normalize_context_view(value: ContextView | dict[str, Any] | None) -> ContextView | None:
    if value is None:
        return None
    if isinstance(value, ContextView):
        return value
    if isinstance(value, dict):
        from nori.context.models import ContextSlice, ContextTrace

        slices = [ContextSlice.from_dict(item) for item in value.get("slices") or []]
        if not slices and value.get("payload"):
            payload = dict(value.get("payload") or {})
            kinds = [str(item) for item in value.get("kinds") or payload.keys()]
            slices = [ContextSlice(kind=kind, payload=dict(payload.get(kind) or {})) for kind in kinds]
        return ContextView(
            agent_name=str(value.get("agent_name") or ""),
            task_id=str(value.get("task_id") or ""),
            slices=slices,
            trace=ContextTrace(**dict(value.get("trace") or {})) if value.get("trace") else ContextTrace(),
        )
    return None


def _normalize_task(value: ContentTask | dict[str, Any] | None) -> ContentTask:
    if isinstance(value, ContentTask):
        return value
    return ContentTask.from_dict(value)


def _normalize_brief(value: ClientBrief | dict[str, Any] | None) -> ClientBrief:
    if isinstance(value, ClientBrief):
        return value
    return ClientBrief.from_dict(value)


def _normalize_contract(value: IntentContract | dict[str, Any] | None) -> IntentContract:
    if isinstance(value, IntentContract):
        return value
    return IntentContract.from_dict(value)


def _normalize_skill(value: NoteSkill | dict[str, Any]) -> dict[str, Any]:
    if isinstance(value, NoteSkill):
        return value.to_dict()
    return dict(value) if isinstance(value, dict) else {}


def _normalize_assets(values: list[UserAsset | dict[str, Any]] | None) -> list[UserAsset]:
    out: list[UserAsset] = []
    for value in values or []:
        if isinstance(value, UserAsset):
            out.append(value)
        elif isinstance(value, dict):
            out.append(UserAsset.from_dict(value))
    return out


def _select_skills(skills: list[dict[str, Any]], task: ContentTask) -> list[dict[str, Any]]:
    if not skills:
        return []
    content_type = (task.content_type or "").lower()
    if content_type in {"video", "video_script"}:
        video_skills = [skill for skill in skills if str(skill.get("note_type") or "").lower() in {"video", "视频"}]
        if video_skills:
            return video_skills[:1]
    return skills[:1]


def _skill_ref(skill: dict[str, Any]) -> dict[str, Any]:
    return {
        "skill_id": str(skill.get("skill_id") or ""),
        "label": str(skill.get("label") or ""),
    }


def _artifact_type(task: ContentTask) -> str:
    content_type = str(task.content_type or "note").strip().lower()
    platform = str(task.platform or "xhs").strip().lower()
    if platform in {"wechat", "wechat_public_account", "公众号"} or content_type in {"article", "公众号文章"}:
        return "article"
    if content_type in {"video", "video_script", "短视频"}:
        return "video_script"
    if content_type in {"image_text", "image_text_post", "图文"}:
        return "image_text_post"
    return "note"


def _creative_angle(skills: list[dict[str, Any]], task: ContentTask, intent: dict[str, Any] | None) -> str:
    if intent and intent.get("creative_angle"):
        return str(intent["creative_angle"])
    if skills and skills[0].get("creative_goal"):
        return str(skills[0]["creative_goal"])
    return task.topic or task.title


def _evidence_refs(task: ContentTask, skills: list[dict[str, Any]]) -> list[dict[str, Any]]:
    refs = [dict(ref) for ref in task.references]
    for skill in skills:
        for note in skill.get("evidence_notes") or []:
            if isinstance(note, dict):
                refs.append({
                    "source": "note_skill_evidence",
                    "skill_id": skill.get("skill_id", ""),
                    "note_id": note.get("note_id", ""),
                    "note_url": note.get("note_url", ""),
                })
    return refs


def _structure(
    skills: list[dict[str, Any]],
    task: ContentTask,
    context: dict[str, Any] | None = None,
    social_profile: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    skill = skills[0] if skills else {}
    if _artifact_type(task) == "image_text_post":
        market = _context_mapping(context, "market_hotspots")
        strategy = _context_mapping(context, "content_strategy")
        topic = task.topic or strategy.get("creative_angle") or task.title
        rows = [
            {"slot": "cover", "purpose": "首图一眼看懂热点/利益点，封面文字 6-14 字。"},
            {"slot": "hotspot_bridge", "purpose": _hotspot_bridge_purpose(market, topic)},
            {"slot": "account_fit", "purpose": "说明账号、产品或场景为什么有资格参与这个热点。"},
            {"slot": "proof_or_example", "purpose": _first_rule(skill.get("body_structure"), fallback="用真实素材、样本证据或用户场景支撑观点。")},
            {"slot": "method_or_choice", "purpose": "给出可保存的选择方法、步骤、清单或避坑判断。"},
            {"slot": "save_or_comment_cta", "purpose": _first_rule(skill.get("interaction_rules"), fallback="用收藏、评论或到店动作收口。")},
        ]
        return _merge_social_page_roles(rows, social_profile)
    rows = [
        {"slot": "title", "purpose": _first_rule(skill.get("title_rules"), fallback=task.title or task.topic)},
        {"slot": "opening", "purpose": _first_rule(skill.get("opening_rules"), fallback="先承接用户场景或痛点。")},
        {"slot": "body", "purpose": _first_rule(skill.get("body_structure"), fallback="展开核心卖点、证据和行动理由。")},
        {"slot": "interaction", "purpose": _first_rule(skill.get("interaction_rules"), fallback="用评论或收藏动作收口。")},
    ]
    if _artifact_type(task) == "video_script":
        rows.insert(0, {"slot": "hook", "purpose": "前 3 秒先抛主题或情绪。"})
    if _artifact_type(task) == "article":
        rows = [
            {"slot": "headline", "purpose": task.title or task.topic},
            {"slot": "lead", "purpose": "导语先交代核心观点和读者收益。"},
            {"slot": "sections", "purpose": "用分节论证观点，穿插案例和素材。"},
            {"slot": "ending", "purpose": "收束观点并给出行动建议。"},
        ]
    return rows


def _media_plan(
    skills: list[dict[str, Any]],
    task: ContentTask,
    assets: list[UserAsset],
    social_profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    image_count = sum(1 for asset in assets if asset.kind == "image")
    skill = skills[0] if skills else {}
    artifact_type = _artifact_type(task)
    plan = {
        "cover": {
            "required": artifact_type in {"note", "image_text_post", "video_script"},
            "rules": list(skill.get("cover_rules") or []),
        },
        "gallery": {
            "required": artifact_type == "image_text_post" or (task.platform == "xhs" and artifact_type == "note"),
            "available_image_count": image_count,
        },
        "video": {
            "required": artifact_type == "video_script",
        },
    }
    if social_profile:
        key = "wechat_cover_pair" if social_profile.get("platform") == "wechat" else "social_card"
        plan[key] = social_profile
    return plan


def _copy_rules(skills: list[dict[str, Any]]) -> dict[str, Any]:
    skill = skills[0] if skills else {}
    return {
        "title_rules": list(skill.get("title_rules") or []),
        "opening_rules": list(skill.get("opening_rules") or []),
        "body_structure": list(skill.get("body_structure") or []),
        "interaction_rules": list(skill.get("interaction_rules") or []),
    }


def _visual_rules(skills: list[dict[str, Any]], social_profile: dict[str, Any] | None = None) -> dict[str, Any]:
    skill = skills[0] if skills else {}
    rules = {
        "visual_rules": list(skill.get("visual_rules") or []),
        "cover_rules": list(skill.get("cover_rules") or []),
    }
    social_rules = social_card_visual_rules(social_profile or {})
    if social_rules:
        rules["social_card"] = social_rules
    return rules


def _constraints(brief: ClientBrief, task: ContentTask, context: dict[str, Any] | None) -> list[str]:
    values = [*brief.constraints, *task.notes]
    for item in (context or {}).get("constraints", []) if isinstance(context, dict) else []:
        values.append(str(item))
    return _dedupe(values)


def _acceptance_checks(contract: IntentContract, brief: ClientBrief, skills: list[dict[str, Any]]) -> list[str]:
    checks: list[str] = []
    for item in contract.must_include:
        checks.append(f"必须包含：{item}")
    for item in [*brief.taboos, *contract.taboos]:
        checks.append(f"避免：{item}")
    for skill in skills:
        for item in skill.get("avoid_rules") or []:
            checks.append(f"避免：{item}")
    return _dedupe(checks)


def _hotspot_strategy(context: dict[str, Any] | None, task: ContentTask) -> dict[str, Any]:
    if _artifact_type(task) != "image_text_post":
        return {}
    market = _context_mapping(context, "market_hotspots")
    strategy = _context_mapping(context, "content_strategy")
    platform = _context_mapping(context, "platform_strategy")
    if not market and not strategy and not platform:
        return {}
    return {
        "mode": "hotspot_image_post",
        "keywords": [str(item) for item in market.get("keywords") or [] if str(item or "")],
        "hot_examples": [dict(item) for item in market.get("hot_examples") or [] if isinstance(item, dict)][:5],
        "trend_insights": [str(item) for item in market.get("trend_insights") or [] if str(item or "")][:5],
        "platform_rules": [dict(item) for item in platform.get("rules") or [] if isinstance(item, dict)][:5],
        "creative_angle": str(strategy.get("creative_angle") or ""),
    }


def _context_mapping(context: dict[str, Any] | None, key: str) -> dict[str, Any]:
    value = (context or {}).get(key) if isinstance(context, dict) else None
    return dict(value) if isinstance(value, dict) else {}


def _hotspot_bridge_purpose(market: dict[str, Any], topic: str) -> str:
    insights = [str(item) for item in market.get("trend_insights") or [] if str(item or "")]
    if insights:
        return f"用热点洞察承接主题：{insights[0]}"
    return f"把热点语境自然转到账号主题：{topic}"


def _merge_social_page_roles(
    rows: list[dict[str, Any]],
    social_profile: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    if not social_profile:
        return rows
    role_by_slot = {
        str(item.get("slot") or ""): item
        for item in social_profile.get("page_plan") or []
        if isinstance(item, dict)
    }
    merged = []
    for row in rows:
        enriched = dict(row)
        role = role_by_slot.get(str(row.get("slot") or ""))
        if role:
            enriched.update({
                "page_role": str(role.get("role") or ""),
                "visual_intent": str(role.get("intent") or ""),
                "source": social_profile.get("source", ""),
            })
        merged.append(enriched)
    return merged


def _first_rule(rows: Any, *, fallback: str) -> str:
    for row in rows or []:
        if isinstance(row, dict) and row.get("rule"):
            return str(row["rule"])
    return fallback


def _dedupe(values: list[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for value in values:
        text = str(value or "").strip()
        if text and text not in seen:
            out.append(text)
            seen.add(text)
    return out


__all__ = ["ContentSpecAgent"]
