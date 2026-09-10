# COMPANION-P00-QUAL-001 — Handoff

## Correction cycle 01 submission

Status: `CORRECTION SUBMITTED — INDEPENDENT ARCHITECT REVIEW REQUIRED`

Focused correction commit: `07d2bda94c341e72e5aa974f32a99b45b7c806fa`; pushed
normally to `origin/codex/p00-qual-001`. PR #5 is OPEN/DRAFT/UNMERGED and
Issue #4 is OPEN. The Notion report and parent directive were updated and
re-fetched after publication. Architect acceptance remains NOT RUN.

This focused correction supersedes the invalid portions of the first result
without erasing them. The IPC harness now uses separate supervisor, producer,
care, and same-user sibling processes with real `AF_UNIX SOCK_SEQPACKET`
traffic, `SO_PASSCRED`/`SCM_CREDENTIALS`, generation binding, capability
rotation, restart/replay, and a direct `pidfd_getfd` probe (`EPERM` observed).
The JCS harness uses a maintained cached oracle and reference edge vectors; the
Python/Rust shells agree on canonical bytes and sustained synthetic parity.
SQLite now exercises synchronized overlap, pre-mutation migration rejection,
full backup equivalence, a safe induced page-limit failure, and adapted
deterministic commit/checkpoint VFS faults. Godot and transient systemd
evidence are retained unchanged.

The result remains provisional. Candidate 2, Rust, SQLite 3.53.4, Godot
4.7.2, and systemd are recommendations/candidates only; no dependency,
supervisor, security mechanism, Phase 01 transition, or product capability is
adopted. Architecture v1.0 remains adopted and Roadmap Phase 01 remains
closed. PR #5 and Issue #4 must remain open for independent Architect review.

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

## Final hardening handoff

The committed `experiments/p00-foundation-qual/results/` bundle and
`validate_results.py` now provide the reproducible fail-closed acceptance
record. Exact package identity is `canonicalize@5.0.0`; queue overflow is
deferred. IPC and SQLite outcomes are bounded `E3_TARGET_TESTED` candidate
evidence, Godot remains retained `E1_OBSERVED`, and transient systemd remains
retained `E3_TARGET_TESTED`. Architecture v1.0 remains adopted, Roadmap Phase
01 remains closed, and no dependency or product capability is self-approved.

Focused hardening commit: `65ba92299338ae5b0484579cd089fa3bc7d99b28` (after
required merge `bbbe5cedd8f82779e3f3d3c369cfb70ba99e9135`). The result-file
hashes are recorded in `results/provenance.json`; the final reconciliation
publication remains limited to metadata/state synchronization.

## Architect Review 03 narrow correction handoff

Status: `NARROW EVIDENCE-BINDING CORRECTION IN PROGRESS — ARCHITECT REVIEW REQUIRED`.
Review merge: `1997e01` (normal merge of `origin/main` review commit
`2ce221d7d9d359e3b23a3b2d9c2619fe709ddae2`). Result summaries are generated
from sanitized runner output; provenance uses honest date-only UTC precision
and exact `canonicalize@5.0.0` npm integrity. The validator independently
checks result/fixture hashes and final Git ancestry, ignores
`validation_results.json` as evidence, and supports a `QUAL_RESULTS_ROOT`
tamper-negative run.

IPC fields are labeled by evidence class and required lifecycle, revocation,
old-channel, capability, descriptor, outage, and companion-independent results
are fail-closed. SQLite derives exact reader counts, migration immutability,
pre-existing state, 0-or-3 commit groups, checkpoint equality, and fault
metadata. Unsupported JCS/toolchain fields were removed; queue overflow stays
`DEFERRED_PHASE_01`.

After publication, bind `provenance.evidence_commit` to the narrow correction
SHA in the one permitted reconciliation commit, rerun validator and
tamper-negative, update PR #5 and Issue #4 without merging/closing, re-fetch
Notion/GitHub, and stop for independent Architect review. Architecture v1.0
remains adopted; Roadmap Phase 01, dependencies, product implementation, and
product capability remain closed.
