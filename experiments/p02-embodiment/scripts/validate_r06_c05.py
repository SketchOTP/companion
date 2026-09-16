#!/usr/bin/env python3
"""Fail-closed validator for controller-owned R06-C05 evidence."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

PACK_SHA = "1596bc28f2aac81344c4ba814a47deaa3f746e88e53278a81985977d41c8af40"
PROFILE = "COMPANION_P02_R06_C05_CONTROLLER_LOCOMOTION_V1"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    args = parser.parse_args()
    data = json.loads(args.result.read_text())
    errors: list[str] = []
    if data.get("profile") != PROFILE:
        errors.append("profile")
    if data.get("pack_sha256") != PACK_SHA:
        errors.append("pack hash")
    if data.get("source_pixels_mutated") is not False:
        errors.append("source mutation")
    contract = data.get("intent_contract", {})
    if contract.get("tick_rate_hz") != 24 or contract.get("canonical_owner") != "controller" or contract.get("presentation_owner") != "godot":
        errors.append("ownership/timing contract")
    expected = {"left": {-48, -96, -144}, "right": {48, 96, 144}}
    observed: dict[str, set[int]] = {"left": set(), "right": set()}
    for case in data.get("cases", []):
        side, velocity = case.get("side"), case.get("velocity")
        if side not in expected or velocity not in expected[side]:
            errors.append(f"unexpected case {side}/{velocity}")
            continue
        observed[side].add(velocity)
        if case.get("trace_validation") is not None or not case.get("directional"):
            errors.append(f"directional trace {side}/{velocity}")
        if case.get("phase_resets") != 0:
            errors.append(f"phase reset {side}/{velocity}")
        if len(case.get("loop_boundary_positions", [])) != 2:
            errors.append(f"loop boundary {side}/{velocity}")
        samples = case.get("samples", [])
        if [s.get("tick") for s in samples] != list(range(len(samples))):
            errors.append(f"tick sequence {side}/{velocity}")
        moving = [s["actor_root_x"] for s in samples if s.get("phase") != "stop"]
        sign = -1 if side == "left" else 1
        if not moving or (moving[-1] - moving[0]) * sign <= 0:
            errors.append(f"travel sign {side}/{velocity}")
    for side, velocities in expected.items():
        if observed[side] != velocities:
            errors.append(f"velocity coverage {side}")
        interruption = data.get(f"{side}_interruption", {})
        if not interruption.get("samples") or interruption.get("end_x") == interruption.get("start_x"):
            errors.append(f"interruption {side}")
    negatives = data.get("negative_matrix", {})
    if negatives.get("passing_baseline") is not True:
        errors.append("negative baseline")
    for name, case in negatives.get("cases", {}).items():
        if case.get("validator_passed") is not False or case.get("independent_reason_detected") is not True:
            errors.append(f"negative {name}")
    digest = hashlib.sha256(args.result.read_bytes()).hexdigest()
    print(json.dumps({"status": "PASS" if not errors else "FAIL", "errors": errors, "result_sha256": digest}, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
