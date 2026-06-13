from __future__ import annotations

import json
import time
from pathlib import Path

from backend.jobs import InProcessExperimentJobStore


def test_job_store_persists_repo_relative_paths(tmp_path):
    storage_root = tmp_path / "data" / "backend" / "jobs"
    run_dir = tmp_path / "cases" / "Holly" / "runs" / "run_1"
    asset_path = tmp_path / "data" / "backend" / "uploads" / "session_1" / "asset.png"
    run_dir.mkdir(parents=True)
    asset_path.parent.mkdir(parents=True)
    asset_path.write_bytes(b"image")

    store = InProcessExperimentJobStore(storage_root=storage_root)
    job = store.submit(
        job_type="content_production",
        metadata={"case_id": "Holly", "run_dir": str(run_dir)},
        target=lambda: {
            "workflow_name": "content_production",
            "run_id": "run_1",
            "run_dir": str(run_dir),
            "status": "succeeded",
            "asset_paths": [str(asset_path)],
            "artifact_paths": {"run": str(run_dir / "run.json")},
        },
    )

    final_job = None
    for _ in range(20):
        final_job = store.get(job["job_id"])
        if final_job and final_job["status"] == "succeeded":
            break
        time.sleep(0.01)

    assert final_job is not None
    assert final_job["metadata"]["run_dir"] == "cases/Holly/runs/run_1"
    assert final_job["result"]["run_dir"] == "cases/Holly/runs/run_1"
    assert final_job["result"]["asset_paths"] == ["data/backend/uploads/session_1/asset.png"]
    assert final_job["result"]["artifact_paths"]["run"] == "cases/Holly/runs/run_1/run.json"

    job_file = storage_root / f"{job['job_id']}.json"
    persisted = json.loads(job_file.read_text(encoding="utf-8"))
    assert str(tmp_path) not in job_file.read_text(encoding="utf-8")
    assert persisted["result"]["run_dir"] == "cases/Holly/runs/run_1"

    restored = InProcessExperimentJobStore(storage_root=storage_root, max_workers=1).get(job["job_id"])
    assert restored["result"]["asset_paths"] == ["data/backend/uploads/session_1/asset.png"]
