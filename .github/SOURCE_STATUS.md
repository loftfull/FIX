# Source status for FIX

Audit baseline: 2026-10-06 UTC. The default branch at that point contained only starter/configuration files. Additional collaboration documentation does not make it a working implementation.

The following branches contain source trees and need integration/acceptance review. They are candidates, not an approved canonical release. Commit counts do not establish product quality, approval or freshness. Counts below compare to the pre-audit default branch; later metadata commits change that comparison.

| Source candidate | Examined commit | Commits ahead / behind at audit | Source-tree entries |
| --- | --- | --- | --- |
| [codex/history-mcp-foundation](https://github.com/loftfull/FIX/tree/codex/history-mcp-foundation) | `70c074fa84e30b711860c5da01c1747fa05f1b21` | 80 / 0 | 175 |
| [project-history-agent-v0.7](https://github.com/loftfull/FIX/tree/project-history-agent-v0.7) | `c41a158a2df088fcd35e46c88580e98d805fd589` | 57 / 0 | 64 |

## Next integration gate (priority:P1)

1. Recover the owner-approved plan, product boundary and source branch from its existing instructions.
2. Check its CI, acceptance scenarios, deployment references, migrations and independent review requirements.
3. Integrate through a reviewable PR with exact source commits and a rollback plan. Resolve conflicts without discarding history.
4. Move the accepted implementation into the canonical branch only after the project gates pass.

Do not recreate the application from this starter branch while ignoring the existing implementation. Do not delete runtime, release or evidence branches because they are absent from this table.
