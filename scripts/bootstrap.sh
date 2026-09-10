#!/usr/bin/env bash
set -euo pipefail

QUAL_ROOT="${QUAL_ROOT:-${XDG_CACHE_HOME:-$HOME/.cache}/companion/qualification/COMPANION-P00-QUAL-001}"
export PATH="$QUAL_ROOT/cargo/bin:$PATH"
export RUSTUP_HOME="${RUSTUP_HOME:-$QUAL_ROOT/rustup}"
export CARGO_HOME="${CARGO_HOME:-$QUAL_ROOT/cargo}"
export COMPANION_SQLITE_BIN="${COMPANION_SQLITE_BIN:-$QUAL_ROOT/artifacts/sqlite3-3.53.4}"
export COMPANION_XDG_ROOT="${COMPANION_XDG_ROOT:-$(mktemp -d "${TMPDIR:-/tmp}/companion-foundation.XXXXXX")}"

command -v cargo >/dev/null || { echo "cargo 1.98.1 is required in QUAL_ROOT" >&2; exit 2; }
test "$(rustc --version | awk '{print $2}')" = "1.98.1"
test -x "$COMPANION_SQLITE_BIN"
python3 scripts/verify_artifacts.py
cargo build --workspace --locked --release
cargo test --workspace --locked
python3 scripts/validate_schemas.py
python3 scripts/storage_smoke.py --output "$COMPANION_XDG_ROOT/storage-results.json"
python3 scripts/direct_care_smoke.py --output "$COMPANION_XDG_ROOT/care-results.json"
"${GODOT_BIN:-$QUAL_ROOT/artifacts/godot-4.7.2-standard.L8kXdw/Godot_v4.7.2-stable_linux.x86_64}" --headless --path godot --editor --quit
printf 'bootstrap_ok rust=%s sqlite=%s xdg=%s\n' "$(rustc --version)" "$($COMPANION_SQLITE_BIN --version | head -1)" "$COMPANION_XDG_ROOT"
