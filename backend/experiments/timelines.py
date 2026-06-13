"""Case-level timelines for content-production experiments."""
from __future__ import annotations

from .common import (
    Any,
    PROJECT_ROOT,
    Path,
    _content_case_dir,
)
from .models import ContentCaseRef
from .repositories import ContentProductionExperimentRepository
from .runs import content_production_comparison_run, content_production_count_by, list_content_production_runs


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
    selection = _case_selection_payload(project_root=project_root, case_id=case_id)
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
            "event_type_counts": content_production_count_by(events, "event_type"),
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


def _case_selection_payload(*, project_root: str | Path, case_id: str) -> dict[str, Any]:
    repository = ContentProductionExperimentRepository(project_root)
    data = repository.read_case_selection(ContentCaseRef(case_id=case_id))
    history = data.get("history") if isinstance(data.get("history"), list) else []
    return {
        "schema_version": int(data.get("schema_version") or 1),
        "case_id": str(data.get("case_id") or case_id),
        "history": [dict(item) for item in history if isinstance(item, dict)],
    }


def _timeline_events_for_run(summary: dict[str, Any]) -> list[dict[str, Any]]:
    case_id = str(summary.get("case_id") or "")
    run_id = str(summary.get("run_id") or "")
    row = _timeline_run_row(summary)
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


def _timeline_run_row(summary: dict[str, Any]) -> dict[str, Any]:
    row = content_production_comparison_run(summary)
    case_id = str(summary.get("case_id") or "")
    run_id = str(row.get("run_id") or "")
    proof = summary.get("proof") if isinstance(summary.get("proof"), dict) else {}
    base = f"/workflows/content-production/runs/{case_id}/{run_id}" if case_id and run_id else ""
    return {
        "status": row.get("status"),
        "acceptance_status": row.get("acceptance_status"),
        "proof_status": str(proof.get("status") or ""),
        "evaluation_status": row.get("evaluation_status"),
        "reference_status": row.get("reference_status"),
        "links": {
            "self": base,
            "acceptance": f"{base}/acceptance" if base else "",
            "evaluations": f"{base}/evaluations" if base else "",
            "evaluation_draft": f"{base}/evaluations/draft" if base else "",
            "replay": f"{base}/replay" if base else "",
            "export": f"{base}/export" if base else "",
        },
    }


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
