#!/usr/bin/env python3
"""Independent semantic validator for committed R04 evidence."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import tempfile
from pathlib import Path


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(results: Path) -> list[str]:
    errors: list[str] = []
    provenance = load(results / "provenance.json")
    for name, expected in provenance.get("result_sha256", {}).items():
        if not (results / name).is_file() or sha(results / name) != expected: errors.append(f"result hash mismatch: {name}")
    intake = load(results / "source_intake.json")
    if intake.get("status") != "PASSED" or not intake.get("clean_process_byte_identical"): errors.append("source intake or deterministic rebuild failed")
    if not intake["identity_smoke"].get("byte_identical") or intake["identity_smoke"].get("candidate_art"): errors.append("identity smoke role or bytes invalid")
    if intake["approved_reference_hashes"] != {"identity": "86ce1f9428f9a998d57e1a99c4245347d5a05e9f0bcf853c2b68065f351bdb56", "turnaround": "3696c7d63594de38d408438d5b882f3207635bc63e59fb270f624715faeb09e4"}: errors.append("approved reference hash mismatch")
    if not all(frame.get("byte_identical") and frame.get("input_sha256") == frame.get("stored_sha256") == frame.get("runtime_sha256") for frame in intake["intake"]["frames"]): errors.append("source byte equality failed")
    negative = load(results / "intake_validation.json")
    expected = {"wrong_dimension": "wrong_dimensions", "wrong_mode": "wrong_mode", "source_hash_tamper": "source_hash_mismatch", "approval_state": "approval_ineligible", "missing_landmark": "landmark_missing", "contact_tamper": "contact_invalid", "duration_tamper": "duration_invalid", "event_order_tamper": "event_order_invalid"}
    if negative.get("production_pixels_generated") is not False: errors.append("production-pixel boundary invalid")
    for name, reason in expected.items():
        if negative.get("negative_cases", {}).get(name) != {"status": "REJECTED", "reason": reason}: errors.append(f"negative mismatch: {name}")
    rust = load(results / "rust_contract.json")
    if rust.get("actual_pack_returncode") != 0 or not rust.get("missing_pack_path_rejected") or rust.get("missing_pack_path_returncode") == 0: errors.append("Rust actual-pack gate failed")
    godot = load(results / "godot_runtime.json")
    observations = godot.get("authored_pack", {}).get("observations", {})
    exact_order = ["intent_received", "track_resolved", "track_validated", "first_frame_loaded", "first_frame_presented", "started", "frame_changed", "track_event", "completed", "visible_state"]
    if observations.get("valid_event_order") != exact_order: errors.append("Godot event order mismatch")
    if observations.get("missing_track_reason") != "track_missing" or observations.get("ineligible_reason") != "approval_ineligible" or observations.get("corrupt_reason") != "frame_hash_mismatch" or observations.get("restored_status") != "started": errors.append("Godot fail-closed or recovery mismatch")
    if observations.get("fps") != 24 or observations.get("duration_weights") != [1, 2] or godot.get("unexpected_error_output"): errors.append("Godot timing or error output mismatch")
    restored = load(results / "export_restore.json")
    if not restored.get("restored_hashes_equal") or restored.get("status") != "PASSED": errors.append("local export/restore mismatch")
    if load(results / "contract_validation.json").get("status") != "PASSED": errors.append("contract validation failed")
    return errors


def tamper_negative(results: Path) -> dict:
    mutations = {
        "result_hash": ("provenance.json", lambda d: d["result_sha256"].__setitem__("source_intake.json", "0" * 64)),
        "byte_equality": ("source_intake.json", lambda d: d["intake"]["frames"][0].__setitem__("byte_identical", False)),
        "rejection_reason": ("intake_validation.json", lambda d: d["negative_cases"]["wrong_mode"].__setitem__("reason", "wrong_dimensions")),
        "event_order": ("godot_runtime.json", lambda d: d["authored_pack"]["observations"]["valid_event_order"].reverse()),
    }
    outcomes = {}
    for name, (filename, mutate) in mutations.items():
        with tempfile.TemporaryDirectory(prefix="companion-r04-result-tamper-") as temporary:
            destination = Path(temporary)
            for source in results.glob("*.json"):
                (destination / source.name).write_bytes(source.read_bytes())
            value = load(destination / filename); mutate(value)
            (destination / filename).write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            rejected = bool(validate(destination))
            if not rejected: raise AssertionError(f"tamper was accepted: {name}")
            outcomes[name] = "REJECTED"
    return outcomes


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--tamper-negative", action="store_true")
    args = parser.parse_args()
    errors = validate(args.results.resolve())
    tamper = tamper_negative(args.results.resolve()) if args.tamper_negative and not errors else {}
    print(json.dumps({"status": "PASSED" if not errors else "FAILED", "errors": errors, "tamper_negative": tamper}, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
