<!-- Last verified: 2026-05-24 | Current stage: P1 Account-Ops Backend -->

# Stage 62: Data Collection And Skill Learning

## Goal

Collect platform evidence and convert high-performing notes into reusable, evidence-backed `NoteSkill` records for generation.

## Data Collection Layer

| Component | Role | Status |
| --- | --- | --- |
| `DataCollector` | Unified facade for search/detail/download/top-notes. | Implemented; external services may be required. |
| `SearchRule`, `DetailRule`, `CreatorRule`, `DownloadRule` | Low-level crawler task contracts. | Implemented. |
| `TopNotesRule` | High-level hot-note collection contract for Nori. | Implemented. |
| Sign service | Required for XHS/Douyin signing. | Exists under `data_collect/sign`; live dependency. |
| Downloader | Media download service. | Exists under `data_collect/downloader`; live dependency. |

## Skill Learning Layer

| Component | Role | Status |
| --- | --- | --- |
| `XHSNoteAnalyzer.analyze_note` | Single-note evidence -> seed skill draft. | Implemented; optional LLM enhancement records structured fallback metadata; `XHSNoteSample` and `XHSSeedSkillDraft` support `to_dict()` / `from_dict()` round trips. |
| `XHSNoteAnalyzer.collect_for_session` | Session context -> keywords -> collected notes -> clustered skills. | Implemented / live path depends on data collection. |
| `SessionSkillReport` | Aggregated skill-learning output. | Implemented in `nori/agents/market_analysis/models.py`; `from_dict()` input cleanup uses shared `nori.core.contracts` helpers. |
| `nori.agents.market_analysis.note_skill_fixture` | Load/write skills-only fixtures that can feed `NoteMakerAgent`. | Implemented. |
| `scripts/smoke_session_skill.py` | Live Holly chain smoke test. | Optional; needs logs, crawler/sign/cookies/LLM. |

## Evidence Flow

```text
Account planning output
-> search keywords
-> DataCollector.collect_top_notes(TopNotesRule)
-> selected notes JSON / media
-> XHSNoteAnalyzer.collect_for_session
-> SessionSkillReport.skills
-> write_note_skill_fixture / load_note_skills
-> NoteMakerAgent skills input
```

## Storage Conventions

| Artifact | Current path pattern |
| --- | --- |
| XHS analyzer data | `nori/skill_base/data/xhs_note_analyzer/...` |
| Session skill JSON | `<run_id>_note_skill_guides.json` or `session_note_skill_guides.json` |
| Case logs | `log/<stage>_<case>_*.json` via `write_stage_log` |

## Live Dependencies

| Dependency | Risk |
| --- | --- |
| CookieBridge / browser cookies | Collection may fail if account cookies are missing or expired. |
| XHS/Douyin signature service | External protocol changes can break requests. |
| Media download | Large files and platform anti-bot behavior can make smoke runs flaky. |
| LLM config | Analyzer LLM enhancement requires `api_config.yaml` and active models. |

## Fallback Observability

| Path | Contract |
| --- | --- |
| `XHSNoteAnalyzer.analyze_note(..., use_llm=True)` | Optional LLM enhancement uses `try_stage_json`; parse/provider failure returns rule draft with `attach_llm_error(validation, "xhs_note_analyzer", error)` and keeps `validation.llm_enhanced=false`. |
| `XHSNoteAnalyzer.collect_for_session(...)` | Session skill learning requires LLM keyword/label stages. These stages route through `call_stage_json(json_mode=True)` and remain fail-fast when parse/provider calls fail, labels are empty, or labels are incomplete. |

Live runbook: [refs/data-collection-live-runbook.md](./refs/data-collection-live-runbook.md).

## Verification

| Test | Coverage |
| --- | --- |
| `tests/test_market_analysis_xhs_note_analyzer.py` | Note loading, rule/LLM enhancement, analyzer fallback metadata, session skill behavior, and required session JSON routing. |
| `tests/test_note_skill_fixture.py` | Report/fixture round trips and direct NoteMaker consumption. |
| `tests/test_model_coercion.py` | Shared model coercion defaults used by skill-learning and ops models. |
| `tests/test_domain_model_contracts.py` | XHS note sample / seed skill draft serialization and restoration. |
| `tests/test_data_collect_top_notes.py` | Top-notes contract without relying on live platform. |
| `scripts/smoke_session_skill.py` | Optional live end-to-end collection and skill report. |
| `wiki/refs/data-collection-live-runbook.md` | Redacted live setup, health check, smoke run, and troubleshooting procedure. |
