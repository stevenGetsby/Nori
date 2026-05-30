"""Monitoring, analysis, and learning-loop facade."""
from __future__ import annotations

from typing import Any

from nori.agents.content_generation.facade import ContentGenerationFacade
from nori.agents.planning.facade import ContextPackBuilder
from nori.core import (
    AccountOperationProject,
    CapabilitySnapshot,
    LearningSignal,
    PerformanceSnapshot,
    WorkflowBase,
    capability_module_names,
    named_workflow_steps,
)
from nori.agents.market_analysis.facade import MarketAnalysisFacade
from nori.agents.user_profiling.facade import UserProfilingFacade

from .models import MetricsSnapshot, StrategyIteration


class LearningLoopFacade(WorkflowBase):
    """Convert monitoring and strategy artifacts into learning signals."""

    module_name = "learning_loop"

    def __init__(self) -> None:
        super().__init__(
            workflow_name=self.module_name,
            steps=named_workflow_steps("performance", "strategy", "capability_snapshot"),
        )

    def performance_snapshot(self, snapshot: MetricsSnapshot | dict[str, Any]) -> PerformanceSnapshot:
        normalized = snapshot if isinstance(snapshot, MetricsSnapshot) else MetricsSnapshot.from_dict(snapshot)
        return PerformanceSnapshot(
            snapshot_id=normalized.snapshot_id,
            ref_id=normalized.ref_id,
            metrics=dict(normalized.metrics),
            source=normalized.source or "manual",
            captured_at=normalized.captured_at,
            metadata=dict(normalized.metadata),
        )

    def learning_signal(
        self,
        *,
        source: str,
        target: str,
        strategy_iteration: StrategyIteration | dict[str, Any] | None = None,
        confidence: float = 0.5,
    ) -> LearningSignal:
        iteration = (
            strategy_iteration
            if isinstance(strategy_iteration, StrategyIteration)
            else StrategyIteration.from_dict(strategy_iteration)
        )
        return LearningSignal(
            signal_id=f"signal_{iteration.iteration_id or source or 'learning'}",
            source=source,
            target=target,
            confidence=confidence,
            evidence_refs=[{"source": "strategy_iteration", "iteration_id": iteration.iteration_id}],
            update_suggestion={
                "diagnosis": list(iteration.diagnosis),
                "decisions": list(iteration.decisions),
                "next_actions": list(iteration.next_actions),
            },
        )

    def performance_snapshots_from_project(
        self,
        project: AccountOperationProject | dict[str, Any] | None,
    ) -> list[PerformanceSnapshot]:
        normalized = project if isinstance(project, AccountOperationProject) else AccountOperationProject.from_dict(project)
        return [self.performance_snapshot(snapshot) for snapshot in normalized.metrics_snapshots]

    def learning_signals_from_project(
        self,
        project: AccountOperationProject | dict[str, Any] | None,
        *,
        source: str,
        target: str,
        confidence: float = 0.5,
    ) -> list[LearningSignal]:
        normalized = project if isinstance(project, AccountOperationProject) else AccountOperationProject.from_dict(project)
        signals = [
            self.learning_signal(
                source=source,
                target=target,
                strategy_iteration=iteration,
                confidence=confidence,
            )
            for iteration in normalized.strategy_iterations
        ]
        for signal in signals:
            signal.metadata.update({
                "project_id": normalized.project_id,
                "project_name": normalized.name,
            })
        return signals

    def capability_snapshot_from_project(
        self,
        project: AccountOperationProject | dict[str, Any] | None,
        *,
        task_ids: list[str] | None = None,
        selected_candidate_ids: dict[str, str] | None = None,
        signal_source: str,
        signal_target: str,
        confidence: float = 0.5,
    ) -> CapabilitySnapshot:
        normalized = project if isinstance(project, AccountOperationProject) else AccountOperationProject.from_dict(project)
        selected_by_task = dict(selected_candidate_ids or {})
        resolved_task_ids = _project_task_ids(normalized, task_ids)
        context_builder = ContextPackBuilder()
        generation = ContentGenerationFacade()
        context_packs = [
            context_builder.build_from_project(normalized, task_id=task_id)
            for task_id in resolved_task_ids
        ]
        candidate_sets = [
            generation.candidate_set_from_project(
                normalized,
                task_id=task_id,
                selected_candidate_id=selected_by_task.get(task_id, ""),
                context_pack=context_pack,
            )
            for task_id, context_pack in zip(resolved_task_ids, context_packs)
        ]
        return CapabilitySnapshot(
            snapshot_id=f"capability_{normalized.project_id or 'project'}",
            project_id=normalized.project_id,
            capability_names=capability_module_names(),
            user_profile=UserProfilingFacade().build_from_project(normalized),
            market_analysis=MarketAnalysisFacade().build_from_project(normalized),
            context_packs=context_packs,
            candidate_sets=candidate_sets,
            performance_snapshots=self.performance_snapshots_from_project(normalized),
            learning_signals=self.learning_signals_from_project(
                normalized,
                source=signal_source,
                target=signal_target,
                confidence=confidence,
            ),
            source_refs=[{
                "source": "account_operation_project",
                "project_id": normalized.project_id,
            }],
            metadata={
                "project_name": normalized.name,
                "task_count": len(resolved_task_ids),
            },
        )

def _project_task_ids(project: AccountOperationProject, task_ids: list[str] | None) -> list[str]:
    requested = _dedupe_strings(task_ids or [])
    if requested:
        return requested
    task_ids_from_tasks = [task.task_id for task in [*project.content_tasks, *project.content_calendar.tasks]]
    task_ids_from_packages = [package.task_id for package in project.content_packages]
    return _dedupe_strings([*task_ids_from_tasks, *task_ids_from_packages])


def _dedupe_strings(values: list[str]) -> list[str]:
    seen = set()
    result = []
    for value in values:
        normalized = str(value or "").strip()
        if normalized and normalized not in seen:
            seen.add(normalized)
            result.append(normalized)
    return result


__all__ = ["LearningLoopFacade"]
