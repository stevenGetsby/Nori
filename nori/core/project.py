"""Shared account-operation project aggregate."""
from __future__ import annotations

from typing import Any

from nori._compat import dataclass, field
from nori.core.contracts import mapping as _mapping, mapping_list as _mapping_list

from .models import AssetLibrary, ClientBrief, ContentCalendar, ContentTask, KPIPlan, OperationPlan


@dataclass(slots=True)
class AccountOperationProject:
    """Top-level account operation workspace spanning all business modules."""

    project_id: str = ""
    name: str = ""
    status: str = "draft"
    client_brief: ClientBrief = field(default_factory=ClientBrief)
    account_positioning: Any = field(default_factory=lambda: _new_account_positioning())
    asset_library: AssetLibrary = field(default_factory=AssetLibrary)
    competitor_research: Any = field(default_factory=lambda: _new_competitor_research())
    operation_plan: OperationPlan = field(default_factory=OperationPlan)
    kpi_plan: KPIPlan = field(default_factory=KPIPlan)
    content_calendar: ContentCalendar = field(default_factory=ContentCalendar)
    content_tasks: list[ContentTask] = field(default_factory=list)
    content_packages: list[Any] = field(default_factory=list)
    compliance_reviews: list[Any] = field(default_factory=list)
    metrics_snapshots: list[Any] = field(default_factory=list)
    strategy_iterations: list[Any] = field(default_factory=list)
    artifacts: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.client_brief = _coerce_client_brief(self.client_brief)
        self.account_positioning = _coerce_account_positioning(self.account_positioning)
        self.asset_library = _coerce_asset_library(self.asset_library)
        self.competitor_research = _coerce_competitor_research(self.competitor_research)
        self.operation_plan = _coerce_operation_plan(self.operation_plan)
        self.kpi_plan = _coerce_kpi_plan(self.kpi_plan)
        self.content_calendar = _coerce_content_calendar(self.content_calendar)
        self.content_tasks = [_coerce_content_task(item) for item in self.content_tasks]
        self.content_packages = [_coerce_content_package(item) for item in self.content_packages]
        self.compliance_reviews = [_coerce_compliance_review(item) for item in self.compliance_reviews]
        self.metrics_snapshots = [_coerce_metrics_snapshot(item) for item in self.metrics_snapshots]
        self.strategy_iterations = [_coerce_strategy_iteration(item) for item in self.strategy_iterations]

    def to_dict(self) -> dict[str, Any]:
        return {
            "project_id": self.project_id,
            "name": self.name,
            "status": self.status,
            "client_brief": self.client_brief.to_dict(),
            "account_positioning": _to_mapping(self.account_positioning),
            "asset_library": _to_mapping(self.asset_library),
            "competitor_research": _to_mapping(self.competitor_research),
            "operation_plan": self.operation_plan.to_dict(),
            "kpi_plan": self.kpi_plan.to_dict(),
            "content_calendar": self.content_calendar.to_dict(),
            "content_tasks": [task.to_dict() for task in self.content_tasks],
            "content_packages": [_to_mapping(package) for package in self.content_packages],
            "compliance_reviews": [_to_mapping(review) for review in self.compliance_reviews],
            "metrics_snapshots": [_to_mapping(snapshot) for snapshot in self.metrics_snapshots],
            "strategy_iterations": [_to_mapping(iteration) for iteration in self.strategy_iterations],
            "artifacts": dict(self.artifacts),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "AccountOperationProject":
        data = _mapping(data)
        return cls(
            project_id=str(data.get("project_id") or ""),
            name=str(data.get("name") or ""),
            status=str(data.get("status") or "draft"),
            client_brief=ClientBrief.from_dict(data.get("client_brief")),
            account_positioning=_coerce_account_positioning(data.get("account_positioning")),
            asset_library=_coerce_asset_library(data.get("asset_library")),
            competitor_research=_coerce_competitor_research(data.get("competitor_research")),
            operation_plan=OperationPlan.from_dict(data.get("operation_plan")),
            kpi_plan=KPIPlan.from_dict(data.get("kpi_plan")),
            content_calendar=ContentCalendar.from_dict(data.get("content_calendar")),
            content_tasks=[ContentTask.from_dict(item) for item in _mapping_list(data.get("content_tasks"))],
            content_packages=[_coerce_content_package(item) for item in _mapping_list(data.get("content_packages"))],
            compliance_reviews=[_coerce_compliance_review(item) for item in _mapping_list(data.get("compliance_reviews"))],
            metrics_snapshots=[_coerce_metrics_snapshot(item) for item in _mapping_list(data.get("metrics_snapshots"))],
            strategy_iterations=[_coerce_strategy_iteration(item) for item in _mapping_list(data.get("strategy_iterations"))],
            artifacts=_mapping(data.get("artifacts")),
            metadata=_mapping(data.get("metadata")),
        )


def _to_mapping(value: Any) -> dict[str, Any]:
    if hasattr(value, "to_dict"):
        return value.to_dict()
    return _mapping(value)


def _coerce_client_brief(value: Any) -> ClientBrief:
    return value if isinstance(value, ClientBrief) else ClientBrief.from_dict(value)


def _coerce_operation_plan(value: Any) -> OperationPlan:
    return value if isinstance(value, OperationPlan) else OperationPlan.from_dict(value)


def _coerce_kpi_plan(value: Any) -> KPIPlan:
    return value if isinstance(value, KPIPlan) else KPIPlan.from_dict(value)


def _coerce_content_calendar(value: Any) -> ContentCalendar:
    return value if isinstance(value, ContentCalendar) else ContentCalendar.from_dict(value)


def _coerce_content_task(value: Any) -> ContentTask:
    return value if isinstance(value, ContentTask) else ContentTask.from_dict(value)


def _new_account_positioning() -> Any:
    from nori.user_profiling.models import AccountPositioning

    return AccountPositioning()


def _coerce_account_positioning(value: Any) -> Any:
    from nori.user_profiling.models import AccountPositioning

    return value if isinstance(value, AccountPositioning) else AccountPositioning.from_dict(value)


def _coerce_asset_library(value: Any) -> AssetLibrary:
    return value if isinstance(value, AssetLibrary) else AssetLibrary.from_dict(value)


def _new_competitor_research() -> Any:
    from nori.market_analysis.models import CompetitorResearch

    return CompetitorResearch()


def _coerce_competitor_research(value: Any) -> Any:
    from nori.market_analysis.models import CompetitorResearch

    return value if isinstance(value, CompetitorResearch) else CompetitorResearch.from_dict(value)


def _coerce_content_package(value: Any) -> Any:
    from nori.content_generation.models import ContentPackage

    return value if isinstance(value, ContentPackage) else ContentPackage.from_dict(value)


def _coerce_compliance_review(value: Any) -> Any:
    from nori.learning_loop.models import ComplianceReview

    return value if isinstance(value, ComplianceReview) else ComplianceReview.from_dict(value)


def _coerce_metrics_snapshot(value: Any) -> Any:
    from nori.learning_loop.models import MetricsSnapshot

    return value if isinstance(value, MetricsSnapshot) else MetricsSnapshot.from_dict(value)


def _coerce_strategy_iteration(value: Any) -> Any:
    from nori.learning_loop.models import StrategyIteration

    return value if isinstance(value, StrategyIteration) else StrategyIteration.from_dict(value)


__all__ = ["AccountOperationProject"]
