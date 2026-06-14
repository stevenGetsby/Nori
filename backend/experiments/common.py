"""Shared imports, constants, and low-level helpers for backend experiments."""
from __future__ import annotations

import json
import os
import hashlib
import importlib
import io
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

from data_collect.adapter import TopNotesResult
import nori.core.llms as llms
from nori.core import CaseWorkspace, ClientBrief, ContentTask, IntentContract, LLMFactory
from nori.core.paths import infer_project_root_from_cases_path, make_portable_paths
from nori.workflows.content_production import (
    ContentProductionConfig,
    ContentProductionWorkflow,
    record_content_production_artifacts,
    top_notes_result_from_dict,
)

from ..reference_urls import provider_fetchable_reference_url


PROJECT_ROOT = Path(__file__).resolve().parents[2]
EXPERIMENT_MANIFEST_NAME = "experiment_manifest.json"
EXPERIMENT_EVALUATIONS_NAME = "experiment_evaluations.json"
EXPERIMENT_SELECTION_NAME = "experiment_selection.json"
EVALUATION_STATUSES = {"passed", "needs_revision", "blocked", "pending"}
SELECTION_DECISIONS = {"selected", "promoted", "needs_revision", "rejected", "archived"}


def _first_stage_time(workflow_run: dict[str, Any]) -> str:
    stages = workflow_run.get("stages") if isinstance(workflow_run.get("stages"), list) else []
    for stage in stages:
        if isinstance(stage, dict) and stage.get("started_at"):
            return str(stage["started_at"])
    return str(workflow_run.get("started_at") or "")


def _read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def _content_run_dir(*, project_root: str | Path, case_id: str, run_id: str) -> Path:
    root = Path(project_root).resolve()
    run_dir = (root / "cases" / str(case_id or "") / "runs" / str(run_id or "")).resolve()
    if not _is_relative_to(run_dir, root / "cases") or not run_dir.is_dir():
        raise FileNotFoundError(f"content-production run not found: {case_id}/{run_id}")
    return run_dir


def _content_case_dir(*, project_root: str | Path, case_id: str) -> Path:
    normalized_case_id = str(case_id or "").strip()
    if not normalized_case_id:
        raise ValueError("case_id is required")
    root = Path(project_root).resolve()
    case_dir = (root / "cases" / normalized_case_id).resolve()
    if not _is_relative_to(case_dir, root / "cases") or not case_dir.is_dir():
        raise FileNotFoundError(f"content-production case not found: {normalized_case_id}")
    return case_dir


def _content_case_dir_or_none(*, project_root: str | Path, case_id: str) -> Path | None:
    normalized_case_id = str(case_id or "").strip()
    if not normalized_case_id:
        return None
    try:
        return _content_case_dir(project_root=project_root, case_id=normalized_case_id)
    except (FileNotFoundError, ValueError):
        return None


def _safe_run_artifact_path(run_dir: Path, artifact_name: str) -> Path:
    name = str(artifact_name or "").strip()
    if not name or name.startswith("/") or ".." in Path(name).parts:
        raise ValueError("invalid artifact name")
    parts = Path(name).parts
    if len(parts) == 1 and Path(name).suffix.lower() in {".json", ".md"}:
        return (run_dir / name).resolve()
    if len(parts) == 2 and parts[0] == "covers" and Path(parts[1]).suffix.lower() in {".jpeg", ".jpg", ".png", ".webp"}:
        return (run_dir / "covers" / parts[1]).resolve()
    raise ValueError("unsupported artifact name")


def _exportable_run_files(run_dir: Path) -> list[tuple[str, Path]]:
    entries: list[tuple[str, Path]] = []
    for path in sorted(run_dir.iterdir()):
        if path.is_file() and path.suffix.lower() in {".json", ".md"}:
            entries.append((path.name, path))
    covers_dir = run_dir / "covers"
    if covers_dir.is_dir():
        for path in sorted(covers_dir.iterdir()):
            if path.is_file() and path.suffix.lower() in {".jpeg", ".jpg", ".png", ".webp"}:
                entries.append((f"covers/{path.name}", path))
    return entries


def _exportable_input_files(run_dir: Path) -> tuple[list[tuple[str, Path]], list[dict[str, str]]]:
    manifest = _read_json(run_dir / "input_manifest.json")
    assets = manifest.get("assets") if isinstance(manifest.get("assets"), list) else []
    entries: list[tuple[str, Path]] = []
    skipped: list[dict[str, str]] = []
    seen: set[Path] = set()
    for index, asset in enumerate(assets, start=1):
        if not isinstance(asset, dict):
            continue
        source = Path(str(asset.get("path") or ""))
        reason = ""
        if not str(asset.get("path") or "").strip():
            reason = "missing_path"
        elif _is_remote_url(str(asset.get("path") or "")):
            reason = "remote_url"
        elif not source.is_file():
            reason = "missing_file"
        elif source.suffix.lower() not in {".jpeg", ".jpg", ".png", ".webp", ".gif"}:
            reason = "unsupported_input_type"
        elif source.resolve() in seen:
            reason = "duplicate"
        if reason:
            skipped.append({"asset_id": str(asset.get("asset_id") or ""), "path": str(asset.get("path") or ""), "reason": reason})
            continue
        seen.add(source.resolve())
        asset_id = _slug(str(asset.get("asset_id") or f"asset_{index}"))
        filename = _safe_export_filename(str(asset.get("filename") or source.name))
        entries.append((f"inputs/{asset_id}_{filename}", source))
    return entries, skipped


def _safe_export_filename(value: str) -> str:
    name = Path(str(value or "")).name
    clean = "".join(ch if ch.isalnum() or ch in {"-", "_", ".", "@"} else "_" for ch in name)
    return clean.strip("._") or "input_asset"


def _is_remote_url(value: str) -> bool:
    return str(value or "").startswith(("http://", "https://"))


def _case_id_from_run_dir(run_dir: Path) -> str:
    parts = run_dir.parts
    if len(parts) >= 3 and parts[-2] == "runs":
        return parts[-3]
    return ""


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent.resolve())
    except ValueError:
        return False
    return True


def _string_list(value: Any) -> list[str]:
    if isinstance(value, (list, tuple)):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value or "").strip()
    return [text] if text else []


def _dict_list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [dict(item) for item in value if isinstance(item, dict)]


def _dedupe_strings(values: list[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for value in values:
        text = str(value or "").strip()
        if text and text not in seen:
            seen.add(text)
            out.append(text)
    return out


def _slug(value: str) -> str:
    text = "".join(ch.lower() if ch.isalnum() else "_" for ch in value)
    return text[:48].strip("_") or "nori"


def _write_json(path: Path, data: Any, *, portable_root: str | Path | None = None) -> None:
    root = portable_root or infer_project_root_from_cases_path(path)
    payload = make_portable_paths(data, root)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str), encoding="utf-8")


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _json_sha256(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _reference_transfer_snapshot(
    asset_rows: list[dict[str, Any]],
    *,
    reference_public_urls_by_path: dict[str, str],
    require_image_references: bool,
) -> dict[str, Any]:
    items: list[dict[str, Any]] = []
    for row in asset_rows:
        path = str(row.get("path") or "")
        public_url = str(row.get("public_reference_url") or "").strip()
        provider_fetchable_url = provider_fetchable_reference_url(public_url)
        if not provider_fetchable_url:
            provider_fetchable_url = provider_fetchable_reference_url(path)
        if not provider_fetchable_url:
            provider_fetchable_url = provider_fetchable_reference_url(str(reference_public_urls_by_path.get(path) or ""))
        items.append(
            {
                "asset_id": str(row.get("asset_id") or ""),
                "filename": str(row.get("filename") or Path(path).name),
                "path": path,
                "public_reference_url": public_url,
                "provider_fetchable_url": provider_fetchable_url,
                "provider_fetchable": bool(provider_fetchable_url),
            }
        )
    provider_fetchable_count = sum(1 for item in items if item["provider_fetchable"])
    selected_count = len(items)
    return {
        "required": bool(require_image_references),
        "selected_count": selected_count,
        "local_count": sum(1 for row in asset_rows if not _is_remote_url(str(row.get("path") or ""))),
        "remote_count": sum(1 for row in asset_rows if _is_remote_url(str(row.get("path") or ""))),
        "provider_fetchable_count": provider_fetchable_count,
        "all_selected_fetchable": bool(selected_count) and provider_fetchable_count == selected_count,
        "strict_public_url_ready": (
            provider_fetchable_count == selected_count and selected_count > 0
        ) if require_image_references else True,
        "items": items,
    }
