#!/usr/bin/env python3
"""Print a redacted Nori project status summary for Codex iterations."""
from __future__ import annotations

import json
import sys
from pathlib import Path


def _repo_root() -> Path:
    if len(sys.argv) > 1:
        return Path(sys.argv[1]).expanduser().resolve()
    return Path.cwd().resolve()


def main() -> int:
    root = _repo_root()
    if not (root / "nori").is_dir():
        print(json.dumps({"error": "run from Nori repo root", "root": str(root)}, ensure_ascii=False, indent=2))
        return 1

    sys.path.insert(0, str(root))
    tests_dir = root / "tests"
    status: dict[str, object] = {
        "root": str(root),
        "exists": {
            "nori": (root / "nori").is_dir(),
            "llms": (root / "llms").is_dir(),
            "data_collect": (root / "data_collect").is_dir(),
            "tests": tests_dir.is_dir(),
            "api_config": (root / "api_config.yaml").is_file(),
            "progress": (root / "进度.md").is_file(),
            "automation_plan": (root / "文档" / "Codex自动化推进计划.md").is_file(),
            "project_skill": (root / "文档" / "codex-skills" / "nori-project-operator" / "SKILL.md").is_file(),
        },
        "test_files": sorted(p.name for p in tests_dir.glob("test_*.py")) if tests_dir.is_dir() else [],
        "legacy_packages": {
            "gen_agents": (root / "nori" / "gen_agents").is_dir(),
            "ops_agents": (root / "nori" / "ops_agents").is_dir(),
            "ana_agents": (root / "nori" / "ana_agents").is_dir(),
            "ops_models": (root / "nori" / "ops_models").is_dir(),
            "agent_models": (root / "nori" / "agent_models").is_dir(),
            "agent_utils": (root / "nori" / "agent_utils").is_dir(),
        },
    }

    try:
        from nori.nori_config import NoriConfig

        cfg = NoriConfig(root / "api_config.yaml")
        status["mode"] = cfg.mode
        status["active_models"] = cfg.active_summary
    except Exception as exc:  # noqa: BLE001
        status["config_error"] = f"{type(exc).__name__}: {exc}"

    print(json.dumps(status, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
