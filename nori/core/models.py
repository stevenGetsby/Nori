"""Compatibility facade for public core model contracts.

Concrete model ownership lives in the narrower ``*_models`` modules. Importing
from ``nori.core.models`` remains supported for callers that need the historical
single-module API.
"""
from __future__ import annotations

from nori.core.asset_models import AssetLibrary, AssetRecord, UserAsset
from nori.core.capability_models import (
    CandidateSet,
    CapabilitySnapshot,
    ContextPack,
    DecisionPoint,
    ExplanationTrace,
    LearningSignal,
    MarketAnalysis,
    PerformanceSnapshot,
)
from nori.core.planning_models import (
    ClientBrief,
    ContentCalendar,
    ContentTask,
    IntentContract,
    KPIPlan,
    OperationPlan,
)
from nori.core.profile_models import UserProfile


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
