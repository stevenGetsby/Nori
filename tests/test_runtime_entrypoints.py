from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=10,
        check=False,
    )


def test_main_default_reports_real_entrypoints_without_stale_server_import():
    result = _run("main.py")

    assert result.returncode == 0
    assert "当前没有内置 web server 入口" in result.stdout
    assert "scripts/run_holly_live_case.py" in result.stdout


def test_smoke_scripts_import_from_canonical_modules_and_expose_help():
    for script in ("scripts/smoke_note_maker.py", "scripts/smoke_session_skill.py", "scripts/backend_holly_smoke.py"):
        result = _run(script, "--help")

        assert result.returncode == 0, result.stderr
        assert "usage:" in result.stdout


def test_runtime_entrypoints_do_not_reference_removed_legacy_roots():
    removed = (
        "nori.agent_models",
        "nori.gen_agents",
        "nori.ana_agents",
        "nori.ops_agents",
        "nori.ops_models",
        "nori.agent_utils",
        "nori.nori.server",
    )
    paths = [
        ROOT / "main.py",
        ROOT / "scripts" / "smoke_note_maker.py",
        ROOT / "scripts" / "smoke_session_skill.py",
        ROOT / "scripts" / "run_holly_live_case.py",
        ROOT / "scripts" / "continue_holly_live_case.py",
        ROOT / "scripts" / "backend_holly_smoke.py",
    ]
    text = "\n".join(path.read_text(encoding="utf-8") for path in paths)

    assert not any(name in text for name in removed)
