"""Automatic review gate and evaluation-draft projection helpers."""
from __future__ import annotations

from .common import (
    Any,
    ClientBrief,
    ContentTask,
    IntentContract,
    Path,
    _dedupe_strings,
    _dict_list,
    _read_json,
    _slug,
    _string_list,
    importlib,
)
from .run_health import run_health_review
from .visual_reviews import visual_reference_review_for_evaluation


def auto_evaluation_draft(
    run_dir: Path,
    *,
    summary: dict[str, Any],
    case_id: str,
    run_id: str,
    reviewer: str,
    metadata: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    package_data = _read_json(run_dir / "content_package.json")
    input_manifest = summary.get("input_manifest") if isinstance(summary.get("input_manifest"), dict) else {}
    replay_request = _read_json(run_dir / "replay_request.json")
    experiment_manifest = summary.get("experiment_manifest") if isinstance(summary.get("experiment_manifest"), dict) else {}
    task = _auto_review_task(
        package_data=package_data,
        input_manifest=input_manifest,
        replay_request=replay_request,
        experiment_manifest=experiment_manifest,
        case_id=case_id,
        run_id=run_id,
    )
    brief = _auto_review_brief(
        replay_request=replay_request,
        experiment_manifest=experiment_manifest,
        input_manifest=input_manifest,
    )
    contract = IntentContract.from_brief_and_task(
        brief,
        task,
        contract_id=f"intent_{_slug(case_id)}_{_slug(run_id)}",
    )
    if not package_data:
        package_data = {"package_id": "", "task_id": task.task_id, "platform": task.platform}
    reviews = [
        review.to_dict()
        for review in _review_content_package(
            package_data,
            task=task,
            client_brief=brief,
            intent_contract=contract,
        )
    ]
    health_review = run_health_review(summary, case_id=case_id, run_id=run_id)
    if health_review["issues"] or health_review["status"] != "passed":
        reviews.append(health_review)
    visual_review = visual_reference_review_for_evaluation(summary, case_id=case_id, run_id=run_id)
    if visual_review:
        reviews.append(visual_review)
    draft = _evaluation_draft_from_reviews(
        reviews,
        reviewer=reviewer,
        metadata={
            "source": "backend.auto_review_gate",
            "case_id": case_id,
            "run_id": run_id,
            "review_count": len(reviews),
            "reviewers": [str(row.get("reviewer") or "") for row in reviews],
            "content_package_available": bool(_read_json(run_dir / "content_package.json")),
            "intent_contract": contract.to_dict(),
            **metadata,
        },
    )
    context = {
        "content_package_available": bool(_read_json(run_dir / "content_package.json")),
        "task": task.to_dict(),
        "client_brief": brief.to_dict(),
        "intent_contract": contract.to_dict(),
        "visual_reference_review": dict(summary.get("visual_reference_review") or {}),
    }
    return draft, reviews, context


def _review_content_package(package: dict[str, Any], **kwargs: Any) -> list[Any]:
    review_module = importlib.import_module("nori.agents.learning_loop.review")
    return review_module.review_content_package(package, **kwargs)


def _auto_review_task(
    *,
    package_data: dict[str, Any],
    input_manifest: dict[str, Any],
    replay_request: dict[str, Any],
    experiment_manifest: dict[str, Any],
    case_id: str,
    run_id: str,
) -> ContentTask:
    inputs = experiment_manifest.get("inputs") if isinstance(experiment_manifest.get("inputs"), dict) else {}
    config = replay_request.get("config") if isinstance(replay_request.get("config"), dict) else {}
    brief = input_manifest.get("brief") if isinstance(input_manifest.get("brief"), dict) else {}
    task_id = (
        str(package_data.get("task_id") or "")
        or str(input_manifest.get("task_id") or "")
        or str((experiment_manifest.get("session") or {}).get("task_id") or "")
        or f"{case_id}:{run_id}"
    )
    topic = str(config.get("topic") or replay_request.get("goal") or package_data.get("title") or case_id)
    objective = str(replay_request.get("goal") or config.get("goals") or "")
    if isinstance(config.get("goals"), list):
        objective = "；".join(str(item) for item in config["goals"] if str(item).strip())
    assets = inputs.get("assets") if isinstance(inputs.get("assets"), list) else input_manifest.get("assets")
    required_assets = [
        str(row.get("filename") or row.get("asset_id") or row.get("path") or "")
        for row in (assets or [])
        if isinstance(row, dict) and str(row.get("filename") or row.get("asset_id") or row.get("path") or "").strip()
    ]
    return ContentTask(
        task_id=task_id,
        title=str(package_data.get("title") or topic or case_id),
        platform=str(package_data.get("platform") or config.get("platform") or replay_request.get("platform") or "xhs"),
        content_type=str(config.get("content_type") or "note"),
        topic=topic,
        objective=objective,
        brief={
            "brief_sha256": str(brief.get("sha256") or ""),
            "cover_title": str((package_data.get("prompts") or {}).get("cover_title") or ""),
            "must_include": _auto_review_must_include(config=config, case_id=case_id),
        },
        required_assets=required_assets,
        package_id=str(package_data.get("package_id") or ""),
        metadata={"case_id": case_id, "run_id": run_id},
    )


def _auto_review_brief(
    *,
    replay_request: dict[str, Any],
    experiment_manifest: dict[str, Any],
    input_manifest: dict[str, Any],
) -> ClientBrief:
    config = replay_request.get("config") if isinstance(replay_request.get("config"), dict) else {}
    metadata = input_manifest.get("metadata") if isinstance(input_manifest.get("metadata"), dict) else {}
    inputs = experiment_manifest.get("inputs") if isinstance(experiment_manifest.get("inputs"), dict) else {}
    return ClientBrief(
        client_name=str(config.get("client_name") or metadata.get("client_name") or ""),
        brand_name=str(config.get("brand_name") or metadata.get("brand_name") or ""),
        platform=str(config.get("platform") or replay_request.get("platform") or "xhs"),
        goals=_string_list(config.get("goals")) or _string_list(replay_request.get("goal")),
        audience=_string_list(config.get("target_audience")),
        positioning_notes=_string_list(config.get("positioning_notes")),
        constraints=_string_list(config.get("constraints")),
        taboos=_string_list(config.get("taboos")),
        source_materials=_dict_list(inputs.get("assets")),
        context={
            "brief_text_present": bool(str(replay_request.get("brief_text") or "").strip()),
            "market_evidence": dict(inputs.get("market_evidence") or input_manifest.get("market_evidence") or {}),
        },
    )


def _auto_review_must_include(*, config: dict[str, Any], case_id: str) -> list[str]:
    values = [
        str(config.get("brand_name") or ""),
        str(config.get("topic") or ""),
        str(case_id or ""),
    ]
    return _dedupe_strings([value for value in values if value])


def _evaluation_draft_from_reviews(
    reviews: list[dict[str, Any]],
    *,
    reviewer: str,
    metadata: dict[str, Any],
) -> dict[str, Any]:
    status = _aggregate_review_status(reviews)
    scores = [int(row.get("score")) for row in reviews if isinstance(row.get("score"), int)]
    issues = [
        {
            **issue,
            "reviewer": str(review.get("reviewer") or ""),
            "review_status": str(review.get("status") or ""),
        }
        for review in reviews
        for issue in review.get("issues", [])
        if isinstance(issue, dict)
    ]
    metrics = {
        "review_count": len(reviews),
        "scores_by_reviewer": {
            str(review.get("reviewer") or f"review_{index}"): review.get("score")
            for index, review in enumerate(reviews, start=1)
        },
        "status_by_reviewer": {
            str(review.get("reviewer") or f"review_{index}"): str(review.get("status") or "")
            for index, review in enumerate(reviews, start=1)
        },
        "issue_count": len(issues),
        "severity_counts": _aggregate_review_severity_counts(reviews),
    }
    suggestions = _dedupe_strings([
        str(item)
        for review in reviews
        for item in review.get("fix_suggestions", [])
        if str(item).strip()
    ])
    return {
        "reviewer": reviewer or "auto_review_gate",
        "source": "auto",
        "status": status,
        "score": min(scores) if scores else 0,
        "notes": _auto_evaluation_notes(status=status, issue_count=len(issues), suggestions=suggestions),
        "issues": issues,
        "metrics": metrics,
        "metadata": metadata,
    }


def _aggregate_review_status(reviews: list[dict[str, Any]]) -> str:
    statuses = [str(row.get("status") or "pending") for row in reviews]
    if any(status == "blocked" for status in statuses):
        return "blocked"
    if any(status == "needs_revision" for status in statuses):
        return "needs_revision"
    if statuses and all(status == "passed" for status in statuses):
        return "passed"
    return "pending"


def _aggregate_review_severity_counts(reviews: list[dict[str, Any]]) -> dict[str, int]:
    counts = {"high": 0, "medium": 0, "low": 0}
    for review in reviews:
        metadata = review.get("metadata") if isinstance(review.get("metadata"), dict) else {}
        severity_counts = metadata.get("severity_counts") if isinstance(metadata.get("severity_counts"), dict) else {}
        for key in counts:
            counts[key] += int(severity_counts.get(key) or 0)
    return counts


def _auto_evaluation_notes(*, status: str, issue_count: int, suggestions: list[str]) -> str:
    if status == "passed":
        return "Auto review gate passed with no blocking issues."
    prefix = f"Auto review gate found {issue_count} issue(s); status={status}."
    if suggestions:
        return f"{prefix} Top suggestion: {suggestions[0]}"
    return prefix


__all__ = ["auto_evaluation_draft"]
