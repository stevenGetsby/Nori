# Artifact Index

This directory contains append-safe JSONL indexes for case-centric artifacts.

- `cases.jsonl`: one row per case workspace.
- `runs.jsonl`: one row per case run.
- `artifacts.jsonl`: one row per generated, source, or migrated artifact.

The files are optimized for simple local scanning by scripts and workbench prototypes. Human-readable source files remain under `cases/{case_id}/`.
