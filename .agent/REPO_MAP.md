# Repository Map

## Entry points

- `AGENTS.md` — mandatory Authority router for Codex.
- `project_goal.md` — root pointer to the durable project goal; not a second goal authority.
- `.agent/INDEX.md` — project-state retrieval router.
- `.agents/skills/authority/SKILL.md` — mandatory Codex Authority lifecycle.

## Major modules / packages

No application module or package exists or is authorized. `experiments/p00-foundation-qual/` is a disposable non-product qualification harness area with Python/Rust synthetic shells, oracle-backed JCS checks, multi-process IPC scripts, and exact SQLite/VFS scripts; its qualification-only Rust lock and cached oracle are not production dependency declarations.

## Important interfaces / contracts

- `.agents/skills/authority/references/directive-contract.md` — Architect-to-Codex directive contract.
- `.agents/skills/authority/references/result-contract.md` — Codex-to-Architect result contract.
- `.agents/skills/authority/references/evidence.md` — evidence ladder.
- `.agents/skills/authority/references/state-files.md` — project-state update rules.
- `.agents/skills/authority/references/safety.md` — safety boundary.
- `.agents/skills/external-discovery/SKILL.md` — prior-art/reuse workflow.

## Tests

No application test suite or governance test runner exists. Governance is validated with explicit structural/content/Git checks recorded in `.agent/OUTCOMES.md`.

## Generated / cache / build areas

Qualification binaries, toolchains, Godot archives, SQLite sources/builds, databases, WAL files, sockets, raw measurements, and temporary VFS runners are private local XDG cache/state outside Git. Existing `.gitignore` and protected primary Graft changes are untouched.

## Governance / agent files

- `.authority/VERSION.json` — Authority package/baseline provenance.
- `.agent/PROJECT_GOAL.md` — durable goal and permanent constraints.
- `.agent/PROJECT_PROFILE.md` — verified repository and technical profile.
- `.agent/CURRENT.md` — mutable current snapshot.
- `.agent/DIRECTIVES.md` — append-only directive ledger.
- `.agent/OUTCOMES.md` — append-only outcome/evidence ledger.
- `.agent/LEARNINGS.md` — append-only durable learnings.
- `.agent/RECORD.md` — append-only decisions and governance events.
- `.agent/REPO_MAP.md` — this repository map.
- `.agent/EXTERNAL.md` — append-only external discovery ledger.
- `.agent/tasks/` — conditional complex-task packets.

## Known sensitive/high-risk areas

No implementation exists. Future sensitive areas include identity/memory persistence, biometrics and perception, consent, trusted contacts, escalation policy/audit, backup/export/restore, secrets, and personal routine data.

## Preserved bootstrap files

- `.gitignore` — initial GitHub bootstrap file; unchanged by Authority installation.
- `LICENSE` — Apache License 2.0; unchanged by Authority installation.
