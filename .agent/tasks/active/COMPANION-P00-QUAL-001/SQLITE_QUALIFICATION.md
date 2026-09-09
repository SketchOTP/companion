# Exact SQLite Qualification

Status: `PARTIAL — E3 BOUNDED MATRIX WITH EXPLICIT FAULT-INJECTION BLOCKERS`

## Exact artifact

- Current official release recheck selected SQLite `3.53.4`, not a numeric minimum. Official news records `3.52.0` as withdrawn; the 3.53.4 release page reports `SQLITE_SOURCE_ID` `2026-07-24 19:02:57 bf7c7f30031888f4e796e429ab3978879485813aaca6f641c7b33e4e09459bcc` and `sqlite3.c` SHA3-256 `67f423e9ebbbdc473cbc4772c872ee6b89f31fde4ed0279a5c25d5f65c043a16`.
- The official 2026 amalgamation archive was cached privately. Local `sqlite3.c` SHA3-256 matched that published value. Archive SHA-256 and compiled-binary SHA-256 are retained privately as integrity records; no official archive SHA-256/signature was found in the checked release material.
- A private non-production CLI was compiled from the exact amalgamation with `gcc`, `SQLITE_THREADSAFE=1`, `SQLITE_ENABLE_FTS5`, and dynamic `libdl`, `libpthread`, and `libm`. The tested filesystem was local ext4/NVMe. SQLite is public domain; the compiler/runtime components retain their own system-license obligations.
- Python's system sqlite binding (`3.45.1`) was not used for this workstream and is therefore not artifact-identity evidence for 3.53.4.
- Topology: one writer, three serial bounded reader checks, WAL journal mode, `synchronous=FULL`, `wal_autocheckpoint=8` for setup and a bounded manual truncate checkpoint; CLI `.backup` invokes SQLite's Backup API.

Record current official release/withdrawal recheck, exact version, `SQLITE_SOURCE_ID`, official source/amalgamation URL, published and locally calculated digests, binding/build inputs, compile options, dependencies, license/provenance, local filesystem, writer/reader topology, WAL/synchronous/checkpoint configuration, and Backup API mechanism.

## Synthetic matrix

`PASSED` on the exact compiled candidate: WAL file existence while a writer connection remained open; whole commit; rollback absence; idempotent duplicate insert; three readers after writer state; pre-commit SIGKILL leaves no row; post-commit SIGKILL leaves the committed row; bounded checkpoint; URI read-only write rejection; bounded `max_page_count` simulated disk-full rejection; incompatible migration precondition rejection; Backup API snapshot; fresh-directory restore count equivalence; corruption of a copied backup detected as not-a-database; and no SQLite file created in the SSHFS repository checkout.

The initial two matrix attempts exposed harness defects in the WAL-presence, disk-full, and corruption probes. Their private raw results were retained as attempts 1–2; attempt 3 corrected the mechanics and is the final bounded result.

`BLOCKED`: deterministic process kills *during* an SQLite commit and *during* checkpoint were not scheduled safely without an intrusive fault VFS. This directive does not authorize that custom VFS or a system-level fault injector. Consequently the complete acceptance matrix is not satisfied.

Record concurrent readers/one writer, commit/rollback, idempotency, WAL/checkpoint, retained-seed pre/during/post-commit kills, restart/replay, bounded read-only/disk-full fault, incompatible migration, consistent backup, fresh-directory restore, copied-store corruption, and SSHFS absence.

## Results

No partial accepted transaction was observed in the executed bounded tests. This is `E3_TARGET_TESTED` only for the exact 3.53.4 amalgamation/build/settings/local filesystem. It does not establish lifetime reliability, concurrency performance, power-loss behavior, migration correctness beyond the one synthetic guard, or eligibility of any language binding.

Report every pass/fail/block, exact commands, seeds, artifacts, partial observations, and zero-partial-accepted-transaction result.

## Disposition

**BLOCKED — MORE EVIDENCE REQUIRED.** 3.53.4 is the exact current non-withdrawn candidate with corroborated source identity, but it must not be adopted until an authorized deterministic commit/checkpoint fault mechanism, more genuinely concurrent reader/writer workloads, and binding-specific identity tests complete.

Recommend the exact candidate/configuration, reject it, or return blocked evidence. Do not adopt a database or extrapolate beyond the tested artifact/configuration.
