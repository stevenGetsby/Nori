"""Case-level experiment reports and recommendations."""
from __future__ import annotations

from .common import Any, PROJECT_ROOT, Path, _content_case_dir_or_none, datetime
from .presenters import content_production_report_run, content_production_report_run_score
from .run_rows import content_production_count_by, content_production_count_values
from .runs import list_content_production_runs
from .selections import case_selection_payload


def content_production_experiment_report(
    *,
    project_root: str | Path = PROJECT_ROOT,
    case_id: str = "",
    limit: int = 50,
) -> dict[str, Any]:
    """Build a case-level experiment report for product/operator review."""

    normalized_limit = max(1, min(int(limit or 50), 500))
    listed = list_content_production_runs(project_root=project_root, case_id=case_id, limit=normalized_limit)
    summaries = [dict(row) for row in listed.get("runs") or [] if isinstance(row, dict)]
    rows = [content_production_report_run(summary) for summary in summaries]
    best_summary = max(summaries, key=content_production_report_run_score) if summaries else {}
    best_run = content_production_report_run(best_summary) if best_summary else {}
    if best_run:
        best_run["selection_reason"] = _best_run_reason(best_run)
    latest_run = rows[0] if rows else {}
    accepted = [row["run_id"] for row in rows if row["acceptance_status"] == "accepted"]
    needs_review = [row["run_id"] for row in rows if row["acceptance_status"] == "needs_review"]
    rejected = [row["run_id"] for row in rows if row["acceptance_status"] == "rejected"]
    summary = _report_summary(rows)
    selection = case_selection_payload(
        _content_case_dir_or_none(project_root=project_root, case_id=case_id),
        include_history=False,
    )
    return {
        "schema_version": 1,
        "case_id": str(case_id or ""),
        "scope": "case" if case_id else "all_cases",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "run_count": len(rows),
        "total_count": int(listed.get("total_count") or len(rows)),
        "filtered_count": int(listed.get("filtered_count") or len(rows)),
        "limit": normalized_limit,
        "has_more": bool(listed.get("has_more")),
        "best_run": best_run,
        "latest_run": latest_run,
        "accepted_run_ids": accepted,
        "needs_review_run_ids": needs_review,
        "rejected_run_ids": rejected,
        "summary": summary,
        "selection": selection.get("current") or {},
        "recommendations": _report_recommendations(rows, best_run=best_run, summary=summary),
        "runs": rows,
        "links": {
            "overview": f"/experiments/content-production/overview?case_id={case_id}" if case_id else "/experiments/content-production/overview",
            "runs": f"/workflows/content-production/runs?case_id={case_id}" if case_id else "/workflows/content-production/runs",
            "cases": "/experiments/content-production/cases",
        },
    }


def _best_run_reason(row: dict[str, Any]) -> str:
    if row.get("acceptance_status") == "accepted":
        return "accepted run with the strongest proof, evaluation, reference, and artifact signal"
    if row.get("acceptance_status") == "needs_review":
        return "highest-scoring run that still needs operator review"
    if row.get("acceptance_status") == "rejected":
        return "least-blocked rejected run; use its blocking checks as the next repair target"
    return "highest-scoring available run"


def _report_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "status_counts": content_production_count_by(rows, "status"),
        "acceptance_status_counts": content_production_count_by(rows, "acceptance_status"),
        "proof_status_counts": content_production_count_by(rows, "proof_status"),
        "reference_status_counts": content_production_count_by(rows, "reference_status"),
        "evaluation_status_counts": content_production_count_by(rows, "evaluation_status"),
        "blocking_check_counts": content_production_count_values([name for row in rows for name in row["blocking_checks"]]),
        "warning_check_counts": content_production_count_values([name for row in rows for name in row["warning_checks"]]),
        "proof_failed_check_counts": content_production_count_values([name for row in rows for name in row["proof_failed_checks"]]),
        "proof_warning_check_counts": content_production_count_values([name for row in rows for name in row["proof_warning_checks"]]),
        "candidate_blocking_reason_counts": content_production_count_values(
            [name for row in rows for name in row["candidate"]["blocking_reasons"]]
        ),
        "evaluation_issue_counts": _evaluation_issue_counts(rows),
        "accepted_count": sum(1 for row in rows if row["acceptance_status"] == "accepted"),
        "needs_review_count": sum(1 for row in rows if row["acceptance_status"] == "needs_review"),
        "rejected_count": sum(1 for row in rows if row["acceptance_status"] == "rejected"),
        "ready_for_review_count": sum(1 for row in rows if row["candidate"]["ready_for_review"]),
        "blocked_count": sum(1 for row in rows if not row["candidate"]["ready_for_review"]),
    }


def _evaluation_issue_counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    issue_codes: list[str] = []
    for row in rows:
        for issue in row.get("evaluation", {}).get("issues") or []:
            if isinstance(issue, dict):
                issue_codes.append(str(issue.get("code") or issue.get("category") or "issue"))
    return content_production_count_values(issue_codes)


def _report_recommendations(
    rows: list[dict[str, Any]],
    *,
    best_run: dict[str, Any],
    summary: dict[str, Any],
) -> list[dict[str, Any]]:
    if not rows:
        return [
            {
                "action_id": "run_first_experiment",
                "severity": "next_step",
                "message": "Run the first content-production experiment for this case.",
            }
        ]

    recommendations: list[dict[str, Any]] = []
    accepted_ids = [row["run_id"] for row in rows if row["acceptance_status"] == "accepted"]
    needs_review_ids = [row["run_id"] for row in rows if row["acceptance_status"] == "needs_review"]
    blocked_counts = dict(summary.get("blocking_check_counts") or {})
    candidate_counts = dict(summary.get("candidate_blocking_reason_counts") or {})
    proof_failed = dict(summary.get("proof_failed_check_counts") or {})
    evaluation_counts = dict(summary.get("evaluation_status_counts") or {})

    if accepted_ids:
        recommendations.append(
            {
                "action_id": "promote_accepted_run",
                "severity": "next_step",
                "message": "Promote the best accepted run into product review, export, or publishing preparation.",
                "run_id": str(best_run.get("run_id") or accepted_ids[0]),
            }
        )
    elif needs_review_ids:
        recommendations.append(
            {
                "action_id": "review_pending_runs",
                "severity": "review",
                "message": "Review the strongest needs_review runs and persist an evaluation decision.",
                "run_ids": needs_review_ids[:5],
            }
        )
    else:
        recommendations.append(
            {
                "action_id": "fix_blockers",
                "severity": "blocking",
                "message": "All visible runs are rejected; fix the most common blocking checks before rerunning.",
                "blocking_check_counts": blocked_counts,
            }
        )

    if blocked_counts.get("strict_reference_satisfied") or candidate_counts.get("strict_reference_not_sent"):
        recommendations.append(
            {
                "action_id": "fix_reference_transfer",
                "severity": "blocking",
                "message": "Fix reference-image transfer so selected uploads are provider-fetchable and sent to the image model.",
            }
        )
    if blocked_counts.get("cover_output_available") or candidate_counts.get("missing_cover") or proof_failed.get("cover_output"):
        recommendations.append(
            {
                "action_id": "rerun_cover_generation",
                "severity": "blocking",
                "message": "Rerun or debug cover generation; at least one run is missing image output.",
            }
        )
    if blocked_counts.get("content_package_available") or candidate_counts.get("missing_content_package"):
        recommendations.append(
            {
                "action_id": "debug_content_package",
                "severity": "blocking",
                "message": "Debug content package generation before comparing creative quality.",
            }
        )
    if evaluation_counts.get("passed", 0) < 1:
        recommendations.append(
            {
                "action_id": "record_or_draft_evaluation",
                "severity": "review",
                "message": "Generate or record at least one passing evaluation so the case has a reviewable winner.",
            }
        )
    return recommendations


__all__ = ["content_production_experiment_report"]
