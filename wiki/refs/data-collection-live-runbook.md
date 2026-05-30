<!-- Last verified: 2026-05-24 | Current stage: P2 Data Collection + Skill Learning -->

# Data Collection Live Runbook

This runbook is for explicit live smoke runs only. Do not run it from the default test suite.

## Secret Rules

- Do not commit `api_config.yaml`, cookies, browser profiles, downloaded private media, or crawler runtime databases.
- Do not paste CookieBridge responses that contain cookie values into issues, wiki files, or logs.
- Prefer `api_config.example.yaml` + environment variables for LLM keys. See [api-config.md](./api-config.md).
- Treat XHS/Douyin live collection as account-sensitive. Stop if the platform asks for fresh login, verification, or abnormal-traffic confirmation.

## Runtime Pieces

| Piece | Default | Role |
| --- | --- | --- |
| `DataCollector` | Python facade | Starts/checks services and calls platform adapters. |
| Sign service | `http://127.0.0.1:8989` | Provides XHS/Douyin request signing. |
| Downloader service | `http://127.0.0.1:8990` | Optional media download service. |
| CookieBridge | `http://localhost:8274` | Browser-extension/local-cookie bridge for platform cookies. |
| LLM config | `api_config.yaml` or `NORI_CONFIG` | Required by `XHSNoteAnalyzer.collect_for_session`. |

## Preflight

From repo root:

```bash
python 文档/codex-skills/nori-project-operator/scripts/nori_status.py .
python -m pytest tests/test_data_collect_top_notes.py tests/test_market_analysis_xhs_note_analyzer.py tests/test_note_skill_fixture.py -q
```

Expected:

- `nori_status.py` finds `nori`, `llms`, `data_collect`, and `tests`; `legacy_packages.*` should be `false` for removed roots.
- Default mocked tests pass without live platform calls.
- `api_config` may be false on machines that intentionally keep private config elsewhere.

## Health Check

Use a short Python check instead of printing cookie payloads:

```bash
python - <<'PY'
from data_collect import DataCollector

dc = DataCollector()
print(dc.health_check("xhs"))
dc.stop_all()
PY
```

Interpretation:

| Field | Healthy signal | If unhealthy |
| --- | --- | --- |
| `sign` | `true` after `start_sign_server()` or existing service | Check port 8989 and `data_collect/sign` dependencies. |
| `downloader` | `true` only when media download service is running | Required only when downloading media. |
| `cookie_bridge.alive` | `true` | Start/repair CookieBridge extension/service. |
| `cookie_bridge.available` | `true` | Make sure browser is logged into target platform and extension has synced cookies. |

Do not expand or log raw cookie values.

## Minimal Top-Notes Smoke

Run one low-volume XHS collection:

```bash
python - <<'PY'
from data_collect import DataCollector, TopNotesRule

dc = DataCollector()
try:
    dc.start_sign_server()
    result = dc.collect_top_notes(TopNotesRule(
        platform="xhs",
        keywords=["花艺"],
        top_k_per_keyword=2,
        download_media=False,
        data_dir="nori/skill_base/data/xhs_note_analyzer/smoke",
    ))
    print({
        "queries": result.queries,
        "notes": len(result.hot_notes),
        "insufficient": result.insufficient,
        "source_data_dir": result.source_data_dir,
    })
finally:
    dc.stop_all()
PY
```

Success means at least one `HotNote` is returned and `insufficient` is empty or explainable for the keyword.

## Session Skill Smoke

Requires:

- valid local LLM config;
- CookieBridge with XHS cookies;
- sign service dependencies available;
- a Holly chain case log under `log/agent_chain_holly_intaker_to_account_planner_*.json`, or an explicit `--case-log`.

Command:

```bash
PYTHONPATH=. python scripts/smoke_session_skill.py --top-k 2 --no-download
```

Outputs:

- full `SessionSkillReport` on stdout;
- summary on stderr;
- `<run_id>_session_skill_report.json`;
- `<run_id>_note_skill_guides.json`.

The skills-only JSON can be loaded by generation tests or scripts:

```python
from nori.agents.market_analysis import load_note_skills
from nori.agents.content_generation.note_maker import NoteMakerAgent

skills = load_note_skills("path/to/note_skill_guides.json")
draft = NoteMakerAgent().run(skills, assets, intent={"goal": "产品种草"})
```

## Troubleshooting

| Symptom | Likely cause | Action |
| --- | --- | --- |
| `SignSrv 未就绪` | Port conflict, missing sign dependencies, or service crash. | Check `http://127.0.0.1:8989/signsrv/pong`; run sign service from repo root via `DataCollector.start_sign_server()`. |
| `CookieBridge 未就绪` | Extension/service not running. | Start CookieBridge, confirm `/api/accounts` is reachable, then rerun health check. |
| `没有可用 xhs cookie` | Browser is logged out, extension did not sync, or local cookie read failed. | Log into XHS in browser, sync extension, avoid printing the cookie payload. |
| Empty or insufficient notes | Keyword too narrow, platform response changed, or account is rate-limited. | Try a broader keyword and `download_media=False`; stop if platform verification appears. |
| `NoteMakerLLMError` during downstream generation | LLM config missing or model output invalid. | Run `llms.ensure_ready("llm")` through a local smoke script and check [api-config.md](./api-config.md). |

## Stop Conditions

Stop the live run when:

- platform verification, captcha, or abnormal-traffic prompt appears;
- CookieBridge returns stale or missing cookies after one browser refresh;
- sign endpoint repeatedly fails after service restart;
- the smoke goal only needs mocked contract validation.
