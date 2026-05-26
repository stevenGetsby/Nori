"""User profiling domain models."""
from __future__ import annotations

from typing import Any

from nori._compat import dataclass, field
from nori.core.contracts import (
    bool_value as _bool,
    dict_list as _dict_list,
    mapping as _mapping,
    mapping_list as _mapping_list,
    string_list as _string_list,
)
from nori.core import ClientBrief


Intention = dict[str, Any]
Context = dict[str, Any]
BenchmarkAccounts = dict[str, Any]
IPPortraitReport = dict[str, Any]


@dataclass(slots=True)
class UserInput:
    """Raw user text and optional image paths for the intake stage."""

    text: str
    images: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "text": self.text,
            "images": list(self.images),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "UserInput":
        data = _mapping(data)
        return cls(
            text=str(data.get("text") or ""),
            images=_string_list(data.get("images")),
        )


@dataclass(slots=True)
class IntakeResult:
    """Normalized user intention, context, and vision-tagged assets."""

    intention: Intention
    context: Context
    missing: list[str]
    questions: list[str]
    assets: list[Any] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def ready(self) -> bool:
        return not self.missing

    def to_dict(self) -> dict[str, Any]:
        data = {
            "intention": dict(self.intention),
            "context": dict(self.context),
            "ready": self.ready,
            "missing": list(self.missing),
            "questions": list(self.questions),
            "assets": [a.to_dict() if hasattr(a, "to_dict") else dict(a) for a in self.assets],
        }
        if self.metadata:
            data["metadata"] = dict(self.metadata)
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "IntakeResult":
        from nori.core import UserAsset

        data = _mapping(data)
        return cls(
            intention=_mapping(data.get("intention")),
            context=_mapping(data.get("context")),
            missing=_string_list(data.get("missing")),
            questions=_string_list(data.get("questions")),
            assets=[UserAsset.from_dict(item) for item in _mapping_list(data.get("assets"))],
            metadata=_mapping(data.get("metadata")),
        )


@dataclass(slots=True)
class AccountPlannerInput:
    """Normalized account-planning input produced after intake."""

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

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "AccountPlannerInput":
        data = _mapping(data)
        return cls(
            text=str(data.get("text") or ""),
            images=_string_list(data.get("images")),
            links=_string_list(data.get("links")),
            intention=_mapping(data.get("intention")),
            context=_mapping(data.get("context")),
            platform=str(data.get("platform") or "xhs"),
            enable_search=_bool(data.get("enable_search")),
            search_limit=_search_limit(data.get("search_limit")),
        )


@dataclass(slots=True)
class AccountPlanResult:
    """Account strategy and IP portrait result from account planning."""

    tags: dict[str, str]
    recommended_positioning: str
    audience_profile: list[str]
    content_directions: list[str]
    benchmark_accounts: BenchmarkAccounts
    unique_selling_points: list[str]
    ip_portrait_report: IPPortraitReport
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = {
            "tags": dict(self.tags),
            "recommended_positioning": self.recommended_positioning,
            "audience_profile": list(self.audience_profile),
            "content_directions": list(self.content_directions),
            "benchmark_accounts": dict(self.benchmark_accounts),
            "unique_selling_points": list(self.unique_selling_points),
            "ip_portrait_report": dict(self.ip_portrait_report),
        }
        if self.metadata:
            data["metadata"] = dict(self.metadata)
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "AccountPlanResult":
        data = _mapping(data)
        return cls(
            tags={str(key): str(value) for key, value in _mapping(data.get("tags")).items()},
            recommended_positioning=str(data.get("recommended_positioning") or ""),
            audience_profile=_string_list(data.get("audience_profile")),
            content_directions=_string_list(data.get("content_directions")),
            benchmark_accounts=_mapping(data.get("benchmark_accounts")),
            unique_selling_points=_string_list(data.get("unique_selling_points")),
            ip_portrait_report=_mapping(data.get("ip_portrait_report")),
            metadata=_mapping(data.get("metadata")),
        )


@dataclass(slots=True, eq=False)
class AccountPositioning:
    """Typed account positioning contract derived from account-planning output."""

    positioning_id: str = ""
    tags: dict[str, str] = field(default_factory=dict)
    recommended_positioning: str = ""
    audience_profile: list[str] = field(default_factory=list)
    content_directions: list[str] = field(default_factory=list)
    unique_selling_points: list[str] = field(default_factory=list)
    content_pillars: list[dict[str, Any]] = field(default_factory=list)
    account_keywords: list[str] = field(default_factory=list)
    cover_design_formats: list[dict[str, Any]] = field(default_factory=list)
    benchmark_refs: list[dict[str, Any]] = field(default_factory=list)
    benchmark_accounts: dict[str, Any] = field(default_factory=dict)
    ip_portrait_report: dict[str, Any] = field(default_factory=dict)
    source: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    extra_fields: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = dict(self.extra_fields)
        _put(data, "positioning_id", self.positioning_id)
        if self.tags:
            data["tags"] = dict(self.tags)
        _put(data, "recommended_positioning", self.recommended_positioning)
        _put(data, "audience_profile", list(self.audience_profile))
        _put(data, "content_directions", list(self.content_directions))
        _put(data, "unique_selling_points", list(self.unique_selling_points))
        _put(data, "content_pillars", _dict_list(self.content_pillars))
        _put(data, "account_keywords", list(self.account_keywords))
        _put(data, "cover_design_formats", _dict_list(self.cover_design_formats))
        _put(data, "benchmark_refs", _dict_list(self.benchmark_refs))
        if self.benchmark_accounts:
            data["benchmark_accounts"] = dict(self.benchmark_accounts)
        if self.ip_portrait_report:
            data["ip_portrait_report"] = dict(self.ip_portrait_report)
        _put(data, "source", self.source)
        if self.metadata:
            data["metadata"] = dict(self.metadata)
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "AccountPositioning":
        data = _mapping(data)
        known = {
            "positioning_id",
            "tags",
            "recommended_positioning",
            "audience_profile",
            "content_directions",
            "unique_selling_points",
            "content_pillars",
            "account_keywords",
            "cover_design_formats",
            "benchmark_refs",
            "benchmark_accounts",
            "ip_portrait_report",
            "source",
            "metadata",
            "extra_fields",
        }
        extra = {key: value for key, value in data.items() if key not in known}
        extra.update(_mapping(data.get("extra_fields")))
        return cls(
            positioning_id=str(data.get("positioning_id") or ""),
            tags={str(key): str(value) for key, value in _mapping(data.get("tags")).items()},
            recommended_positioning=str(data.get("recommended_positioning") or ""),
            audience_profile=_string_list(data.get("audience_profile")),
            content_directions=_string_list(data.get("content_directions")),
            unique_selling_points=_string_list(data.get("unique_selling_points")),
            content_pillars=_positioning_pillars(data.get("content_pillars")),
            account_keywords=_string_list(data.get("account_keywords")),
            cover_design_formats=_dict_list(data.get("cover_design_formats")),
            benchmark_refs=_dict_list(data.get("benchmark_refs")),
            benchmark_accounts=_mapping(data.get("benchmark_accounts")),
            ip_portrait_report=_mapping(data.get("ip_portrait_report")),
            source=str(data.get("source") or ""),
            metadata=_mapping(data.get("metadata")),
            extra_fields=extra,
        )

    @classmethod
    def from_account_plan(cls, account_plan: Any, *, positioning_id: str = "") -> "AccountPositioning":
        if account_plan is None:
            return cls(positioning_id=positioning_id)
        data = account_plan.to_dict() if hasattr(account_plan, "to_dict") else _mapping(account_plan)
        report = _mapping(data.get("ip_portrait_report"))
        benchmark_accounts = _mapping(data.get("benchmark_accounts"))
        return cls(
            positioning_id=positioning_id,
            tags={str(key): str(value) for key, value in _mapping(data.get("tags")).items()},
            recommended_positioning=str(data.get("recommended_positioning") or ""),
            audience_profile=_string_list(data.get("audience_profile")),
            content_directions=_string_list(data.get("content_directions")),
            unique_selling_points=_string_list(data.get("unique_selling_points")),
            content_pillars=_positioning_pillars(report.get("content_pillars")),
            account_keywords=_string_list(report.get("account_keywords")),
            cover_design_formats=_dict_list(report.get("cover_design_formats")),
            benchmark_refs=_benchmark_refs(benchmark_accounts),
            benchmark_accounts=benchmark_accounts,
            ip_portrait_report=report,
            source="account_plan",
        )

    def summary(self) -> str:
        return self.recommended_positioning or str(self.extra_fields.get("persona") or "")

    def keys(self) -> Any:
        return self.to_dict().keys()

    def items(self) -> Any:
        return self.to_dict().items()

    def values(self) -> Any:
        return self.to_dict().values()

    def get(self, key: str, default: Any = None) -> Any:
        return self.to_dict().get(key, default)

    def __getitem__(self, key: str) -> Any:
        return self.to_dict()[key]

    def __iter__(self) -> Any:
        return iter(self.to_dict().items())

    def __len__(self) -> int:
        return len(self.to_dict())

    def __bool__(self) -> bool:
        return bool(self.to_dict())

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, AccountPositioning):
            return self.to_dict() == other.to_dict()
        if isinstance(other, dict):
            return self.to_dict() == other
        return NotImplemented


def _put(data: dict[str, Any], key: str, value: Any) -> None:
    if value:
        data[key] = value


def _positioning_pillars(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    pillars: list[dict[str, Any]] = []
    for item in value:
        if isinstance(item, dict):
            pillars.append(dict(item))
        elif str(item).strip():
            pillars.append({"name": str(item).strip()})
    return pillars


def _benchmark_refs(value: dict[str, Any]) -> list[dict[str, Any]]:
    refs: list[dict[str, Any]] = []
    for keyword in _string_list(value.get("search_keywords"))[:5]:
        refs.append({"source": "benchmark_keyword", "keyword": keyword})
    for account in _mapping_list(value.get("accounts"))[:5]:
        refs.append({
            "source": "benchmark_account",
            "name": str(account.get("name") or account.get("author") or ""),
            "url": str(account.get("url") or ""),
        })
    for sample in _mapping_list(value.get("search_results"))[:5]:
        refs.append({
            "source": "benchmark_search_result",
            "title": str(sample.get("title") or ""),
            "url": str(sample.get("url") or ""),
            "keyword": str(sample.get("keyword") or ""),
        })
    return [ref for ref in refs if any(item for item in ref.values())]


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


def _search_limit(value: Any) -> int:
    if isinstance(value, bool):
        return 5
    try:
        return int(value)
    except (TypeError, ValueError):
        return 5


AccountPlannerInput.__module__ = __name__
AccountPlanResult.__module__ = __name__
IntakeResult.__module__ = __name__
UserInput.__module__ = __name__
AccountPositioning.__module__ = __name__

__all__ = [
    "AccountPlanResult",
    "AccountPlannerInput",
    "AccountPositioning",
    "BenchmarkAccounts",
    "ClientBrief",
    "Context",
    "IPPortraitReport",
    "IntakeResult",
    "Intention",
    "UserInput",
]
