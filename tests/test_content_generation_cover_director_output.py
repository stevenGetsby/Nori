"""Tests for CoverDirector cover image output helper."""

from __future__ import annotations

import base64

import pytest

from nori.agents.content_generation.cover_director import output as cover_output


class _OutputError(RuntimeError):
    pass


_TINY_PNG_BYTES = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
)
_TINY_PNG_DATA_URI = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="


def test_save_image_writes_data_uri_with_safe_skill_id(tmp_path):
    path = cover_output.save_image(
        _TINY_PNG_DATA_URI,
        tmp_path,
        "种草推荐 / friends",
        error_type=_OutputError,
    )

    assert path.parent == tmp_path
    assert path.name.startswith("cover_种草推荐_friends_")
    assert path.suffix == ".png"
    assert path.read_bytes() == _TINY_PNG_BYTES


def test_save_image_downloads_http_url_with_user_agent(tmp_path):
    requests: list[object] = []

    class _FakeResp:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def read(self) -> bytes:
            return _TINY_PNG_BYTES

    def fake_urlopen(req, timeout=60):
        requests.append(req)
        assert timeout == 60
        return _FakeResp()

    path = cover_output.save_image(
        "https://example.com/cover.png",
        tmp_path,
        "cover",
        error_type=_OutputError,
        urlopen=fake_urlopen,
    )

    assert path.suffix == ".png"
    assert path.read_bytes() == _TINY_PNG_BYTES
    assert requests
    assert requests[0].headers["User-agent"] == "nori-cover-director/1.0"


def test_save_image_raises_domain_error_for_bad_data_uri(tmp_path):
    with pytest.raises(_OutputError, match="base64"):
        cover_output.save_image(
            "data:image/png;base64,not-base64",
            tmp_path,
            "cover",
            error_type=_OutputError,
        )


def test_save_image_raises_domain_error_for_download_failure(tmp_path):
    def fake_urlopen(req, timeout=60):  # noqa: ARG001
        raise TimeoutError("down")

    with pytest.raises(_OutputError, match="下载封面失败"):
        cover_output.save_image(
            "https://example.com/cover.png",
            tmp_path,
            "cover",
            error_type=_OutputError,
            urlopen=fake_urlopen,
        )
