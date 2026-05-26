<!-- Last verified: 2026-05-24 | Current stage: P3 Production Orchestration -->

# Spec: Generation Artifact Round Trip

## Background

`ContentProducerAgent` stores full `NoteDraft.to_dict()` and `CoverResult.to_dict()` snapshots in `ContentPackage.prompts`. Those snapshots were useful for inspection, but the generation artifact models did not have explicit `from_dict()` methods, forcing future artifact stores or replay tools to rebuild them manually.

## Goal

Make generation artifacts restorable through their model classes:

- `UserAsset.from_dict(...)`;
- `AssetBundle.from_dict(...)`;
- `CandidateTitle.from_dict(...)`;
- `NoteDraft.from_dict(...)`;
- `CoverResult.from_dict(...)`.

## Non-Goals

- Do not change the serialized JSON shape.
- Do not make production persistence decisions.
- Do not add database or replay runtime.

## Acceptance

- `AssetBundle.from_dict(bundle.to_dict()).to_dict() == bundle.to_dict()`.
- `NoteDraft.from_dict(draft.to_dict()).to_dict() == draft.to_dict()`.
- `CoverResult.from_dict(cover.to_dict()).to_dict() == cover.to_dict()`.
- Existing NoteMaker, CoverDirector, and ContentProducer tests still pass.

## Verification

- `python -m pytest tests/test_agent_models.py tests/test_gen_agents_note_maker.py tests/test_gen_agents_cover_director.py tests/test_ops_agents_content_producer.py -q`

## Follow-Up

`NoteMakerAgent` and `ContentProducerAgent` now delegate dict asset inputs to `UserAsset.from_dict(...)`, making that method the single normalization point for generated and user-supplied asset dictionaries.
