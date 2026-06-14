"""Case-level overview, selected-run resolution, and list projections."""
from __future__ import annotations

from .common import (
    Any,
    PROJECT_ROOT,
    Path,
    _content_case_dir,
    _content_case_dir_or_none,
)
from .artifacts import _run_export_url
from .case_reports import content_production_experiment_report
from .run_rows import (
    content_production_comparison_run,
    content_production_count_by,
)
from .runs import (
    list_content_production_runs,
    summarize_content_production_run,
)
from .selections import case_selection_payload


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


def get_content_production_case_selected_run(
    *,
    project_root: str | Path = PROJECT_ROOT,
    case_id: str,
    fallback_to_best: bool = True,
) -> dict[str, Any]:
    """Resolve the current selected run for a case, optionally falling back to best_run."""

    case_dir = _content_case_dir(project_root=project_root, case_id=case_id)
    selection_payload = case_selection_payload(case_dir, include_history=True)
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


def list_content_production_cases(*, project_root: str | Path = PROJECT_ROOT) -> dict[str, Any]:
    """Return case-level summaries for recorded content-production experiments."""

    overview = content_production_experiment_overview(project_root=project_root, limit=1)
    return {
        "case_count": overview["case_count"],
        "run_count": overview["run_count"],
        "cases": overview["cases"],
        "summary": dict(overview.get("summary") or {}),
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
    selection = case_selection_payload(
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


__all__ = [
    "content_production_experiment_overview",
    "get_content_production_case_selected_run",
    "list_content_production_cases",
]
