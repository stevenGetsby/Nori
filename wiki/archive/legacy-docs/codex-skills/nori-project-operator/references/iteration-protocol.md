# Nori Iteration Protocol

## Start

1. Run:

```bash
python 文档/codex-skills/nori-project-operator/scripts/nori_status.py
```

2. Read the relevant files for the selected area.
3. Check whether the requested task is design-only or implementation.

## Task Selection

Pick exactly one task unless the user asks for a larger batch.

Prefer this order:

1. Broken tests or broken imports.
2. LLM gateway safety and testability.
3. Data models for the account-operations loop.
4. Agent contracts with mocked tests.
5. Orchestration and persistence.
6. UI, live publishing, live crawler, and real API smoke tests.

## Implementation Rules

- Keep changes narrow.
- Use the owning business module's `models.py` for dataclass contracts; do not recreate the removed `nori/agent_models` compatibility root.
- Mock `llms.chat`, `llms.image`, and `DataCollector` in unit tests.
- Do not call live APIs from tests.
- Do not write secrets into docs, fixtures, or logs.
- If a live run is needed, add a smoke script and require explicit user approval before running it.

## Status Update Template

At the end of an iteration, update the project plan with:

```text
日期:
本轮目标:
改动:
测试:
风险/阻塞:
下一轮:
```

## Handoff

The final response should include:

- what changed;
- which tests passed or why tests were not run;
- the next recommended task.
