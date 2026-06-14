"""Reusable run-row projections and counters for content-production experiments."""
from __future__ import annotations

from .common import Any, _string_list, json


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


def content_production_value_diff(rows: list[dict[str, Any]], key: str) -> dict[str, Any]:
    values = {row["run_id"]: row.get(key) for row in rows}
    comparable = [json.dumps(value, ensure_ascii=False, sort_keys=True, default=str) for value in values.values()]
    return {
        "changed": len(set(comparable)) > 1,
        "by_run": values,
    }


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


__all__ = [
    "content_production_comparison_run",
    "content_production_count_by",
    "content_production_count_values",
    "content_production_value_diff",
]
