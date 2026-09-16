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
AUTHORITY_REVISION = "r06-production-transition-authority-v1"
AUTHORITY_PATH = Path(__file__).resolve().parents[1] / "godot" / "transition_authority.json"


def load_authority() -> dict:
    authority = json.loads(AUTHORITY_PATH.read_text())
    if authority.get("revision") != AUTHORITY_REVISION or not isinstance(authority.get("edges"), dict):
        raise ValueError("production transition authority metadata invalid")
    return authority


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    payload = json.loads(args.path.read_text())
    authority = load_authority()
    cases = payload.get("cases")
    errors: list[str] = []
    if payload.get("status") != "PASS": errors.append("Godot campaign status is not PASS")
    if payload.get("process") != "Godot": errors.append("campaign was not produced by Godot")
    if payload.get("authority") != "godot_production_legal_graph": errors.append("wrong authority")
    if payload.get("authority_revision") != AUTHORITY_REVISION: errors.append("wrong authority revision")
    if payload.get("pack_sha256") != PACK_SHA: errors.append("wrong pack digest")
    if not isinstance(cases, list) or payload.get("case_count") != len(cases): errors.append("case count mismatch")
    if isinstance(cases, list):
        for case in cases:
            start, request = case.get("start_state"), case.get("request")
            expected = authority["edges"].get(start, {}).get(request, [])
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
