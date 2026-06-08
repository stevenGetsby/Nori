"""Session-scoped asset persistence for backend experiments."""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path
from typing import Any
from uuid import uuid4

from fastapi import UploadFile


ALLOWED_IMAGE_SUFFIXES = {".gif", ".jpeg", ".jpg", ".png", ".webp"}


def save_uploaded_asset(
    *,
    upload: UploadFile,
    upload_root: str | Path,
    session_id: str,
    task_id: str = "",
    usage: str = "reference",
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Persist one uploaded image and return its stable asset row."""

    filename = _safe_filename(upload.filename or "asset")
    suffix = Path(filename).suffix.lower()
    content_type = str(upload.content_type or "")
    if suffix not in ALLOWED_IMAGE_SUFFIXES and not content_type.startswith("image/"):
        raise ValueError(f"unsupported asset type: {upload.filename or content_type or 'unknown'}")

    asset_id = f"asset_{uuid4().hex[:12]}"
    target_dir = Path(upload_root) / _safe_segment(session_id)
    target_dir.mkdir(parents=True, exist_ok=True)
    path = target_dir / f"{asset_id}_{filename}"

    upload.file.seek(0)
    with path.open("wb") as out:
        shutil.copyfileobj(upload.file, out)

    row = {
        "asset_id": asset_id,
        "session_id": session_id,
        "task_id": task_id,
        "kind": "image",
        "path": str(path),
        "filename": filename,
        "content_type": content_type,
        "size_bytes": path.stat().st_size,
        "usage": usage,
        "metadata": dict(metadata or {}),
    }
    (target_dir / f"{asset_id}.json").write_text(json.dumps(row, ensure_ascii=False, indent=2), encoding="utf-8")
    return row


def append_session_assets(existing: list[dict[str, Any]] | None, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = {str(row.get("asset_id") or ""): dict(row) for row in existing or [] if row.get("asset_id")}
    for row in rows:
        by_id[str(row["asset_id"])] = dict(row)
    return list(by_id.values())


def select_assets(
    rows: list[dict[str, Any]],
    *,
    asset_ids: list[str] | None = None,
) -> list[dict[str, Any]]:
    selected_ids = [str(value).strip() for value in asset_ids or [] if str(value).strip()]
    if not selected_ids:
        return [dict(row) for row in rows if row.get("kind") == "image"]
    by_id = {str(row.get("asset_id") or ""): row for row in rows}
    missing = [asset_id for asset_id in selected_ids if asset_id not in by_id]
    if missing:
        raise ValueError(f"asset not found in session: {missing}")
    return [dict(by_id[asset_id]) for asset_id in selected_ids]


def parse_metadata_json(value: str = "") -> dict[str, Any]:
    text = str(value or "").strip()
    if not text:
        return {}
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("metadata_json must be a JSON object")
    return data


def _safe_filename(value: str) -> str:
    name = Path(value).name.strip() or "asset"
    safe = re.sub(r"[^A-Za-z0-9._@+-]+", "_", name)
    return safe[:160].strip("._") or "asset"


def _safe_segment(value: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9_-]+", "_", str(value or "").strip())
    return safe[:80].strip("_") or "session"


__all__ = [
    "ALLOWED_IMAGE_SUFFIXES",
    "append_session_assets",
    "parse_metadata_json",
    "save_uploaded_asset",
    "select_assets",
]
