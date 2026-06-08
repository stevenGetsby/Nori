# Nori Web

`web/` is the product-frontend boundary for Nori.

It is intentionally separate from:

- `nori/`: Python runtime, agents, workflows, context, memory, and artifact contracts.
- `backend/`: product-service adapters that web clients should call.
- `wiki/visuals/`: architecture diagrams and static documentation visuals.
- `hyperframes/`: promotional video projects.

## Current Status

There is no production workbench app yet. This directory exists to keep UI
experiments and future frontend code out of documentation visuals and out of
Python runtime packages.

Existing static demos live under `web/prototypes/`, including the earlier
`nori-demo-html/` and the newer `nori-workbench-v2-demo/`. They are prototype
artifacts, not the product workbench and not backend-integrated UI.

## Intended Workbench Surface

The future Nori workbench should expose the real workflow contracts:

1. Intake: user brief, target platform, assets, and constraints.
2. Context: compiled `ContextPack` and agent-specific `ContextView`.
3. Spec: `ContentDesignSpec`, including selected skills, media plan, visual
   rules, acceptance checks, and human review gates.
4. Generation: `ArtifactGenerationAgent` execution status and artifact refs.
5. Package: `ContentPackage` preview, cover/image paths, note body, tags,
   prompts, source refs, material usage, and review output.

## Boundary Rules

- Do not put agent logic, prompt construction, LLM calls, crawler calls, or
  artifact persistence in `web/`.
- Do not import directly from deep `nori.agents.*` implementation modules from
  frontend code. Use `backend/` service routes once a backend-integrated UI exists.
- Keep prototype-only HTML under `web/prototypes/`.
- Keep architecture diagrams under `wiki/visuals/`.
- Keep promo-video compositions under `hyperframes/`.
