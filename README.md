# Project History Agent / FIX — v0.6 candidate

Evidence-first project continuity, chat lineage and AI handoff system.

Canonical GitHub repository: `https://github.com/loftfull/FIX`

## Current architecture

1. `PROJECT_HISTORY.events.jsonl` — append-only SHA-256 hash-chained source of truth.
2. `PROJECT_MEMORY.json` — deterministic snapshot rebuilt from the journal.
3. `PROJECT_MEMORY.md` — human/AI-readable handoff projection.
4. `HistoryAdapter` providers discover prior sessions; they never decide lineage.
5. `detect_chat_lineage()` remains the evidence gate for `new / continuation / unknown`.

## v0.6 additions

- `ClaudeCodeHistoryAdapter` for Claude Code project/session JSONL;
- `CodexHistoryAdapter` for Codex rollout/session JSONL;
- `ChatGPTExportHistoryAdapter` for an explicitly supplied ChatGPT `conversations.json` export;
- current-chat public-safe source bundle under `chat/current/`;
- canonical repository provenance for `loftfull/FIX`;
- design + implementation plan under `docs/superpowers/`.

## Current-chat lineage

The current project chat is explicitly recorded as a continuation of the earlier ChatGPT chat `агент`:

```text
агент [new]
  -> current Project History Agent chat [continuation, explicit]
```

See `chat/current/PROJECT_MEMORY.md` and `chat/current/USER_MESSAGES.md`.

## Safety / truth rules

- request != implementation;
- plan != verified result;
- topic similarity alone never proves chat continuation;
- local path != current GitHub HEAD;
- secrets are redacted before journal persistence;
- no host adapter may mutate the source conversation history;
- ChatGPT account history is used only from an explicitly supplied export or an actual host-provided history interface.

## Verification

```bash
python -m unittest discover -s tests -v
python -m compileall -q project_history_agent.py project_history_journal.py project_history_auditor.py project_history_hooks.py project_history_doctor.py history_adapters.py
python project_history_doctor.py .
```

The browser screenshot E2E may report `ENV_BLOCKED` in restricted sandboxes; that is not counted as a screenshot PASS.

## Handoff entrypoints

For a new AI model, read in this order:

1. `PROJECT_MEMORY.md`
2. `PROJECT_HISTORY_AGENT.md`
3. `PROJECT_HISTORY.events.jsonl` only when detailed provenance is needed
4. `chat/current/PROJECT_MEMORY.md` for the current ChatGPT continuation chain
5. `SELF_TEST_REPORT.md`

## Status

v0.6 remains a **candidate** until the independent external-model audit gate A6 is completed against primary evidence, journal, snapshot and visual artifacts.
