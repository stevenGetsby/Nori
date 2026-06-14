"""Smoke the backend content-production API with the local Holly case.

Default mode performs session creation, asset upload, and run preflight only.
Use --run to execute the real workflow and model calls.
"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient
import httpx

from backend import NoriBackend, create_app
from backend.experiments import ContentProductionExperimentRunner
from backend.fixtures import holly_content_production_fixture
from backend.reference_urls import provider_fetchable_reference_url


def main() -> int:
    parser = argparse.ArgumentParser(description="Backend API smoke for the local Holly content-production case.")
    parser.add_argument("--project-root", default=str(ROOT), help="Project root containing cases/Holly.")
    parser.add_argument("--api-base-url", default="", help="Use a running backend API instead of in-process TestClient.")
    parser.add_argument("--max-assets", type=int, default=4, help="Number of Holly fixture images to upload.")
    parser.add_argument("--backend-public-base-url", default="", help="Public backend URL for strict relay references.")
    parser.add_argument("--require-image-references", action="store_true", help="Require selected images to reach the image provider.")
    parser.add_argument("--execution-mode", choices=["sync", "background"], default="sync")
    parser.add_argument("--run", action="store_true", help="Execute the real workflow after preflight.")
    parser.add_argument(
        "--allow-unverified-reference-url",
        action="store_true",
        help="Allow live strict-reference runs with a placeholder/local backend public URL.",
    )
    parser.add_argument(
        "--verify-reference-urls",
        action="store_true",
        help="Probe selected provider-fetchable reference URLs during preflight, even without --run.",
    )
    parser.add_argument("--reference-url-probe-timeout", type=float, default=3.0, help="Seconds for each strict-reference URL probe.")
    parser.add_argument("--stage-timeout-seconds", type=float, default=0.0, help="Override every content-production stage timeout for live run checks.")
    parser.add_argument("--content-package-timeout-seconds", type=float, default=0.0, help="Override content_package stage timeout for live run checks.")
    parser.add_argument("--job-poll-timeout", type=float, default=900.0, help="Seconds to wait for background --run jobs.")
    parser.add_argument("--job-poll-interval", type=float, default=3.0, help="Seconds between background job polls.")
    parser.add_argument("--no-poll-job", action="store_true", help="Do not poll background --run jobs to terminal status.")
    parser.add_argument(
        "--check-reference-image-generation",
        action="store_true",
        help="Call the active image model with published reference URLs before --run.",
    )
    parser.add_argument(
        "--require-reference-image-generation-check",
        action="store_true",
        help="Require preflight/run to have a successful image-provider reference-image check for the selected assets.",
    )
    parser.add_argument(
        "--reference-generation-prompt",
        default="Generate a simple product image using the provided Holly reference image.",
        help="Prompt for --check-reference-image-generation.",
    )
    parser.add_argument("--reference-generation-size", default="1024x1024", help="Image size for --check-reference-image-generation.")
    parser.add_argument("--keep-data", action="store_true", help="Keep backend session/upload state under the project root.")
    args = parser.parse_args()

    if (
        args.run
        and args.require_image_references
        and args.backend_public_base_url
        and not args.allow_unverified_reference_url
    ):
        _assert_live_reference_base_url(args.backend_public_base_url)

    project_root = Path(args.project_root).resolve()
    fixture = holly_content_production_fixture(project_root=project_root, max_assets=args.max_assets)
    if args.api_base_url:
        result = _smoke(project_root=project_root, state_root=project_root, fixture=fixture, args=args)
    elif args.run:
        result = _smoke(project_root=project_root, state_root=project_root, fixture=fixture, args=args)
    elif args.keep_data:
        result = _smoke(project_root=project_root, state_root=project_root, fixture=fixture, args=args)
    else:
        with tempfile.TemporaryDirectory(prefix="nori_backend_holly_smoke_") as tmp:
            result = _smoke(project_root=project_root, state_root=Path(tmp), fixture=fixture, args=args)

    print(json.dumps(result["payload"], ensure_ascii=False, indent=2, default=str))
    return result["exit_code"]


def _smoke(*, project_root: Path, state_root: Path, fixture: dict, args: argparse.Namespace) -> dict:
    if args.api_base_url:
        client = _HttpBackendClient(args.api_base_url)
        backend_state_root = ""
    else:
        service = NoriBackend(
            experiment_runner=ContentProductionExperimentRunner(project_root=state_root),
            upload_root=state_root / "data" / "backend" / "uploads",
        )
        client = _TestBackendClient(TestClient(create_app(backend=service)))
        backend_state_root = str(state_root)
    client.job_poll_timeout = float(getattr(args, "job_poll_timeout", 900.0) or 900.0)
    client.job_poll_interval = float(getattr(args, "job_poll_interval", 3.0) or 3.0)

    session = _post_ok(client, "/sessions", {"user_id": "holly", "profile_id": "holly", "metadata": {"project": "Holly"}})
    asset_ids = _upload_assets(client, session["session_id"], [Path(path) for path in fixture["asset_paths"]])
    published_references = None
    if _should_publish_references(args):
        published_references = _publish_references(client, session["session_id"], asset_ids, args=args)
    request = {
        key: value
        for key, value in fixture.items()
        if key not in {"asset_paths"}
    }
    if args.stage_timeout_seconds > 0 or args.content_package_timeout_seconds > 0:
        request.setdefault("config", {})
        config = dict(request.get("config") or {})
        if args.stage_timeout_seconds > 0:
            config["stage_timeout_seconds"] = args.stage_timeout_seconds
        if args.content_package_timeout_seconds > 0:
            config["content_package_timeout_seconds"] = args.content_package_timeout_seconds
        request["config"] = config
    request.update(
        {
            "session_id": session["session_id"],
            "asset_ids": asset_ids,
            "backend_public_base_url": args.backend_public_base_url,
            "require_image_references": bool(args.require_image_references),
            "require_reference_image_generation_check": bool(
                getattr(args, "require_reference_image_generation_check", False)
            ),
            "verify_reference_urls": _should_verify_reference_urls(args),
            "reference_url_probe_timeout": args.reference_url_probe_timeout,
            "execution_mode": args.execution_mode,
        }
    )

    preflight = _post_ok(client, "/workflows/content-production/runs/preflight", request)
    reference_image_generation_check = None
    if _should_check_reference_image_generation(args):
        reference_image_generation_check = _check_reference_image_generation(
            client,
            preflight,
            session_id=session["session_id"],
            asset_ids=asset_ids,
            fixture=fixture,
            args=args,
        )
        if reference_image_generation_check.get("ready"):
            request["require_reference_image_generation_check"] = True
            preflight = _post_ok(client, "/workflows/content-production/runs/preflight", request)
    result = {
        "project_root": str(project_root),
        "backend_state_root": backend_state_root,
        "backend_api_base_url": getattr(client, "api_base_url", ""),
        "state_persistent": bool(args.run or args.keep_data),
        "session_id": session["session_id"],
        "asset_ids": asset_ids,
        "published_references": published_references,
        "preflight": preflight,
        "reference_image_generation_check": reference_image_generation_check,
        "job": None,
        "run": None,
    }
    if reference_image_generation_check is not None and not reference_image_generation_check.get("ready"):
        return {"payload": result, "exit_code": 3}
    if args.run:
        if not preflight.get("ready"):
            return {"payload": result, "exit_code": 2}
        response = client.post_json("/workflows/content-production/runs", request)
        run_response = _response_json_or_raise(response, label="/workflows/content-production/runs")
        run_data = run_response.get("data") if isinstance(run_response.get("data"), dict) else {}
        result["run"] = run_data or run_response
        if response.status_code == 202 and _should_poll_job(args):
            final_job = _poll_job(client, run_data)
            result["job"] = final_job
            if final_job.get("status") in {"succeeded", "failed"} and isinstance(final_job.get("result"), dict):
                result["run"] = final_job["result"]
            if final_job.get("status") != "succeeded":
                return {"payload": result, "exit_code": 1}
        if response.status_code not in {201, 202}:
            return {"payload": result, "exit_code": 1}

    return {
        "payload": result,
        "exit_code": 0 if preflight.get("ready") or not args.require_image_references else 2,
    }


def _should_publish_references(args: argparse.Namespace) -> bool:
    return bool(args.require_image_references or str(args.backend_public_base_url or "").strip())


def _should_verify_reference_urls(args: argparse.Namespace) -> bool:
    if bool(getattr(args, "verify_reference_urls", False)):
        return True
    return bool(args.run and args.require_image_references and not args.allow_unverified_reference_url)


def _should_check_reference_image_generation(args: argparse.Namespace) -> bool:
    return bool(getattr(args, "check_reference_image_generation", False))


def _should_poll_job(args: argparse.Namespace) -> bool:
    return not bool(getattr(args, "no_poll_job", False))


def _poll_job(client, run_data: dict[str, Any]) -> dict[str, Any]:
    links = run_data.get("links") if isinstance(run_data.get("links"), dict) else {}
    href = str(links.get("self") or "")
    if not href:
        job_id = str(run_data.get("job_id") or "")
        href = f"/experiments/jobs/{job_id}" if job_id else ""
    if not href:
        raise RuntimeError("background run did not include a job self link")
    deadline = time.monotonic() + _job_poll_timeout(client)
    interval = _job_poll_interval(client)
    last_job: dict[str, Any] = {}
    while time.monotonic() <= deadline:
        data = _get_ok(client, href)
        job = data.get("job") if isinstance(data.get("job"), dict) else data
        if isinstance(job, dict):
            last_job = job
            if str(job.get("status") or "") in {"succeeded", "failed", "cancelled", "interrupted"}:
                return job
        time.sleep(interval)
    raise RuntimeError(f"background job did not finish before timeout: {last_job}")


def _job_poll_timeout(client) -> float:
    return float(getattr(client, "job_poll_timeout", 900.0))


def _job_poll_interval(client) -> float:
    return max(0.1, float(getattr(client, "job_poll_interval", 3.0)))


def _publish_references(client, session_id: str, asset_ids: list[str], *, args: argparse.Namespace) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "asset_ids": list(asset_ids),
        "project": "Holly",
    }
    backend_public_base_url = str(args.backend_public_base_url or "").strip()
    if backend_public_base_url:
        payload["backend_public_base_url"] = backend_public_base_url
    return _post_ok(client, f"/sessions/{session_id}/assets/publish-references", payload)


def _check_reference_image_generation(
    client,
    preflight: dict[str, Any],
    *,
    session_id: str,
    asset_ids: list[str],
    fixture: dict[str, Any],
    args: argparse.Namespace,
) -> dict[str, Any]:
    urls = _preflight_provider_fetchable_urls(preflight)
    if not urls:
        return _reference_image_generation_blocked_result(
            reason="no_provider_fetchable_reference_images",
            preflight=preflight,
            reference_images=[],
        )
    if not preflight.get("ready"):
        return _reference_image_generation_blocked_result(
            reason="preflight_not_ready",
            preflight=preflight,
            reference_images=urls,
        )
    payload = {
        "prompt": str(getattr(args, "reference_generation_prompt", "") or "Generate a simple product image using the provided Holly reference image."),
        "asset_ids": list(asset_ids),
        "backend_public_base_url": str(getattr(args, "backend_public_base_url", "") or ""),
        "verify_reference_urls": _should_verify_reference_urls(args),
        "reference_url_probe_timeout": float(getattr(args, "reference_url_probe_timeout", 3.0) or 3.0),
        "size": str(getattr(args, "reference_generation_size", "") or "1024x1024"),
        "metadata": {
            "source": "backend_holly_smoke",
            "case_id": str(fixture.get("case_id") or "Holly"),
        },
    }
    return _post_ok(client, f"/sessions/{session_id}/assets/reference-image-generation-check", payload)


def _reference_image_generation_blocked_result(
    *,
    reason: str,
    preflight: dict[str, Any],
    reference_images: list[str],
) -> dict[str, Any]:
    checks = preflight.get("checks") if isinstance(preflight.get("checks"), list) else []
    failed_checks = [
        str(item.get("name") or "")
        for item in checks
        if isinstance(item, dict) and str(item.get("status") or "") == "failed"
    ]
    return {
        "ready": False,
        "reason": reason,
        "reference_images": list(reference_images),
        "provider_fetchable_count": len(reference_images),
        "preflight_ready": bool(preflight.get("ready")),
        "failed_checks": [item for item in failed_checks if item],
        "message": _reference_image_generation_blocked_message(reason),
    }


def _reference_image_generation_blocked_message(reason: str) -> str:
    if reason == "preflight_not_ready":
        return "Preflight is not ready; fix failed preflight checks before spending an image-provider call."
    return (
        "Preflight did not expose any provider-fetchable reference image URLs. "
        "Use --backend-public-base-url with a real HTTPS backend URL, configure OSS, "
        "or publish references before checking image-provider reference support."
    )


def _preflight_provider_fetchable_urls(preflight: dict[str, Any]) -> list[str]:
    assets = preflight.get("assets") if isinstance(preflight.get("assets"), dict) else {}
    items = assets.get("items") if isinstance(assets.get("items"), list) else []
    urls = []
    for item in items:
        if not isinstance(item, dict):
            continue
        url = provider_fetchable_reference_url(str(item.get("provider_fetchable_url") or ""))
        if url:
            urls.append(url)
    return list(dict.fromkeys(urls))


class _TestBackendClient:
    api_base_url = ""

    def __init__(self, client: TestClient) -> None:
        self._client = client

    def post_json(self, path: str, payload: dict[str, Any]):
        return self._client.post(path, json=payload)

    def get_json(self, path: str):
        return self._client.get(path)

    def post_files(self, path: str, *, files: list[tuple[str, tuple[str, bytes, str]]], data: dict[str, str]):
        return self._client.post(path, files=files, data=data)


class _HttpBackendClient:
    def __init__(self, api_base_url: str) -> None:
        self.api_base_url = _normalize_api_base_url(api_base_url)

    def post_json(self, path: str, payload: dict[str, Any]):
        return httpx.post(self._url(path), json=payload, timeout=120.0)

    def get_json(self, path: str):
        return httpx.get(self._url(path), timeout=120.0)

    def post_files(self, path: str, *, files: list[tuple[str, tuple[str, bytes, str]]], data: dict[str, str]):
        return httpx.post(self._url(path), files=files, data=data, timeout=120.0)

    def _url(self, path: str) -> str:
        return f"{self.api_base_url}/{path.lstrip('/')}"


def _normalize_api_base_url(value: str) -> str:
    url = str(value or "").strip().rstrip("/")
    if not url:
        raise RuntimeError("--api-base-url cannot be empty")
    if not url.startswith(("http://", "https://")):
        raise RuntimeError("--api-base-url must start with http:// or https://")
    return url


def _post_ok(client, path: str, payload: dict) -> dict:
    response = client.post_json(path, payload)
    data = _response_json_or_raise(response, label=path)
    if response.status_code >= 400:
        raise RuntimeError(f"{path} failed: {response.status_code} {data}")
    return data["data"]


def _get_ok(client, path: str) -> dict:
    response = client.get_json(path)
    data = _response_json_or_raise(response, label=path)
    if response.status_code >= 400:
        raise RuntimeError(f"{path} failed: {response.status_code} {data}")
    return data["data"]


def _upload_assets(client, session_id: str, paths: list[Path]) -> list[str]:
    files = []
    for path in paths:
        files.append(("files", (path.name, path.read_bytes(), _content_type(path))))
    response = client.post_files(
        f"/sessions/{session_id}/assets",
        files=files,
        data={"usage": "reference", "metadata_json": '{"source":"holly_backend_smoke"}'},
    )
    data = _response_json_or_raise(response, label="asset upload")
    if response.status_code >= 400:
        raise RuntimeError(f"asset upload failed: {response.status_code} {data}")
    return [row["asset_id"] for row in data["data"]["assets"]]


def _response_json_or_raise(response, *, label: str) -> dict[str, Any]:
    try:
        data = response.json()
    except Exception as exc:  # noqa: BLE001
        preview = _response_text_preview(response)
        raise RuntimeError(f"{label} failed: {response.status_code} non-json response: {preview}") from exc
    if not isinstance(data, dict):
        raise RuntimeError(f"{label} failed: {response.status_code} JSON response is not an object: {data!r}")
    return data


def _response_text_preview(response, *, limit: int = 500) -> str:
    text = str(getattr(response, "text", "") or "")
    text = " ".join(text.split())
    if len(text) > limit:
        return f"{text[:limit]}..."
    return text


def _content_type(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".jpg", ".jpeg"}:
        return "image/jpeg"
    if suffix == ".webp":
        return "image/webp"
    return "image/png"


def _assert_live_reference_base_url(value: str) -> None:
    """Reject placeholder/local public URLs before live strict-reference model calls."""

    url = str(value or "").strip()
    if provider_fetchable_reference_url(url):
        return
    raise RuntimeError(
        f"--backend-public-base-url {url!r} is not a real provider-fetchable public HTTPS URL. "
        "Use an HTTPS tunnel/production backend URL, configure OSS, or omit "
        "--require-image-references for non-strict live smoke runs."
    )


if __name__ == "__main__":
    raise SystemExit(main())
