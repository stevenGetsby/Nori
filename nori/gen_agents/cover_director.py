"""CoverDirectorAgent: 把 NoteDraft + skill + 用户参考图 装配成一张小红书封面图。

3 道 LLM 工序：
  1. CoverRefSelector  — 如果上游传了 tagged_assets（Intaker 打过语义标签），
                         用 LLM 从全量资产里选出本次封面需要的 0~N 张参考图
  2. CoverPromptWriter — 用 LLM 根据 skill.cover_rules / visual_rules + draft.title + bundle
                         写出一段 gpt-image-2 视觉 prompt
  3. CoverImageMaker   — 调 llms.image(prompt, reference_images=选出的参考图) 生图并落盘

失败抛 CoverDirectorError；不再走规则兜底。
"""
from __future__ import annotations

import base64
import json
import re
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any

import llms
from nori.agent_models import (
    AssetBundle,
    CoverResult,
    NoteDraft,
    NoteSkill,
    UserAsset,
)

from ._image_io import image_to_bytes


# 小红书封面贴近 3:4；relay::gpt-image-2 推荐 1072x1440
DEFAULT_SIZE = "1072x1440"

# 参考图硬上限（保护下游生图 API 上下文）。LLM 可以选 0～N 张。
MAX_REFERENCES = 8

# 旧路径（未传 tagged_assets）采用的软上限
MAX_PROMPT_REFERENCES = 3


class CoverDirectorError(RuntimeError):
    """CoverDirector 任一工序失败时抛出。"""


class CoverDirectorAgent:
    """根据 NoteDraft + skill + 参考图生成一张封面（纯 LLM）。"""

    def run(
        self,
        draft: NoteDraft,
        skill: NoteSkill | dict[str, Any],
        reference_assets: list[UserAsset] | None = None,
        *,
        out_dir: str | Path,
        size: str = DEFAULT_SIZE,
        intent: dict[str, Any] | None = None,
        tagged_assets: list[UserAsset] | None = None,
    ) -> CoverResult:
        skill_dict = _normalize_skill(skill)
        intent = dict(intent or {})

        if tagged_assets:
            ref_paths = _select_references_llm(draft, skill_dict, intent, tagged_assets)
        else:
            ref_paths = _collect_reference_paths(draft, reference_assets)

        prompt = _design_prompt_llm(draft, skill_dict, ref_paths, intent)

        # 参考图进入 llms.image 前先压缩，避免 relay::gpt-image-2 413
        ref_bytes = [b for b in (image_to_bytes(p) for p in ref_paths) if b]

        try:
            images = llms.image(
                prompt,
                usage="image",
                size=size,
                reference_images=ref_bytes or None,
            )
        except Exception as exc:  # noqa: BLE001
            raise CoverDirectorError(f"llms.image 失败: {type(exc).__name__}: {exc}") from exc

        if not images:
            raise CoverDirectorError("llms.image 没返回任何图")

        cover_path = _save_image(images[0], Path(out_dir), skill_dict.get("skill_id") or "cover")
        return CoverResult(
            cover_path=str(cover_path),
            prompt=prompt,
            size=size,
            reference_paths=ref_paths,
            source=images[0][:80],
        )


make_cover = CoverDirectorAgent().run


# ============ 工序 0（可选）：CoverRefSelector ============

def _select_references_llm(
    draft: NoteDraft,
    skill: dict[str, Any],
    intent: dict[str, Any],
    tagged_assets: list[UserAsset],
) -> list[str]:
    """从打过 vision tag 的资产里让 LLM 选 0~N 张作为封面参考。

    返回路径列表（去重、存在、上限 MAX_REFERENCES）；可以为空。
    """
    images = [
        {
            "index": i,
            "path": a.path,
            "subject": a.subject,
            "vision_roles": list(a.vision_roles),
            "brand_signals": list(a.brand_signals),
            "usable_for": list(a.usable_for),
            "quality": a.quality,
        }
        for i, a in enumerate(tagged_assets)
        if a.kind == "image" and a.path
    ]
    if not images:
        return []

    user_text = str(intent.get("user_text") or "").strip() or "用户未提供额外文本说明。"
    user_prompt = (
        f"小红书封面需要选择参考图。\n"
        f"用户原始诉求：{user_text}\n\n"
        f"note 标题：{draft.title}\n"
        f"语气：{skill.get('tone', '')}；类型：{skill.get('note_type', '')}\n"
        f"创作目标：{skill.get('creative_goal', '')}\n"
        f"用户意图：{json.dumps(intent, ensure_ascii=False)}\n\n"
        f"封面规则：{json.dumps(skill.get('cover_rules') or [], ensure_ascii=False)}\n"
        f"视觉规则：{json.dumps(skill.get('visual_rules') or [], ensure_ascii=False)}\n\n"
        f"资产池（已经被 Intaker 打过语义标签）：\n"
        f"{json.dumps(images, ensure_ascii=False, indent=2)}\n\n"
        "请结合用户原始诉求从资产池里选出本次封面需要作为参考的图片 index：\n"
        "  - 你可以选 0 张（纯文生图）、也可以选多张；推荐 1~5 张\n"
        "  - 优先 usable_for 包含 cover 的\n"
        "  - 优先 brand_signals 非空且跟 note 主题/用户诉求相关的\n"
        "  - usable_for=not_usable 或 quality=low 的不要选\n"
        "  - 不要选重复主体的图\n\n"
        '输出 JSON：{"chosen_indices": [<选中的 index>], "rationale": "<一句话说明为什么选这几张>"}'
    )

    data = _call_json(
        system="你是 Nori 的封面参考图选取工序，只输出 JSON。",
        user=user_prompt,
        timeout=45,
    )

    chosen = data.get("chosen_indices")
    if not isinstance(chosen, list):
        return []

    paths: list[str] = []
    seen: set[str] = set()
    for v in chosen:
        try:
            idx = int(v)
        except (TypeError, ValueError):
            continue
        if 0 <= idx < len(tagged_assets):
            a = tagged_assets[idx]
            if a.kind == "image" and a.path and a.path not in seen and Path(a.path).exists():
                paths.append(a.path)
                seen.add(a.path)
        if len(paths) >= MAX_REFERENCES:
            break
    return paths


# ============ 工序 1：CoverPromptWriter ============

def _design_prompt_llm(
    draft: NoteDraft,
    skill: dict[str, Any],
    reference_paths: list[str],
    intent: dict[str, Any],
) -> str:
    bundle_dict = draft.asset_bundle or {}
    brand_facts = list(bundle_dict.get("brand_facts") or [])
    text_points = list(bundle_dict.get("text_points") or [])

    user_prompt = (
        f"小红书 note 标题：{draft.title}\n"
        f"语气：{skill.get('tone', '')}；类型：{skill.get('note_type', '')}\n"
        f"创作目标：{skill.get('creative_goal', '')}\n"
        f"用户意图：{json.dumps(intent, ensure_ascii=False)}\n\n"
        f"品牌信息：{json.dumps(brand_facts, ensure_ascii=False)}\n"
        f"主要卖点：{json.dumps(text_points[:3], ensure_ascii=False)}\n\n"
        f"封面规则：\n{json.dumps(skill.get('cover_rules') or [], ensure_ascii=False, indent=2)}\n\n"
        f"视觉规则：\n{json.dumps(skill.get('visual_rules') or [], ensure_ascii=False, indent=2)}\n\n"
        f"禁止项：{json.dumps(skill.get('avoid_rules') or [], ensure_ascii=False)}\n"
        f"参考图数量：{len(reference_paths)}（已作为 reference_images 传给生图模型）\n\n"
        "请为这条小红书 note 写一段 gpt-image-2 视觉 prompt：\n"
        "  - 用一段英文叙述 + 中文标题文字（标题原样置入画面，6-14 字）\n"
        "  - 明确构图、主体、色彩、光线、风格、文字版式；3:4 竖图\n"
        "  - 若有参考图，请显式说明保留参考图的主体/品牌元素\n"
        "  - 不要硬广价格、不要伪造 logo / 第三方认证 / UI 截图\n\n"
        '只输出 JSON：{"prompt": "<一段完整的视觉 prompt>"}'
    )

    data = _call_json(
        system="你是 Nori 的封面 prompt 工序，只输出 JSON。",
        user=user_prompt,
        timeout=60,
    )
    prompt = str(data.get("prompt") or "").strip()
    if not prompt:
        raise CoverDirectorError("CoverPromptWriter 返回空 prompt")
    return prompt


# ============ 工序 2：保存图 ============

def _save_image(payload: str, out_dir: Path, skill_id: str) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_id = re.sub(r"[^\w\-]+", "_", skill_id)[:40] or "cover"

    if payload.startswith("data:"):
        header, _, b64 = payload.partition(",")
        mime = header.split(":", 1)[-1].split(";")[0] if ":" in header else "image/png"
        ext = mime.split("/")[-1] or "png"
        path = out_dir / f"cover_{safe_id}_{ts}.{ext}"
        try:
            path.write_bytes(base64.b64decode(b64))
        except (ValueError, TypeError) as exc:
            raise CoverDirectorError(f"data-uri base64 解析失败: {exc}") from exc
        return path

    path = out_dir / f"cover_{safe_id}_{ts}.png"
    try:
        req = urllib.request.Request(payload, headers={"User-Agent": "nori-cover-director/1.0"})
        with urllib.request.urlopen(req, timeout=60) as resp:  # noqa: S310 - controlled url from llms.image
            path.write_bytes(resp.read())
    except Exception as exc:  # noqa: BLE001
        raise CoverDirectorError(f"下载封面失败: {type(exc).__name__}: {exc}") from exc
    return path


# ============ 工具 ============

def _normalize_skill(skill: NoteSkill | dict[str, Any]) -> dict[str, Any]:
    if isinstance(skill, NoteSkill):
        return skill.to_dict()
    if isinstance(skill, dict):
        return skill
    raise TypeError(f"skill 必须是 NoteSkill 或 dict，收到 {type(skill)!r}")


def _collect_reference_paths(
    draft: NoteDraft,
    reference_assets: list[UserAsset] | None,
) -> list[str]:
    """优先用 draft.cover_path + image_paths（NoteMaker 已经判过主视觉）；都没有时回退到 assets。"""
    paths: list[str] = []
    seen: set[str] = set()

    def _add(p: str) -> None:
        if p and Path(p).exists() and p not in seen:
            paths.append(p)
            seen.add(p)

    if draft.cover_path:
        _add(draft.cover_path)
    for p in draft.image_paths:
        if len(paths) >= MAX_PROMPT_REFERENCES:
            break
        _add(p)

    if not paths and reference_assets:
        for a in reference_assets:
            if a.kind == "image":
                _add(a.path)
                if len(paths) >= MAX_PROMPT_REFERENCES:
                    break

    return paths[:MAX_PROMPT_REFERENCES]


def _call_json(*, system: str, user: str, timeout: int) -> dict[str, Any]:
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
        raise CoverDirectorError(f"LLM 输出无法解析为 JSON: {exc.preview!r}") from exc
    except Exception as exc:  # noqa: BLE001
        raise CoverDirectorError(f"llms.chat 失败: {type(exc).__name__}: {exc}") from exc
