"""Shared contracts for Nori's capability and runtime architecture."""
from __future__ import annotations

from typing import Any, Final

from nori.core.lazy_exports import lazy_export


_LAZY_EXPORTS: Final[dict[str, str | None]] = {
    "AccountOperationProject": "project",
    "AgentBase": "agent",
    "AgentInputPreparer": "agent",
    "AgentPrompt": "agent",
    "AgentPromptBuilder": "agent",
    "ArtifactStore": "artifacts",
    "CAPABILITY_MODULES": "architecture",
    "AssetLibrary": "asset_models",
    "AssetRecord": "asset_models",
    "CaseWorkspace": "case_store",
    "CandidateSet": "capability_models",
    "CapabilitySnapshot": "capability_models",
    "CapabilityModule": "architecture",
    "capability_registry_snapshot": "architecture",
    "ChatCapabilityError": "contracts",
    "ChatJSONError": "contracts",
    "ChatResultError": "contracts",
    "ClientBrief": "planning_models",
    "ContentCalendar": "planning_models",
    "ContentTask": "planning_models",
    "ContextPack": "capability_models",
    "DecisionPoint": "capability_models",
    "ExplanationTrace": "capability_models",
    "ImageCapabilityError": "contracts",
    "ImageResultError": "contracts",
    "IntentContract": "planning_models",
    "KPIPlan": "planning_models",
    "LLMClientConfigError": "contracts",
    "LLMFactory": "llm",
    "LearningSignal": "capability_models",
    "MarketAnalysis": "capability_models",
    "ModelConfig": "contracts",
    "OperationPlan": "planning_models",
    "PerformanceSnapshot": "capability_models",
    "ProviderConfig": "contracts",
    "ResolvedModel": "contracts",
    "StableArtifactAssembler": "artifacts",
    "StoredArtifact": "artifacts",
    "UserAsset": "asset_models",
    "UserProfile": "profile_models",
    "WorkflowBase": "workflow",
    "WorkflowStep": "workflow",
    "capability_module_names": "architecture",
    "contracts": None,
    "get_capability_module": "architecture",
    "named_workflow_steps": "workflow",
    "passthrough_step": "workflow",
}


def __getattr__(name: str) -> Any:
    value = lazy_export(__name__, _LAZY_EXPORTS, name)
    globals()[name] = value
    return value


__all__ = [*_LAZY_EXPORTS]
