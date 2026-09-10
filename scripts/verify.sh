#!/usr/bin/env bash
set -euo pipefail

QUAL_ROOT="${QUAL_ROOT:-${XDG_CACHE_HOME:-$HOME/.cache}/companion/qualification/COMPANION-P00-QUAL-001}"
export PATH="$QUAL_ROOT/cargo/bin:$PATH" RUSTUP_HOME="${RUSTUP_HOME:-$QUAL_ROOT/rustup}" CARGO_HOME="${CARGO_HOME:-$QUAL_ROOT/cargo}"
export COMPANION_SQLITE_BIN="${COMPANION_SQLITE_BIN:-$QUAL_ROOT/artifacts/sqlite3-3.53.4}"
if test -f "$QUAL_ROOT/artifacts/sqlite-amalgamation-3530400/sqlite3.c"; then
  export COMPANION_SQLITE_SOURCE="$QUAL_ROOT/artifacts/sqlite-amalgamation-3530400/sqlite3.c"
fi
test -f "${COMPANION_SQLITE_SOURCE:-}" || { echo "exact SQLite 3.53.4 source is mandatory for acceptance verification" >&2; exit 2; }
test "$(sha256sum "$COMPANION_SQLITE_SOURCE" | awk '{print $1}')" = "b1dd5d74ec7f29055a6684fa06fb3c2f6821c87dd38f9a458dfd2e8a1db28189" || { echo "SQLite 3.53.4 source digest mismatch" >&2; exit 2; }
export COMPANION_XDG_ROOT="${COMPANION_XDG_ROOT:-$(mktemp -d "${TMPDIR:-/tmp}/companion-verify.XXXXXX")}"

python3 scripts/verify_artifacts.py
cargo fmt --all -- --check
cargo clippy --workspace --all-targets --all-features --locked -- -D warnings
cargo test --workspace --locked
cargo build --workspace --locked --release
python3 scripts/validate_schemas.py
python3 scripts/contract_closeout.py
python3 scripts/check_contract_types.py
python3 scripts/cycle_matrix.py --cycles 1000 --seeds 17,23,41 --output "$COMPANION_XDG_ROOT/cycle-results.json"
python3 scripts/storage_smoke.py --output "$COMPANION_XDG_ROOT/storage-results.json"
python3 scripts/sqlite_identity_check.py --output "$COMPANION_XDG_ROOT/sqlite-identity-results.json"
python3 scripts/direct_care_smoke.py --output "$COMPANION_XDG_ROOT/care-results.json"
python3 scripts/failure_matrix.py --output "$COMPANION_XDG_ROOT/failure-results.json"
python3 scripts/phase01_closeout.py --cycles 3000 --seeds 17,23,41 --output "$COMPANION_XDG_ROOT/phase01-closeout-results.json"
if test -f evidence/phase01-closeout/manifest.json; then
  python3 scripts/validate_phase01_closeout.py
fi
if test -n "${GODOT_BIN:-}"; then
  python3 scripts/godot_bridge_smoke.py --output "$COMPANION_XDG_ROOT/godot-bridge-results.json"
fi
SOURCE_DATE_EPOCH="${SOURCE_DATE_EPOCH:-0}" python3 scripts/generate_sbom.py --output "$COMPANION_XDG_ROOT/sbom.spdx.json"
python3 scripts/validate_sbom.py --input "$COMPANION_XDG_ROOT/sbom.spdx.json"
python3 scripts/security_checks.py
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
