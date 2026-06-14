"""Zip export bundles for content-production experiment artifacts."""
from __future__ import annotations

from .common import (
    Any,
    PROJECT_ROOT,
    Path,
    _content_case_dir,
    _content_run_dir,
    _exportable_input_files,
    _exportable_run_files,
    _file_sha256,
    _slug,
    datetime,
    io,
    json,
    zipfile,
)
from .artifacts import _artifact_media_type, _run_export_url, inspect_content_production_run_artifacts
from .delivery_payloads import delivery_review_evidence, run_review_evidence


def build_content_production_run_export(
    *,
    project_root: str | Path = PROJECT_ROOT,
    case_id: str,
    run_id: str,
    include_inputs: bool = False,
) -> dict[str, Any]:
    """Build a zip bundle for one recorded content-production run."""

    from .runs import summarize_content_production_run

    run_dir = _content_run_dir(project_root=project_root, case_id=case_id, run_id=run_id)
    summary = summarize_content_production_run(project_root=project_root, case_id=case_id, run_id=run_id)
    artifact_inspection = inspect_content_production_run_artifacts(
        project_root=project_root,
        case_id=case_id,
        run_id=run_id,
    )
    review_evidence = run_review_evidence(summary=summary, inspection=artifact_inspection)
    json_entries: dict[str, Any] = {
        "artifact_inspection.json": artifact_inspection,
        "review_evidence.json": review_evidence,
        "run_summary.json": summary,
    }
    entries = _exportable_run_files(run_dir)
    skipped_inputs: list[dict[str, str]] = []
    if include_inputs:
        input_entries, skipped_inputs = _exportable_input_files(run_dir)
        entries.extend(input_entries)
    manifest = {
        "schema_version": 1,
        "case_id": str(case_id),
        "run_id": str(run_id),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "include_inputs": bool(include_inputs),
        "files": [
            {
                "path": path,
                "media_type": "application/json",
                "size_bytes": len(json.dumps(data, ensure_ascii=False, default=str).encode("utf-8")),
            }
            for path, data in json_entries.items()
        ] + [
            {
                "path": arcname,
                "media_type": _artifact_media_type(path),
                "size_bytes": path.stat().st_size,
                "sha256": _file_sha256(path),
            }
            for arcname, path in entries
        ],
        "skipped_inputs": skipped_inputs,
    }
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("export_manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2))
        for path, data in json_entries.items():
            archive.writestr(path, json.dumps(data, ensure_ascii=False, indent=2, default=str))
        for arcname, path in entries:
            archive.write(path, arcname=arcname)
    return {
        "filename": f"nori_content_production_{_slug(str(case_id))}_{_slug(str(run_id))}.zip",
        "media_type": "application/zip",
        "content": buffer.getvalue(),
        "manifest": manifest,
    }


def build_content_production_case_export(
    *,
    project_root: str | Path = PROJECT_ROOT,
    case_id: str,
) -> dict[str, Any]:
    """Build a zip bundle for one recorded content-production case."""

    from .case_reports import content_production_experiment_report
    from .cases import list_content_production_cases
    from .runs import list_content_production_runs
    from .selections import get_content_production_case_selection

    _content_case_dir(project_root=project_root, case_id=case_id)
    report = content_production_experiment_report(project_root=project_root, case_id=case_id, limit=500)
    selection = get_content_production_case_selection(project_root=project_root, case_id=case_id)
    cases = list_content_production_cases(project_root=project_root)
    case_summary = next((row for row in cases.get("cases") or [] if row.get("case_id") == case_id), {})
    runs = list_content_production_runs(project_root=project_root, case_id=case_id, limit=500).get("runs", [])
    selected_run_id = str((selection.get("current") or {}).get("run_id") or "")
    entries: dict[str, Any] = {
        "case_report.json": report,
        "case_selection.json": {
            key: value
            for key, value in selection.items()
            if key != "report"
        },
        "case_summary.json": case_summary,
    }
    for summary in runs:
        run_id = str(summary.get("run_id") or "")
        if run_id:
            entries[f"runs/{_slug(run_id)}/summary.json"] = summary
    manifest = {
        "schema_version": 1,
        "case_id": str(case_id),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "run_count": len(runs),
        "selected_run_id": selected_run_id,
        "selected_run_export_url": _run_export_url(case_id, selected_run_id) if selected_run_id else "",
        "files": [
            {
                "path": path,
                "media_type": "application/json",
                "size_bytes": len(json.dumps(data, ensure_ascii=False, default=str).encode("utf-8")),
            }
            for path, data in entries.items()
        ],
    }
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("case_export_manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2, default=str))
        for path, data in entries.items():
            archive.writestr(path, json.dumps(data, ensure_ascii=False, indent=2, default=str))
    return {
        "filename": f"nori_content_production_case_{_slug(str(case_id))}.zip",
        "media_type": "application/zip",
        "content": buffer.getvalue(),
        "manifest": manifest,
    }


def build_content_production_case_delivery_export(
    *,
    project_root: str | Path = PROJECT_ROOT,
    case_id: str,
    allow_unready: bool = False,
) -> dict[str, Any]:
    """Build a delivery bundle for the run selected by the case delivery gate."""

    from .delivery import content_production_case_delivery
    from .runs import summarize_content_production_run

    delivery = content_production_case_delivery(
        project_root=project_root,
        case_id=case_id,
        allow_unpromoted=allow_unready,
    )
    run_id = str(delivery.get("run_id") or "")
    if not run_id:
        raise ValueError("case has no delivery run to export")
    if not bool(delivery.get("ready")) and not allow_unready:
        blockers = ", ".join(str(item) for item in delivery.get("blocking_reasons") or []) or "not_ready"
        raise ValueError(f"case delivery is not ready: {blockers}")

    normalized_case_id = str(delivery.get("case_id") or case_id)
    run_dir = _content_run_dir(project_root=project_root, case_id=normalized_case_id, run_id=run_id)
    summary = summarize_content_production_run(project_root=project_root, case_id=normalized_case_id, run_id=run_id)
    artifact_inspection = dict(delivery.get("artifact_inspection") or {})
    review_evidence = delivery_review_evidence(delivery=delivery, summary=summary)
    json_entries: dict[str, Any] = {
        "delivery.json": delivery,
        "artifact_inspection.json": artifact_inspection,
        "review_evidence.json": review_evidence,
        "case_compare.json": delivery.get("case_compare") or {},
        "next_actions.json": delivery.get("next_actions") or {},
        "run_summary.json": summary,
    }
    run_entries = [(f"run/{arcname}", path) for arcname, path in _exportable_run_files(run_dir)]
    generated_at = datetime.now().isoformat(timespec="seconds")
    manifest = {
        "schema_version": 1,
        "case_id": normalized_case_id,
        "run_id": run_id,
        "generated_at": generated_at,
        "ready": bool(delivery.get("ready")),
        "status": str(delivery.get("status") or ""),
        "allow_unready": bool(allow_unready),
        "blocking_reasons": list(delivery.get("blocking_reasons") or []),
        "warning_reasons": list(delivery.get("warning_reasons") or []),
        "files": [
            {
                "path": path,
                "media_type": "application/json",
                "size_bytes": len(json.dumps(data, ensure_ascii=False, default=str).encode("utf-8")),
            }
            for path, data in json_entries.items()
        ] + [
            {
                "path": arcname,
                "media_type": _artifact_media_type(path),
                "size_bytes": path.stat().st_size,
                "sha256": _file_sha256(path),
            }
            for arcname, path in run_entries
        ],
    }
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("delivery_export_manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2, default=str))
        for path, data in json_entries.items():
            archive.writestr(path, json.dumps(data, ensure_ascii=False, indent=2, default=str))
        for arcname, path in run_entries:
            archive.write(path, arcname=arcname)
    return {
        "filename": f"nori_content_production_delivery_{_slug(normalized_case_id)}_{_slug(run_id)}.zip",
        "media_type": "application/zip",
        "content": buffer.getvalue(),
        "manifest": manifest,
    }


__all__ = [
    "build_content_production_case_delivery_export",
    "build_content_production_case_export",
    "build_content_production_run_export",
]
