"""AccountPlanner input normalization helpers."""
from __future__ import annotations

from pathlib import Path

from nori.user_profiling.models import AccountPlannerInput


def normalize_input(
    user_input: AccountPlannerInput | str,
    images: list[str] | None,
    links: list[str] | None,
) -> AccountPlannerInput:
    if isinstance(user_input, AccountPlannerInput):
        return AccountPlannerInput(
            text=user_input.text,
            images=[*user_input.images, *(images or [])],
            links=[*user_input.links, *(links or [])],
            intention=dict(user_input.intention),
            context=dict(user_input.context),
            platform=user_input.platform or "xhs",
            enable_search=user_input.enable_search,
            search_limit=user_input.search_limit,
        )
    return AccountPlannerInput(text=str(user_input or ""), images=list(images or []), links=list(links or []))


def asset_context(path: str) -> dict[str, str]:
    suffix = Path(path).suffix.lower().lstrip(".")
    return {"path": path, "kind": suffix or "image"}
