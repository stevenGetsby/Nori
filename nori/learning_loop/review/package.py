"""Class-owned input contract for review agents."""
from __future__ import annotations

from typing import Any

from nori.content_generation.models import ContentPackage
from nori.core import AccountOperationProject, AgentInputPreparer, ClientBrief, ContentTask


class ReviewInputPreparer(AgentInputPreparer):
    """Restore persisted review inputs before policy evaluation."""

    def normalize_package(self, value: ContentPackage | dict[str, Any]) -> ContentPackage:
        if isinstance(value, ContentPackage):
            return value
        return ContentPackage.from_dict(value)

    def normalize_task(self, value: ContentTask | dict[str, Any] | None) -> ContentTask | None:
        if isinstance(value, ContentTask):
            return value
        if isinstance(value, dict):
            return ContentTask.from_dict(value)
        return None

    def normalize_client_brief(
        self,
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


__all__ = ["ReviewInputPreparer"]
