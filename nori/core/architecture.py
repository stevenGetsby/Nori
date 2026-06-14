"""Registry for Nori's runtime capability modules."""
from __future__ import annotations

from typing import Any

from nori._compat import dataclass


@dataclass(frozen=True, slots=True)
class CapabilityModule:
    """Stable metadata for one agent-owned business capability group."""

    name: str
    package: str
    responsibility: str
    agents: tuple[str, ...] = ()
    contracts: tuple[str, ...] = ()
    depends_on: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "package": self.package,
            "responsibility": self.responsibility,
            "agents": list(self.agents),
            "contracts": list(self.contracts),
            "depends_on": list(self.depends_on),
        }


CAPABILITY_MODULES: tuple[CapabilityModule, ...] = (
    CapabilityModule(
        name="user_profiling",
        package="nori.agents.user_profiling",
        responsibility="Understand user input, brand assets, account positioning, and audience assumptions.",
        agents=("IntakeAgent", "AccountPlannerAgent"),
        contracts=("UserInput", "IntakeResult", "AccountPlannerInput", "AccountPlanResult"),
    ),
    CapabilityModule(
        name="market_analysis",
        package="nori.agents.market_analysis",
        responsibility="Turn market evidence into reusable note skills and content references.",
        agents=("XHSNoteAnalyzer",),
        contracts=("NoteSkill", "SessionSkillReport"),
    ),
    CapabilityModule(
        name="planning",
        package="nori.agents.planning",
        responsibility="Build operation, KPI, and content-calendar plans from the current profile and task.",
        agents=("OperationPlannerAgent", "KPIPlannerAgent", "CalendarPlannerAgent"),
        contracts=("AccountOperationProject", "KPIPlan", "ContentCalendar", "ContentTask"),
        depends_on=("user_profiling", "market_analysis"),
    ),
    CapabilityModule(
        name="content_generation",
        package="nori.agents.content_generation",
        responsibility="Design reusable content specs, then instantiate them into generated packages.",
        agents=("ContentSpecAgent", "ArtifactGenerationAgent", "ContentProducerAgent", "NoteMakerAgent", "CoverDirectorAgent"),
        contracts=("ContentDesignSpec", "ContentPackage", "NoteDraft", "CoverResult"),
        depends_on=("planning", "market_analysis"),
    ),
    CapabilityModule(
        name="learning_loop",
        package="nori.agents.learning_loop",
        responsibility="Review generated content and convert outcomes into learning signals.",
        agents=("ReviewGateAgent", "StrategyIterationAgent"),
        contracts=("ComplianceReview", "MetricsSnapshot", "StrategyIteration"),
        depends_on=("content_generation",),
    ),
)


def capability_module_names() -> list[str]:
    """Return the canonical capability order used by runtime orchestration."""

    return [module.name for module in CAPABILITY_MODULES]


def get_capability_module(name: str) -> CapabilityModule | None:
    """Look up a capability module by canonical name."""

    normalized = str(name or "").strip()
    for module in CAPABILITY_MODULES:
        if module.name == normalized:
            return module
    return None


def capability_registry_snapshot() -> dict[str, Any]:
    """Return a JSON-serializable view of the agent-owned capability registry."""

    return {
        "module_names": capability_module_names(),
        "modules": [module.to_dict() for module in CAPABILITY_MODULES],
    }


__all__ = [
    "CAPABILITY_MODULES",
    "CapabilityModule",
    "capability_module_names",
    "capability_registry_snapshot",
    "get_capability_module",
]
