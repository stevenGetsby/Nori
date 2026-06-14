"""Case-level action planning for content-production experiments."""
from __future__ import annotations

from .common import Any, PROJECT_ROOT, Path, _content_case_dir_or_none
from .artifacts import _run_export_url
from .action_builders import (
    case_repair_actions,
    case_review_actions,
    first_run_action,
    inspect_best_run_action,
    promote_selected_run_action,
    promoted_run_actions,
    select_best_run_action,
    stale_selection_repair_action,
)
from .case_reports import content_production_experiment_report
from .selections import _case_selection_payload


def content_production_case_next_actions(
    *,
    project_root: str | Path = PROJECT_ROOT,
    case_id: str,
    limit: int = 500,
) -> dict[str, Any]:
    """Return a backend-derived action plan for one content-production case."""

    case_dir = _content_case_dir_or_none(project_root=project_root, case_id=case_id)
    report = content_production_experiment_report(project_root=project_root, case_id=case_id, limit=limit)
    selection_payload = _case_selection_payload(case_dir, include_history=True)
    selection = dict(selection_payload.get("current") or {})
    rows = [row for row in report.get("runs") or [] if isinstance(row, dict)]
    selected_run_id = str(selection.get("run_id") or "")
    selected_run = next((row for row in rows if str(row.get("run_id") or "") == selected_run_id), {})
    best_run = dict(report.get("best_run") or {})
    target_run = dict(selected_run or best_run)
    selected_missing = bool(selected_run_id and not selected_run)
    status = _case_next_action_status(
        run_count=len(rows),
        selection=selection,
        selected_missing=selected_missing,
        target_run=target_run,
    )
    actions = _case_next_actions(
        case_id=case_id,
        status=status,
        selection=selection,
        selected_missing=selected_missing,
        selected_run=selected_run,
        best_run=best_run,
        target_run=target_run,
        report=report,
    )
    return {
        "schema_version": 1,
        "case_id": str(case_id),
        "status": status,
        "run_count": len(rows),
        "selected_run_id": selected_run_id,
        "best_run_id": str(best_run.get("run_id") or ""),
        "target_run_id": str(target_run.get("run_id") or ""),
        "selection": selection,
        "selected_run": selected_run,
        "best_run": best_run,
        "target_run": target_run,
        "selected_missing": selected_missing,
        "primary_action": actions[0] if actions else {},
        "actions": actions,
        "recommendations": list(report.get("recommendations") or []),
        "summary": dict(report.get("summary") or {}),
        "links": {
            "report": f"/experiments/content-production/report?case_id={case_id}",
            "selection": f"/experiments/content-production/cases/{case_id}/selection",
            "selected_run": f"/experiments/content-production/cases/{case_id}/selected-run",
            "timeline": f"/experiments/content-production/cases/{case_id}/timeline",
            "export": f"/experiments/content-production/cases/{case_id}/export",
            "runs": f"/workflows/content-production/runs?case_id={case_id}",
            "run": f"/workflows/content-production/runs/{case_id}/{target_run.get('run_id')}" if target_run else "",
            "run_export": _run_export_url(case_id, str(target_run.get("run_id") or "")) if target_run else "",
        },
    }


def _case_next_action_status(
    *,
    run_count: int,
    selection: dict[str, Any],
    selected_missing: bool,
    target_run: dict[str, Any],
) -> str:
    if run_count == 0:
        return "needs_first_run"
    if selected_missing:
        return "selection_stale"
    if not selection:
        return "needs_selection"
    decision = str(selection.get("decision") or "")
    if decision in {"rejected", "archived"}:
        return "selection_rejected"
    acceptance = str(target_run.get("acceptance_status") or "")
    evaluation = str(target_run.get("evaluation_status") or "")
    if decision == "promoted" and acceptance == "accepted" and evaluation == "passed":
        return "promoted"
    if acceptance == "accepted" and evaluation == "passed":
        return "ready_to_promote"
    if acceptance == "needs_review" or evaluation == "pending":
        return "needs_review"
    return "blocked"


def _case_next_actions(
    *,
    case_id: str,
    status: str,
    selection: dict[str, Any],
    selected_missing: bool,
    selected_run: dict[str, Any],
    best_run: dict[str, Any],
    target_run: dict[str, Any],
    report: dict[str, Any],
) -> list[dict[str, Any]]:
    if status == "needs_first_run":
        return [first_run_action(case_id=case_id)]

    if selected_missing:
        return [stale_selection_repair_action(case_id=case_id, best_run=best_run)]

    actions: list[dict[str, Any]] = []
    if status == "promoted" and target_run:
        return promoted_run_actions(case_id=case_id, target_run=target_run)

    if not selection and best_run:
        actions.append(select_best_run_action(case_id=case_id, best_run=best_run))

    target_acceptance = str(target_run.get("acceptance_status") or "")
    target_evaluation = str(target_run.get("evaluation_status") or "")
    if status == "ready_to_promote" and target_run:
        actions.append(promote_selected_run_action(case_id=case_id, target_run=target_run))
    elif target_run and (target_acceptance == "rejected" or target_evaluation in {"blocked", "needs_revision"}):
        actions.extend(case_repair_actions(case_id=case_id, target_run=target_run, report=report))
    elif status in {"needs_review", "needs_selection"} and target_run:
        actions.extend(case_review_actions(case_id=case_id, target_run=target_run))
    elif status in {"blocked", "selection_rejected"} and target_run:
        actions.extend(case_repair_actions(case_id=case_id, target_run=target_run, report=report))

    if not actions and best_run:
        actions.append(inspect_best_run_action(case_id=case_id, best_run=best_run))
    return actions
