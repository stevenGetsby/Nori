"""Shared domain contracts for the high-level Nori architecture."""
from __future__ import annotations

from typing import Any

from nori._compat import dataclass, field
from nori.core.contracts import dict_list as _dict_list
from nori.core.contracts import int_value as _int
from nori.core.contracts import mapping as _mapping
from nori.core.contracts import mapping_list as _mapping_list
from nori.core.contracts import string_list as _string_list


@dataclass(slots=True)
class UserProfile:
    """Long-lived user/account/brand profile used before task-specific work."""

    user_id: str = ""
    display_name: str = ""
    platform: str = "xhs"
    account_profile: dict[str, Any] = field(default_factory=dict)
    brand_profile: dict[str, Any] = field(default_factory=dict)
    preferences: dict[str, Any] = field(default_factory=dict)
    constraints: list[str] = field(default_factory=list)
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "user_id": self.user_id,
            "display_name": self.display_name,
            "platform": self.platform,
            "account_profile": dict(self.account_profile),
            "brand_profile": dict(self.brand_profile),
            "preferences": dict(self.preferences),
            "constraints": list(self.constraints),
            "source_refs": _dict_rows(self.source_refs),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "UserProfile":
        data = _mapping(data)
        return cls(
            user_id=str(data.get("user_id") or ""),
            display_name=str(data.get("display_name") or data.get("name") or ""),
            platform=str(data.get("platform") or "xhs"),
            account_profile=_mapping(data.get("account_profile")),
            brand_profile=_mapping(data.get("brand_profile")),
            preferences=_mapping(data.get("preferences")),
            constraints=_string_list(data.get("constraints")),
            source_refs=_mapping_list(data.get("source_refs")),
            metadata=_mapping(data.get("metadata")),
        )


@dataclass(slots=True)
class UserAsset:
    """One user-provided image or text asset shared across workflow stages."""

    kind: str
    path: str = ""
    text: str = ""
    vision_roles: list[str] = field(default_factory=list)
    subject: str = ""
    brand_signals: list[str] = field(default_factory=list)
    usable_for: list[str] = field(default_factory=list)
    quality: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "path": self.path,
            "text": self.text,
            "vision_roles": list(self.vision_roles),
            "subject": self.subject,
            "brand_signals": list(self.brand_signals),
            "usable_for": list(self.usable_for),
            "quality": self.quality,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "UserAsset":
        data = _mapping(data)
        kind = str(data.get("kind") or "")
        if not kind:
            kind = "image" if data.get("path") else "text" if data.get("text") else ""
        return cls(
            kind=kind,
            path=str(data.get("path") or ""),
            text=str(data.get("text") or ""),
            vision_roles=_string_list(data.get("vision_roles"), drop_blank=True),
            subject=str(data.get("subject") or ""),
            brand_signals=_string_list(data.get("brand_signals"), drop_blank=True),
            usable_for=_string_list(data.get("usable_for"), drop_blank=True),
            quality=str(data.get("quality") or ""),
        )


@dataclass(slots=True)
class AssetRecord:
    """A normalized client or production asset reference."""

    asset_id: str = ""
    kind: str = ""
    path: str = ""
    text: str = ""
    usage: list[str] = field(default_factory=list)
    status: str = "available"
    tags: list[str] = field(default_factory=list)
    source: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "asset_id": self.asset_id,
            "kind": self.kind,
            "path": self.path,
            "text": self.text,
            "usage": list(self.usage),
            "status": self.status,
            "tags": list(self.tags),
            "source": self.source,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "AssetRecord":
        data = _mapping(data)
        return cls(
            asset_id=str(data.get("asset_id") or data.get("id") or ""),
            kind=str(data.get("kind") or ""),
            path=str(data.get("path") or ""),
            text=str(data.get("text") or ""),
            usage=_string_list(data.get("usage") or data.get("usable_for")),
            status=str(data.get("status") or "available"),
            tags=_string_list(data.get("tags")),
            source=str(data.get("source") or ""),
            metadata=_mapping(data.get("metadata")),
        )


@dataclass(slots=True)
class AssetLibrary:
    """Project-level asset index for source materials and generated assets."""

    library_id: str = ""
    assets: list[AssetRecord] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "library_id": self.library_id,
            "assets": [asset.to_dict() for asset in self.assets],
            "notes": list(self.notes),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "AssetLibrary":
        data = _mapping(data)
        return cls(
            library_id=str(data.get("library_id") or ""),
            assets=[AssetRecord.from_dict(item) for item in _mapping_list(data.get("assets"))],
            notes=_string_list(data.get("notes")),
            metadata=_mapping(data.get("metadata")),
        )

    def get(self, asset_id: str) -> AssetRecord | None:
        for asset in self.assets:
            if asset.asset_id == asset_id:
                return asset
        return None

    def usable_assets(self, usage: str | None = None) -> list[AssetRecord]:
        return [
            asset
            for asset in self.assets
            if asset.status == "available" and (usage is None or usage in asset.usage)
        ]


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


@dataclass(slots=True)
class MarketAnalysis:
    """Market and competitor evidence snapshot consumed by context building."""

    analysis_id: str = ""
    platform: str = "xhs"
    keywords: list[str] = field(default_factory=list)
    competitor_samples: list[dict[str, Any]] = field(default_factory=list)
    hot_examples: list[dict[str, Any]] = field(default_factory=list)
    trend_insights: list[str] = field(default_factory=list)
    audience_insights: list[str] = field(default_factory=list)
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "analysis_id": self.analysis_id,
            "platform": self.platform,
            "keywords": list(self.keywords),
            "competitor_samples": _dict_rows(self.competitor_samples),
            "hot_examples": _dict_rows(self.hot_examples),
            "trend_insights": list(self.trend_insights),
            "audience_insights": list(self.audience_insights),
            "source_refs": _dict_rows(self.source_refs),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "MarketAnalysis":
        data = _mapping(data)
        return cls(
            analysis_id=str(data.get("analysis_id") or ""),
            platform=str(data.get("platform") or "xhs"),
            keywords=_string_list(data.get("keywords")),
            competitor_samples=_mapping_list(data.get("competitor_samples")),
            hot_examples=_mapping_list(data.get("hot_examples")),
            trend_insights=_string_list(data.get("trend_insights")),
            audience_insights=_string_list(data.get("audience_insights")),
            source_refs=_mapping_list(data.get("source_refs")),
            metadata=_mapping(data.get("metadata")),
        )


@dataclass(slots=True)
class DecisionPoint:
    """One explicit human/system decision slot in the workflow."""

    decision_id: str = ""
    kind: str = ""
    options: list[dict[str, Any]] = field(default_factory=list)
    recommended_option: str = ""
    selected_option: str = ""
    rationale: str = ""
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    human_notes: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "kind": self.kind,
            "options": _dict_rows(self.options),
            "recommended_option": self.recommended_option,
            "selected_option": self.selected_option,
            "rationale": self.rationale,
            "evidence_refs": _dict_rows(self.evidence_refs),
            "human_notes": self.human_notes,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "DecisionPoint":
        data = _mapping(data)
        return cls(
            decision_id=str(data.get("decision_id") or ""),
            kind=str(data.get("kind") or ""),
            options=_mapping_list(data.get("options")),
            recommended_option=str(data.get("recommended_option") or ""),
            selected_option=str(data.get("selected_option") or ""),
            rationale=str(data.get("rationale") or ""),
            evidence_refs=_mapping_list(data.get("evidence_refs")),
            human_notes=str(data.get("human_notes") or ""),
            metadata=_mapping(data.get("metadata")),
        )


@dataclass(slots=True)
class ExplanationTrace:
    """xAI trace for decisions, candidate generation, reviews, and learning."""

    trace_id: str = ""
    input_refs: list[str] = field(default_factory=list)
    retrieved_evidence: list[dict[str, Any]] = field(default_factory=list)
    decisions: list[dict[str, Any]] = field(default_factory=list)
    stage_steps: list[dict[str, Any]] = field(default_factory=list)
    selected_assets: list[dict[str, Any]] = field(default_factory=list)
    selected_skill: str = ""
    review_findings: list[dict[str, Any]] = field(default_factory=list)
    final_rationale: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "input_refs": list(self.input_refs),
            "retrieved_evidence": _dict_rows(self.retrieved_evidence),
            "decisions": _dict_rows(self.decisions),
            "stage_steps": _dict_rows(self.stage_steps),
            "selected_assets": _dict_rows(self.selected_assets),
            "selected_skill": self.selected_skill,
            "review_findings": _dict_rows(self.review_findings),
            "final_rationale": self.final_rationale,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "ExplanationTrace":
        data = _mapping(data)
        return cls(
            trace_id=str(data.get("trace_id") or ""),
            input_refs=_string_list(data.get("input_refs")),
            retrieved_evidence=_mapping_list(data.get("retrieved_evidence")),
            decisions=_mapping_list(data.get("decisions")),
            stage_steps=_stage_rows(data.get("stage_steps") or data.get("agent_steps")),
            selected_assets=_mapping_list(data.get("selected_assets")),
            selected_skill=str(data.get("selected_skill") or ""),
            review_findings=_mapping_list(data.get("review_findings")),
            final_rationale=str(data.get("final_rationale") or ""),
            metadata=_mapping(data.get("metadata")),
        )


@dataclass(slots=True)
class ContextPack:
    """Unified context bundle consumed by decision and generation modules."""

    context_pack_id: str = ""
    user_profile: UserProfile = field(default_factory=UserProfile)
    task_intent: dict[str, Any] = field(default_factory=dict)
    market_analysis: MarketAnalysis = field(default_factory=MarketAnalysis)
    assets: list[dict[str, Any]] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    decision_points: list[DecisionPoint] = field(default_factory=list)
    explanation_trace: ExplanationTrace = field(default_factory=ExplanationTrace)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "context_pack_id": self.context_pack_id,
            "user_profile": self.user_profile.to_dict(),
            "task_intent": dict(self.task_intent),
            "market_analysis": self.market_analysis.to_dict(),
            "assets": _dict_rows(self.assets),
            "constraints": list(self.constraints),
            "evidence_refs": _dict_rows(self.evidence_refs),
            "decision_points": [point.to_dict() for point in self.decision_points],
            "explanation_trace": self.explanation_trace.to_dict(),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "ContextPack":
        data = _mapping(data)
        return cls(
            context_pack_id=str(data.get("context_pack_id") or ""),
            user_profile=UserProfile.from_dict(data.get("user_profile")),
            task_intent=_mapping(data.get("task_intent")),
            market_analysis=MarketAnalysis.from_dict(data.get("market_analysis")),
            assets=_mapping_list(data.get("assets")),
            constraints=_string_list(data.get("constraints")),
            evidence_refs=_mapping_list(data.get("evidence_refs")),
            decision_points=[DecisionPoint.from_dict(item) for item in _mapping_list(data.get("decision_points"))],
            explanation_trace=ExplanationTrace.from_dict(data.get("explanation_trace")),
            metadata=_mapping(data.get("metadata")),
        )


@dataclass(slots=True)
class CandidateSet:
    """Multiple generated candidates before human selection/finalization."""

    candidate_set_id: str = ""
    task_id: str = ""
    candidates: list[dict[str, Any]] = field(default_factory=list)
    selected_candidate_id: str = ""
    decision_point: DecisionPoint = field(default_factory=DecisionPoint)
    explanation_trace: ExplanationTrace = field(default_factory=ExplanationTrace)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_set_id": self.candidate_set_id,
            "task_id": self.task_id,
            "candidates": _dict_rows(self.candidates),
            "selected_candidate_id": self.selected_candidate_id,
            "decision_point": self.decision_point.to_dict(),
            "explanation_trace": self.explanation_trace.to_dict(),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "CandidateSet":
        data = _mapping(data)
        return cls(
            candidate_set_id=str(data.get("candidate_set_id") or ""),
            task_id=str(data.get("task_id") or ""),
            candidates=_mapping_list(data.get("candidates")),
            selected_candidate_id=str(data.get("selected_candidate_id") or ""),
            decision_point=DecisionPoint.from_dict(data.get("decision_point")),
            explanation_trace=ExplanationTrace.from_dict(data.get("explanation_trace")),
            metadata=_mapping(data.get("metadata")),
        )


@dataclass(slots=True)
class PerformanceSnapshot:
    """Normalized monitoring snapshot for one generated package/task."""

    snapshot_id: str = ""
    ref_id: str = ""
    metrics: dict[str, Any] = field(default_factory=dict)
    source: str = "manual"
    captured_at: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "ref_id": self.ref_id,
            "metrics": dict(self.metrics),
            "source": self.source,
            "captured_at": self.captured_at,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "PerformanceSnapshot":
        data = _mapping(data)
        return cls(
            snapshot_id=str(data.get("snapshot_id") or ""),
            ref_id=str(data.get("ref_id") or ""),
            metrics=_mapping(data.get("metrics")),
            source=str(data.get("source") or "manual"),
            captured_at=str(data.get("captured_at") or ""),
            metadata=_mapping(data.get("metadata")),
        )


@dataclass(slots=True)
class LearningSignal:
    """A learning event that can update preference, market memory, or strategy."""

    signal_id: str = ""
    source: str = ""
    target: str = ""
    confidence: float = 0.0
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    update_suggestion: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "signal_id": self.signal_id,
            "source": self.source,
            "target": self.target,
            "confidence": self.confidence,
            "evidence_refs": _dict_rows(self.evidence_refs),
            "update_suggestion": dict(self.update_suggestion),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "LearningSignal":
        data = _mapping(data)
        return cls(
            signal_id=str(data.get("signal_id") or ""),
            source=str(data.get("source") or ""),
            target=str(data.get("target") or ""),
            confidence=_float(data.get("confidence")),
            evidence_refs=_mapping_list(data.get("evidence_refs")),
            update_suggestion=_mapping(data.get("update_suggestion")),
            metadata=_mapping(data.get("metadata")),
        )


@dataclass(slots=True)
class CapabilitySnapshot:
    """Complete capability-level view for one operation project or workflow run."""

    snapshot_id: str = ""
    project_id: str = ""
    capability_names: list[str] = field(default_factory=list)
    user_profile: UserProfile = field(default_factory=UserProfile)
    market_analysis: MarketAnalysis = field(default_factory=MarketAnalysis)
    context_packs: list[ContextPack] = field(default_factory=list)
    candidate_sets: list[CandidateSet] = field(default_factory=list)
    performance_snapshots: list[PerformanceSnapshot] = field(default_factory=list)
    learning_signals: list[LearningSignal] = field(default_factory=list)
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "project_id": self.project_id,
            "capability_names": list(self.capability_names),
            "user_profile": self.user_profile.to_dict(),
            "market_analysis": self.market_analysis.to_dict(),
            "context_packs": [pack.to_dict() for pack in self.context_packs],
            "candidate_sets": [candidate_set.to_dict() for candidate_set in self.candidate_sets],
            "performance_snapshots": [snapshot.to_dict() for snapshot in self.performance_snapshots],
            "learning_signals": [signal.to_dict() for signal in self.learning_signals],
            "source_refs": _dict_rows(self.source_refs),
            "metadata": dict(self.metadata),
        }

    def validate(self) -> list[dict[str, Any]]:
        issues: list[dict[str, Any]] = []
        _validate_required_capabilities(issues, self.capability_names)
        _validate_candidate_context(issues, self.context_packs, self.candidate_sets)
        return issues

    def is_valid(self) -> bool:
        return not self.validate()

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "CapabilitySnapshot":
        data = _mapping(data)
        return cls(
            snapshot_id=str(data.get("snapshot_id") or ""),
            project_id=str(data.get("project_id") or ""),
            capability_names=_string_list(data.get("capability_names") or data.get("module_names")),
            user_profile=UserProfile.from_dict(data.get("user_profile")),
            market_analysis=MarketAnalysis.from_dict(data.get("market_analysis")),
            context_packs=[ContextPack.from_dict(item) for item in _mapping_list(data.get("context_packs"))],
            candidate_sets=[CandidateSet.from_dict(item) for item in _mapping_list(data.get("candidate_sets"))],
            performance_snapshots=[
                PerformanceSnapshot.from_dict(item)
                for item in _mapping_list(data.get("performance_snapshots"))
            ],
            learning_signals=[
                LearningSignal.from_dict(item)
                for item in _mapping_list(data.get("learning_signals"))
            ],
            source_refs=_mapping_list(data.get("source_refs")),
            metadata=_mapping(data.get("metadata")),
        )


@dataclass(slots=True)
class DomainSnapshot:
    """Complete projected domain view for one operation project or workflow run."""

    snapshot_id: str = ""
    project_id: str = ""
    module_names: list[str] = field(default_factory=list)
    user_profile: UserProfile = field(default_factory=UserProfile)
    market_analysis: MarketAnalysis = field(default_factory=MarketAnalysis)
    context_packs: list[ContextPack] = field(default_factory=list)
    candidate_sets: list[CandidateSet] = field(default_factory=list)
    performance_snapshots: list[PerformanceSnapshot] = field(default_factory=list)
    learning_signals: list[LearningSignal] = field(default_factory=list)
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "project_id": self.project_id,
            "module_names": list(self.module_names),
            "user_profile": self.user_profile.to_dict(),
            "market_analysis": self.market_analysis.to_dict(),
            "context_packs": [pack.to_dict() for pack in self.context_packs],
            "candidate_sets": [candidate_set.to_dict() for candidate_set in self.candidate_sets],
            "performance_snapshots": [snapshot.to_dict() for snapshot in self.performance_snapshots],
            "learning_signals": [signal.to_dict() for signal in self.learning_signals],
            "source_refs": _dict_rows(self.source_refs),
            "metadata": dict(self.metadata),
        }

    def validate(self) -> list[dict[str, Any]]:
        issues: list[dict[str, Any]] = []
        _validate_required_modules(issues, self.module_names)
        _validate_candidate_context(issues, self.context_packs, self.candidate_sets)
        return issues

    def is_valid(self) -> bool:
        return not self.validate()

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "DomainSnapshot":
        data = _mapping(data)
        return cls(
            snapshot_id=str(data.get("snapshot_id") or ""),
            project_id=str(data.get("project_id") or ""),
            module_names=_string_list(data.get("module_names")),
            user_profile=UserProfile.from_dict(data.get("user_profile")),
            market_analysis=MarketAnalysis.from_dict(data.get("market_analysis")),
            context_packs=[ContextPack.from_dict(item) for item in _mapping_list(data.get("context_packs"))],
            candidate_sets=[CandidateSet.from_dict(item) for item in _mapping_list(data.get("candidate_sets"))],
            performance_snapshots=[
                PerformanceSnapshot.from_dict(item)
                for item in _mapping_list(data.get("performance_snapshots"))
            ],
            learning_signals=[
                LearningSignal.from_dict(item)
                for item in _mapping_list(data.get("learning_signals"))
            ],
            source_refs=_mapping_list(data.get("source_refs")),
            metadata=_mapping(data.get("metadata")),
        )


def _dict_rows(values: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [dict(value) for value in values if isinstance(value, dict)]


def _stage_rows(values: Any) -> list[dict[str, Any]]:
    rows = _mapping_list(values)
    for row in rows:
        if "stage" not in row and "agent" in row:
            row["stage"] = row.pop("agent")
    return rows


def _validate_required_modules(issues: list[dict[str, Any]], module_names: list[str]) -> None:
    required = [
        "user_profiling",
        "market_analysis",
        "context_building",
        "content_generation",
        "learning_loop",
    ]
    present = set(module_names)
    for module_name in required:
        if module_name not in present:
            issues.append(_issue(
                "missing_required_module",
                "module_names",
                f"DomainSnapshot is missing required module '{module_name}'.",
                module_name=module_name,
            ))


def _validate_required_capabilities(issues: list[dict[str, Any]], capability_names: list[str]) -> None:
    required = [
        "user_profiling",
        "market_analysis",
        "planning",
        "content_generation",
        "learning_loop",
    ]
    present = set(capability_names)
    for capability_name in required:
        if capability_name not in present:
            issues.append(_issue(
                "missing_required_capability",
                "capability_names",
                f"CapabilitySnapshot is missing required capability '{capability_name}'.",
                capability_name=capability_name,
            ))


def _validate_candidate_context(
    issues: list[dict[str, Any]],
    context_packs: list[ContextPack],
    candidate_sets: list[CandidateSet],
) -> None:
    context_task_ids = _context_task_ids(context_packs)
    for index, candidate_set in enumerate(candidate_sets):
        path = f"candidate_sets[{index}]"
        if candidate_set.task_id and candidate_set.task_id not in context_task_ids:
            issues.append(_issue(
                "candidate_set_without_context",
                path,
                f"CandidateSet task_id '{candidate_set.task_id}' has no matching ContextPack task_id.",
                task_id=candidate_set.task_id,
            ))
        candidate_ids = _candidate_ids(candidate_set.candidates)
        if candidate_set.selected_candidate_id and candidate_set.selected_candidate_id not in candidate_ids:
            issues.append(_issue(
                "selected_candidate_missing",
                path,
                f"selected_candidate_id '{candidate_set.selected_candidate_id}' is not present in candidates.",
                selected_candidate_id=candidate_set.selected_candidate_id,
            ))


def _context_task_ids(context_packs: list[ContextPack]) -> set[str]:
    task_ids = set()
    for pack in context_packs:
        task_id = str(pack.task_intent.get("task_id") or "").strip()
        if task_id:
            task_ids.add(task_id)
    return task_ids


def _candidate_ids(candidates: list[dict[str, Any]]) -> set[str]:
    ids = set()
    for candidate in candidates:
        candidate_id = str(candidate.get("id") or "").strip()
        if candidate_id:
            ids.add(candidate_id)
    return ids


def _issue(code: str, path: str, message: str, **metadata: Any) -> dict[str, Any]:
    return {
        "code": code,
        "path": path,
        "message": message,
        "severity": "error",
        "metadata": dict(metadata),
    }


def _float(value: Any) -> float:
    if isinstance(value, bool):
        return 0.0
    try:
        return float(value or 0.0)
    except (TypeError, ValueError):
        return 0.0


__all__ = [
    "AssetLibrary",
    "AssetRecord",
    "CandidateSet",
    "CapabilitySnapshot",
    "ClientBrief",
    "ContentCalendar",
    "ContextPack",
    "ContentTask",
    "DecisionPoint",
    "DomainSnapshot",
    "ExplanationTrace",
    "IntentContract",
    "KPIPlan",
    "LearningSignal",
    "MarketAnalysis",
    "OperationPlan",
    "PerformanceSnapshot",
    "UserAsset",
    "UserProfile",
]
