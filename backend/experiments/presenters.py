"""Presentation projections shared by content-production experiment surfaces."""
from __future__ import annotations

from .common import Any
from .reference_acceptance import content_production_summary_reference_transfer
from .run_rows import content_production_comparison_run


def content_production_report_run(summary: dict[str, Any]) -> dict[str, Any]:
    """Project a run summary into the case/report run row returned by product surfaces."""

    row = content_production_comparison_run(summary)
    case_id = str(summary.get("case_id") or "")
    run_id = row["run_id"]
    proof = summary.get("proof") if isinstance(summary.get("proof"), dict) else {}
    acceptance = summary.get("acceptance") if isinstance(summary.get("acceptance"), dict) else {}
    evidence = acceptance.get("evidence") if isinstance(acceptance.get("evidence"), dict) else {}
    evaluations = summary.get("evaluations") if isinstance(summary.get("evaluations"), dict) else {}
    evaluation = evaluations.get("summary") if isinstance(evaluations.get("summary"), dict) else {}
    transfer = content_production_summary_reference_transfer(summary)
    artifact_catalog = [item for item in summary.get("artifact_catalog") or [] if isinstance(item, dict)]
    base = f"/workflows/content-production/runs/{case_id}/{run_id}" if case_id and run_id else ""
    return {
        "case_id": case_id,
        "run_id": run_id,
        "session_id": row["session_id"],
        "task_id": row["task_id"],
        "workflow_name": str(summary.get("workflow_name") or ""),
        "status": row["status"],
        "created_at": row["created_at"],
        "finished_at": row["finished_at"],
        "acceptance_status": row["acceptance_status"],
        "accepted": row["accepted"],
        "proof_status": str(proof.get("status") or ""),
        "evaluation_status": row["evaluation_status"],
        "evaluation_score": row["evaluation_score"],
        "evaluation_count": row["evaluation_count"],
        "reference_status": row["reference_status"],
        "reference_required": row["reference_required"],
        "reference_sent": row["reference_sent"],
        "asset_ids": list(row.get("asset_ids") or []),
        "run_options": dict(row.get("run_options") or {}),
        "backend_public_base_url": str(row.get("backend_public_base_url") or ""),
        "provider_fetchable_count": int(
            transfer.get("provider_fetchable_count") or evidence.get("provider_fetchable_count") or 0
        ),
        "selected_reference_count": int(
            transfer.get("selected_count") or evidence.get("selected_reference_count") or 0
        ),
        "cover_count": row["cover_count"],
        "artifact_count": len(summary.get("artifact_paths") or {}),
        "artifact_catalog_count": len(artifact_catalog),
        "blocking_checks": row["acceptance_blocking_checks"],
        "warning_checks": row["acceptance_warning_checks"],
        "proof_failed_checks": list(proof.get("failed_checks") or []),
        "proof_warning_checks": list(proof.get("warning_checks") or []),
        "candidate": row["candidate"],
        "evaluation": dict(evaluation),
        "links": {
            "self": base,
            "acceptance": f"{base}/acceptance" if base else "",
            "evaluations": f"{base}/evaluations" if base else "",
            "evaluation_draft": f"{base}/evaluations/draft" if base else "",
            "replay": f"{base}/replay" if base else "",
            "export": f"{base}/export" if base else "",
        },
    }


def content_production_report_run_score(summary: dict[str, Any]) -> tuple[int, int, int, int, int, int, float, str]:
    """Rank run summaries for report best-run selection."""

    row = content_production_comparison_run(summary)
    proof = summary.get("proof") if isinstance(summary.get("proof"), dict) else {}
    acceptance_rank = {"accepted": 3, "needs_review": 2, "rejected": 1}.get(row["acceptance_status"], 0)
    proof_rank = {"ready": 3, "needs_review": 2, "blocked": 1}.get(str(proof.get("status") or ""), 0)
    evaluation_rank = {"passed": 3, "pending": 2, "needs_revision": 1, "blocked": 0}.get(
        row["evaluation_status"], 0
    )
    reference_rank = 2 if (not row["reference_required"] or row["reference_sent"]) else 0
    cover_rank = min(int(row["cover_count"] or 0), 3)
    artifact_rank = min(len(row["artifact_names"]), 10)
    score = row.get("evaluation_score")
    numeric_score = float(score) if isinstance(score, (int, float)) else -1.0
    return (
        acceptance_rank,
        proof_rank,
        evaluation_rank,
        reference_rank,
        cover_rank,
        artifact_rank,
        numeric_score,
        str(row.get("created_at") or ""),
    )
