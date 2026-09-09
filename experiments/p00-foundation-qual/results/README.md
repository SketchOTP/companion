# Committed qualification result bundle

These files are sanitized, machine-readable summaries of the bounded
`COMPANION-P00-QUAL-001` qualification runs. They are committed so a fresh
checkout can validate the verdict without access to private caches.

This is disposable qualification infrastructure, not the Companion runtime.
Its dependencies and measurements are not production-approved. Passing these
checks does not establish product, security, reliability, safety, or SLA
capability. Private binaries, toolchains, databases, WAL files, raw host
identifiers, secrets, credentials, media, and raw measurements remain outside
Git.

## Reproducible regeneration

This bundle is regenerated only from the qualification checkout and private
local XDG cache. Required inputs are the existing CPython 3.12 executable, the
isolated Rust 1.98.1 release toolchain, Node `v24.20.0`, the cached
`canonicalize@5.0.0` tarball, and the exact SQLite 3.53.4 binary and
amalgamation. Set `QUAL_RUST_BINARY`, `QUAL_JCS_PACKAGE`, `QUAL_JCS_ORACLE`,
`QUAL_SQLITE`, `QUAL_SQLITE_SOURCE_DIR`, and `QUAL_RESULTS` to private cache
paths; do not use repository-controlled dependencies or caches.

Run in this order:

1. Build and test the Rust shell with `cargo test` and `cargo build --release`.
2. Run `jcs_conformance.py` with the isolated Node oracle and release Rust
   binary, retaining stdout outside Git.
3. Run `run_toolchain_measure.py`, retaining raw timing/resource output outside
   Git.
4. Run `ipc_trust_qualification.py --run`, retaining only sanitized JSON.
5. Run `sqlite_matrix.py` with the exact binary and amalgamation; keep its
   temporary databases, WAL files, fault runner, and raw measurements in the
   private XDG qualification root.
6. Generate the committed summaries deterministically from sanitized runner
   outputs (sorted-key canonical JSON and fixed indentation); never hand-edit
   conclusion fields.
7. Recalculate fixture and summary SHA-256 values, set the final evidence commit
   and hashes in `provenance.json`, and run
   `python3 experiments/p00-foundation-qual/scripts/validate_results.py`.

The validator independently recomputes every manifest-listed result hash and
the fixture hash, checks evidence-commit ancestry, and writes
`validation_results.json` as output. For a tamper-negative check, copy this
directory to a temporary private directory, alter one result byte, and run
`QUAL_RESULTS_ROOT=<temporary-copy> python3 .../validate_results.py`; it must
exit nonzero. Only sanitized result JSON, provenance, this README, and source
scripts belong in Git. Caches, binaries, toolchains, databases, WAL/SHM/lock
files, raw logs, and temporary worktrees remain outside Git.
