<!-- Last verified: 2026-05-24 | Current stage: P0 Documentation Hygiene -->

# Spec: Shared Model Coercion

## Background

`nori.ops_models.account_ops` and `nori.agent_models.xhs_note` both normalize untrusted dict input in `from_dict()` methods. They previously carried duplicated private helpers for mapping, list-of-dict, string-list, optional string, and integer coercion. That makes new model contracts easy to drift as more agents and ops models are added.

## Goal

Centralize low-level model input cleanup without changing public dataclass contracts:

- provide a neutral shared module outside `agent_models` and `ops_models`;
- preserve existing ops behavior where blank strings in string lists are retained;
- preserve existing skill-learning behavior where blank strings are dropped;
- keep bool-to-int coercion guarded so `True` does not become `1` accidentally;
- parse persisted boolean strings such as `"true"` / `"false"` without using plain `bool(value)`;
- cover the shared defaults with offline tests.

## Non-Goals

- Do not introduce Pydantic or a DB layer.
- Do not convert all dataclass serialization into reflection.
- Do not change generated JSON shapes.

## Implemented Files

- `nori/_model_coercion.py`
- `nori/ops_models/account_ops.py`
- `nori/agent_models/xhs_note.py`
- `tests/test_model_coercion.py`

## Verification

- `python -m pytest tests/test_model_coercion.py tests/test_ops_models.py tests/test_ops_models_asset_research.py tests/test_note_skill_fixture.py tests/test_ana_agents_xhs_note_analyzer.py -q`

## Follow-Up

`bool_value(...)` is now the canonical helper for persisted boolean fields. `AccountPlannerInput.enable_search`, `NoteDraft.llm_enhanced`, and `SessionSkillReport.llm_enhanced` use it so `"false"` does not restore as `True`.
