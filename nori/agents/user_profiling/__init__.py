"""User/account/brand profiling module."""
from __future__ import annotations

from nori.core import ClientBrief, UserProfile
from nori.core.lazy_exports import lazy_export

from .schemas import AccountPositioning
from .schemas import AccountPlannerInput, AccountPlanResult, IntakeResult, UserInput

_LAZY_EXPORTS = {
    "AccountPlannerAgent": "account_planner",
    "account_plan": "account_planner",
    "IntakeAgent": "intaker",
    "intake": "intaker",
    "UserProfilingFacade": "facade",
}

__all__ = [
    "AccountPlannerAgent",
    "AccountPlannerInput",
    "AccountPlanResult",
    "AccountPositioning",
    "ClientBrief",
    "IntakeAgent",
    "IntakeResult",
    "UserInput",
    "UserProfile",
    "UserProfilingFacade",
    "account_plan",
    "intake",
]


def __getattr__(name: str):
    return lazy_export(__name__, _LAZY_EXPORTS, name)
