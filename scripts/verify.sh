#!/usr/bin/env bash
set -euo pipefail

QUAL_ROOT="${QUAL_ROOT:-${XDG_CACHE_HOME:-$HOME/.cache}/companion/qualification/COMPANION-P00-QUAL-001}"
export PATH="$QUAL_ROOT/cargo/bin:$PATH" RUSTUP_HOME="${RUSTUP_HOME:-$QUAL_ROOT/rustup}" CARGO_HOME="${CARGO_HOME:-$QUAL_ROOT/cargo}"
export COMPANION_SQLITE_BIN="${COMPANION_SQLITE_BIN:-$QUAL_ROOT/artifacts/sqlite3-3.53.4}"
if test -f "$QUAL_ROOT/artifacts/sqlite-amalgamation-3530400/sqlite3.c"; then
  export COMPANION_SQLITE_SOURCE="$QUAL_ROOT/artifacts/sqlite-amalgamation-3530400/sqlite3.c"
fi
export COMPANION_XDG_ROOT="${COMPANION_XDG_ROOT:-$(mktemp -d "${TMPDIR:-/tmp}/companion-verify.XXXXXX")}"

python3 scripts/verify_artifacts.py
cargo fmt --all -- --check
cargo clippy --workspace --all-targets --all-features --locked -- -D warnings
cargo test --workspace --locked
cargo build --workspace --locked --release
python3 scripts/validate_schemas.py
python3 scripts/check_contract_types.py
python3 scripts/cycle_matrix.py --cycles 1000 --seeds 17,23,41 --output "$COMPANION_XDG_ROOT/cycle-results.json"
python3 scripts/storage_smoke.py --output "$COMPANION_XDG_ROOT/storage-results.json"
python3 scripts/direct_care_smoke.py --output "$COMPANION_XDG_ROOT/care-results.json"
python3 scripts/failure_matrix.py --output "$COMPANION_XDG_ROOT/failure-results.json"
python3 scripts/generate_sbom.py --output "$COMPANION_XDG_ROOT/sbom.spdx.json"
FOUNDATION_SUPERVISOR=target/release/ops-supervisor COMPANION_XDG_ROOT="$COMPANION_XDG_ROOT" target/release/ops-supervisor >"$COMPANION_XDG_ROOT/supervisor.log" 2>&1 &
SUPERVISOR_PID=$!
trap 'kill "$SUPERVISOR_PID" 2>/dev/null || true; wait "$SUPERVISOR_PID" 2>/dev/null || true' EXIT
for _ in $(seq 1 100); do
  test -S "$COMPANION_XDG_ROOT/companion/supervisor.sock" && break
  sleep 0.05
done
python3 scripts/health.py --json
kill -TERM "$SUPERVISOR_PID"
wait "$SUPERVISOR_PID"
trap - EXIT
python3 scripts/foundation_runtime_check.py --output "$COMPANION_XDG_ROOT/runtime-results.json"
git diff --check
printf 'verification_ok\n'
