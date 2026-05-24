---
name: nori-project-operator
description: Operate the Nori codebase through bounded software-engineering iterations that move it from a Xiaohongshu content-generation agent toward an account-operations SOP Agent system. Use when Codex is asked to advance Nori, implement the next roadmap item, harden LLM/API calls, design or build ops_models or ops_agents, update the Nori automation plan, run Nori project maintenance, or continue recurring automation work for /Users/headmasterx/Documents/Nori.
---

# Nori Project Operator

## Core Contract

Run one small, verifiable Nori project iteration at a time. Favor backend contracts, model boundaries, tests, and progress updates over broad rewrites.

## Start Every Iteration

1. Work from `/Users/headmasterx/Documents/Nori` unless the user names another checkout.
2. Read these first:
   - `文档/Codex自动化推进计划.md`
   - `进度.md`
   - `README.md`
   - `references/roadmap.md`
3. Run:

```bash
python 文档/codex-skills/nori-project-operator/scripts/nori_status.py
```

If the installed skill copy has newer scripts, prefer:

```bash
python ~/.codex/skills/nori-project-operator/scripts/nori_status.py /Users/headmasterx/Documents/Nori
```

## Select One Task

Pick exactly one bounded task unless the user explicitly asks for a batch.

Priority order:

1. Broken tests, broken imports, or unsafe secret handling.
2. LLM gateway hardening: vision routing, central JSON chat helper, telemetry, provider capability checks.
3. Account-operations data models: project, brief, plan, calendar, tasks, reviews, metrics, strategy iterations.
4. Planning agents with mocked LLM calls: operation planner, KPI planner, calendar planner, topic planner.
5. Production bridge: content task to note generation to cover generation to content package.
6. Review and iteration: compliance reviewer, review analyzer, strategy optimizer.
7. UI, real publishing, live crawler, live metrics, and multi-platform adapters.

Use `references/account-ops-system.md` for the desired closed-loop product shape. Use `references/llm-api-map.md` before changing any LLM, image, vision, config, or JSON parsing code.

## Implementation Rules

- Treat Nori's current executable core as `IntakeAgent -> AccountPlannerAgent -> NoteMakerAgent -> CoverDirectorAgent`.
- Treat `data_collect` and `XHSNoteAnalyzer` as the research/skill-learning side, not as generation code.
- Treat `llms` as the only allowed direct model API gateway. Do not add raw provider SDK calls elsewhere unless extending `llms`.
- Do not print, copy, or document API keys from `api_config.yaml`.
- Do not run live crawler, live image generation, or expensive real LLM smoke tests unless the user asks for a live run.
- Mock `llms.chat`, `llms.achat`, `llms.image`, and data collection in unit tests.
- Prefer dataclasses and `to_dict` / `from_dict` style when extending current Nori models unless the repo deliberately migrates.
- Keep generation code separate from analysis-learning code:
  - `nori/gen_agents`: current user-facing generation.
  - `nori/ana_agents`: research, note analysis, and skill learning.
  - `nori/agent_models`: existing shared generation models.
  - `nori/ops_models`: future account-operations SOP models.
  - `nori/ops_agents`: future planning/review/optimization agents.
- Update docs only for behavior that exists or is explicitly marked as planned.

## Definition of Done

Each iteration must end with:

- one coherent change or a documented blocker;
- focused tests added or updated when code changes;
- focused tests run, then `python -m pytest tests -q` when feasible;
- `文档/Codex自动化推进计划.md` or `进度.md` updated with status, tests, risk, and next task;
- a concise handoff naming the next recommended task.

## Status Update Format

Append a short note to the relevant project progress document:

```text
日期:
本轮目标:
改动:
测试:
风险/阻塞:
下一轮:
```

## References

- Read `references/llm-api-map.md` before changing model routing, API config, JSON parsing, vision calls, or image generation.
- Read `references/roadmap.md` before choosing implementation work.
- Read `references/iteration-protocol.md` before running an automated or recurring Codex iteration.
- Read `references/account-ops-system.md` before adding ops models or ops agents.

## Scripts

- `scripts/nori_status.py`: redacted status summary for a Nori checkout.
