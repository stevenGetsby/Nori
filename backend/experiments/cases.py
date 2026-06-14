"""Case-level reports, workbench state, and comparisons."""
from __future__ import annotations

from .common import (
    Any,
    PROJECT_ROOT,
    Path,
    _content_case_dir,
    _content_case_dir_or_none,
    datetime,
)
from .artifacts import _run_export_url
from .presenters import content_production_report_run, content_production_report_run_score
from .runs import (
    content_production_comparison_run,
    content_production_count_by,
    content_production_count_values,
    compare_content_production_runs,
    list_content_production_runs,
    summarize_content_production_run,
)
from .selections import _case_selection_payload


def content_production_experiment_overview(
    *,
    project_root: str | Path = PROJECT_ROOT,
    case_id: str = "",
    limit: int = 20,
) -> dict[str, Any]:
    """Aggregate recorded content-production experiments for product dashboards."""

    normalized_limit = max(1, min(int(limit or 20), 100))
    summaries = list_content_production_runs(project_root=project_root, case_id=case_id).get("runs", [])
    rows = [_overview_run(summary) for summary in summaries]
    cases: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        cases.setdefault(row["case_id"], []).append(row)

    blocked_reasons: dict[str, int] = {}
    for row in rows:
        for reason in row["candidate"]["blocking_reasons"]:
            blocked_reasons[reason] = blocked_reasons.get(reason, 0) + 1

    return {
        "case_id": str(case_id or ""),
        "run_count": len(rows),
        "case_count": len(cases),
        "latest_runs": rows[:normalized_limit],
        "summary": {
            "status_counts": content_production_count_by(rows, "status"),
            "acceptance_status_counts": content_production_count_by(rows, "acceptance_status"),
            "reference_status_counts": content_production_count_by(rows, "reference_status"),
            "evaluation_status_counts": content_production_count_by(rows, "evaluation_status"),
            "ready_count": sum(1 for row in rows if row["candidate"]["ready_for_review"]),
            "blocked_count": sum(1 for row in rows if not row["candidate"]["ready_for_review"]),
            "blocking_reason_counts": blocked_reasons,
        },
        "cases": [
            _overview_case(case_rows, project_root=project_root)
            for _case_id, case_rows in sorted(
                cases.items(),
                key=lambda item: str(item[1][0].get("created_at") or ""),
                reverse=True,
            )
        ],
    }


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
    selection = _case_selection_payload(_content_case_dir_or_none(project_root=project_root, case_id=case_id), include_history=False)
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


def get_content_production_case_selected_run(
    *,
    project_root: str | Path = PROJECT_ROOT,
    case_id: str,
    fallback_to_best: bool = True,
) -> dict[str, Any]:
    """Resolve the current selected run for a case, optionally falling back to best_run."""

    case_dir = _content_case_dir(project_root=project_root, case_id=case_id)
    selection_payload = _case_selection_payload(case_dir, include_history=True)
    selection = dict(selection_payload.get("current") or {})
    report = content_production_experiment_report(project_root=project_root, case_id=case_id, limit=500)
    source = "selection" if selection.get("run_id") else ""
    run_id = str(selection.get("run_id") or "")
    if not run_id and fallback_to_best:
        best_run = report.get("best_run") if isinstance(report.get("best_run"), dict) else {}
        run_id = str(best_run.get("run_id") or "")
        source = "best_run" if run_id else ""
    run = summarize_content_production_run(project_root=project_root, case_id=case_id, run_id=run_id) if run_id else {}
    reason = ""
    if not run_id:
        reason = "no_selection_or_best_run"
    elif not run:
        reason = "selected_run_not_found" if source == "selection" else "best_run_not_found"
    return {
        "schema_version": 1,
        "case_id": str(case_id),
        "resolved": bool(run),
        "source": source,
        "fallback_to_best": bool(fallback_to_best),
        "reason": reason,
        "run_id": run_id if run else "",
        "selection": selection,
        "run": run,
        "report": report,
        "links": {
            "selection": f"/experiments/content-production/cases/{case_id}/selection",
            "timeline": f"/experiments/content-production/cases/{case_id}/timeline",
            "export": f"/experiments/content-production/cases/{case_id}/export",
            "run": f"/workflows/content-production/runs/{case_id}/{run_id}" if run else "",
            "run_export": _run_export_url(case_id, run_id) if run else "",
        },
    }


def content_production_case_compare(
    *,
    project_root: str | Path = PROJECT_ROOT,
    case_id: str,
    limit: int = 500,
) -> dict[str, Any]:
    """Build a case-centered comparison snapshot for experiment decision UIs."""

    from .actions import content_production_case_next_actions

    normalized_case_id = str(case_id or "").strip()
    if not normalized_case_id:
        raise ValueError("case_id is required")
    normalized_limit = max(1, min(int(limit or 500), 1000))
    report = content_production_experiment_report(
        project_root=project_root,
        case_id=normalized_case_id,
        limit=normalized_limit,
    )
    summaries = [
        dict(row)
        for row in list_content_production_runs(
            project_root=project_root,
            case_id=normalized_case_id,
            limit=normalized_limit,
        ).get("runs", [])
        if isinstance(row, dict)
    ]
    selection_payload = _case_selection_payload(
        _content_case_dir_or_none(project_root=project_root, case_id=normalized_case_id),
        include_history=True,
    )
    selection = dict(selection_payload.get("current") or {})
    next_actions = content_production_case_next_actions(
        project_root=project_root,
        case_id=normalized_case_id,
        limit=normalized_limit,
    )
    best_run = dict(report.get("best_run") or {})
    selected_run_id = str(selection.get("run_id") or "")
    best_run_id = str(best_run.get("run_id") or "")
    recommended_run_id = selected_run_id or best_run_id
    report_rows_by_id = {
        str(row.get("run_id") or ""): row
        for row in report.get("runs") or []
        if isinstance(row, dict)
    }
    candidates = [
        _case_compare_candidate(
            summary,
            report_row=report_rows_by_id.get(str(summary.get("run_id") or ""), {}),
            selected_run_id=selected_run_id,
            best_run_id=best_run_id,
            recommended_run_id=recommended_run_id,
        )
        for summary in summaries
    ]
    comparison = (
        compare_content_production_runs(
            project_root=project_root,
            case_id=normalized_case_id,
            run_ids=[str(summary.get("run_id") or "") for summary in summaries],
        )
        if len(summaries) >= 2
        else {}
    )
    return {
        "schema_version": 1,
        "case_id": normalized_case_id,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "run_count": len(candidates),
        "selected_run_id": selected_run_id,
        "best_run_id": best_run_id,
        "recommended_run_id": recommended_run_id,
        "selection": selection,
        "selection_history": list(selection_payload.get("history") or []),
        "best_run": best_run,
        "selected_run": next((row for row in candidates if row["run_id"] == selected_run_id), {}),
        "recommended_run": next((row for row in candidates if row["run_id"] == recommended_run_id), {}),
        "candidates": candidates,
        "summary": dict(report.get("summary") or {}),
        "comparison_summary": dict((comparison.get("summary") or {}) if isinstance(comparison, dict) else {}),
        "differences": dict((comparison.get("differences") or {}) if isinstance(comparison, dict) else {}),
        "next_actions": next_actions,
        "primary_action": dict(next_actions.get("primary_action") or {}),
        "recommendations": list(report.get("recommendations") or []),
        "links": {
            "report": f"/experiments/content-production/report?case_id={normalized_case_id}",
            "runs": f"/workflows/content-production/runs?case_id={normalized_case_id}",
            "run_template": f"/experiments/content-production/run-template?case_id={normalized_case_id}",
            "compare_runs": (
                "/workflows/content-production/runs/compare?"
                f"case_id={normalized_case_id}&run_ids="
                f"{','.join(row['run_id'] for row in candidates)}"
            ) if len(candidates) >= 2 else "",
            "selection": f"/experiments/content-production/cases/{normalized_case_id}/selection",
            "selected_run": f"/experiments/content-production/cases/{normalized_case_id}/selected-run",
            "next_actions": f"/experiments/content-production/cases/{normalized_case_id}/next-actions",
            "case_evaluation_draft": f"/experiments/content-production/cases/{normalized_case_id}/evaluations/draft",
            "case_evaluations": f"/experiments/content-production/cases/{normalized_case_id}/evaluations",
            "timeline": f"/experiments/content-production/cases/{normalized_case_id}/timeline",
            "export": f"/experiments/content-production/cases/{normalized_case_id}/export",
        },
    }


def list_content_production_cases(*, project_root: str | Path = PROJECT_ROOT) -> dict[str, Any]:
    """Return case-level summaries for recorded content-production experiments."""

    overview = content_production_experiment_overview(project_root=project_root, limit=1)
    return {
        "case_count": overview["case_count"],
        "run_count": overview["run_count"],
        "cases": overview["cases"],
        "summary": dict(overview.get("summary") or {}),
    }


def _case_compare_candidate(
    summary: dict[str, Any],
    *,
    report_row: dict[str, Any],
    selected_run_id: str,
    best_run_id: str,
    recommended_run_id: str,
) -> dict[str, Any]:
    row = content_production_comparison_run(summary)
    run_id = row["run_id"]
    case_id = str(summary.get("case_id") or "")
    proof = summary.get("proof") if isinstance(summary.get("proof"), dict) else {}
    report_data = dict(report_row or {})
    base = f"/workflows/content-production/runs/{case_id}/{run_id}" if case_id and run_id else ""
    return {
        **row,
        "case_id": case_id,
        "is_selected": bool(run_id and run_id == selected_run_id),
        "is_best": bool(run_id and run_id == best_run_id),
        "is_recommended": bool(run_id and run_id == recommended_run_id),
        "proof_status": str(proof.get("status") or ""),
        "proof_failed_checks": list(proof.get("failed_checks") or []),
        "proof_warning_checks": list(proof.get("warning_checks") or []),
        "provider_fetchable_count": int(report_data.get("provider_fetchable_count") or 0),
        "selected_reference_count": int(report_data.get("selected_reference_count") or 0),
        "artifact_count": int(report_data.get("artifact_count") or len(row.get("artifact_names") or [])),
        "artifact_catalog_count": int(report_data.get("artifact_catalog_count") or 0),
        "selection_reason": str(report_data.get("selection_reason") or ""),
        "links": {
            "self": base,
            "acceptance": f"{base}/acceptance" if base else "",
            "evaluations": f"{base}/evaluations" if base else "",
            "evaluation_draft": f"{base}/evaluations/draft" if base else "",
            "replay": f"{base}/replay" if base else "",
            "export": f"{base}/export" if base else "",
        },
    }


def _overview_run(summary: dict[str, Any]) -> dict[str, Any]:
    row = content_production_comparison_run(summary)
    evaluation = summary.get("evaluations") if isinstance(summary.get("evaluations"), dict) else {}
    evaluation_summary_data = evaluation.get("summary") if isinstance(evaluation.get("summary"), dict) else {}
    reference = summary.get("image_reference") if isinstance(summary.get("image_reference"), dict) else {}
    artifacts = summary.get("artifact_paths") if isinstance(summary.get("artifact_paths"), dict) else {}
    case_id = str(summary.get("case_id") or "")
    return {
        "case_id": case_id,
        "run_id": row["run_id"],
        "workflow_name": str(summary.get("workflow_name") or ""),
        "status": row["status"],
        "created_at": row["created_at"],
        "finished_at": row["finished_at"],
        "reference_status": row["reference_status"],
        "reference_required": row["reference_required"],
        "reference_sent": row["reference_sent"],
        "cover_count": row["cover_count"],
        "artifact_count": len(artifacts),
        "evaluation_status": row["evaluation_status"],
        "evaluation_score": row["evaluation_score"],
        "evaluation_count": row["evaluation_count"],
        "candidate": row["candidate"],
        "proof_status": str((summary.get("proof") or {}).get("status") or ""),
        "proof_failed_checks": list((summary.get("proof") or {}).get("failed_checks") or []),
        "proof_warning_checks": list((summary.get("proof") or {}).get("warning_checks") or []),
        "acceptance_status": row["acceptance_status"],
        "accepted": row["accepted"],
        "acceptance_blocking_checks": row["acceptance_blocking_checks"],
        "acceptance_warning_checks": row["acceptance_warning_checks"],
        "links": {
            "self": f"/workflows/content-production/runs/{case_id}/{row['run_id']}",
            "evaluations": f"/workflows/content-production/runs/{case_id}/{row['run_id']}/evaluations",
            "replay": f"/workflows/content-production/runs/{case_id}/{row['run_id']}/replay",
            "export": f"/workflows/content-production/runs/{case_id}/{row['run_id']}/export",
        },
        "image_reference": {
            "status": str(reference.get("status") or ""),
            "selected_count": int(reference.get("selected_count") or 0),
            "sent": bool(reference.get("sent")),
            "fallback": str(reference.get("fallback") or ""),
        },
        "evaluations": evaluation_summary_data,
    }


def _overview_case(rows: list[dict[str, Any]], *, project_root: str | Path = PROJECT_ROOT) -> dict[str, Any]:
    latest = rows[0] if rows else {}
    case_id = str(latest.get("case_id") or "")
    latest_run_id = str(latest.get("run_id") or "")
    latest_base = f"/workflows/content-production/runs/{case_id}/{latest_run_id}" if case_id and latest_run_id else ""
    selection = _case_selection_payload(
        _content_case_dir_or_none(project_root=project_root, case_id=case_id),
        include_history=False,
    ).get("current") or {}
    return {
        "case_id": case_id,
        "run_count": len(rows),
        "latest_run_id": latest_run_id,
        "latest_status": str(latest.get("status") or ""),
        "latest_created_at": str(latest.get("created_at") or ""),
        "latest_finished_at": str(latest.get("finished_at") or ""),
        "status_counts": content_production_count_by(rows, "status"),
        "acceptance_status_counts": content_production_count_by(rows, "acceptance_status"),
        "reference_status_counts": content_production_count_by(rows, "reference_status"),
        "evaluation_status_counts": content_production_count_by(rows, "evaluation_status"),
        "ready_count": sum(1 for row in rows if row["candidate"]["ready_for_review"]),
        "blocked_count": sum(1 for row in rows if not row["candidate"]["ready_for_review"]),
        "selection": selection,
        "selected_run_id": str(selection.get("run_id") or ""),
        "selection_decision": str(selection.get("decision") or ""),
        "links": {
            "runs": f"/workflows/content-production/runs?case_id={case_id}" if case_id else "",
            "run_template": f"/experiments/content-production/run-template?case_id={case_id}" if case_id else "",
            "selection": f"/experiments/content-production/cases/{case_id}/selection" if case_id else "",
            "selected_run": f"/experiments/content-production/cases/{case_id}/selected-run" if case_id else "",
            "next_actions": f"/experiments/content-production/cases/{case_id}/next-actions" if case_id else "",
            "case_evaluation_draft": f"/experiments/content-production/cases/{case_id}/evaluations/draft" if case_id else "",
            "case_evaluations": f"/experiments/content-production/cases/{case_id}/evaluations" if case_id else "",
            "case_delivery": f"/experiments/content-production/cases/{case_id}/delivery" if case_id else "",
            "case_delivery_export": f"/experiments/content-production/cases/{case_id}/delivery/export" if case_id else "",
            "case_replay": f"/experiments/content-production/cases/{case_id}/replay" if case_id else "",
            "case_timeline": f"/experiments/content-production/cases/{case_id}/timeline" if case_id else "",
            "case_export": f"/experiments/content-production/cases/{case_id}/export" if case_id else "",
            "latest_run": latest_base,
            "latest_export": f"{latest_base}/export" if latest_base else "",
            "latest_replay": f"{latest_base}/replay" if latest_base else "",
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
