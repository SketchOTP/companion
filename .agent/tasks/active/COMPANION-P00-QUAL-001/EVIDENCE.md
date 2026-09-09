# Qualification Evidence Record

## Correction cycle 01 — evidence disposition (2026-09-09)

Status: `CORRECTION SUBMITTED — PUBLICATION / INDEPENDENT REVIEW PENDING`

The Architect Review 01 finding is retained: the original Candidate 1/2 IPC
result never crossed a socket, ordinary JSON serializers did not establish
JCS, SQLite readers were serial, the migration check was only a guard
observation, and backup/restore was count-only. Those are failed or limited
historical attempts, not silently upgraded evidence.

The replacement evidence is:

- **Toolchain/JCS — E3_TARGET_TESTED:** maintained `canonical@5.0.0` oracle
  (qualification-only, cached outside Git) agreed with Python and Rust on
  eight vectors including escaped duplicate decoded names and non-BMP UTF-16
  ordering; both shells passed persistent multi-message parity and release-Rust
  measurements. Rust remains a candidate only.
- **IPC — E3_TARGET_TESTED:** four real processes exchanged actual
  `SOCK_SEQPACKET` packets; care consumed `SCM_CREDENTIALS`, generation, and
  per-generation HMAC; sibling injection, stale channel/capability, replay,
  restart, and descriptor probes were exercised. `pidfd_getfd` returned exact
  `EPERM` on this host. Candidate 2 is not adopted and exclusions remain
  root/kernel/full-account/authorized-producer compromise.
- **SQLite — E3_TARGET_TESTED bounded:** exact 3.53.4 passed synchronized
  reader/writer overlap, migration rejection before mutation, full logical and
  schema backup equivalence, induced page-limit failure with post-reopen
  atomicity, and adapted deterministic commit/checkpoint VFS return/crash
  points. It remains blocked for adoption pending Architect review and any
  broader evidence required.
- **Godot — E1_OBSERVED** and **systemd-user — E3_TARGET_TESTED** remain
  accepted retained evidence; they were not rerun without a material change.

All generated binaries, caches, databases, WAL files, raw measurements, and
toolchains remain private local qualification state. No dependency, Phase 01
transition, product source, safety runtime, or product capability was
self-approved. Architecture v1.0 remains adopted and unchanged.

### Live authority re-fetch

The final live Notion query returned 45 Architecture Decision Ledger rows and
55 Research Evidence Register rows. Evidence 54 is the official Linux
`pidfd_getfd(2)` record; Evidence 55 is the official SQLite I/O-error,
crash/power-loss, and concurrency-testing record. Both were materially
available and included in this correction. No authority-count discrepancy
remains.

### Correction command receipts

- `python3 -m py_compile experiments/p00-foundation-qual/python/qual_shell.py experiments/p00-foundation-qual/scripts/*.py`: `PASSED`.
- Isolated `cargo build --offline --locked --release` and `cargo test --offline --locked`: `PASSED` (0 Rust unit tests; release build used for measurements).
- `jcs_conformance.py`: `PASSED`; eight oracle vectors, decoded escaped duplicate, non-BMP UTF-16 order, numeric profile rejections, and Python/Rust/oracle agreement.
- `run_toolchain_measure.py`: `PASSED`; 12 rounds × 32 warm requests, per-index digest parity, cold/warm latency, child CPU, and RSS retained privately.
- `ipc_trust_qualification.py --run`: `PASSED` bounded process matrix; weak baseline injection accepted as expected insufficiency, Candidate 2 attacks/restarts/stale controls passed, exact `pidfd_getfd=EPERM` retained.
- `sqlite_matrix.py`: `PASSED` bounded matrix; overlap, migration, page-limit atomicity, backup equivalence, and four adapted VFS fault outcomes passed with integrity/whole-or-absent checks.
- `git diff --check` and repository scope inspection: `PASSED`; no root `AGENTS.md`/`.gitignore` change in the secondary worktree and no generated qualification output tracked.

Status: `DRAFTED — FINAL SCOPE/PUBLICATION VALIDATION PENDING`

## Authority reconstruction

`ADEQUATE`: live Notion retrieval on 2026-09-09 returned all ten named pages without truncation, the full 45-row ADR ledger, and the full 53-row evidence register. ADR-38–45 and Evidence 47–53 were individually reconciled. Issue #4 was `OPEN` with one Architect execution-sync comment. Primary protected work showed only the two stated paths; the task ran in a clean local-ext4 secondary branch at `fb4d475…`.

Record exact live Notion/GitHub sources, counts, retrieval markers, current branch/worktree, protected-work proof, and confidence.

## External source register

- Rust 1.98.1 official release announcement: exact 1.98.1 fixes the 1.98.0 vtable miscompilation; private isolated toolchain; MIT/Apache-2.0; recheck before any upgrade.
- Python 3.12 official documentation: 3.12.14 current docs baseline; host CPython is 3.12.3; PSF License; docs do not prove host suitability.
- RFC 8785 and Linux unix(7): canonicalization and local-peer primitives; they do not choose a complete service or same-UID authorization design.
- Godot 4.7.2 release/archive/GitHub asset: 2026-08-18, commit `ed1daf0bf`, standard archive SHA-256 matched published GitHub digest; MIT; source-correlated integrity only.
- SQLite WAL/news/release/Backup API: exact 3.53.4, source ID and published sqlite3.c SHA3 matched; 3.52.0 withdrawn; public domain; no generic SQLite adoption follows.
- systemd user-service documentation and host `systemd 255`: transient-manager primitives; no production policy follows.

For every materially used source/artifact record title, owner, release/update date, URL, version/source ID/digest, license, what it proves, limitations, workstream, and recheck trigger.

## Commands and environment

All generated outputs are confined to sanitized private local XDG-style qualification state/cache roots. Retained raw machine-readable files include toolchain, IPC, and SQLite attempt/final JSON. Toolchain fixture SHA-256 is `569b94e…b8e5f`; both implementations produced digest `04d5a59a…b3f3e`. No private paths, usernames, hostnames, serials, credentials, media, or personal data are included in committed records.

Record sanitized commands, exact candidate versions, environment variables, local XDG root classes, seeds, fixture hashes, locks, and generated-artifact index. Do not publish usernames, hostnames, private paths, serials, credentials, media, or personal data.

## Test evidence

Toolchain parity/negative checks and 12-sample lifecycle rounds: `PASSED` (`E3`). Weak IPC same-user injection: `PASSED` as expected insufficiency; Candidate 2 bounded attack suite: `PASSED` (`E3`). Godot asset digest/version-only: `PASSED` (`E1`). SQLite attempt 1–2 harness defects are retained; final bounded matrix is `PARTIAL E3` because deterministic during-commit/checkpoint kills are `BLOCKED`. Transient user-supervision probe: `PASSED` (`E3`).

Link machine-readable results and summarize passes, failures, blocked cases, timing/resource distributions, IPC attacks, Godot version result, SQLite fault/restore results, and supervision probes.

## Scope validation

Final changed-path and protected-primary rechecks: `PASSED`. The task branch does not modify root `AGENTS.md` or `.gitignore`, and it adds no product directory or live-data integration. `git diff --check`, task worktree cleanliness after publication reconciliation, and final remote equality: `PASSED`. The protected primary worktree remains read-only with only its pre-existing Graft edits.

Publication: Notion coder report and parent directive were updated and re-fetched after the final reconciliation push; GitHub Issue #4 comment `5608260248` was posted; PR #5 is open and unmerged. No approval was claimed.

Prove protected root files were untouched, only authorized Git paths changed, generated outputs remained outside Git, no product directories or live data integrations were added, `git diff --check` passed, branch history is normal, the task worktree is clean, and issue/PR/Notion publication agrees.

## Evidence levels

No evidence exceeds `E3_TARGET_TESTED`. Product/runtime/safety capability, reliability, security certification, dependency adoption, and Phase 01 authorization are not established.

Use only `E1_OBSERVED` and `E3_TARGET_TESTED` where justified. State product/runtime/safety evidence as not established.
