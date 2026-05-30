"""Tests for XHS note metadata loading helpers."""

from __future__ import annotations

import json
from pathlib import Path

from nori.agents.market_analysis.xhs_note_analyzer import loader as xhs_note_loader
from nori.agents.market_analysis.models import XHSNoteSample


def _write_meta(tmp_path: Path, note_data: dict, author_data: dict | None = None) -> Path:
    author_dir = tmp_path / "cold_start_data" / "xhs" / "设计" / "author_1"
    note_dir = author_dir / "posts" / "note_001"
    note_dir.mkdir(parents=True)
    if author_data is not None:
        (author_dir / "meta.json").write_text(
            json.dumps(author_data, ensure_ascii=False),
            encoding="utf-8",
        )
    meta_path = note_dir / "meta.json"
    meta_path.write_text(json.dumps(note_data, ensure_ascii=False), encoding="utf-8")
    return meta_path


def test_load_note_sample_restores_note_and_author_metadata(tmp_path):
    meta_path = _write_meta(
        tmp_path,
        {
            "note_id": "note_001",
            "title": "报告！ 年夜饭薯该宠幸谁？",
            "desc": "正文\n#新年答案之书 #小红书答案之书",
            "user_id": "",
            "liked_count": "1.2万",
            "collected_count": "1,234",
            "comment_count": "20",
            "share_count": "6",
            "tag_list": "#新年答案之书[话题] #小红书答案之书",
            "image_count": "3",
            "note_type": "normal",
            "note_url": "https://www.xiaohongshu.com/explore/note_001",
        },
        {"user_id": "author_1", "nickname": "测试作者"},
    )

    note = xhs_note_loader.load_note_sample(meta_path)

    assert isinstance(note, XHSNoteSample)
    assert note.category == "设计"
    assert note.author_id == "author_1"
    assert note.author_name == "测试作者"
    assert note.note_id == "note_001"
    assert note.metrics == {"liked": 12000, "collected": 1234, "commented": 20, "shared": 6}
    assert note.image_count == 3
    assert note.tags == ["#新年答案之书", "#小红书答案之书"]


def test_load_note_sample_uses_path_fallbacks_when_fields_are_missing(tmp_path):
    meta_path = _write_meta(tmp_path, {"title": "无 id 笔记", "desc": ""})

    note = xhs_note_loader.load_note_sample(meta_path)

    assert note.note_id == "note_001"
    assert note.author_id == "author_1"
    assert note.author_name == ""
    assert note.metrics == {"liked": 0, "collected": 0, "commented": 0, "shared": 0}


def test_read_json_rejects_non_object_payload(tmp_path):
    path = tmp_path / "meta.json"
    path.write_text("[1, 2, 3]", encoding="utf-8")

    try:
        xhs_note_loader.read_json_object(path)
    except ValueError as exc:
        assert "Expected JSON object" in str(exc)
    else:
        raise AssertionError("expected ValueError for non-object JSON")
