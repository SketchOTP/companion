#!/usr/bin/env python3
"""Independently verify the raw production-Godot transition campaign.

Godot owns the legal decision.  This verifier only recomputes the expected
shape of the frozen graph and checks that the observed route agrees with it;
it never supplies a route to the runtime.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

PACK_SHA = "1596bc28f2aac81344c4ba814a47deaa3f746e88e53278a81985977d41c8af40"
STATES = [
    "front_rest", "left_profile_rest", "right_profile_rest", "left_start",
    "left_loop", "left_stop", "right_start", "right_loop", "right_stop", "listen",
]
REQUESTS = ["left", "right", "listen", "stop", "cancel"]


def expected_route(start: str, request: str) -> list[str]:
    if request == "left" and start in {"front_rest", "listen", "left_profile_rest"}:
        return [start, "left_start", "left_loop", "left_stop", "left_profile_rest"]
    if request == "right" and start in {"front_rest", "listen", "right_profile_rest"}:
        return [start, "right_start", "right_loop", "right_stop", "right_profile_rest"]
    if request == "listen" and start in {"front_rest", "listen"}:
        return [start, "listen"]
    if request == "stop" and start in {"left_start", "left_loop"}:
        return [start, "left_stop", "left_profile_rest"]
    if request == "stop" and start in {"right_start", "right_loop"}:
        return [start, "right_stop", "right_profile_rest"]
    if request == "cancel" and start in {"left_start", "left_loop"}:
        return [start, "left_stop"]
    if request == "cancel" and start in {"right_start", "right_loop"}:
        return [start, "right_stop"]
    return []


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    payload = json.loads(args.path.read_text())
    cases = payload.get("cases")
    errors: list[str] = []
    if payload.get("status") != "PASS": errors.append("Godot campaign status is not PASS")
    if payload.get("process") != "Godot": errors.append("campaign was not produced by Godot")
    if payload.get("authority") != "godot_production_legal_graph": errors.append("wrong authority")
    if payload.get("pack_sha256") != PACK_SHA: errors.append("wrong pack digest")
    if not isinstance(cases, list) or payload.get("case_count") != len(cases): errors.append("case count mismatch")
    if isinstance(cases, list):
        for case in cases:
            start, request = case.get("start_state"), case.get("request")
            expected = expected_route(start, request)
            observed = case.get("route") or []
            if case.get("pack_sha256") != PACK_SHA: errors.append(f"{case.get('case_id')}: pack mismatch")
            if bool(case.get("accepted")) != bool(expected): errors.append(f"{case.get('case_id')}: acceptance mismatch")
            if observed != expected: errors.append(f"{case.get('case_id')}: route mismatch")
            if (case.get("terminal_state") != (expected[-1] if expected else start)):
                errors.append(f"{case.get('case_id')}: terminal mismatch")
    result = {
        "status": "PASS" if not errors else "FAIL",
        "source": str(args.path),
        "source_sha256": hashlib.sha256(args.path.read_bytes()).hexdigest(),
        "case_count": len(cases) if isinstance(cases, list) else 0,
        "errors": errors[:50],
        "authority": "independent_python_verifier_only",
        "evidence_ceiling": "E3_TARGET_TESTED",
    }
    print(json.dumps(result, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
