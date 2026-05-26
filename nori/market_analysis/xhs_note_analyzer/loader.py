"""Load local Xiaohongshu note metadata into analyzer samples."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from nori.market_analysis.models import XHSNoteSample


def load_note_sample(meta_path: str | Path) -> XHSNoteSample:
    path = Path(meta_path)
    data = read_json_object(path)
    author_dir = path.parent.parent.parent
    author_meta_path = author_dir / "meta.json"
    author_data = read_json_object(author_meta_path) if author_meta_path.exists() else {}
    return XHSNoteSample(
        meta_path=path,
        category=author_dir.parent.name,
        author_id=str(data.get("user_id") or author_data.get("user_id") or author_dir.name),
        author_name=str(author_data.get("nickname") or ""),
        note_id=str(data.get("note_id") or path.parent.name),
        title=str(data.get("title") or "").strip(),
        desc=str(data.get("desc") or "").strip(),
        tags=tags_from_meta(data),
        metrics={
            "liked": count_text(data.get("liked_count")),
            "collected": count_text(data.get("collected_count")),
            "commented": count_text(data.get("comment_count")),
            "shared": count_text(data.get("share_count")),
        },
        image_count=int(data.get("image_count") or count_text(data.get("image_count"))),
        note_type=str(data.get("note_type") or data.get("type") or ""),
        note_url=str(data.get("note_url") or ""),
    )


def read_json_object(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return data


def tags_from_meta(data: dict[str, Any]) -> list[str]:
    tag_list = str(data.get("tag_list") or "")
    desc = str(data.get("desc") or "")
    raw = re.findall(r"#[^#\s]+", f"{tag_list} {desc}")
    cleaned = []
    for tag in raw:
        tag = tag.replace("[话题]", "").strip()
        if tag and tag not in cleaned:
            cleaned.append(tag)
    return cleaned


def count_text(value: Any) -> int:
    if isinstance(value, int):
        return value
    text = str(value or "0").strip().replace(",", "")
    if not text:
        return 0
    multiplier = 1
    if text.endswith("万"):
        multiplier = 10000
        text = text[:-1]
    try:
        return int(float(text) * multiplier)
    except ValueError:
        return 0


__all__ = ["count_text", "load_note_sample", "read_json_object", "tags_from_meta"]
