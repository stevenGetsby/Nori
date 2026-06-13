"""Case-level selections, reports, comparisons, delivery, and timelines."""
from __future__ import annotations

from .common import (
    Any,
    Callable,
    CaseWorkspace,
    ClientBrief,
    ContentProductionConfig,
    ContentProductionWorkflow,
    ContentTask,
    EVALUATION_STATUSES,
    EXPERIMENT_EVALUATIONS_NAME,
    EXPERIMENT_MANIFEST_NAME,
    EXPERIMENT_SELECTION_NAME,
    IntentContract,
    LLMFactory,
    PROJECT_ROOT,
    Path,
    SELECTION_DECISIONS,
    TopNotesResult,
    _case_id_from_run_dir,
    _content_case_dir,
    _content_case_dir_or_none,
    _content_run_dir,
    _dedupe_strings,
    _dict_list,
    _exportable_input_files,
    _exportable_run_files,
    _file_sha256,
    _first_stage_time,
    _is_relative_to,
    _is_remote_url,
    _json_sha256,
    _read_json,
    _reference_transfer_snapshot,
    _safe_run_artifact_path,
    _slug,
    _string_list,
    _write_json,
    datetime,
    hashlib,
    importlib,
    infer_project_root_from_cases_path,
    io,
    json,
    llms,
    os,
    provider_fetchable_reference_url,
    record_content_production_artifacts,
    top_notes_result_from_dict,
    zipfile,
)
from .artifacts import _run_export_url, _run_replay_url, inspect_content_production_run_artifacts
from .diagnostics import content_production_diagnostics
from .models import ContentCaseRef
from .repositories import ContentProductionExperimentRepository
from .reviews import _summary_reference_transfer, content_production_run_acceptance_report
from .runs import (
    _comparison_run,
    _count_by,
    _count_values,
    compare_content_production_runs,
    list_content_production_runs,
    summarize_content_production_run,
)


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
            "status_counts": _count_by(rows, "status"),
            "acceptance_status_counts": _count_by(rows, "acceptance_status"),
            "reference_status_counts": _count_by(rows, "reference_status"),
            "evaluation_status_counts": _count_by(rows, "evaluation_status"),
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
    rows = [_report_run(summary) for summary in summaries]
    best_summary = max(summaries, key=_report_run_score) if summaries else {}
    best_run = _report_run(best_summary) if best_summary else {}
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


def get_content_production_case_selection(
    *,
    project_root: str | Path = PROJECT_ROOT,
    case_id: str,
) -> dict[str, Any]:
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
        "run": _report_run(summary),
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
    selection_payload = _case_selection_payload(case_dir, include_history=True)
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
    delivery = _case_delivery_payload(
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
        "run": _report_run(summary) if summary else {},
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


def content_production_case_timeline(
    *,
    project_root: str | Path = PROJECT_ROOT,
    case_id: str,
    limit: int = 200,
) -> dict[str, Any]:
    """Return a chronological audit timeline for one content-production case."""

    _content_case_dir(project_root=project_root, case_id=case_id)
    normalized_limit = max(1, min(int(limit or 200), 1000))
    runs = list_content_production_runs(project_root=project_root, case_id=case_id, limit=1000).get("runs", [])
    selection = get_content_production_case_selection(project_root=project_root, case_id=case_id)
    events: list[dict[str, Any]] = []
    for summary in runs:
        events.extend(_timeline_events_for_run(summary))
    for item in selection.get("history") or []:
        if isinstance(item, dict):
            events.append(_timeline_selection_event(item))
    events = sorted(events, key=_timeline_sort_key, reverse=True)
    visible = events[:normalized_limit]
    return {
        "schema_version": 1,
        "case_id": str(case_id),
        "event_count": len(events),
        "returned_count": len(visible),
        "limit": normalized_limit,
        "has_more": len(events) > normalized_limit,
        "events": visible,
        "summary": {
            "event_type_counts": _count_by(events, "event_type"),
            "run_count": len(runs),
            "evaluation_count": sum(1 for event in events if event["event_type"] == "evaluation_recorded"),
            "selection_count": sum(1 for event in events if event["event_type"] == "selection_recorded"),
        },
        "links": {
            "report": f"/experiments/content-production/report?case_id={case_id}",
            "cases": "/experiments/content-production/cases",
            "selection": f"/experiments/content-production/cases/{case_id}/selection",
            "export": f"/experiments/content-production/cases/{case_id}/export",
            "runs": f"/workflows/content-production/runs?case_id={case_id}",
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
    row = _comparison_run(summary)
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
    row = _comparison_run(summary)
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
        "status_counts": _count_by(rows, "status"),
        "acceptance_status_counts": _count_by(rows, "acceptance_status"),
        "reference_status_counts": _count_by(rows, "reference_status"),
        "evaluation_status_counts": _count_by(rows, "evaluation_status"),
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


def _report_run(summary: dict[str, Any]) -> dict[str, Any]:
    row = _comparison_run(summary)
    case_id = str(summary.get("case_id") or "")
    run_id = row["run_id"]
    proof = summary.get("proof") if isinstance(summary.get("proof"), dict) else {}
    acceptance = summary.get("acceptance") if isinstance(summary.get("acceptance"), dict) else {}
    evidence = acceptance.get("evidence") if isinstance(acceptance.get("evidence"), dict) else {}
    evaluations = summary.get("evaluations") if isinstance(summary.get("evaluations"), dict) else {}
    evaluation = evaluations.get("summary") if isinstance(evaluations.get("summary"), dict) else {}
    transfer = _summary_reference_transfer(summary)
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
        "provider_fetchable_count": int(transfer.get("provider_fetchable_count") or evidence.get("provider_fetchable_count") or 0),
        "selected_reference_count": int(transfer.get("selected_count") or evidence.get("selected_reference_count") or 0),
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


def _report_run_score(summary: dict[str, Any]) -> tuple[int, int, int, int, int, int, float, str]:
    row = _comparison_run(summary)
    proof = summary.get("proof") if isinstance(summary.get("proof"), dict) else {}
    acceptance_rank = {"accepted": 3, "needs_review": 2, "rejected": 1}.get(row["acceptance_status"], 0)
    proof_rank = {"ready": 3, "needs_review": 2, "blocked": 1}.get(str(proof.get("status") or ""), 0)
    evaluation_rank = {"passed": 3, "pending": 2, "needs_revision": 1, "blocked": 0}.get(row["evaluation_status"], 0)
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
        "status_counts": _count_by(rows, "status"),
        "acceptance_status_counts": _count_by(rows, "acceptance_status"),
        "proof_status_counts": _count_by(rows, "proof_status"),
        "reference_status_counts": _count_by(rows, "reference_status"),
        "evaluation_status_counts": _count_by(rows, "evaluation_status"),
        "blocking_check_counts": _count_values([name for row in rows for name in row["blocking_checks"]]),
        "warning_check_counts": _count_values([name for row in rows for name in row["warning_checks"]]),
        "proof_failed_check_counts": _count_values([name for row in rows for name in row["proof_failed_checks"]]),
        "proof_warning_check_counts": _count_values([name for row in rows for name in row["proof_warning_checks"]]),
        "candidate_blocking_reason_counts": _count_values(
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
    return _count_values(issue_codes)


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


def _workbench_active_run_id(case_compare: dict[str, Any]) -> str:
    for key in ("recommended_run_id", "target_run_id", "selected_run_id", "best_run_id"):
        value = str(case_compare.get(key) or "").strip()
        if value:
            return value
    return ""


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


def _case_delivery_payload(*, case_id: str, run_id: str, inspection: dict[str, Any]) -> dict[str, Any]:
    if not run_id or not inspection:
        return {
            "content_package": {},
            "covers": [],
            "export_url": "",
            "artifact_inspection_url": "",
        }
    return {
        "content_package": dict(inspection.get("content_package") or {}),
        "covers": list(inspection.get("covers") or []),
        "visual_reference_review": dict(inspection.get("visual_reference_review") or {}),
        "export_url": _run_export_url(case_id, run_id),
        "artifact_inspection_url": f"/workflows/content-production/runs/{case_id}/{run_id}/artifacts/inspect",
    }


def _delivery_review_evidence(*, delivery: dict[str, Any], summary: dict[str, Any]) -> dict[str, Any]:
    inspection = delivery.get("artifact_inspection") if isinstance(delivery.get("artifact_inspection"), dict) else {}
    return {
        "schema_version": 1,
        "case_id": str(delivery.get("case_id") or summary.get("case_id") or ""),
        "run_id": str(delivery.get("run_id") or summary.get("run_id") or ""),
        "ready": bool(delivery.get("ready")),
        "status": str(delivery.get("status") or ""),
        "blocking_reasons": list(delivery.get("blocking_reasons") or []),
        "warning_reasons": list(delivery.get("warning_reasons") or []),
        "proof": dict(delivery.get("proof") or summary.get("proof") or {}),
        "acceptance": dict(delivery.get("acceptance") or summary.get("acceptance") or {}),
        "evaluations": dict(inspection.get("evaluations") or summary.get("evaluations") or {}),
        "image_reference": dict(inspection.get("image_reference") or summary.get("image_reference") or {}),
        "visual_reference_review": dict(
            inspection.get("visual_reference_review")
            or summary.get("visual_reference_review")
            or {}
        ),
        "artifact_counts": dict(inspection.get("artifact_counts") or {}),
        "missing_core_artifacts": list(inspection.get("missing_core_artifacts") or []),
    }


def _run_review_evidence(*, summary: dict[str, Any], inspection: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "case_id": str(summary.get("case_id") or ""),
        "run_id": str(summary.get("run_id") or ""),
        "status": str(summary.get("status") or ""),
        "proof": dict(summary.get("proof") or {}),
        "acceptance": dict(summary.get("acceptance") or {}),
        "evaluations": dict(inspection.get("evaluations") or summary.get("evaluations") or {}),
        "image_reference": dict(inspection.get("image_reference") or summary.get("image_reference") or {}),
        "visual_reference_review": dict(
            inspection.get("visual_reference_review")
            or summary.get("visual_reference_review")
            or {}
        ),
        "artifact_counts": dict(inspection.get("artifact_counts") or {}),
        "missing_core_artifacts": list(inspection.get("missing_core_artifacts") or []),
    }


def _workbench_case(row: dict[str, Any], *, project_root: str | Path) -> dict[str, Any]:
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
    actions = _case_next_actions(
        case_id=case_id,
        status="needs_first_run",
        selection={},
        selected_missing=False,
        selected_run={},
        best_run={},
        target_run={},
        report={},
    )
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
        template_href = f"/experiments/content-production/run-template?case_id={case_id}&human_gate_mode=skip"
        return [
            {
                "action_id": "run_first_experiment",
                "severity": "next_step",
                "label": "Run experiment",
                "message": "Build a backend launch template, resolve missing fields, then run the first content-production experiment for this case.",
                "method": "GET",
                "href": template_href,
                "payload": {"case_id": case_id, "human_gate_mode": "skip"},
                "links": {
                    "run_template": template_href,
                    "preflight": "/workflows/content-production/runs/preflight",
                    "run": "/workflows/content-production/runs",
                },
            }
        ]

    if selected_missing:
        return [
            {
                "action_id": "repair_stale_selection",
                "severity": "blocking",
                "label": "Repair selection",
                "message": "The current case selection points to a run that no longer exists; select the best visible run.",
                "run_id": str(best_run.get("run_id") or ""),
                "method": "POST",
                "href": f"/experiments/content-production/cases/{case_id}/selection",
                "payload": _selection_payload(best_run, decision="selected", reason="replace stale selection"),
            }
        ]

    actions: list[dict[str, Any]] = []
    if status == "promoted" and target_run:
        run_id = str(target_run.get("run_id") or "")
        return [
            {
                "action_id": "export_promoted_run",
                "severity": "next_step",
                "label": "Export run",
                "message": "The selected run has already been promoted; export it for product review or publishing.",
                "run_id": run_id,
                "method": "GET",
                "href": _run_export_url(case_id, run_id),
            },
            {
                "action_id": "inspect_promoted_run",
                "severity": "review",
                "label": "Inspect run",
                "message": "Inspect the promoted run artifacts, proof, and evaluation evidence.",
                "run_id": run_id,
                "method": "GET",
                "href": f"/workflows/content-production/runs/{case_id}/{run_id}/artifacts/inspect",
            },
        ]

    if not selection and best_run:
        actions.append(
            {
                "action_id": "select_best_run",
                "severity": "next_step",
                "label": "Select best run",
                "message": "Persist the backend-selected best run as the current operator selection.",
                "run_id": str(best_run.get("run_id") or ""),
                "method": "POST",
                "href": f"/experiments/content-production/cases/{case_id}/selection",
                "payload": _selection_payload(best_run, decision="selected", reason="backend best run"),
            }
        )

    target_acceptance = str(target_run.get("acceptance_status") or "")
    target_evaluation = str(target_run.get("evaluation_status") or "")
    if status == "ready_to_promote" and target_run:
        actions.append(
            {
                "action_id": "promote_selected_run",
                "severity": "next_step",
                "label": "Promote run",
                "message": "The selected run is accepted and has a passing evaluation; export it for product review or publishing.",
                "run_id": str(target_run.get("run_id") or ""),
                "method": "POST",
                "href": f"/experiments/content-production/cases/{case_id}/promotion",
                "payload": {
                    "run_id": str(target_run.get("run_id") or ""),
                    "reason": "promote accepted run",
                },
            }
        )
    elif target_run and (target_acceptance == "rejected" or target_evaluation in {"blocked", "needs_revision"}):
        actions.extend(_repair_actions(case_id=case_id, target_run=target_run, report=report))
    elif status in {"needs_review", "needs_selection"} and target_run:
        actions.extend(_review_actions(case_id=case_id, target_run=target_run))
    elif status in {"blocked", "selection_rejected"} and target_run:
        actions.extend(_repair_actions(case_id=case_id, target_run=target_run, report=report))

    if not actions and best_run:
        actions.append(
            {
                "action_id": "inspect_best_run",
                "severity": "review",
                "label": "Inspect run",
                "message": "Inspect the strongest visible run and decide whether to evaluate, select, or rerun.",
                "run_id": str(best_run.get("run_id") or ""),
                "method": "GET",
                "href": f"/workflows/content-production/runs/{case_id}/{best_run.get('run_id')}",
            }
        )
    return actions


def _selection_payload(run: dict[str, Any], *, decision: str, reason: str) -> dict[str, Any]:
    run_id = str(run.get("run_id") or "")
    return {
        "run_id": run_id,
        "decision": decision,
        "reviewer": "operator",
        "reason": reason,
    }


def _review_actions(*, case_id: str, target_run: dict[str, Any]) -> list[dict[str, Any]]:
    run_id = str(target_run.get("run_id") or "")
    base = f"/experiments/content-production/cases/{case_id}"
    actions = [
        {
            "action_id": "draft_evaluation",
            "severity": "review",
            "label": "Draft evaluation",
            "message": "Generate a deterministic backend evaluation draft for the target run.",
            "run_id": run_id,
            "method": "POST",
            "href": f"{base}/evaluations/draft",
            "payload": {"run_id": run_id, "reviewer": "operator", "persist": False},
        }
    ]
    if str(target_run.get("evaluation_status") or "") == "pending":
        actions.append(
            {
                "action_id": "record_evaluation",
                "severity": "review",
                "label": "Record evaluation",
                "message": "Persist a manual or automated evaluation decision for the target run.",
                "run_id": run_id,
                "method": "POST",
                "href": f"{base}/evaluations",
                "payload": {"run_id": run_id},
            }
        )
    return actions


def _repair_actions(*, case_id: str, target_run: dict[str, Any], report: dict[str, Any]) -> list[dict[str, Any]]:
    run_id = str(target_run.get("run_id") or "")
    blockers = [
        *[str(item) for item in target_run.get("blocking_checks") or []],
        *[str(item) for item in target_run.get("proof_failed_checks") or []],
    ]
    if (
        "strict_reference_satisfied" in blockers
        or "provider_reference_check_satisfied" in blockers
        or "reference_image_generation_check" in blockers
        or str(target_run.get("reference_status") or "") in {"fallback", "failed_required"}
    ):
        action_id = "check_reference_image_generation" if (
            "provider_reference_check_satisfied" in blockers or "reference_image_generation_check" in blockers
        ) else "fix_reference_transfer"
        href = _reference_repair_href(action_id=action_id, target_run=target_run)
        payload = _reference_repair_payload(action_id=action_id, case_id=case_id, target_run=target_run)
        return [
            {
                "action_id": action_id,
                "severity": "blocking",
                "label": "Check references" if action_id == "check_reference_image_generation" else "Fix references",
                "message": (
                    "Run the session reference-image generation check, then rerun the experiment with strict provider-check evidence."
                    if action_id == "check_reference_image_generation"
                    else "Publish selected images as provider-fetchable references, then rerun the experiment."
                ),
                "run_id": run_id,
                "method": "POST",
                "href": href,
                "payload": payload,
                "blockers": blockers,
            },
            _rerun_action(case_id=case_id, run_id=run_id, blockers=blockers, target_run=target_run),
        ]
    recommendations = [item for item in report.get("recommendations") or [] if isinstance(item, dict)]
    return [
        {
            "action_id": "fix_blockers",
            "severity": "blocking",
            "label": "Fix blockers",
            "message": "Fix the target run blockers before promoting this case.",
            "run_id": run_id,
            "method": "GET",
            "href": f"/workflows/content-production/runs/{case_id}/{run_id}/acceptance",
            "blockers": blockers,
            "recommendation_ids": [str(item.get("action_id") or "") for item in recommendations if item.get("action_id")],
        },
        _rerun_action(case_id=case_id, run_id=run_id, blockers=blockers, target_run=target_run),
    ]


def _reference_repair_href(*, action_id: str, target_run: dict[str, Any]) -> str:
    session_id = str(target_run.get("session_id") or "").strip()
    route = (
        "reference-image-generation-check"
        if action_id == "check_reference_image_generation"
        else "publish-references"
    )
    if session_id:
        return f"/sessions/{session_id}/assets/{route}"
    return f"/sessions/{{session_id}}/assets/{route}"


def _reference_repair_payload(*, action_id: str, case_id: str, target_run: dict[str, Any]) -> dict[str, Any]:
    asset_ids = [str(item) for item in target_run.get("asset_ids") or [] if str(item)]
    run_options = target_run.get("run_options") if isinstance(target_run.get("run_options"), dict) else {}
    backend_public_base_url = str(
        target_run.get("backend_public_base_url") or run_options.get("backend_public_base_url") or ""
    ).strip()
    payload: dict[str, Any] = {"asset_ids": asset_ids}
    if backend_public_base_url:
        payload["backend_public_base_url"] = backend_public_base_url
    if action_id == "check_reference_image_generation":
        try:
            timeout = float(run_options.get("reference_url_probe_timeout") or 3.0)
        except (TypeError, ValueError):
            timeout = 3.0
        payload.update(
            {
                "verify_reference_urls": bool(run_options.get("verify_reference_urls")),
                "reference_url_probe_timeout": timeout,
                "prompt": "Generate a simple product image using the selected session reference image.",
                "size": "1024x1024",
                "metadata": {
                    "source": "content_production_case_next_actions",
                    "case_id": case_id,
                    "run_id": str(target_run.get("run_id") or ""),
                },
            }
        )
    else:
        payload["metadata"] = {
            "source": "content_production_case_next_actions",
            "case_id": case_id,
            "run_id": str(target_run.get("run_id") or ""),
        }
    return payload


def _rerun_action(
    *,
    case_id: str,
    run_id: str,
    blockers: list[str],
    target_run: dict[str, Any] | None = None,
) -> dict[str, Any]:
    target_run = target_run if isinstance(target_run, dict) else {}
    session_id = str(target_run.get("session_id") or "").strip()
    payload: dict[str, Any] = {"run_id": run_id, "human_gate_mode": "skip", "metadata": {"blockers": blockers}}
    if session_id:
        payload["session_id"] = session_id
    return {
        "action_id": "replay_or_rerun",
        "severity": "next_step",
        "label": "Replay run",
        "message": "Replay the target run after fixing blockers, or start a new run with corrected inputs.",
        "run_id": run_id,
        "method": "POST",
        "href": f"/experiments/content-production/cases/{case_id}/replay",
        "payload": payload,
        "blockers": blockers,
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
    run = _report_run(run_summary)
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


def _timeline_events_for_run(summary: dict[str, Any]) -> list[dict[str, Any]]:
    case_id = str(summary.get("case_id") or "")
    run_id = str(summary.get("run_id") or "")
    row = _report_run(summary)
    base = {
        "case_id": case_id,
        "run_id": run_id,
        "workflow_name": str(summary.get("workflow_name") or ""),
        "run_status": str(row.get("status") or ""),
        "acceptance_status": str(row.get("acceptance_status") or ""),
        "proof_status": str(row.get("proof_status") or ""),
        "evaluation_status": str(row.get("evaluation_status") or ""),
        "reference_status": str(row.get("reference_status") or ""),
        "links": dict(row.get("links") or {}),
    }
    events: list[dict[str, Any]] = []
    created_at = str(summary.get("created_at") or "")
    if created_at:
        events.append(
            {
                **base,
                "event_id": f"run_started:{case_id}:{run_id}",
                "event_type": "run_started",
                "timestamp": created_at,
                "title": f"Run started: {run_id}",
            }
        )
    finished_at = str(summary.get("finished_at") or "")
    if finished_at:
        events.append(
            {
                **base,
                "event_id": f"run_finished:{case_id}:{run_id}",
                "event_type": "run_finished",
                "timestamp": finished_at,
                "title": f"Run finished: {run_id}",
            }
        )
    evaluations = summary.get("evaluations") if isinstance(summary.get("evaluations"), dict) else {}
    for evaluation in evaluations.get("items") or []:
        if isinstance(evaluation, dict):
            events.append(_timeline_evaluation_event(evaluation, base=base))
    return events


def _timeline_evaluation_event(evaluation: dict[str, Any], *, base: dict[str, Any]) -> dict[str, Any]:
    evaluation_id = str(evaluation.get("evaluation_id") or "")
    run_id = str(base.get("run_id") or "")
    timestamp = str(evaluation.get("created_at") or "")
    return {
        **base,
        "event_id": evaluation_id or f"evaluation:{base.get('case_id')}:{run_id}:{timestamp}",
        "event_type": "evaluation_recorded",
        "timestamp": timestamp,
        "title": f"Evaluation recorded: {run_id}",
        "evaluation_id": evaluation_id,
        "reviewer": str(evaluation.get("reviewer") or ""),
        "source": str(evaluation.get("source") or ""),
        "status": str(evaluation.get("status") or ""),
        "score": evaluation.get("score"),
        "issue_count": len(evaluation.get("issues") or []),
    }


def _timeline_selection_event(selection: dict[str, Any]) -> dict[str, Any]:
    case_id = str(selection.get("case_id") or "")
    run_id = str(selection.get("run_id") or "")
    return {
        "event_id": str(selection.get("selection_id") or f"selection:{case_id}:{run_id}:{selection.get('selected_at') or ''}"),
        "event_type": "selection_recorded",
        "timestamp": str(selection.get("selected_at") or ""),
        "title": f"Selection recorded: {run_id}",
        "case_id": case_id,
        "run_id": run_id,
        "decision": str(selection.get("decision") or ""),
        "reviewer": str(selection.get("reviewer") or ""),
        "reason": str(selection.get("reason") or ""),
        "matches_report_best": bool(selection.get("matches_report_best")),
        "run_status": str((selection.get("run") or {}).get("status") or ""),
        "acceptance_status": str((selection.get("run") or {}).get("acceptance_status") or ""),
        "links": dict((selection.get("run") or {}).get("links") or {}),
    }


def _timeline_sort_key(event: dict[str, Any]) -> tuple[str, str, str]:
    return (
        str(event.get("timestamp") or ""),
        str(event.get("event_type") or ""),
        str(event.get("event_id") or ""),
    )
