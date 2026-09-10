# Persistence Foundation — COMPANION-P01-FOUNDATION-001

Status: `PENDING CODEX EXECUTION`

Document the exact SQLite 3.53.4 integration and the separate companion, care and vault development stores.

Required details:

- source/binding/build identity and compile options;
- local ext4/NVMe path class;
- one writer per authority store;
- WAL, synchronous and checkpoint policy;
- store identity and schema version;
- append-only event/audit tables;
- transaction and idempotency rules;
- versioned migrations and incompatible-version behavior;
- integrity checks;
- Backup API snapshot and fresh-directory restore;
- synthetic data only.

Required proof:

- no shared writable database;
- no SQLite/WAL/lock file beneath the checkout or on SSHFS;
- migration, integrity, crash/restart, bounded disk-full, backup and restore tests;
- store corruption causes visible failure/degradation;
- `care-core` does not require the companion store;
- release-unqualified surfaces remain explicit.
