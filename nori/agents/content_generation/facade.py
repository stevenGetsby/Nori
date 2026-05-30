"""Content generation facade and candidate-set helpers."""
from __future__ import annotations

from typing import Any

from nori.agents.planning.facade import ContextPackBuilder
from nori.core import (
    AccountOperationProject,
    CandidateSet,
    ContentTask,
    ContextPack,
    DecisionPoint,
    ExplanationTrace,
    WorkflowBase,
    named_workflow_steps,
)

from .models import ContentPackage


class ContentGenerationFacade(WorkflowBase):
    """Convert generated packages into candidate-set contracts."""

    module_name = "content_generation"

    def __init__(self) -> None:
        super().__init__(
            workflow_name=self.module_name,
            steps=named_workflow_steps("context_pack", "content_packages", "candidate_set"),
        )

    def candidate_set(
        self,
        packages: list[ContentPackage | dict[str, Any]],
        *,
        task: ContentTask | dict[str, Any] | None = None,
        context_pack: ContextPack | dict[str, Any] | None = None,
        candidate_set_id: str = "",
        selected_candidate_id: str = "",
    ) -> CandidateSet:
        pack = context_pack if isinstance(context_pack, ContextPack) else ContextPack.from_dict(context_pack)
        normalized_task = _task_from_input(task=task, context_pack=pack)
        normalized_packages = [
            package if isinstance(package, ContentPackage) else ContentPackage.from_dict(package)
            for package in packages
        ]
        candidates = [
            {
                "id": package.package_id or package.task_id or f"candidate_{index + 1}",
                "package": package.to_dict(),
                "status": package.status,
            }
            for index, package in enumerate(normalized_packages)
        ]
        decision = DecisionPoint(
            decision_id=f"decision_{candidate_set_id or normalized_task.task_id or 'candidate'}",
            kind="candidate_selection",
            options=[{"id": row["id"], "label": row["package"].get("title", row["id"])} for row in candidates],
            recommended_option=selected_candidate_id or (candidates[0]["id"] if candidates else ""),
            selected_option=selected_candidate_id,
        )
        return CandidateSet(
            candidate_set_id=candidate_set_id or f"candidates_{normalized_task.task_id or 'default'}",
            task_id=normalized_task.task_id,
            candidates=candidates,
            selected_candidate_id=selected_candidate_id,
            decision_point=decision,
            explanation_trace=ExplanationTrace(
                trace_id=f"trace_{candidate_set_id or normalized_task.task_id or 'candidate'}",
                input_refs=_generation_input_refs(pack, normalized_task),
                retrieved_evidence=list(pack.evidence_refs),
                decisions=[decision.to_dict()],
                stage_steps=[{"stage": "ContentGenerationFacade", "output_count": len(candidates)}],
                final_rationale="CandidateSet groups generated packages for human selection.",
            ),
            metadata=_generation_metadata(pack),
        )

    def candidate_set_from_project(
        self,
        project: AccountOperationProject | dict[str, Any] | None,
        *,
        task_id: str = "",
        candidate_set_id: str = "",
        selected_candidate_id: str = "",
        context_pack: ContextPack | dict[str, Any] | None = None,
    ) -> CandidateSet:
        normalized = project if isinstance(project, AccountOperationProject) else AccountOperationProject.from_dict(project)
        normalized_task_id = str(task_id or "").strip()
        packages = [
            package
            for package in normalized.content_packages
            if not normalized_task_id or package.task_id == normalized_task_id
        ]
        pack = (
            context_pack
            if isinstance(context_pack, ContextPack)
            else ContextPack.from_dict(context_pack)
        )
        if not pack.context_pack_id:
            pack = ContextPackBuilder().build_from_project(normalized, task_id=normalized_task_id)
        candidate_set = self.candidate_set(
            packages,
            task=_task_from_project(normalized, normalized_task_id),
            context_pack=pack,
            candidate_set_id=candidate_set_id,
            selected_candidate_id=selected_candidate_id,
        )
        candidate_set.metadata.update({
            "project_id": normalized.project_id,
            "project_name": normalized.name,
        })
        return candidate_set


def _task_from_input(
    *,
    task: ContentTask | dict[str, Any] | None,
    context_pack: ContextPack,
) -> ContentTask:
    if task is not None:
        return task if isinstance(task, ContentTask) else ContentTask.from_dict(task)
    intent = dict(context_pack.task_intent)
    return ContentTask(
        task_id=str(intent.get("task_id") or ""),
        topic=str(intent.get("topic") or ""),
        objective=str(intent.get("objective") or ""),
        content_type=str(intent.get("content_type") or "note"),
        platform=str(intent.get("platform") or "xhs"),
        brief=dict(intent.get("brief") or {}),
    )


def _task_from_project(project: AccountOperationProject, task_id: str) -> ContentTask:
    if task_id:
        for task in [*project.content_tasks, *project.content_calendar.tasks]:
            if task.task_id == task_id:
                return task
    return project.content_tasks[0] if project.content_tasks else ContentTask(task_id=task_id)


def _generation_input_refs(context_pack: ContextPack, task: ContentTask) -> list[str]:
    refs = []
    if context_pack.context_pack_id:
        refs.append(context_pack.context_pack_id)
    if task.task_id:
        refs.append(task.task_id)
    return refs


def _generation_metadata(context_pack: ContextPack) -> dict[str, Any]:
    metadata = dict(context_pack.metadata)
    if context_pack.context_pack_id:
        metadata["context_pack_id"] = context_pack.context_pack_id
    return metadata


__all__ = ["ContentGenerationFacade"]
