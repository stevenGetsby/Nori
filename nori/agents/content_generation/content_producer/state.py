"""ContentProducer task/project state transition helpers."""
from __future__ import annotations

from nori.core import AccountOperationProject
from typing import Any

from nori.core import ContentTask

from ..schemas import ContentPackage


def production_error(exc: Exception, task: ContentTask, *, stage: str | None = None) -> dict[str, Any]:
    resolved_stage = stage or error_stage(exc)
    return {
        "stage": resolved_stage,
        "task_id": task.task_id,
        "package_id": task.package_id,
        "error_type": type(exc).__name__,
        "message": f"{resolved_stage} failed: {type(exc).__name__}: {exc}",
    }


def error_stage(exc: Exception) -> str:
    name = type(exc).__name__.lower()
    if "cover" in name:
        return "cover"
    if "note" in name:
        return "note"
    return "production"


def attach_error(
    task: ContentTask,
    project: AccountOperationProject | None,
    error: dict[str, Any],
) -> None:
    task.status = "failed"
    task.metadata = {**dict(task.metadata), "production_error": dict(error)}
    if project is not None:
        errors = list(project.metadata.get("production_errors") or [])
        errors.append(dict(error))
        project.metadata = {**dict(project.metadata), "production_errors": errors}


def attach_success(
    task: ContentTask,
    project: AccountOperationProject | None,
    package: ContentPackage,
) -> None:
    task.package_id = package.package_id
    task.status = "drafted"
    task.metadata = {
        **dict(task.metadata),
        "production": {
            "status": "drafted",
            "package_id": package.package_id,
            "producer": "ContentProducerAgent",
        },
    }
    if project is not None:
        project.content_packages.append(package)
        project.metadata = {
            **dict(project.metadata),
            "last_produced_package_id": package.package_id,
        }
