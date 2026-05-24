"""Account-operations SOP data models.

These contracts are intentionally provider-free. They describe the account
operations loop that future ops agents can plan, persist, and test without
calling live LLM, crawler, or publishing services.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ClientBrief:
    """Client-facing requirements for an account operation project."""

    client_name: str = ""
    brand_name: str = ""
    platform: str = "xhs"
    goals: list[str] = field(default_factory=list)
    audience: list[str] = field(default_factory=list)
    positioning_notes: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    taboos: list[str] = field(default_factory=list)
    source_materials: list[dict[str, Any]] = field(default_factory=list)
    context: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "client_name": self.client_name,
            "brand_name": self.brand_name,
            "platform": self.platform,
            "goals": list(self.goals),
            "audience": list(self.audience),
            "positioning_notes": list(self.positioning_notes),
            "constraints": list(self.constraints),
            "taboos": list(self.taboos),
            "source_materials": _dict_list(self.source_materials),
            "context": dict(self.context),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "ClientBrief":
        data = _mapping(data)
        return cls(
            client_name=str(data.get("client_name") or ""),
            brand_name=str(data.get("brand_name") or ""),
            platform=str(data.get("platform") or "xhs"),
            goals=_string_list(data.get("goals")),
            audience=_string_list(data.get("audience")),
            positioning_notes=_string_list(data.get("positioning_notes")),
            constraints=_string_list(data.get("constraints")),
            taboos=_string_list(data.get("taboos")),
            source_materials=_dict_list(data.get("source_materials")),
            context=_mapping(data.get("context")),
        )


@dataclass(slots=True)
class OperationPlan:
    """Strategy and cadence for a bounded account operation cycle."""

    plan_id: str = ""
    horizon_days: int = 30
    objectives: list[str] = field(default_factory=list)
    content_pillars: list[str] = field(default_factory=list)
    cadence: str = ""
    kpi_targets: dict[str, Any] = field(default_factory=dict)
    milestones: list[dict[str, Any]] = field(default_factory=list)
    risk_controls: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "plan_id": self.plan_id,
            "horizon_days": self.horizon_days,
            "objectives": list(self.objectives),
            "content_pillars": list(self.content_pillars),
            "cadence": self.cadence,
            "kpi_targets": dict(self.kpi_targets),
            "milestones": _dict_list(self.milestones),
            "risk_controls": list(self.risk_controls),
            "notes": list(self.notes),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "OperationPlan":
        data = _mapping(data)
        return cls(
            plan_id=str(data.get("plan_id") or ""),
            horizon_days=_int(data.get("horizon_days"), default=30),
            objectives=_string_list(data.get("objectives")),
            content_pillars=_string_list(data.get("content_pillars")),
            cadence=str(data.get("cadence") or ""),
            kpi_targets=_mapping(data.get("kpi_targets")),
            milestones=_dict_list(data.get("milestones")),
            risk_controls=_string_list(data.get("risk_controls")),
            notes=_string_list(data.get("notes")),
        )


@dataclass(slots=True)
class KPIPlan:
    """Measurable targets for an operation plan."""

    plan_id: str = ""
    horizon_days: int = 30
    targets: dict[str, Any] = field(default_factory=dict)
    milestones: list[dict[str, Any]] = field(default_factory=list)
    measurement_notes: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "plan_id": self.plan_id,
            "horizon_days": self.horizon_days,
            "targets": dict(self.targets),
            "milestones": _dict_list(self.milestones),
            "measurement_notes": list(self.measurement_notes),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "KPIPlan":
        data = _mapping(data)
        return cls(
            plan_id=str(data.get("plan_id") or ""),
            horizon_days=_int(data.get("horizon_days"), default=30),
            targets=_mapping(data.get("targets")),
            milestones=_dict_list(data.get("milestones")),
            measurement_notes=_string_list(data.get("measurement_notes")),
            metadata=_mapping(data.get("metadata")),
        )


@dataclass(slots=True)
class ContentTask:
    """A single scheduled content unit in the account operation workflow."""

    task_id: str = ""
    title: str = ""
    scheduled_date: str = ""
    platform: str = "xhs"
    content_type: str = "note"
    topic: str = ""
    objective: str = ""
    status: str = "planned"
    priority: int = 0
    owner: str = ""
    brief: dict[str, Any] = field(default_factory=dict)
    required_assets: list[str] = field(default_factory=list)
    references: list[dict[str, Any]] = field(default_factory=list)
    package_id: str = ""
    notes: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "title": self.title,
            "scheduled_date": self.scheduled_date,
            "platform": self.platform,
            "content_type": self.content_type,
            "topic": self.topic,
            "objective": self.objective,
            "status": self.status,
            "priority": self.priority,
            "owner": self.owner,
            "brief": dict(self.brief),
            "required_assets": list(self.required_assets),
            "references": _dict_list(self.references),
            "package_id": self.package_id,
            "notes": list(self.notes),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "ContentTask":
        data = _mapping(data)
        return cls(
            task_id=str(data.get("task_id") or ""),
            title=str(data.get("title") or ""),
            scheduled_date=str(data.get("scheduled_date") or ""),
            platform=str(data.get("platform") or "xhs"),
            content_type=str(data.get("content_type") or "note"),
            topic=str(data.get("topic") or ""),
            objective=str(data.get("objective") or ""),
            status=str(data.get("status") or "planned"),
            priority=_int(data.get("priority"), default=0),
            owner=str(data.get("owner") or ""),
            brief=_mapping(data.get("brief")),
            required_assets=_string_list(data.get("required_assets")),
            references=_dict_list(data.get("references")),
            package_id=str(data.get("package_id") or ""),
            notes=_string_list(data.get("notes")),
            metadata=_mapping(data.get("metadata")),
        )


@dataclass(slots=True)
class ContentPackage:
    """Generated content artifacts attached to a content task."""

    package_id: str = ""
    task_id: str = ""
    platform: str = "xhs"
    title: str = ""
    body: str = ""
    tags: list[str] = field(default_factory=list)
    cover_path: str = ""
    image_paths: list[str] = field(default_factory=list)
    prompts: dict[str, Any] = field(default_factory=dict)
    material_usage: list[dict[str, Any]] = field(default_factory=list)
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    status: str = "draft"
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "package_id": self.package_id,
            "task_id": self.task_id,
            "platform": self.platform,
            "title": self.title,
            "body": self.body,
            "tags": list(self.tags),
            "cover_path": self.cover_path,
            "image_paths": list(self.image_paths),
            "prompts": dict(self.prompts),
            "material_usage": _dict_list(self.material_usage),
            "source_refs": _dict_list(self.source_refs),
            "status": self.status,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "ContentPackage":
        data = _mapping(data)
        return cls(
            package_id=str(data.get("package_id") or ""),
            task_id=str(data.get("task_id") or ""),
            platform=str(data.get("platform") or "xhs"),
            title=str(data.get("title") or ""),
            body=str(data.get("body") or ""),
            tags=_string_list(data.get("tags")),
            cover_path=str(data.get("cover_path") or ""),
            image_paths=_string_list(data.get("image_paths")),
            prompts=_mapping(data.get("prompts")),
            material_usage=_dict_list(data.get("material_usage")),
            source_refs=_dict_list(data.get("source_refs")),
            status=str(data.get("status") or "draft"),
            metadata=_mapping(data.get("metadata")),
        )


@dataclass(slots=True)
class ComplianceReview:
    """Review report for generated content before publish handoff."""

    review_id: str = ""
    package_id: str = ""
    task_id: str = ""
    status: str = "pending"
    score: int = 0
    issues: list[dict[str, Any]] = field(default_factory=list)
    fix_suggestions: list[str] = field(default_factory=list)
    reviewer: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "review_id": self.review_id,
            "package_id": self.package_id,
            "task_id": self.task_id,
            "status": self.status,
            "score": self.score,
            "issues": _dict_list(self.issues),
            "fix_suggestions": list(self.fix_suggestions),
            "reviewer": self.reviewer,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "ComplianceReview":
        data = _mapping(data)
        return cls(
            review_id=str(data.get("review_id") or ""),
            package_id=str(data.get("package_id") or ""),
            task_id=str(data.get("task_id") or ""),
            status=str(data.get("status") or "pending"),
            score=_int(data.get("score"), default=0),
            issues=_dict_list(data.get("issues")),
            fix_suggestions=_string_list(data.get("fix_suggestions")),
            reviewer=str(data.get("reviewer") or ""),
            metadata=_mapping(data.get("metadata")),
        )


@dataclass(slots=True)
class MetricsSnapshot:
    """Observed metrics for a task, package, or operation cycle."""

    snapshot_id: str = ""
    ref_id: str = ""
    captured_at: str = ""
    metrics: dict[str, Any] = field(default_factory=dict)
    source: str = ""
    notes: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "ref_id": self.ref_id,
            "captured_at": self.captured_at,
            "metrics": dict(self.metrics),
            "source": self.source,
            "notes": list(self.notes),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "MetricsSnapshot":
        data = _mapping(data)
        return cls(
            snapshot_id=str(data.get("snapshot_id") or ""),
            ref_id=str(data.get("ref_id") or ""),
            captured_at=str(data.get("captured_at") or ""),
            metrics=_mapping(data.get("metrics")),
            source=str(data.get("source") or ""),
            notes=_string_list(data.get("notes")),
            metadata=_mapping(data.get("metadata")),
        )


@dataclass(slots=True)
class StrategyIteration:
    """Learning record that turns review and metrics into next-cycle changes."""

    iteration_id: str = ""
    project_id: str = ""
    input_refs: list[str] = field(default_factory=list)
    diagnosis: list[str] = field(default_factory=list)
    decisions: list[str] = field(default_factory=list)
    next_actions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "iteration_id": self.iteration_id,
            "project_id": self.project_id,
            "input_refs": list(self.input_refs),
            "diagnosis": list(self.diagnosis),
            "decisions": list(self.decisions),
            "next_actions": list(self.next_actions),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "StrategyIteration":
        data = _mapping(data)
        return cls(
            iteration_id=str(data.get("iteration_id") or ""),
            project_id=str(data.get("project_id") or ""),
            input_refs=_string_list(data.get("input_refs")),
            diagnosis=_string_list(data.get("diagnosis")),
            decisions=_string_list(data.get("decisions")),
            next_actions=_string_list(data.get("next_actions")),
            metadata=_mapping(data.get("metadata")),
        )


@dataclass(slots=True)
class ContentCalendar:
    """Calendar-level grouping for account operation content tasks."""

    calendar_id: str = ""
    start_date: str = ""
    end_date: str = ""
    cadence: str = ""
    themes: list[str] = field(default_factory=list)
    tasks: list[ContentTask] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "calendar_id": self.calendar_id,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "cadence": self.cadence,
            "themes": list(self.themes),
            "tasks": [task.to_dict() for task in self.tasks],
            "notes": list(self.notes),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "ContentCalendar":
        data = _mapping(data)
        return cls(
            calendar_id=str(data.get("calendar_id") or ""),
            start_date=str(data.get("start_date") or ""),
            end_date=str(data.get("end_date") or ""),
            cadence=str(data.get("cadence") or ""),
            themes=_string_list(data.get("themes")),
            tasks=[ContentTask.from_dict(item) for item in _mapping_list(data.get("tasks"))],
            notes=_string_list(data.get("notes")),
            metadata=_mapping(data.get("metadata")),
        )


@dataclass(slots=True)
class AccountOperationProject:
    """Top-level account operation workspace for one client/account."""

    project_id: str = ""
    name: str = ""
    status: str = "draft"
    client_brief: ClientBrief = field(default_factory=ClientBrief)
    account_positioning: dict[str, Any] = field(default_factory=dict)
    operation_plan: OperationPlan = field(default_factory=OperationPlan)
    kpi_plan: KPIPlan = field(default_factory=KPIPlan)
    content_calendar: ContentCalendar = field(default_factory=ContentCalendar)
    content_tasks: list[ContentTask] = field(default_factory=list)
    content_packages: list[ContentPackage] = field(default_factory=list)
    compliance_reviews: list[ComplianceReview] = field(default_factory=list)
    metrics_snapshots: list[MetricsSnapshot] = field(default_factory=list)
    strategy_iterations: list[StrategyIteration] = field(default_factory=list)
    artifacts: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "project_id": self.project_id,
            "name": self.name,
            "status": self.status,
            "client_brief": self.client_brief.to_dict(),
            "account_positioning": dict(self.account_positioning),
            "operation_plan": self.operation_plan.to_dict(),
            "kpi_plan": self.kpi_plan.to_dict(),
            "content_calendar": self.content_calendar.to_dict(),
            "content_tasks": [task.to_dict() for task in self.content_tasks],
            "content_packages": [package.to_dict() for package in self.content_packages],
            "compliance_reviews": [review.to_dict() for review in self.compliance_reviews],
            "metrics_snapshots": [snapshot.to_dict() for snapshot in self.metrics_snapshots],
            "strategy_iterations": [iteration.to_dict() for iteration in self.strategy_iterations],
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
            account_positioning=_mapping(data.get("account_positioning")),
            operation_plan=OperationPlan.from_dict(data.get("operation_plan")),
            kpi_plan=KPIPlan.from_dict(data.get("kpi_plan")),
            content_calendar=ContentCalendar.from_dict(data.get("content_calendar")),
            content_tasks=[ContentTask.from_dict(item) for item in _mapping_list(data.get("content_tasks"))],
            content_packages=[ContentPackage.from_dict(item) for item in _mapping_list(data.get("content_packages"))],
            compliance_reviews=[
                ComplianceReview.from_dict(item)
                for item in _mapping_list(data.get("compliance_reviews"))
            ],
            metrics_snapshots=[
                MetricsSnapshot.from_dict(item)
                for item in _mapping_list(data.get("metrics_snapshots"))
            ],
            strategy_iterations=[
                StrategyIteration.from_dict(item)
                for item in _mapping_list(data.get("strategy_iterations"))
            ],
            artifacts=_mapping(data.get("artifacts")),
            metadata=_mapping(data.get("metadata")),
        )


def _mapping(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, dict) else {}


def _mapping_list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [dict(item) for item in value if isinstance(item, dict)]


def _dict_list(value: Any) -> list[dict[str, Any]]:
    return _mapping_list(value)


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if not isinstance(value, list):
        return []
    return [str(item) for item in value]


def _int(value: Any, *, default: int) -> int:
    if isinstance(value, bool):
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


__all__ = [
    "AccountOperationProject",
    "ClientBrief",
    "ComplianceReview",
    "ContentCalendar",
    "ContentPackage",
    "ContentTask",
    "KPIPlan",
    "MetricsSnapshot",
    "OperationPlan",
    "StrategyIteration",
]
