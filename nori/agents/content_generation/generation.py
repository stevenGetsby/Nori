"""Top-level generation router for text, image, and package artifacts."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from nori.core import AgentBase, ContentTask, IntentContract, LLMFactory, UserAsset
from nori.agents.market_analysis.models import NoteSkill

from .content_producer import ContentProducerAgent
from .cover_director import CoverDirectorAgent
from .models import ContentPackage, CoverResult, NoteDraft
from .note_maker import NoteMakerAgent


class GenerationAgent(AgentBase):
    """Route generation requests to specialized child agents.

    The system-level stage stays small and explicit: it owns routing and shared
    contracts, while text, image, and package creation remain specialized.
    """

    stage_name = "generation"

    def __init__(
        self,
        *,
        content_producer: Any | None = None,
        note_maker: Any | None = None,
        cover_director: Any | None = None,
        llm_factory: LLMFactory | None = None,
    ) -> None:
        super().__init__(stage_name=self.stage_name, use_llm=True, llm_factory=llm_factory)
        self.note_maker = note_maker or NoteMakerAgent(llm_factory=self.llm_factory)
        self.cover_director = cover_director or CoverDirectorAgent(llm_factory=self.llm_factory)
        self.content_producer = content_producer or ContentProducerAgent(
            note_maker=self.note_maker,
            cover_director=self.cover_director,
            llm_factory=self.llm_factory,
        )

    @property
    def routes(self) -> list[str]:
        return ["note_package", "text", "image"]

    def run(self, artifact_type: str = "note_package", **kwargs: Any) -> ContentPackage | NoteDraft | CoverResult:
        route = str(artifact_type or "note_package").strip()
        if route == "note_package":
            return self._run_note_package(**kwargs)
        if route == "text":
            return self._run_text(**kwargs)
        if route == "image":
            return self._run_image(**kwargs)
        raise ValueError(f"Unsupported generation artifact_type: {artifact_type!r}")

    def _run_note_package(
        self,
        *,
        task: ContentTask | dict[str, Any],
        skills: list[NoteSkill | dict[str, Any]],
        assets: list[UserAsset | dict[str, Any]] | None = None,
        out_dir: str | Path,
        intent_contract: IntentContract | dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> ContentPackage:
        return self.content_producer.run(
            task,
            skills=skills,
            assets=assets,
            out_dir=out_dir,
            intent_contract=intent_contract,
            **kwargs,
        )

    def _run_text(
        self,
        *,
        skills: list[NoteSkill | dict[str, Any]],
        assets: list[UserAsset | dict[str, Any]],
        intent: dict[str, Any] | None = None,
        context: dict[str, Any] | None = None,
        **_kwargs: Any,
    ) -> NoteDraft:
        return self.note_maker.run(skills, assets, intent=intent, context=context)

    def _run_image(
        self,
        *,
        draft: NoteDraft,
        skill: NoteSkill | dict[str, Any],
        out_dir: str | Path,
        reference_assets: list[UserAsset] | None = None,
        intent: dict[str, Any] | None = None,
        tagged_assets: list[UserAsset] | None = None,
        **kwargs: Any,
    ) -> CoverResult:
        return self.cover_director.run(
            draft,
            skill,
            reference_assets=reference_assets,
            out_dir=out_dir,
            intent=intent,
            tagged_assets=tagged_assets,
            **kwargs,
        )


__all__ = ["GenerationAgent"]
