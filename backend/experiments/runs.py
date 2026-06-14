"""Run listing, summaries, comparisons, and run-level helpers."""
from __future__ import annotations

from .common import (
    Any,
    EXPERIMENT_MANIFEST_NAME,
    PROJECT_ROOT,
    Path,
    _dedupe_strings,
    _first_stage_time,
    _read_json,
    _string_list,
    json,
)
from .artifacts import artifact_catalog_for_run, artifact_urls_for_run, cover_urls_for_run
from .reference_images import _enrich_image_reference_trace, image_reference_from_package
from .acceptance import (
    content_production_summary_reference_transfer,
    content_production_run_acceptance_report,
    content_production_run_proof,
)
from .reviews import (
    _read_evaluations,
    evaluation_summary,
)
from .visual_reviews import visual_reference_review


def list_content_production_runs(
    *,
    project_root: str | Path = PROJECT_ROOT,
    case_id: str = "",
    status: str = "",
    proof_status: str = "",
    reference_status: str = "",
    evaluation_status: str = "",
    search: str = "",
    limit: int = 100,
    offset: int = 0,
) -> dict[str, Any]:
    root = Path(project_root)
    case_dirs = [root / "cases" / case_id] if case_id else sorted((root / "cases").glob("*"))
    all_runs: list[dict[str, Any]] = []
    for case_dir in case_dirs:
        runs_dir = case_dir / "runs"
        if not runs_dir.is_dir():
            continue
        for run_dir in sorted((path for path in runs_dir.iterdir() if path.is_dir()), reverse=True):
            summary = summarize_content_production_run(project_root=root, case_id=case_dir.name, run_id=run_dir.name)
            if summary:
                all_runs.append(summary)
    filters = {
        "case_id": str(case_id or ""),
        "status": str(status or ""),
        "proof_status": str(proof_status or ""),
        "reference_status": str(reference_status or ""),
        "evaluation_status": str(evaluation_status or ""),
        "search": str(search or ""),
    }
    filtered = [
        summary
        for summary in all_runs
        if _run_matches_filters(
            summary,
            status=filters["status"],
            proof_status=filters["proof_status"],
            reference_status=filters["reference_status"],
            evaluation_status=filters["evaluation_status"],
            search=filters["search"],
        )
    ]
    normalized_offset = max(0, int(offset or 0))
    normalized_limit = max(1, min(int(limit or 100), 500))
    paged = filtered[normalized_offset : normalized_offset + normalized_limit]
    rows = [content_production_comparison_run(summary) for summary in filtered]
    return {
        "runs": paged,
        "total_count": len(all_runs),
        "filtered_count": len(filtered),
        "returned_count": len(paged),
        "offset": normalized_offset,
        "limit": normalized_limit,
        "has_more": normalized_offset + normalized_limit < len(filtered),
        "filters": filters,
        "summary": {
            "status_counts": content_production_count_by(rows, "status"),
            "proof_status_counts": content_production_count_values([str((summary.get("proof") or {}).get("status") or "") for summary in filtered]),
            "acceptance_status_counts": content_production_count_values(
                [str((summary.get("acceptance") or {}).get("status") or "") for summary in filtered]
            ),
            "reference_status_counts": content_production_count_by(rows, "reference_status"),
            "evaluation_status_counts": content_production_count_by(rows, "evaluation_status"),
            "ready_count": sum(1 for row in rows if row["candidate"]["ready_for_review"]),
            "blocked_count": sum(1 for row in rows if not row["candidate"]["ready_for_review"]),
        },
    }


def compare_content_production_runs(
    *,
    project_root: str | Path = PROJECT_ROOT,
    case_id: str,
    run_ids: list[str],
) -> dict[str, Any]:
    """Compare recorded content-production runs within one case workspace."""

    normalized_case_id = str(case_id or "").strip()
    if not normalized_case_id:
        raise ValueError("case_id is required")
    normalized_run_ids = _dedupe_strings(run_ids)
    if len(normalized_run_ids) < 2:
        raise ValueError("at least two run_ids are required")

    summaries: list[dict[str, Any]] = []
    missing: list[str] = []
    for run_id in normalized_run_ids:
        summary = summarize_content_production_run(
            project_root=project_root,
            case_id=normalized_case_id,
            run_id=run_id,
        )
        if summary:
            summaries.append(summary)
        else:
            missing.append(run_id)
    if missing:
        raise FileNotFoundError(f"content-production runs not found: {normalized_case_id}/{missing}")

    rows = [content_production_comparison_run(summary) for summary in summaries]
    return {
        "case_id": normalized_case_id,
        "run_ids": normalized_run_ids,
        "run_count": len(rows),
        "runs": rows,
        "summary": {
            "status_counts": content_production_count_by(rows, "status"),
            "acceptance_status_counts": content_production_count_by(rows, "acceptance_status"),
            "reference_status_counts": content_production_count_by(rows, "reference_status"),
            "ready_run_ids": [row["run_id"] for row in rows if row["candidate"]["ready_for_review"]],
            "blocked_run_ids": [row["run_id"] for row in rows if not row["candidate"]["ready_for_review"]],
            "artifact_names": sorted({name for row in rows for name in row["artifact_names"]}),
            "evaluation_status_counts": content_production_count_by(rows, "evaluation_status"),
        },
        "differences": {
            "brief_sha256": _value_diff(rows, "brief_sha256"),
            "asset_fingerprints": _value_diff(rows, "asset_fingerprints"),
            "input_fingerprints": _value_diff(rows, "input_fingerprints"),
            "market_queries": _value_diff(rows, "market_queries"),
            "run_options": _value_diff(rows, "run_options"),
            "image_model": _value_diff(rows, "image_model"),
            "artifact_names": _value_diff(rows, "artifact_names"),
            "evaluation_status": _value_diff(rows, "evaluation_status"),
        },
    }


def summarize_content_production_run(
    *,
    project_root: str | Path = PROJECT_ROOT,
    case_id: str,
    run_id: str,
) -> dict[str, Any]:
    root = Path(project_root)
    run_dir = root / "cases" / case_id / "runs" / run_id
    if not run_dir.is_dir():
        return {}
    run_manifest = _read_json(run_dir / "run.json")
    workflow_run = _read_json(run_dir / "workflow_run.json")
    input_manifest = _read_json(run_dir / "input_manifest.json")
    experiment_manifest = _read_json(run_dir / EXPERIMENT_MANIFEST_NAME)
    evaluations = _read_evaluations(run_dir)
    manifest_evaluations = experiment_manifest.get("evaluations") if isinstance(experiment_manifest.get("evaluations"), dict) else {}
    if not evaluations and isinstance(manifest_evaluations.get("items"), list):
        evaluations = [dict(item) for item in manifest_evaluations["items"] if isinstance(item, dict)]
    evaluation_summary_data = (
        dict(manifest_evaluations.get("summary") or {})
        if not evaluations and isinstance(manifest_evaluations.get("summary"), dict)
        else evaluation_summary(evaluations)
    )
    package = _read_json(run_dir / "content_package.json")
    covers_dir = run_dir / "covers"
    cover_paths = [
        str(path)
        for path in sorted(covers_dir.iterdir())
        if path.is_file() and path.suffix.lower() in {".jpeg", ".jpg", ".png", ".webp"}
    ] if covers_dir.is_dir() else []
    summary = {
        "case_id": case_id,
        "run_id": run_id,
        "run_dir": str(run_dir),
        "workflow_name": run_manifest.get("workflow") or workflow_run.get("workflow_name") or "",
        "status": run_manifest.get("status") or workflow_run.get("status") or "",
        "created_at": _first_stage_time(workflow_run),
        "finished_at": workflow_run.get("finished_at", ""),
        "artifact_paths": {
            path.name: str(path)
            for path in sorted(run_dir.iterdir())
            if path.is_file() and path.suffix.lower() in {".json", ".md"}
        },
        "cover_paths": cover_paths,
        "artifact_urls": artifact_urls_for_run(run_dir, case_id=case_id, run_id=run_id),
        "cover_urls": cover_urls_for_run(run_dir, case_id=case_id, run_id=run_id),
        "artifact_catalog": artifact_catalog_for_run(run_dir, case_id=case_id, run_id=run_id),
        "input_manifest": input_manifest,
        "experiment_manifest": experiment_manifest,
        "evaluations": {
            "items": evaluations,
            "summary": evaluation_summary_data,
        },
        "image_reference": (
            dict(experiment_manifest.get("reference_images") or {})
            if experiment_manifest
            else image_reference_from_package(package)
        ),
        "workflow_run": workflow_run,
    }
    summary["image_reference"] = _enrich_image_reference_trace(
        summary.get("image_reference") if isinstance(summary.get("image_reference"), dict) else {},
        content_production_summary_reference_transfer(summary),
    )
    summary["proof"] = content_production_run_proof(summary)
    summary["proof_status"] = str(summary["proof"].get("status") or "")
    summary["proof_failed_checks"] = list(summary["proof"].get("failed_checks") or [])
    summary["proof_warning_checks"] = list(summary["proof"].get("warning_checks") or [])
    summary["acceptance"] = content_production_run_acceptance_report(summary)
    summary["acceptance_status"] = str(summary["acceptance"].get("status") or "")
    summary["acceptance_blocking_checks"] = list(summary["acceptance"].get("blocking_checks") or [])
    summary["acceptance_warning_checks"] = list(summary["acceptance"].get("warning_checks") or [])
    summary["visual_reference_review"] = visual_reference_review(summary)
    return summary


def content_production_comparison_run(summary: dict[str, Any]) -> dict[str, Any]:
    manifest = summary.get("experiment_manifest") if isinstance(summary.get("experiment_manifest"), dict) else {}
    inputs = manifest.get("inputs") if isinstance(manifest.get("inputs"), dict) else {}
    input_manifest = summary.get("input_manifest") if isinstance(summary.get("input_manifest"), dict) else {}
    reference = summary.get("image_reference") if isinstance(summary.get("image_reference"), dict) else {}
    evaluations = summary.get("evaluations") if isinstance(summary.get("evaluations"), dict) else {}
    evaluation = evaluations.get("summary") if isinstance(evaluations.get("summary"), dict) else {}
    acceptance = summary.get("acceptance") if isinstance(summary.get("acceptance"), dict) else {}
    artifacts = sorted((summary.get("artifact_paths") or {}).keys())
    run_options = dict(inputs.get("run_options") or input_manifest.get("run_options") or {})
    assets = inputs.get("assets") if isinstance(inputs.get("assets"), list) else input_manifest.get("assets") or []
    asset_ids = [str(item.get("asset_id") or "") for item in assets if isinstance(item, dict) and item.get("asset_id")]
    session = manifest.get("session") if isinstance(manifest.get("session"), dict) else {}
    fingerprints = inputs.get("fingerprints") if isinstance(inputs.get("fingerprints"), dict) else input_manifest.get("fingerprints")
    if not isinstance(fingerprints, dict):
        fingerprints = {}
    models = manifest.get("models") if isinstance(manifest.get("models"), dict) else {}
    image_model = models.get("image") if isinstance(models.get("image"), dict) else {}
    row = {
        "run_id": str(summary.get("run_id") or ""),
        "session_id": str(session.get("session_id") or input_manifest.get("session_id") or ""),
        "task_id": str(session.get("task_id") or input_manifest.get("task_id") or ""),
        "status": str(summary.get("status") or ""),
        "created_at": str(summary.get("created_at") or ""),
        "finished_at": str(summary.get("finished_at") or ""),
        "brief_sha256": str((inputs.get("brief") or input_manifest.get("brief") or {}).get("sha256") or ""),
        "asset_fingerprints": _asset_fingerprints(assets),
        "asset_ids": asset_ids,
        "input_fingerprints": dict(fingerprints),
        "market_queries": _string_list((inputs.get("market_evidence") or input_manifest.get("market_evidence") or {}).get("queries")),
        "run_options": run_options,
        "backend_public_base_url": str(run_options.get("backend_public_base_url") or ""),
        "image_model": {
            "key": str(image_model.get("key") or ""),
            "provider_id": str(image_model.get("provider_id") or ""),
            "model_id": str(image_model.get("model_id") or ""),
        },
        "reference_status": str(reference.get("status") or ""),
        "reference_required": bool(reference.get("required")),
        "reference_sent": bool(reference.get("sent")),
        "cover_count": len(summary.get("cover_paths") or []),
        "artifact_names": artifacts,
        "evaluation_status": str(evaluation.get("status") or "pending"),
        "evaluation_score": evaluation.get("score"),
        "evaluation_count": int(evaluation.get("count") or 0),
        "acceptance_status": str(acceptance.get("status") or ""),
        "accepted": bool(acceptance.get("accepted")),
        "acceptance_blocking_checks": list(acceptance.get("blocking_checks") or []),
        "acceptance_warning_checks": list(acceptance.get("warning_checks") or []),
    }
    row["candidate"] = _candidate_status(row)
    return row


def _candidate_status(row: dict[str, Any]) -> dict[str, Any]:
    blockers: list[str] = []
    if row["status"] != "succeeded":
        blockers.append("run_not_succeeded")
    if "content_package.json" not in row["artifact_names"]:
        blockers.append("missing_content_package")
    if row["cover_count"] < 1:
        blockers.append("missing_cover")
    if row["reference_required"] and not row["reference_sent"]:
        blockers.append("strict_reference_not_sent")
    if row.get("evaluation_status") == "blocked":
        blockers.append("evaluation_blocked")
    elif row.get("evaluation_status") == "needs_revision":
        blockers.append("evaluation_needs_revision")
    return {
        "ready_for_review": not blockers,
        "blocking_reasons": blockers,
    }


def _run_matches_filters(
    summary: dict[str, Any],
    *,
    status: str,
    proof_status: str,
    reference_status: str,
    evaluation_status: str,
    search: str,
) -> bool:
    row = content_production_comparison_run(summary)
    if status and row["status"] != status:
        return False
    actual_proof_status = str((summary.get("proof") or {}).get("status") or "")
    if proof_status and actual_proof_status != proof_status:
        return False
    if reference_status and row["reference_status"] != reference_status:
        return False
    if evaluation_status and row["evaluation_status"] != evaluation_status:
        return False
    needle = str(search or "").strip().lower()
    if not needle:
        return True
    return needle in _run_search_text(summary, row)


def _run_search_text(summary: dict[str, Any], row: dict[str, Any]) -> str:
    input_manifest = summary.get("input_manifest") if isinstance(summary.get("input_manifest"), dict) else {}
    experiment_manifest = summary.get("experiment_manifest") if isinstance(summary.get("experiment_manifest"), dict) else {}
    inputs = experiment_manifest.get("inputs") if isinstance(experiment_manifest.get("inputs"), dict) else {}
    market = inputs.get("market_evidence") if isinstance(inputs.get("market_evidence"), dict) else input_manifest.get("market_evidence")
    artifacts = [str(item.get("artifact_name") or "") for item in summary.get("artifact_catalog") or [] if isinstance(item, dict)]
    values = [
        str(summary.get("case_id") or ""),
        str(summary.get("run_id") or ""),
        str(summary.get("workflow_name") or ""),
        row["status"],
        str((summary.get("proof") or {}).get("status") or ""),
        str((summary.get("acceptance") or {}).get("status") or ""),
        row["reference_status"],
        row["evaluation_status"],
        *row["market_queries"],
        *_string_list((market or {}).get("queries") if isinstance(market, dict) else []),
        *artifacts,
    ]
    return " ".join(value.lower() for value in values if value)


def _asset_fingerprints(assets: Any) -> list[str]:
    out: list[str] = []
    source = assets if isinstance(assets, list) else []
    for item in source:
        if not isinstance(item, dict):
            continue
        value = (
            str(item.get("sha256") or "").strip()
            or str(item.get("public_reference_url") or "").strip()
            or str(item.get("path") or "").strip()
            or str(item.get("asset_id") or "").strip()
        )
        if value:
            out.append(value)
    return out


def content_production_count_by(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        value = str(row.get(key) or "")
        counts[value] = counts.get(value, 0) + 1
    return counts


def content_production_count_values(values: list[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for value in values:
        text = str(value or "")
        counts[text] = counts.get(text, 0) + 1
    return counts


def _value_diff(rows: list[dict[str, Any]], key: str) -> dict[str, Any]:
    values = {row["run_id"]: row.get(key) for row in rows}
    comparable = [json.dumps(value, ensure_ascii=False, sort_keys=True, default=str) for value in values.values()]
    return {
        "changed": len(set(comparable)) > 1,
        "by_run": values,
    }
