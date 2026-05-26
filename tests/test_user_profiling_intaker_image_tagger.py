import base64

import llms

from nori.user_profiling.models import UserInput
from nori.user_profiling.intaker import image_tagger


_TINY_PNG_BYTES = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
)


def test_image_tagger_make_image_asset_filters_and_limits_fields():
    asset = image_tagger.make_image_asset(
        "/tmp/a.png",
        {
            "vision_roles": ["Brand_Logo", "weird", "brand_logo", "portrait"],
            "subject": "X" * 100,
            "brand_signals": [" ", "nori "],
            "usable_for": ["Cover", "bad"],
            "quality": "HIGH",
        },
    )

    assert asset.kind == "image"
    assert asset.path == "/tmp/a.png"
    assert asset.vision_roles == ["brand_logo", "portrait"]
    assert asset.usable_for == ["cover"]
    assert asset.brand_signals == ["nori"]
    assert asset.quality == "high"
    assert len(asset.subject) == 60


def test_image_tagger_build_tagged_assets_skips_vision_when_disabled(monkeypatch):
    def fail_tag_images(*args, **kwargs):
        raise AssertionError("vision tagging should be skipped")

    monkeypatch.setattr(image_tagger, "tag_images_llm", fail_tag_images)

    assets = image_tagger.build_tagged_assets(
        UserInput(text="做一篇种草笔记", images=["/tmp/a.png"]),
        use_vision=False,
    )

    assert [asset.kind for asset in assets] == ["image", "text"]
    assert assets[0].path == "/tmp/a.png"
    assert assets[0].vision_roles == []
    assert assets[1].text == "做一篇种草笔记"


def test_image_tagger_tag_one_image_uses_chat_json_helper(tmp_path, monkeypatch):
    image_path = tmp_path / "a.png"
    image_path.write_bytes(_TINY_PNG_BYTES)
    calls: list[dict] = []
    sentinel_chat = object()

    def fake_chat_json(messages, *, usage="llm", _chat=None, **kwargs):
        calls.append({"messages": messages, "usage": usage, "_chat": _chat, "kwargs": kwargs})
        return {"vision_roles": ["product_shot"], "usable_for": ["cover"], "quality": "high"}

    monkeypatch.setattr(llms, "chat", sentinel_chat)
    monkeypatch.setattr(llms, "chat_json", fake_chat_json)

    tag = image_tagger.tag_one_image_llm(str(image_path), "给品牌种草")

    assert tag == {"vision_roles": ["product_shot"], "usable_for": ["cover"], "quality": "high"}
    assert calls[0]["usage"] == "vision"
    assert calls[0]["_chat"] is sentinel_chat
    assert calls[0]["kwargs"]["timeout"] == 60
    assert calls[0]["kwargs"]["json_mode"] is True
    user_parts = calls[0]["messages"][1]["content"]
    assert sum(1 for part in user_parts if part.get("type") == "image_url") == 1
