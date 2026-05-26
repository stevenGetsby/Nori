"""Production bridge from planned content tasks to generated packages."""
from __future__ import annotations

from nori.core import AccountOperationProject
from pathlib import Path
from typing import Any

from nori.core import AgentBase, LLMFactory
from nori.content_generation.models import UserAsset
from nori.core import ClientBrief, ContentTask

from ..cover_director import CoverDirectorAgent
from ..note_maker import NoteMakerAgent
from . import builder as _package_builder
from . import inputs as _package_inputs
from . import state as _production_state
from ..models import ContentPackage


class ContentProductionError(RuntimeError):
    """Raised when task-to-package production fails."""

    def __init__(self, message: str, *, error: dict[str, Any]) -> None:
        super().__init__(message)
        self.error = dict(error)


class ContentProducerAgent(AgentBase):
    """Bridge `ContentTask` planning output into a generated `ContentPackage`.

    This layer owns orchestration and bookkeeping only. It delegates copy
    generation to `NoteMakerAgent` and cover rendering to `CoverDirectorAgent`.
    """

    def __init__(
        self,
        *,
        note_maker: Any | None = None,
        cover_director: Any | None = None,
        llm_factory: LLMFactory | None = None,
    ) -> None:
        super().__init__(stage_name="content_producer", use_llm=True, llm_factory=llm_factory)
        self.note_maker = note_maker or NoteMakerAgent(llm_factory=self.llm_factory)
        self.cover_director = cover_director or CoverDirectorAgent(llm_factory=self.llm_factory)

    def run(
        self,
        task: ContentTask | dict[str, Any],
        *,
        skills: list[Any],
        assets: list[UserAsset | dict[str, Any]] | None = None,
        out_dir: str | Path,
        client_brief: ClientBrief | dict[str, Any] | None = None,
        project: AccountOperationProject | None = None,
        intent: dict[str, Any] | None = None,
        context: dict[str, Any] | None = None,
        use_cover: bool = True,
    ) -> ContentPackage:
        normalized_task = _normalize_task(task)
        brief = _normalize_client_brief(client_brief or (project.client_brief if project else None))
        merged_intent = _package_inputs.build_intent(normalized_task, brief, intent)
        merged_context = _package_inputs.build_context(normalized_task, brief, project, context)
        normalized_assets = _package_inputs.normalize_assets(assets, normalized_task, brief)
        status_before = normalized_task.status

        try:
            draft = self.note_maker.run(
                skills,
                normalized_assets,
                intent=merged_intent,
                context=merged_context,
            )
            cover = None
            if use_cover:
                cover = self.cover_director.run(
                    draft,
                    _package_inputs.selected_skill(skills, draft.skill_id),
                    reference_assets=normalized_assets,
                    out_dir=out_dir,
                    intent=merged_intent,
                    tagged_assets=normalized_assets,
                )
        except Exception as exc:  # noqa: BLE001 - convert agent failures into contract metadata.
            error = _production_state.production_error(
                exc,
                normalized_task,
                stage=_production_state.error_stage(exc),
            )
            _production_state.attach_error(normalized_task, project, error)
            raise ContentProductionError(error["message"], error=error) from exc

        package = _package_builder.package_from_outputs(
            normalized_task,
            draft,
            cover,
            skills=skills,
            assets=normalized_assets,
            brief=brief,
            project=project,
            status_before=status_before,
            use_cover=use_cover,
        )
        _production_state.attach_success(normalized_task, project, package)
        return package


def produce_content_package(
    task: ContentTask | dict[str, Any],
    **kwargs: Any,
) -> ContentPackage:
    """Convenience wrapper for one-shot task production."""

    note_maker = kwargs.pop("note_maker", None)
    cover_director = kwargs.pop("cover_director", None)
    return ContentProducerAgent(
        note_maker=note_maker,
        cover_director=cover_director,
    ).run(task, **kwargs)


def _normalize_task(value: ContentTask | dict[str, Any]) -> ContentTask:
    if isinstance(value, ContentTask):
        return value
    return ContentTask.from_dict(value)


def _normalize_client_brief(value: ClientBrief | dict[str, Any] | None) -> ClientBrief:
    if isinstance(value, ClientBrief):
        return value
    return ClientBrief.from_dict(value)


__all__ = [
    "ContentProducerAgent",
    "ContentProductionError",
    "produce_content_package",
]
