"""Market analysis facade over competitor research and hot examples."""
from __future__ import annotations

from typing import Any

from nori.core import MarketAnalysis, WorkflowBase, named_workflow_steps

from .schemas import CompetitorResearch


class MarketAnalysisFacade(WorkflowBase):
    """Build market-analysis contracts from existing evidence models."""

    module_name = "market_analysis"

    def __init__(self) -> None:
        super().__init__(
            workflow_name=self.module_name,
            steps=named_workflow_steps("competitor_research", "market_analysis"),
        )

    def build_analysis(
        self,
        research: CompetitorResearch | dict[str, Any] | None = None,
        *,
        hot_examples: list[dict[str, Any]] | None = None,
        audience_insights: list[str] | None = None,
    ) -> MarketAnalysis:
        normalized = research if isinstance(research, CompetitorResearch) else CompetitorResearch.from_dict(research)
        return MarketAnalysis(
            analysis_id=normalized.research_id,
            platform=normalized.platform,
            keywords=list(normalized.keywords),
            competitor_samples=[sample.to_dict() for sample in normalized.samples],
            hot_examples=list(hot_examples or []),
            trend_insights=list(normalized.insights),
            audience_insights=list(audience_insights or []),
            source_refs=[{"source": "competitor_research", "research_id": normalized.research_id}],
        )

    def build_from_project(
        self,
        project: Any,
        *,
        hot_examples: list[dict[str, Any]] | None = None,
        audience_insights: list[str] | None = None,
    ) -> MarketAnalysis:
        project_data = _project_data(project)
        project_id = str(project_data.get("project_id") or "")
        project_name = str(project_data.get("name") or "")
        analysis = self.build_analysis(
            project_data.get("competitor_research"),
            hot_examples=hot_examples,
            audience_insights=audience_insights,
        )
        analysis.source_refs.append({
            "source": "account_operation_project",
            "project_id": project_id,
        })
        analysis.metadata.update({
            "project_id": project_id,
            "project_name": project_name,
        })
        return analysis


def _project_data(project: Any) -> dict[str, Any]:
    if hasattr(project, "to_dict"):
        return project.to_dict()
    return dict(project or {})


__all__ = ["MarketAnalysisFacade"]
