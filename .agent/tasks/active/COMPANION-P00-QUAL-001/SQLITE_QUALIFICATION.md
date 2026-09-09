# Exact SQLite Qualification

## Correction cycle 01 — superseding storage result (2026-09-09)

Status: `CORRECTION SUBMITTED — E3 TARGET-TESTED BOUNDED MATRIX; ARCHITECT REVIEW REQUIRED`

The previous result's “concurrent readers” were serial checks, its migration
test only observed a guard, and its restore check compared row counts. Those
limitations remain historical below. The corrected matrix uses the exact
SQLite 3.53.4 amalgamation/CLI and adds synchronized overlap, actual
pre-mutation migration rejection, full backup equivalence, safe page-limit
failure, and a qualification-only deterministic VFS wrapper.

Current artifact identity remains exact SQLite 3.53.4 with source ID
`2026-07-24 19:02:57 bf7c7f30031888f4e796e429ab3978879485813aaca6f641c7b33e4e09459bcc`;
the published `sqlite3.c` SHA3-256 and local hash match. The build uses
`SQLITE_THREADSAFE=1`, `SQLITE_ENABLE_FTS5`, and dynamic `libdl`, `libpthread`,
and `libm` on local ext4/NVMe. The Python system binding (3.45.1) is not used.

Correction outcomes from the retained private result are:

- True one-writer/two-reader overlap: `overlap_proven=true`; readers during an
  uncommitted writer saw the prior count (5), readers after commit saw the new
  count (6), and a checkpoint ran during the writer.
- Incompatible migration: CLI `-bail` stopped on the guard with
  `incompatible-schema`; schema digest, ordered rows, user version, and
  integrity were unchanged (`rejected_before_mutation=true`).
- Backup/restore: fresh-directory restore matched integrity, schema digest,
  ordered logical rows, row count, and user version; copied-file corruption was
  detected as “file is not a database”.
- Deterministic VFS faults: a narrowly adapted qualification-only wrapper
  against the exact amalgamation injected first-`xSync` return and crash faults
  at commit and checkpoint boundaries. All four cases reopened with
  `PRAGMA integrity_check=ok` and whole-or-absent target state. The runner
  binary hash is retained privately as
  `a69bef9ae86f00a82ee16b0ce97e16a7c30a5942c0d7cfbe9682c4b554e21e4e`.
- Safe simulated disk-full: a fresh 1 KiB-page database with a connection
  `max_page_count=3` returned `database or disk is full` for the oversized
  transaction; after reopen the target row was absent and integrity was `ok`.
  This is a bounded induced failure, not a general lifetime `SQLITE_FULL`
  reliability claim.

The corrected bounded matrix is `E3_TARGET_TESTED` for this exact build,
configuration, local filesystem, synthetic data, and injected fault points.
SQLite remains `BLOCKED — MORE EVIDENCE REQUIRED` for adoption pending
Architect review, broader retained-seed stress, binding-specific qualification,
and any additional fault surface the Architect requires. No database or
dependency was selected or adopted.

Historical status at first submission: `SUPERSEDED — SERIAL/COUNT-ONLY CHECKS AND NO FAULT VFS`

## Historical first submission (superseded; retained for audit)

The original matrix is retained below to document its serial-reader,
guard-only migration, count-only restore, and missing deterministic fault
coverage. It is not the correction result.

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
