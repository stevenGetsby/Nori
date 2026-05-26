<!-- Last verified: 2026-05-24 | Current stage: P1 Account-Ops Backend | Status: implemented -->

# Spec: Asset Library And Competitor Research Models

## Background

P1 still tracks client source materials and competitor evidence as loose dicts: `ClientBrief.source_materials`, `ContentTask.references`, and `AccountOperationProject.account_positioning`. This makes later production, review, and DataCollector integration harder because there is no stable contract for asset ids, usage, metrics, or evidence provenance.

## Goal

Add provider-free dataclass models:

- `AssetRecord`
- `AssetLibrary`
- `CompetitorSample`
- `CompetitorResearch`

Attach `asset_library` and `competitor_research` to `AccountOperationProject`.

## Non-Goals

- No DB persistence.
- No file copy or media download.
- No live crawler call.
- No replacement of legacy `ClientBrief.source_materials` or `ContentTask.references` in this pass.

## Contracts

### AssetRecord

Fields:

- `asset_id`
- `kind`
- `path`
- `text`
- `usage`
- `status`
- `tags`
- `source`
- `metadata`

### AssetLibrary

Fields:

- `library_id`
- `assets`
- `notes`
- `metadata`

Helpers:

- `usable_assets(usage=None) -> list[AssetRecord]`
- `get(asset_id) -> AssetRecord | None`

### CompetitorSample

Fields:

- `sample_id`
- `platform`
- `author_name`
- `note_id`
- `title`
- `url`
- `keyword`
- `metrics`
- `summary`
- `content_angles`
- `source_refs`
- `metadata`

### CompetitorResearch

Fields:

- `research_id`
- `platform`
- `keywords`
- `samples`
- `insights`
- `metadata`

Helpers:

- `top_samples(metric="liked", limit=5) -> list[CompetitorSample]`
- `to_task_references(limit=5) -> list[dict]`

## Compatibility

Existing fields remain:

- `ClientBrief.source_materials`
- `ContentTask.references`
- `AccountOperationProject.account_positioning`

New models add typed structure without forcing migration.

## Verification

- Unit tests cover round-trip serialization, helper behavior, nested `AccountOperationProject` serialization, and package compatibility.
- Default suite remains `python -m pytest tests -q`.
