"""Stable object-key construction for Nori runtime uploads."""
from __future__ import annotations

import hashlib
import re
from datetime import datetime
from pathlib import Path


DEFAULT_REFERENCE_PREFIX = "nori/reference-images"


def reference_image_key(
    *,
    prefix: str,
    project: str,
    session: str,
    source_path: str,
    payload: bytes,
    content_type: str,
    now: datetime | None = None,
) -> str:
    """Build a traceable, content-addressed key for one reference image."""
    now = now or datetime.now()
    root = clean_prefix(prefix or DEFAULT_REFERENCE_PREFIX)
    project_slug = slug(project or "nori")
    session_slug = slug(session or "session")
    digest = hashlib.sha256(payload).hexdigest()[:16]
    stem = slug(Path(source_path).stem or "reference")
    ext = extension_for(source_path, content_type)
    return f"{root}/{project_slug}/{session_slug}/{now:%Y%m%d}/{digest}_{stem}{ext}"


def clean_prefix(value: str) -> str:
    return str(value or "").strip().strip("/") or DEFAULT_REFERENCE_PREFIX


def slug(value: str, *, limit: int = 80) -> str:
    text = re.sub(r"[^\w.-]+", "-", str(value or "").strip(), flags=re.UNICODE)
    text = text.strip("-_.")
    return (text[:limit].strip("-_.") or "item")


def extension_for(source_path: str, content_type: str) -> str:
    mime = str(content_type or "").lower()
    if mime == "image/jpeg":
        return ".jpg"
    if mime == "image/png":
        return ".png"
    if mime == "image/webp":
        return ".webp"
    if mime == "image/gif":
        return ".gif"
    suffix = Path(source_path).suffix.lower()
    return suffix if suffix in {".jpg", ".jpeg", ".png", ".webp", ".gif"} else ".png"


__all__ = ["DEFAULT_REFERENCE_PREFIX", "clean_prefix", "extension_for", "reference_image_key", "slug"]
