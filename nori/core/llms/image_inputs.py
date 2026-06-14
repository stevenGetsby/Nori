"""Image input normalization helpers for the LLM gateway."""
from __future__ import annotations

import base64
from pathlib import Path
from typing import Any


def load_image_bytes(item: Any) -> bytes:
    """Normalize supported image input shapes to bytes.

    Invalid or unreadable values return empty bytes so callers can filter them
    before deciding whether a request is text-to-image or image-to-image.
    """
    if item is None:
        return b""
    if isinstance(item, (bytes, bytearray)):
        return bytes(item)
    if isinstance(item, Path):
        try:
            return item.read_bytes()
        except Exception:  # noqa: BLE001
            return b""
    if isinstance(item, str):
        value = item.strip()
        if not value:
            return b""
        if value.startswith("data:"):
            _, _, payload = value.partition(",")
            try:
                return base64.b64decode(payload)
            except Exception:  # noqa: BLE001
                return b""
        if value.startswith(("http://", "https://")):
            return b""
        try:
            path = Path(value)
            if path.is_file():
                return path.read_bytes()
        except Exception:  # noqa: BLE001
            pass
        try:
            return base64.b64decode(value, validate=True)
        except Exception:  # noqa: BLE001
            return b""
    return b""


def load_image_url(item: Any) -> str:
    """Return a remote image URL reference if the input is already URL-shaped."""
    if not isinstance(item, str):
        return ""
    value = item.strip()
    if value.startswith(("http://", "https://")):
        return value
    return ""


def split_reference_images(items: list[Any] | None) -> tuple[list[bytes], list[str]]:
    """Split caller references into local bytes and remote image URLs."""
    ref_bytes: list[bytes] = []
    ref_urls: list[str] = []
    for item in items or []:
        url = load_image_url(item)
        if url:
            ref_urls.append(url)
            continue
        raw = load_image_bytes(item)
        if raw:
            ref_bytes.append(raw)
    return ref_bytes, ref_urls


def bytes_to_data_uri(raw: bytes) -> str:
    return f"data:{sniff_mime(raw)};base64,{base64.b64encode(raw).decode()}"


def sniff_mime(raw: bytes) -> str:
    if raw.startswith(b"\x89PNG"):
        return "image/png"
    if raw[:3] == b"\xff\xd8\xff":
        return "image/jpeg"
    if raw[:6] in (b"GIF87a", b"GIF89a"):
        return "image/gif"
    if raw[:4] == b"RIFF" and raw[8:12] == b"WEBP":
        return "image/webp"
    return "image/png"
