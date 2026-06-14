"""Action payload builders for content-production experiment cases."""
from __future__ import annotations

from .common import Any
from .artifacts import _run_export_url


def first_run_action(*, case_id: str) -> dict[str, Any]:
    template_href = f"/experiments/content-production/run-template?case_id={case_id}&human_gate_mode=skip"
    return {
        "action_id": "run_first_experiment",
        "severity": "next_step",
        "label": "Run experiment",
        "message": (
            "Build a backend launch template, resolve missing fields, then run the first "
            "content-production experiment for this case."
        ),
        "method": "GET",
        "href": template_href,
        "payload": {"case_id": case_id, "human_gate_mode": "skip"},
        "links": {
            "run_template": template_href,
            "preflight": "/workflows/content-production/runs/preflight",
            "run": "/workflows/content-production/runs",
        },
    }


def stale_selection_repair_action(*, case_id: str, best_run: dict[str, Any]) -> dict[str, Any]:
    return {
        "action_id": "repair_stale_selection",
        "severity": "blocking",
        "label": "Repair selection",
        "message": "The current case selection points to a run that no longer exists; select the best visible run.",
        "run_id": str(best_run.get("run_id") or ""),
        "method": "POST",
        "href": f"/experiments/content-production/cases/{case_id}/selection",
        "payload": selection_action_payload(best_run, decision="selected", reason="replace stale selection"),
    }


def promoted_run_actions(*, case_id: str, target_run: dict[str, Any]) -> list[dict[str, Any]]:
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


def select_best_run_action(*, case_id: str, best_run: dict[str, Any]) -> dict[str, Any]:
    return {
        "action_id": "select_best_run",
        "severity": "next_step",
        "label": "Select best run",
        "message": "Persist the backend-selected best run as the current operator selection.",
        "run_id": str(best_run.get("run_id") or ""),
        "method": "POST",
        "href": f"/experiments/content-production/cases/{case_id}/selection",
        "payload": selection_action_payload(best_run, decision="selected", reason="backend best run"),
    }


def promote_selected_run_action(*, case_id: str, target_run: dict[str, Any]) -> dict[str, Any]:
    run_id = str(target_run.get("run_id") or "")
    return {
        "action_id": "promote_selected_run",
        "severity": "next_step",
        "label": "Promote run",
        "message": "The selected run is accepted and has a passing evaluation; export it for product review or publishing.",
        "run_id": run_id,
        "method": "POST",
        "href": f"/experiments/content-production/cases/{case_id}/promotion",
        "payload": {
            "run_id": run_id,
            "reason": "promote accepted run",
        },
    }


def inspect_best_run_action(*, case_id: str, best_run: dict[str, Any]) -> dict[str, Any]:
    return {
        "action_id": "inspect_best_run",
        "severity": "review",
        "label": "Inspect run",
        "message": "Inspect the strongest visible run and decide whether to evaluate, select, or rerun.",
        "run_id": str(best_run.get("run_id") or ""),
        "method": "GET",
        "href": f"/workflows/content-production/runs/{case_id}/{best_run.get('run_id')}",
    }


def selection_action_payload(run: dict[str, Any], *, decision: str, reason: str) -> dict[str, Any]:
    run_id = str(run.get("run_id") or "")
    return {
        "run_id": run_id,
        "decision": decision,
        "reviewer": "operator",
        "reason": reason,
    }


def case_review_actions(*, case_id: str, target_run: dict[str, Any]) -> list[dict[str, Any]]:
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


def case_repair_actions(*, case_id: str, target_run: dict[str, Any], report: dict[str, Any]) -> list[dict[str, Any]]:
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
                    "Run the session reference-image generation check, then rerun the experiment with strict "
                    "provider-check evidence."
                    if action_id == "check_reference_image_generation"
                    else "Publish selected images as provider-fetchable references, then rerun the experiment."
                ),
                "run_id": run_id,
                "method": "POST",
                "href": href,
                "payload": payload,
                "blockers": blockers,
            },
            rerun_action(case_id=case_id, run_id=run_id, blockers=blockers, target_run=target_run),
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
        rerun_action(case_id=case_id, run_id=run_id, blockers=blockers, target_run=target_run),
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


def rerun_action(
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
