# Nori Workbench

Production-oriented frontend for the Nori content-generation workbench.

This app rebuilds the design handoff demo as maintainable React/TypeScript code
instead of extending the prototype bundle in `web/prototypes/`.

## Run

```bash
npm install
npm run dev
```

Open the Vite URL printed by the command, usually:

```text
http://127.0.0.1:5173/
```

Workspace routes are hash-based so the static build can be served without a
frontend router fallback:

- `/#compose` - content generation cockpit
- `/#planning` - account positioning, operating plan, and content calendar
- `/#context` - account memory, platform strategy, and market signals
- `/#skills` - reusable skill/spec system
- `/#library` - artifact store and delivery review

## Verify

```bash
npm test
npm run build
```

## Product Shape

The app follows the backend workflow contract described in `web/README.md`:

1. Intake: user brief, platform, content format, and assets.
2. Context: platform strategy, account profile, market signal, and references.
3. Spec: skill-backed `ContentDesignSpec` planning and review gates.
4. Generation: observable agent execution state.
5. Package: artifact preview, acceptance status, and export.

## Backend Boundary

Frontend code should call backend routes through the service boundary instead of
importing runtime modules from `nori/`.

For local development, Vite proxies `/api/*` to `http://127.0.0.1:8000/*`.
On startup the app requests a bootstrap payload. In default Vite development it
uses the local fixture:

```text
GET /mock/workbench-bootstrap.json
```

This keeps the demo clean when the backend is not running, and the top bar shows
`Mock bootstrap`.

The compose workspace follows the same rule. Its first backend-facing action is
run-template preparation. In default local development the button reads:

```text
GET /mock/content-generation-options.json
GET /mock/content-generation-plan.json
GET /mock/session.json
GET /mock/session-assets.json
GET /mock/reference-image-generation-check.json
GET /mock/run-template.json
GET /mock/preflight.json
GET /mock/content-run.json
GET /mock/content-production-runs.json
GET /mock/artifact-inspection.json
```

That keeps local QA free of backend-availability noise while still showing the
catalog-driven product flow: generation options, recommended entrypoint,
missing fields, checks, blocking reasons, run results, artifact inspection, and
next actions.

To force the real backend route, start Vite with:

```bash
VITE_NORI_USE_API=1 npm run dev
```

Then the app requests:

```text
GET /api/experiments/content-production/workbench
GET /api/content/generation/options
POST /api/content/generation/plan
POST /api/sessions
POST /api/sessions/{session_id}/assets
POST /api/sessions/{session_id}/assets/reference-image-generation-check
POST /api/experiments/content-production/run-template
POST /api/workflows/content-production/runs/preflight
POST /api/workflows/content-production/runs
GET /api/workflows/content-production/runs?case_id={case_id}
GET /api/workflows/content-production/runs/{case_id}/{run_id}/artifacts/inspect
```

Uploaded reference assets are session-backed. The compose workspace creates a
session on first upload, sends image files as multipart `files`, then includes
the resulting `session_id` and `asset_ids` in the run-template draft.
The operator can also run a reference image generation check before preflight;
when it passes, the template draft enables `require_reference_image_generation_check`.

If the backend request succeeds, the top bar shows `Backend live`. If it fails,
the app stays usable and shows `Local demo fallback`, making it explicit that
the page is rendering curated local product data rather than live backend state.

Start the backend separately when integrating real data:

```bash
python -m backend.server --host 127.0.0.1 --port 8000
```

Useful integration entrypoints:

- `GET /api/experiments/content-production/workbench`
- `GET /api/content/generation/options`
- `POST /api/content/generation/plan`
- `POST /api/sessions`
- `POST /api/sessions/{session_id}/assets`
- `POST /api/sessions/{session_id}/assets/reference-image-generation-check`
- `GET/POST /api/experiments/content-production/run-template`
- `POST /api/workflows/content-production/runs/preflight`
- `POST /api/workflows/content-production/runs`
- `GET /api/workflows/content-production/runs?case_id={case_id}`
- `GET /api/workflows/content-production/runs/{case_id}/{run_id}/artifacts/inspect`
