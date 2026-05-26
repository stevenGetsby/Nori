<!-- Last verified: 2026-05-24 | Current stage: P2 Data Collection + Skill Learning -->

# Spec: NoteSkill Fixture Bridge

## Background

`XHSNoteAnalyzer.collect_for_session()` already writes a skills-only JSON artifact, but downstream tests and smoke scripts still needed ad hoc JSON loading before calling `NoteMakerAgent`.

## Goal

Make learned `SessionSkillReport` outputs directly reusable by generation code:

- model-level `from_dict()` for `NoteEvidence`, `NoteSkill`, and `SessionSkillReport`;
- a stable skills-only fixture shape: `{"skills": [...]}`;
- one loader that accepts report objects, full report dicts, skills-only dict/list payloads, and JSON paths;
- a writer that creates deterministic fixture JSON for tests or smoke scripts.

## Contract

Public helpers:

- `load_note_skills(source) -> list[NoteSkill]`
- `note_skill_fixture(source) -> dict[str, Any]`
- `write_note_skill_fixture(source, path) -> Path`

Accepted source shapes:

- `SessionSkillReport`
- `NoteSkill`
- `list[NoteSkill | dict]`
- `{"skills": [...]}`
- JSON path containing the same dict shape

## Acceptance

- A full `SessionSkillReport.to_dict()` can be loaded back into `NoteSkill` objects.
- The skills-only JSON written by analyzer remains `{"skills": [...]}`.
- Legacy dicts using `id` instead of `skill_id` are accepted.
- Loaded skills can be passed to `NoteMakerAgent.run()` without manual conversion.

## Implemented Files

- `nori/agent_models/xhs_note.py`
- `nori/agent_utils/note_skill_fixture.py`
- `nori/agent_utils/__init__.py`
- `nori/ana_agents/xhs_note_analyzer.py`
- `tests/test_note_skill_fixture.py`
- `wiki/62-stage-data-collection-and-skill-learning.md`
- `wiki/60-stage-generation-core.md`
- `wiki/30-api-reference.md`
- `wiki/85-backlog.md`
