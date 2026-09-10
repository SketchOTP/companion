#!/usr/bin/env bash
set -euo pipefail

QUAL_ROOT="${QUAL_ROOT:-${XDG_CACHE_HOME:-$HOME/.cache}/companion/qualification/COMPANION-P00-QUAL-001}"
export PATH="$QUAL_ROOT/cargo/bin:$PATH"
export RUSTUP_HOME="${RUSTUP_HOME:-$QUAL_ROOT/rustup}"
export CARGO_HOME="${CARGO_HOME:-$QUAL_ROOT/cargo}"
export COMPANION_SQLITE_BIN="${COMPANION_SQLITE_BIN:-$QUAL_ROOT/artifacts/sqlite3-3.53.4}"
if test -f "$QUAL_ROOT/artifacts/sqlite-amalgamation-3530400/sqlite3.c"; then
  export COMPANION_SQLITE_SOURCE="$QUAL_ROOT/artifacts/sqlite-amalgamation-3530400/sqlite3.c"
fi
export COMPANION_XDG_ROOT="${COMPANION_XDG_ROOT:-$(mktemp -d "${TMPDIR:-/tmp}/companion-foundation.XXXXXX")}"

command -v cargo >/dev/null || { echo "cargo 1.98.1 is required in QUAL_ROOT" >&2; exit 2; }
test "$(rustc --version | awk '{print $2}')" = "1.98.1"
if test ! -x "$COMPANION_SQLITE_BIN" || test ! -f "${COMPANION_SQLITE_SOURCE:-}"; then
  test "${QUAL_ALLOW_FETCH:-0}" = "1" || { echo "exact SQLite 3.53.4 artifact missing from private cache (set QUAL_ALLOW_FETCH=1 for official fetch)" >&2; exit 2; }
  command -v curl >/dev/null || { echo "curl is required for official artifact fetch" >&2; exit 2; }
  command -v unzip >/dev/null || { echo "unzip is required for official artifact fetch" >&2; exit 2; }
  mkdir -p "$QUAL_ROOT/artifacts"
  curl --fail --location --output "$QUAL_ROOT/artifacts/sqlite-amalgamation-3530400.zip" https://www.sqlite.org/2026/sqlite-amalgamation-3530400.zip
  unzip -q -o "$QUAL_ROOT/artifacts/sqlite-amalgamation-3530400.zip" -d "$QUAL_ROOT/artifacts"
  test -f "$QUAL_ROOT/artifacts/sqlite-amalgamation-3530400/sqlite3.c" && export COMPANION_SQLITE_SOURCE="$QUAL_ROOT/artifacts/sqlite-amalgamation-3530400/sqlite3.c"
  test -x "$COMPANION_SQLITE_BIN" || { echo "SQLite CLI fetch/build is not implicit; provide exact private binary" >&2; exit 2; }
fi
test -x "$COMPANION_SQLITE_BIN" || { echo "exact SQLite 3.53.4 artifact missing from private cache" >&2; exit 2; }
test -f "${COMPANION_SQLITE_SOURCE:-}" || { echo "exact SQLite 3.53.4 amalgamation missing from private cache" >&2; exit 2; }
test "$(sha256sum "$COMPANION_SQLITE_SOURCE" | awk '{print $1}')" = "b1dd5d74ec7f29055a6684fa06fb3c2f6821c87dd38f9a458dfd2e8a1db28189" || { echo "SQLite 3.53.4 source digest mismatch" >&2; exit 2; }
python3 scripts/verify_artifacts.py
cargo build --workspace --locked --release
cargo test --workspace --locked
python3 scripts/sqlite_identity_check.py --output "$COMPANION_XDG_ROOT/sqlite-identity-results.json"
python3 scripts/validate_schemas.py
python3 scripts/foundation_runtime_check.py --output "$COMPANION_XDG_ROOT/runtime-results.json"
python3 scripts/storage_smoke.py --output "$COMPANION_XDG_ROOT/storage-results.json"
python3 scripts/direct_care_smoke.py --output "$COMPANION_XDG_ROOT/care-results.json"
GODOT_ARCHIVE="$QUAL_ROOT/artifacts/Godot_v4.7.2-stable_linux.x86_64.zip"
GODOT_DIR="$QUAL_ROOT/artifacts/godot-4.7.2-standard"
GODOT_BIN="${GODOT_BIN:-$GODOT_DIR/Godot_v4.7.2-stable_linux.x86_64}"
if test ! -x "$GODOT_BIN"; then
  command -v unzip >/dev/null || { echo "unzip is required for deterministic Godot extraction" >&2; exit 2; }
  if test ! -f "$GODOT_ARCHIVE"; then
    test "${QUAL_ALLOW_FETCH:-0}" = "1" || { echo "official Godot archive missing from private cache (set QUAL_ALLOW_FETCH=1 for official fetch)" >&2; exit 2; }
    command -v curl >/dev/null || { echo "curl is required for official artifact fetch" >&2; exit 2; }
    mkdir -p "$QUAL_ROOT/artifacts"
    curl --fail --location --output "$GODOT_ARCHIVE" https://github.com/godotengine/godot-builds/releases/download/4.7.2-stable/Godot_v4.7.2-stable_linux.x86_64.zip
  fi
  test "$(sha256sum "$GODOT_ARCHIVE" | awk '{print $1}')" = "cadd3204e728a35d3f13adb7fd0d7902636b79f6b95c40c265eb73b6c35329e4" || { echo "Godot archive digest mismatch" >&2; exit 2; }
  mkdir -p "$GODOT_DIR"
  unzip -q -o "$GODOT_ARCHIVE" -d "$GODOT_DIR"
  chmod 700 "$GODOT_BIN"
fi
test -x "$GODOT_BIN" || { echo "official Godot 4.7.2 executable missing from deterministic cache" >&2; exit 2; }
"$GODOT_BIN" --headless --path godot --editor --quit
printf 'bootstrap_ok rust=%s sqlite_artifact=%s godot=%s\n' "$(rustc --version)" "$(basename "$COMPANION_SQLITE_BIN")" "$(basename "$GODOT_BIN")"
