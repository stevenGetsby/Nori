"""Planning and task contracts shared across Nori workflow stages."""
from __future__ import annotations

from typing import Any

from nori._compat import dataclass, field
from nori.core.contracts import dict_list as _dict_list
from nori.core.contracts import int_value as _int
from nori.core.contracts import mapping as _mapping
from nori.core.contracts import mapping_list as _mapping_list
from nori.core.contracts import string_list as _string_list


@dataclass(slots=True)
class ClientBrief:
    """Client-facing requirements shared across planning, production, and review."""

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
    """A single scheduled content unit shared by planning, generation, and review."""

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
class IntentContract:
    """Frozen acceptance contract shared by generation and review stages."""

    contract_id: str = ""
    brand_name: str = ""
    platform: str = "xhs"
    primary_goal: str = ""
    business_goals: list[str] = field(default_factory=list)
    audience: list[str] = field(default_factory=list)
    positioning_notes: list[str] = field(default_factory=list)
    must_include: list[str] = field(default_factory=list)
    tone: list[str] = field(default_factory=list)
    deliverables: list[str] = field(default_factory=list)
    taboos: list[str] = field(default_factory=list)
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "contract_id": self.contract_id,
            "brand_name": self.brand_name,
            "platform": self.platform,
            "primary_goal": self.primary_goal,
            "business_goals": list(self.business_goals),
            "audience": list(self.audience),
            "positioning_notes": list(self.positioning_notes),
            "must_include": list(self.must_include),
            "tone": list(self.tone),
            "deliverables": list(self.deliverables),
            "taboos": list(self.taboos),
            "source_refs": _dict_list(self.source_refs),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "IntentContract":
        data = _mapping(data)
        return cls(
            contract_id=str(data.get("contract_id") or ""),
            brand_name=str(data.get("brand_name") or ""),
            platform=str(data.get("platform") or "xhs"),
            primary_goal=str(data.get("primary_goal") or ""),
            business_goals=_string_list(data.get("business_goals")),
            audience=_string_list(data.get("audience")),
            positioning_notes=_string_list(data.get("positioning_notes")),
            must_include=_string_list(data.get("must_include")),
            tone=_string_list(data.get("tone")),
            deliverables=_string_list(data.get("deliverables")),
            taboos=_string_list(data.get("taboos")),
            source_refs=_dict_list(data.get("source_refs")),
            metadata=_mapping(data.get("metadata")),
        )

    @classmethod
    def from_brief_and_task(
        cls,
        brief: "ClientBrief" | dict[str, Any] | None,
        task: ContentTask | dict[str, Any] | None,
        *,
        contract_id: str = "",
    ) -> "IntentContract":
        normalized_brief = brief if isinstance(brief, ClientBrief) else ClientBrief.from_dict(brief)
        normalized_task = task if isinstance(task, ContentTask) else ContentTask.from_dict(task)
        task_brief = dict(normalized_task.brief or {})
        brand_name = normalized_brief.brand_name
        topic = normalized_task.topic or normalized_task.title
        deliverable = str(task_brief.get("deliverable") or normalized_task.content_type or "").strip()
        return cls(
            contract_id=contract_id or f"intent_{normalized_task.task_id or 'default'}",
            brand_name=brand_name,
            platform=normalized_task.platform or normalized_brief.platform,
            primary_goal=normalized_task.objective or (normalized_brief.goals[0] if normalized_brief.goals else ""),
            business_goals=list(normalized_brief.goals),
            audience=list(normalized_brief.audience),
            positioning_notes=list(normalized_brief.positioning_notes),
            must_include=_dedupe_contract_terms([
                brand_name,
                topic,
                *_string_list(task_brief.get("must_include")),
            ]),
            tone=_dedupe_contract_terms([
                *tone_terms(normalized_brief.constraints),
                *_string_list(task_brief.get("tone")),
            ]),
            deliverables=[deliverable] if deliverable else [],
            taboos=list(normalized_brief.taboos),
            source_refs=[
                {"source": "client_brief", "brand_name": brand_name},
                {"source": "content_task", "task_id": normalized_task.task_id},
            ],
        )

    def missing_terms(self, text: str) -> list[str]:
        haystack = str(text or "")
        return [term for term in self.must_include if term and term not in haystack]


def tone_terms(constraints: list[str]) -> list[str]:
    known = ["不羁", "自信", "有趣", "搞怪", "走心", "犀利", "亲和", "反叛", "温暖"]
    text = "\n".join(constraints)
    return [term for term in known if term in text]


def _dedupe_contract_terms(values: list[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for value in values:
        text = str(value or "").strip()
        if text and text not in seen:
            out.append(text)
            seen.add(text)
    return out


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


__all__ = [
    "ClientBrief",
    "ContentCalendar",
    "ContentTask",
    "IntentContract",
    "KPIPlan",
    "OperationPlan",
    "tone_terms",
]
