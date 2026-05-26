"""Registry for Nori's shared layer and five domain modules."""
from __future__ import annotations

from nori._compat import dataclass


@dataclass(frozen=True, slots=True)
class DomainModule:
    """Stable metadata for one top-level domain module."""

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


def domain_module_names() -> list[str]:
    """Return the canonical module order used by orchestration and docs."""

    return [module.name for module in DOMAIN_MODULES]


def get_domain_module(name: str) -> DomainModule | None:
    """Look up a domain module by canonical name."""

    normalized = str(name or "").strip()
    for module in DOMAIN_MODULES:
        if module.name == normalized:
            return module
    return None


__all__ = [
    "DOMAIN_MODULES",
    "DomainModule",
    "domain_module_names",
    "get_domain_module",
]
