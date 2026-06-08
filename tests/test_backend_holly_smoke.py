from __future__ import annotations

from types import SimpleNamespace

import pytest

from backend.reference_urls import provider_fetchable_reference_url
import scripts.backend_holly_smoke as HOLLY_SMOKE
from scripts.backend_holly_smoke import _HttpBackendClient, _assert_live_reference_base_url, _normalize_api_base_url


def test_holly_smoke_rejects_placeholder_reference_url_for_live_strict_run():
    with pytest.raises(RuntimeError, match="not a real provider-fetchable public HTTPS URL"):
        _assert_live_reference_base_url("https://backend.example.test")


def test_holly_smoke_rejects_local_reference_url_for_live_strict_run():
    with pytest.raises(RuntimeError, match="not a real provider-fetchable public HTTPS URL"):
        _assert_live_reference_base_url("https://127.0.0.1:8000")


def test_holly_smoke_accepts_public_https_reference_url_for_live_strict_run():
    _assert_live_reference_base_url("https://nori-public.nori.ai")


def test_reference_url_helper_rejects_placeholder_and_non_https_urls():
    assert provider_fetchable_reference_url("https://backend.example.test/ref.png") == ""
    assert provider_fetchable_reference_url("https://example.org/ref.png") == ""
    assert provider_fetchable_reference_url("http://assets.nori.ai/ref.png") == ""
    assert provider_fetchable_reference_url("https://assets.nori.ai/ref.png") == "https://assets.nori.ai/ref.png"


def test_holly_smoke_normalizes_running_backend_api_base_url():
    assert _normalize_api_base_url(" http://127.0.0.1:8000/ ") == "http://127.0.0.1:8000"
    assert _HttpBackendClient("http://127.0.0.1:8000/")._url("/sessions") == "http://127.0.0.1:8000/sessions"


def test_holly_smoke_rejects_invalid_running_backend_api_base_url():
    with pytest.raises(RuntimeError, match="--api-base-url must start"):
        _normalize_api_base_url("127.0.0.1:8000")


def test_holly_smoke_publishes_uploaded_assets_before_strict_preflight(monkeypatch, tmp_path):
    image_path = tmp_path / "ref.png"
    image_path.write_bytes(b"fake-png-bytes")
    calls = []

    class FakeResponse:
        def __init__(self, data, status_code=200):
            self._data = data
            self.status_code = status_code

        def json(self):
            return self._data

    class FakeClient:
        api_base_url = "http://127.0.0.1:8000"

        def __init__(self, _api_base_url):
            pass

        def post_json(self, path, payload):
            calls.append(("post_json", path, payload))
            if path == "/sessions":
                return FakeResponse({"data": {"session_id": "session_1"}})
            if path == "/sessions/session_1/assets/publish-references":
                return FakeResponse(
                    {
                        "data": {
                            "ready": True,
                            "published_count": 1,
                            "assets": [{"asset_id": "asset_1", "public_reference_url": "https://backend.nori.ai/ref.png"}],
                        }
                    }
                )
            if path == "/workflows/content-production/runs/preflight":
                return FakeResponse({"data": {"ready": True, "actions": []}})
            raise AssertionError(path)

        def post_files(self, path, *, files, data):
            calls.append(("post_files", path, data))
            return FakeResponse({"data": {"assets": [{"asset_id": "asset_1"}]}})

    monkeypatch.setattr(HOLLY_SMOKE, "_HttpBackendClient", FakeClient)
    args = SimpleNamespace(
        api_base_url="http://127.0.0.1:8000",
        backend_public_base_url="https://backend.nori.ai",
        require_image_references=True,
        verify_reference_urls=False,
        run=False,
        allow_unverified_reference_url=False,
        reference_url_probe_timeout=0.2,
        stage_timeout_seconds=0.0,
        content_package_timeout_seconds=0.0,
        execution_mode="sync",
        keep_data=False,
    )

    result = HOLLY_SMOKE._smoke(
        project_root=tmp_path,
        state_root=tmp_path,
        fixture={
            "asset_paths": [str(image_path)],
            "case_id": "Holly",
            "brief_text": "brief",
            "market_evidence": {"queries": ["q"]},
            "config": {},
        },
        args=args,
    )

    assert result["exit_code"] == 0
    assert result["payload"]["published_references"]["ready"] is True
    assert [call[1] for call in calls if call[0] == "post_json"] == [
        "/sessions",
        "/sessions/session_1/assets/publish-references",
        "/workflows/content-production/runs/preflight",
    ]
    publish_payload = next(call[2] for call in calls if call[0] == "post_json" and call[1].endswith("/publish-references"))
    assert publish_payload["asset_ids"] == ["asset_1"]
    assert publish_payload["backend_public_base_url"] == "https://backend.nori.ai"


def test_holly_smoke_can_verify_reference_urls_during_preflight_only(monkeypatch, tmp_path):
    image_path = tmp_path / "ref.png"
    image_path.write_bytes(b"fake-png-bytes")
    preflight_payloads = []

    class FakeResponse:
        def __init__(self, data, status_code=200):
            self._data = data
            self.status_code = status_code

        def json(self):
            return self._data

    class FakeClient:
        api_base_url = ""

        def __init__(self, _api_base_url):
            pass

        def post_json(self, path, payload):
            if path == "/sessions":
                return FakeResponse({"data": {"session_id": "session_1"}})
            if path == "/sessions/session_1/assets/publish-references":
                return FakeResponse({"data": {"ready": True, "assets": []}})
            if path == "/workflows/content-production/runs/preflight":
                preflight_payloads.append(payload)
                return FakeResponse({"data": {"ready": True, "reference_images": {"url_probe": {"enabled": True}}}})
            raise AssertionError(path)

        def post_files(self, path, *, files, data):
            return FakeResponse({"data": {"assets": [{"asset_id": "asset_1"}]}})

    monkeypatch.setattr(HOLLY_SMOKE, "_HttpBackendClient", FakeClient)
    args = SimpleNamespace(
        api_base_url="http://127.0.0.1:8000",
        backend_public_base_url="https://backend.nori.ai",
        require_image_references=True,
        verify_reference_urls=True,
        run=False,
        allow_unverified_reference_url=False,
        reference_url_probe_timeout=0.2,
        stage_timeout_seconds=0.0,
        content_package_timeout_seconds=0.0,
        execution_mode="sync",
        keep_data=False,
    )

    result = HOLLY_SMOKE._smoke(
        project_root=tmp_path,
        state_root=tmp_path,
        fixture={
            "asset_paths": [str(image_path)],
            "case_id": "Holly",
            "brief_text": "brief",
            "market_evidence": {"queries": ["q"]},
            "config": {},
        },
        args=args,
    )

    assert result["exit_code"] == 0
    assert preflight_payloads[0]["verify_reference_urls"] is True
    assert preflight_payloads[0]["reference_url_probe_timeout"] == 0.2


def test_holly_smoke_can_check_reference_image_generation_after_preflight(monkeypatch, tmp_path):
    image_path = tmp_path / "ref.png"
    image_path.write_bytes(b"fake-png-bytes")
    generation_payloads = []

    class FakeResponse:
        def __init__(self, data, status_code=200):
            self._data = data
            self.status_code = status_code

        def json(self):
            return self._data

    class FakeClient:
        api_base_url = "http://127.0.0.1:8000"

        def __init__(self, _api_base_url):
            pass

        def post_json(self, path, payload):
            if path == "/sessions":
                return FakeResponse({"data": {"session_id": "session_1"}})
            if path == "/sessions/session_1/assets/publish-references":
                return FakeResponse({"data": {"ready": True, "assets": []}})
            if path == "/workflows/content-production/runs/preflight":
                return FakeResponse(
                    {
                        "data": {
                            "ready": True,
                            "assets": {
                                "items": [
                                    {"provider_fetchable_url": "https://assets.nori.ai/ref.png"},
                                    {"provider_fetchable_url": ""},
                                ]
                            },
                        }
                    }
                )
            if path == "/sessions/session_1/assets/reference-image-generation-check":
                generation_payloads.append(payload)
                return FakeResponse({"data": {"ready": True, "image_count": 1}})
            raise AssertionError(path)

        def post_files(self, path, *, files, data):
            return FakeResponse({"data": {"assets": [{"asset_id": "asset_1"}]}})

    monkeypatch.setattr(HOLLY_SMOKE, "_HttpBackendClient", FakeClient)
    args = SimpleNamespace(
        api_base_url="http://127.0.0.1:8000",
        backend_public_base_url="https://backend.nori.ai",
        require_image_references=True,
        verify_reference_urls=False,
        check_reference_image_generation=True,
        reference_generation_prompt="test prompt",
        reference_generation_size="1024x1024",
        run=False,
        allow_unverified_reference_url=False,
        reference_url_probe_timeout=0.2,
        stage_timeout_seconds=0.0,
        content_package_timeout_seconds=0.0,
        execution_mode="sync",
        keep_data=False,
    )

    result = HOLLY_SMOKE._smoke(
        project_root=tmp_path,
        state_root=tmp_path,
        fixture={
            "asset_paths": [str(image_path)],
            "case_id": "Holly",
            "brief_text": "brief",
            "market_evidence": {"queries": ["q"]},
            "config": {},
        },
        args=args,
    )

    assert result["exit_code"] == 0
    assert result["payload"]["reference_image_generation_check"]["ready"] is True
    assert generation_payloads == [
        {
            "prompt": "test prompt",
            "asset_ids": ["asset_1"],
            "backend_public_base_url": "https://backend.nori.ai",
            "verify_reference_urls": False,
            "reference_url_probe_timeout": 0.2,
            "size": "1024x1024",
            "metadata": {"source": "backend_holly_smoke", "case_id": "Holly"},
        }
    ]


def test_holly_smoke_stops_before_run_when_reference_image_generation_check_fails(monkeypatch, tmp_path):
    image_path = tmp_path / "ref.png"
    image_path.write_bytes(b"fake-png-bytes")
    run_calls = []

    class FakeResponse:
        def __init__(self, data, status_code=200):
            self._data = data
            self.status_code = status_code

        def json(self):
            return self._data

    class FakeClient:
        api_base_url = "http://127.0.0.1:8000"

        def __init__(self, _api_base_url):
            pass

        def post_json(self, path, payload):
            if path == "/sessions":
                return FakeResponse({"data": {"session_id": "session_1"}})
            if path == "/sessions/session_1/assets/publish-references":
                return FakeResponse({"data": {"ready": True, "assets": []}})
            if path == "/workflows/content-production/runs/preflight":
                return FakeResponse(
                    {
                        "data": {
                            "ready": True,
                            "assets": {"items": [{"provider_fetchable_url": "https://assets.nori.ai/ref.png"}]},
                        }
                    }
                )
            if path == "/sessions/session_1/assets/reference-image-generation-check":
                return FakeResponse({"data": {"ready": False, "reason": "image_generation_error"}})
            if path == "/workflows/content-production/runs":
                run_calls.append(payload)
                return FakeResponse({"data": {}}, status_code=201)
            raise AssertionError(path)

        def post_files(self, path, *, files, data):
            return FakeResponse({"data": {"assets": [{"asset_id": "asset_1"}]}})

    monkeypatch.setattr(HOLLY_SMOKE, "_HttpBackendClient", FakeClient)
    args = SimpleNamespace(
        api_base_url="http://127.0.0.1:8000",
        backend_public_base_url="https://backend.nori.ai",
        require_image_references=True,
        verify_reference_urls=False,
        check_reference_image_generation=True,
        reference_generation_prompt="test prompt",
        reference_generation_size="1024x1024",
        run=True,
        allow_unverified_reference_url=False,
        reference_url_probe_timeout=0.2,
        stage_timeout_seconds=0.0,
        content_package_timeout_seconds=0.0,
        execution_mode="sync",
        keep_data=False,
    )

    result = HOLLY_SMOKE._smoke(
        project_root=tmp_path,
        state_root=tmp_path,
        fixture={
            "asset_paths": [str(image_path)],
            "case_id": "Holly",
            "brief_text": "brief",
            "market_evidence": {"queries": ["q"]},
            "config": {},
        },
        args=args,
    )

    assert result["exit_code"] == 3
    assert result["payload"]["reference_image_generation_check"]["ready"] is False
    assert run_calls == []


def test_holly_smoke_reference_image_generation_check_requires_fetchable_urls(monkeypatch, tmp_path):
    image_path = tmp_path / "ref.png"
    image_path.write_bytes(b"fake-png-bytes")
    generation_calls = []

    class FakeResponse:
        def __init__(self, data, status_code=200):
            self._data = data
            self.status_code = status_code

        def json(self):
            return self._data

    class FakeClient:
        api_base_url = "http://127.0.0.1:8000"

        def __init__(self, _api_base_url):
            pass

        def post_json(self, path, payload):
            if path == "/sessions":
                return FakeResponse({"data": {"session_id": "session_1"}})
            if path == "/sessions/session_1/assets/publish-references":
                return FakeResponse({"data": {"ready": False, "assets": []}})
            if path == "/workflows/content-production/runs/preflight":
                return FakeResponse(
                    {
                        "data": {
                            "ready": False,
                            "checks": [
                                {
                                    "name": "reference_transfer",
                                    "status": "failed",
                                    "message": "missing public URL",
                                }
                            ],
                            "assets": {"items": [{"provider_fetchable_url": ""}]},
                        }
                    }
                )
            if path == "/sessions/session_1/assets/reference-image-generation-check":
                generation_calls.append(payload)
                return FakeResponse({"data": {"ready": True}})
            raise AssertionError(path)

        def post_files(self, path, *, files, data):
            return FakeResponse({"data": {"assets": [{"asset_id": "asset_1"}]}})

    monkeypatch.setattr(HOLLY_SMOKE, "_HttpBackendClient", FakeClient)
    args = SimpleNamespace(
        api_base_url="http://127.0.0.1:8000",
        backend_public_base_url="",
        require_image_references=True,
        verify_reference_urls=False,
        check_reference_image_generation=True,
        reference_generation_prompt="test prompt",
        reference_generation_size="1024x1024",
        run=True,
        allow_unverified_reference_url=False,
        reference_url_probe_timeout=0.2,
        stage_timeout_seconds=0.0,
        content_package_timeout_seconds=0.0,
        execution_mode="sync",
        keep_data=False,
    )

    result = HOLLY_SMOKE._smoke(
        project_root=tmp_path,
        state_root=tmp_path,
        fixture={
            "asset_paths": [str(image_path)],
            "case_id": "Holly",
            "brief_text": "brief",
            "market_evidence": {"queries": ["q"]},
            "config": {},
        },
        args=args,
    )

    check = result["payload"]["reference_image_generation_check"]
    assert result["exit_code"] == 3
    assert check["ready"] is False
    assert check["reason"] == "no_provider_fetchable_reference_images"
    assert check["preflight_ready"] is False
    assert check["failed_checks"] == ["reference_transfer"]
    assert generation_calls == []


def test_holly_smoke_reports_non_json_api_responses():
    class FakeResponse:
        status_code = 502
        text = "<html>bad gateway</html>"

        def json(self):
            raise ValueError("not json")

    class FakeClient:
        def post_json(self, path, payload):
            return FakeResponse()

    with pytest.raises(RuntimeError, match="/workflows/content-production/runs/preflight failed: 502"):
        HOLLY_SMOKE._post_ok(FakeClient(), "/workflows/content-production/runs/preflight", {"case_id": "Holly"})


def test_holly_smoke_polls_background_run_until_succeeded(monkeypatch, tmp_path):
    image_path = tmp_path / "ref.png"
    image_path.write_bytes(b"fake-png-bytes")
    polls = []

    class FakeResponse:
        def __init__(self, data, status_code=200):
            self._data = data
            self.status_code = status_code
            self.text = ""

        def json(self):
            return self._data

    class FakeClient:
        api_base_url = "http://127.0.0.1:8000"

        def __init__(self, _api_base_url):
            pass

        def post_json(self, path, payload):
            if path == "/sessions":
                return FakeResponse({"data": {"session_id": "session_1"}})
            if path == "/sessions/session_1/assets/publish-references":
                return FakeResponse({"data": {"ready": True, "assets": []}})
            if path == "/workflows/content-production/runs/preflight":
                return FakeResponse({"data": {"ready": True, "assets": {"items": []}}})
            if path == "/workflows/content-production/runs":
                return FakeResponse(
                    {
                        "data": {
                            "job_id": "job_1",
                            "status": "running",
                            "links": {"self": "/experiments/jobs/job_1"},
                        }
                    },
                    status_code=202,
                )
            raise AssertionError(path)

        def get_json(self, path):
            polls.append(path)
            return FakeResponse(
                {
                    "data": {
                        "job": {
                            "job_id": "job_1",
                            "status": "succeeded",
                            "result": {"run_id": "run_1", "status": "succeeded"},
                        }
                    }
                }
            )

        def post_files(self, path, *, files, data):
            return FakeResponse({"data": {"assets": [{"asset_id": "asset_1"}]}})

    monkeypatch.setattr(HOLLY_SMOKE, "_HttpBackendClient", FakeClient)
    args = SimpleNamespace(
        api_base_url="http://127.0.0.1:8000",
        backend_public_base_url="https://backend.nori.ai",
        require_image_references=False,
        verify_reference_urls=False,
        check_reference_image_generation=False,
        run=True,
        allow_unverified_reference_url=False,
        reference_url_probe_timeout=0.2,
        stage_timeout_seconds=0.0,
        content_package_timeout_seconds=0.0,
        execution_mode="background",
        job_poll_timeout=1.0,
        job_poll_interval=0.01,
        no_poll_job=False,
        keep_data=False,
    )

    result = HOLLY_SMOKE._smoke(
        project_root=tmp_path,
        state_root=tmp_path,
        fixture={
            "asset_paths": [str(image_path)],
            "case_id": "Holly",
            "brief_text": "brief",
            "market_evidence": {"queries": ["q"]},
            "config": {},
        },
        args=args,
    )

    assert result["exit_code"] == 0
    assert result["payload"]["job"]["status"] == "succeeded"
    assert result["payload"]["run"] == {"run_id": "run_1", "status": "succeeded"}
    assert polls == ["/experiments/jobs/job_1"]
