"""Cover image persistence helper for CoverDirector."""
from __future__ import annotations

import base64
import re
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, TypeVar


ErrorT = TypeVar("ErrorT", bound=Exception)
UrlOpen = Callable[..., Any]


def save_image(
    payload: str,
    out_dir: Path,
    skill_id: str,
    *,
    error_type: type[ErrorT],
    urlopen: UrlOpen | None = None,
) -> Path:
    """Persist a data-uri or remote URL image payload to the cover output directory."""
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_id = re.sub(r"[^\w\-]+", "_", skill_id)[:40] or "cover"

    if payload.startswith("data:"):
        header, _, b64 = payload.partition(",")
        mime = header.split(":", 1)[-1].split(";")[0] if ":" in header else "image/png"
        ext = mime.split("/")[-1] or "png"
        path = out_dir / f"cover_{safe_id}_{ts}.{ext}"
        try:
            path.write_bytes(base64.b64decode(b64))
        except (ValueError, TypeError) as exc:
            raise error_type(f"data-uri base64 解析失败: {exc}") from exc
        return path

    path = out_dir / f"cover_{safe_id}_{ts}.png"
    open_url = urlopen or urllib.request.urlopen
    try:
        req = urllib.request.Request(payload, headers={"User-Agent": "nori-cover-director/1.0"})
        with open_url(req, timeout=60) as resp:
            path.write_bytes(resp.read())
    except Exception as exc:  # noqa: BLE001
        raise error_type(f"下载封面失败: {type(exc).__name__}: {exc}") from exc
    return path
