"""User/account/brand profiling facade."""
from __future__ import annotations

from typing import Any

from nori.core import ClientBrief, UserProfile, WorkflowBase, named_workflow_steps

from .models import AccountPositioning


class UserProfilingFacade(WorkflowBase):
    """Build long-lived profile contracts from existing brief/positioning models."""

    module_name = "user_profiling"

    def __init__(self) -> None:
        super().__init__(
            workflow_name=self.module_name,
            steps=named_workflow_steps("client_brief", "account_positioning", "user_profile"),
        )

    def build_profile(
        self,
        *,
        user_id: str = "",
        client_brief: ClientBrief | dict[str, Any] | None = None,
        account_positioning: AccountPositioning | dict[str, Any] | None = None,
        preferences: dict[str, Any] | None = None,
    ) -> UserProfile:
        brief = client_brief if isinstance(client_brief, ClientBrief) else ClientBrief.from_dict(client_brief)
        positioning = (
            account_positioning
            if isinstance(account_positioning, AccountPositioning)
            else AccountPositioning.from_dict(account_positioning)
        )
        return UserProfile(
            user_id=user_id or brief.client_name,
            display_name=brief.client_name or brief.brand_name,
            platform=brief.platform,
            account_profile=positioning.to_dict(),
            brand_profile={
                "brand_name": brief.brand_name,
                "source_materials": list(brief.source_materials),
            },
            preferences=dict(preferences or brief.context.get("preferences") or {}),
            constraints=[*brief.constraints, *brief.taboos],
            source_refs=[{"source": "client_brief"}, {"source": "account_positioning"}],
        )

    def build_from_project(
        self,
        project: Any,
        *,
        user_id: str = "",
        preferences: dict[str, Any] | None = None,
    ) -> UserProfile:
        project_data = _project_data(project)
        project_id = str(project_data.get("project_id") or "")
        project_name = str(project_data.get("name") or "")
        profile = self.build_profile(
            user_id=user_id or project_id,
            client_brief=project_data.get("client_brief"),
            account_positioning=project_data.get("account_positioning"),
            preferences=preferences,
        )
        profile.source_refs.append({
            "source": "account_operation_project",
            "project_id": project_id,
        })
        profile.metadata.update({
            "project_id": project_id,
            "project_name": project_name,
        })
        return profile


def _project_data(project: Any) -> dict[str, Any]:
    if hasattr(project, "to_dict"):
        return project.to_dict()
    return dict(project or {})


__all__ = ["UserProfilingFacade"]
