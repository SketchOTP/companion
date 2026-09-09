#!/usr/bin/env python3
"""Fail-closed validation of the committed sanitized qualification bundle."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FILES = ("jcs_toolchain_results.json", "ipc_results.json", "sqlite_results.json", "validation_results.json")
FORBIDDEN = re.compile(r"/(?:home|srv|tmp|run)/|(?:username|hostname|serial|secret|capability_bytes|pid)\\s*[:=]", re.I)


def load(name: str):
    value = json.loads((RESULTS / name).read_text(encoding="utf-8"))
    text = json.dumps(value, sort_keys=True)
    if FORBIDDEN.search(text):
        raise AssertionError(f"forbidden private field in {name}")
    return value


def main() -> int:
    try:
        jcs = load("jcs_toolchain_results.json")
        ipc = load("ipc_results.json")
        sqlite = load("sqlite_results.json")
        validation = load("validation_results.json")
        provenance = json.loads((RESULTS / "provenance.json").read_text(encoding="utf-8"))
        if not provenance.get("git_commit") or not provenance.get("commands") or not provenance.get("evidence_ceiling"):
            raise AssertionError("incomplete provenance")
        if jcs["oracle"]["package"] != "canonicalize@5.0.0": raise AssertionError("oracle identity")
        if jcs["status"] != "PASSED" or jcs["recommendation"] == "RUST": raise AssertionError("JCS/toolchain status")
        if not all(value is True for value in jcs["conformance"].values()): raise AssertionError("JCS conformance")
        for key, value in jcs["behavioral_parity"].items():
            if key == "queue_overflow":
                if value != "DEFERRED_PHASE_01": raise AssertionError("queue claim")
            elif value is not True: raise AssertionError(f"behavioral parity: {key}")
        if not jcs["rust"]["release_build"] or jcs["rust"]["tests_passed"] < 1: raise AssertionError("Rust tests/build")
        if not ipc["process_boundary"]["four_independent_roles_started"]: raise AssertionError("IPC roles")
        if not all(value is True for key, value in ipc["process_boundary"].items() if key not in {"care_supervisor_copy_read"}): raise AssertionError("IPC boundary")
        if ipc["process_boundary"]["care_supervisor_copy_read"] is not False: raise AssertionError("care copy read")
        if not all(value is True for key, value in ipc["security_tests"].items() if key not in {"weak_same_user_pathname_injection", "same_user_sibling_direct_injection", "pidfd_getfd", "proc_fd_duplication"}): raise AssertionError("IPC attack matrix")
        if ipc["security_tests"]["pidfd_getfd"] != {"syscall": "pidfd_getfd", "status": "error", "errno": 1, "name": "EPERM"}: raise AssertionError("pidfd_getfd exact result")
        if sqlite["status"] != "PASSED_BOUNDED_MATRIX" or not sqlite["artifact"]["local_matches_published"]: raise AssertionError("SQLite artifact")
        if not all(value is True for value in sqlite["concurrency"].values() if isinstance(value, bool)): raise AssertionError("SQLite concurrency")
        if not all(value is True for value in sqlite["migration"].values() if isinstance(value, bool)): raise AssertionError("SQLite migration")
        if not all(value is True for value in sqlite["disk_full"].values() if isinstance(value, bool)): raise AssertionError("SQLite disk-full")
        if not all(value is True for value in sqlite["backup_restore"].values()): raise AssertionError("SQLite backup")
        faults = sqlite["fault_vfs"]
        if not faults["all_integrity_ok"] or not faults["all_atomicity_assertions"]: raise AssertionError("SQLite VFS aggregate")
        for name in ("commit_return", "commit_crash", "checkpoint_return", "checkpoint_crash"):
            outcome = faults[name]
            expected = 69 if name.endswith("return") else 70
            if outcome["returncode"] != expected or outcome["integrity"] != "ok" or not outcome["whole_or_absent"] or not outcome["sync_file_class"] or outcome["sync_ordinal"] != 1:
                raise AssertionError(f"SQLite fault {name}")
        if validation.get("expected_exit_code") != 0: raise AssertionError("validation metadata")
        forbidden = json.dumps(provenance, sort_keys=True)
        if FORBIDDEN.search(forbidden): raise AssertionError("forbidden provenance field")
    except (OSError, json.JSONDecodeError, KeyError, TypeError, AssertionError) as error:
        print(f"VALIDATION FAILED: {error}", file=sys.stderr)
        return 1
    print("VALIDATION PASSED: committed qualification result bundle is internally consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
