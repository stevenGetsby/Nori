"""Delivery payload and review-evidence projections for experiment handoff bundles."""
from __future__ import annotations

from .common import Any
from .artifacts import _run_export_url


def case_delivery_payload(*, case_id: str, run_id: str, inspection: dict[str, Any]) -> dict[str, Any]:
    if not run_id or not inspection:
        return {
            "content_package": {},
            "covers": [],
            "export_url": "",
            "artifact_inspection_url": "",
        }
    return {
        "content_package": dict(inspection.get("content_package") or {}),
        "covers": list(inspection.get("covers") or []),
        "visual_reference_review": dict(inspection.get("visual_reference_review") or {}),
        "export_url": _run_export_url(case_id, run_id),
        "artifact_inspection_url": f"/workflows/content-production/runs/{case_id}/{run_id}/artifacts/inspect",
    }


def delivery_review_evidence(*, delivery: dict[str, Any], summary: dict[str, Any]) -> dict[str, Any]:
    inspection = delivery.get("artifact_inspection") if isinstance(delivery.get("artifact_inspection"), dict) else {}
    return {
        "schema_version": 1,
        "case_id": str(delivery.get("case_id") or summary.get("case_id") or ""),
        "run_id": str(delivery.get("run_id") or summary.get("run_id") or ""),
        "ready": bool(delivery.get("ready")),
        "status": str(delivery.get("status") or ""),
        "blocking_reasons": list(delivery.get("blocking_reasons") or []),
        "warning_reasons": list(delivery.get("warning_reasons") or []),
        "proof": dict(delivery.get("proof") or summary.get("proof") or {}),
        "acceptance": dict(delivery.get("acceptance") or summary.get("acceptance") or {}),
        "evaluations": dict(inspection.get("evaluations") or summary.get("evaluations") or {}),
        "image_reference": dict(inspection.get("image_reference") or summary.get("image_reference") or {}),
        "visual_reference_review": dict(
            inspection.get("visual_reference_review")
            or summary.get("visual_reference_review")
            or {}
        ),
        "artifact_counts": dict(inspection.get("artifact_counts") or {}),
        "missing_core_artifacts": list(inspection.get("missing_core_artifacts") or []),
    }


def run_review_evidence(*, summary: dict[str, Any], inspection: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "case_id": str(summary.get("case_id") or ""),
        "run_id": str(summary.get("run_id") or ""),
        "status": str(summary.get("status") or ""),
        "proof": dict(summary.get("proof") or {}),
        "acceptance": dict(summary.get("acceptance") or {}),
        "evaluations": dict(inspection.get("evaluations") or summary.get("evaluations") or {}),
        "image_reference": dict(inspection.get("image_reference") or summary.get("image_reference") or {}),
        "visual_reference_review": dict(
            inspection.get("visual_reference_review")
            or summary.get("visual_reference_review")
            or {}
        ),
        "artifact_counts": dict(inspection.get("artifact_counts") or {}),
        "missing_core_artifacts": list(inspection.get("missing_core_artifacts") or []),
    }
