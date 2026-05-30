"""Intaker Agent: normalize text/image user input into Intention + Context.

图片处理两道工序：
  - _rule_intake / _llm_intake : 走文本理解，拿 intention + context
  - image_tagger               : vision LLM “单图 + 用户文本”并发调用，给每张图打
                                  语义标签，写进 IntakeResult.assets 供下游 Agent 选图
"""
from __future__ import annotations

from nori.core import AgentBase, LLMFactory
from nori.shared.llm_json import attach_llm_error, try_stage_json
from nori.agents.user_profiling.models import IntakeResult, UserInput

from . import normalizer as _intake_normalizer
from . import image_tagger as _image_tagger
from .package import IntakeTextPromptBuilder, IntakeVisionPromptBuilder


# vision 打标的并发度（每张图 = 1 次 LLM）
VISION_PARALLELISM = _image_tagger.VISION_PARALLELISM

# 允许的视觉角色字典；超出此集合的 LLM 输出会被丢弃
ALLOWED_VISION_ROLES = _image_tagger.ALLOWED_VISION_ROLES
ALLOWED_USABLE_FOR = _image_tagger.ALLOWED_USABLE_FOR
ALLOWED_QUALITY = _image_tagger.ALLOWED_QUALITY


class IntakeAgent(AgentBase):
    """First-step agent for the new Nori flow."""

    stage_name = "intaker"

    def __init__(
        self,
        *,
        use_llm: bool = True,
        use_vision: bool = True,
        llm_factory: LLMFactory | None = None,
    ) -> None:
        super().__init__(stage_name=self.stage_name, use_llm=use_llm, llm_factory=llm_factory)
        self.use_vision = use_vision

    def run(
        self,
        user_input: UserInput | str,
        images: list[str] | None = None,
        *,
        use_llm: bool | None = None,
        use_vision: bool | None = None,
    ) -> IntakeResult:
        normalized = _intake_normalizer.normalize_input(user_input, images)
        fallback = _intake_normalizer.rule_intake(normalized)
        should_use_llm = self.should_use_llm(use_llm)
        result = fallback if not should_use_llm else (_llm_intake(normalized, fallback, llm_factory=self.llm_factory) or fallback)

        # use_llm=False 时整体关闭所有 LLM 调用（包括 vision 打标）
        if use_vision is None:
            should_use_vision = self.use_vision and should_use_llm
        else:
            should_use_vision = use_vision
        result.assets = _image_tagger.build_tagged_assets(
            normalized,
            use_vision=should_use_vision,
            parallelism=_vision_parallelism(),
            llm_factory=self.llm_factory,
        )
        return result


intake = IntakeAgent().run


IntakeVisionLLMError = _image_tagger.IntakeVisionLLMError


_TEXT_PROMPT_BUILDER = IntakeTextPromptBuilder()
_VISION_PROMPT_BUILDER = IntakeVisionPromptBuilder()
SYSTEM_PROMPT = _TEXT_PROMPT_BUILDER.system_prompt
USER_PROMPT = _TEXT_PROMPT_BUILDER.user_prompt_template


def _llm_intake(
    normalized: UserInput,
    fallback: IntakeResult,
    *,
    llm_factory: LLMFactory | None = None,
) -> IntakeResult | None:
    llm_gateway = llm_factory or LLMFactory()
    data, error = try_stage_json(
        system=_TEXT_PROMPT_BUILDER.system_prompt,
        user=_TEXT_PROMPT_BUILDER.build_user_prompt(normalized),
        chat_func=llm_gateway.chat_func,
        chat_json_func=llm_gateway.chat_json_func,
    )
    if data is None:
        if error:
            attach_llm_error(fallback.metadata, "intake_text", error)
        return None
    result = _intake_normalizer.normalize_llm_result(data, normalized, fallback)
    result.metadata = {**dict(result.metadata), "llm_enhanced": True}
    return result


# ============ 视觉打标工序 ============

VISION_SYSTEM_PROMPT = _VISION_PROMPT_BUILDER.system_prompt
VISION_USER_TEMPLATE = _VISION_PROMPT_BUILDER.user_prompt_template


def _vision_parallelism() -> int:
    return int(VISION_PARALLELISM)
