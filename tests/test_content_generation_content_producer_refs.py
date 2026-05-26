"""Tests for ContentPackage provenance helpers."""

from __future__ import annotations

from nori.core import AccountOperationProject
from nori.core import ContentTask, ClientBrief

from nori.content_generation.models import UserAsset
from nori.content_generation.content_producer import refs as content_package_refs


def _task() -> ContentTask:
    return ContentTask(
        task_id="task_001",
        title="母亲节花束搭配",
        required_assets=["product_photo"],
        references=[{"source": "benchmark_note", "note_id": "xhs_001"}],
    )


def _brief() -> ClientBrief:
    return ClientBrief(client_name="花店主理人", brand_name="春日花房")


def test_material_usage_records_input_assets_and_required_assets():
    rows = content_package_refs.material_usage(
        [UserAsset(kind="text", text="卖点" * 80, usable_for=["copy"])],
        _task(),
    )

    assert rows[0]["source"] == "input_asset"
    assert rows[0]["kind"] == "text"
    assert rows[0]["text_preview"] == ("卖点" * 80)[:120]
    assert rows[0]["usable_for"] == ["copy"]
    assert {"source": "task_required_asset", "kind": "product_photo"} in rows


def test_source_refs_collects_task_skill_brief_and_project_sources():
    refs = content_package_refs.source_refs(
        _task(),
        [{"skill_id": "flower_skill", "label": "花店种草"}],
        _brief(),
        AccountOperationProject(project_id="ops_001"),
    )

    assert {"source": "benchmark_note", "note_id": "xhs_001"} in refs
    assert {"source": "note_skill", "skill_id": "flower_skill", "label": "花店种草"} in refs
    assert {"source": "client_brief", "client_name": "花店主理人", "brand_name": "春日花房"} in refs
    assert {"source": "account_operation_project", "project_id": "ops_001"} in refs


def test_package_id_and_image_paths_are_stable_and_deduped():
    assert content_package_refs.package_id_for_task(_task()) == "pkg_task_001"
    assert content_package_refs.slug(" 母亲节 花束! ") == "母亲节_花束"
    assert content_package_refs.dedupe(["/tmp/a.jpg", "", "/tmp/a.jpg", "/tmp/b.jpg"]) == [
        "/tmp/a.jpg",
        "/tmp/b.jpg",
    ]
