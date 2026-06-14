"""Content-production experiment workbench snapshots."""
from __future__ import annotations

from .common import Any, PROJECT_ROOT, Path, datetime
from .artifacts import inspect_content_production_run_artifacts
from .cases import content_production_experiment_overview
from .comparisons import content_production_case_compare
from .diagnostics import content_production_diagnostics


def content_production_experiment_workbench(
    *,
    project_root: str | Path = PROJECT_ROOT,
    case_id: str = "",
    limit: int = 20,
    include_diagnostics: bool = True,
    environ: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Build one product-console snapshot for backend content-production experiments."""

    normalized_case_id = str(case_id or "").strip()
    normalized_limit = max(1, min(int(limit or 20), 100))
    diagnostics = (
        content_production_diagnostics(project_root=project_root, environ=environ)
        if include_diagnostics
        else {}
    )
    overview = content_production_experiment_overview(
        project_root=project_root,
        case_id=normalized_case_id,
        limit=normalized_limit,
    )
    cases = [
        _workbench_case(row, project_root=project_root)
        for row in (overview.get("cases") or [])[:normalized_limit]
        if isinstance(row, dict)
    ]
    if normalized_case_id and not cases:
        cases = [_empty_workbench_case(normalized_case_id)]
    primary_actions = [
        {"case_id": row["case_id"], **dict(row.get("primary_action") or {})}
        for row in cases
        if isinstance(row.get("primary_action"), dict) and row.get("primary_action")
    ]
    case_compare = (
        content_production_case_compare(
            project_root=project_root,
            case_id=normalized_case_id,
            limit=normalized_limit,
        )
        if normalized_case_id
        else {}
    )
    active_run_id = _workbench_active_run_id(case_compare)
    active_run_artifacts = (
        inspect_content_production_run_artifacts(
            project_root=project_root,
            case_id=normalized_case_id,
            run_id=active_run_id,
        )
        if normalized_case_id and active_run_id
        else {}
    )
    from .delivery import content_production_case_delivery

    case_delivery = (
        content_production_case_delivery(
            project_root=project_root,
            case_id=normalized_case_id,
        )
        if normalized_case_id
        else {}
    )
    return {
        "schema_version": 1,
        "scope": "case" if normalized_case_id else "all_cases",
        "case_id": normalized_case_id,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "ready": bool(diagnostics.get("ready", True)) if include_diagnostics else True,
        "status": _workbench_status(diagnostics=diagnostics, cases=cases, overview=overview),
        "diagnostics": diagnostics,
        "overview": overview,
        "cases": cases,
        "primary_actions": primary_actions,
        "case_compare": case_compare,
        "case_delivery": case_delivery,
        "active_run_id": active_run_id,
        "active_run_artifacts": active_run_artifacts,
        "links": {
            "diagnostics": "/experiments/content-production/diagnostics",
            "overview": (
                f"/experiments/content-production/overview?case_id={normalized_case_id}"
                if normalized_case_id
                else "/experiments/content-production/overview"
            ),
            "cases": "/experiments/content-production/cases",
            "runs": (
                f"/workflows/content-production/runs?case_id={normalized_case_id}"
                if normalized_case_id
                else "/workflows/content-production/runs"
            ),
            "run_template": (
                f"/experiments/content-production/run-template?case_id={normalized_case_id}"
                if normalized_case_id
                else "/experiments/content-production/run-template"
            ),
            "case_compare": f"/experiments/content-production/cases/{normalized_case_id}/compare" if normalized_case_id else "",
            "case_delivery": f"/experiments/content-production/cases/{normalized_case_id}/delivery" if normalized_case_id else "",
            "case_delivery_export": (
                f"/experiments/content-production/cases/{normalized_case_id}/delivery/export"
                if normalized_case_id
                else ""
            ),
            "case_replay": f"/experiments/content-production/cases/{normalized_case_id}/replay" if normalized_case_id else "",
            "case_evaluation_draft": (
                f"/experiments/content-production/cases/{normalized_case_id}/evaluations/draft"
                if normalized_case_id
                else ""
            ),
            "case_evaluations": (
                f"/experiments/content-production/cases/{normalized_case_id}/evaluations"
                if normalized_case_id
                else ""
            ),
            "active_run_artifacts": (
                f"/workflows/content-production/runs/{normalized_case_id}/{active_run_id}/artifacts/inspect"
                if normalized_case_id and active_run_id
                else ""
            ),
        },
    }


def _workbench_active_run_id(case_compare: dict[str, Any]) -> str:
    for key in ("recommended_run_id", "target_run_id", "selected_run_id", "best_run_id"):
        value = str(case_compare.get(key) or "").strip()
        if value:
            return value
    return ""


def _workbench_case(row: dict[str, Any], *, project_root: str | Path) -> dict[str, Any]:
    from .actions import content_production_case_next_actions

    case_id = str(row.get("case_id") or "")
    next_actions = content_production_case_next_actions(project_root=project_root, case_id=case_id)
    case_base = f"/experiments/content-production/cases/{case_id}" if case_id else ""
    return {
        **dict(row),
        "action_status": str(next_actions.get("status") or ""),
        "target_run_id": str(next_actions.get("target_run_id") or ""),
        "primary_action": dict(next_actions.get("primary_action") or {}),
        "actions": list(next_actions.get("actions") or []),
        "action_count": len(next_actions.get("actions") or []),
        "links": {
            **dict(row.get("links") or {}),
            "next_actions": f"{case_base}/next-actions" if case_base else "",
            "case_evaluation_draft": f"{case_base}/evaluations/draft" if case_base else "",
            "case_evaluations": f"{case_base}/evaluations" if case_base else "",
        },
    }


def _empty_workbench_case(case_id: str) -> dict[str, Any]:
    from .action_builders import first_run_action

    actions = [first_run_action(case_id=case_id)]
    return {
        "case_id": case_id,
        "run_count": 0,
        "latest_run_id": "",
        "latest_status": "",
        "ready_count": 0,
        "blocked_count": 0,
        "selection": {},
        "selected_run_id": "",
        "selection_decision": "",
        "action_status": "needs_first_run",
        "target_run_id": "",
        "primary_action": actions[0] if actions else {},
        "actions": actions,
        "action_count": len(actions),
        "links": {
            "runs": f"/workflows/content-production/runs?case_id={case_id}",
            "run_template": f"/experiments/content-production/run-template?case_id={case_id}",
            "selection": f"/experiments/content-production/cases/{case_id}/selection",
            "next_actions": f"/experiments/content-production/cases/{case_id}/next-actions",
            "case_evaluation_draft": f"/experiments/content-production/cases/{case_id}/evaluations/draft",
            "case_evaluations": f"/experiments/content-production/cases/{case_id}/evaluations",
        },
    }


def _workbench_status(*, diagnostics: dict[str, Any], cases: list[dict[str, Any]], overview: dict[str, Any]) -> str:
    if diagnostics and str(diagnostics.get("status") or "") == "blocked":
        return "setup_blocked"
    if not cases and int(overview.get("run_count") or 0) == 0:
        return "empty"
    severities = [
        str((row.get("primary_action") or {}).get("severity") or "")
        for row in cases
        if isinstance(row.get("primary_action"), dict)
    ]
    if "blocking" in severities:
        return "needs_attention"
    if severities:
        return "actionable"
    return "ready"


__all__ = ["content_production_experiment_workbench"]
