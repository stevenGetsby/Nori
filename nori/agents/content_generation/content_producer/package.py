"""ContentProducer package preparation and assembly."""
from __future__ import annotations

from typing import Any

from nori._compat import dataclass, field
from nori.agents.content_generation.schemas import ContentPackage, CoverResult, NoteDraft
from nori.core import AccountOperationProject, ClientBrief, ContentTask, IntentContract, StableArtifactAssembler, UserAsset


@dataclass(slots=True)
class PreparedContentPackageInput:
    """Normalized deterministic inputs passed into generation substages."""

    assets: list[UserAsset] = field(default_factory=list)
    intent: dict[str, Any] = field(default_factory=dict)
    context: dict[str, Any] = field(default_factory=dict)


class ContentPackageAssembler(StableArtifactAssembler):
    """Prepare content-production inputs and assemble the final package."""

    default_slug = "task"

    def __init__(
        self,
        *,
        producer_name: str = "ContentProducerAgent",
        version: str = "p3-content-task-production-bridge",
    ) -> None:
        self.producer_name = producer_name
        self.version = version

    def prepare(
        self,
        task: ContentTask,
        brief: ClientBrief,
        *,
        assets: list[UserAsset | dict[str, Any]] | None = None,
        project: AccountOperationProject | None = None,
        intent_override: dict[str, Any] | None = None,
        context_override: dict[str, Any] | None = None,
    ) -> PreparedContentPackageInput:
        return PreparedContentPackageInput(
            assets=self.normalize_assets(assets, task, brief),
            intent=self.build_intent(task, brief, intent_override),
            context=self.build_context(task, brief, project, context_override),
        )

    def normalize_assets(
        self,
        assets: list[UserAsset | dict[str, Any]] | None,
        task: ContentTask,
        brief: ClientBrief,
    ) -> list[UserAsset]:
        normalized = [self.normalize_asset(item) for item in (assets or []) if item]
        if not any(asset.kind == "text" and asset.text.strip() for asset in normalized):
            normalized.append(UserAsset(kind="text", text=self.task_brief_text(task, brief)))
        return normalized

    def normalize_asset(self, value: UserAsset | dict[str, Any]) -> UserAsset:
        if isinstance(value, UserAsset):
            return value
        return UserAsset.from_dict(value if isinstance(value, dict) else {})

    def task_brief_text(self, task: ContentTask, brief: ClientBrief) -> str:
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
        self,
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
        self,
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

    def selected_skill(self, skills: list[Any], skill_id: str) -> Any:
        for skill in skills:
            data = skill.to_dict() if hasattr(skill, "to_dict") else (skill if isinstance(skill, dict) else {})
            if data.get("skill_id") == skill_id:
                return skill
        return skills[0]

    def package_id_for_task(self, task: ContentTask) -> str:
        return task.package_id or f"pkg_{self.slug(task.task_id or task.title or task.topic or 'task')}"

    def build(
        self,
        task: ContentTask,
        draft: NoteDraft,
        cover: CoverResult | None,
        *,
        skills: list[Any],
        assets: list[UserAsset],
        brief: ClientBrief,
        project: AccountOperationProject | None,
        intent_contract: IntentContract | None = None,
        status_before: str,
        use_cover: bool,
    ) -> ContentPackage:
        cover_path = cover.cover_path if cover else draft.cover_path
        image_paths = self.dedupe([*draft.image_paths, *((cover.reference_paths if cover else []) or [])])
        return ContentPackage(
            package_id=self.package_id_for_task(task),
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
            material_usage=self.material_usage(assets, task),
            source_refs=self.source_refs(task, skills, brief, project),
            status="draft",
            metadata={
                "production": {
                    "producer": self.producer_name,
                    "version": self.version,
                    "task_status_before": status_before,
                    "cover_enabled": use_cover,
                    "cover_generated": cover is not None,
                },
                "intent_contract": intent_contract.to_dict() if intent_contract and intent_contract.contract_id else {},
            },
        )

    def material_usage(self, assets: list[UserAsset], task: ContentTask) -> list[dict[str, Any]]:
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
        self,
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


__all__ = ["ContentPackageAssembler", "PreparedContentPackageInput"]
