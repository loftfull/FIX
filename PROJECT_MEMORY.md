# PROJECT_MEMORY — AI handoff report

## 0. Карточка проекта
- Project ID: `project-history-agent`
- Имя: Project History Agent
- Описание: Evidence-first project historian with append-only journal, chat lineage, project passport, plan-to-fact ledger, visual provenance and host-native history adapters.
- Цель: Preserve evidence-based project history across chats, models, repositories and environments
- Каноническая версия: v0.7 candidate

## 0.1 Быстрый handoff для новой AI-модели
- Project ID: `project-history-agent`
- Каноническая версия: v0.7 candidate
- Текущий чат: chat-current-project-history-agent
- Следующий проверяемый шаг: Use docs/HISTORY_WORKFLOW.md for explicit import/local watcher. Retrieve original INSTA chat exports for full lineage; current reconstruction is partial. Validate Windows CI and deployment on user machine before claiming autonomous installed operation. Browser ChatGPT remote connection and full A6 remain open.
- Правило продолжения: сначала прочитать этот отчёт и PROJECT_MEMORY.json; не повышать reported/planned до verified без новой проверки.

## CRITICAL_CONSTRAINTS — обязательные ограничения
- Never infer chat continuation from topic similarity alone
- Keep requested/planned/reported/observed/verified distinct
- Redact secrets before persistence
- Do not call the system fully accepted before A6 independent external-model audit passes

## 1. Где находится проект
| Среда | Расположение | Branch | SHA | Статус | Проверено |
|---|---|---|---|---|---|
| github_code_checkpoint | https://github.com/loftfull/FIX | project-history-agent-v0.6 | f27e837e5941a9ecd6a36160f5efccc743e155f1 | historical_code_checkpoint | 2026-09-16 |
| chatgpt_library | /Project History Agent/v0.5 | — | — | observed | 2026-09-16 |
| github_branch | https://github.com/loftfull/FIX/tree/project-history-agent-v0.6 | project-history-agent-v0.6 | — | observed_now | 2026-09-16 |
| github_branch | https://github.com/loftfull/FIX/tree/project-history-agent-v0.7 | project-history-agent-v0.7 | — | observed_now | 2026-09-16 |
| github_code_checkpoint | https://github.com/loftfull/FIX/commit/bfbc90f6200150e171036a8367def055f49fd106 | project-history-agent-v0.7 | bfbc90f6200150e171036a8367def055f49fd106 | verified_code_checkpoint | 2026-09-16 |
| github_code_checkpoint | https://github.com/loftfull/FIX/commit/f2628d2a65294c063b0098ceb84b3d011b8208a4 | project-history-agent-v0.7 | f2628d2a65294c063b0098ceb84b3d011b8208a4 | verified_code_checkpoint | 2026-09-16 |

## 2. Цепочка чатов
| Дата | Чат | Класс | Родитель | Основание |
|---|---|---|---|---|
| 2026-09-15 | агент | new | — | explicit_origin |
| 2026-09-15 | Продолжение проекта из чата «агент» | continuation | chat-agent-origin | explicit |

## 3. Планы → фактические изменения
| План | Статус плана | Связанные версии | Фактически внесено |
|---|---|---|---|
| v0.3 deterministic ledger + structural auditor | implemented | v0.3 deterministic ledger + auditor | canonical PROJECT_MEMORY.json; deterministic dedupe; separate structural auditor; A1-A5 acceptance tests |
| v0.4 chat lineage + AI handoff + visual evidence | implemented | v0.4 chat lineage + handoff + visuals | first-run Chat Lineage Resolver; Project Passport and Quick Handoff; plan→fact/version ledger; visual evidence registry; current-chat and TERMINAL real tests |
| v0.5 durable journal + adapters + lifecycle + doctor | implemented | v0.5 durable project history | append-only SHA-256 journal; atomic persistence and lock; pre-persistence secret redaction; HistoryAdapter boundary; lifecycle hooks; doctor; deterministic replay |
| v0.6 canonical FIX transfer + host-native history adapters | implemented | v0.6 FIX canonical transfer + host-native adapters | canonical repository loftfull/FIX; current chat bundle in chat/current; Claude Code JSONL adapter; Codex rollout/session adapter; explicit ChatGPT conversations.json export adapter; v0.6 regression tests |
| v0.7 bounded direct host-history wiring | implemented | v0.7 direct host-history wiring | HostHistoryDiscovery with bounded Claude Code/Codex roots; ChatGPT explicit-export-only discovery; doctor auto-wires discovered adapter; discover-history and history-search CLI; provider discovery remains candidate-only, not lineage authority; stable-identity candidate ranking with explicit ref > repository > project+identity > path > project > artifact > topic; CLI optional current-context ranking without lineage classification |
| v0.7 stable-identity candidate ranking | implemented | — | — |

## 4. Версии и фактические изменения
### v0.3 deterministic ledger + auditor · 2026-09-15 · verified
- canonical PROJECT_MEMORY.json
- deterministic dedupe
- separate structural auditor
- A1-A5 acceptance tests
### v0.4 chat lineage + handoff + visuals · 2026-09-16 · verified
- first-run Chat Lineage Resolver
- Project Passport and Quick Handoff
- plan→fact/version ledger
- visual evidence registry
- current-chat and TERMINAL real tests
### v0.5 durable project history · 2026-09-16 · verified
- append-only SHA-256 journal
- atomic persistence and lock
- pre-persistence secret redaction
- HistoryAdapter boundary
- lifecycle hooks
- doctor
- deterministic replay
### v0.6 FIX canonical transfer + host-native adapters · 2026-09-16 · verified
- canonical repository loftfull/FIX
- current chat bundle in chat/current
- Claude Code JSONL adapter
- Codex rollout/session adapter
- explicit ChatGPT conversations.json export adapter
- v0.6 regression tests
### v0.7 direct host-history wiring · 2026-09-16 · verified
- HostHistoryDiscovery with bounded Claude Code/Codex roots
- ChatGPT explicit-export-only discovery
- doctor auto-wires discovered adapter
- discover-history and history-search CLI
- provider discovery remains candidate-only, not lineage authority
- stable-identity candidate ranking with explicit ref > repository > project+identity > path > project > artifact > topic
- CLI optional current-context ranking without lineage classification

## 5. Скриншоты и визуальные подтверждения
- Скриншоты не найдены или их источник пока недоступен.

## 6. Хронология
- 2026-09-15 · **verified** · Project History Agent originated in ChatGPT chat агент.
- 2026-09-15 · **verified** · Current chat explicitly requested continuation from chat агент.
- 2026-09-16 · **verified** · v0.5 durable history package passed its deterministic and real-project candidate gates; A6 remained NOT_RUN.
- 2026-09-16 · **requested** · User designated loftfull/FIX as repository for the current project and asked to transfer all current-chat project data and continue development.
- 2026-09-16 · **observed** · Current chat bundle, standing instructions, host-native adapters and v0.6 tests were transferred to FIX working branch.
- 2026-09-16 · **verified** · Local v0.6 regression: 58 tests discovered, 57 PASS, 0 FAIL/ERROR, 1 pre-existing ENV_BLOCKED browser-navigation skip.
- 2026-09-16 · **verified** · GitHub Actions run 35062306733 passed Compile, Repository smoke, Structural audit and Doctor on head 589bea6d60aed243da840b7d0fe2ac5101fee5e6.
- 2026-09-16 · **requested** · User requested continued autonomous development after v0.6 transfer and verification.
- 2026-09-16 · **observed** · Implemented bounded host-history discovery, doctor auto-wiring and CLI discovery/search for v0.7.
- 2026-09-16 · **verified** · GitHub Actions run 35064023880 passed the v0.7 host-history wiring gate on code checkpoint bfbc90f6200150e171036a8367def055f49fd106.
- 2026-09-16 · **verified** · GitHub Actions run 35064575273 passed stable-identity candidate ranking on code checkpoint f2628d2a65294c063b0098ceb84b3d011b8208a4.
- 2026-09-23 · **observed** · Implemented experimental read-only MCP bridge using official SDK 2.2.0; 42 local tests passed, including 10 bridge checks. Independent agent audit found redaction and provenance defects, corrected with regressions. INSTA completeness, remote ChatGPT access and daily autonomy remain untested; A6 remains open.
- 2026-09-24 · **observed** · Implemented revision-preserving normalized import, branch-aware ChatGPT adapter, sourced strategy review and local Git watcher with daily catchup. 90 local tests PASS; real 18-message chat and 139 INSTA issue comments plus two documents imported; repeated imports idempotent. Independent audits closed reproduced metadata/date/filter/redaction and handoff constraints defects. Original INSTA chats, user-machine deployment and full A6 remain unavailable/unaccepted.
- 2026-09-24 · **observed** · Initial Windows CI executed 58 tests with 1 failure and 6 errors from implicit cp1252 reads in test assertions; Linux jobs passed. Four test modules now explicitly read/write UTF-8. Windows rerun pending; no production readiness claim.

## 7. Варианты и ответвления
- `v0.3-ledger-auditor` — v0.3 deterministic ledger · archived
- `v0.4-lineage-handoff` — v0.4 lineage + handoff · archived
  - continues → `v0.3-ledger-auditor`
- `v0.5-durable-journal` — v0.5 durable journal · archived
  - continues → `v0.4-lineage-handoff`
- `v0.6-host-native-adapters` — v0.6 FIX canonical repo + host-native adapters · candidate
  - continues → `v0.5-durable-journal`
- `v0.7-host-wiring` — v0.7 bounded direct host-history wiring · candidate
  - continues → `v0.6-host-native-adapters`

## 8. Нерешённые противоречия
- Нет зафиксированных противоречий.

## 9. Очередь поиска
- Run A6 independent external-model audit against primary evidence + segmented journal + snapshot + current-chat bundle.
- Evaluate pre-compaction/session-end hooks for discovered Claude Code and Codex hosts.

## 10. Источники
- `S001` — Earlier ChatGPT chat агент
- `S002` — Current ChatGPT continuation chat bundle
- `S003` — v0.5 Library baseline
- `S004` — FIX GitHub code checkpoint
- `S005` — v0.6 local regression output
- `S006` — GitHub Actions run 35062306733
- `S007` — User continuation request for v0.7
- `S008` — FIX v0.7 working branch
- `S009` — v0.7 GitHub Actions run 35064023880
- `S010` — v0.7 ranking GitHub Actions run 35064575273
- `S011` — MCP foundation local trial and research 2026-09-23
- `S012` — Real evidence import, INSTA partial reconstruction and local observer trial
- `S013` — Windows CI encoding failure and explicit UTF-8 correction

## 11. Передача
- Текущий чат: chat-current-project-history-agent
- Следующий шаг: Use docs/HISTORY_WORKFLOW.md for explicit import/local watcher. Retrieve original INSTA chat exports for full lineage; current reconstruction is partial. Validate Windows CI and deployment on user machine before claiming autonomous installed operation. Browser ChatGPT remote connection and full A6 remain open.
- Обновлено: 2026-09-24T05:31:02.051685+00:00
