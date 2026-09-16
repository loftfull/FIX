# GitHub analogue audit — Project History Agent

Дата проверки: 2026-09-16

Цель: найти решения, из которых можно перенести архитектурные паттерны, не превращая Project History Agent в тяжёлую memory-platform.

## `thedotmack/claude-mem`

Полезные паттерны: persistent memory между сессиями, lifecycle hooks, observations/summaries/citations, progressive disclosure, автоматическое восстановление контекста. В PHA перенесены session-start discipline, quick handoff и source IDs; отдельный worker/vector DB не принят как обязательная зависимость.

## `Vvkmnn/claude-historian-mcp`

Наиболее близкий аналог history discovery. Полезны scoped search, `inspect(session_id)`, streaming JSONL, deduplication, project/file-aware ranking. В PHA v0.5/v0.6 это превратилось в `HistoryAdapter.search/inspect`; relevance score остаётся только способом найти кандидата и никогда не доказывает continuation.

## `basicmachines-co/basic-memory`

Полезны local-first plain text, multi-host MCP, session-start/pre-compaction checkpoint, snapshots/backups. PHA сохраняет Markdown как portable projection и JSON/journal как детерминированное состояние, не принимает full knowledge graph/vector stack как обязательный core.

## `rosehgal/handoff`

Самый близкий handoff-аналог: per-project handoff, session-start/action/stop hooks, append-only JSONL source of truth, Markdown projection, atomic writes/file locks, cross-agent work, secret redaction до записи и doctor. Эти архитектурные паттерны реализованы в v0.5, при этом PHA сохраняет собственные evidence-gated chat lineage, locations, plan→fact, branches и visual provenance.

## `Rimagination/ChatMem`

Подтверждает ценность provider-neutral local history для Claude, Codex, Gemini, OpenCode, Hermes и других агентов. v0.6 следует этому направлению узко: provider readers находятся за `HistoryAdapter`, а core получает нормализованные evidence candidates.

## v0.6 implementation

Реализованы:
- `ClaudeCodeHistoryAdapter` — read-only Claude Code JSONL;
- `CodexHistoryAdapter` — read-only Codex rollout/session JSONL;
- `ChatGPTExportHistoryAdapter` — только явно переданный `conversations.json` export;
- canonical repository `loftfull/FIX`;
- current-chat journal/snapshot/handoff in `chat/current/`.

Не делать в core пока:
- собственную vector DB;
- always-on daemon;
- cloud/team sync;
- автоматическое semantic merging чатов;
- vendor-native state authority.

Главный differentiator PHA остаётся прежним: history search лишь находит evidence candidates; решение `new / continuation / unknown` принимает отдельный evidence-gated lineage resolver.
