"""Context-pack construction facade."""
from __future__ import annotations

from nori.core import AssetLibrary
from nori.core import AccountOperationProject
from typing import Any

from nori.core import (
    ContentTask,
    ContextPack,
    DecisionPoint,
    ExplanationTrace,
    MarketAnalysis,
    UserProfile,
    WorkflowBase,
    named_workflow_steps,
)
from nori.agents.market_analysis.facade import MarketAnalysisFacade
from nori.agents.user_profiling.facade import UserProfilingFacade



class ContextPackBuilder(WorkflowBase):
    """Build the unified context object that downstream generation should consume."""

    module_name = "planning"

    def __init__(self) -> None:
        super().__init__(
            workflow_name=self.module_name,
            steps=named_workflow_steps("profile", "task", "market", "assets", "context_pack"),
        )

    def build(
        self,
        *,
        context_pack_id: str = "",
        user_profile: UserProfile | dict[str, Any] | None = None,
        task: ContentTask | dict[str, Any] | None = None,
        market_analysis: MarketAnalysis | dict[str, Any] | None = None,
        asset_library: AssetLibrary | dict[str, Any] | None = None,
        decision_points: list[DecisionPoint | dict[str, Any]] | None = None,
    ) -> ContextPack:
        normalized_task = task if isinstance(task, ContentTask) else ContentTask.from_dict(task)
        normalized_assets = asset_library if isinstance(asset_library, AssetLibrary) else AssetLibrary.from_dict(asset_library)
        profile = user_profile if isinstance(user_profile, UserProfile) else UserProfile.from_dict(user_profile)
        market = market_analysis if isinstance(market_analysis, MarketAnalysis) else MarketAnalysis.from_dict(market_analysis)
        points = [
            point if isinstance(point, DecisionPoint) else DecisionPoint.from_dict(point)
            for point in (decision_points or [])
        ]
        trace = ExplanationTrace(
            trace_id=f"trace_{context_pack_id or normalized_task.task_id or 'context'}",
            input_refs=[
                ref
                for ref in [profile.user_id, normalized_task.task_id, market.analysis_id]
                if ref
            ],
            retrieved_evidence=[*market.source_refs, *normalized_task.references],
            decisions=[point.to_dict() for point in points],
            selected_assets=[asset.to_dict() for asset in normalized_assets.usable_assets()],
            final_rationale="ContextPack assembled from profile, task, market, and assets.",
        )
        return ContextPack(
            context_pack_id=context_pack_id or f"ctx_{normalized_task.task_id or profile.user_id or 'default'}",
            user_profile=profile,
            task_intent={
                "task_id": normalized_task.task_id,
                "topic": normalized_task.topic,
                "objective": normalized_task.objective,
                "content_type": normalized_task.content_type,
                "platform": normalized_task.platform,
                "brief": dict(normalized_task.brief),
            },
            market_analysis=market,
            assets=[asset.to_dict() for asset in normalized_assets.usable_assets()],
            constraints=list(profile.constraints),
            evidence_refs=[*market.source_refs, *normalized_task.references],
            decision_points=points,
            explanation_trace=trace,
        )

    def build_from_project(
        self,
        project: AccountOperationProject | dict[str, Any] | None,
        *,
        task_id: str = "",
        task: ContentTask | dict[str, Any] | None = None,
        decision_points: list[DecisionPoint | dict[str, Any]] | None = None,
    ) -> ContextPack:
        normalized = project if isinstance(project, AccountOperationProject) else AccountOperationProject.from_dict(project)
        selected_task = _project_task(normalized, task_id=task_id, task=task)
        context_pack = self.build(
            context_pack_id=f"ctx_{selected_task.task_id or normalized.project_id or 'project'}",
            user_profile=UserProfilingFacade().build_from_project(normalized),
            task=selected_task,
            market_analysis=MarketAnalysisFacade().build_from_project(normalized),
            asset_library=normalized.asset_library,
            decision_points=decision_points,
        )
        context_pack.metadata.update({
            "project_id": normalized.project_id,
            "project_name": normalized.name,
        })
        context_pack.explanation_trace.metadata.update({
            "project_id": normalized.project_id,
            "project_name": normalized.name,
        })
        return context_pack


def _project_task(
    project: AccountOperationProject,
    *,
    task_id: str = "",
    task: ContentTask | dict[str, Any] | None = None,
) -> ContentTask:
    if task is not None:
        return task if isinstance(task, ContentTask) else ContentTask.from_dict(task)
    normalized_task_id = str(task_id or "").strip()
    candidates = [*project.content_tasks, *project.content_calendar.tasks]
    if normalized_task_id:
        for candidate in candidates:
            if candidate.task_id == normalized_task_id:
                return candidate
    return candidates[0] if candidates else ContentTask(task_id=normalized_task_id)


__all__ = ["ContextPackBuilder"]
