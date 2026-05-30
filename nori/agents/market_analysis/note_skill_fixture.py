"""Fixture IO helpers for learned NoteSkill records."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from nori.agents.market_analysis.models import NoteSkill, SessionSkillReport


def note_skill_fixture(value: Any) -> dict[str, Any]:
    """Return the stable skills-only JSON shape accepted by NoteMaker tests."""

    return {"skills": [skill.to_dict() for skill in load_note_skills(value)]}


def write_note_skill_fixture(value: Any, path: str | Path) -> Path:
    """Write a skills-only fixture JSON and return its path."""

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(note_skill_fixture(value), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return output_path


def load_note_skills(source: Any) -> list[NoteSkill]:
    """Load NoteSkill objects from a report, skills-only fixture, list, or JSON path."""

    if isinstance(source, (str, Path)):
        data = json.loads(Path(source).read_text(encoding="utf-8"))
        return load_note_skills(data)
    if isinstance(source, SessionSkillReport):
        return list(source.skills)
    if isinstance(source, NoteSkill):
        return [source]
    if isinstance(source, dict):
        if "skills" in source:
            return load_note_skills(source.get("skills"))
        raise ValueError("NoteSkill fixture dict must contain a 'skills' key")
    if isinstance(source, list):
        return [_normalize_skill(item) for item in source if item]
    raise TypeError(f"Unsupported NoteSkill source: {type(source)!r}")


def _normalize_skill(value: Any) -> NoteSkill:
    if isinstance(value, NoteSkill):
        return value
    if isinstance(value, dict):
        return NoteSkill.from_dict(value)
    raise TypeError(f"Unsupported NoteSkill item: {type(value)!r}")


__all__ = [
    "load_note_skills",
    "note_skill_fixture",
    "write_note_skill_fixture",
]
