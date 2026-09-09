# Qualification Evidence Record

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

Pending final changed-path, secret scan, branch, diff, publication, and protected-primary recheck. No product directory or protected root file is part of the task branch.

Prove protected root files were untouched, only authorized Git paths changed, generated outputs remained outside Git, no product directories or live data integrations were added, `git diff --check` passed, branch history is normal, the task worktree is clean, and issue/PR/Notion publication agrees.

## Evidence levels

No evidence exceeds `E3_TARGET_TESTED`. Product/runtime/safety capability, reliability, security certification, dependency adoption, and Phase 01 authorization are not established.

Use only `E1_OBSERVED` and `E3_TARGET_TESTED` where justified. State product/runtime/safety evidence as not established.
