"""Case-centered comparison snapshots for content-production experiments."""
from __future__ import annotations

from .common import Any, PROJECT_ROOT, Path, _content_case_dir_or_none, datetime
from .actions import content_production_case_next_actions
from .cases import content_production_experiment_report
from .run_rows import content_production_comparison_run
from .runs import (
    compare_content_production_runs,
    list_content_production_runs,
)
from .selections import _case_selection_payload


def content_production_case_compare(
    *,
    project_root: str | Path = PROJECT_ROOT,
    case_id: str,
    limit: int = 500,
) -> dict[str, Any]:
    """Build a case-centered comparison snapshot for experiment decision UIs."""

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


__all__ = [
    "content_production_case_compare",
]
