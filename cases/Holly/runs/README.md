# Holly Runs

Each direct child directory is one workflow run or probe. Existing legacy runs were migrated from `cases/Holly/runs`.

- `source/`: virtual run for source-level artifacts such as the original brief and showcase brief.
- `archive/`: older ad hoc generation tests kept for reference.
- `*_holly_live`: full content generation runs.
- `*_preflight`: preflight runs.
- `*_reference_fidelity*`: image reference fidelity probes.

New Holly content runs should be created through `CaseWorkspace.create_run_dir(...)` so `run.json` and `data/artifact_index/*.jsonl` stay current.
