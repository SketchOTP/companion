#!/usr/bin/env bash
set -euo pipefail

if [ -z "${DISPLAY:-}" ]; then echo "window_probe_blocked display unavailable"; exit 2; fi
QUAL_ROOT="${QUAL_ROOT:-${XDG_CACHE_HOME:-$HOME/.cache}/companion/qualification/COMPANION-P00-QUAL-001}"
GODOT_BIN="${GODOT_BIN:-$QUAL_ROOT/artifacts/godot-4.7.2-standard/Godot_v4.7.2-stable_linux.x86_64}"
"$GODOT_BIN" --path godot --resolution 640x360 --position 80,80 >/tmp/companion-foundation-godot.log 2>&1 &
pid=$!
trap 'kill "$pid" 2>/dev/null || true; wait "$pid" 2>/dev/null || true' EXIT
sleep 2
tree="$(xwininfo -root -tree 2>/dev/null || true)"
if command -v xwininfo >/dev/null && grep -Fq 'Companion Foundation Habitat' <<<"$tree"; then
  echo "window_probe_passed resolution=640x360 position=80,80"
else
  echo "window_probe_failed window-not-observed" >&2; exit 1
fi
