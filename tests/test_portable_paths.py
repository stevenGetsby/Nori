from __future__ import annotations

from pathlib import Path

from nori.core.paths import make_portable_paths, repo_relative_path


def test_repo_relative_path_handles_plain_and_file_url_paths(tmp_path):
    asset = tmp_path / "cases" / "Holly" / "asset.png"

    assert repo_relative_path(asset, tmp_path) == "cases/Holly/asset.png"
    assert repo_relative_path(f"file://{asset}", tmp_path) == "cases/Holly/asset.png"


def test_make_portable_paths_handles_nested_values_and_embedded_text(tmp_path):
    run_dir = tmp_path / "cases" / "Holly" / "runs" / "run_1"
    data = {
        str(run_dir / "run.json"): {
            "run_dir": str(run_dir),
            "summary": f"Run dir: `{run_dir}`",
        }
    }

    assert make_portable_paths(data, tmp_path) == {
        "cases/Holly/runs/run_1/run.json": {
            "run_dir": "cases/Holly/runs/run_1",
            "summary": "Run dir: `cases/Holly/runs/run_1`",
        }
    }
