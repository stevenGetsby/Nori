from __future__ import annotations

from datetime import datetime

from nori.storage.paths import reference_image_key, slug
from nori.storage.reference_publisher import ReferenceImagePublisher, image_content_type


PNG_BYTES = b"\x89PNG\r\n\x1a\nfake"


class FakeStore:
    def __init__(self) -> None:
        self.calls = []

    def put_bytes(self, *, key: str, payload: bytes, content_type: str):
        self.calls.append({"key": key, "payload": payload, "content_type": content_type})

        class Stored:
            url = f"https://nori.tos-cn-beijing.volces.com/{key}?signed=1"
            public_url = f"https://nori.tos-cn-beijing.volces.com/{key}"
            bucket = "nori"
            size = len(payload)

        stored = Stored()
        stored.key = key
        stored.content_type = content_type
        return stored


def test_reference_image_key_uses_project_session_date_and_hash():
    key = reference_image_key(
        prefix="nori/reference-images/",
        project="Holly Shit 小红书",
        session="20260607_live",
        source_path="/tmp/资源 50@2x.png",
        payload=PNG_BYTES,
        content_type="image/png",
        now=datetime(2026, 6, 7, 10, 0, 0),
    )

    assert key.startswith("nori/reference-images/Holly-Shit-小红书/20260607_live/20260607/")
    assert key.endswith("_资源-50-2x.png")


def test_slug_keeps_readable_unicode_but_removes_path_delimiters():
    assert slug(" Holly/Shit 开心拉屎 ") == "Holly-Shit-开心拉屎"


def test_reference_publisher_uploads_local_image_to_store(tmp_path):
    path = tmp_path / "ref.png"
    path.write_bytes(PNG_BYTES)
    store = FakeStore()
    publisher = ReferenceImagePublisher(store=store, prefix="nori/reference-images", enabled=True)

    refs = publisher.publish_paths(
        [str(path)],
        project="holly",
        session="session_1",
        now=datetime(2026, 6, 7, 10, 0, 0),
    )

    assert len(refs.items) == 1
    assert refs.inputs == [refs.items[0].url]
    assert refs.items[0].uploaded is True
    assert refs.items[0].key.startswith("nori/reference-images/holly/session_1/20260607/")
    assert refs.to_extra()["reference_object_keys"] == [refs.items[0].key]
    assert store.calls[0]["payload"] == PNG_BYTES
    assert store.calls[0]["content_type"] == "image/png"


def test_reference_publisher_disabled_keeps_local_bytes(tmp_path):
    path = tmp_path / "ref.png"
    path.write_bytes(PNG_BYTES)
    refs = ReferenceImagePublisher.disabled().publish_paths([str(path)])

    assert refs.inputs == [PNG_BYTES]
    assert refs.items[0].uploaded is False
    assert refs.items[0].reason == "local_bytes"


def test_image_content_type_detects_common_image_bytes():
    assert image_content_type("a.jpg", b"\xff\xd8\xffjpeg") == "image/jpeg"
    assert image_content_type("a.png", PNG_BYTES) == "image/png"
