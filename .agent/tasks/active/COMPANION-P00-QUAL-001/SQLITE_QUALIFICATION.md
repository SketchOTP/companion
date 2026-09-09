# Exact SQLite Qualification

Status: `PENDING CODEX EXECUTION`

## Exact artifact

Record current official release/withdrawal recheck, exact version, `SQLITE_SOURCE_ID`, official source/amalgamation URL, published and locally calculated digests, binding/build inputs, compile options, dependencies, license/provenance, local filesystem, writer/reader topology, WAL/synchronous/checkpoint configuration, and Backup API mechanism.

## Synthetic matrix

Record concurrent readers/one writer, commit/rollback, idempotency, WAL/checkpoint, retained-seed pre/during/post-commit kills, restart/replay, bounded read-only/disk-full fault, incompatible migration, consistent backup, fresh-directory restore, copied-store corruption, and SSHFS absence.

## Results

Report every pass/fail/block, exact commands, seeds, artifacts, partial observations, and zero-partial-accepted-transaction result.

## Disposition

Recommend the exact candidate/configuration, reject it, or return blocked evidence. Do not adopt a database or extrapolate beyond the tested artifact/configuration.
