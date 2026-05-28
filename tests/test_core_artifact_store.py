from __future__ import annotations

import json

from nori.core import ArtifactStore


def test_artifact_store_writes_stage_json_and_manifest(tmp_path):
    store = ArtifactStore(tmp_path)

    saved = store.save_stage("intent", {"brand": "Holly"}, input_refs=["brief.md"])

    assert saved.stage == "intent"
    assert saved.path == tmp_path / "intent.json"
    assert saved.exists
    assert store.load_stage("intent") == {"brand": "Holly"}
    manifest = json.loads((tmp_path / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["artifacts"]["intent"]["path"] == "intent.json"
    assert manifest["artifacts"]["intent"]["input_refs"] == ["brief.md"]


def test_artifact_store_resume_prefers_existing_stage(tmp_path):
    store = ArtifactStore(tmp_path)
    store.save_stage("market", {"count": 2})
    calls = []

    value = store.get_or_build("market", lambda: calls.append("called") or {"count": 3})

    assert value == {"count": 2}
    assert calls == []
