"""Path serialization helpers."""
from __future__ import annotations

from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse


def repo_relative_path(value: str | Path, root: str | Path) -> str:
    """Return a repo-relative string when ``value`` is inside ``root``."""

    text = str(value or "")
    if not text:
        return ""

    root_path = Path(root)
    for root_text in _root_texts(root_path):
        if text == root_text:
            return "."
        prefix = f"{root_text}/"
        if text.startswith(prefix):
            return text[len(prefix) :]

    file_url_path = _file_url_path(text)
    if file_url_path is not None:
        rel = repo_relative_path(file_url_path, root_path)
        return rel if rel != str(file_url_path) else text

    path = Path(text)
    if not path.is_absolute():
        return text
    try:
        return str(path.resolve(strict=False).relative_to(root_path.resolve(strict=False)))
    except (OSError, RuntimeError, ValueError):
        return text


def make_portable_paths(value: Any, root: str | Path | None) -> Any:
    """Recursively convert repo-local absolute paths to repo-relative strings."""

    if root is None:
        return value
    if isinstance(value, Path):
        return repo_relative_path(value, root)
    if isinstance(value, str):
        portable = repo_relative_path(value, root)
        if portable != value:
            return portable
        return _replace_embedded_root_prefixes(value, Path(root))
    if isinstance(value, list):
        return [make_portable_paths(item, root) for item in value]
    if isinstance(value, tuple):
        return [make_portable_paths(item, root) for item in value]
    if isinstance(value, dict):
        return {
            make_portable_paths(key, root) if isinstance(key, (str, Path)) else key: make_portable_paths(item, root)
            for key, item in value.items()
        }
    return value


def infer_project_root_from_cases_path(path: str | Path) -> Path | None:
    parts = Path(path).resolve(strict=False).parts
    for index, part in enumerate(parts):
        if part == "cases" and index > 0:
            return Path(*parts[:index])
    return None


def infer_project_root_from_backend_jobs_path(path: str | Path) -> Path | None:
    parts = Path(path).resolve(strict=False).parts
    for index in range(0, max(0, len(parts) - 2)):
        if parts[index : index + 3] == ("data", "backend", "jobs") and index > 0:
            return Path(*parts[:index])
    return None


def _replace_embedded_root_prefixes(value: str, root: Path) -> str:
    text = value
    for root_text in _root_texts(root):
        text = text.replace(f"{root_text}/", "")
    return text


def _root_texts(root: Path) -> tuple[str, ...]:
    texts = {str(root)}
    try:
        texts.add(str(root.resolve(strict=False)))
    except (OSError, RuntimeError):
        pass
    return tuple(text.rstrip("/") for text in texts if text)


def _file_url_path(value: str) -> Path | None:
    if not value.startswith("file://"):
        return None
    parsed = urlparse(value)
    if parsed.scheme != "file" or not parsed.path:
        return None
    return Path(unquote(parsed.path))


__all__ = [
    "infer_project_root_from_backend_jobs_path",
    "infer_project_root_from_cases_path",
    "make_portable_paths",
    "repo_relative_path",
]
