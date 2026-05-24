"""Case log helpers shared by generation and analysis agents."""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


def write_agent_log(
    *,
    agent: str,
    case: str,
    input_data: dict[str, Any],
    output_data: dict[str, Any],
    config: dict[str, Any] | None = None,
    log_dir: str | Path = "log",
) -> Path:
    """Write one agent test case input/output snapshot to log/ as JSON."""
    created_at = datetime.now()
    payload = {
        "agent": agent,
        "case": case,
        "created_at": created_at.isoformat(timespec="seconds"),
        "config": dict(config or {}),
        "input": input_data,
        "output": output_data,
    }
    directory = Path(log_dir)
    directory.mkdir(parents=True, exist_ok=True)
    stem = f"{_slug(agent)}_{_slug(case)}_{created_at.strftime('%Y%m%d_%H%M%S_%f')}"
    path = directory / f"{stem}.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    return path


def _slug(value: str) -> str:
    text = str(value or "case").strip().lower()
    text = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "_", text)
    text = text.strip("_")
    return text or "case"
