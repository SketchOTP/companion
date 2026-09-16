#!/usr/bin/env python3
"""Validate the single production transition-authority data source."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "godot" / "transition_authority.json"
REVISION = "r06-production-transition-authority-v1"


def main() -> int:
    authority = json.loads(PATH.read_text(encoding="utf-8"))
    edges = authority.get("edges")
    errors: list[str] = []
    if authority.get("revision") != REVISION:
        errors.append("authority revision mismatch")
    if not isinstance(edges, dict) or not edges:
        errors.append("authority edges missing")
    states = set(edges or {})
    for start, requests in (edges or {}).items():
        if not isinstance(requests, dict):
            errors.append(f"{start}: request table is not an object")
            continue
        for request, route in requests.items():
            if not isinstance(route, list) or not route:
                errors.append(f"{start}/{request}: empty route")
                continue
            if route[0] != start:
                errors.append(f"{start}/{request}: route does not begin at start")
            if any(state not in states for state in route):
                errors.append(f"{start}/{request}: route references unknown state")
    result = {"status": "PASS" if not errors else "FAIL", "revision": authority.get("revision"), "state_count": len(states), "edge_count": sum(len(v) for v in (edges or {}).values() if isinstance(v, dict)), "errors": errors}
    print(json.dumps(result, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
