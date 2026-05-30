"""Session report artifact helpers for XHS hot-note analysis."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from nori.agents.market_analysis.note_skill_fixture import note_skill_fixture
from nori.agents.market_analysis.models import SessionSkillReport


def report_stamp(source_keyword_dirs: dict[str, str]) -> str:
    for path_text in source_keyword_dirs.values():
        name = Path(path_text).name
        match = re.match(r"(\d{8}_\d{6})_", name)
        if match:
            return match.group(1)
    return "session"


def skills_output(report: SessionSkillReport) -> dict[str, Any]:
    return note_skill_fixture(report)


def write_session_outputs(report: SessionSkillReport) -> dict[str, Path]:
    if not report.source_data_dir:
        return {}

    stamp = report_stamp(report.source_keyword_dirs)
    output_dir = Path(report.source_data_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    report_path = output_dir / f"{stamp}_session_skill_report.json"
    report_path.write_text(
        json.dumps(report.to_dict(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    skills_path = output_dir / f"{stamp}_note_skill_guides.json"
    skills_path.write_text(
        json.dumps(skills_output(report), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return {"report": report_path, "skills": skills_path}


__all__ = ["report_stamp", "skills_output", "write_session_outputs"]
