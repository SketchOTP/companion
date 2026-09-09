# COMPANION-P00-QUAL-001 — Handoff

Status: `PARTIAL QUALIFICATION COMPLETE — INDEPENDENT ARCHITECT REVIEW REQUIRED`

## Executive result

- Toolchain: frozen Python 3.12.3 and isolated Rust 1.98.1 shells agreed on the selected JCS fixture and negatives. Recommend Rust as the future authoritative-service candidate, not adopted (`E3`).
- IPC: same-user pathname injection succeeded and rejects the weak baseline. A private seqpacket/generation/capability/nondumpable candidate passed the bounded synthetic attacks; recommend it for a later implementation experiment, not adoption (`E3`).
- Godot: exact standard 4.7.2 artifact has a matching official GitHub SHA-256 and version/build output; no GUI/project/renderer operation occurred (`E1`).
- SQLite: exact 3.53.4 amalgamation source identity and published sqlite3.c SHA3 matched. The bounded local matrix passed many atomicity, recovery, and backup cases but is incomplete because deterministic commit/checkpoint-kill tests are blocked (`E3 partial`).
- Supervision: a degraded user manager nevertheless ran transient synthetic user services; no Companion-named failed unit was observed. systemd user supervision is feasible as a later candidate (`E3`).

None of these results opens Roadmap Phase 01 or adopts a language, IPC mechanism, Godot artifact, SQLite build, or supervisor.

Summarize each workstream, exact evidence level, recommendation, failed/blocking cases, and why the result does or does not permit a Phase 01 opening.

## Architect decisions requested

1. Whether the bounded Rust result is sufficient to select Rust for future authoritative-service implementation, with Python retained only for tooling/tests.
2. Whether to authorize Candidate 2's private-channel plus per-generation-capability IPC design for a real Phase 01 process-shell test.
3. Whether the Godot source-correlated artifact evidence is enough to approve the exact 4.7.2 dependency in a later directive.
4. Whether to authorize an intrusive local SQLite fault-VFS or equivalent to complete deterministic commit/checkpoint kill coverage; until then SQLite remains blocked.
5. Whether to carry systemd user supervision into a later Phase 01 foundation directive.

Present only evidence-backed decisions:

- authoritative service toolchain;
- direct-care IPC producer identity/capability design;
- Godot 4.7.2 artifact disposition;
- exact SQLite artifact/build disposition;
- supervision direction;
- any required follow-up.

Do not self-adopt.

## Repository and publication

Base: `fb4d4750182bae765e8366265d6cfb1ee36e105d`; branch: `codex/p00-qual-001`; qualification commits: `c6c8141a28186b4b30ad438c7f504fce9602f070`, `9668cad9b1c1062f0b4c322784fe53f5c52eaad3`, and reconciliation `db136f60c6548718caa809ef06ec4fd71873e612`. PR #5 targets `main` and is open/unmerged; Issue #4 is open and contains comment `5608260248`. The required Notion coder report and parent directive were updated and re-fetched after the reconciliation push; final remote equality passed. Primary Graft edits remained protected and were never read into this packet.

Record baseline, task branch, commits, PR, issue, changed paths, clean worktree, protected main-worktree status, Notion report, and remote equality.

## Boundary

Architecture v1.0 remains adopted. Roadmap Phase 01, all dependency adoption, ordinary product implementation, media, live safety behavior, and product-capability claims remain pending Architect authority.

Explicitly confirm that Architecture v1.0 remains adopted, while Roadmap Phase 01, dependencies, ordinary product implementation, real media, live safety behavior, and product-capability claims remain pending Architect authority.
