# Phase 01 closeout evidence

This directory contains sanitized, committed summaries for the final Phase 01
foundation gate. It is evidence only; it is not runtime state and does not
claim product, safety, security, reliability, or SLA capability.

Regeneration is performed on a clean local ext4/NVMe checkout with the exact
locked Rust workspace and the private XDG qualification cache. Run, in order:

1. `cargo fmt --all -- --check`, `cargo clippy --workspace --locked`, and
   `cargo test --workspace --locked`.
2. `cargo build --workspace --locked --release`.
3. `python3 scripts/contract_closeout.py`.
4. `python3 scripts/phase01_closeout.py --cycles 3000 --seeds 17,23,41 --output <private>/phase01_closeout.json`.
5. `python3 scripts/failure_matrix.py --output <private>/failure_matrix.json`.
6. Run `scripts/soak.py --duration-seconds 3600` with output directed to a
   private XDG path; do not commit raw logs, databases, WAL files, binaries,
   host identifiers, or media.
7. Copy only sanitized JSON summaries into this directory, update
   `manifest.json` hashes and the final evidence commit, then run
   `python3 scripts/validate_phase01_closeout.py`.

The validator recomputes every result and fixture SHA-256, checks Git ancestry,
asserts the expected matrix relations, and writes `validation.json`; it does
not consume `validation.json` as evidence. A tamper-negative copy must fail
with a nonzero exit after changing any result byte.
