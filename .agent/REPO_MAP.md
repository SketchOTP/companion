# Repository Map

## Entry points

- `AGENTS.md` — mandatory Authority router for Codex.
- `.agent/INDEX.md` — current project-state router.
- `.agents/skills/authority/SKILL.md` — Authority lifecycle.
- `Cargo.toml` — Rust foundation workspace.
- `godot/project.godot` — Godot 4.7 embodiment project.

## Accepted Phase 01 foundation

- `crates/foundation-core/` — contracts, canonicalization, XDG paths,
  persistence, IPC, logging, and version foundations.
- `crates/foundation-services/` — ops-supervisor, companion-core, care-core,
  identity-consent-vault, sensor-gateway, and godot-bridge shells.
- `contracts/` — versioned JSON Schemas and fixtures.
- `migrations/` — companion/care/vault development migrations.
- `godot/` — neutral bounded habitat and bridge foundation.
- `scripts/` — bootstrap, verification, health, matrices, artifact, SBOM, and
  evidence tooling.
- `evidence/` — sanitized bounded engineering evidence.
- `experiments/p00-foundation-qual/` — preserved disposable Phase 00
  qualification harnesses; not product runtime.

## Active Phase 02 planned ownership

Codex must extend the repository with a clean structure equivalent to:

- `assets/reference/approved/` — exact approved identity/turnaround masters and
  manifests.
- `assets/authoring/` — project-authored construction, vector/pose/keyframe, and
  body-revision sources.
- `assets/clips/` — clip specifications and landmark/contact/event tracks.
- `assets/review/` — selected contact sheets and review derivatives within the
  ordinary-Git binary budget.
- `crates/embodiment-contracts/` or an equivalent bounded module —
  MonAnimationClip and intent/result types.
- `godot/mon/` — MonAvatar, layers, animation director, resource import, and
  test scenes.
- `tools/embodiment/` or equivalent — deterministic frame export, validation,
  atlas/pack, contact-sheet, artifact, and evidence tooling.
- `evidence/phase02-embodiment/` — sanitized manifests/results, not the complete
  generated PNG corpus.

The exact directory names may change when a cleaner modular layout is justified,
but source/reference/generated/runtime/review/evidence ownership must remain
unambiguous.

## Generated and binary outputs

Bulk full-canvas PNG frames, atlases, runtime packs, complete contact sheets, and
motion artifacts are deterministic versioned build/CI artifacts and local export
bundles. They are not ordinary-Git history by default. Do not configure Git LFS
without separate Architect/operator authority.

Private tool caches, build output, imported Godot cache, runtime data, databases,
WAL files, sockets, logs, and temporary measurements remain outside Git under
validated local XDG paths.

## Governance

- `.agent/CURRENT.md` — mutable current state.
- `.agent/INDEX.md` — retrieval map.
- `.agent/DIRECTIVES.md`, `OUTCOMES.md`, `LEARNINGS.md`, `RECORD.md`,
  `EXTERNAL.md` — append-only history after adoption.
- `.agent/tasks/active/COMPANION-P02-EMBODIMENT-001/` — active task.
- `.agent/tasks/completed/COMPANION-P01-FOUNDATION-001/` — accepted Phase 01
  packet and Architect acceptance.

## Sensitive/high-risk boundaries

Godot and asset tooling may not own organism state, memory, biometric identity,
consent, secrets, contacts, care policy, incidents, or notification authority.
No media capture, speech/model dependency, real user data, or live care behavior
is authorized in Phase 02.

## Protected operator files

The primary SSHFS worktree contains operator-owned modifications to root
`.gitignore` and `AGENTS.md`. Do not read the modified contents into evidence or
commit/reset/stash/overwrite/reformat/copy them.
