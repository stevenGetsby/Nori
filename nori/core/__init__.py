"""Shared contracts for Nori's domain architecture."""
from __future__ import annotations

from importlib import import_module
from typing import Any, Final


_LAZY_EXPORTS: Final[dict[str, str]] = {
    "AccountOperationProject": "project",
    "AgentBase": "agent",
    "ArtifactStore": "artifacts",
    "AssetLibrary": "models",
    "AssetRecord": "models",
    "CandidateSet": "models",
    "ChatCapabilityError": "contracts",
    "ChatJSONError": "contracts",
    "ChatResultError": "contracts",
    "ClientBrief": "models",
    "ContentCalendar": "models",
    "ContentTask": "models",
    "ContextPack": "models",
    "DOMAIN_MODULES": "architecture",
    "DecisionPoint": "models",
    "DomainModule": "architecture",
    "DomainSnapshot": "models",
    "ExplanationTrace": "models",
    "ImageCapabilityError": "contracts",
    "ImageResultError": "contracts",
    "IntentContract": "models",
    "IntentLLMResult": "contracts",
    "KPIPlan": "models",
    "LLMClientConfigError": "contracts",
    "LLMFactory": "llm",
    "LearningSignal": "models",
    "MarketAnalysis": "models",
    "ModelConfig": "contracts",
    "OperationPlan": "models",
    "PerformanceSnapshot": "models",
    "ProviderConfig": "contracts",
    "ResolvedModel": "contracts",
    "StructuredCallResult": "contracts",
    "StableArtifactAssembler": "artifacts",
    "StoredArtifact": "artifacts",
    "TargetSelectionResult": "contracts",
    "UserAsset": "models",
    "UserProfile": "models",
    "WorkflowBase": "workflow",
    "WorkflowStep": "workflow",
    "domain_module_names": "architecture",
    "get_domain_module": "architecture",
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
