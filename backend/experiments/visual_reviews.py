"""Visual-reference review helpers for content-production runs."""
from __future__ import annotations

from .common import Any, _slug


def visual_reference_review(summary: dict[str, Any]) -> dict[str, Any]:
    """Build a deterministic review panel for human visual-reference checks."""

    image_reference = summary.get("image_reference") if isinstance(summary.get("image_reference"), dict) else {}
    input_manifest = summary.get("input_manifest") if isinstance(summary.get("input_manifest"), dict) else {}
    run_options = input_manifest.get("run_options") if isinstance(input_manifest.get("run_options"), dict) else {}
    evaluations = summary.get("evaluations") if isinstance(summary.get("evaluations"), dict) else {}
    evaluation = evaluations.get("summary") if isinstance(evaluations.get("summary"), dict) else {}
    trace = [dict(item) for item in image_reference.get("trace") or [] if isinstance(item, dict)]
    cover_urls = list(summary.get("cover_urls") or [])
    required = bool(image_reference.get("required") or run_options.get("require_image_references"))
    selected_count = int(image_reference.get("selected_count") or len(trace) or 0)
    sent = bool(image_reference.get("sent"))
    evaluation_status = str(evaluation.get("status") or "pending")
    applicable = required or selected_count > 0
    checks = [
        _visual_reference_check(
            "references_selected",
            "passed" if selected_count > 0 else ("failed" if required else "not_applicable"),
            "reference images were selected" if selected_count > 0 else "no reference images were selected",
            selected_count=selected_count,
        ),
        _visual_reference_check(
            "reference_trace_available",
            "passed" if trace else ("failed" if required else "not_applicable"),
            "per-reference trace is available" if trace else "per-reference trace is missing",
            trace_count=len(trace),
        ),
        _visual_reference_check(
            "references_sent_to_gateway",
            "passed" if sent else ("failed" if required else "not_applicable"),
            "selected references were sent to the image gateway" if sent else "selected references were not sent",
            sent=sent,
            reference_status=str(image_reference.get("status") or ""),
        ),
        _visual_reference_check(
            "cover_output_available",
            "passed" if cover_urls else ("failed" if applicable else "not_applicable"),
            "cover output is available" if cover_urls else "cover output is missing",
            cover_count=len(cover_urls),
        ),
        _visual_reference_check(
            "human_visual_match_review",
            "passed" if evaluation_status == "passed" else ("pending" if applicable else "not_applicable"),
            "latest evaluation passed" if evaluation_status == "passed" else "human visual match review is still required",
            evaluation_status=evaluation_status,
            latest_evaluation_id=str(evaluation.get("latest_evaluation_id") or ""),
        ),
    ]
    failed = [check for check in checks if check["status"] == "failed"]
    pending = [check for check in checks if check["status"] == "pending"]
    status = "not_applicable"
    if failed:
        status = "blocked"
    elif applicable and pending:
        status = "needs_human_review"
    elif applicable:
        status = "passed"
    return {
        "schema_version": 1,
        "status": status,
        "required": required,
        "human_review_required": status in {"blocked", "needs_human_review"},
        "selected_count": selected_count,
        "sent": sent,
        "trace_count": len(trace),
        "provider_fetchable_count": int(
            image_reference.get("trace_provider_fetchable_count")
            or sum(1 for item in trace if item.get("provider_fetchable"))
        ),
        "cover_count": len(cover_urls),
        "cover_urls": cover_urls,
        "reference_trace": trace,
        "checks": checks,
        "evaluation_status": evaluation_status,
        "review_questions": [
            "Does the generated cover preserve the visible brand/product/IP cues from the uploaded references?",
            "Does the cover use the references as visual source material instead of only following the text prompt?",
            "Are important user-provided assets missing, distorted, or replaced by unrelated imagery?",
        ],
    }


def visual_reference_review_for_evaluation(summary: dict[str, Any], *, case_id: str, run_id: str) -> dict[str, Any]:
    visual = summary.get("visual_reference_review") if isinstance(summary.get("visual_reference_review"), dict) else {}
    status = str(visual.get("status") or "")
    if status == "not_applicable" or not status:
        return {}
    issue = _visual_reference_issue(visual) if status != "passed" else {}
    issues = [issue] if issue else []
    return {
        "review_id": f"review_visual_reference_{_slug(case_id)}_{_slug(run_id)}",
        "package_id": "",
        "task_id": str((summary.get("input_manifest") or {}).get("task_id") or ""),
        "status": "passed" if status == "passed" else ("blocked" if status == "blocked" else "pending"),
        "score": 100 if status == "passed" else (45 if status == "blocked" else 75),
        "issues": issues,
        "fix_suggestions": _visual_reference_suggestions(visual),
        "reviewer": "visual_reference",
        "metadata": {
            "review_type": "rule_based_visual_reference",
            "visual_reference_status": status,
            "selected_count": int(visual.get("selected_count") or 0),
            "sent": bool(visual.get("sent")),
            "trace_count": int(visual.get("trace_count") or 0),
            "provider_fetchable_count": int(visual.get("provider_fetchable_count") or 0),
            "cover_count": int(visual.get("cover_count") or 0),
            "review_questions": list(visual.get("review_questions") or []),
        },
    }


def _visual_reference_check(name: str, status: str, message: str, **extra: Any) -> dict[str, Any]:
    data = {"name": name, "status": status, "message": message}
    data.update({key: value for key, value in extra.items() if value is not None and value != "" and value != []})
    return data


def _visual_reference_issue(visual: dict[str, Any]) -> dict[str, Any]:
    status = str(visual.get("status") or "")
    if status == "blocked":
        severity = "high"
        message = "Visual reference evidence is blocked; selected references or cover output are missing."
    else:
        severity = "medium"
        message = "Human visual match review is required before accepting reference-driven cover quality."
    return {
        "code": f"visual_reference_{status or 'review_required'}",
        "severity": severity,
        "field": "visual_reference_review",
        "message": message,
        "evidence": (
            f"selected={int(visual.get('selected_count') or 0)}; "
            f"sent={bool(visual.get('sent'))}; "
            f"trace={int(visual.get('trace_count') or 0)}; "
            f"covers={int(visual.get('cover_count') or 0)}"
        ),
    }


def _visual_reference_suggestions(visual: dict[str, Any]) -> list[str]:
    status = str(visual.get("status") or "")
    if status == "passed":
        return []
    if status == "blocked":
        return ["先修复参考图传输、trace 或 cover 输出，再进入视觉参考验收。"]
    return ["人工对照 reference trace 和封面图，确认品牌/IP/产品视觉元素是否被实际吸收。"]
