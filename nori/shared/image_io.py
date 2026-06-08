"""共享图片预处理：压缩 + 编码，给 vision LLM / 图生图 API 用。

- 单图 → data-uri：给 nori.core.llms.chat 的 vision content 用
- 单图 → bytes   ：给 nori.core.llms.image 的 reference_images 用

超过 `max_bytes` 的图会被缩放到 `max_long_edge` 并转为 JPEG（质量 `jpeg_quality`）。
"""
from __future__ import annotations

import base64
import io
import mimetypes
from pathlib import Path

from PIL import Image


# 默认上限：vision / 图生图 单图建议 <= 1.5MB，长边 <= 1280
DEFAULT_MAX_LONG_EDGE = 1280
DEFAULT_JPEG_QUALITY = 85
DEFAULT_MAX_BYTES = 1_500_000


def image_to_data_uri(
    path: str | Path,
    *,
    max_long_edge: int = DEFAULT_MAX_LONG_EDGE,
    jpeg_quality: int = DEFAULT_JPEG_QUALITY,
    max_bytes: int = DEFAULT_MAX_BYTES,
) -> str:
    """读图并按需压缩，返回 data:image/...;base64,... 字符串。

    读取失败或压缩失败返回 ""。
    """
    p = Path(path)
    if not p.is_file():
        return ""
    try:
        raw = p.read_bytes()
    except OSError:
        return ""
    if len(raw) <= max_bytes:
        mime, _ = mimetypes.guess_type(p.name)
        mime = mime or "image/png"
        return f"data:{mime};base64,{base64.b64encode(raw).decode('ascii')}"
    compressed = _compress_to_jpeg(raw, max_long_edge=max_long_edge, jpeg_quality=jpeg_quality)
    if not compressed:
        return ""
    return f"data:image/jpeg;base64,{base64.b64encode(compressed).decode('ascii')}"


def image_to_bytes(
    path: str | Path,
    *,
    max_long_edge: int = DEFAULT_MAX_LONG_EDGE,
    jpeg_quality: int = DEFAULT_JPEG_QUALITY,
    max_bytes: int = DEFAULT_MAX_BYTES,
) -> bytes:
    """读图并按需压缩，返回原始 bytes（不带 data-uri 头）。

    读取失败或压缩失败返回 b""。
    """
    p = Path(path)
    if not p.is_file():
        return b""
    try:
        raw = p.read_bytes()
    except OSError:
        return b""
    if len(raw) <= max_bytes:
        return raw
    return _compress_to_jpeg(raw, max_long_edge=max_long_edge, jpeg_quality=jpeg_quality)


def _compress_to_jpeg(raw: bytes, *, max_long_edge: int, jpeg_quality: int) -> bytes:
    try:
        img = Image.open(io.BytesIO(raw))
        img = _flatten_to_rgb(img)
        w, h = img.size
        scale = max_long_edge / max(w, h)
        if scale < 1.0:
            img = img.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=jpeg_quality, optimize=True)
        return buf.getvalue()
    except Exception:  # noqa: BLE001 - 压缩失败由调用方降级处理
        return b""


def _flatten_to_rgb(img: Image.Image) -> Image.Image:
    """JPEG 不支持 alpha；带透明的图填白底转 RGB。"""
    if img.mode == "P":
        img = img.convert("RGBA")
    if img.mode in ("RGBA", "LA"):
        bg = Image.new("RGB", img.size, (255, 255, 255))
        mask = img.split()[-1]
        bg.paste(img.convert("RGB"), mask=mask)
        return bg
    if img.mode != "RGB":
        return img.convert("RGB")
    return img


__all__ = ["image_to_bytes", "image_to_data_uri"]
