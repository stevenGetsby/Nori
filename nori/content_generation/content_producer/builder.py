"""ContentPackage construction helpers for ContentProducerAgent."""
from __future__ import annotations

from nori.core import AccountOperationProject
from typing import Any

from nori.content_generation.models import CoverResult, NoteDraft
from nori.core import ClientBrief, ContentTask, UserAsset

from . import inputs as _package_inputs
from . import refs as _package_refs
from ..models import ContentPackage


def normalize_assets(
    assets: list[UserAsset | dict[str, Any]] | None,
    task: ContentTask,
    brief: ClientBrief,
) -> list[UserAsset]:
    return _package_inputs.normalize_assets(assets, task, brief)


def normalize_asset(value: UserAsset | dict[str, Any]) -> UserAsset:
    return _package_inputs.normalize_asset(value)


def task_brief_text(task: ContentTask, brief: ClientBrief) -> str:
    return _package_inputs.task_brief_text(task, brief)


def build_intent(
    task: ContentTask,
    brief: ClientBrief,
    override: dict[str, Any] | None,
) -> dict[str, Any]:
    return _package_inputs.build_intent(task, brief, override)


def build_context(
    task: ContentTask,
    brief: ClientBrief,
    project: AccountOperationProject | None,
    override: dict[str, Any] | None,
) -> dict[str, Any]:
    return _package_inputs.build_context(task, brief, project, override)


def selected_skill(skills: list[Any], skill_id: str) -> Any:
    return _package_inputs.selected_skill(skills, skill_id)


def package_from_outputs(
    task: ContentTask,
    draft: NoteDraft,
    cover: CoverResult | None,
    *,
    skills: list[Any],
    assets: list[UserAsset],
    brief: ClientBrief,
    project: AccountOperationProject | None,
    status_before: str,
    use_cover: bool,
) -> ContentPackage:
    package_id = _package_refs.package_id_for_task(task)
    cover_path = cover.cover_path if cover else draft.cover_path
    image_paths = _package_refs.dedupe([*draft.image_paths, *((cover.reference_paths if cover else []) or [])])
    return ContentPackage(
        package_id=package_id,
        task_id=task.task_id,
        platform=task.platform,
        title=draft.title,
        body=draft.body,
        tags=list(draft.tags),
        cover_path=cover_path,
        image_paths=image_paths,
        prompts={
            "note_draft": draft.to_dict(),
            "cover_result": cover.to_dict() if cover else None,
        },
        material_usage=_package_refs.material_usage(assets, task),
        source_refs=_package_refs.source_refs(task, skills, brief, project),
        status="draft",
        metadata={
            "production": {
                "producer": "ContentProducerAgent",
                "version": "p3-content-task-production-bridge",
                "task_status_before": status_before,
                "cover_enabled": use_cover,
                "cover_generated": cover is not None,
            }
        },
    )


def material_usage(assets: list[UserAsset], task: ContentTask) -> list[dict[str, Any]]:
    return _package_refs.material_usage(assets, task)


def source_refs(
    task: ContentTask,
    skills: list[Any],
    brief: ClientBrief,
    project: AccountOperationProject | None,
) -> list[dict[str, Any]]:
    return _package_refs.source_refs(task, skills, brief, project)


def slug(value: str) -> str:
    return _package_refs.slug(value)


def dedupe(values: list[str]) -> list[str]:
    return _package_refs.dedupe(values)
