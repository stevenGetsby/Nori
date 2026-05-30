"""Registry for Nori's runtime capability modules."""
from __future__ import annotations

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


@dataclass(frozen=True, slots=True)
class DomainModule:
    """Deprecated alias shape for the previous five-module domain registry."""

    name: str
    package: str
    facade: str
    responsibility: str
    contracts: tuple[str, ...] = ()
    depends_on: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "package": self.package,
            "facade": self.facade,
            "responsibility": self.responsibility,
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
        responsibility="Generate note copy, cover images, and final content packages.",
        agents=("NoteMakerAgent", "CoverDirectorAgent", "ContentProducerAgent"),
        contracts=("NoteDraft", "CoverResult", "ContentPackage"),
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


DOMAIN_MODULES: tuple[DomainModule, ...] = (
    DomainModule(
        name="user_profiling",
        package="nori.user_profiling",
        facade="UserProfilingFacade",
        responsibility="Build long-lived user, account, brand, preference, and constraint profiles.",
        contracts=("UserProfile", "UserAsset"),
    ),
    DomainModule(
        name="market_analysis",
        package="nori.market_analysis",
        facade="MarketAnalysisFacade",
        responsibility="Normalize market, competitor, trend, and audience evidence.",
        contracts=("MarketAnalysis",),
    ),
    DomainModule(
        name="context_building",
        package="nori.context_building",
        facade="ContextPackBuilder",
        responsibility="Assemble profile, task, market, asset, decision, and evidence context for generation.",
        contracts=("ContextPack", "DecisionPoint", "ExplanationTrace"),
        depends_on=("user_profiling", "market_analysis"),
    ),
    DomainModule(
        name="content_generation",
        package="nori.content_generation",
        facade="ContentGenerationFacade",
        responsibility="Group generated outputs into candidate sets for review and selection.",
        contracts=("CandidateSet", "DecisionPoint", "ExplanationTrace"),
        depends_on=("context_building",),
    ),
    DomainModule(
        name="learning_loop",
        package="nori.learning_loop",
        facade="LearningLoopFacade",
        responsibility="Convert monitoring, review, and strategy evidence into learning signals.",
        contracts=("PerformanceSnapshot", "LearningSignal", "DomainSnapshot"),
        depends_on=("user_profiling", "market_analysis", "context_building", "content_generation"),
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


def domain_module_names() -> list[str]:
    """Return the legacy domain module order.

    New runtime code should use ``capability_module_names`` instead.
    """

    return [module.name for module in DOMAIN_MODULES]


def get_domain_module(name: str) -> DomainModule | None:
    """Look up a domain module by canonical name."""

    normalized = str(name or "").strip()
    for module in DOMAIN_MODULES:
        if module.name == normalized:
            return module
    return None


__all__ = [
    "CAPABILITY_MODULES",
    "DOMAIN_MODULES",
    "CapabilityModule",
    "DomainModule",
    "capability_module_names",
    "domain_module_names",
    "get_capability_module",
    "get_domain_module",
]
