# Persistence Foundation — COMPANION-P01-FOUNDATION-001

Status: `IMPLEMENTED — AWAITING ARCHITECT REVIEW`

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

## Implemented persistence surface

The shared Rust Store resolves one `companion.sqlite3`, `care.sqlite3`, and
`vault.sqlite3` under private XDG data, applies WAL plus `synchronous=FULL`,
creates authority-specific append/audit tables, supports idempotent inserts,
integrity checks and SQLite Backup API command execution. `scripts/storage_smoke.py`
records three distinct stores, duplicate idempotency, integrity `ok`, and
fresh-directory backup/restore equivalence using synthetic data. Long-duration
crash, disk-full, migration, and power-loss qualification remain conditional;
no release suitability is claimed.

## Review 01 continuation

`foundation_core::persistence::Store` now binds the SQLite C ABI directly and
uses prepared statements with bound values for event and receipt writes. It
executes committed migration text transactionally, records a migration SHA-256,
enables WAL/FULL synchronous mode, performs integrity/checkpoint operations,
and uses the SQLite Online Backup API for fresh-file snapshots. When the
private `COMPANION_SQLITE_SOURCE` input is present, `build.rs` compiles and
statically links the cached 3.53.4 amalgamation; the resulting binary reports
3.53.4 and carries no SQLite dynamic dependency. Hosts without that private
input use a visible development fallback and do not receive an exact-version
claim. Full crash, power-loss, migration and long-duration qualification
remain unqualified.

## Architect Review 02 continuation

`build.rs`, `bootstrap.sh`, and `verify.sh` now require the exact private
SQLite 3.53.4 amalgamation and verify its SHA-256 before compiling; the host
library is available only through an explicit nonauthoritative developer
fallback. Runtime health reports `sqlite3_libversion`, `sqlite3_sourceid`, and
`sqlite3_compileoption_get` values. `scripts/sqlite_identity_check.py` asserts
the accepted version/source identity and source digest against a live resident
supervisor. The bounded store smoke remains synthetic and does not claim
lifetime, power-loss, or release reliability.
