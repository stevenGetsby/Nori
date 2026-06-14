"""Tests for content-review scoring and issue helpers."""

from __future__ import annotations

from nori.agents.learning_loop.review import scoring as content_review_scoring


def test_issue_truncates_evidence_and_omits_empty_evidence():
    no_evidence = content_review_scoring.issue("missing_title", "high", "title", "缺少标题")
    with_evidence = content_review_scoring.issue("unsupported", "high", "body", "高风险", "x" * 220)

    assert no_evidence == {
        "code": "missing_title",
        "severity": "high",
        "field": "title",
        "message": "缺少标题",
    }
    assert with_evidence["evidence"] == "x" * 180


def test_score_status_and_severity_counts_follow_penalty_policy():
    issues = [
        content_review_scoring.issue("client_taboo_term", "high", "body", "bad"),
        content_review_scoring.issue("cover_prompt_not_aligned", "medium", "prompt", "bad"),
        content_review_scoring.issue("brand_not_reflected", "low", "body", "bad"),
        {"severity": "unknown"},
    ]

    score = content_review_scoring.score_issues(issues)

    assert score == 40
    assert content_review_scoring.status_for_issues(issues, score) == "blocked"
    assert content_review_scoring.severity_counts(issues) == {"high": 1, "medium": 1, "low": 1}
    assert content_review_scoring.status_for_issues([], 100) == "passed"
    assert content_review_scoring.status_for_issues([content_review_scoring.issue("x", "low", "f", "m")], 95) == "needs_revision"


def test_suggestions_map_known_codes_and_dedupe_output():
    issues = [
        content_review_scoring.issue("missing_title", "high", "title", "bad"),
        content_review_scoring.issue("missing_body", "high", "body", "bad"),
        content_review_scoring.issue("client_taboo_term", "high", "body", "bad"),
        content_review_scoring.issue("unknown", "low", "other", "bad"),
    ]

    suggestions = content_review_scoring.suggestions(issues)

    assert suggestions == [
        "补齐标题和正文后再进入审核。",
        "删除或替换客户明确禁用的表达。",
        "按审核问题修订后重新提交。",
    ]


def test_dedupe_preserves_order():
    assert content_review_scoring.dedupe(["a", "b", "a", "c", "b"]) == ["a", "b", "c"]
