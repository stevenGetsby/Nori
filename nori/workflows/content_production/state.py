"""State contracts for the content production workflow."""
from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any, TypedDict

from data_collect.adapter import TopNotesResult
from nori.core import LLMFactory


TopNotesCollector = Callable[[Path], TopNotesResult]


class ContentProductionState(TypedDict, total=False):
    """Mutable state passed between content production stages."""

    run_dir: Path
    market_dir: Path
    covers_dir: Path
    llm_factory: LLMFactory
    brief_text: str
    asset_paths: list[Path]
    reference_public_urls_by_path: dict[str, str]
    top_notes_collector: TopNotesCollector
    _artifact_refs: dict[str, str]

    top_result: TopNotesResult
    market_report: Any
    intake: Any
    account_plan: Any
    client_brief: Any
    project: Any
    kpi_plan: Any
    calendar: Any
    task: Any
    content_context_pack: Any
    content_context_view: Any
    content_spec: Any
    package: Any
    reviews: list[Any]
