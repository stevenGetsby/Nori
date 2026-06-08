<!-- Last verified: 2026-05-24 | Current stage: P1 Account-Ops Backend -->

# Design Principle

## Scope

Nori currently has no active product UI. `web/` is reserved for future product UI/prototypes; this file defines product/visual rules for generated XHS artifacts and future workbench UI, not a shipped frontend.

## Product UX Principles

| Principle | Rule |
| --- | --- |
| Operators need evidence | Show source assets, selected skill, references, prompt, and review output for each generated package. |
| Do not expose internals as choices | Users should not manually pick `NoteSkill` or model plumbing unless in debug mode. |
| Keep workflow inspectable | Each stage should expose inputs, outputs, errors, and artifact paths. |
| Default to manual publish | Until publish safety exists, output export-ready packages rather than direct posting. |

## XHS Cover Rules

| Area | Current rule |
| --- | --- |
| Aspect | Default `1072x1440`, close to XHS 3:4. |
| Subject | Product/IP/brand asset should dominate roughly 65-70% of the cover when applicable. |
| Text | Title comes from `NoteDraft.title`; keep cover text short and high contrast. |
| Reference assets | Prefer `usable_for=cover`, relevant `brand_signals`, and non-low-quality images. |
| Avoid | Fake platform UI, false verification, stray logo/watermark, overstuffed text, mismatched brand signals. |

## Future Workbench UI

| Surface | Required controls |
| --- | --- |
| Task intake | Prompt field, asset uploader, platform/content type selector, constraints. |
| Planning | Brief summary, account positioning, operation plan, KPI targets, calendar table. |
| Production | Content task list, generate/regenerate buttons, artifact viewer, prompt/reference inspector. |
| Review | Compliance score, issue list, required changes, accept/retry actions. |
| Metrics | Manual metric entry first, strategy iteration notes, next-task suggestions. |

## Artifact Inspection Contract

Every generated content package should eventually expose:

```text
task_id
brief
skill_refs
asset_bundle
note_draft
cover_result
review_report
version / created_at
```
