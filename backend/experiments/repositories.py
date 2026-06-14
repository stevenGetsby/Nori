"""Filesystem repositories for backend experiment state."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from .common import (
    EXPERIMENT_EVALUATIONS_NAME,
    EXPERIMENT_SELECTION_NAME,
    PROJECT_ROOT,
    _content_case_dir,
    _content_run_dir,
    _read_json,
    _write_json,
)
from .models import ContentCaseRef, ContentRunRef


class ContentProductionExperimentRepository:
    """Repository boundary over the current JSON/filesystem experiment store."""

    def __init__(self, project_root: str | Path = PROJECT_ROOT) -> None:
        self.project_root = Path(project_root)

    def run_dir(self, ref: ContentRunRef) -> Path:
        return _content_run_dir(project_root=self.project_root, case_id=ref.case_id, run_id=ref.run_id)

    def case_dir(self, ref: ContentCaseRef) -> Path:
        return _content_case_dir(project_root=self.project_root, case_id=ref.case_id)

    def read_json(self, path: Path) -> dict[str, Any]:
        return _read_json(path)

    def write_json(self, path: Path, data: Any) -> None:
        _write_json(path, data)

    def read_evaluations(self, ref: ContentRunRef) -> list[dict[str, Any]]:
        data = self.read_json(self.run_dir(ref) / EXPERIMENT_EVALUATIONS_NAME)
        values = data.get("evaluations") if isinstance(data.get("evaluations"), list) else []
        return [dict(item) for item in values if isinstance(item, dict)]

    def write_evaluations(self, ref: ContentRunRef, evaluations: list[dict[str, Any]]) -> None:
        self.write_json(self.run_dir(ref) / EXPERIMENT_EVALUATIONS_NAME, {"evaluations": evaluations})

    def read_case_selection(self, ref: ContentCaseRef) -> dict[str, Any]:
        return self.read_json(self.case_dir(ref) / EXPERIMENT_SELECTION_NAME)

    def write_case_selection(self, ref: ContentCaseRef, payload: dict[str, Any]) -> None:
        self.write_json(self.case_dir(ref) / EXPERIMENT_SELECTION_NAME, payload)
