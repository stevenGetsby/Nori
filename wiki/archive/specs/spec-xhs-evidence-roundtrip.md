<!-- Last verified: 2026-05-24 | Current stage: Data Collection / Skill Learning -->

# Spec: XHS Evidence Round Trip

## Background

`XHSNoteAnalyzer` turns collected note metadata into `XHSNoteSample` and then into `XHSSeedSkillDraft`. These are evidence artifacts in the skill-learning pipeline and should be restorable from saved JSON snapshots just like `NoteSkill` and `SessionSkillReport`.

## Goal

Make XHS evidence artifacts restorable through model classes:

- `XHSNoteSample.from_dict(...)`;
- `XHSSeedSkillDraft.from_dict(...)`.

## Non-Goals

- Do not change analyzer output JSON shape.
- Do not change crawler or downloader behavior.
- Do not add live platform dependencies to default tests.

## Acceptance

- `XHSNoteSample.from_dict(note.to_dict()).to_dict() == note.to_dict()`.
- `XHSSeedSkillDraft.from_dict(draft.to_dict()).to_dict() == draft.to_dict()`.
- Note metrics are coerced through shared integer coercion, so string counts are accepted and booleans do not become `1`.
- Existing analyzer and fixture tests still pass.

## Verification

- `python -m pytest tests/test_agent_models.py tests/test_ana_agents_xhs_note_analyzer.py tests/test_note_skill_fixture.py tests/test_model_coercion.py -q`
