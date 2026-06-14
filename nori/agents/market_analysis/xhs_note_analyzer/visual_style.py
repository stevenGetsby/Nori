"""Vision style extraction for downloaded XHS hot-note images."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from nori.core import LLMFactory
from nori.shared.image_io import image_to_data_uri
from nori.shared.llm_json import try_stage_messages_json


SYSTEM_PROMPT = "你是 Nori 的小红书热帖视觉风格分析器。只输出 JSON。"


def enrich_hot_note_visual_styles(
    hot_notes: list[Any],
    *,
    llm_factory: LLMFactory | None = None,
    max_images_per_note: int = 3,
) -> list[Any]:
    """Mutate hot notes with visual_style parsed from downloaded images."""
    gateway = llm_factory or LLMFactory()
    for note in hot_notes:
        if isinstance(getattr(note, "visual_style", None), dict) and note.visual_style.get("status") == "ok":
            continue
        note.visual_style = analyze_hot_note_visual_style(
            note,
            llm_factory=gateway,
            max_images=max_images_per_note,
        )
    return hot_notes


def analyze_hot_note_visual_style(
    note: Any,
    *,
    llm_factory: LLMFactory | None = None,
    max_images: int = 3,
) -> dict[str, Any]:
    paths = _existing_image_paths(note, limit=max_images)
    if not paths:
        return {"status": "no_images", "image_paths": []}

    content: list[dict[str, Any]] = [
        {
            "type": "text",
            "text": _user_prompt(note, paths),
        }
    ]
    for path in paths:
        uri = image_to_data_uri(path)
        if uri:
            content.append({"type": "image_url", "image_url": {"url": uri}})
    if len(content) == 1:
        return {"status": "unreadable_images", "image_paths": [str(path) for path in paths]}

    gateway = llm_factory or LLMFactory()
    data, error = try_stage_messages_json(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": content},
        ],
        usage="vision",
        timeout=90,
        chat_json_func=gateway.chat_json_func,
    )
    if not isinstance(data, dict):
        return {
            "status": "vision_failed",
            "image_paths": [str(path) for path in paths],
            "error": error or {},
        }
    return _normalize_style(data, paths)


def _existing_image_paths(note: Any, *, limit: int) -> list[Path]:
    candidates: list[str] = []
    cover_path = str(getattr(note, "cover_path", "") or "").strip()
    if cover_path:
        candidates.append(cover_path)
    candidates.extend(str(path).strip() for path in (getattr(note, "image_paths", []) or []) if str(path).strip())

    paths: list[Path] = []
    seen: set[str] = set()
    for candidate in candidates:
        path = Path(candidate)
        key = str(path.resolve()) if path.exists() else str(path)
        if key in seen or not path.is_file():
            continue
        paths.append(path)
        seen.add(key)
        if len(paths) >= limit:
            break
    return paths


def _user_prompt(note: Any, paths: list[Path]) -> str:
    return f"""\
请分析这些小红书热帖图片的可迁移视觉风格，不要复刻具体作品、logo、水印、人物身份或品牌元素。

热帖信息：
- keyword: {getattr(note, "keyword", "")}
- title: {getattr(note, "title", "")}
- liked: {getattr(note, "liked", 0)}
- collected: {getattr(note, "collected", 0)}
- image_paths: {[str(path) for path in paths]}

请输出 JSON，字段固定：
{{
  "composition": "构图方式，例如主体占比、视角、留白、景别",
  "subject_focus": "视觉主体如何被突出",
  "palette": "色彩和材质倾向",
  "lighting": "光线、阴影、反光、氛围",
  "texture": "质感表现和细节处理",
  "typography": "封面文字位置、层级、字体气质；没有文字就写无明显文字",
  "layout": "图文关系、信息密度、安全区",
  "hook_text_strategy": "封面一句话如何制造点击",
  "reusable_rules": ["可迁移到新封面的视觉规则，3-6条"],
  "avoid": ["不能照搬或应避免的点，1-4条"]
}}
"""


def _normalize_style(data: dict[str, Any], paths: list[Path]) -> dict[str, Any]:
    def text(key: str, limit: int = 180) -> str:
        return str(data.get(key) or "").strip()[:limit]

    def string_list(key: str, limit: int) -> list[str]:
        raw = data.get(key)
        if isinstance(raw, str):
            items = [raw]
        elif isinstance(raw, list):
            items = [str(item) for item in raw]
        else:
            items = []
        out: list[str] = []
        seen: set[str] = set()
        for item in items:
            value = item.strip()
            if value and value not in seen:
                out.append(value[:180])
                seen.add(value)
            if len(out) >= limit:
                break
        return out

    return {
        "status": "ok",
        "image_paths": [str(path) for path in paths],
        "composition": text("composition"),
        "subject_focus": text("subject_focus"),
        "palette": text("palette"),
        "lighting": text("lighting"),
        "texture": text("texture"),
        "typography": text("typography"),
        "layout": text("layout"),
        "hook_text_strategy": text("hook_text_strategy"),
        "reusable_rules": string_list("reusable_rules", 6),
        "avoid": string_list("avoid", 4),
    }


__all__ = [
    "SYSTEM_PROMPT",
    "analyze_hot_note_visual_style",
    "enrich_hot_note_visual_styles",
]
