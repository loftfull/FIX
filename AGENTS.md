# Project History Agent standing instructions

Before work:

1. Read `PROJECT_HISTORY_AGENT.md`.
2. Read `PROJECT_MEMORY.md` and treat `PROJECT_HISTORY.events.jsonl` as the append-only source of truth.
3. Run `python project_history_doctor.py .` before claiming the handoff state is healthy.
4. Do not rewrite old journal records. State upgrades must be new `*.patch` mutations.
5. Do not classify chats as continuations from topic similarity alone.
6. Preserve evidence classes: requested / planned / reported / observed / verified / inferred / unknown.
7. Never persist real credentials or secrets. Redact before journal write.
8. After substantial work, update the journal and regenerate `PROJECT_MEMORY.json` + `PROJECT_MEMORY.md`.
