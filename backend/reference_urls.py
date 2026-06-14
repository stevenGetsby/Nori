"""Reference URL validation shared by backend preflight, manifests, and smoke scripts."""
from __future__ import annotations

import ipaddress
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from urllib.parse import urlparse


def provider_fetchable_reference_url(value: str) -> str:
    """Return a URL only when it is plausible for an external image provider to fetch."""

    url = str(value or "").strip()
    parsed = urlparse(url)
    host = str(parsed.hostname or "").lower()
    if parsed.scheme != "https" or not host:
        return ""
    if is_placeholder_or_local_host(host):
        return ""
    return url


def probe_reference_url(value: str, *, timeout: float = 3.0) -> dict[str, Any]:
    """Best-effort local reachability probe for one provider-fetchable reference URL."""

    url = provider_fetchable_reference_url(value)
    if not url:
        return {
            "url": str(value or "").strip(),
            "reachable": False,
            "status_code": 0,
            "content_type": "",
            "error_type": "InvalidReferenceUrl",
            "error": "URL is not a provider-fetchable public HTTPS reference",
        }
    try:
        return _probe_url(url, method="HEAD", timeout=timeout)
    except HTTPError as exc:
        if exc.code not in {405, 501}:
            return _probe_error(url, exc)
    except Exception as exc:  # noqa: BLE001
        return _probe_error(url, exc)
    try:
        return _probe_url(url, method="GET", timeout=timeout)
    except Exception as exc:  # noqa: BLE001
        return _probe_error(url, exc)


def _probe_url(url: str, *, method: str, timeout: float) -> dict[str, Any]:
    headers = {"User-Agent": "NoriReferenceProbe/1.0"}
    if method == "GET":
        headers["Range"] = "bytes=0-0"
    request = Request(url, headers=headers, method=method)
    with urlopen(request, timeout=max(0.1, float(timeout or 3.0))) as response:  # noqa: S310
        status_code = int(getattr(response, "status", 0) or response.getcode() or 0)
        content_type = str(response.headers.get("Content-Type") or "").split(";", 1)[0].strip()
    return {
        "url": url,
        "reachable": 200 <= status_code < 400,
        "status_code": status_code,
        "content_type": content_type,
        "error_type": "" if 200 <= status_code < 400 else "HTTPStatusError",
        "error": "" if 200 <= status_code < 400 else f"HTTP status {status_code}",
    }


def is_placeholder_or_local_host(host: str) -> bool:
    """Detect hosts that should not be treated as provider-fetchable."""

    value = str(host or "").lower().strip(".")
    if value in {
        "localhost",
        "backend.example.test",
        "example.test",
        "example.com",
        "example.net",
        "example.org",
    }:
        return True
    if (
        value.endswith(".localhost")
        or value.endswith(".local")
        or value.endswith(".test")
        or value.endswith(".example.com")
        or value.endswith(".example.net")
        or value.endswith(".example.org")
        or value.endswith(".example.test")
    ):
        return True
    try:
        address = ipaddress.ip_address(value)
    except ValueError:
        return False
    return address.is_private or address.is_loopback or address.is_link_local or address.is_reserved


def _probe_error(url: str, exc: Exception) -> dict[str, Any]:
    status_code = int(getattr(exc, "code", 0) or 0)
    reason = getattr(exc, "reason", None)
    return {
        "url": url,
        "reachable": False,
        "status_code": status_code,
        "content_type": "",
        "error_type": type(exc).__name__,
        "error": str(reason or exc),
    }


__all__ = ["is_placeholder_or_local_host", "probe_reference_url", "provider_fetchable_reference_url"]
