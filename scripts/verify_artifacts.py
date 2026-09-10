#!/usr/bin/env python3
"""Verify exact private-cache artifacts without modifying the host."""
import hashlib, os, pathlib, subprocess, sys
root=pathlib.Path(os.environ.get("QUAL_ROOT", pathlib.Path.home()/".cache/companion/qualification/COMPANION-P00-QUAL-001"))
godot=pathlib.Path(os.environ.get("GODOT_BIN", root/"artifacts/godot-4.7.2-standard.L8kXdw/Godot_v4.7.2-stable_linux.x86_64"))
godot_archive=root/"artifacts/Godot_v4.7.2-stable_linux.x86_64.zip"
sqlite=pathlib.Path(os.environ.get("COMPANION_SQLITE_BIN", root/"artifacts/sqlite3-3.53.4"))
expected="cadd3204e728a35d3f13adb7fd0d7902636b79f6b95c40c265eb73b6c35329e4"
errors=[]
if not godot.is_file() or not godot_archive.is_file() or hashlib.sha256(godot_archive.read_bytes()).hexdigest()!=expected: errors.append("Godot artifact archive missing or SHA-256 mismatch")
if not sqlite.is_file(): errors.append("SQLite artifact missing")
else:
    version=subprocess.run([str(sqlite),"--version"],capture_output=True,text=True,check=False).stdout
    if "3.53.4" not in version: errors.append("SQLite version mismatch")
if errors:
    for error in errors: print("ERROR",error,file=sys.stderr)
    raise SystemExit(1)
print("artifact_verification_ok godot=4.7.2 sqlite=3.53.4")
