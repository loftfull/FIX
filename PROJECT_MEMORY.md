# PROJECT_MEMORY — AI handoff report

## 0. Карточка проекта
- Project ID: `project-history-agent`
- Имя: Project History Agent
- Описание: Evidence-first project historian with append-only journal, chat lineage, project passport, plan-to-fact ledger, visual provenance and host-native history adapters.
- Цель: Preserve evidence-based project history across chats, models, repositories and environments
- Каноническая версия: v0.6 candidate

## 0.1 Быстрый handoff для новой AI-модели
- Project ID: `project-history-agent`
- Каноническая версия: v0.6 candidate
- Текущий чат: chat-current-project-history-agent
- Следующий проверяемый шаг: A6 independent external-model audit; then v0.7 direct host wiring / archive policy.
- Правило продолжения: сначала прочитать этот отчёт и PROJECT_MEMORY.json; не повышать reported/planned до verified без новой проверки.

## 1. Где находится проект
| Среда | Расположение | Branch | SHA | Статус | Проверено |
|---|---|---|---|---|---|
| github_code_checkpoint | https://github.com/loftfull/FIX | project-history-agent-v0.6 | f27e837e5941a9ecd6a36160f5efccc743e155f1 | historical_code_checkpoint | 2026-09-16 |
| chatgpt_library | /Project History Agent/v0.5 | — | — | observed | 2026-09-16 |
| github_branch | https://github.com/loftfull/FIX/tree/project-history-agent-v0.6 | project-history-agent-v0.6 | — | observed_now | 2026-09-16 |

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

## 7. Варианты и ответвления
- `v0.3-ledger-auditor` — v0.3 deterministic ledger · archived
- `v0.4-lineage-handoff` — v0.4 lineage + handoff · archived
  - continues → `v0.3-ledger-auditor`
- `v0.5-durable-journal` — v0.5 durable journal · archived
  - continues → `v0.4-lineage-handoff`
- `v0.6-host-native-adapters` — v0.6 FIX canonical repo + host-native adapters · candidate
  - continues → `v0.5-durable-journal`

## 8. Нерешённые противоречия
- Нет зафиксированных противоречий.

## 9. Очередь поиска
- Run A6 independent external-model audit against primary evidence + journal + snapshot + current-chat bundle.
- Evaluate direct host wiring for Claude Code/Codex adapters without weakening evidence-gated lineage.

## 10. Источники
- `S001` — Earlier ChatGPT chat агент
- `S002` — Current ChatGPT continuation chat bundle
- `S003` — v0.5 Library baseline
- `S004` — FIX GitHub code checkpoint
- `S005` — v0.6 local regression output
- `S006` — GitHub Actions run 35062306733

## 11. Передача
- Текущий чат: chat-current-project-history-agent
- Следующий шаг: A6 independent external-model audit; then v0.7 direct host wiring / archive policy.
- Обновлено: 2026-09-16T06:01:31.827825+00:00
