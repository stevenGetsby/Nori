"""Tests for CoverDirector reference image selection helpers."""

from __future__ import annotations

from nori.agents.content_generation.schemas import CandidateTitle, NoteDraft
from nori.core import UserAsset
from nori.agents.content_generation.cover_director.package import CoverReferenceSelector


cover_refs = CoverReferenceSelector()


def _draft(cover_path: str = "", image_paths: list[str] | None = None) -> NoteDraft:
    return NoteDraft(
        skill_id="planting",
        title="通勤香薰｜复购的小确幸",
        body="正文",
        tags=["香薰"],
        comment_hook="评论区告诉我",
        cover_path=cover_path,
        image_paths=list(image_paths or []),
        candidate_titles=[CandidateTitle(text="通勤香薰｜复购的小确幸")],
        metrics_target={},
        asset_bundle={},
        validation={"status": "pass", "issues": []},
        llm_enhanced=True,
    )


def _image_asset(path: str, **tag) -> UserAsset:
    return UserAsset(
        kind="image",
        path=path,
        vision_roles=tag.get("vision_roles", []),
        subject=tag.get("subject", ""),
        brand_signals=tag.get("brand_signals", []),
        usable_for=tag.get("usable_for", []),
        quality=tag.get("quality", ""),
    )


def test_collect_reference_paths_prefers_draft_paths_and_dedupes_existing_files(tmp_path):
    paths = []
    for name in ["cover.jpg", "body1.jpg", "body2.jpg", "body3.jpg", "fallback.jpg"]:
        p = tmp_path / name
        p.write_bytes(b"img")
        paths.append(str(p))
    missing = str(tmp_path / "missing.jpg")

    draft = _draft(cover_path=paths[0], image_paths=[paths[1], paths[0], missing, paths[2], paths[3]])
    fallback_assets = [_image_asset(paths[4])]

    result = cover_refs.collect_legacy_paths(
        draft,
        fallback_assets,
        max_references=3,
    )

    assert result == paths[:3]


def test_collect_reference_paths_falls_back_to_reference_assets_only_when_draft_has_no_paths(tmp_path):
    ref1 = tmp_path / "ref1.jpg"; ref1.write_bytes(b"img")
    ref2 = tmp_path / "ref2.jpg"; ref2.write_bytes(b"img")
    non_image = tmp_path / "doc.txt"; non_image.write_text("text", encoding="utf-8")

    result = cover_refs.collect_legacy_paths(
        _draft(),
        [
            UserAsset(kind="text", path=str(non_image)),
            _image_asset(str(ref1)),
            _image_asset(str(ref2)),
        ],
        max_references=1,
    )

    assert result == [str(ref1)]


def test_collect_reference_paths_keeps_remote_url_references():
    url = "https://example.test/holly-ref.jpg"
    result = cover_refs.collect_legacy_paths(
        _draft(cover_path=url),
        [],
        max_references=1,
    )

    assert result == [url]


def test_select_references_llm_filters_dedupes_and_caps_chosen_indices(tmp_path):
    a = tmp_path / "a.png"; a.write_bytes(b"img")
    b = tmp_path / "b.png"; b.write_bytes(b"img")
    missing = tmp_path / "missing.png"
    tagged = [
        _image_asset(str(a), subject="logo", brand_signals=["Nori"], usable_for=["cover"], quality="high"),
        _image_asset(str(b), subject="product", vision_roles=["product_shot"], usable_for=["cover"], quality="high"),
        UserAsset(kind="text", path=str(tmp_path / "copy.txt")),
        _image_asset(str(missing), subject="missing", usable_for=["cover"]),
    ]
    calls: list[dict] = []

    def fake_json_call(**kwargs):
        calls.append(kwargs)
        return {"chosen_indices": [0, 1, 1, 2, 3, 99, "bad"]}

    result = cover_refs.select_with_llm(
        _draft(),
        {"tone": "朋友安利", "note_type": "图文", "creative_goal": "真实使用感"},
        {"user_text": "需要突出品牌和产品"},
        tagged,
        json_call=fake_json_call,
        max_references=2,
    )

    assert result == [str(a), str(b)]
    assert len(calls) == 1
    assert "资产池" in calls[0]["user"]
    assert str(a) in calls[0]["user"]
    assert "copy.txt" not in calls[0]["user"]


def test_select_references_llm_returns_empty_for_no_images_or_invalid_response(tmp_path):
    text = tmp_path / "copy.txt"; text.write_text("copy", encoding="utf-8")
    calls: list[dict] = []

    def fake_json_call(**kwargs):
        calls.append(kwargs)
        return {"chosen_indices": "0"}

    assert cover_refs.select_with_llm(
        _draft(),
        {},
        {},
        [UserAsset(kind="text", path=str(text))],
        json_call=fake_json_call,
    ) == []
    assert calls == []

    image = tmp_path / "image.jpg"; image.write_bytes(b"img")
    assert cover_refs.select_with_llm(
        _draft(),
        {},
        {},
        [_image_asset(str(image))],
        json_call=fake_json_call,
    ) == []


def test_select_references_llm_accepts_remote_url_assets():
    url = "https://example.test/holly-ref.jpg"

    def fake_json_call(**kwargs):
        return {"chosen_indices": [0]}

    result = cover_refs.select_with_llm(
        _draft(),
        {},
        {},
        [_image_asset(url, usable_for=["cover"])],
        json_call=fake_json_call,
    )

    assert result == [url]
