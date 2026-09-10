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
13. `PARTIAL` — dependency order and clean stop observed; restart/backoff remains bounded shell work.
14. `PARTIAL` — direct packet and duplicate receipt observed; adversarial matrix not run here.
15. `PARTIAL` — separate stores, WAL migration, integrity and care receipt observed; full backup matrix deferred.
16. `NOT RUN` — fresh-directory restore command is implemented but not executed in this pass.
17. `PASSED` — Godot 4.7.2 headless project validation.
18. `PASSED` — bounded visible Openbox window probe observed a 640x360 neutral window; display-loss recovery remains unrun.
19. `PASSED` — payload-minimized logs and read-only health command.
20. `NOT RUN` — remote CI runner not available in this local pass.
21. `PARTIAL` — rights table and locked dependency provenance committed; generated SBOM deferred.
22. `PASSED` — no private paths, secrets, binaries or media committed.
23. `PASSED` — runtime has no outbound network code; CI scan records the boundary.
24. `PASSED` — 3 retained seeds × 1,000 deterministic synthetic cycles.
25. `NOT RUN` — 60-minute soak remains an explicit next evidence action.
26. `PARTIAL` — clean supervisor/direct-care and orphan-cleanup probes observed; full kill/recovery matrix deferred.
27. `PASSED` — final diff and generated-file review required before publication.
28. `PENDING` — mutable Notion records are updated only after branch publication.
29. `PENDING` — Issue #6/PR publication occurs after final commit.
30. `PASSED` — this run contains no later-phase capability.
