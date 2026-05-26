"""ContentProducer input and context preparation helpers."""
from __future__ import annotations

from nori.core import AccountOperationProject
from typing import Any

from nori.content_generation.models import UserAsset
from nori.core import ClientBrief, ContentTask


def normalize_assets(
    assets: list[UserAsset | dict[str, Any]] | None,
    task: ContentTask,
    brief: ClientBrief,
) -> list[UserAsset]:
    """Restore assets and add a task/brief text asset when text context is missing."""
    normalized = [normalize_asset(item) for item in (assets or []) if item]
    if not any(asset.kind == "text" and asset.text.strip() for asset in normalized):
        normalized.append(UserAsset(kind="text", text=task_brief_text(task, brief)))
    return normalized


def normalize_asset(value: UserAsset | dict[str, Any]) -> UserAsset:
    if isinstance(value, UserAsset):
        return value
    return UserAsset.from_dict(value if isinstance(value, dict) else {})


def task_brief_text(task: ContentTask, brief: ClientBrief) -> str:
    parts = [
        f"任务标题：{task.title}",
        f"主题：{task.topic}",
        f"目标：{task.objective}",
        f"平台：{task.platform}",
        f"内容类型：{task.content_type}",
    ]
    if task.brief:
        parts.append(f"任务 brief：{task.brief}")
    if brief.brand_name:
        parts.append(f"品牌：{brief.brand_name}")
    if brief.audience:
        parts.append(f"受众：{'、'.join(brief.audience)}")
    if brief.constraints:
        parts.append(f"约束：{'、'.join(brief.constraints)}")
    if brief.taboos:
        parts.append(f"禁忌：{'、'.join(brief.taboos)}")
    return "\n".join(part for part in parts if part and not part.endswith("："))


def build_intent(
    task: ContentTask,
    brief: ClientBrief,
    override: dict[str, Any] | None,
) -> dict[str, Any]:
    data = {
        "goal": task.objective or (brief.goals[0] if brief.goals else ""),
        "format": "小红书图文" if task.platform == "xhs" else task.content_type,
        "topic": task.topic or task.title,
        "platform": task.platform,
        "content_type": task.content_type,
    }
    data.update(dict(override or {}))
    return data


def build_context(
    task: ContentTask,
    brief: ClientBrief,
    project: AccountOperationProject | None,
    override: dict[str, Any] | None,
) -> dict[str, Any]:
    data: dict[str, Any] = {
        "task": task.to_dict(),
        "client_brief": brief.to_dict(),
    }
    if project is not None:
        data["project"] = {
            "project_id": project.project_id,
            "name": project.name,
            "account_positioning": dict(project.account_positioning),
            "operation_plan": project.operation_plan.to_dict(),
        }
    data.update(dict(override or {}))
    return data


def selected_skill(skills: list[Any], skill_id: str) -> Any:
    for skill in skills:
        data = skill.to_dict() if hasattr(skill, "to_dict") else (skill if isinstance(skill, dict) else {})
        if data.get("skill_id") == skill_id:
            return skill
    return skills[0]
