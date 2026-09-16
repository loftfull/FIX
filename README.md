# Project History Agent / FIX

Canonical repository for Project History Agent, transferred from the ChatGPT project history on 2026-09-16.

Development history, current-chat lineage, durable event journals, handoff reports, tests, schemas and migration evidence are maintained in this repository.

## Current state

- Stable candidate line: **v0.6** on `project-history-agent-v0.6`.
- Exact verified head: `43d1f111b151c0ff2f6307271ab8b5fdc631fb04`.
- GitHub Actions run `35063295715`: PASS (Compile, Repository smoke, segmented journal chain, Structural audit, Doctor).
- Root history is Git-native segmented: immutable `PROJECT_HISTORY.events.jsonl` base plus ordered `PROJECT_HISTORY.segments/*.jsonl` continuations.
- Current ChatGPT continuation is preserved under `chat/current/` with explicit lineage `агент -> current`.
- A6 independent external-model audit remains NOT_RUN and blocks full acceptance.

## Development direction

v0.7 focuses on host-native history discovery/wiring for Claude Code and Codex while keeping the core provider-neutral and evidence-gated. ChatGPT history remains explicit-only unless the host exposes an authorized history interface or the user provides an export.
