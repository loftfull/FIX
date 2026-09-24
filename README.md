# Project History Agent / FIX

Canonical repository for Project History Agent, transferred from the ChatGPT project history on 2026-09-16.

Development history, current-chat lineage, durable event journals, handoff reports, tests, schemas and migration evidence are maintained in this repository.

## Current state

- Current development: **v0.8.1 candidate with subsequent repairs**, branch `codex/history-mcp-foundation`, draft PR #5. Not a fully accepted release.
- Current requirements and gaps: `PROJECT_MEMORY.md`; plan inventory: `docs/PLAN_COVERAGE_2026-09-24.md`. Resolve the actual checkout with `git rev-parse HEAD`; dated observations are not live HEAD pointers.
- Historical v0.6 checkpoint: `43d1f111b151c0ff2f6307271ab8b5fdc631fb04`; Actions `35063295715` PASS applies only to that checkpoint, not current code.
- Root history is Git-native segmented: immutable `PROJECT_HISTORY.events.jsonl` base plus ordered `PROJECT_HISTORY.segments/*.jsonl` continuations.
- Current ChatGPT continuation is preserved under `chat/current/` with explicit lineage `агент -> current`.
- A6 independent external-model audit remains NOT_RUN and blocks full acceptance.

## Development direction

Priority: complete a verified transfer of selected project history to a new session, preserving decisions, conflicts and unresolved sources. Host adapters, imports and MCP exist as bounded components. Continuous ChatGPT capture and automatic message-limit handoff remain unimplemented. See `docs/CRITIC_REVIEW_2026-09-24.md` and subsequent repair receipts.

## Core installation

Before any writer/lifecycle command run `python -m pip install -r requirements-core.txt`.
Portalocker3.2.0 supplies OS-backed locks. Persistent lock files are normal; never
delete them while any FIX process is running. MCP/visual/vault dependencies remain
in their separate requirements files. Stop older FIX writers before upgrading: old
age-based locks and OS locks are not a compatible mixed-process protocol.
