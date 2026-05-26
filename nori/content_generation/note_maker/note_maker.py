"""NoteMakerAgent: 把 skill 列表 + 用户 assets 全程 LLM 装配成一篇 xhs note 草稿。

3 道 LLM 工序：
  1. SkillPicker   — 从 skill 列表挑 1 条最合适的
  2. AssetCurator  — 把图片/文本分门别类成 AssetBundle
  3. NoteComposer  — 一次性出标题 + 候选 + 正文 + tags + 钩子 + 自检

任何 LLM 调用失败都直接抛 NoteMakerLLMError，不再走规则兜底。
封面选 AssetBundle.main_images 的第一张（LLM 已经判定过哪些是主视觉）。
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from nori.core import AgentBase, LLMFactory
from nori.shared.llm_json import call_stage_json
from nori.content_generation.models import NoteDraft, UserAsset
from nori.market_analysis.models import NoteSkill

from . import asset_curator as _asset_curator
from . import note_composer as _note_composer
from . import skill_picker as _skill_picker


class NoteMakerLLMError(RuntimeError):
    """LLM 任一工序失败时抛出。"""


class NoteMakerAgent(AgentBase):
    """根据 skill 列表 + 用户素材产出一篇 xhs note 草稿（纯 LLM）。"""

    stage_name = "note_maker"

    def __init__(self, *, llm_factory: LLMFactory | None = None) -> None:
        super().__init__(stage_name=self.stage_name, use_llm=True, llm_factory=llm_factory)

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

        skill = norm_skills[0] if len(norm_skills) == 1 else _skill_picker.pick_skill_llm(
            norm_skills,
            intent,
            context,
            json_call=self._call_json,
            error_type=NoteMakerLLMError,
        )
        bundle = _asset_curator.curate_assets_llm(norm_assets, skill, intent, json_call=self._call_json)
        composed = _note_composer.compose_note_llm(
            skill,
            bundle,
            intent,
            json_call=self._call_json,
            error_type=NoteMakerLLMError,
        )
        cover_path, image_paths = _asset_curator.pick_visual_paths(bundle)

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

    def _call_json(self, *, system: str, user: str, timeout: int) -> dict[str, Any]:
        """统一的 LLM JSON 调用入口，失败一律抛 NoteMakerLLMError。"""
        return call_stage_json(
            system=system,
            user=user,
            timeout=timeout,
            error_type=NoteMakerLLMError,
            chat_func=self.llm_factory.chat_func,
            chat_json_func=self.llm_factory.chat_json_func,
        )


make_note = NoteMakerAgent().run


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
        return UserAsset.from_dict(asset)
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
