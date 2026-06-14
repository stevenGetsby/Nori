"""Presenter helpers for experiment jobs and content-production run results."""
from __future__ import annotations

from typing import Any


def enrich_content_run_result(
    result: dict[str, Any] | None,
    *,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Attach backend-owned follow-up links and actions to a run result."""

    if not isinstance(result, dict):
        return None
    enriched = dict(result)
    links = dict(enriched.get("links") or {})
    links.update(content_run_links(metadata=dict(metadata or {}), result=enriched))
    if links:
        enriched["links"] = links
    actions = _content_run_actions(result=enriched, links=links)
    if actions:
        enriched["actions"] = actions
    return enriched


def content_run_links(*, metadata: dict[str, Any], result: dict[str, Any] | None) -> dict[str, str]:
    data = result if isinstance(result, dict) else {}
    manifest = data.get("experiment_manifest") if isinstance(data.get("experiment_manifest"), dict) else {}
    experiment = manifest.get("experiment") if isinstance(manifest.get("experiment"), dict) else {}
    input_manifest = data.get("input_manifest") if isinstance(data.get("input_manifest"), dict) else {}
    case_id = str(data.get("case_id") or experiment.get("case_id") or input_manifest.get("case_id") or metadata.get("case_id") or "").strip()
    run_id = str(data.get("run_id") or experiment.get("run_id") or "").strip()
    if not case_id or not run_id:
        return {}
    base = f"/workflows/content-production/runs/{case_id}/{run_id}"
    return {
        "run": base,
        "acceptance": f"{base}/acceptance",
        "evaluations": f"{base}/evaluations",
        "evaluation_draft": f"{base}/evaluations/draft",
        "replay": f"{base}/replay",
        "export": f"{base}/export",
        "inspect_artifacts": f"{base}/artifacts/inspect",
        "case_compare": f"/experiments/content-production/cases/{case_id}/compare",
        "case_next_actions": f"/experiments/content-production/cases/{case_id}/next-actions",
        "case_selected_run": f"/experiments/content-production/cases/{case_id}/selected-run",
        "case_evaluation_draft": f"/experiments/content-production/cases/{case_id}/evaluations/draft",
        "case_evaluations": f"/experiments/content-production/cases/{case_id}/evaluations",
        "case_replay": f"/experiments/content-production/cases/{case_id}/replay",
        "case_promotion": f"/experiments/content-production/cases/{case_id}/promotion",
        "case_delivery": f"/experiments/content-production/cases/{case_id}/delivery",
        "case_timeline": f"/experiments/content-production/cases/{case_id}/timeline",
        "case_export": f"/experiments/content-production/cases/{case_id}/export",
    }


def job_actions(
    *,
    status: str,
    links: dict[str, str],
    result: dict[str, Any] | None,
    cancel_requested: bool = False,
) -> list[dict[str, Any]]:
    actions: list[dict[str, Any]] = []
    if status in {"queued", "running", "cancelling"} and links.get("self"):
        actions.append(
            {
                "action_id": "poll_job",
                "severity": "next_step",
                "method": "GET",
                "href": links["self"],
                "message": "Poll this background experiment job until it reaches a terminal status.",
            }
        )
    if status in {"queued", "running"} and not cancel_requested and links.get("cancel"):
        actions.append(
            {
                "action_id": "cancel_job",
                "severity": "optional",
                "method": "POST",
                "href": links["cancel"],
                "payload": {"reason": "operator requested cancellation"},
                "message": "Request cancellation for this background experiment job.",
            }
        )
    if isinstance(result, dict):
        actions.extend(list(result.get("actions") or []))
    return actions


def _content_run_actions(*, result: dict[str, Any], links: dict[str, str]) -> list[dict[str, Any]]:
    run_id = str(result.get("run_id") or "").strip()
    if not run_id:
        return []
    status = str(result.get("status") or "").strip()
    action_ids = (
        [
            "inspect_failure_artifacts",
            "replay_run",
            "case_next_actions",
            "export_run",
        ]
        if status == "failed"
        else [
            "inspect_run",
            "draft_evaluation",
            "case_next_actions",
            "export_run",
            "replay_run",
            "promote_run",
        ]
    )
    actions_by_id = {
        "inspect_run": {
            "action_id": "inspect_run",
            "severity": "next_step",
            "method": "GET",
            "href": links.get("inspect_artifacts", ""),
            "message": "Inspect generated artifacts, cover previews, proof, acceptance, and evaluation state.",
        },
        "inspect_failure_artifacts": {
            "action_id": "inspect_failure_artifacts",
            "severity": "next_step",
            "method": "GET",
            "href": links.get("inspect_artifacts", ""),
            "message": "Inspect failure artifacts and manifests before deciding whether to replay.",
        },
        "draft_evaluation": {
            "action_id": "draft_evaluation",
            "severity": "next_step",
            "method": "POST",
            "href": links.get("case_evaluation_draft", ""),
            "payload": {"run_id": run_id, "reviewer": "operator", "persist": False},
            "message": "Build a review draft for this run without hard-coding the run-level URL.",
        },
        "case_next_actions": {
            "action_id": "case_next_actions",
            "severity": "next_step",
            "method": "GET",
            "href": links.get("case_next_actions", ""),
            "message": "Ask the backend for the current case-level decision plan.",
        },
        "export_run": {
            "action_id": "export_run",
            "severity": "optional",
            "method": "GET",
            "href": links.get("export", ""),
            "message": "Download a review/archive bundle for this run.",
        },
        "replay_run": {
            "action_id": "replay_run",
            "severity": "optional",
            "method": "POST",
            "href": links.get("case_replay", ""),
            "payload": {"run_id": run_id, "human_gate_mode": "skip"},
            "message": "Replay this run from its stored request snapshot.",
        },
        "promote_run": {
            "action_id": "promote_run",
            "severity": "optional",
            "method": "POST",
            "href": links.get("case_promotion", ""),
            "payload": {
                "run_id": run_id,
                "reviewer": "operator",
                "reason": "Promote the accepted experiment run.",
                "allow_unaccepted": False,
            },
            "message": "Promote this run after acceptance/evaluation confirms it is ready.",
        },
    }
    return [actions_by_id[action_id] for action_id in action_ids if actions_by_id[action_id].get("href")]


__all__ = ["content_run_links", "enrich_content_run_result", "job_actions"]
