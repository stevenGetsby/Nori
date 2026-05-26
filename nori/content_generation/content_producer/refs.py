"""ContentPackage provenance and stable-id helpers."""
from __future__ import annotations

from nori.core import AccountOperationProject
import re
from typing import Any

from nori.content_generation.models import UserAsset
from nori.core import ClientBrief, ContentTask
from nori.shared.normalization import dedupe_preserve_order


def package_id_for_task(task: ContentTask) -> str:
    return task.package_id or f"pkg_{slug(task.task_id or task.title or task.topic or 'task')}"


def material_usage(assets: list[UserAsset], task: ContentTask) -> list[dict[str, Any]]:
    rows = []
    for index, asset in enumerate(assets):
        rows.append({
            "source": "input_asset",
            "index": index,
            "kind": asset.kind,
            "path": asset.path,
            "text_preview": asset.text[:120],
            "usable_for": list(asset.usable_for),
        })
    for item in task.required_assets:
        rows.append({"source": "task_required_asset", "kind": item})
    return rows


def source_refs(
    task: ContentTask,
    skills: list[Any],
    brief: ClientBrief,
    project: AccountOperationProject | None,
) -> list[dict[str, Any]]:
    refs = [dict(item) for item in task.references]
    refs.extend(
        {
            "source": "note_skill",
            "skill_id": data.get("skill_id", ""),
            "label": data.get("label", ""),
        }
        for data in (
            skill.to_dict() if hasattr(skill, "to_dict") else (skill if isinstance(skill, dict) else {})
            for skill in skills
        )
    )
    if brief.client_name or brief.brand_name:
        refs.append({
            "source": "client_brief",
            "client_name": brief.client_name,
            "brand_name": brief.brand_name,
        })
    if project is not None and project.project_id:
        refs.append({"source": "account_operation_project", "project_id": project.project_id})
    return refs


def slug(value: str) -> str:
    text = re.sub(r"[^\w\-]+", "_", value.strip())
    return text[:80].strip("_") or "task"


def dedupe(values: list[str]) -> list[str]:
    return dedupe_preserve_order(value for value in values if value)
