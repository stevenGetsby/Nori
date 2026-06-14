"""Case selection and promotion state for content-production experiments."""
from __future__ import annotations

from .common import (
    Any,
    EXPERIMENT_SELECTION_NAME,
    PROJECT_ROOT,
    SELECTION_DECISIONS,
    Path,
    _content_case_dir,
    _read_json,
    datetime,
    hashlib,
)
from .acceptance import content_production_run_acceptance_report
from .artifacts import _run_export_url, _run_replay_url
from .models import ContentCaseRef
from .presenters import content_production_report_run
from .repositories import ContentProductionExperimentRepository
from .runs import summarize_content_production_run


def get_content_production_case_selection(
    *,
    project_root: str | Path = PROJECT_ROOT,
    case_id: str,
) -> dict[str, Any]:
    from .case_reports import content_production_experiment_report

    repository = ContentProductionExperimentRepository(project_root)
    case_ref = ContentCaseRef(case_id=case_id)
    case_dir = repository.case_dir(case_ref)
    payload = _case_selection_payload(case_dir, include_history=True)
    payload["report"] = content_production_experiment_report(project_root=project_root, case_id=case_id)
    return payload


def record_content_production_case_selection(
    *,
    project_root: str | Path = PROJECT_ROOT,
    case_id: str,
    selection: dict[str, Any],
) -> dict[str, Any]:
    from .case_reports import content_production_experiment_report

    repository = ContentProductionExperimentRepository(project_root)
    case_ref = ContentCaseRef(case_id=case_id)
    case_dir = repository.case_dir(case_ref)
    run_id = str(selection.get("run_id") or "").strip()
    if not run_id:
        raise ValueError("run_id is required")
    summary = summarize_content_production_run(project_root=project_root, case_id=case_id, run_id=run_id)
    if not summary:
        raise FileNotFoundError(f"content-production run not found: {case_id}/{run_id}")

    existing = _case_selection_payload(case_dir, include_history=True)
    report = content_production_experiment_report(project_root=project_root, case_id=case_id)
    normalized = _normalize_case_selection(
        selection,
        case_id=case_id,
        run_summary=summary,
        report=report,
        existing_count=len(existing.get("history") or []) + 1,
    )
    history = [*list(existing.get("history") or []), normalized]
    payload = {
        "schema_version": 1,
        "case_id": case_id,
        "current": normalized,
        "history": history,
    }
    repository.write_case_selection(case_ref, payload)
    return {
        "case_id": case_id,
        "selection": normalized,
        "current": normalized,
        "history": history,
        "report": content_production_experiment_report(project_root=project_root, case_id=case_id),
        "selection_path": str(case_dir / EXPERIMENT_SELECTION_NAME),
    }


def promote_content_production_case_run(
    *,
    project_root: str | Path = PROJECT_ROOT,
    case_id: str,
    promotion: dict[str, Any],
) -> dict[str, Any]:
    """Promote an accepted run into the current case decision."""

    from .case_reports import content_production_experiment_report

    normalized_case_id = str(case_id or "").strip()
    if not normalized_case_id:
        raise ValueError("case_id is required")
    case_dir = _content_case_dir(project_root=project_root, case_id=normalized_case_id)
    selection_payload = _case_selection_payload(case_dir, include_history=True)
    selection = dict(selection_payload.get("current") or {})
    report = content_production_experiment_report(project_root=project_root, case_id=normalized_case_id, limit=500)
    best_run = report.get("best_run") if isinstance(report.get("best_run"), dict) else {}
    run_id = (
        str(promotion.get("run_id") or "").strip()
        or str(selection.get("run_id") or "").strip()
        or str(best_run.get("run_id") or "").strip()
    )
    if not run_id:
        raise ValueError("run_id is required")
    summary = summarize_content_production_run(project_root=project_root, case_id=normalized_case_id, run_id=run_id)
    if not summary:
        raise FileNotFoundError(f"content-production run not found: {normalized_case_id}/{run_id}")
    acceptance = content_production_run_acceptance_report(summary)
    allow_unaccepted = bool(promotion.get("allow_unaccepted"))
    if not bool(acceptance.get("accepted")) and not allow_unaccepted:
        raise ValueError(
            "run is not accepted; pass allow_unaccepted=true to promote with override"
        )
    reason = str(promotion.get("reason") or "").strip()
    if not reason:
        reason = "accepted run promoted" if bool(acceptance.get("accepted")) else "unaccepted run promoted with override"
    metadata = {
        "source": "backend.promote_content_production_case_run",
        "allow_unaccepted": allow_unaccepted,
        "acceptance_status": str(acceptance.get("status") or ""),
        **dict(promotion.get("metadata") or {}),
    }
    selection_result = record_content_production_case_selection(
        project_root=project_root,
        case_id=normalized_case_id,
        selection={
            "run_id": run_id,
            "decision": "promoted",
            "reviewer": str(promotion.get("reviewer") or "operator"),
            "reason": reason,
            "notes": str(promotion.get("notes") or ""),
            "metadata": metadata,
        },
    )
    return {
        "schema_version": 1,
        "case_id": normalized_case_id,
        "run_id": run_id,
        "promoted": True,
        "override": allow_unaccepted and not bool(acceptance.get("accepted")),
        "selection": dict(selection_result.get("selection") or {}),
        "selection_history_count": len(selection_result.get("history") or []),
        "acceptance": acceptance,
        "proof": dict(summary.get("proof") or {}),
        "run": content_production_report_run(summary),
        "links": {
            "selection": f"/experiments/content-production/cases/{normalized_case_id}/selection",
            "selected_run": f"/experiments/content-production/cases/{normalized_case_id}/selected-run",
            "case_compare": f"/experiments/content-production/cases/{normalized_case_id}/compare",
            "next_actions": f"/experiments/content-production/cases/{normalized_case_id}/next-actions",
            "run": f"/workflows/content-production/runs/{normalized_case_id}/{run_id}",
            "artifact_inspection": f"/workflows/content-production/runs/{normalized_case_id}/{run_id}/artifacts/inspect",
            "export": _run_export_url(normalized_case_id, run_id),
            "replay": _run_replay_url(normalized_case_id, run_id),
        },
    }


def _case_selection_payload(case_dir: Path | None, *, include_history: bool) -> dict[str, Any]:
    if case_dir is None:
        return {"schema_version": 1, "case_id": "", "current": {}, "history": [] if include_history else []}
    data = _read_json(case_dir / EXPERIMENT_SELECTION_NAME)
    current = data.get("current") if isinstance(data.get("current"), dict) else {}
    history = data.get("history") if isinstance(data.get("history"), list) else []
    payload = {
        "schema_version": int(data.get("schema_version") or 1),
        "case_id": str(data.get("case_id") or case_dir.name),
        "current": dict(current),
    }
    if include_history:
        payload["history"] = [dict(item) for item in history if isinstance(item, dict)]
    return payload


def _normalize_case_selection(
    data: dict[str, Any],
    *,
    case_id: str,
    run_summary: dict[str, Any],
    report: dict[str, Any],
    existing_count: int,
) -> dict[str, Any]:
    decision = str(data.get("decision") or "selected").strip().lower()
    if decision not in SELECTION_DECISIONS:
        raise ValueError(f"unsupported selection decision: {decision}")
    run = content_production_report_run(run_summary)
    reviewer = str(data.get("reviewer") or "operator").strip() or "operator"
    created_at = datetime.now().isoformat(timespec="seconds")
    run_id = str(run.get("run_id") or "")
    seed = f"{case_id}:{run_id}:{decision}:{reviewer}:{created_at}:{existing_count}"
    best_run = report.get("best_run") if isinstance(report.get("best_run"), dict) else {}
    best_run_id = str(best_run.get("run_id") or "")
    return {
        "selection_id": f"sel_{hashlib.sha256(seed.encode('utf-8')).hexdigest()[:12]}",
        "selected_at": created_at,
        "case_id": case_id,
        "run_id": run_id,
        "decision": decision,
        "reviewer": reviewer,
        "reason": str(data.get("reason") or ""),
        "notes": str(data.get("notes") or ""),
        "metadata": dict(data.get("metadata") or {}),
        "report_best_run_id": best_run_id,
        "matches_report_best": bool(best_run_id and run_id == best_run_id),
        "run": {
            "status": run.get("status"),
            "acceptance_status": run.get("acceptance_status"),
            "proof_status": run.get("proof_status"),
            "evaluation_status": run.get("evaluation_status"),
            "evaluation_score": run.get("evaluation_score"),
            "reference_status": run.get("reference_status"),
            "reference_sent": run.get("reference_sent"),
            "cover_count": run.get("cover_count"),
            "links": dict(run.get("links") or {}),
        },
    }
