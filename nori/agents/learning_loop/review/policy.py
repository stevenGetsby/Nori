"""Rule policy helpers for ContentPackage review."""
from __future__ import annotations

import re
from typing import Any

from nori.agents.content_generation.schemas import ContentPackage
from nori.core import ClientBrief, ContentTask
from nori.shared.normalization import string_list as _shared_string_list

from .scoring import (
    issue,
    score_issues,
    severity_counts,
    status_for_issues,
    suggestions,
)
from ..schemas import ComplianceReview

ABSOLUTE_CLAIM_PATTERNS = (
    "保证",
    "一定",
    "100%",
    "百分百",
    "全网第一",
    "最便宜",
    "立刻见效",
    "马上见效",
    "治疗",
    "疗效",
    "官方认证",
)


def compliance_issues(package: ContentPackage, brief: ClientBrief) -> list[dict[str, Any]]:
    """Return rule-based text compliance issues for a package."""
    issues: list[dict[str, Any]] = []
    if not package.title.strip():
        issues.append(issue("missing_title", "high", "title", "缺少标题"))
    if not package.body.strip():
        issues.append(issue("missing_body", "high", "body", "缺少正文"))
    if package.platform == "xhs" and len(package.title.strip()) > 30:
        issues.append(issue("xhs_title_too_long", "medium", "title", "小红书标题超过 30 字", package.title[:60]))
    if len(package.body.strip()) > 1000:
        issues.append(issue("body_too_long", "medium", "body", "正文超过当前图文流建议长度", str(len(package.body))))

    for taboo in string_list(brief.taboos):
        if taboo and contains(package.title, taboo) or taboo and contains(package.body, taboo):
            issues.append(issue("client_taboo_term", "high", "body", f"命中客户禁忌词：{taboo}", taboo))

    for pattern in ABSOLUTE_CLAIM_PATTERNS:
        if contains(package.title, pattern) or contains(package.body, pattern):
            issues.append(issue("unsupported_absolute_claim", "high", "body", f"疑似绝对化或高风险承诺：{pattern}", pattern))

    validation = note_validation(package)
    if validation.get("status") == "needs_human_review":
        evidence = "; ".join(string_list(validation.get("issues")))[:160]
        issues.append(issue("note_maker_needs_human_review", "medium", "prompts.note_draft.validation", "NoteMaker 标记需要人工审核", evidence))
    return issues


def consistency_issues(
    package: ContentPackage,
    task: ContentTask | None,
    brief: ClientBrief,
) -> list[dict[str, Any]]:
    """Return rule-based consistency issues for task, package, and cover prompt."""
    issues: list[dict[str, Any]] = []
    if task:
        if package.task_id and task.task_id and package.task_id != task.task_id:
            issues.append(issue("task_id_mismatch", "high", "task_id", "Package task_id 与任务不一致", f"{package.task_id} != {task.task_id}"))
        if package.platform and task.platform and package.platform != task.platform:
            issues.append(issue("platform_mismatch", "high", "platform", "Package platform 与任务不一致", f"{package.platform} != {task.platform}"))
        if task.topic and not any_keyword_in_text(keywords(task.topic), f"{package.title}\n{package.body}"):
            issues.append(issue("topic_not_reflected", "medium", "title/body", "标题或正文没有体现任务主题", task.topic))
        if task.objective and not any_keyword_in_text(keywords(task.objective), package.body):
            issues.append(issue("objective_not_reflected", "medium", "body", "正文没有体现任务目标", task.objective))
        for asset in missing_required_assets(task, package):
            issues.append(issue("required_asset_not_tracked", "low", "material_usage", f"任务要求素材未进入 material_usage：{asset}", asset))

    cover_prompt = cover_prompt_text(package)
    cover_title = str(task.brief.get("cover_title") or "").strip() if task else ""
    expected_cover_terms = cover_title or package.title
    if cover_prompt and expected_cover_terms and not any_keyword_in_text(keywords(expected_cover_terms), cover_prompt):
        issues.append(issue("cover_prompt_not_aligned", "medium", "prompts.cover_result.prompt", "封面 prompt 没有体现标题或封面标题", expected_cover_terms))

    if brief.brand_name and not contains(f"{package.title}\n{package.body}\n{cover_prompt}", brief.brand_name):
        issues.append(issue("brand_not_reflected", "low", "title/body", "客户品牌名没有出现在内容或封面 prompt 中", brief.brand_name))
    return issues


def build_review(
    *,
    package: ContentPackage,
    task: ContentTask | None,
    reviewer: str,
    issues: list[dict[str, Any]],
    metadata: dict[str, Any],
) -> ComplianceReview:
    """Build a ComplianceReview from normalized policy issues."""
    score = score_issues(issues)
    return ComplianceReview(
        review_id=f"review_{reviewer}_{package.package_id or package.task_id or 'package'}",
        package_id=package.package_id,
        task_id=package.task_id or (task.task_id if task else ""),
        status=status_for_issues(issues, score),
        score=score,
        issues=issues,
        fix_suggestions=suggestions(issues),
        reviewer=reviewer,
        metadata={
            **metadata,
            "issue_count": len(issues),
            "severity_counts": severity_counts(issues),
        },
    )


def note_validation(package: ContentPackage) -> dict[str, Any]:
    draft = package.prompts.get("note_draft")
    if not isinstance(draft, dict):
        return {}
    validation = draft.get("validation")
    return validation if isinstance(validation, dict) else {}


def cover_prompt_text(package: ContentPackage) -> str:
    cover = package.prompts.get("cover_result")
    if not isinstance(cover, dict):
        return ""
    return str(cover.get("prompt") or "")


def missing_required_assets(task: ContentTask, package: ContentPackage) -> list[str]:
    represented = " ".join(
        str(value)
        for row in package.material_usage
        for value in row.values()
    )
    missing = []
    for item in task.required_assets:
        if item and item not in represented:
            missing.append(item)
    return missing


def contains(text: str, needle: str) -> bool:
    return needle.strip().lower() in text.lower()


def keywords(text: str) -> list[str]:
    raw = re.split(r"[\s,，。；;、｜|/]+", text)
    output = [item.strip() for item in raw if len(item.strip()) >= 2]
    if not output and text.strip():
        output = [text.strip()]
    return output


def any_keyword_in_text(values: list[str], text: str) -> bool:
    return any(contains(text, keyword) for keyword in values)


def string_list(value: Any) -> list[str]:
    return _shared_string_list(value)
