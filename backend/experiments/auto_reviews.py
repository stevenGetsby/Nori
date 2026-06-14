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
    run_health_review = _run_health_review(summary, case_id=case_id, run_id=run_id)
    if run_health_review["issues"] or run_health_review["status"] != "passed":
        reviews.append(run_health_review)
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


def _run_health_review(summary: dict[str, Any], *, case_id: str, run_id: str) -> dict[str, Any]:
    proof = summary.get("proof") if isinstance(summary.get("proof"), dict) else {}
    acceptance = summary.get("acceptance") if isinstance(summary.get("acceptance"), dict) else {}
    checks = [check for check in proof.get("checks", []) if isinstance(check, dict)]
    checks_by_name = {str(check.get("name") or ""): check for check in checks}
    issue_names = _dedupe_strings([
        *[str(name) for name in proof.get("failed_checks", [])],
        *[str(name) for name in proof.get("warning_checks", [])],
        *[str(name) for name in acceptance.get("blocking_checks", [])],
        *[str(name) for name in acceptance.get("warning_checks", [])],
    ])
    issues = [
        _run_health_issue(name, checks_by_name.get(name, {}))
        for name in issue_names
        if name != "evaluation" and name != "evaluation_passed"
    ]
    score = _run_health_score(issues)
    return {
        "review_id": f"review_run_health_{_slug(case_id)}_{_slug(run_id)}",
        "package_id": "",
        "task_id": str((summary.get("input_manifest") or {}).get("task_id") or ""),
        "status": _run_health_status(issues, score),
        "score": score,
        "issues": issues,
        "fix_suggestions": _run_health_suggestions(issues),
        "reviewer": "run_health",
        "metadata": {
            "review_type": "rule_based_run_health",
            "proof_status": str(proof.get("status") or ""),
            "acceptance_status": str(acceptance.get("status") or ""),
            "issue_count": len(issues),
            "severity_counts": _issue_severity_counts(issues),
        },
    }


def _run_health_issue(name: str, check: dict[str, Any]) -> dict[str, Any]:
    severity = _run_health_severity(name, str(check.get("status") or ""))
    message = str(check.get("message") or _run_health_message(name))
    issue = {
        "code": f"run_{name}",
        "severity": severity,
        "field": f"proof.{name}",
        "message": message,
    }
    evidence = _run_health_evidence(check)
    if evidence:
        issue["evidence"] = evidence
    return issue


def _run_health_message(name: str) -> str:
    return {
        "workflow_succeeded": "workflow did not complete successfully",
        "market_evidence": "market evidence is missing",
        "content_package": "content package is missing",
        "content_package_available": "content package is missing",
        "cover_output": "cover output is missing",
        "cover_output_available": "cover output is missing",
        "reference_transfer": "reference transfer is not ready",
        "reference_images_sent": "selected reference images were not sent",
        "reference_image_generation_check": "provider reference-image generation check is not ready",
        "strict_reference_satisfied": "strict reference-image requirement is not satisfied",
        "provider_reference_check_satisfied": "provider reference-image generation check is not satisfied",
        "replay_snapshot": "replay snapshot is missing",
        "replay_snapshot_available": "replay snapshot is missing",
        "export_available": "export endpoint or artifacts are missing",
        "proof_ready": "proof has blocking or warning checks",
        "artifact_catalog_available": "artifact catalog is empty",
    }.get(name, f"run health check needs attention: {name}")


def _run_health_severity(name: str, check_status: str) -> str:
    if check_status == "warning" or name in {"replay_snapshot", "replay_snapshot_available", "export_available", "artifact_catalog_available"}:
        return "medium"
    if name in {
        "workflow_succeeded",
        "market_evidence",
        "content_package",
        "content_package_available",
        "cover_output",
        "cover_output_available",
        "reference_transfer",
        "reference_images_sent",
        "reference_image_generation_check",
        "strict_reference_satisfied",
        "provider_reference_check_satisfied",
        "proof_ready",
    }:
        return "high"
    return "medium"


def _run_health_evidence(check: dict[str, Any]) -> str:
    values = []
    for key in ("artifact_url", "url", "proof_status", "failed_checks", "warning_checks"):
        value = check.get(key)
        if value:
            values.append(f"{key}={value}")
    return "; ".join(values)[:180]


def _run_health_score(issues: list[dict[str, Any]]) -> int:
    score = 100
    for issue in issues:
        severity = str(issue.get("severity") or "")
        if severity == "high":
            score -= 40
        elif severity == "medium":
            score -= 15
        elif severity == "low":
            score -= 5
    return max(0, score)


def _run_health_status(issues: list[dict[str, Any]], score: int) -> str:
    if any(str(issue.get("severity") or "") == "high" for issue in issues) or score < 60:
        return "blocked"
    if issues or score < 85:
        return "needs_revision"
    return "passed"


def _run_health_suggestions(issues: list[dict[str, Any]]) -> list[str]:
    suggestions = []
    for issue in issues:
        code = str(issue.get("code") or "")
        if code in {"run_market_evidence"}:
            suggestions.append("补齐真实 market_evidence 后重新运行实验。")
        elif code in {"run_reference_transfer", "run_reference_images_sent", "run_strict_reference_satisfied"}:
            suggestions.append("修复 OSS/backend public URL/reference 传输后重新运行严格参考图实验。")
        elif code in {"run_content_package", "run_content_package_available"}:
            suggestions.append("重新运行内容生成，确保 content_package.json 写入成功。")
        elif code in {"run_cover_output", "run_cover_output_available"}:
            suggestions.append("重新运行封面生成，确保 cover 输出可下载。")
        elif code in {"run_replay_snapshot", "run_replay_snapshot_available"}:
            suggestions.append("补齐 replay_request.json，保证实验可复现。")
        elif code == "run_export_available":
            suggestions.append("检查 artifact catalog 和 export endpoint，保证评审包可交付。")
        elif code == "run_workflow_succeeded":
            suggestions.append("先修复 workflow 失败原因，再进入内容质量评估。")
        else:
            suggestions.append("按 run health issue 修复实验证据后重新评估。")
    return _dedupe_strings(suggestions)


def _issue_severity_counts(issues: list[dict[str, Any]]) -> dict[str, int]:
    counts = {"high": 0, "medium": 0, "low": 0}
    for issue in issues:
        severity = str(issue.get("severity") or "")
        if severity in counts:
            counts[severity] += 1
    return counts


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
