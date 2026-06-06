<!-- Last verified: 2026-06-01 | Current stage: P1 Account-Ops Backend -->

# Known Pitfalls

| Symptom | Cause | Fix |
| --- | --- | --- |
| Live LLM calls fail with missing active model | No private `api_config.yaml` was found; status script reports empty active models. | Copy `api_config.example.yaml` to a private ignored config or set `NORI_CONFIG`; use `api_key_env` and see [refs/api-config.md](./refs/api-config.md). |
| Live LLM calls fail with `Using SOCKS proxy, but the 'socksio' package is not installed` | The local environment routes HTTPX/OpenAI-compatible SDK traffic through a SOCKS proxy, but `socksio` is not installed. | Install `socksio` or install HTTPX with SOCKS support before live API smoke runs: `python -m pip install 'socksio>=1.0.0'`. |
| Live image calls fail with `image 模型 relay::gpt-image-2 的 api_key 为空` | Active image usage points at `relay::gpt-image-2`, but the relay provider did not resolve an API key from `RELAY_API_KEY` or literal local config. | Set `RELAY_API_KEY` or put a private ignored literal key in `api_config.yaml`; also replace example relay `base_url` with the real OpenAI-compatible image relay endpoint. |
| Relay image generation returns a normal image but ignores the reference | The relay may accept `image_urls`, `images`, or `image` fields without applying them as image references. | Send URL references as `extra_body.reference_images` first. Verify with a hidden-content probe instead of trusting `reference_images_sent=true`. |
| `NORI_CONFIG` points to a missing file | Explicit config path should not silently fall back to another model config. | Fix the path or unset `NORI_CONFIG`; `NoriConfig` intentionally raises `FileNotFoundError`. |
| `dataclass(slots=True)` breaks on Python 3.9 | Local Anaconda Python 3.9 uses a `dataclasses` implementation without `slots`. | Use `nori._compat.dataclass` for shared model/result classes; it keeps slots on supported Python and drops the unsupported keyword on Python 3.9. |
| Showcase tests fail when Holly fixture is absent | Intaker/AccountPlanner tests reference `SHOWCASE/Holly/设计理念.md` and brand-material images. | Keep the lightweight fixture directory in the repo or mark those tests fixture-dependent if it is intentionally removed. |
| Image generation request too large | Raw reference images can exceed provider limits. | Use `nori/shared/image_io.py` compression path; CoverDirector already uses it. |
| README drifts back to historical `文档/` entrypoints | Older docs predate the canonical wiki and may reference missing files. | Keep README as a short navigation page that points to `wiki/`; put durable project truth in wiki. |
| Default test suite accidentally hits live services | Tests may import live-capable code, but should monkeypatch/fallback by default. | Keep live calls in `scripts/smoke_*.py` or explicitly marked tests. |
| Data collection returns empty/failed results | Sign service, CookieBridge, cookies, or platform protocol may be unavailable. | Check [refs/data-collection-live-runbook.md](./refs/data-collection-live-runbook.md); run live crawler only in explicit smoke context. |
| Duplicate concept spread across `文档/`, `进度.md`, and wiki | Historical docs predate wiki. | Treat root `进度.md` as historical only; put durable current truth in wiki. |
