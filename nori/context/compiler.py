"""Compile business context packs and agent-specific context views."""
from __future__ import annotations

from typing import Any

from nori.core import (
    AccountOperationProject,
    AssetLibrary,
    ContentTask,
    ContextPack,
    DecisionPoint,
    ExplanationTrace,
    MarketAnalysis,
    UserProfile,
    WorkflowBase,
    named_workflow_steps,
)

from .models import ContextSlice


class ContextCompiler(WorkflowBase):
    """Build the business context object consumed by generation decisions."""

    module_name = "context"

    def __init__(self) -> None:
        super().__init__(
            workflow_name=self.module_name,
            steps=named_workflow_steps("profile", "task", "market", "assets", "skills", "context_pack"),
        )

    def build(
        self,
        *,
        context_pack_id: str = "",
        user_profile: UserProfile | dict[str, Any] | None = None,
        task: ContentTask | dict[str, Any] | None = None,
        market_analysis: MarketAnalysis | dict[str, Any] | None = None,
        asset_library: AssetLibrary | dict[str, Any] | None = None,
        skills: list[Any] | None = None,
        platform_rules: list[dict[str, Any]] | None = None,
        content_strategy: dict[str, Any] | None = None,
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
        skill_rows = [_to_dict_row(skill) for skill in (skills or []) if skill]
        asset_rows = [asset.to_dict() for asset in normalized_assets.usable_assets()]
        constraints = _dedupe([*profile.constraints, *normalized_task.notes])
        task_payload = _task_payload(normalized_task)
        pack_id = context_pack_id or f"ctx_{normalized_task.task_id or profile.user_id or 'default'}"
        slices = _context_slices(
            profile=profile,
            task_payload=task_payload,
            market=market,
            asset_rows=asset_rows,
            skill_rows=skill_rows,
            platform_rules=platform_rules or [],
            content_strategy=content_strategy or {},
            constraints=constraints,
        )
        trace = ExplanationTrace(
            trace_id=f"trace_{pack_id}",
            input_refs=[
                ref
                for ref in [profile.user_id, normalized_task.task_id, market.analysis_id]
                if ref
            ],
            retrieved_evidence=[*market.source_refs, *normalized_task.references],
            decisions=[point.to_dict() for point in points],
            selected_assets=asset_rows,
            final_rationale="ContextPack compiled from profile, task, market, skills, assets, and strategy slices.",
            metadata={"context_layer": "orchestration"},
        )
        return ContextPack(
            context_pack_id=pack_id,
            user_profile=profile,
            task_intent=task_payload,
            market_analysis=market,
            assets=asset_rows,
            constraints=constraints,
            evidence_refs=[*market.source_refs, *normalized_task.references],
            decision_points=points,
            explanation_trace=trace,
            context_slices=[context_slice.to_dict() for context_slice in slices],
            metadata={"context_layer": "orchestration"},
        )

    def build_from_project(
        self,
        project: AccountOperationProject | dict[str, Any] | None,
        *,
        task_id: str = "",
        task: ContentTask | dict[str, Any] | None = None,
        asset_library: AssetLibrary | dict[str, Any] | None = None,
        skills: list[Any] | None = None,
        platform_rules: list[dict[str, Any]] | None = None,
        content_strategy: dict[str, Any] | None = None,
        decision_points: list[DecisionPoint | dict[str, Any]] | None = None,
    ) -> ContextPack:
        from nori.agents.market_analysis.facade import MarketAnalysisFacade
        from nori.agents.user_profiling.facade import UserProfilingFacade

        normalized = project if isinstance(project, AccountOperationProject) else AccountOperationProject.from_dict(project)
        selected_task = _project_task(normalized, task_id=task_id, task=task)
        context_pack = self.build(
            context_pack_id=f"ctx_{selected_task.task_id or normalized.project_id or 'project'}",
            user_profile=UserProfilingFacade().build_from_project(normalized),
            task=selected_task,
            market_analysis=MarketAnalysisFacade().build_from_project(normalized),
            asset_library=asset_library if asset_library is not None else normalized.asset_library,
            skills=skills,
            platform_rules=platform_rules,
            content_strategy=content_strategy,
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


def _context_slices(
    *,
    profile: UserProfile,
    task_payload: dict[str, Any],
    market: MarketAnalysis,
    asset_rows: list[dict[str, Any]],
    skill_rows: list[dict[str, Any]],
    platform_rules: list[dict[str, Any]],
    content_strategy: dict[str, Any],
    constraints: list[str],
) -> list[ContextSlice]:
    scope = {
        "platform": str(task_payload.get("platform") or market.platform or profile.platform or ""),
        "task_id": str(task_payload.get("task_id") or ""),
    }
    return [
        ContextSlice(
            kind="brand_profile",
            payload=profile.to_dict(),
            scope=scope,
            source_refs=list(profile.source_refs),
            priority=20,
        ),
        ContextSlice(
            kind="task_intent",
            payload=task_payload,
            scope=scope,
            source_refs=[{"source": "content_task", "task_id": str(task_payload.get("task_id") or "")}],
            priority=10,
        ),
        ContextSlice(
            kind="platform_strategy",
            payload={
                "platform": task_payload.get("platform", ""),
                "content_type": task_payload.get("content_type", ""),
                "rules": _dict_rows(platform_rules),
            },
            scope=scope,
            priority=30,
        ),
        ContextSlice(
            kind="market_hotspots",
            payload={
                "keywords": list(market.keywords),
                "hot_examples": list(market.hot_examples),
                "trend_insights": list(market.trend_insights),
                "audience_insights": list(market.audience_insights),
            },
            scope=scope,
            source_refs=list(market.source_refs),
            priority=40,
        ),
        ContextSlice(
            kind="learned_skills",
            payload={"skills": skill_rows},
            scope=scope,
            source_refs=[{"source": "skill", "skill_id": str(row.get("skill_id") or "")} for row in skill_rows],
            priority=50,
        ),
        ContextSlice(
            kind="content_strategy",
            payload=dict(content_strategy),
            scope=scope,
            priority=60,
        ),
        ContextSlice(
            kind="asset_context",
            payload={"assets": asset_rows},
            scope=scope,
            source_refs=[{"source": "asset", "asset_id": str(row.get("asset_id") or row.get("id") or "")} for row in asset_rows],
            priority=70,
        ),
        ContextSlice(
            kind="constraints",
            payload={"constraints": constraints},
            scope=scope,
            priority=80,
        ),
    ]


def _task_payload(task: ContentTask) -> dict[str, Any]:
    return {
        "task_id": task.task_id,
        "topic": task.topic,
        "objective": task.objective,
        "content_type": task.content_type,
        "platform": task.platform,
        "brief": dict(task.brief),
    }


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


def _to_dict_row(value: Any) -> dict[str, Any]:
    if hasattr(value, "to_dict"):
        return value.to_dict()
    return dict(value) if isinstance(value, dict) else {}


def _dict_rows(values: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [dict(value) for value in values if isinstance(value, dict)]


def _dedupe(values: list[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for value in values:
        text = str(value or "").strip()
        if text and text not in seen:
            out.append(text)
            seen.add(text)
    return out


ContextPackBuilder = ContextCompiler

__all__ = ["ContextCompiler", "ContextPackBuilder"]
