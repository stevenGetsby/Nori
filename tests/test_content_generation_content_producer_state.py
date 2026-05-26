"""Tests for ContentProducer task/project state helpers."""

from __future__ import annotations

from nori.core import AccountOperationProject
from nori.core import ContentTask

from nori.content_generation.content_producer import state as content_production_state
from nori.content_generation.models import ContentPackage


def _task() -> ContentTask:
    return ContentTask(task_id="task_001", package_id="", status="planned")


def _package() -> ContentPackage:
    return ContentPackage(package_id="pkg_task_001", task_id="task_001")


def test_production_error_classifies_stage_and_formats_contract():
    note_error = RuntimeError("llm down")
    cover_error = type("CoverGenerationError", (RuntimeError,), {})("bad cover")

    note = content_production_state.production_error(note_error, _task())
    cover = content_production_state.production_error(cover_error, _task())

    assert note["stage"] == "production"
    assert note["task_id"] == "task_001"
    assert note["error_type"] == "RuntimeError"
    assert "llm down" in note["message"]
    assert cover["stage"] == "cover"


def test_attach_error_marks_task_failed_and_appends_project_error():
    task = _task()
    project = AccountOperationProject(project_id="ops_001")
    error = {"stage": "production", "task_id": "task_001", "message": "failed"}

    content_production_state.attach_error(task, project, error)

    assert task.status == "failed"
    assert task.metadata["production_error"] == error
    assert project.metadata["production_errors"] == [error]


def test_attach_success_marks_task_drafted_and_attaches_project_package():
    task = _task()
    package = _package()
    project = AccountOperationProject(project_id="ops_001")

    content_production_state.attach_success(task, project, package)

    assert task.package_id == "pkg_task_001"
    assert task.status == "drafted"
    assert task.metadata["production"] == {
        "status": "drafted",
        "package_id": "pkg_task_001",
        "producer": "ContentProducerAgent",
    }
    assert project.content_packages == [package]
    assert project.metadata["last_produced_package_id"] == "pkg_task_001"
