#!/usr/bin/env python3
"""Independent C02 result validator; generated validation is never an input."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
IDENTITY_SHA = "86ce1f9428f9a998d57e1a99c4245347d5a05e9f0bcf853c2b68065f351bdb56"
TURNAROUND_SHA = "3696c7d63594de38d408438d5b882f3207635bc63e59fb270f624715faeb09e4"


def sha(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()
def load(path: Path) -> dict: return json.loads(path.read_text(encoding="utf-8"))


def validate(results: Path) -> list[str]:
    errors: list[str] = []
    try:
        provenance = load(results / "provenance.json")
        required = ["source_intake.json", "intake_validation.json", "rust_contract.json", "godot_runtime.json", "export_restore.json", "contract_validation.json"]
        for name in required:
            expected = provenance.get("result_sha256", {}).get(name); path = results / name
            if not expected or not path.is_file() or sha(path) != expected: errors.append(f"result hash mismatch: {name}")
        commit = provenance.get("git_commit", "")
        if not commit or subprocess.run(["git", "merge-base", "--is-ancestor", commit, "HEAD"], cwd=ROOT).returncode != 0: errors.append("evidence commit is not an ancestor of checked-out HEAD")
        for relative, expected in provenance.get("fixture_sha256", {}).items():
            path = ROOT / relative
            if not path.is_file() or sha(path) != expected: errors.append(f"fixture hash mismatch: {relative}")
        if not provenance.get("execution_start_utc") or not provenance.get("execution_end_utc"): errors.append("timestamps missing")
        if "T00:00:00Z" in json.dumps(provenance): errors.append("date-only placeholder timestamp")
        intake = load(results / "source_intake.json")
        if intake.get("status") != "PASSED" or intake.get("profile") != "phase02_bounded_motion_proof_v1" or intake.get("track_count") != 8 or intake.get("frame_count") != 31 or intake.get("clean_process_byte_identical") is not True: errors.append("complete positive profile not proven")
        if intake.get("approved_reference_hashes") != {"identity": IDENTITY_SHA, "turnaround": TURNAROUND_SHA}: errors.append("approved reference hashes mismatch")
        smoke = intake.get("identity_smoke", {})
        if smoke.get("byte_identical") is not True or smoke.get("candidate_art") is not False: errors.append("identity smoke boundary invalid")
        if not all(row.get("byte_identical") is True and row.get("input_sha256") == row.get("stored_sha256") == row.get("runtime_sha256") for row in intake.get("intake", {}).get("frames", [])): errors.append("source byte equality failed")
        negative = load(results / "intake_validation.json"); eq = negative.get("category_equations", {})
        if negative.get("status") != "PASSED" or negative.get("production_pixels_generated") is not False or negative.get("invalid_accepted") != 0: errors.append("negative boundary failed")
        if eq.get("requested_total") != eq.get("accepted", 0) + eq.get("rejected", 0) + eq.get("duplicate", 0) or eq.get("accepted") != 0 or eq.get("rejected") != len(negative.get("negative_cases", {})) or eq.get("duplicate") != 0: errors.append("negative equations failed")
        expected = {"right_profile_mismatch": "request_profile_incomplete", "missing_neutral_role": "request_profile_incomplete", "duplicate_neutral_role": "request_profile_duplicate_role", "wrong_entry_exit_frame_facing": "filename_invalid", "missing_facing_changed": "request_profile_event_missing", "missing_walk_footfalls": "request_profile_event_missing", "listen_acknowledge_order": "request_profile_event_missing", "invalid_reuse_target_hash": "reuse_reference_invalid", "wrong_dimension": "wrong_dimensions", "wrong_mode": "png_color_type_invalid", "source_hash_tamper": "source_hash_mismatch", "approval_state": "approval_ineligible", "missing_srgb": "missing_srgb", "iccp_only_false_srgb": "missing_srgb", "duplicate_srgb": "srgb_duplicate", "trailing_bytes": "png_trailing_or_missing_iend", "malformed_chunk_order": "png_chunk_order_invalid", "mid_intake_failure": "injected_mid_intake_failure", "stale_output": "destination_not_empty"}
        for name, reason in expected.items():
            if negative.get("negative_cases", {}).get(name) != {"status": "REJECTED", "reason": reason}: errors.append(f"negative mismatch: {name}")
        rust = load(results / "rust_contract.json")
        if rust.get("status") == "PASSED":
            if rust.get("actual_pack_returncode") != 0 or rust.get("missing_pack_path_rejected") is not True or rust.get("track_count") != 8 or rust.get("frame_count") != 31: errors.append("Rust actual-pack gate failed")
        elif rust.get("status") == "NOT_RUN": errors.append("Rust actual-pack evidence unavailable")
        else: errors.append("Rust result status invalid")
        if load(results / "contract_validation.json").get("status") != "PASSED": errors.append("contract validation failed")
        restored = load(results / "export_restore.json")
        if restored.get("status") != "PASSED" or restored.get("restored_hashes_equal") is not True: errors.append("export/restore mismatch")
        godot = load(results / "godot_runtime.json")
        if godot.get("status") == "PASSED" and godot.get("unexpected_error_output") is True: errors.append("unexpected Godot ERROR output")
        if godot.get("status") not in {"PASSED", "BLOCKED", "NOT_RUN"}: errors.append("Godot result status invalid")
        if godot.get("status") != "PASSED": errors.append("render-boundary Godot evidence unavailable")
    except (OSError, json.JSONDecodeError, KeyError) as exc: errors.append(f"validator exception: {exc}")
    return errors


def tamper_negative(results: Path) -> dict[str, bool]:
    outcomes: dict[str, bool] = {}
    mutations = {
        "result_hash": lambda d: d["provenance"]["result_sha256"].__setitem__("source_intake.json", "0" * 64),
        "category_outcome": lambda d: d["intake_validation"]["category_equations"].__setitem__("accepted", 1),
        "rejection_reason": lambda d: d["intake_validation"]["negative_cases"]["missing_srgb"].__setitem__("reason", "wrong"),
        "invalid_accepted": lambda d: d["intake_validation"].__setitem__("invalid_accepted", 1),
        "acceptance_observation": lambda d: d["source_intake"].__setitem__("frame_count", 30),
    }
    with tempfile.TemporaryDirectory(prefix="r04-c02-tamper-") as td:
        base = Path(td)
        for name, mutate in mutations.items():
            case = base / name; case.mkdir();
            for path in results.glob("*.json"): shutil.copyfile(path, case / path.name)
            docs = {key: load(case / f"{key}.json") for key in ["provenance", "intake_validation", "source_intake"]}
            mutate(docs); stable = lambda p, v: p.write_text(json.dumps(v, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            for key, value in docs.items(): stable(case / f"{key}.json", value)
            outcomes[name] = bool(validate(case))
    return outcomes


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--results", type=Path, required=True); parser.add_argument("--tamper-negative", action="store_true"); args = parser.parse_args(); results = args.results.resolve(); errors = validate(results); tamper = tamper_negative(results) if args.tamper_negative else {}
    if args.tamper_negative and not all(tamper.values()): errors.append("tamper-negative mutation was accepted")
    status = "PASSED" if not errors else "BLOCKED" if all(item.startswith("render-boundary") for item in errors) else "FAILED"
    print(json.dumps({"status": status, "errors": errors, "tamper_negative": tamper}, sort_keys=True));
    return 0 if not errors else 1


if __name__ == "__main__": raise SystemExit(main())
