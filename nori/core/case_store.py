"""Case-centric artifact workspace helpers."""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from nori._compat import dataclass


CASE_SCHEMA_VERSION = 1


@dataclass(slots=True)
class CaseWorkspace:
    """Human-readable case workspace plus machine-readable artifact index.

    The case directory owns briefs, assets, runs, outputs, and showcase files.
    The shared ``data/artifact_index`` directory keeps cross-case JSONL indexes
    that scripts and future workbench surfaces can scan without walking files.
    """

    root: str | Path
    case_id: str
    title: str = ""

    def __post_init__(self) -> None:
        self.root = Path(self.root)
        self.case_id = str(self.case_id).strip()
        if not self.case_id:
            raise ValueError("case_id is required")
        if not self.title:
            self.title = self.case_id

    @property
    def case_dir(self) -> Path:
        return self.root / "cases" / self.case_id

    @property
    def brief_dir(self) -> Path:
        return self.case_dir / "brief"

    @property
    def assets_dir(self) -> Path:
        return self.case_dir / "assets"

    @property
    def raw_assets_dir(self) -> Path:
        return self.assets_dir / "raw"

    @property
    def selected_assets_dir(self) -> Path:
        return self.assets_dir / "selected"

    @property
    def public_refs_dir(self) -> Path:
        return self.assets_dir / "public_refs"

    @property
    def runs_dir(self) -> Path:
        return self.case_dir / "runs"

    @property
    def outputs_dir(self) -> Path:
        return self.case_dir / "outputs"

    @property
    def showcase_dir(self) -> Path:
        return self.case_dir / "showcase"

    @property
    def artifact_index_dir(self) -> Path:
        return self.root / "data" / "artifact_index"

    @property
    def case_manifest_path(self) -> Path:
        return self.case_dir / "case.json"

    def ensure(self) -> "CaseWorkspace":
        for path in (
            self.brief_dir,
            self.raw_assets_dir,
            self.selected_assets_dir,
            self.public_refs_dir,
            self.runs_dir,
            self.outputs_dir,
            self.showcase_dir,
            self.artifact_index_dir,
        ):
            path.mkdir(parents=True, exist_ok=True)
        self.case_manifest_path.write_text(
            json.dumps(self.case_manifest(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        self._upsert_index_row("cases.jsonl", "case_id", self.case_index_row())
        return self

    def case_manifest(self) -> dict[str, Any]:
        return {
            "schema_version": CASE_SCHEMA_VERSION,
            "case_id": self.case_id,
            "title": self.title,
            "directories": {
                "brief": "brief",
                "assets": "assets",
                "raw_assets": "assets/raw",
                "selected_assets": "assets/selected",
                "public_refs": "assets/public_refs",
                "runs": "runs",
                "outputs": "outputs",
                "showcase": "showcase",
            },
            "artifact_index": _relative_path(self.artifact_index_dir, self.root),
        }

    def case_index_row(self) -> dict[str, Any]:
        return {
            "schema_version": CASE_SCHEMA_VERSION,
            "case_id": self.case_id,
            "title": self.title,
            "path": _relative_path(self.case_dir, self.root),
            "manifest_path": _relative_path(self.case_manifest_path, self.root),
        }

    def create_run_dir(
        self,
        workflow: str,
        *,
        at: datetime | None = None,
        run_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Path:
        self.ensure()
        actual_run_id = run_id or f"{(at or datetime.now()).strftime('%Y%m%d_%H%M%S')}_{_slug(workflow)}"
        run_dir = self.runs_dir / actual_run_id
        run_dir.mkdir(parents=True, exist_ok=False)
        (run_dir / "artifacts").mkdir(parents=True, exist_ok=True)
        row = {
            "schema_version": CASE_SCHEMA_VERSION,
            "case_id": self.case_id,
            "run_id": actual_run_id,
            "workflow": workflow,
            "path": _relative_path(run_dir, self.root),
            "status": "created",
            "metadata": dict(metadata or {}),
        }
        self._write_run_manifest(run_dir, row)
        self._upsert_index_row("runs.jsonl", "run_id", row)
        return run_dir

    def record_run(
        self,
        run_dir: str | Path,
        *,
        workflow: str,
        status: str = "created",
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        self.ensure()
        path = Path(run_dir)
        path.mkdir(parents=True, exist_ok=True)
        row = {
            "schema_version": CASE_SCHEMA_VERSION,
            "case_id": self.case_id,
            "run_id": path.name,
            "workflow": workflow,
            "path": _relative_path(path, self.root),
            "status": status,
            "metadata": dict(metadata or {}),
        }
        self._write_run_manifest(path, row)
        self._upsert_index_row("runs.jsonl", "run_id", row)
        return row

    def record_artifact(
        self,
        *,
        run_id: str,
        artifact_type: str,
        path: str | Path,
        created_by: str,
        input_artifacts: list[str] | None = None,
        status: str = "created",
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        self.ensure()
        artifact_path = Path(path)
        artifact_path.parent.mkdir(parents=True, exist_ok=True)
        row = {
            "schema_version": CASE_SCHEMA_VERSION,
            "artifact_id": f"{self.case_id}:{run_id}:{artifact_type}",
            "case_id": self.case_id,
            "run_id": run_id,
            "type": artifact_type,
            "path": _relative_path(artifact_path, self.root),
            "created_by": created_by,
            "input_artifacts": list(input_artifacts or []),
            "status": status,
            "metadata": dict(metadata or {}),
        }
        self._upsert_index_row("artifacts.jsonl", "artifact_id", row)
        self._upsert_run_artifact(run_id, row)
        return row

    def _write_run_manifest(self, run_dir: Path, row: dict[str, Any]) -> None:
        manifest_path = run_dir / "run.json"
        manifest = _read_json(manifest_path, default={})
        artifacts = manifest.get("artifacts") if isinstance(manifest.get("artifacts"), list) else []
        manifest = {**row, "artifacts": artifacts}
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    def _upsert_run_artifact(self, run_id: str, row: dict[str, Any]) -> None:
        run_dir = self.runs_dir / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        manifest_path = run_dir / "run.json"
        manifest = _read_json(manifest_path, default={})
        if not manifest:
            manifest = {
                "schema_version": CASE_SCHEMA_VERSION,
                "case_id": self.case_id,
                "run_id": run_id,
                "workflow": "source",
                "path": _relative_path(run_dir, self.root),
                "status": "created",
                "metadata": {},
            }
        artifacts = manifest.get("artifacts") if isinstance(manifest.get("artifacts"), list) else []
        rows = _upsert_rows(artifacts, "artifact_id", row)
        manifest["artifacts"] = rows
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    def _upsert_index_row(self, filename: str, key: str, row: dict[str, Any]) -> None:
        path = self.artifact_index_dir / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        rows = _read_jsonl(path)
        rows = _upsert_rows(rows, key, row)
        _write_jsonl(path, rows)


def _slug(value: str) -> str:
    text = re.sub(r"[^\w\-]+", "_", str(value or "").strip())
    return text[:80].strip("_") or "run"


def _relative_path(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def _read_json(path: Path, *, default: Any) -> Any:
    if not path.is_file():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        data = json.loads(line)
        if isinstance(data, dict):
            rows.append(data)
    return rows


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    text = "\n".join(json.dumps(row, ensure_ascii=False, default=str) for row in rows)
    path.write_text(f"{text}\n" if text else "", encoding="utf-8")


def _upsert_rows(rows: list[dict[str, Any]], key: str, row: dict[str, Any]) -> list[dict[str, Any]]:
    out = [existing for existing in rows if existing.get(key) != row.get(key)]
    out.append(row)
    return out


__all__ = ["CaseWorkspace"]
