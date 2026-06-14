"""Artifact catalog, inspection, URLs, and resolution."""
from __future__ import annotations

from .common import (
    Any,
    EXPERIMENT_MANIFEST_NAME,
    PROJECT_ROOT,
    Path,
    _case_id_from_run_dir,
    _content_run_dir,
    _file_sha256,
    _is_relative_to,
    _read_json,
    _safe_run_artifact_path,
    datetime,
)
from .reference_images import _enrich_image_reference_trace, image_reference_from_package, image_reference_summary


def inspect_content_production_run_artifacts(
    *,
    project_root: str | Path = PROJECT_ROOT,
    case_id: str,
    run_id: str,
) -> dict[str, Any]:
    """Return a product-ready artifact inspection payload for one run."""

    from .runs import summarize_content_production_run

    summary = summarize_content_production_run(project_root=project_root, case_id=case_id, run_id=run_id)
    if not summary:
        raise FileNotFoundError(f"content-production run not found: {case_id}/{run_id}")
    run_dir = _content_run_dir(project_root=project_root, case_id=case_id, run_id=run_id)
    catalog = [dict(row) for row in summary.get("artifact_catalog") or [] if isinstance(row, dict)]
    catalog_by_name = {str(row.get("artifact_name") or ""): row for row in catalog}
    markdown = [
        _artifact_inspection_entry(run_dir, row)
        for row in catalog
        if str(row.get("artifact_name") or "").endswith(".md")
    ]
    covers = [
        _artifact_inspection_entry(run_dir, row)
        for row in catalog
        if str(row.get("artifact_type") or "") == "cover"
    ]
    manifest_names = [
        "input_manifest.json",
        EXPERIMENT_MANIFEST_NAME,
        "replay_request.json",
        "workflow_run.json",
        "run.json",
    ]
    manifests = {
        _artifact_panel_key(name): _artifact_inspection_entry(
            run_dir,
            catalog_by_name.get(name, {"artifact_name": name}),
        )
        for name in manifest_names
    }
    core = {
        "content_package": _artifact_inspection_entry(
            run_dir,
            catalog_by_name.get("content_package.json", {"artifact_name": "content_package.json"}),
        ),
        "input_manifest": manifests["input_manifest"],
        "experiment_manifest": manifests["experiment_manifest"],
        "replay_request": manifests["replay_request"],
        "cover_output": {
            "available": bool(covers),
            "count": len(covers),
            "items": covers,
        },
    }
    missing_core = [
        name
        for name, entry in core.items()
        if name != "cover_output" and not bool(entry.get("available"))
    ]
    if not covers:
        missing_core.append("cover_output")
    return {
        "schema_version": 1,
        "case_id": str(case_id),
        "run_id": str(run_id),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "status": str(summary.get("status") or ""),
        "workflow_name": str(summary.get("workflow_name") or ""),
        "created_at": str(summary.get("created_at") or ""),
        "finished_at": str(summary.get("finished_at") or ""),
        "ready_for_review": bool((summary.get("proof") or {}).get("ready_for_review")),
        "proof": dict(summary.get("proof") or {}),
        "acceptance": dict(summary.get("acceptance") or {}),
        "evaluations": dict(summary.get("evaluations") or {}),
        "image_reference": dict(summary.get("image_reference") or {}),
        "visual_reference_review": dict(summary.get("visual_reference_review") or {}),
        "core_artifacts": core,
        "content_package": core["content_package"],
        "manifests": manifests,
        "markdown": markdown,
        "covers": covers,
        "artifact_catalog": catalog,
        "artifact_counts": {
            "total": len(catalog),
            "json": sum(1 for row in catalog if str(row.get("artifact_name") or "").endswith(".json")),
            "markdown": len(markdown),
            "covers": len(covers),
        },
        "missing_core_artifacts": missing_core,
        "links": {
            "run": f"/workflows/content-production/runs/{case_id}/{run_id}",
            "export": _run_export_url(str(case_id), str(run_id)),
            "replay": _run_replay_url(str(case_id), str(run_id)),
            "acceptance": f"/workflows/content-production/runs/{case_id}/{run_id}/acceptance",
            "evaluations": f"/workflows/content-production/runs/{case_id}/{run_id}/evaluations",
            "evaluation_draft": f"/workflows/content-production/runs/{case_id}/{run_id}/evaluations/draft",
        },
    }


def artifact_urls_for_run(run_dir: str | Path, *, case_id: str = "", run_id: str = "") -> dict[str, str]:
    path = Path(run_dir)
    actual_case_id = case_id or _case_id_from_run_dir(path)
    actual_run_id = run_id or path.name
    return {
        item.name: f"/workflows/content-production/runs/{actual_case_id}/{actual_run_id}/artifacts/{item.name}"
        for item in sorted(path.iterdir())
        if item.is_file() and item.suffix.lower() in {".json", ".md"}
    } if path.is_dir() and actual_case_id and actual_run_id else {}


def cover_urls_for_run(run_dir: str | Path, *, case_id: str = "", run_id: str = "") -> list[str]:
    path = Path(run_dir)
    actual_case_id = case_id or _case_id_from_run_dir(path)
    actual_run_id = run_id or path.name
    covers_dir = path / "covers"
    return [
        f"/workflows/content-production/runs/{actual_case_id}/{actual_run_id}/artifacts/covers/{item.name}"
        for item in sorted(covers_dir.iterdir())
        if item.is_file() and item.suffix.lower() in {".jpeg", ".jpg", ".png", ".webp"}
    ] if covers_dir.is_dir() and actual_case_id and actual_run_id else []


def _run_export_url(case_id: str, run_id: str) -> str:
    return f"/workflows/content-production/runs/{case_id}/{run_id}/export" if case_id and run_id else ""


def _run_replay_url(case_id: str, run_id: str) -> str:
    return f"/workflows/content-production/runs/{case_id}/{run_id}/replay" if case_id and run_id else ""


def artifact_catalog_for_run(run_dir: str | Path, *, case_id: str = "", run_id: str = "") -> list[dict[str, Any]]:
    """Return whitelisted run artifact metadata for product detail UIs."""

    path = Path(run_dir)
    actual_case_id = case_id or _case_id_from_run_dir(path)
    actual_run_id = run_id or path.name
    if not path.is_dir() or not actual_case_id or not actual_run_id:
        return []

    rows: list[dict[str, Any]] = []
    for item in sorted(path.iterdir()):
        if item.is_file() and item.suffix.lower() in {".json", ".md"}:
            artifact_name = item.name
            rows.append(_artifact_catalog_entry(item, artifact_name=artifact_name, case_id=actual_case_id, run_id=actual_run_id))

    covers_dir = path / "covers"
    if covers_dir.is_dir():
        for item in sorted(covers_dir.iterdir()):
            if item.is_file() and item.suffix.lower() in {".jpeg", ".jpg", ".png", ".webp"}:
                artifact_name = f"covers/{item.name}"
                rows.append(
                    _artifact_catalog_entry(item, artifact_name=artifact_name, case_id=actual_case_id, run_id=actual_run_id)
                )
    return rows


def _artifact_catalog_entry(path: Path, *, artifact_name: str, case_id: str, run_id: str) -> dict[str, Any]:
    suffix = path.suffix.lower()
    artifact_type = "cover" if artifact_name.startswith("covers/") else "run_artifact"
    row = {
        "name": path.name,
        "artifact_name": artifact_name,
        "artifact_type": artifact_type,
        "media_type": _artifact_media_type(path),
        "size_bytes": path.stat().st_size,
        "sha256": _file_sha256(path),
        "url": f"/workflows/content-production/runs/{case_id}/{run_id}/artifacts/{artifact_name}",
    }
    if suffix in {".json", ".md"}:
        row["preview"] = _artifact_text_preview(path)
    else:
        row["preview"] = {"kind": "image", "available": False}
    return row


def _artifact_inspection_entry(run_dir: Path, row: dict[str, Any]) -> dict[str, Any]:
    artifact_name = str(row.get("artifact_name") or "")
    if not artifact_name:
        return {"available": False, "artifact_name": ""}
    path = _artifact_path_from_catalog_name(run_dir, artifact_name)
    if not path.is_file():
        return {
            "available": False,
            "artifact_name": artifact_name,
            "reason": "missing_artifact",
        }
    entry = {
        "available": True,
        **dict(row),
    }
    suffix = path.suffix.lower()
    if suffix == ".json":
        data = _read_json(path)
        entry["data"] = data
        entry["json_summary"] = {
            "keys": sorted(str(key) for key in data.keys()),
            "field_count": len(data),
        }
    elif suffix == ".md":
        entry["text"] = str((row.get("preview") or {}).get("text") or "")
    elif suffix in {".jpeg", ".jpg", ".png", ".webp"}:
        entry["preview"] = {"kind": "image", "available": True, "url": str(row.get("url") or "")}
    return entry


def _artifact_path_from_catalog_name(run_dir: Path, artifact_name: str) -> Path:
    name = str(artifact_name or "")
    if name.startswith("covers/"):
        return run_dir / "covers" / Path(name).name
    return run_dir / Path(name).name


def _artifact_panel_key(artifact_name: str) -> str:
    stem = Path(str(artifact_name or "")).stem
    return "experiment_manifest" if artifact_name == EXPERIMENT_MANIFEST_NAME else stem


def _artifact_media_type(path: Path) -> str:
    suffix = path.suffix.lower()
    return {
        ".json": "application/json",
        ".md": "text/markdown",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
    }.get(suffix, "application/octet-stream")


def _artifact_text_preview(path: Path, *, max_chars: int = 4096) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="replace")
    return {
        "kind": "text",
        "text": text[:max_chars],
        "char_count": len(text),
        "truncated": len(text) > max_chars,
    }


def resolve_content_production_artifact_path(
    *,
    project_root: str | Path = PROJECT_ROOT,
    case_id: str,
    run_id: str,
    artifact_name: str,
) -> Path:
    root = Path(project_root).resolve()
    run_dir = (root / "cases" / case_id / "runs" / run_id).resolve()
    if not _is_relative_to(run_dir, root / "cases") or not run_dir.is_dir():
        raise ValueError(f"content-production run not found: {case_id}/{run_id}")
    artifact = _safe_run_artifact_path(run_dir, artifact_name)
    if not artifact.is_file():
        raise FileNotFoundError(f"run artifact not found: {artifact_name}")
    return artifact


__all__ = [
    "_enrich_image_reference_trace",
    "_run_export_url",
    "_run_replay_url",
    "artifact_catalog_for_run",
    "artifact_urls_for_run",
    "cover_urls_for_run",
    "image_reference_from_package",
    "image_reference_summary",
    "inspect_content_production_run_artifacts",
    "resolve_content_production_artifact_path",
]
