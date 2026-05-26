<!-- Last verified: 2026-05-24 | Current stage: P1 Account-Ops Backend -->

# Spec: Account Positioning Model

## Background

`AccountOperationProject.account_positioning` was a loose dict. That kept early planner integration easy, but it made downstream production/review code depend on undocumented keys from `AccountPlanResult`.

## Goal

Add a typed, provider-free `AccountPositioning` model that:

- normalizes `AccountPlanResult` into stable fields;
- preserves legacy dict payloads without dropping unknown keys;
- still supports `dict(project.account_positioning)` for older call sites;
- round-trips through `AccountOperationProject.to_dict()` / `from_dict()`;
- is produced by `OperationPlannerAgent`.

## Contract

Canonical fields:

- `positioning_id`
- `tags`
- `recommended_positioning`
- `audience_profile`
- `content_directions`
- `unique_selling_points`
- `content_pillars`
- `account_keywords`
- `cover_design_formats`
- `benchmark_refs`
- `benchmark_accounts`
- `ip_portrait_report`
- `source`
- `metadata`

Unknown legacy fields are preserved at the top level via `extra_fields`, but `extra_fields` itself is not emitted by `to_dict()`.

## Acceptance

- `AccountPositioning.from_account_plan()` extracts pillars, keywords, cover formats, and benchmark refs from `AccountPlanResult`.
- `AccountOperationProject(account_positioning={"persona": "..."})` serializes back to the same legacy shape.
- `OperationPlannerAgent(use_llm=False)` stores an `AccountPositioning` instance.
- Existing content production context remains compatible through `dict(project.account_positioning)`.
- Tests cover model extraction, legacy round trip, and planner integration.

## Implemented Files

- `nori/ops_models/account_ops.py`
- `nori/ops_models/__init__.py`
- `nori/ops_agents/operation_planner.py`
- `tests/test_ops_models_account_positioning.py`
- `wiki/61-stage-account-ops-backend.md`
- `wiki/30-api-reference.md`
- `wiki/85-backlog.md`
- `wiki/90-changelog.md`
