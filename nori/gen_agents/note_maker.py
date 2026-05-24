"""NoteMakerAgent: 把 skill 列表 + 用户 assets 全程 LLM 装配成一篇 xhs note 草稿。

3 道 LLM 工序：
  1. SkillPicker   — 从 skill 列表挑 1 条最合适的
  2. AssetCurator  — 把图片/文本分门别类成 AssetBundle
  3. NoteComposer  — 一次性出标题 + 候选 + 正文 + tags + 钩子 + 自检

任何 LLM 调用失败都直接抛 NoteMakerLLMError，不再走规则兜底。
封面选 AssetBundle.main_images 的第一张（LLM 已经判定过哪些是主视觉）。
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import llms
from nori.agent_models import (
    AssetBundle,
    CandidateTitle,
    NoteDraft,
    NoteSkill,
    UserAsset,
)


class NoteMakerLLMError(RuntimeError):
    """LLM 任一工序失败时抛出。"""


class NoteMakerAgent:
    """根据 skill 列表 + 用户素材产出一篇 xhs note 草稿（纯 LLM）。"""

    def run(
        self,
        skills: list[NoteSkill | dict[str, Any]],
        assets: list[UserAsset | dict[str, Any]],
        *,
        intent: dict[str, Any] | None = None,
        context: dict[str, Any] | None = None,
    ) -> NoteDraft:
        intent = dict(intent or {})
        context = dict(context or {})
        norm_skills = [_normalize_skill(s) for s in skills if s]
        if not norm_skills:
            raise ValueError("NoteMakerAgent.run 需要至少一条 skill")
        norm_assets = [_normalize_asset(a) for a in assets if a]

        skill = norm_skills[0] if len(norm_skills) == 1 else _pick_skill_llm(norm_skills, intent, context)
        bundle = _curate_assets_llm(norm_assets, skill, intent)
        composed = _compose_note_llm(skill, bundle, intent)
        cover_path, image_paths = _pick_visual_paths(bundle)

        return NoteDraft(
            skill_id=str(skill.get("skill_id") or ""),
            title=composed["title"],
            body=composed["body"],
            tags=composed["tags"],
            comment_hook=composed["comment_hook"],
            cover_path=cover_path,
            image_paths=image_paths,
            candidate_titles=composed["candidate_titles"],
            metrics_target=_metrics_target(skill),
            asset_bundle=bundle.to_dict(),
            validation=composed["validation"],
            llm_enhanced=True,
        )


make_note = NoteMakerAgent().run


# ============ 工序 1：SkillPicker ============

def _pick_skill_llm(
    skills: list[dict[str, Any]],
    intent: dict[str, Any],
    context: dict[str, Any],
) -> dict[str, Any]:
    summary = [
        {
            "skill_id": s.get("skill_id"),
            "label": s.get("label"),
            "goal": s.get("goal"),
            "tone": s.get("tone"),
            "note_type": s.get("note_type"),
            "creative_goal": s.get("creative_goal"),
            "metrics_summary": s.get("metrics_summary"),
        }
        for s in skills
    ]
    data = _call_json(
        system="你是 Nori 的 Skill 选择器，只输出 JSON。",
        user=(
            f"用户意图：\n{json.dumps(intent, ensure_ascii=False)}\n\n"
            f"上下文：\n{json.dumps(context, ensure_ascii=False)}\n\n"
            f"候选 skill：\n{json.dumps(summary, ensure_ascii=False, indent=2)}\n\n"
            '选 1 个最契合用户意图的 skill。输出 {"skill_id": "..."}。'
        ),
        timeout=30,
    )
    chosen_id = str(data.get("skill_id") or "").strip()
    for skill in skills:
        if skill.get("skill_id") == chosen_id:
            return skill
    raise NoteMakerLLMError(f"SkillPicker 返回未知 skill_id: {chosen_id!r}")


# ============ 工序 2：AssetCurator ============

def _curate_assets_llm(
    assets: list[UserAsset],
    skill: dict[str, Any],
    intent: dict[str, Any],
) -> AssetBundle:
    images = [(i, a) for i, a in enumerate(assets) if a.kind == "image"]
    texts = [(i, a) for i, a in enumerate(assets) if a.kind == "text" and a.text.strip()]

    image_input = [
        {
            "index": i,
            "path": a.path,
            "vision_roles": list(a.vision_roles),
            "subject": a.subject,
            "brand_signals": list(a.brand_signals),
            "usable_for": list(a.usable_for),
            "quality": a.quality,
        }
        for i, a in images
    ]
    text_input = [
        {"index": i, "text": a.text.strip()[:400]}
        for i, a in texts
    ]

    if not image_input and not text_input:
        return AssetBundle()

    data = _call_json(
        system="你是 Nori 的素材整理工序，只输出 JSON。",
        user=(
            f"创作目标：{skill.get('creative_goal', '')}\n"
            f"语气：{skill.get('tone', '')}；类型：{skill.get('note_type', '')}\n"
            f"用户意图：{json.dumps(intent, ensure_ascii=False)}\n\n"
            f"图片素材（按 index 引用）：\n{json.dumps(image_input, ensure_ascii=False, indent=2)}\n\n"
            f"文本素材（按 index 引用）：\n{json.dumps(text_input, ensure_ascii=False, indent=2)}\n\n"
            "请把素材整理成 5 个桶：\n"
            "  - main_image_indices：主视觉图片 index（封面优先）\n"
            "  - aux_image_indices：辅助图 index\n"
            "  - text_points：用户的卖点/描述短句\n"
            "  - brand_facts：品牌名/口号/理念/人设\n"
            "  - data_points：数据/数字/案例\n"
            "保留原文，不要改写。每个文本桶最多 6 条。\n"
            '输出 JSON：{"main_image_indices": [], "aux_image_indices": [], '
            '"text_points": [], "brand_facts": [], "data_points": []}'
        ),
        timeout=60,
    )

    bundle = AssetBundle()
    main_idx = _int_list(data.get("main_image_indices"))
    aux_idx = _int_list(data.get("aux_image_indices"))
    used: set[int] = set()
    for i in main_idx:
        if 0 <= i < len(assets) and assets[i].kind == "image" and i not in used:
            bundle.main_images.append(assets[i])
            used.add(i)
    for i in aux_idx:
        if 0 <= i < len(assets) and assets[i].kind == "image" and i not in used:
            bundle.aux_images.append(assets[i])
            used.add(i)
    for i, a in images:
        if i not in used:
            bundle.aux_images.append(a)
    if not bundle.main_images and bundle.aux_images:
        bundle.main_images.append(bundle.aux_images.pop(0))

    bundle.text_points = _str_list(data.get("text_points"))[:6]
    bundle.brand_facts = _str_list(data.get("brand_facts"))[:6]
    bundle.data_points = _str_list(data.get("data_points"))[:6]
    return bundle


# ============ 工序 3：NoteComposer ============

def _compose_note_llm(
    skill: dict[str, Any],
    bundle: AssetBundle,
    intent: dict[str, Any],
) -> dict[str, Any]:
    data = _call_json(
        system="你是 Nori 的小红书 note 写手，只输出 JSON。",
        user=(
            f"创作目标：{skill.get('creative_goal', '')}\n"
            f"语气：{skill.get('tone', '')}；类型：{skill.get('note_type', '')}\n"
            f"用户意图：{json.dumps(intent, ensure_ascii=False)}\n\n"
            f"素材卖点：{json.dumps(bundle.text_points, ensure_ascii=False)}\n"
            f"品牌信息：{json.dumps(bundle.brand_facts, ensure_ascii=False)}\n"
            f"数据点：{json.dumps(bundle.data_points, ensure_ascii=False)}\n\n"
            f"标题规则：\n{json.dumps(skill.get('title_rules') or [], ensure_ascii=False, indent=2)}\n\n"
            f"开场规则：\n{json.dumps(skill.get('opening_rules') or [], ensure_ascii=False, indent=2)}\n\n"
            f"正文结构：\n{json.dumps(skill.get('body_structure') or [], ensure_ascii=False, indent=2)}\n\n"
            f"互动规则：\n{json.dumps(skill.get('interaction_rules') or [], ensure_ascii=False, indent=2)}\n\n"
            f"禁止项：{json.dumps(skill.get('avoid_rules') or [], ensure_ascii=False)}\n\n"
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

    title = str(data.get("title") or "").strip()
    body = str(data.get("body") or "").strip()
    if not title or not body:
        raise NoteMakerLLMError("NoteComposer 缺 title 或 body")

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

    tags = [str(t).strip() for t in (data.get("tags") or []) if str(t).strip()][:5]
    hook = str(data.get("comment_hook") or "").strip()

    validation = data.get("validation") if isinstance(data.get("validation"), dict) else {}
    status = str(validation.get("status") or "pass").strip() or "pass"
    issues = [str(x).strip() for x in (validation.get("issues") or []) if str(x).strip()]

    return {
        "title": title,
        "body": body,
        "tags": tags,
        "comment_hook": hook,
        "candidate_titles": candidates,
        "validation": {"status": status, "issues": issues},
    }


# ============ 视觉路径 ============

def _pick_visual_paths(bundle: AssetBundle) -> tuple[str, list[str]]:
    """封面=第一张 main_images；其余进图集，xhs 9 图上限内取 8 张。"""
    cover = bundle.main_images[0].path if bundle.main_images else ""
    others = [a.path for a in bundle.main_images[1:] + bundle.aux_images if a.path]
    return cover, others[:8]


# ============ 工具 ============

def _normalize_skill(skill: NoteSkill | dict[str, Any]) -> dict[str, Any]:
    if isinstance(skill, NoteSkill):
        return skill.to_dict()
    if isinstance(skill, dict):
        return skill
    raise TypeError(f"skill 必须是 NoteSkill 或 dict，收到 {type(skill)!r}")


def _normalize_asset(asset: UserAsset | dict[str, Any]) -> UserAsset:
    if isinstance(asset, UserAsset):
        return asset
    if isinstance(asset, dict):
        kind = str(asset.get("kind") or "").strip()
        if not kind:
            kind = "image" if asset.get("path") else "text"
        return UserAsset(
            kind=kind,
            path=str(asset.get("path") or ""),
            text=str(asset.get("text") or ""),
            vision_roles=[str(v) for v in (asset.get("vision_roles") or [])],
            subject=str(asset.get("subject") or ""),
            brand_signals=[str(s) for s in (asset.get("brand_signals") or [])],
            usable_for=[str(u) for u in (asset.get("usable_for") or [])],
            quality=str(asset.get("quality") or ""),
        )
    if isinstance(asset, (str, Path)):
        path = str(asset)
        if path and Path(path).suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".gif"}:
            return UserAsset(kind="image", path=path)
        return UserAsset(kind="text", text=path)
    raise TypeError(f"asset 必须是 UserAsset / dict / 路径，收到 {type(asset)!r}")


def _metrics_target(skill: dict[str, Any]) -> dict[str, Any]:
    summary = skill.get("metrics_summary") or {}
    return {
        "liked_target": summary.get("liked_p50") or summary.get("liked_p75") or 0,
        "collected_target": summary.get("collected_p50") or 0,
        "sample": summary.get("sample") or 0,
    }


def _int_list(value: Any) -> list[int]:
    out: list[int] = []
    for v in value or []:
        try:
            out.append(int(v))
        except (TypeError, ValueError):
            continue
    return out


def _str_list(value: Any) -> list[str]:
    return [str(v).strip() for v in (value or []) if str(v).strip()]


def _call_json(*, system: str, user: str, timeout: int) -> dict[str, Any]:
    """统一的 LLM JSON 调用入口，失败一律抛 NoteMakerLLMError。"""
    try:
        return llms.chat_json(
            [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            usage="llm",
            timeout=timeout,
            _chat=llms.chat,
        )
    except llms.ChatJSONError as exc:
        raise NoteMakerLLMError(f"LLM 输出无法解析为 JSON: {exc.preview!r}") from exc
    except Exception as exc:  # noqa: BLE001
        raise NoteMakerLLMError(f"llms.chat 失败: {type(exc).__name__}: {exc}") from exc
