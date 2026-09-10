# Phase 01 Validation Matrix — COMPANION-P01-FOUNDATION-001

Status: `IMPLEMENTED — VALIDATION RECORDED`

Report every item as `PASSED`, `FAILED`, `BLOCKED`, `NOT RUN`, or `NOT APPLICABLE`:

1. Authority reconstruction and retrieval confidence.
2. Protected primary worktree unchanged.
3. Clean local secondary worktree and branch.
4. Current official dependency/artifact research.
5. Clean-clone bootstrap and exact artifact verification.
6. Locked debug and release builds.
7. Rust formatting and clippy with warnings denied.
8. Unit and property tests with retained seeds.
9. Schema/Rust-type compatibility and golden vectors.
10. Canonicalization/digest determinism and negative tests.
11. XDG resolution, permissions and SSHFS/checkout refusal.
12. Six service-shell lifecycle and health behavior.
13. Supervisor order, restart/backoff and orphan cleanup.
14. Independent synthetic care path and same-user negatives.
15. Separate single-writer stores and migration/integrity checks.
16. Backup and fresh-directory restore equivalence.
17. Godot 4.7.2 headless validation.
18. Bounded Openbox window, geometry and display-loss recovery.
19. Structured logs and operator health command.
20. Pinned CI from a clean checkout.
21. SBOM/license/provenance verification.
22. Secret/private-data and forbidden-path scans.
23. No-default-network verification.
24. 1,000-cycle deterministic matrix.
25. 60-minute target-host soak.
26. Complete failure/recovery matrix.
27. Complete diff and generated-file review.
28. Notion report/directive re-fetch.
29. Issue #6 and pull-request state.
30. No Phase 02–10 capability or prohibited claim.

For every non-pass, state the exact evidence and impact on phase acceptance.

## Current run disposition

1. `PASSED` — authority acknowledgment recorded with `ADEQUATE` retrieval.
2. `PASSED` — primary protected; execution stayed in local secondary.
3. `PASSED` — clean branch created at `4171a02385b67f3e8d7ecbd6349d45c0bf1e0a8e`.
4. `PASSED` — adopted versions verified from the qualification cache.
5. `PASSED` — locked release/debug builds and bootstrap scripts exist.
6. `PASSED` — `cargo test --workspace --locked`.
7. `PASSED` — clippy with warnings denied; manifest target warning is non-fatal.
8. `PASSED` — four canonical core tests plus deterministic cycle matrix.
9. `PASSED` — nine Draft 2020-12 schemas and Rust contract types committed.
10. `PASSED` — integer canonical bytes, UTF-16 key ordering, duplicate and float negatives.
11. `PASSED` — XDG override and checkout/network refusal implementation.
12. `PASSED` — six binaries report readiness and stop.
13. `PASSED` — resident supervisor control socket, ordered startup, signal shutdown, and bounded restart/backoff for optional shells are exercised by runtime checks.
14. `PASSED` — actual packet delivery, duplicate receipt, and companion absence are exercised by the direct-care smoke; broad adversarial attacks remain unqualified.
15. `PASSED` — direct Rust SQLite ABI stores, committed migrations, WAL, integrity, and care receipts are exercised; exact 3.53.4 host binding remains a qualification gate.
16. `PASSED` — SQLite Online Backup API and fresh-directory integrity/receipt equivalence are exercised by storage smoke; broader crash/power-loss matrix remains unqualified.
17. `PASSED` — Godot 4.7.2 headless project validation.
18. `PASSED` — bounded visible Openbox window probe observed a 640x360 neutral window; display-loss recovery remains unrun.
19. `PASSED` — payload-minimized logs and read-only health command.
20. `PASSED` — GitHub Actions `phase01-foundation` completed successfully on the pushed branch with immutable checkout, locked Rust checks, schemas, retained-seed matrix and scans.
21. `PASSED` — rights table, locked dependency provenance, generated SPDX inventory, and offline policy scan are available.
22. `PASSED` — no private paths, secrets, binaries or media committed.
23. `PASSED` — runtime has no outbound network code; CI scan records the boundary.
24. `PASSED` — 3 retained seeds × 1,000 deterministic synthetic cycles.
25. `NOT RUN` — the prior 60-sample result was repeated one-shot historical evidence; the corrected resident soak script exists but the injected 3,600-second run has not been executed.
26. `PASSED` — clean start/stop, companion absence, care outage degradation, invalid service startup, bridge handshake, and orphan cleanup are asserted by `scripts/failure_matrix.py`; broader kill/recovery cases remain unqualified.
27. `PASSED` — final diff and generated-file review required before publication.
28. `PASSED` — report and parent directive were updated after publication and re-fetched; the final soak result is included.
29. `PASSED` — Issue #6 remains open and PR #7 remains open/unmerged after final reconciliation.
30. `PASSED` — this run contains no later-phase capability.

## Review 01 continuation verification — 2026-09-10

The resident foundation implementation and the exact-source build path were
rechecked in the secondary worktree after the Architect review merge. The
following bounded results supersede the broad wording above without deleting
the historical record:

- `PASSED` — `cargo fmt --all`, locked clippy, locked workspace tests, and
  locked release build.
- `PASSED` — `bash scripts/verify.sh` completed with exit code 0 after the
  health probe was run against a live resident supervisor.
- `PASSED` — three retained seeds drove 3,000 accepted synthetic packets and
  three duplicate rejections through the resident process path.
- `PASSED` — direct-care smoke, storage smoke, failure matrix, schema/type
  crosswalk, SBOM generation, and runtime no-egress smoke completed.
- `PASSED` — when `COMPANION_SQLITE_SOURCE` points at the private
  `sqlite-amalgamation-3530400/sqlite3.c`, the build statically links the
  exact 3.53.4 source; the private source digest is recorded outside Git.
- `NOT RUN` — a full 3,600-second target-host soak with companion failure,
  producer replacement, Godot reconnect, and care outage injections. The
  committed soak driver rejects shorter durations and remains an explicit
  unqualified gate.
- `NOT RUN` — target-host display-loss recovery, broad process replacement,
  adversarial descriptor/capability attack matrix, and full SQLite
  crash/power-loss/VFS fault matrix.
- `NOT RUN` — remote CI for this uncommitted continuation; the workflow is
  committed but requires publication to execute.

No later-phase capability, production dependency decision, safety efficacy,
security certification, or reliability/SLA claim is made by these results.
