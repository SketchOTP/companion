#!/usr/bin/env python3
"""Validate C03 support evidence and its fail-closed stop condition."""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path


def support_rows_valid(rows: list[dict]) -> bool:
    for row in rows:
        visible = set(row.get("visible_grounded_soles", []))
        support = row.get("support_foot")
        state = row.get("support_state")
        if state != ("double" if len(visible) > 1 else "single" if len(visible) == 1 else "none"):
            return False
        if support is not None and support not in visible:
            return False
        if row.get("ambiguity"):
            return False
        if not row.get("source_sha256") or not row.get("source_contacts"):
            return False
    return True


def plan_valid(plan: dict, direction: str) -> bool:
    sign = -1 if direction == "left" else 1
    anchors = plan.get("touchdown_anchors", [])
    deltas = [float(value) for value in plan.get("touchdown_deltas_px", [])]
    if len(anchors) < 3 or len(deltas) != len(anchors) - 1:
        return False
    if not all(delta * sign > 0 for delta in deltas):
        return False
    if float(plan.get("net_displacement_px", 0.0)) * sign <= 0:
        return False
    if float(plan.get("max_planted_slip_px", 999.0)) > 2:
        return False
    return True


def positive_predicate(payload: dict) -> bool:
    return (
        support_rows_valid(payload.get("walk_tracks", {}).get("left", []))
        and support_rows_valid(payload.get("walk_tracks", {}).get("right", []))
        and plan_valid(payload.get("left_two_loop_plan", {}), "left")
        and plan_valid(payload.get("right_two_loop_plan", {}), "right")
    )


def negative_matrix(payload: dict) -> dict[str, bool]:
    def rejected(mutated: dict) -> bool:
        return not positive_predicate(mutated)

    omitted = copy.deepcopy(payload)
    omitted["walk_tracks"]["left"][6]["visible_grounded_soles"] = []
    omitted["walk_tracks"]["left"][6]["support_state"] = "none"

    swapped = copy.deepcopy(payload)
    swapped["walk_tracks"]["left"][7]["support_foot"] = "ground_contact_right"

    reversed_touchdown = copy.deepcopy(payload)
    reversed_touchdown["left_two_loop_plan"]["touchdown_deltas_px"] = [abs(x) for x in reversed_touchdown["left_two_loop_plan"]["touchdown_deltas_px"]]

    zero_loop = copy.deepcopy(payload)
    zero_loop["left_two_loop_plan"]["net_displacement_px"] = 0.0
    zero_loop["left_two_loop_plan"]["touchdown_deltas_px"] = [0.0] * len(zero_loop["left_two_loop_plan"]["touchdown_deltas_px"])

    recentered = copy.deepcopy(payload)
    anchors = recentered["left_two_loop_plan"]["touchdown_anchors"]
    if len(anchors) > 2:
        anchors[-1]["anchor"] = copy.deepcopy(anchors[1]["anchor"])
    recentered["left_two_loop_plan"]["touchdown_deltas_px"] = [0.0] * (len(anchors) - 1)

    reset = copy.deepcopy(payload)
    if len(reset["left_two_loop_plan"].get("ticks", [])) > 2:
        reset["left_two_loop_plan"]["ticks"][2]["actor_root"]["x"] += 100.0
    reset["left_two_loop_plan"]["max_actor_step_px"] = 100.0

    slip = copy.deepcopy(payload)
    slip["left_two_loop_plan"]["max_planted_slip_px"] = 3.0

    return {
        "omitted_passing_up_support_rejected": rejected(omitted),
        "support_identity_swap_rejected": rejected(swapped),
        "reversed_touchdown_rejected": rejected(reversed_touchdown),
        "zero_net_loop_rejected": rejected(zero_loop),
        "second_loop_recenter_rejected": rejected(recentered),
        "hidden_root_reset_rejected": rejected(reset),
        "planted_slip_over_two_px_rejected": rejected(slip),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence", type=Path, required=True)
    args = parser.parse_args()
    evidence = args.evidence.resolve()
    payload = json.loads((evidence / "support_investigation.json").read_text())
    negatives = negative_matrix(payload)
    result = {
        "profile": "COMPANION_P02_R06_C03_SUPPORT_VALIDATION_V1",
        "status": "PASS" if positive_predicate(payload) and all(negatives.values()) else "BLOCKED",
        "positive_predicate": positive_predicate(payload),
        "negative_tests": negatives,
        "left_net_displacement_px": payload["left_two_loop_plan"]["net_displacement_px"],
        "right_net_displacement_px": payload["right_two_loop_plan"]["net_displacement_px"],
    }
    (evidence / "validation.json").write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    # BLOCKED is an intentional directive stop, distinct from a validator
    # crash.  Negative tests must still pass before returning that stop.
    return 0 if result["status"] == "PASS" else 2 if all(negatives.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
