"""Data models for the Account Planner Agent."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .base import BenchmarkAccounts, Context, IPPortraitReport, Intention


@dataclass(slots=True)
class AccountPlannerInput:
    text: str = ""
    images: list[str] = field(default_factory=list)
    links: list[str] = field(default_factory=list)
    intention: Intention = field(default_factory=dict)
    context: Context = field(default_factory=dict)
    platform: str = "xhs"
    enable_search: bool = False
    search_limit: int = 5

    @classmethod
    def from_intaker(
        cls,
        intaker_result: Any,
        *,
        text: str = "",
        images: list[str] | None = None,
        links: list[str] | None = None,
        platform: str = "xhs",
        enable_search: bool = False,
        search_limit: int = 5,
    ) -> "AccountPlannerInput":
        data = intaker_result.to_dict() if hasattr(intaker_result, "to_dict") else dict(intaker_result or {})
        context = dict(getattr(intaker_result, "context", data.get("context", {})) or {})
        return cls(
            text=text,
            images=list(images if images is not None else _image_paths_from_context(context)),
            links=list(links or []),
            intention=dict(getattr(intaker_result, "intention", data.get("intention", {})) or {}),
            context=context,
            platform=platform,
            enable_search=enable_search,
            search_limit=search_limit,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "text": self.text,
            "images": list(self.images),
            "links": list(self.links),
            "intention": dict(self.intention),
            "context": dict(self.context),
            "platform": self.platform,
            "enable_search": self.enable_search,
            "search_limit": self.search_limit,
        }


@dataclass(slots=True)
class AccountPlanResult:
    tags: dict[str, str]
    recommended_positioning: str
    audience_profile: list[str]
    content_directions: list[str]
    benchmark_accounts: BenchmarkAccounts
    unique_selling_points: list[str]
    ip_portrait_report: IPPortraitReport

    def to_dict(self) -> dict[str, Any]:
        return {
            "tags": dict(self.tags),
            "recommended_positioning": self.recommended_positioning,
            "audience_profile": list(self.audience_profile),
            "content_directions": list(self.content_directions),
            "benchmark_accounts": dict(self.benchmark_accounts),
            "unique_selling_points": list(self.unique_selling_points),
            "ip_portrait_report": dict(self.ip_portrait_report),
        }


def _image_paths_from_context(context: Context) -> list[str]:
    images = context.get("images")
    if not isinstance(images, list):
        return []
    paths: list[str] = []
    for image in images:
        if isinstance(image, dict) and image.get("path"):
            paths.append(str(image["path"]))
        elif isinstance(image, str):
            paths.append(image)
    return paths


__all__ = ["AccountPlanResult", "AccountPlannerInput"]
