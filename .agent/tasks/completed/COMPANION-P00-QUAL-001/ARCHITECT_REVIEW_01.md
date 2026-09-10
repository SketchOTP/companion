# Architect Review 01 — COMPANION-P00-QUAL-001

Status: `CONTINUE — FOCUSED CORRECTIONS REQUIRED`

- Reviewed base: `fb4d4750182bae765e8366265d6cfb1ee36e105d`
- Reviewed PR head: `e415e37b23ba24593cd9c05bbe073322dffa5b46`
- Pull request: `#5` — open, unmerged, changes required
- Issue: `#4` — open
- Architecture v1.0: adopted and unchanged
- Roadmap Phase 01: closed
- Product implementation: closed
- Canonical Notion review: https://app.notion.com/p/3d6833cb27ff815baf6bf4d635073d65

## Retained evidence

Do not repeat these areas unless the source, artifact, host, or branch state changes:

- Protected primary-worktree handling and clean ext4/NVMe secondary worktree.
- Complete authority reconstruction and governance-only/product-free scope.
- Weak mode-0600 pathname/UID/message-field baseline: a separate same-user process successfully injected a valid-looking message, proving that baseline insufficient.
- Exact Godot 4.7.2 Linux x86_64 artifact identity, published/local digest match, and version-only execution as `E1_OBSERVED` source-correlated evidence.
- Bounded transient systemd-user lifecycle/restart/status feasibility as `E3_TARGET_TESTED`; no production supervisor selection.
- Exact SQLite 3.53.4 source identity and executed basic transaction/WAL/backup/restore/fault observations as partial evidence only.
- Python/Rust timing measurements for the one ASCII/integer fixture as a provisional microbenchmark only.

## Defect 1 — IPC Candidate 1/2 evidence is invalid

`experiments/p00-foundation-qual/scripts/ipc_trust_qualification.py` creates a socketpair, but `exchange(sock, ...)` ignores `sock` and directly calls `care_decide(...)`. Candidate 1 and Candidate 2 therefore do not transmit a message between processes or even between socket endpoints. The producer, care logic, HMAC generation/verification, and `PR_SET_DUMPABLE` call all run in one parent process.

The `/proc/<pid>/fd/<n>` `os.open()` probe is not a substitute for `pidfd_getfd()`. `ENXIO` when opening a socket symlink does not prove descriptor duplication is blocked.

Consequences:

- Candidate 1/2 `E3_TARGET_TESTED` security evidence is rejected.
- Candidate 2 is not adopted or qualified.
- The weak-baseline result remains valid.

### Required real multi-process test

Use distinct supervisor, producer, care, and unauthorized same-user sibling processes.

- Supervisor creates a private `SOCK_SEQPACKET` channel and generation.
- Producer receives only its endpoint and least-exposure generation capability.
- Care receives only its endpoint, expected producer process handle/generation, and verification material.
- Messages must actually traverse the socket.
- Care must receive kernel-supplied sender credentials with `SO_PASSCRED`/`SCM_CREDENTIALS`, or provide a tested equivalent. Never trust message-declared identity.
- Bind the expected producer to a pidfd or another race-resistant process-generation mechanism; do not rely only on a numeric PID.
- Apply non-dumpability/confinement in the actual producer and care child processes.
- Prove unrelated descriptors are closed and close-on-exec is effective.
- Provision capability material through a private inherited channel, sealed memory object, or equally narrow mechanism—not argv, environment, logs, or repository files.
- Test `pidfd_getfd()` directly from the unauthorized sibling where supported and record the exact result. `/proc` checks are supplementary only.
- Exercise producer restart, care restart, old-channel revocation, old-capability rejection, PID/generation mismatch, replay, duplicates, malformed input, companion outage, and companion-database absence.
- Preserve the threat ceiling: no claim against root, kernel compromise, full account compromise, or a fully compromised authorized producer.

## Defect 2 — toolchain harness does not qualify RFC 8785/JCS

The Python shell uses `json.dumps(..., sort_keys=True)`. The Rust shell uses `serde_json::to_vec`. Neither call alone implements RFC 8785. RFC 8785 requires ECMAScript-compatible primitive serialization and recursive ordering of raw property names by UTF-16 code units.

The Rust duplicate-key scanner compares raw escaped spelling rather than decoded names, so equivalent property names such as `"a"` and `"\u0061"` are not proven to collide. The submitted fixture contains only ASCII property names and integers. The Rust shell also does not exercise an equivalent bounded queue, and the comparison lacks sustained RSS/CPU evidence.

Consequences:

- The common digest is accepted only for the one frozen ASCII/integer fixture.
- The JCS parity claim is rejected.
- Rust remains a candidate; no toolchain selection is made.

### Required corrected comparison

- Use maintained RFC 8785 implementation candidates in both languages or one independently verified reference oracle. Record exact versions, hashes, licenses, maintenance, and qualification-only status.
- Run official/reference vectors for UTF-16 property sorting, non-BMP names, control-character escaping, Unicode preservation, invalid Unicode, canonical numbers, and duplicate names after escape decoding.
- Add `{"a":1,"\u0061":2}` as a mandatory duplicate-name rejection case.
- If the Companion profile prohibits fractional JSON numbers, test and document that stricter schema boundary separately from JCS itself.
- Make both service shells equivalent in framing, multi-message idempotency, queue capacity/overflow, rejection reasons, startup/shutdown, and controlled exits.
- Measure a Rust release build, not debug only.
- Separate cold-start and warm request runs. Add a bounded sustained synthetic run with CPU and RSS for both candidates and retain raw distributions.
- Reissue a recommendation only after semantic parity succeeds. Do not self-adopt Rust or Python.

## Defect 3 — SQLite evidence is correctly partial but the harness overlabels several checks

- `concurrent_readers` runs serial queries; it is not concurrent reader/writer coverage.
- `incompatible_migration_fail_closed` only tests `user_version != 2`; it does not execute and reject an incompatible migration.
- Disk-full handling records an error but does not prove logical atomicity after failure.
- Backup/restore equivalence compares only row counts.
- During-commit and during-checkpoint failure points remain untested.

### Authorized SQLite correction

A qualification-only VFS/fault harness based on current official SQLite public test methods is authorized within the existing disposable scope and private local ext4/NVMe root. No system modification or user/repository data is permitted.

Required evidence:

- True overlapping one-writer/multiple-reader execution with barriers and retained seeds.
- Actual incompatible migration attempt rejected before mutation.
- Explicit post-failure atomicity assertion for `SQLITE_FULL`/injected I/O failure.
- Backup/restore integrity, schema/version, complete ordered logical-content digest, and fresh-directory equivalence.
- Deterministic VFS failure or crash points during commit and checkpoint, with each logical transaction wholly present or absent and `integrity_check` passing after recovery.
- Current release/withdrawal recheck before execution and exact artifact identity preservation.

If this cannot be completed inside the authorized boundary, report `BLOCKED` with exact evidence. Do not upgrade SQLite eligibility.

## Durable evidence correction

Update all affected task documents, the Notion report/directive, PR description, and Issue #4 so they state:

- Weak-baseline IPC evidence is retained.
- Candidate 1/2 are unqualified until real multi-process testing passes.
- The current toolchain result proves one ASCII/integer fixture only, not JCS.
- Rust is not selected.
- SQLite serial reads, migration guard, and count-only restore are named accurately.
- Godot and transient systemd results are retained and need not be rerun unless facts change.
- No dependency, IPC mechanism, database, supervisor, Roadmap Phase 01 transition, or product capability is adopted.

## Acceptance criteria

1. IPC candidates use real separate processes and actual socket transmission.
2. Care verifies kernel/process-bound producer identity and generation.
3. Unauthorized same-user sibling input is prevented under the stated threat model.
4. Producer/care restart and stale channel/capability revocation are tested.
5. JCS claims pass official/reference vectors or are removed.
6. Escaped duplicate names and UTF-16 sorting are correct.
7. Python/Rust shells have equivalent framing, queues, idempotency, and rejection behavior.
8. Release-build and bounded CPU/RSS evidence is added without product claims.
9. SQLite concurrency, migration, disk atomicity, restore equivalence, and deterministic VFS faults are tested or explicitly blocked.
10. Evidence labels match actual execution.
11. PR #5 and Issue #4 remain open and unmerged.
12. Protected primary-worktree changes remain untouched.

## Publication discipline

Continue on `codex/p00-qual-001` and update PR #5. Do not create another PR, push to `main`, merge, rewrite prior evidence, or delete failed attempts. Add one focused correction commit and at most one publication-reconciliation commit. Update Notion and Issue #4, then stop for independent Architect re-review.
