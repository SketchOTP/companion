# Phase 01 Review 04 evidence bundle

This directory contains sanitized, committed outputs for the narrow
Architect-Review-04 evidence-semantics correction. It is qualification evidence
for the Phase 01 foundation only; it is not the Companion runtime and does not
establish product, safety, security, reliability, or SLA capability.

## Regeneration

Run from a clean local-ext4/NVMe task worktree with the already pinned release
build and private cached Godot artifact. Keep all generated binaries, temporary
XDG roots, SQLite databases/WAL files, raw logs, and host-specific paths outside
Git.

1. Build and test: `cargo test --workspace --locked` and
   `cargo build --workspace --locked --release` using the pinned local toolchain.
2. Run `scripts/phase01_closeout.py --cycles 3000 --seeds 17,23,41` and write its
   JSON output to a private temporary file.
3. Run `scripts/failure_matrix.py` with `FOUNDATION_SUPERVISOR` and the private
   Godot artifact environment variables; retain only its sanitized JSON output.
4. Run `scripts/godot_bridge_smoke.py` with the verified artifact and write its
   output here after checking it contains no private identifiers.
5. Run `scripts/contract_closeout.py --wire-evidence <phase01-json>` to generate
   the contract summary from the actual ordinary/direct-care wire result.
6. Run `scripts/regression900.py --duration-seconds 900` and retain only its
   sanitized JSON output.
7. Copy those five sanitized outputs into this directory, compute their
   SHA-256 values and the fixture hash, and write `manifest.json` with the
   observed date-only UTC execution field and exact source identities.
8. Run `python3 experiments/p00-foundation-qual/scripts/validate_phase01_review04.py`.
   The validator recomputes every listed hash, checks Git ancestry and all
   semantic equations, and writes `validation_results.json` as output only.
9. Run `python3 experiments/p00-foundation-qual/scripts/tamper_negative_review04.py`
   to copy this bundle privately and verify that five independent mutations
   (hash, expected outcome, reason, invalid acceptance, acceptance-group
   observation) all fail validation with nonzero status.

Only this README, `manifest.json`, the five sanitized result JSON files, and the
validator output belong in Git. No private cache, binary, database, WAL/SHM/
lock file, raw measurement, media, credential, secret, PID, hostname, username,
or absolute local path may be committed.
