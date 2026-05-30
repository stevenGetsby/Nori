"""Tests for CoverDirectorAgent (NoteDraft + skill + 参考图 → 本地封面)."""

from __future__ import annotations

import base64
import importlib
import json

import llms
import pytest

from nori.content_generation.models import CandidateTitle, CoverResult, NoteDraft
from nori.core import ImageCapabilityError, UserAsset
from nori.content_generation import CoverDirectorAgent
from nori.content_generation.cover_director import CoverDirectorError

cd_module = importlib.import_module("nori.content_generation.cover_director.cover_director")


# 1x1 透明 PNG 字节
_TINY_PNG_BYTES = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
)
_TINY_PNG_DATA_URI = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="


def _planting_skill() -> dict:
    return {
        "skill_id": "种草推荐·朋友安利笔记制作指南",
        "label": "种草推荐·朋友安利",
        "goal": "planting",
        "note_type": "图文",
        "tone": "朋友安利",
        "creative_goal": "像朋友推荐一样把真实使用感讲清楚。",
        "cover_rules": [{"name": "一句话钩子", "rule": "封面 6-14 字钩子", "evidence": ""}],
        "visual_rules": [{"name": "封面承担点击", "rule": "封面要表达主题", "evidence": ""}],
        "avoid_rules": ["不要硬广"],
    }


def _draft(cover_path: str = "", image_paths: list[str] | None = None) -> NoteDraft:
    return NoteDraft(
        skill_id="种草推荐·朋友安利笔记制作指南",
        title="通勤香薰｜复购的小确幸",
        body="正文",
        tags=["香薰"],
        comment_hook="评论区告诉我 👇",
        cover_path=cover_path,
        image_paths=list(image_paths or []),
        candidate_titles=[CandidateTitle(text="通勤香薰｜复购的小确幸")],
        metrics_target={},
        asset_bundle={
            "brand_facts": ["小众设计师品牌"],
            "text_points": ["下班通勤香气治愈"],
        },
        validation={"status": "pass", "issues": []},
        llm_enhanced=True,
    )


_PROMPT_JSON = json.dumps({
    "prompt": "A cozy 3:4 cover, soft warm light, perfume bottle on a wooden desk, Chinese title text '通勤香薰｜复购的小确幸' centered top, brand color teal accent."
})


def test_cover_director_writes_local_png_from_data_uri(tmp_path, monkeypatch):
    ref = tmp_path / "main.jpg"
    ref.write_bytes(_TINY_PNG_BYTES)
    draft = _draft(cover_path=str(ref))
    skill = _planting_skill()

    chat_calls: list[dict] = []
    image_calls: list[dict] = []

    def fake_chat(messages, *, usage="llm", **kwargs):
        chat_calls.append({"messages": messages, "usage": usage, "kwargs": kwargs})
        return _PROMPT_JSON

    def fake_image(prompt, *, usage="image", size=None, reference_images=None, **kwargs):
        image_calls.append({
            "prompt": prompt,
            "usage": usage,
            "size": size,
            "reference_images": reference_images,
            "kwargs": kwargs,
        })
        return [_TINY_PNG_DATA_URI]

    monkeypatch.setattr(llms, "chat", fake_chat)
    monkeypatch.setattr(llms, "image", fake_image)

    out = tmp_path / "covers"
    result = CoverDirectorAgent().run(draft, skill, out_dir=out)

    assert isinstance(result, CoverResult)
    assert result.cover_path.endswith(".png")
    cover_file = (tmp_path / "covers").iterdir().__next__()
    assert cover_file.read_bytes() == _TINY_PNG_BYTES
    assert result.prompt.startswith("A cozy")
    assert result.size == "1072x1440"
    assert result.reference_paths == [str(ref)]
    assert len(chat_calls) == 1
    assert image_calls[0]["size"] == "1072x1440"
    assert image_calls[0]["reference_images"] is not None


def test_cover_director_routes_prompt_json_through_llms_chat_json(tmp_path, monkeypatch):
    draft = _draft()
    skill = _planting_skill()
    sentinel_chat = object()
    calls: list[dict] = []

    def fake_chat_json(messages, *, usage="llm", _chat=None, **kwargs):
        calls.append({"messages": messages, "usage": usage, "_chat": _chat, "kwargs": kwargs})
        return json.loads(_PROMPT_JSON)

    monkeypatch.setattr(llms, "chat", sentinel_chat)
    monkeypatch.setattr(llms, "chat_json", fake_chat_json)
    monkeypatch.setattr(llms, "image", lambda *a, **k: [_TINY_PNG_DATA_URI])

    result = CoverDirectorAgent().run(draft, skill, out_dir=tmp_path)

    assert result.prompt.startswith("A cozy")
    assert len(calls) == 1
    assert calls[0]["usage"] == "llm"
    assert calls[0]["_chat"] is sentinel_chat
    assert calls[0]["kwargs"]["json_mode"] is True


def test_cover_director_writes_png_from_http_url(tmp_path, monkeypatch):
    draft = _draft()
    skill = _planting_skill()

    monkeypatch.setattr(llms, "chat", lambda *a, **k: _PROMPT_JSON)
    monkeypatch.setattr(llms, "image", lambda *a, **k: ["https://example.com/cover.png"])

    class _FakeResp:
        def __init__(self, payload: bytes) -> None:
            self._payload = payload

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def read(self) -> bytes:
            return self._payload

    def fake_urlopen(req, timeout=60):  # noqa: ARG001
        return _FakeResp(_TINY_PNG_BYTES)

    monkeypatch.setattr(cd_module.urllib.request, "urlopen", fake_urlopen)

    out = tmp_path / "covers"
    result = CoverDirectorAgent().run(draft, skill, out_dir=out)

    assert result.cover_path.endswith(".png")
    assert (out / result.cover_path.split("/")[-1]).read_bytes() == _TINY_PNG_BYTES


def test_cover_director_uses_intent_size_override(tmp_path, monkeypatch):
    draft = _draft()
    skill = _planting_skill()

    monkeypatch.setattr(llms, "chat", lambda *a, **k: _PROMPT_JSON)
    captured: dict = {}

    def fake_image(prompt, *, usage="image", size=None, reference_images=None, **kwargs):
        captured["size"] = size
        return [_TINY_PNG_DATA_URI]

    monkeypatch.setattr(llms, "image", fake_image)

    CoverDirectorAgent().run(draft, skill, out_dir=tmp_path, size="1024x1360")
    assert captured["size"] == "1024x1360"


def test_cover_director_falls_back_to_reference_assets_when_draft_empty(tmp_path, monkeypatch):
    ref = tmp_path / "ref.jpg"
    ref.write_bytes(_TINY_PNG_BYTES)
    draft = _draft()  # 没 cover_path / image_paths
    skill = _planting_skill()
    refs_asset = [UserAsset(kind="image", path=str(ref))]

    captured: dict = {}

    def fake_image(prompt, *, usage="image", size=None, reference_images=None, **kwargs):
        captured["refs"] = reference_images
        return [_TINY_PNG_DATA_URI]

    monkeypatch.setattr(llms, "chat", lambda *a, **k: _PROMPT_JSON)
    monkeypatch.setattr(llms, "image", fake_image)

    result = CoverDirectorAgent().run(draft, skill, refs_asset, out_dir=tmp_path)
    assert result.reference_paths == [str(ref)]
    assert captured["refs"] is not None
    assert len(captured["refs"]) == 1


def test_cover_director_retries_without_local_refs_when_provider_rejects_reference_bytes(tmp_path, monkeypatch):
    ref = tmp_path / "local-ref.jpg"
    ref.write_bytes(_TINY_PNG_BYTES)
    draft = _draft(cover_path=str(ref))
    skill = _planting_skill()
    calls: list[list | None] = []

    def fake_image(prompt, *, usage="image", size=None, reference_images=None, **kwargs):
        calls.append(reference_images)
        if reference_images:
            raise ImageCapabilityError("local reference images are not supported")
        return [_TINY_PNG_DATA_URI]

    monkeypatch.setattr(llms, "chat", lambda *a, **k: _PROMPT_JSON)
    monkeypatch.setattr(llms, "image", fake_image)

    result = CoverDirectorAgent().run(draft, skill, out_dir=tmp_path)

    assert result.reference_paths == [str(ref)]
    assert calls[0] is not None
    assert calls[1] is None
    assert result.extra["reference_images_sent"] is False
    assert result.extra["reference_image_fallback"] == "local_refs_not_supported"


def test_cover_director_preserves_remote_url_references(tmp_path, monkeypatch):
    url = "https://example.test/holly-ref.jpg"
    draft = _draft(cover_path=url)
    skill = _planting_skill()
    captured: dict = {}

    def fake_image(prompt, *, usage="image", size=None, reference_images=None, **kwargs):
        captured["refs"] = reference_images
        return [_TINY_PNG_DATA_URI]

    monkeypatch.setattr(llms, "chat", lambda *a, **k: _PROMPT_JSON)
    monkeypatch.setattr(llms, "image", fake_image)

    result = CoverDirectorAgent().run(draft, skill, out_dir=tmp_path)
    assert result.reference_paths == [url]
    assert captured["refs"] == [url]


def test_cover_director_passes_none_references_when_no_assets(tmp_path, monkeypatch):
    draft = _draft()
    skill = _planting_skill()

    captured: dict = {}

    def fake_image(prompt, *, usage="image", size=None, reference_images=None, **kwargs):
        captured["refs"] = reference_images
        return [_TINY_PNG_DATA_URI]

    monkeypatch.setattr(llms, "chat", lambda *a, **k: _PROMPT_JSON)
    monkeypatch.setattr(llms, "image", fake_image)

    CoverDirectorAgent().run(draft, skill, out_dir=tmp_path)
    assert captured["refs"] is None


def test_cover_director_raises_when_prompt_empty(tmp_path, monkeypatch):
    draft = _draft()
    skill = _planting_skill()
    monkeypatch.setattr(llms, "chat", lambda *a, **k: json.dumps({"prompt": ""}))

    with pytest.raises(CoverDirectorError, match="返回空 prompt"):
        CoverDirectorAgent().run(draft, skill, out_dir=tmp_path)


def test_cover_director_raises_when_image_api_empty(tmp_path, monkeypatch):
    draft = _draft()
    skill = _planting_skill()
    monkeypatch.setattr(llms, "chat", lambda *a, **k: _PROMPT_JSON)
    monkeypatch.setattr(llms, "image", lambda *a, **k: [])

    with pytest.raises(CoverDirectorError, match="没返回任何图"):
        CoverDirectorAgent().run(draft, skill, out_dir=tmp_path)


def test_cover_director_raises_when_image_api_throws(tmp_path, monkeypatch):
    draft = _draft()
    skill = _planting_skill()
    monkeypatch.setattr(llms, "chat", lambda *a, **k: _PROMPT_JSON)

    def boom(*a, **k):
        raise RuntimeError("image down")

    monkeypatch.setattr(llms, "image", boom)
    with pytest.raises(CoverDirectorError, match="llms.image 失败"):
        CoverDirectorAgent().run(draft, skill, out_dir=tmp_path)


def test_cover_director_raises_when_chat_returns_non_json(tmp_path, monkeypatch):
    draft = _draft()
    skill = _planting_skill()
    monkeypatch.setattr(llms, "chat", lambda *a, **k: "no json")

    with pytest.raises(CoverDirectorError, match="无法解析为 JSON"):
        CoverDirectorAgent().run(draft, skill, out_dir=tmp_path)


def test_cover_director_caps_reference_paths_to_three(tmp_path, monkeypatch):
    refs = []
    for i in range(5):
        p = tmp_path / f"r{i}.jpg"
        p.write_bytes(_TINY_PNG_BYTES)
        refs.append(str(p))
    draft = _draft(cover_path=refs[0], image_paths=refs[1:])
    skill = _planting_skill()

    monkeypatch.setattr(llms, "chat", lambda *a, **k: _PROMPT_JSON)
    captured: dict = {}

    def fake_image(prompt, *, usage="image", size=None, reference_images=None, **kwargs):
        captured["refs"] = reference_images
        return [_TINY_PNG_DATA_URI]

    monkeypatch.setattr(llms, "image", fake_image)

    result = CoverDirectorAgent().run(draft, skill, out_dir=tmp_path)
    assert len(result.reference_paths) == 3
    assert len(captured["refs"]) == 3


# ============ tagged_assets 路径：LLM 自己选参考图 ============

def _make_tagged_asset(path: str, **tag) -> UserAsset:
    return UserAsset(
        kind="image",
        path=path,
        vision_roles=tag.get("vision_roles", []),
        subject=tag.get("subject", ""),
        brand_signals=tag.get("brand_signals", []),
        usable_for=tag.get("usable_for", []),
        quality=tag.get("quality", ""),
    )


def test_cover_director_uses_tagged_assets_via_llm_selection(tmp_path, monkeypatch):
    a = tmp_path / "logo.png"; a.write_bytes(_TINY_PNG_BYTES)
    b = tmp_path / "product.jpg"; b.write_bytes(_TINY_PNG_BYTES)
    c = tmp_path / "noise.png"; c.write_bytes(_TINY_PNG_BYTES)

    tagged = [
        _make_tagged_asset(str(a), vision_roles=["brand_logo"], brand_signals=["holly"], usable_for=["cover"], quality="high"),
        _make_tagged_asset(str(b), vision_roles=["product_shot"], usable_for=["cover", "body"], quality="high"),
        _make_tagged_asset(str(c), vision_roles=["raw_material"], usable_for=["not_usable"], quality="low"),
    ]
    # draft.cover_path / image_paths 全留空：确认走 tagged 路径而不是 fallback
    draft = _draft()

    chat_calls: list[str] = []

    def fake_chat(messages, *, usage="llm", **kwargs):
        # 第 1 次调用：CoverRefSelector；第 2 次：CoverPromptWriter
        chat_calls.append(messages[1]["content"])
        if len(chat_calls) == 1:
            return json.dumps({"chosen_indices": [0, 1], "rationale": "logo+产品"})
        return _PROMPT_JSON

    captured: dict = {}

    def fake_image(prompt, *, usage="image", size=None, reference_images=None, **kwargs):
        captured["refs"] = reference_images
        return [_TINY_PNG_DATA_URI]

    monkeypatch.setattr(llms, "chat", fake_chat)
    monkeypatch.setattr(llms, "image", fake_image)

    result = CoverDirectorAgent().run(draft, _planting_skill(), out_dir=tmp_path, tagged_assets=tagged)

    assert result.reference_paths == [str(a), str(b)]
    assert len(captured["refs"]) == 2
    # 第 1 次 chat 是选图工序，prompt 必须出现资产池
    assert "资产池" in chat_calls[0] or "chosen_indices" in chat_calls[0]


def test_cover_director_accepts_zero_refs_from_tagged_selector(tmp_path, monkeypatch):
    a = tmp_path / "x.png"; a.write_bytes(_TINY_PNG_BYTES)
    tagged = [_make_tagged_asset(str(a), vision_roles=["unknown"], usable_for=["not_usable"])]
    draft = _draft()

    def fake_chat(messages, *, usage="llm", **kwargs):
        if "chosen_indices" in messages[1]["content"] or "资产池" in messages[1]["content"]:
            return json.dumps({"chosen_indices": [], "rationale": "都不合适"})
        return _PROMPT_JSON

    captured: dict = {}

    def fake_image(prompt, *, usage="image", size=None, reference_images=None, **kwargs):
        captured["refs"] = reference_images
        return [_TINY_PNG_DATA_URI]

    monkeypatch.setattr(llms, "chat", fake_chat)
    monkeypatch.setattr(llms, "image", fake_image)

    result = CoverDirectorAgent().run(draft, _planting_skill(), out_dir=tmp_path, tagged_assets=tagged)
    assert result.reference_paths == []
    assert captured["refs"] is None  # llms.image 不传 reference_images


def test_cover_director_caps_tagged_selection_at_max_references(tmp_path, monkeypatch):
    paths = []
    for i in range(12):
        p = tmp_path / f"r{i}.png"; p.write_bytes(_TINY_PNG_BYTES)
        paths.append(str(p))
    tagged = [_make_tagged_asset(p, vision_roles=["product_shot"], usable_for=["cover"]) for p in paths]
    draft = _draft()

    def fake_chat(messages, *, usage="llm", **kwargs):
        if "chosen_indices" in messages[1]["content"] or "资产池" in messages[1]["content"]:
            return json.dumps({"chosen_indices": list(range(12))})
        return _PROMPT_JSON

    monkeypatch.setattr(llms, "chat", fake_chat)
    monkeypatch.setattr(llms, "image", lambda *a, **k: [_TINY_PNG_DATA_URI])

    result = CoverDirectorAgent().run(draft, _planting_skill(), out_dir=tmp_path, tagged_assets=tagged)
    # MAX_REFERENCES = 8
    assert len(result.reference_paths) == cd_module.MAX_REFERENCES == 8


def test_cover_director_ignores_out_of_range_or_missing_indices(tmp_path, monkeypatch):
    a = tmp_path / "a.png"; a.write_bytes(_TINY_PNG_BYTES)
    tagged = [_make_tagged_asset(str(a), vision_roles=["product_shot"], usable_for=["cover"])]
    draft = _draft()

    def fake_chat(messages, *, usage="llm", **kwargs):
        if "资产池" in messages[1]["content"]:
            return json.dumps({"chosen_indices": [0, 99, "bad", -1]})
        return _PROMPT_JSON

    monkeypatch.setattr(llms, "chat", fake_chat)
    monkeypatch.setattr(llms, "image", lambda *a, **k: [_TINY_PNG_DATA_URI])

    result = CoverDirectorAgent().run(draft, _planting_skill(), out_dir=tmp_path, tagged_assets=tagged)
    assert result.reference_paths == [str(a)]
