from __future__ import annotations

import re
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {
    ".css",
    ".html",
    ".js",
    ".json",
    ".jsonl",
    ".jsx",
    ".md",
    ".mjs",
    ".py",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".yaml",
    ".yml",
}

MACHINE_LOCAL_PREFIXES = (
    "/" + "Users" + "/",
    "/" + "home" + "/",
    "/" + "Volumes" + "/",
)
LOCAL_POSIX_PATH_RE = re.compile(
    r"(^|[\s\"'`([{:=])(" + "|".join(re.escape(prefix) for prefix in MACHINE_LOCAL_PREFIXES) + r")"
)
FILE_URL_RE = re.compile("file" + r"://[^\s\"'`)]+")
WINDOWS_PATH_RE = re.compile(r"(^|[\s\"'`([{=])([A-Za-z]:\\[^\s\"'`)]+)")


def _tracked_text_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
    )
    files: list[Path] = []
    for raw in result.stdout.split(b"\0"):
        if not raw:
            continue
        path = REPO_ROOT / raw.decode("utf-8")
        if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
            files.append(path)
    for extra in (REPO_ROOT / "AGENTS.md",):
        if extra.is_file():
            files.append(extra)
    return files


def _line_findings(path: Path) -> list[str]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        return []

    findings: list[str] = []
    for line_number, line in enumerate(lines, start=1):
        if LOCAL_POSIX_PATH_RE.search(line) or FILE_URL_RE.search(line) or WINDOWS_PATH_RE.search(line):
            rel = path.relative_to(REPO_ROOT)
            findings.append(f"{rel}:{line_number}: {line.strip()[:180]}")
    return findings


def test_tracked_text_files_do_not_contain_machine_local_paths():
    findings: list[str] = []
    for path in _tracked_text_files():
        findings.extend(_line_findings(path))

    assert not findings, "Machine-local paths must not be committed:\n" + "\n".join(findings[:80])
