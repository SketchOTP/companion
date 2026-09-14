#!/usr/bin/env python3
"""Fail-closed semantic validator for the C06 controller qualification."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

PACK_SHA = "1596bc28f2aac81344c4ba814a47deaa3f746e88e53278a81985977d41c8af40"
EXPECTED_NEGATIVES = {
    "duplicate_intent_id", "equal_sequence_replay", "lower_stale_sequence",
    "wrong_cancellation_target", "cancellation_replay_after_completion",
    "wrong_direction", "direction_facing_mismatch", "velocity_sign_mismatch",
    "missing_track", "wrong_profile_track", "front_left_fallback",
    "fixed_step_tick_drop", "fixed_step_tick_duplicate", "loop_recenter",
    "hidden_root_reset", "animation_phase_reset", "ineligible_or_corrupt_pack",
}


def validate(result: dict) -> list[str]:
    errors: list[str] = []
    if result.get("status") != "PASS": errors.append("status")
    if result.get("pack_sha256") != PACK_SHA: errors.append("pack_sha256")
    if result.get("source_pixels_mutated") is not False: errors.append("source_pixels_mutated")
    contract = result.get("intent_contract", {})
    if contract.get("schema_major") != 2 or contract.get("fixed_hz") != 24: errors.append("contract_version_or_clock")
    if contract.get("canonical_owner") != "controller" or contract.get("presentation_owner") != "godot": errors.append("ownership")
    if contract.get("gait_rate_calibration") != {"48": 0.5, "96": 1.0, "144": 1.5}: errors.append("gait_calibration")
    cases = result.get("cases", [])
    if len(cases) != 6: errors.append("case_count")
    for case in cases:
        side = case.get("side"); velocity = case.get("velocity")
        sign = -1 if side == "left" else 1
        if not case.get("directional") or case.get("net_displacement_px", 0) * sign <= 0: errors.append(f"direction:{side}:{velocity}")
        if case.get("semantic_ticks") != 72: errors.append(f"ticks:{side}:{velocity}")
        if case.get("phase_resets") != 0 or not case.get("stop_terminal"): errors.append(f"stop:{side}:{velocity}")
        expected_rate = abs(velocity) / 96
        if any(s.get("playback_rate") != expected_rate for s in case.get("samples", []) if s.get("velocity")): errors.append(f"rate:{side}:{velocity}")
        if case.get("track_ids", [])[-1:] != ["r06_playback_track_09" if side == "left" else "r06_playback_track_14"]: errors.append(f"stop_track:{side}")
    cadence = result.get("render_cadence_probe", {})
    if set(cadence) != {"30fps", "60fps"}: errors.append("cadence_keys")
    if any(v.get("semantic_ticks") != 24 or v.get("final_x") != 96.0 or not v.get("accepted") for v in cadence.values()): errors.append("cadence_equivalence")
    negatives = result.get("negative_matrix", {})
    if negatives.get("passing_baseline") is not True: errors.append("negative_baseline")
    if set(negatives.get("cases", {})) != EXPECTED_NEGATIVES: errors.append("negative_coverage")
    for name, case in negatives.get("cases", {}).items():
        if case.get("independent") is not True or case.get("status") != "failed": errors.append(f"negative:{name}")
    for key in ("normal_rendered_review", "quarter_rendered_review"):
        if result.get(key, {}).get("status") != "delegated_to_godot": errors.append(key)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    args = parser.parse_args()
    data = json.loads(args.result.read_text())
    errors = validate(data)
    if errors:
        print(json.dumps({"status": "FAIL", "errors": errors}, indent=2))
        return 1
    print(json.dumps({"status": "PASS", "errors": [], "result_sha256": hashlib.sha256(args.result.read_bytes()).hexdigest()}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
