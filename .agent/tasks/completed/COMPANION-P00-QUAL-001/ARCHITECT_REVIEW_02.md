# Architect Review 02 — COMPANION-P00-QUAL-001

## Verdict

`CONTINUE — FINAL EVIDENCE HARDENING REQUIRED`

- Reviewed base: `9ea7cdbb824a9d5be88181a4374df7a4e593fbbe`
- Reviewed PR head: `9be80e14e907f7973c1161bda041986e06f85a6e`
- Pull request: `#5` — open, draft, unmerged
- GitHub issue: `#4` — open
- Merge approval: `NOT GRANTED`
- Architecture v1.0: `ADOPTED / UNCHANGED`
- Roadmap Phase 01: `CLOSED`
- Dependency adoption: `NONE`
- Product implementation: `CLOSED`
- Canonical Notion review: https://app.notion.com/p/3d6833cb27ff8113bc7dcc42e96237f0

## Review scope

The Architect independently inspected PR #5 metadata and correction history, the corrected Notion result, the complete changed-file list, and the actual Python, Rust, Node, IPC, measurement, SQLite, and VFS source. Primary sources were rechecked for RFC 8785, Linux `pidfd_getfd`, SQLite fault testing, and the `canonicalize` package identity.

## Evidence accepted for retention

Do not repeat these items unless their inputs change:

1. Protected primary-worktree handling and clean ext4/NVMe secondary-worktree use.
2. The weak mode-0600 pathname-socket result proving same-UID plus declared identity is insufficient.
3. The corrected use of separate supervisor, producer, care, and attacker processes with actual `SOCK_SEQPACKET` traffic, `SCM_CREDENTIALS`, producer PID/UID checking, pidfd liveness checking, generation/capability rejection, restart/replay exercises, and the exact host `pidfd_getfd=EPERM` observation. This is bounded candidate evidence, not mechanism adoption.
4. The exact Godot 4.7.2 artifact evidence already accepted at `E1_OBSERVED`.
5. The transient systemd-user feasibility evidence already accepted at bounded `E3_TARGET_TESTED`.
6. The corrected Python/Rust release-build measurements as provisional engineering measurements only.
7. The improved SQLite overlap, migration rejection, backup/restore equivalence, page-limit failure, and narrow `xSync` fault observations as bounded candidate evidence only.

## Why PR #5 is not yet mergeable

### 1. No committed machine-verifiable result set or fail-closed gate

Detailed outputs remain only in private local storage. The repository has narrative summaries but no sanitized result bundle tying each claim to exact commands, artifact identities, fixture hashes, expected outcomes, observed outcomes, and pass/fail derivation.

Several scripts can exit successfully when critical expectations are false:

- the IPC matrix prints a result object but does not assert every required security and lifecycle outcome;
- the SQLite matrix writes results and prints booleans without failing when overlap, migration, restore, fault integrity, or atomicity checks are false;
- the toolchain runner compares only `accepted` and digest for valid unique messages, not complete response, rejection, and idempotency parity.

A green process exit is not yet an acceptance gate.

### 2. IPC ownership and supervisor trust claims are imprecise

The corrected IPC path is real. However, the supervisor retains original copies of both socketpair endpoints and retains the generation secret during the test. This differs from the durable claim that each child receives the only required endpoint and all unrelated copies are closed.

The supervisor is a trusted lifecycle authority, so limited retention may be permissible, but it must be explicit and least-privileged:

- close the supervisor's producer-side data endpoint after handoff;
- either close the care-side copy after startup or state precisely why the trusted supervisor retains it for care restart and prove it never reads or consumes producer packets;
- state that the supervisor provisions and revokes capabilities and is therefore trusted, rather than implying the capability is secret from the supervisor;
- assert child readiness, child `PR_SET_DUMPABLE=0` success, descriptor inheritance state, expected kernel credentials, pidfd status, generation, and revocation outcomes.

### 3. RFC 8785/profile coverage and Python/Rust parity remain overstated

The maintained package is named `canonicalize` version `5.0.0`, not `canonical` version `5.0.0`. Record its exact source commit or registry-integrity identity and the exact Node runtime.

The current JCS runner sends eight standalone vectors only to the Node oracle. Python and Rust are compared with the oracle for one extended valid event. Therefore nested, control, non-BMP, and primitive claims across all three implementations are not yet established.

Additional parity defects:

- Python `--canonical` validates an event; Rust `--canonical` canonicalizes parsed input without calling event validation.
- Server-level duplicate and idempotency behavior is not exercised because every measured request ID is unique.
- Invalid and rejection responses are not compared across languages.
- The reported queue-overflow check is a local container probe; both servers process and immediately remove one message, so no real service-level overflow is exercised.
- The measurement client does not implement robust exact-length header reads.
- `cargo test` reports zero tests.

These defects do not invalidate the provisional timing data, but they block a toolchain selection claim based on semantic parity.

### 4. SQLite verdict derivation is too weak

The corrected SQLite harness improves the exercised surface, but:

- `fault_matrix()` reports `status=PASSED` whenever the runner exists even if `all_integrity_ok` or `all_whole_or_absent` is false;
- `count in {0,1}` is not an atomicity proof for a one-row primary-key transaction;
- a checkpoint fault happens after the target transaction is committed, so allowing target count `0` would accept committed-data loss;
- the commit fault needs a multi-row transaction so all-or-none behavior is distinguishable;
- expected fault-runner exit status is not asserted;
- the VFS does not record which file class, `xSync` flags, or fault ordinal was injected.

Narrow `xSync` evidence may remain bounded. `xWrite`, `xTruncate`, WAL-index, compound-failure, and power-loss behavior remain unqualified.

### 5. Publication records are stale or imprecise

PR #5's body still describes the pre-correction SQLite blocker and does not summarize the corrected evidence. The Notion report uses `canonical@5.0.0`, which is not the package name.

## Final focused correction

Continue on `codex/p00-qual-001` and PR #5. Do not create another branch or PR.

### A. Commit a sanitized evidence bundle and validator

Add `experiments/p00-foundation-qual/results/` containing:

- a provenance manifest with exact commands, source commits, candidate versions, tool/runtime versions, fixture hashes, artifact hashes, timestamps, sanitized host-class fields, and result-file hashes;
- sanitized JSON outputs for JCS/toolchain, IPC, and SQLite;
- an assertion-driven top-level validator that consumes the committed result files and exits nonzero for any unmet expected outcome;
- a README defining the evidence ceiling and regeneration procedure.

Do not commit private paths, host/user names, secrets, raw capability bytes, serials, media, downloaded binaries, databases, WAL files, or caches.

### B. Harden IPC evidence

- Close the supervisor's producer-side socket copy after producer handoff.
- Minimize and explicitly document any supervisor-held care endpoint or secret required for restart; remove misleading exclusive-ownership claims.
- Add a readiness barrier and assertions for child hardening, endpoint inheritance, expected `SCM_CREDENTIALS`, pidfd liveness, valid/duplicate/spoof/malformed/stale outcomes, care restart, producer replacement, old-channel revocation, old-capability rejection, companion absence, and degraded producer outage.
- Record the exact `pidfd_getfd` outcome without treating `EPERM` as universal proof.
- Exit nonzero when any expected result differs.

### C. Complete bounded canonicalization/toolchain parity

- Correct all package references to `canonicalize@5.0.0`.
- Record exact package source commit or registry-integrity identity, tarball digest, Apache-2.0 license, Node requirement, and exact Node runtime.
- Run every relevant object, string, nesting, control, and non-BMP valid vector through Python, Rust, and the oracle by embedding it inside a valid project-profile event where necessary.
- Keep RFC 8785 floating-point examples oracle-only while asserting that both project-profile shells reject non-integer numeric input.
- Align Python and Rust canonical/event validation behavior and rejection codes.
- Add escaped-name duplication, server-level duplicate/idempotency, malformed/version rejection, controlled shutdown, and complete response parity checks.
- Implement a real bounded service queue-overflow test or remove every queue-overflow qualification claim and mark it deferred to Phase 01.
- Implement exact-length header reads in the measurement client.
- Add Rust tests that fail on canonicalization, duplicate-key, framing, idempotency, and rejection regressions; zero tests is not a passing test suite.

### D. Make SQLite tests fail closed

- Derive overall status only from asserted sub-results; exit nonzero if concurrency, migration immutability, disk-full atomicity, backup/restore equivalence, integrity, expected fault exit, or fault outcome fails.
- Assert reader counts before and after commit, not only barrier strings.
- Require complete pre/post logical equality for the failed disk-full transaction.
- Use a multi-row commit transaction and prove the entire group is present or absent.
- For checkpoint faults, require every already committed row to remain present and the logical state digest to remain unchanged after reopen.
- Record and assert the injected `xSync` file class, flags, and ordinal.
- Preserve the narrow evidence ceiling and keep SQLite non-adopted.

### E. Reconcile publication

Update the task records, Coder Qualification Report, parent directive, PR #5 body, and Issue #4. Preserve earlier failed attempts as history. Leave PR #5 draft/open/unmerged and Issue #4 open.

## Acceptance gate

The next review requires:

1. Sanitized machine-readable results committed and tied to exact provenance.
2. One top-level validation command that fails closed and passes on the committed result set.
3. IPC expected outcomes asserted and supervisor endpoint/secret ownership described accurately.
4. Every claimed valid canonicalization vector compared across Python, Rust, and the exact oracle; project numeric rejection handled separately.
5. Python/Rust event behavior, idempotency, rejection, framing, and shutdown parity asserted; queue claim genuinely tested or removed.
6. SQLite multi-row commit atomicity, checkpoint committed-state preservation, disk-full pre/post equality, full restore equivalence, expected exit codes, and VFS injection metadata asserted.
7. All scripts exit nonzero on a failed acceptance property.
8. PR, Notion, and Issue wording and package identity are current.
9. Protected work remains untouched and no dependency, Phase 01 transition, product implementation, security certification, reliability claim, or safety-efficacy claim is created.

## Disposition

- Qualification task: continued for one final hardening cycle.
- PR #5: draft, open, unmerged; not approved.
- Real multi-process IPC evidence: retained as bounded candidate evidence; mechanism not adopted.
- Toolchain/JCS evidence: retained as provisional profile and timing evidence; language not selected.
- SQLite evidence: retained as bounded candidate evidence; storage not adopted.
- Godot artifact and systemd-user evidence: previously accepted; no rerun required.
- Architecture v1.0: remains adopted.
- Roadmap Phase 01 and product implementation: remain closed.
