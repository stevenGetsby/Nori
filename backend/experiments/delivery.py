"""Case-level delivery readiness and handoff evidence."""
from __future__ import annotations

from .common import Any, PROJECT_ROOT, Path, _content_case_dir_or_none, datetime
from .acceptance import content_production_run_acceptance_report
from .actions import content_production_case_next_actions
from .artifacts import _run_export_url, _run_replay_url, inspect_content_production_run_artifacts
from .delivery_payloads import case_delivery_payload
from .presenters import content_production_report_run
from .case_reports import content_production_experiment_report
from .comparisons import content_production_case_compare
from .runs import summarize_content_production_run
from .selections import case_selection_payload


def content_production_case_delivery(
    *,
    project_root: str | Path = PROJECT_ROOT,
    case_id: str,
    allow_unpromoted: bool = False,
) -> dict[str, Any]:
    """Return a case-level delivery readiness snapshot."""

    normalized_case_id = str(case_id or "").strip()
    if not normalized_case_id:
        raise ValueError("case_id is required")

    case_dir = _content_case_dir_or_none(project_root=project_root, case_id=normalized_case_id)
    selection_payload = case_selection_payload(case_dir, include_history=True)
    selection = dict(selection_payload.get("current") or {})
    report = content_production_experiment_report(
        project_root=project_root,
        case_id=normalized_case_id,
        limit=500,
    )
    best_run = dict(report.get("best_run") or {})
    run_id = str(selection.get("run_id") or "").strip() or str(best_run.get("run_id") or "").strip()
    promoted = str(selection.get("decision") or "") == "promoted" and bool(selection.get("run_id"))
    blockers: list[str] = []
    warnings: list[str] = []
    summary: dict[str, Any] = {}
    acceptance: dict[str, Any] = {}
    inspection: dict[str, Any] = {}

    if not run_id:
        blockers.append("no_run")
    else:
        summary = summarize_content_production_run(
            project_root=project_root,
            case_id=normalized_case_id,
            run_id=run_id,
        )
        if not summary:
            blockers.append("run_not_found")
        else:
            acceptance = content_production_run_acceptance_report(summary)
            inspection = inspect_content_production_run_artifacts(
                project_root=project_root,
                case_id=normalized_case_id,
                run_id=run_id,
            )
            if not promoted and not allow_unpromoted:
                blockers.append("not_promoted")
            elif not promoted:
                warnings.append("unpromoted_preview")
            if str(acceptance.get("status") or "") != "accepted":
                blockers.append("not_accepted")
            missing_core = [str(item) for item in inspection.get("missing_core_artifacts") or [] if item]
            if missing_core:
                blockers.append("missing_core_artifacts")
            if not _run_export_url(normalized_case_id, run_id):
                blockers.append("missing_export")

    status = _case_delivery_status(blockers, warnings)
    case_compare = content_production_case_compare(
        project_root=project_root,
        case_id=normalized_case_id,
        limit=500,
    )
    next_actions = content_production_case_next_actions(
        project_root=project_root,
        case_id=normalized_case_id,
        limit=500,
    )
    delivery = case_delivery_payload(
        case_id=normalized_case_id,
        run_id=run_id if summary else "",
        inspection=inspection,
    )
    return {
        "schema_version": 1,
        "case_id": normalized_case_id,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "ready": not blockers,
        "status": status,
        "allow_unpromoted": bool(allow_unpromoted),
        "run_id": run_id if summary else "",
        "promoted": promoted,
        "selection": selection,
        "selection_history": list(selection_payload.get("history") or []),
        "blocking_reasons": blockers,
        "warning_reasons": warnings,
        "acceptance": acceptance,
        "proof": dict(summary.get("proof") or {}) if summary else {},
        "run": content_production_report_run(summary) if summary else {},
        "artifact_inspection": inspection,
        "case_compare": case_compare,
        "next_actions": next_actions,
        "delivery": delivery,
        "links": {
            "workbench": f"/experiments/content-production/workbench?case_id={normalized_case_id}",
            "case_compare": f"/experiments/content-production/cases/{normalized_case_id}/compare",
            "selection": f"/experiments/content-production/cases/{normalized_case_id}/selection",
            "promotion": f"/experiments/content-production/cases/{normalized_case_id}/promotion",
            "next_actions": f"/experiments/content-production/cases/{normalized_case_id}/next-actions",
            "delivery_export": f"/experiments/content-production/cases/{normalized_case_id}/delivery/export",
            "run": f"/workflows/content-production/runs/{normalized_case_id}/{run_id}" if summary else "",
            "artifact_inspection": (
                f"/workflows/content-production/runs/{normalized_case_id}/{run_id}/artifacts/inspect"
                if summary
                else ""
            ),
            "export": _run_export_url(normalized_case_id, run_id) if summary else "",
            "replay": _run_replay_url(normalized_case_id, run_id) if summary else "",
        },
    }


def _case_delivery_status(blockers: list[str], warnings: list[str]) -> str:
    if not blockers:
        return "preview_ready" if "unpromoted_preview" in warnings else "ready"
    if "no_run" in blockers:
        return "needs_run"
    if "run_not_found" in blockers:
        return "missing_run"
    if "not_promoted" in blockers:
        return "needs_promotion"
    if "not_accepted" in blockers:
        return "needs_acceptance"
    if "missing_core_artifacts" in blockers:
        return "needs_artifacts"
    return "blocked"
