"""Operator acceptance reports for content-production runs."""
from __future__ import annotations

from .common import Any
from .artifacts import _run_export_url, _run_replay_url
from .reference_acceptance import (
    acceptance_reference_check,
    acceptance_reference_generation_check,
)


def content_production_run_acceptance_report(summary: dict[str, Any]) -> dict[str, Any]:
    """Build the operator/product acceptance report for one experiment run."""

    from .run_rows import content_production_comparison_run

    row = content_production_comparison_run(summary)
    proof = summary.get("proof") if isinstance(summary.get("proof"), dict) else {}
    artifact_paths = summary.get("artifact_paths") if isinstance(summary.get("artifact_paths"), dict) else {}
    artifact_catalog = [item for item in summary.get("artifact_catalog") or [] if isinstance(item, dict)]
    case_id = str(summary.get("case_id") or "")
    run_id = str(summary.get("run_id") or row.get("run_id") or "")
    evaluations = summary.get("evaluations") if isinstance(summary.get("evaluations"), dict) else {}
    evaluation = evaluations.get("summary") if isinstance(evaluations.get("summary"), dict) else {}
    reference = proof.get("reference") if isinstance(proof.get("reference"), dict) else {}
    transfer = reference.get("transfer") if isinstance(reference.get("transfer"), dict) else {}
    image_reference = reference.get("image_reference") if isinstance(reference.get("image_reference"), dict) else {}
    generation_check = reference.get("generation_check") if isinstance(reference.get("generation_check"), dict) else {}
    reference_required = bool(reference.get("required") or row.get("reference_required"))
    generation_check_required = bool(reference.get("generation_check_required"))
    export_url = _run_export_url(case_id, run_id)
    replay_url = _run_replay_url(case_id, run_id)
    proof_failed = list(proof.get("failed_checks") or [])
    proof_warnings = list(proof.get("warning_checks") or [])
    evaluation_status = str(evaluation.get("status") or "pending")
    evaluation_check_status = "passed"
    evaluation_message = "latest evaluation passed"
    if evaluation_status in {"blocked", "needs_revision"}:
        evaluation_check_status = "failed"
        evaluation_message = f"latest evaluation status is {evaluation_status}"
    elif evaluation_status != "passed":
        evaluation_check_status = "warning"
        evaluation_message = "no passing evaluation has been recorded"

    checks = [
        _acceptance_check(
            "workflow_succeeded",
            "passed" if row["status"] == "succeeded" else "failed",
            "workflow completed successfully" if row["status"] == "succeeded" else "workflow did not complete successfully",
            workflow_status=row["status"],
        ),
        _acceptance_check(
            "proof_ready",
            "failed" if proof_failed else ("warning" if proof_warnings else "passed"),
            "proof checks are ready" if not proof_failed and not proof_warnings else "proof has blocking or warning checks",
            proof_status=str(proof.get("status") or ""),
            failed_checks=proof_failed,
            warning_checks=proof_warnings,
        ),
        _acceptance_check(
            "content_package_available",
            "passed" if "content_package.json" in artifact_paths else "failed",
            "content_package.json is available" if "content_package.json" in artifact_paths else "content_package.json is missing",
            artifact_url=str((summary.get("artifact_urls") or {}).get("content_package.json") or ""),
        ),
        _acceptance_check(
            "cover_output_available",
            "passed" if row["cover_count"] > 0 else "failed",
            "cover output is available" if row["cover_count"] > 0 else "cover output is missing",
            cover_count=row["cover_count"],
        ),
        _acceptance_check(
            "artifact_catalog_available",
            "passed" if artifact_catalog else "warning",
            "artifact catalog is available" if artifact_catalog else "artifact catalog is empty",
            catalog_count=len(artifact_catalog),
        ),
        _acceptance_check(
            "export_available",
            "passed" if export_url and artifact_catalog else "warning",
            "export endpoint can be used" if export_url and artifact_catalog else "export endpoint or exportable artifacts are missing",
            url=export_url,
        ),
        _acceptance_check(
            "replay_snapshot_available",
            "passed" if "replay_request.json" in artifact_paths and replay_url else "warning",
            "replay snapshot is available" if "replay_request.json" in artifact_paths and replay_url else "replay snapshot is missing",
            artifact_url=str((summary.get("artifact_urls") or {}).get("replay_request.json") or ""),
            url=replay_url,
        ),
        acceptance_reference_check(
            reference_required=reference_required,
            transfer=transfer,
            image_reference=image_reference,
        ),
        *(
            [
                acceptance_reference_generation_check(
                    generation_check_required=generation_check_required,
                    generation_check=generation_check,
                )
            ]
            if generation_check_required or generation_check
            else []
        ),
        _acceptance_check(
            "evaluation_passed",
            evaluation_check_status,
            evaluation_message,
            evaluation_status=evaluation_status,
            score=evaluation.get("score"),
            latest_evaluation_id=str(evaluation.get("latest_evaluation_id") or ""),
        ),
    ]
    failed = [check for check in checks if check["status"] == "failed"]
    warnings = [check for check in checks if check["status"] == "warning"]
    status = "rejected" if failed else ("needs_review" if warnings else "accepted")
    return {
        "schema_version": 1,
        "accepted": status == "accepted",
        "status": status,
        "blocking_checks": [check["name"] for check in failed],
        "warning_checks": [check["name"] for check in warnings],
        "checks": checks,
        "evidence": {
            "case_id": case_id,
            "run_id": run_id,
            "proof_status": str(proof.get("status") or ""),
            "workflow_status": row["status"],
            "evaluation": dict(evaluation),
            "reference_required": reference_required,
            "reference_sent": bool(image_reference.get("sent") or row.get("reference_sent")),
            "reference_generation_check_required": generation_check_required,
            "reference_generation_check_ready": bool(generation_check.get("ready")),
            "reference_generation_check_covers_selected": bool(
                generation_check.get("covers_selected_reference_images")
            ),
            "reference_generation_check_reason": str(generation_check.get("reason") or ""),
            "reference_status": str(image_reference.get("status") or row.get("reference_status") or ""),
            "provider_fetchable_count": int(transfer.get("provider_fetchable_count") or 0),
            "selected_reference_count": int(transfer.get("selected_count") or image_reference.get("selected_count") or 0),
            "reference_trace_count": int(image_reference.get("trace_count") or len(image_reference.get("trace") or [])),
            "reference_trace_provider_fetchable_count": int(image_reference.get("trace_provider_fetchable_count") or 0),
            "reference_trace_sent_count": int(image_reference.get("trace_sent_count") or 0),
            "reference_trace": list(image_reference.get("trace") or []),
            "artifact_catalog_count": len(artifact_catalog),
            "cover_count": row["cover_count"],
            "cover_urls": list(summary.get("cover_urls") or []),
            "export_url": export_url,
            "replay_url": replay_url,
        },
    }


def _acceptance_check(name: str, status: str, message: str, **extra: Any) -> dict[str, Any]:
    data = {"name": name, "status": status, "message": message}
    data.update({key: value for key, value in extra.items() if not _empty_acceptance_extra(value)})
    return data


def _empty_acceptance_extra(value: Any) -> bool:
    return value is None or value == "" or value == []


__all__ = ["content_production_run_acceptance_report"]
