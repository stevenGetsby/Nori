"""Shared contracts for Nori's capability and runtime architecture."""
from __future__ import annotations

from importlib import import_module
from typing import Any, Final


_LAZY_EXPORTS: Final[dict[str, str]] = {
    "AccountOperationProject": "project",
    "AgentBase": "agent",
    "AgentInputPreparer": "agent",
    "AgentPrompt": "agent",
    "AgentPromptBuilder": "agent",
    "ArtifactStore": "artifacts",
    "CAPABILITY_MODULES": "architecture",
    "AssetLibrary": "asset_models",
    "AssetRecord": "asset_models",
    "CandidateSet": "capability_models",
    "CapabilitySnapshot": "capability_models",
    "CapabilityModule": "architecture",
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
    "IntentLLMResult": "contracts",
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
    "StructuredCallResult": "contracts",
    "StableArtifactAssembler": "artifacts",
    "StoredArtifact": "artifacts",
    "TargetSelectionResult": "contracts",
    "UserAsset": "asset_models",
    "UserProfile": "profile_models",
    "WorkflowBase": "workflow",
    "WorkflowStep": "workflow",
    "capability_module_names": "architecture",
    "get_capability_module": "architecture",
    "named_workflow_steps": "workflow",
    "passthrough_step": "workflow",
}


def __getattr__(name: str) -> Any:
    if name == "contracts":
        module = import_module(f"{__name__}.contracts")
        globals()[name] = module
        return module
    module_name = _LAZY_EXPORTS.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module = import_module(f"{__name__}.{module_name}")
    value = getattr(module, name)
    globals()[name] = value
    return value


__all__ = [*_LAZY_EXPORTS, "contracts"]
