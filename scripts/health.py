#!/usr/bin/env python3
"""Read-only operator health view for the foundation."""
import argparse, json, os, pathlib, shutil, subprocess, time
ROLES = ["ops-supervisor", "companion-core", "care-core", "identity-consent-vault", "sensor-gateway", "godot-bridge"]
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--json", action="store_true"); args = ap.parse_args()
    root = pathlib.Path(os.environ.get("COMPANION_XDG_ROOT", pathlib.Path.home() / ".local/share/companion"))
    ps = subprocess.run(["ps", "-eo", "comm="], capture_output=True, text=True, check=False).stdout.splitlines()
    rows = [{"role": role, "running": any(role in line for line in ps), "status": "unknown"} for role in ROLES]
    out = {"version": "companion-foundation/0.1.0", "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "storage_root_class": "private-xdg", "root_exists": root.exists(),
           "sqlite_available": shutil.which(os.environ.get("COMPANION_SQLITE_BIN", "sqlite3")) is not None,
           "processes": rows, "network_default": "deny", "degraded": ["no persistent runtime started"],
           "privacy_class": "PUBLIC_METADATA"}
    print(json.dumps(out, indent=2, sort_keys=True) if args.json else "foundation health: read-only; no persistent runtime started")
if __name__ == "__main__": main()
