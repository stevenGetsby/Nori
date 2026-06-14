"""Xiaohongshu-specific search, download, and top-note collection."""
from __future__ import annotations

import json
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, List

import httpx

from data_collect.adapter import DownloadRule, HotNote, SearchRule, TopNotesResult, TopNotesRule

if TYPE_CHECKING:
    from data_collect.adapter import DataCollector


_XHS_SORT_MAP = {
    "general": "general",
    "popular": "popularity_descending",
    "latest": "time_descending",
}
_XHS_SEARCH_PAGE_SIZE = 20


class XHSPlatformAdapter:
    """小红书平台适配器：搜索、下载、会话素材采集。"""

    platform = "xhs"

    def __init__(self, collector: DataCollector) -> None:
        self.collector = collector

    def search(self, rule: SearchRule) -> dict:
        if rule.platform != self.platform:
            raise ValueError(f"XHSPlatformAdapter 只支持 xhs，收到: {rule.platform}")
        return self.collector._run_crawler(
            platform=rule.platform,
            crawler_type="search",
            keywords=",".join(rule.keywords),
            sort=_XHS_SORT_MAP.get(rule.sort, rule.sort),
            enable_comments=rule.enable_comments,
            enable_sub_comments=rule.enable_sub_comments,
            save_option=rule.save_option,
            data_dir=rule.data_dir,
            sqlite_path=rule.sqlite_path,
            max_notes=rule.max_notes,
        )

    def download(self, rule: DownloadRule) -> List[str]:
        if rule.platform != self.platform:
            raise ValueError(f"XHSPlatformAdapter 只支持 xhs，收到: {rule.platform}")
        self.collector.start_downloader()
        save_dir = Path(rule.save_dir).expanduser().resolve()
        save_dir.mkdir(parents=True, exist_ok=True)
        saved: List[str] = []
        cookies = self.collector._platform_cookie_string(rule.platform)
        with httpx.Client(timeout=60) as client:
            for target in rule.targets:
                detail = client.post(
                    f"{self.collector.downloader_url}/api/v1/content_detail",
                    json={"platform": rule.platform, "content_url": target, "cookies": cookies},
                ).json()
                saved.extend(_save_assets(detail, save_dir, rule))
        return saved

    def collect_top_notes(self, rule: TopNotesRule) -> TopNotesResult:
        """每关键词抓 popular 两页（约 40 条），合并去重后按点赞数降序取 top_k。

        不做时间窗 / min_liked 过滤；TopNotesRule.days / min_liked 字段保留向后兼容但被忽略。
        """
        if rule.platform != self.platform:
            raise ValueError(f"XHSPlatformAdapter 只支持 xhs，收到: {rule.platform}")
        if not rule.keywords:
            raise ValueError("TopNotesRule.keywords 不能为空")

        base_data_dir = Path(rule.data_dir).expanduser()
        if not base_data_dir.is_absolute():
            base_data_dir = self.collector.project_root / base_data_dir
        base_data_dir.mkdir(parents=True, exist_ok=True)
        run_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        keyword_data_dirs: dict[str, Path] = {}
        # 固定抓两页：max_notes = 2 * 每页 20 = 40，crawler 内部自动翻页
        max_notes = max(rule.top_k_per_keyword, _XHS_SEARCH_PAGE_SIZE * 2)

        for keyword in rule.keywords:
            keyword_text = str(keyword)
            keyword_dir = base_data_dir / f"{run_stamp}_{_safe_path_part(keyword_text)}"
            keyword_dir.mkdir(parents=True, exist_ok=True)
            keyword_data_dirs[keyword_text] = keyword_dir
            self.collector.search(SearchRule(
                platform=rule.platform,
                keywords=[keyword_text],
                sort="popular",
                max_notes=max_notes,
                enable_comments=False,
                save_option="json",
                data_dir=str(keyword_dir),
            ))

        hot_notes: List[HotNote] = []
        insufficient: List[dict] = []
        seen: set[str] = set()
        for keyword in rule.keywords:
            keyword_text = str(keyword)
            keyword_dir = keyword_data_dirs[keyword_text]
            rows = _query_xhs_json_notes(keyword_dir, keyword_text)
            unique_rows: dict[str, dict] = {}
            for row in rows:
                note_id = str(row.get("note_id") or "").strip()
                if not note_id:
                    continue
                current = unique_rows.get(note_id)
                if current is None or _parse_count(row.get("liked_count")) > _parse_count(current.get("liked_count")):
                    unique_rows[note_id] = row
            scored = sorted(unique_rows.values(), key=lambda item: _parse_count(item.get("liked_count")), reverse=True)
            picked = []
            for row in scored:
                if row["note_id"] in seen:
                    continue
                picked.append(row)
                if len(picked) >= rule.top_k_per_keyword:
                    break
            if len(picked) < rule.top_k_per_keyword:
                insufficient.append({
                    "keyword": keyword_text,
                    "got": len(picked),
                    "need": rule.top_k_per_keyword,
                })
            for row in picked:
                seen.add(row["note_id"])
                hot_notes.append(_row_to_hot_note(row, keyword_text))

        notes_by_keyword: dict[str, list[HotNote]] = {}
        for note in hot_notes:
            notes_by_keyword.setdefault(note.keyword, []).append(note)
            poster_dir = keyword_data_dirs[note.keyword] / _safe_path_part(note.note_id or note.title)
            poster_dir.mkdir(parents=True, exist_ok=True)
            if rule.download_media:
                try:
                    paths = self.collector.download(DownloadRule(
                        platform=rule.platform,
                        targets=[note.note_url or note.note_id],
                        save_dir=str(poster_dir),
                    ))
                except Exception:
                    paths = []
                if not paths:
                    paths = _download_search_row_media(row, poster_dir, rule)
                _organize_poster_assets(note, poster_dir, paths)
            _write_note_json(poster_dir / "note.json", note)

        for keyword in keyword_data_dirs:
            notes = notes_by_keyword.get(keyword, [])
            selected_path = keyword_data_dirs[keyword] / "selected_notes.json"
            selected_path.write_text(
                json.dumps([note.to_dict() for note in notes], ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

        return TopNotesResult(
            platform=rule.platform,
            queries=list(rule.keywords),
            hot_notes=hot_notes,
            insufficient=insufficient,
            source_data_dir=str(base_data_dir),
            source_keyword_dirs={keyword: str(path) for keyword, path in keyword_data_dirs.items()},
        )


def _save_assets(detail: dict, save_dir: Path, rule: DownloadRule) -> List[str]:
    saved: List[str] = []
    if not isinstance(detail, dict):
        return saved
    data = detail.get("data") or {}
    if isinstance(data, dict) and isinstance(data.get("content"), dict):
        data = data["content"]
    urls: list[tuple[str, str]] = []
    if rule.include_cover and data.get("cover_url"):
        urls.append((data["cover_url"], "cover"))
    if rule.include_images:
        for index, url in enumerate(data.get("image_urls") or data.get("image_list") or []):
            urls.append((url, f"image_{index}"))
    video_url = data.get("video_download_url") or data.get("video_url")
    if rule.include_video and video_url:
        urls.append((video_url, "video"))
    with httpx.Client(timeout=120, follow_redirects=True) as client:
        for url, label in urls:
            try:
                with client.stream("GET", url) as resp:
                    resp.raise_for_status()
                    ext = Path(url.split("?", 1)[0]).suffix or _extension_for_content_type(resp.headers.get("content-type", ""))
                    content_id = data.get("id") or data.get("content_id") or "asset"
                    file_path = save_dir / f"{rule.platform}_{content_id}_{label}{ext}"
                    with open(file_path, "wb") as file:
                        for chunk in resp.iter_bytes():
                            file.write(chunk)
                saved.append(str(file_path))
            except Exception:
                continue
    return saved


def _download_search_row_media(row: dict, save_dir: Path, rule: DownloadRule) -> List[str]:
    """Fallback media download from search result CDN URLs.

    The XHS detail downloader can fail when the detail API asks for a fresh
    login challenge. Search rows still carry CDN image URLs; those are enough
    for market visual-style learning and avoid blocking the whole workflow.
    """
    urls: list[tuple[str, str]] = []
    if rule.include_cover:
        cover_url = str(row.get("cover_url") or row.get("cover") or "").strip()
        if cover_url:
            urls.append((cover_url, "cover"))
    if rule.include_images:
        for index, url in enumerate(_row_image_urls(row)):
            urls.append((url, f"image_{index}"))
    if not urls:
        return []

    save_dir.mkdir(parents=True, exist_ok=True)
    content_id = str(row.get("note_id") or row.get("id") or "asset")
    saved: List[str] = []
    with httpx.Client(timeout=120, follow_redirects=True) as client:
        for url, label in urls:
            try:
                with client.stream("GET", url) as resp:
                    resp.raise_for_status()
                    ext = Path(url.split("?", 1)[0]).suffix or _extension_for_content_type(resp.headers.get("content-type", ""))
                    if ext == ".bin" and "webp" in url:
                        ext = ".webp"
                    file_path = save_dir / f"{rule.platform}_{content_id}_{label}{ext}"
                    with open(file_path, "wb") as file:
                        for chunk in resp.iter_bytes():
                            file.write(chunk)
                saved.append(str(file_path))
            except Exception:
                continue
    return saved


def _row_image_urls(row: dict) -> list[str]:
    value = row.get("image_list") or row.get("image_urls") or ""
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value or "").strip()
    if not text:
        return []
    try:
        parsed = json.loads(text)
    except Exception:
        parsed = None
    if isinstance(parsed, list):
        urls: list[str] = []
        for item in parsed:
            if isinstance(item, str):
                urls.append(item.strip())
            elif isinstance(item, dict):
                url = str(item.get("url") or item.get("trace_id") or "").strip()
                if url.startswith(("http://", "https://")):
                    urls.append(url)
        return [url for url in urls if url]
    return [item.strip() for item in text.split(",") if item.strip().startswith(("http://", "https://"))]


def _organize_poster_assets(note: HotNote, poster_dir: Path, paths: list[str]) -> None:
    images_dir = poster_dir / "images"
    for path_text in paths:
        source_path = Path(path_text)
        if not source_path.exists():
            continue
        name = source_path.name
        suffix = source_path.suffix or ".bin"
        if "_cover" in name:
            images_dir.mkdir(parents=True, exist_ok=True)
            target_path = images_dir / f"cover{suffix}"
            note.cover_path = str(target_path)
        elif "_image" in name:
            images_dir.mkdir(parents=True, exist_ok=True)
            image_index = _asset_index(name)
            target_path = images_dir / f"image_{image_index}{suffix}"
            note.image_paths.append(str(target_path))
        elif "_video" in name:
            target_path = poster_dir / f"video{suffix}"
            note.video_path = str(target_path)
        else:
            continue
        if source_path != target_path:
            if target_path.exists():
                target_path.unlink()
            shutil.move(str(source_path), str(target_path))
    note.image_paths = sorted(note.image_paths, key=_asset_index)


def _write_note_json(path: Path, note: HotNote) -> None:
    path.write_text(json.dumps(note.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")


def _query_xhs_json_notes(data_dir: Path, keyword: str) -> List[dict]:
    rows: List[dict] = []
    for path in sorted(data_dir.glob("*contents*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(data, list):
            continue
        for item in data:
            if not isinstance(item, dict):
                continue
            if str(item.get("source_keyword") or "").strip() != keyword:
                continue
            rows.append(item)
    return rows


def _parse_count(value) -> int:
    if value is None:
        return 0
    if isinstance(value, int):
        return value
    text = str(value).strip().replace(",", "")
    if not text:
        return 0
    multiplier = 1
    if text.endswith("万"):
        multiplier = 10000
        text = text[:-1]
    try:
        return int(float(text) * multiplier)
    except (ValueError, TypeError):
        return 0


def _time_ms(value) -> int:
    try:
        timestamp = int(float(str(value or "0").strip()))
    except (ValueError, TypeError):
        return 0
    if timestamp and timestamp < 10_000_000_000:
        return timestamp * 1000
    return timestamp


def _extension_for_content_type(content_type: str) -> str:
    content_type = content_type.split(";", 1)[0].strip().lower()
    return {
        "image/jpeg": ".jpg",
        "image/jpg": ".jpg",
        "image/png": ".png",
        "image/webp": ".webp",
        "image/gif": ".gif",
        "video/mp4": ".mp4",
    }.get(content_type, ".bin")


def _safe_path_part(value: str, *, max_length: int = 80) -> str:
    text = re.sub(r"[\\/:*?\"<>|\s]+", "_", str(value or "").strip())
    text = re.sub(r"_+", "_", text).strip("._")
    return (text or "unknown")[:max_length]


def _asset_index(value: str) -> int:
    match = re.search(r"image_(\d+)", str(value))
    if not match:
        return 0
    return int(match.group(1))


def _row_to_hot_note(row: dict, keyword: str) -> HotNote:
    tag_list = row.get("tag_list") or ""
    tags: List[str] = []
    if tag_list:
        try:
            parsed = json.loads(tag_list)
            if isinstance(parsed, list):
                for tag in parsed:
                    if isinstance(tag, dict):
                        name = str(tag.get("name") or "").strip()
                        if name:
                            tags.append(name)
                    elif isinstance(tag, str):
                        name = tag.strip()
                        if name:
                            tags.append(name)
        except Exception:
            tags = [item.strip() for item in str(tag_list).split(",") if item.strip()]

    image_list = row.get("image_list") or ""
    image_count = 0
    if image_list:
        try:
            parsed = json.loads(image_list)
            if isinstance(parsed, list):
                image_count = len(parsed)
        except Exception:
            image_count = len([item for item in str(image_list).split(",") if item.strip()])

    return HotNote(
        note_id=str(row.get("note_id") or ""),
        keyword=keyword,
        title=str(row.get("title") or "").strip(),
        desc=str(row.get("desc") or "").strip(),
        author_id=str(row.get("user_id") or ""),
        author_name=str(row.get("nickname") or ""),
        liked=_parse_count(row.get("liked_count")),
        collected=_parse_count(row.get("collected_count")),
        comment=_parse_count(row.get("comment_count")),
        share=_parse_count(row.get("share_count")),
        tags=tags,
        image_count=image_count,
        note_type=str(row.get("type") or ""),
        note_url=str(row.get("note_url") or ""),
        time_ms=_time_ms(row.get("time")),
    )
