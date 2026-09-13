#!/usr/bin/env python3
"""Fail-closed semantic validator for the R05 candidate evidence bundle."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RESULT_NAMES = ["candidate_pack.json", "intake.json", "rust_contract.json", "godot_runtime.json", "frame_qa.json", "export_restore.json"]
EXPECTED_SHEETS = {
    "neutral-construction-sheet.png": "aa6e2efd8cf7f9a2273bf22b9ebbbc6904fd364ba6749113087b4447617e2d39",
    "neutral-right-profile.png": "7dd7bc596d27f10073ebbf4b4fbae15735992dc1569f9eaae59a3b6cbf485dd4",
    "idle-breathe-sheet.png": "b201607ee9fcf170585a4d69f763cbe24b58fc93119054d086eae291f2ecffe7",
    "walk-sheet.png": "01ba5c7a781fd6cd627632d3cd6ed4505498c990181b969c84e73dec5b4afe36",
    "orient-front-to-front-left-sheet.png": "99ef17e22db3ac0514a082244a850ae7d8db427610ead01e62ce969587aed92d",
    "listen-acknowledge-sheet.png": "2a0de17f14a9f7797ffad777f9ac46d2987cd19d508a51e5a58d34b5230a5855",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(results: Path) -> list[str]:
    errors: list[str] = []
    try:
        provenance = load(results / "provenance.json")
        for name in RESULT_NAMES:
            if provenance.get("result_sha256", {}).get(name) != sha(results / name):
                errors.append(f"result hash mismatch: {name}")
        commit = provenance.get("git_commit", "")
        if not commit or subprocess.run(["git", "merge-base", "--is-ancestor", commit, "HEAD"], cwd=ROOT, capture_output=True).returncode:
            errors.append("evidence commit is not an ancestor of HEAD")
        if provenance.get("source_sheet_sha256") != EXPECTED_SHEETS:
            errors.append("provenance source sheet identity mismatch")
        for name, expected in EXPECTED_SHEETS.items():
            if sha(ROOT / "assets/source/p02/r05/imagegen" / name) != expected:
                errors.append(f"committed source sheet mismatch: {name}")

        candidate = load(results / "candidate_pack.json")
        if candidate.get("status") != "PASSED" or candidate.get("approval_state") != "candidate" or candidate.get("operator_visual_approval") != "PENDING":
            errors.append("candidate authority state mismatch")
        if candidate.get("track_count") != 8 or candidate.get("frame_occurrences") != 33 or candidate.get("unique_source_hashes") != 29:
            errors.append("bounded candidate count equation mismatch")
        if candidate.get("expected_roles") != candidate.get("observed_roles"):
            errors.append("bounded request profile mismatch")
        if candidate.get("clean_process_byte_identical") is not True or candidate.get("committed_manifest_byte_identical") is not True:
            errors.append("deterministic source pack mismatch")

        intake = load(results / "intake.json")
        if intake.get("status") != "PASSED" or intake.get("operation") != "review" or intake.get("approval_state") != "candidate" or intake.get("source_bytes_mutated") is not False:
            errors.append("immutable candidate intake failed")
        if len(intake.get("frames", [])) != 33 or not all(row.get("byte_identical") is True and row.get("input_sha256") == row.get("stored_sha256") == row.get("runtime_sha256") for row in intake.get("frames", [])):
            errors.append("frame byte-preservation equation failed")

        rust = load(results / "rust_contract.json")
        if rust.get("status") != "PASSED" or rust.get("actual_pack_returncode") != 0 or rust.get("missing_pack_path_rejected") is not True or rust.get("track_count") != 8:
            errors.append("Rust actual candidate-pack round trip failed")

        godot = load(results / "godot_runtime.json")
        runs = [godot.get("import", {}), *godot.get("runs", [])]
        if godot.get("status") != "PASSED" or godot.get("godot_error_count") != 0 or len(runs) != 3:
            errors.append("canonical Godot candidate qualification failed")
        for run in runs:
            if run.get("status") != "PASSED" or run.get("process_exit_code") != 0 or run.get("godot_error_lines"):
                errors.append(f"Godot run failed: {run.get('label')}")
        for run in godot.get("runs", []):
            semantic = run.get("semantic_test_result", {})
            observations = semantic.get("observations", {})
            if semantic.get("status") != "PASS" or semantic.get("errors") != [] or observations.get("required_tracks_started") != 8 or observations.get("walk_markers") != ["footfall_left", "footfall_right"] or observations.get("listen_markers") != ["attention_acquired", "acknowledge", "settled"] or observations.get("reverse_orient_markers") != ["facing_changed"]:
                errors.append(f"Godot semantic mismatch: {run.get('label')}")
            if observations.get("ineligible_reason") != "approval_ineligible" or observations.get("corrupt_reason") != "frame_hash_mismatch" or observations.get("restored_status") != "started":
                errors.append(f"Godot failure/recovery mismatch: {run.get('label')}")

        qa = load(results / "frame_qa.json")
        if qa.get("status") != "PASSED" or qa.get("root_metadata_exact") is not True or qa.get("safety_region_violations") or qa.get("transparent_perimeter_violations") or qa.get("identity_quality") != "OPERATOR_VISUAL_REVIEW_PENDING":
            errors.append("frame QA boundary failed")
        if not qa.get("planted_contact_observations") or any(row.get("status") != "PASSED" or row.get("max_rendered_drift_px", 999) > 2 for row in qa.get("planted_contact_observations", [])):
            errors.append("planted contact evidence failed")

        restored = load(results / "export_restore.json")
        if restored.get("status") != "PASSED" or restored.get("restored_hashes_equal") is not True:
            errors.append("local export/restore failed")
    except (OSError, KeyError, json.JSONDecodeError) as exc:
        errors.append(f"validator exception: {exc}")
    return errors


def tamper_negative(results: Path) -> dict:
    cases = {}
    mutations = {
        "approval_escalation": ("candidate_pack.json", lambda value: value.update({"approval_state": "operator_approved"})),
        "track_count": ("candidate_pack.json", lambda value: value.update({"track_count": 7})),
        "byte_preservation": ("intake.json", lambda value: value["frames"][0].update({"byte_identical": False})),
        "godot_error": ("godot_runtime.json", lambda value: value.update({"godot_error_count": 1})),
        "contact_drift": ("frame_qa.json", lambda value: value["planted_contact_observations"][0].update({"max_rendered_drift_px": 3})),
    }
    for name, (filename, mutation) in mutations.items():
        with tempfile.TemporaryDirectory(prefix="companion-r05-tamper-") as temporary:
            clone = Path(temporary) / "results"
            import shutil
            shutil.copytree(results, clone)
            value = load(clone / filename); mutation(value)
            (clone / filename).write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            provenance = load(clone / "provenance.json")
            provenance["result_sha256"][filename] = sha(clone / filename)
            (clone / "provenance.json").write_text(json.dumps(provenance, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            failed = bool(validate(clone))
            cases[name] = "REJECTED" if failed else "ACCEPTED_UNEXPECTEDLY"
    return {"status": "PASSED" if all(value == "REJECTED" for value in cases.values()) else "FAILED", "cases": cases}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--tamper-negative", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    errors = validate(args.results.resolve())
    negative = tamper_negative(args.results.resolve()) if args.tamper_negative and not errors else None
    result = {"status": "PASSED" if not errors and (negative is None or negative["status"] == "PASSED") else "FAILED", "errors": errors, "tamper_negative": negative}
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return 0 if result["status"] == "PASSED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
