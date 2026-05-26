"""Content review input normalization helpers."""
from __future__ import annotations

from nori.core import AccountOperationProject
from typing import Any

from nori.content_generation.models import ContentPackage
from nori.core import ClientBrief, ContentTask


def normalize_package(value: ContentPackage | dict[str, Any]) -> ContentPackage:
    if isinstance(value, ContentPackage):
        return value
    return ContentPackage.from_dict(value)


def normalize_task(value: ContentTask | dict[str, Any] | None) -> ContentTask | None:
    if isinstance(value, ContentTask):
        return value
    if isinstance(value, dict):
        return ContentTask.from_dict(value)
    return None


def normalize_client_brief(
    value: ClientBrief | dict[str, Any] | None,
    project: AccountOperationProject | None = None,
) -> ClientBrief:
    if isinstance(value, ClientBrief):
        return value
    if isinstance(value, dict):
        return ClientBrief.from_dict(value)
    if project is not None:
        return project.client_brief
    return ClientBrief()
