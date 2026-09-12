#!/usr/bin/env python3
"""Independent, fail-closed validator for the committed/sanitized R04-C01 set."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
IDENTITY_SHA = "86ce1f9428f9a998d57e1a99c4245347d5a05e9f0bcf853c2b68065f351bdb56"
TURNAROUND_SHA = "3696c7d63594de38d408438d5b882f3207635bc63e59fb270f624715faeb09e4"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(results: Path) -> list[str]:
    errors: list[str] = []
    try:
        provenance = load(results / "provenance.json")
        required_results = ["source_intake.json", "intake_validation.json", "rust_contract.json", "godot_runtime.json", "export_restore.json", "contract_validation.json"]
        for name in required_results:
            expected = provenance.get("result_sha256", {}).get(name)
            if not expected or not (results / name).is_file() or sha(results / name) != expected:
                errors.append(f"result hash mismatch: {name}")
        if not provenance.get("git_commit"):
            errors.append("git commit binding missing")
        else:
            ancestry = subprocess.run(["git", "merge-base", "--is-ancestor", provenance["git_commit"], "HEAD"], cwd=ROOT)
            if ancestry.returncode != 0:
                errors.append("evidence commit is not an ancestor of checked-out HEAD")
        for relative, expected in provenance.get("fixture_sha256", {}).items():
            path = ROOT / relative
            if not path.is_file() or sha(path) != expected:
                errors.append(f"fixture hash mismatch: {relative}")
        if not provenance.get("execution_start_utc") or not provenance.get("execution_end_utc"):
            errors.append("observed execution timestamps missing")
        if "2026-09-09T00:00:00Z" in json.dumps(provenance):
            errors.append("placeholder timestamp present")

        intake = load(results / "source_intake.json")
        if intake.get("status") != "PASSED" or intake.get("clean_process_byte_identical") is not True:
            errors.append("source intake or deterministic rebuild failed")
        if intake.get("approved_reference_hashes") != {"identity": IDENTITY_SHA, "turnaround": TURNAROUND_SHA}:
            errors.append("approved reference hash mismatch")
        smoke = intake.get("identity_smoke", {})
        if smoke.get("byte_identical") is not True or smoke.get("candidate_art") is not False:
            errors.append("identity smoke role or bytes invalid")
        rows = intake.get("intake", {}).get("frames", [])
        if not rows or not all(row.get("byte_identical") is True and row.get("input_sha256") == row.get("stored_sha256") == row.get("runtime_sha256") for row in rows):
            errors.append("source byte equality failed")

        negative = load(results / "intake_validation.json")
        if negative.get("production_pixels_generated") is not False or negative.get("invalid_accepted") != 0:
            errors.append("production-pixel or invalid-accepted boundary failed")
        equations = negative.get("category_equations", {})
        if negative.get("status") != "PASSED" or equations.get("requested_total") != equations.get("accepted", 0) + equations.get("rejected", 0) + equations.get("duplicate", 0) or equations.get("accepted") != 0 or equations.get("rejected") != len(negative.get("negative_cases", {})) or equations.get("duplicate") != 0:
            errors.append("negative category equations failed")
        expected = {
            "wrong_dimension": "wrong_dimensions", "wrong_mode": "png_color_type_invalid",
            "source_hash_tamper": "source_hash_mismatch", "approval_state": "approval_ineligible",
            "missing_landmark": "landmark_missing", "contact_tamper": "contact_invalid",
            "duration_tamper": "duration_invalid", "event_tick_tamper": "event_tick_frame_mismatch",
            "duplicate_asset": "duplicate_source_asset", "missing_srgb": "missing_srgb",
            "orientation_endpoint": "orientation_endpoint_mismatch", "invalid_landmark_state": "landmark_state_invalid",
            "duplicate_frame_id": "duplicate_frame_identity", "duplicate_track_id": "duplicate_track_id",
            "incomplete_profile": "request_profile_incomplete", "sixteen_bit_rgba": "png_bit_depth_invalid",
            "blank_image": "blank_image", "opaque_background": "opaque_background",
            "path_traversal": "manifest_invalid", "stale_destination": "destination_not_empty",
        }
        for name, reason in expected.items():
            if negative.get("negative_cases", {}).get(name) != {"status": "REJECTED", "reason": reason}:
                errors.append(f"negative mismatch: {name}")

        rust = load(results / "rust_contract.json")
        if rust.get("status") == "PASSED":
            if rust.get("actual_pack_returncode") != 0 or rust.get("missing_pack_path_rejected") is not True or rust.get("missing_pack_path_returncode") == 0:
                errors.append("Rust actual-pack gate failed")
        elif rust.get("status") != "NOT_RUN":
            errors.append("Rust result has unknown status")
        if load(results / "contract_validation.json").get("status") != "PASSED":
            errors.append("contract validation failed")
        restored = load(results / "export_restore.json")
        if restored.get("status") != "PASSED" or restored.get("restored_hashes_equal") is not True:
            errors.append("local export/restore mismatch")

        godot = load(results / "godot_runtime.json")
        if godot.get("status") == "PASSED":
            if godot.get("unexpected_error_output") is True:
                errors.append("unexpected Godot ERROR output")
            output = godot.get("output", "")
            if "first_frame_render_committed" not in output or '"status": "PASS"' not in output:
                errors.append("Godot render-commit or exact-track result missing")
        elif godot.get("status") != "NOT_RUN":
            errors.append("Godot result has unknown status")
    except (KeyError, OSError, json.JSONDecodeError) as exc:
        errors.append(f"result bundle unreadable: {exc}")
    return errors


def tamper_negative(results: Path) -> dict[str, str]:
    mutations = {
        "result_hash": ("provenance.json", lambda d: d["result_sha256"].__setitem__("source_intake.json", "0" * 64)),
        "category_outcome": ("intake_validation.json", lambda d: d["category_equations"].__setitem__("accepted", 1)),
        "rejection_reason": ("intake_validation.json", lambda d: d["negative_cases"]["wrong_mode"].__setitem__("reason", "wrong_dimensions")),
        "invalid_accepted": ("intake_validation.json", lambda d: d.__setitem__("invalid_accepted", 1)),
        "acceptance_observation": ("source_intake.json", lambda d: d.__setitem__("clean_process_byte_identical", False)),
    }
    outcomes: dict[str, str] = {}
    for name, (filename, mutate) in mutations.items():
        with tempfile.TemporaryDirectory(prefix="companion-r04-c01-tamper-") as temporary:
            destination = Path(temporary)
            for source in results.glob("*.json"):
                (destination / source.name).write_bytes(source.read_bytes())
            value = load(destination / filename); mutate(value)
            (destination / filename).write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            if not validate(destination):
                raise AssertionError(f"tamper was accepted: {name}")
            outcomes[name] = "REJECTED"
    return outcomes


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--results", type=Path, required=True); parser.add_argument("--tamper-negative", action="store_true")
    args = parser.parse_args(); errors = validate(args.results.resolve()); tamper = tamper_negative(args.results.resolve()) if args.tamper_negative and not errors else {}
    print(json.dumps({"status": "PASSED" if not errors else "FAILED", "errors": errors, "tamper_negative": tamper}, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
