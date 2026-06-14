# Nori LLM API Map

## Gateway

All business code should call `llms`, not provider SDKs directly.

- `nori/nori_config.py`: loads `api_config.yaml`, resolves `provider::model_id`, applies `NORI_MODE`.
- `llms/config.py`: exposes `get_active(usage)` and `resolve(model_key)`.
- `llms/mode.py`: switches `direct` / `ghc`; `ensure_ready()` checks API key or GHC `/models`.
- `llms/client.py`: creates OpenAI-compatible sync/async clients.
- `llms/call.py`: exposes `chat`, `chat_json`, `achat`, and `image`.

## Active Usages

`api_config.yaml` maps each mode to usages:

- `llm`: text chat.
- `vision`: Intaker multimodal image tagging.
- `image`: image generation/editing.
- `video`: configured but no active business call site found.

Never quote provider keys in docs or logs.

## Text Chat

`llms.chat(messages, usage="llm", **kwargs)`:

- resolves active model by usage;
- merges model constraints:
  - `temperature_fixed`
  - `max_output`
  - `extra_body`
- uses `max_completion_tokens` for OpenAI/GHC `gpt-5*`, otherwise `max_tokens`;
- calls `client.chat.completions.create(...)`;
- returns the first message content stripped.

`llms.achat(...)` is the async equivalent.

`llms.chat_json(messages, usage="llm", **kwargs)`:

- calls `llms.chat(...)` with the same usage/kwargs;
- parses the returned content as a JSON object;
- accepts plain JSON, fenced JSON, or embedded JSON object text;
- raises `ChatJSONError` when the response is empty, invalid, or not an object;
- does not inject `response_format` by default, so provider compatibility stays unchanged unless a caller passes it explicitly.

## Image Generation

`llms.image(prompt, usage="image", size=None, reference_images=None, **kwargs)`:

- normalizes reference images from bytes, data URI, base64, or local path;
- for Google, uses native `google-genai` `generate_content`;
- for Relay + references, calls OpenAI-compatible `images.generate` with reference data URIs in `extra_body`, trying `image_urls`, `images`, then `image`;
- for other OpenAI-compatible providers + references, calls `images.edit`;
- without references, calls `images.generate`;
- returns URLs or `data:image/...;base64,...` strings.

`CoverDirectorAgent` saves the returned first image to disk.

## Current Call Sites

- `IntakeAgent`
  - text intake: `llms.chat_json(..., usage="llm")`, fallback to rules on failure.
  - image tagging: one multimodal `llms.chat_json(..., usage="vision")` per image, concurrent; failed image tags fall back to bare image assets.
- `AccountPlannerAgent`
  - `_llm_plan(...)`: `llms.chat_json(..., usage="llm")`, fallback to structural plan.
- `XHSNoteAnalyzer`
  - single-note enhancer, keyword generator, and note labeler all use `llms.chat_json(..., usage="llm")`.
  - session-level skill generation requires LLM success and enough collected notes.
- `NoteMakerAgent`
  - SkillPicker, AssetCurator, NoteComposer use `llms.chat_json(..., usage="llm")`.
  - failures raise `NoteMakerLLMError`.
- `CoverDirectorAgent`
  - reference selector and prompt writer use `llms.chat_json(..., usage="llm")`.
  - image maker uses `llms.image(..., usage="image")`.
  - failures raise `CoverDirectorError`.
- `llms.intent_extractor`
  - standalone P1 utility; JSON extraction with error field, no exception to caller.
- `llms.target_selector`
  - standalone edit-routing utility; JSON selection with error field, no exception to caller.

## Improvement Queue

1. Move secrets out of `api_config.yaml` into environment or ignored local config.
2. Route Intaker image tagging through `usage="vision"` or remove unused vision active model. (done)
3. Centralize JSON chat parsing instead of duplicating `_call_json` in agents. (`chat_json` added; `IntakeAgent`, `AccountPlannerAgent`, `XHSNoteAnalyzer`, `NoteMakerAgent`, and `CoverDirectorAgent` migrated)
4. Add model-call telemetry: usage, model key, latency, error class, artifact id.
5. Add provider capability checks before image edit/reference calls.
6. Add retry/backoff policy for transient LLM and image errors.
7. Create tests around config mode switching and image routing without live APIs.
