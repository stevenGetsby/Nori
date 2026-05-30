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

import urllib.request
from pathlib import Path
from typing import Any

from nori.core import AgentBase, ImageCapabilityError, LLMFactory
from nori.shared.llm_json import call_stage_json
from nori.content_generation.models import CoverResult, NoteDraft
from nori.core import UserAsset
from nori.market_analysis.models import NoteSkill

from . import output as _cover_output
from .package import (
    DEFAULT_MAX_PROMPT_REFERENCES,
    DEFAULT_MAX_REFERENCES,
    CoverPromptBuilder,
    CoverReferenceSelector,
)


# 小红书封面贴近 3:4；relay::gpt-image-2 推荐 1072x1440
DEFAULT_SIZE = "1072x1440"

# 参考图硬上限（保护下游生图 API 上下文）。LLM 可以选 0～N 张。
MAX_REFERENCES = DEFAULT_MAX_REFERENCES

# 旧路径（未传 tagged_assets）采用的软上限
MAX_PROMPT_REFERENCES = DEFAULT_MAX_PROMPT_REFERENCES


class CoverDirectorError(RuntimeError):
    """CoverDirector 任一工序失败时抛出。"""


class CoverDirectorAgent(AgentBase):
    """根据 NoteDraft + skill + 参考图生成一张封面（纯 LLM）。"""

    stage_name = "cover_director"

    def __init__(self, *, llm_factory: LLMFactory | None = None) -> None:
        super().__init__(stage_name=self.stage_name, use_llm=True, llm_factory=llm_factory)
        self.reference_selector = CoverReferenceSelector()
        self.prompt_builder = CoverPromptBuilder()

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
            ref_paths = self.reference_selector.select_with_llm(
                draft,
                skill_dict,
                intent,
                tagged_assets,
                json_call=self._call_json,
                max_references=MAX_REFERENCES,
            )
        else:
            ref_paths = self.reference_selector.collect_legacy_paths(
                draft,
                reference_assets,
                max_references=MAX_PROMPT_REFERENCES,
            )

        prompt = self.prompt_builder.design_with_llm(
            draft,
            skill_dict,
            ref_paths,
            intent,
            json_call=self._call_json,
            error_type=CoverDirectorError,
        )

        # Local references are compressed before llms.image; remote URLs are
        # preserved because relay::gpt-image-2 accepts URL refs but rejects base64.
        ref_inputs = [self.reference_selector.to_image_input(p) for p in ref_paths]
        ref_inputs = [item for item in ref_inputs if item]

        reference_images_sent = bool(ref_inputs)
        reference_fallback = ""
        try:
            images = self.llm_factory.image(
                prompt,
                usage="image",
                size=size,
                reference_images=ref_inputs or None,
            )
        except ImageCapabilityError as exc:
            if not _has_local_reference_inputs(ref_inputs):
                raise CoverDirectorError(f"llms.image 失败: {type(exc).__name__}: {exc}") from exc
            reference_images_sent = False
            reference_fallback = "local_refs_not_supported"
            try:
                images = self.llm_factory.image(
                    prompt,
                    usage="image",
                    size=size,
                    reference_images=None,
                )
            except Exception as retry_exc:  # noqa: BLE001
                raise CoverDirectorError(
                    f"llms.image 失败: {type(retry_exc).__name__}: {retry_exc}"
                ) from retry_exc
        except Exception as exc:  # noqa: BLE001
            raise CoverDirectorError(f"llms.image 失败: {type(exc).__name__}: {exc}") from exc

        if not images:
            raise CoverDirectorError("llms.image 没返回任何图")

        cover_path = _cover_output.save_image(
            images[0],
            Path(out_dir),
            skill_dict.get("skill_id") or "cover",
            error_type=CoverDirectorError,
            urlopen=urllib.request.urlopen,
        )
        return CoverResult(
            cover_path=str(cover_path),
            prompt=prompt,
            size=size,
            reference_paths=ref_paths,
            source=images[0][:80],
            extra={
                "reference_images_sent": reference_images_sent,
                "reference_image_fallback": reference_fallback,
            },
        )

    def _call_json(self, *, system: str, user: str, timeout: int) -> dict[str, Any]:
        return call_stage_json(
            system=system,
            user=user,
            timeout=timeout,
            error_type=CoverDirectorError,
            chat_func=self.llm_factory.chat_func,
            chat_json_func=self.llm_factory.chat_json_func,
        )


make_cover = CoverDirectorAgent().run


# ============ 工具 ============

def _normalize_skill(skill: NoteSkill | dict[str, Any]) -> dict[str, Any]:
    if isinstance(skill, NoteSkill):
        return skill.to_dict()
    if isinstance(skill, dict):
        return skill
    raise TypeError(f"skill 必须是 NoteSkill 或 dict，收到 {type(skill)!r}")


def _has_local_reference_inputs(items: list[Any]) -> bool:
    return any(not (isinstance(item, str) and item.startswith(("http://", "https://"))) for item in items)
