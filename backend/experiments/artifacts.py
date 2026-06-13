"""Artifact catalog, resolution, reference traces, and zip exports."""
from __future__ import annotations

from .common import (
    Any,
    EXPERIMENT_MANIFEST_NAME,
    PROJECT_ROOT,
    Path,
    _case_id_from_run_dir,
    _content_case_dir,
    _content_run_dir,
    _exportable_input_files,
    _exportable_run_files,
    _file_sha256,
    _is_relative_to,
    _read_json,
    _safe_run_artifact_path,
    _slug,
    datetime,
    io,
    json,
    provider_fetchable_reference_url,
    zipfile,
)


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


def build_content_production_run_export(
    *,
    project_root: str | Path = PROJECT_ROOT,
    case_id: str,
    run_id: str,
    include_inputs: bool = False,
) -> dict[str, Any]:
    """Build a zip bundle for one recorded content-production run."""

    from .delivery import _run_review_evidence
    from .runs import summarize_content_production_run

    run_dir = _content_run_dir(project_root=project_root, case_id=case_id, run_id=run_id)
    summary = summarize_content_production_run(project_root=project_root, case_id=case_id, run_id=run_id)
    artifact_inspection = inspect_content_production_run_artifacts(
        project_root=project_root,
        case_id=case_id,
        run_id=run_id,
    )
    review_evidence = _run_review_evidence(summary=summary, inspection=artifact_inspection)
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

    from .cases import (
        content_production_experiment_report,
        list_content_production_cases,
    )
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

    from .delivery import _delivery_review_evidence, content_production_case_delivery
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
    review_evidence = _delivery_review_evidence(delivery=delivery, summary=summary)
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


def image_reference_summary(run_dir: str | Path, *, require_image_references: bool = False) -> dict[str, Any]:
    summary = image_reference_from_package(_read_json(Path(run_dir) / "content_package.json"))
    summary["required"] = bool(require_image_references)
    if require_image_references and summary.get("selected_count") and not summary.get("sent"):
        summary["status"] = "failed_required"
    return summary


def image_reference_from_package(package: dict[str, Any]) -> dict[str, Any]:
    cover_result = ((package.get("prompts") or {}).get("cover_result") or {})
    extra = cover_result.get("extra") or {}
    selected_paths = list(cover_result.get("reference_paths") or [])
    sent = bool(extra.get("reference_images_sent"))
    fallback = str(extra.get("reference_image_fallback") or "")
    status = "not_selected"
    if selected_paths and sent:
        status = "sent"
    elif selected_paths and fallback:
        status = "fallback"
    elif selected_paths:
        status = "selected_not_sent"
    return {
        "status": status,
        "required": False,
        "selected_count": len(selected_paths),
        "selected_paths": selected_paths,
        "sent": sent,
        "fallback": fallback,
        "uploaded": bool(extra.get("reference_images_uploaded")),
        "upload_count": int(extra.get("reference_upload_count") or 0),
        "object_keys": list(extra.get("reference_object_keys") or []),
        "public_urls": list(extra.get("reference_public_urls") or []),
        "trace": _image_reference_trace_from_cover_result(
            selected_paths=selected_paths,
            extra=extra,
            sent=sent,
        ),
    }


def _image_reference_trace_from_cover_result(
    *,
    selected_paths: list[Any],
    extra: dict[str, Any],
    sent: bool,
) -> list[dict[str, Any]]:
    """Build per-reference evidence from the cover package, compatible with old runs."""

    published_items = [item for item in extra.get("reference_items") or [] if isinstance(item, dict)]
    public_urls = [str(value) for value in extra.get("reference_public_urls") or [] if str(value or "").strip()]
    object_keys = [str(value) for value in extra.get("reference_object_keys") or [] if str(value or "").strip()]
    trace: list[dict[str, Any]] = []
    for index, raw_path in enumerate(selected_paths):
        selected_path = str(raw_path or "")
        item = _published_reference_for_path(selected_path, published_items, index=index)
        public_url = str(item.get("public_url") or item.get("url_public") or "")
        if not public_url and index < len(public_urls):
            public_url = public_urls[index]
        object_key = str(item.get("key") or "")
        if not object_key and index < len(object_keys):
            object_key = object_keys[index]
        model_input = str(item.get("url") or public_url or "")
        provider_fetchable_url = provider_fetchable_reference_url(public_url) or provider_fetchable_reference_url(selected_path)
        trace.append(
            {
                "index": index,
                "selected_path": selected_path,
                "public_url": public_url,
                "provider_fetchable_url": provider_fetchable_url,
                "provider_fetchable": bool(provider_fetchable_url),
                "object_key": object_key,
                "publish_reason": str(item.get("reason") or ""),
                "uploaded": bool(item.get("uploaded")) if item else False,
                "sent": bool(sent),
                "model_input_type": "url" if model_input.startswith(("http://", "https://")) else ("bytes" if sent else ""),
            }
        )
    return trace


def _published_reference_for_path(path: str, items: list[dict[str, Any]], *, index: int) -> dict[str, Any]:
    if index < len(items):
        return dict(items[index])
    for item in items:
        if str(item.get("original_path") or "") == path:
            return dict(item)
    return {}


def _image_reference_trace_with_transfer(
    image_reference: dict[str, Any],
    transfer: dict[str, Any],
) -> list[dict[str, Any]]:
    trace = [dict(item) for item in image_reference.get("trace") or [] if isinstance(item, dict)]
    transfer_items = [dict(item) for item in transfer.get("items") or [] if isinstance(item, dict)]
    if not trace:
        selected_count = int(image_reference.get("selected_count") or 0)
        required = bool(image_reference.get("required") or transfer.get("required"))
        if selected_count > 0 or required:
            trace = [
                _trace_from_transfer_item(item, index=index, sent=bool(image_reference.get("sent")))
                for index, item in enumerate(transfer_items)
            ]
    if not transfer_items:
        return trace
    return [_merge_trace_transfer_item(item, transfer_items) for item in trace]


def _trace_from_transfer_item(item: dict[str, Any], *, index: int, sent: bool) -> dict[str, Any]:
    provider_fetchable_url = str(item.get("provider_fetchable_url") or "")
    return {
        "index": index,
        "asset_id": str(item.get("asset_id") or ""),
        "filename": str(item.get("filename") or ""),
        "selected_path": str(item.get("path") or ""),
        "public_url": str(item.get("public_reference_url") or ""),
        "provider_fetchable_url": provider_fetchable_url,
        "provider_fetchable": bool(provider_fetchable_url or item.get("provider_fetchable")),
        "sent": sent,
    }


def _merge_trace_transfer_item(trace_item: dict[str, Any], transfer_items: list[dict[str, Any]]) -> dict[str, Any]:
    match = _match_transfer_item(trace_item, transfer_items)
    if not match:
        return trace_item
    merged = dict(trace_item)
    for key, value in {
        "asset_id": str(match.get("asset_id") or ""),
        "filename": str(match.get("filename") or ""),
        "input_path": str(match.get("path") or ""),
        "transfer_public_reference_url": str(match.get("public_reference_url") or ""),
        "transfer_provider_fetchable_url": str(match.get("provider_fetchable_url") or ""),
    }.items():
        if value:
            merged[key] = value
    if not merged.get("provider_fetchable_url") and match.get("provider_fetchable_url"):
        merged["provider_fetchable_url"] = str(match.get("provider_fetchable_url") or "")
    merged["provider_fetchable"] = bool(merged.get("provider_fetchable") or match.get("provider_fetchable"))
    return merged


def _match_transfer_item(trace_item: dict[str, Any], transfer_items: list[dict[str, Any]]) -> dict[str, Any]:
    candidates = {
        str(trace_item.get("selected_path") or ""),
        str(trace_item.get("public_url") or ""),
        str(trace_item.get("provider_fetchable_url") or ""),
    }
    for item in transfer_items:
        values = {
            str(item.get("path") or ""),
            str(item.get("public_reference_url") or ""),
            str(item.get("provider_fetchable_url") or ""),
        }
        if candidates.intersection(value for value in values if value):
            return item
    return {}


def _enrich_image_reference_trace(image_reference: dict[str, Any], transfer: dict[str, Any]) -> dict[str, Any]:
    enriched = dict(image_reference)
    trace = _image_reference_trace_with_transfer(enriched, transfer)
    if trace:
        enriched["trace"] = trace
        enriched["trace_count"] = len(trace)
        enriched["trace_provider_fetchable_count"] = sum(1 for item in trace if item.get("provider_fetchable"))
        enriched["trace_sent_count"] = sum(1 for item in trace if item.get("sent"))
    return enriched
