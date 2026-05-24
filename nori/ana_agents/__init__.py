"""Analysis and learning agents for Nori."""
from __future__ import annotations

__all__ = ["XHSNoteAnalyzer"]


def __getattr__(name: str):
	if name in __all__:
		from .xhs_note_analyzer import XHSNoteAnalyzer

		return {"XHSNoteAnalyzer": XHSNoteAnalyzer}[name]
	raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
