#!/usr/bin/env python3
"""Fail-closed structural validator for the C04 locomotion investigation."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


EXPECTED_PACK_SHA = "1596bc28f2aac81344c4ba814a47deaa3f746e88e53278a81985977d41c8af40"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    args = parser.parse_args()
    result = json.loads(args.result.read_text())
    errors: list[str] = []
    if result.get("profile") != "COMPANION_P02_R06_C04_RUNTIME_TRANSFORM_LOCOMOTION_V1":
        errors.append("profile")
    if result.get("source_pack_sha256") != EXPECTED_PACK_SHA:
        errors.append("source pack hash")
    if result.get("source_pixels_mutated") is not False:
        errors.append("source pixels mutated")
    transform = result.get("actual_godot_coordinate_transform", {})
    required = {
        "native_image_dimensions": [1254, 1254],
        "animated_sprite_centered": True,
        "sprite_offset_px": [0.0, 0.0],
        "sprite_scale": [0.5, 0.5],
        "mon_root_position_world": [320.0, 320.0],
        "source_registration_anchor_px": [627.0, 627.0],
    }
    for key, value in required.items():
        if transform.get(key) != value:
            errors.append(f"transform {key}")
    for direction in ("left", "right"):
        rows = result.get(f"{direction}_frames", [])
        if not rows:
            errors.append(f"missing {direction} frames")
        for row in rows:
            if set(row.get("stable_leg_identity", {})) != {"near", "far"}:
                errors.append(f"stable legs {row.get('frame_id')}")
            if row.get("support_state") not in {"single", "double", "none"}:
                errors.append(f"support state {row.get('frame_id')}")
            if row.get("source_sha256") is None or row.get("source_contact") is None or row.get("sprite_local_contact") is None:
                errors.append(f"contact record {row.get('frame_id')}")
        plan = result.get(f"{direction}_repeated_loop_plan", {})
        if not plan.get("anchors"):
            errors.append(f"missing {direction} anchors")
    negatives = result.get("negative_tests", {})
    if negatives.get("baseline_valid") is not True:
        errors.append("negative baseline is not valid")
    for name, case in negatives.get("cases", {}).items():
        if case.get("validator_passed") is not False or case.get("independent_reason_detected") is not True:
            errors.append(f"negative {name}")
    # This directive intentionally stops when the corrected evidence still
    # cannot establish directional travel.  A blocked result is valid evidence
    # only when the precise contradiction is retained.
    if result.get("status") != "BLOCKED":
        errors.append("expected BLOCKED contradiction")
    if not result.get("stop_reason"):
        errors.append("missing stop reason")
    print(json.dumps({"status": "PASS" if not errors else "FAIL", "errors": errors, "result_sha256": hashlib.sha256(args.result.read_bytes()).hexdigest()}, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
