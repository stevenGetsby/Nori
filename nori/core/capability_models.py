"""Capability-level evidence, decision, and learning contracts."""
from __future__ import annotations

from typing import Any

from nori._compat import dataclass, field
from nori.core.contracts import mapping as _mapping
from nori.core.contracts import mapping_list as _mapping_list
from nori.core.contracts import string_list as _string_list
from nori.core.model_helpers import dict_rows as _dict_rows
from nori.core.model_helpers import float_value as _float
from nori.core.model_helpers import stage_rows as _stage_rows
from nori.core.profile_models import UserProfile


@dataclass(slots=True)
class MarketAnalysis:
    """Market and competitor evidence snapshot consumed by context assembly."""

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
    context_slices: list[dict[str, Any]] = field(default_factory=list)
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
            "context_slices": _dict_rows(self.context_slices),
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
            context_slices=_mapping_list(data.get("context_slices")),
            market_analysis=MarketAnalysis.from_dict(data.get("market_analysis")),
            assets=_mapping_list(data.get("assets")),
            constraints=_string_list(data.get("constraints")),
            evidence_refs=_mapping_list(data.get("evidence_refs")),
            decision_points=[DecisionPoint.from_dict(item) for item in _mapping_list(data.get("decision_points"))],
            explanation_trace=ExplanationTrace.from_dict(data.get("explanation_trace")),
            metadata=_mapping(data.get("metadata")),
        )

    def context_slices_by_kind(self, kind: str) -> list[Any]:
        from nori.context.schemas import ContextSlice

        return [
            ContextSlice.from_dict(item)
            for item in self.context_slices
            if str(item.get("kind") or "") == kind
        ]


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


__all__ = [
    "CandidateSet",
    "CapabilitySnapshot",
    "ContextPack",
    "DecisionPoint",
    "ExplanationTrace",
    "LearningSignal",
    "MarketAnalysis",
    "PerformanceSnapshot",
]
