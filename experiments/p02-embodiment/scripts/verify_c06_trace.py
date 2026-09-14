#!/usr/bin/env python3
"""Shared verifier for positive Godot C06 traces and scheduler negatives."""
from __future__ import annotations

import copy
import json
import math
import sys
from pathlib import Path


def verify_positive(trace: dict) -> list[str]:
    errors: list[str] = []
    samples = trace.get("samples", [])
    if not samples:
        return ["samples_missing"]
    ticks = [s.get("semantic_tick") for s in samples]
    if ticks != list(range(len(ticks))):
        errors.append("semantic_tick_sequence")
    for a, b in zip(samples, samples[1:]):
        if abs(float(b.get("actor_root_x", 0)) - float(a.get("actor_root_x", 0))) > 4.000001:
            errors.append("actor_position_discontinuity")
            break
    cruise = [s for s in samples if s.get("phase") == "cruise" and s.get("velocity")]
    if not cruise:
        errors.append("cruise_samples_missing")
    for a, b in zip(cruise, cruise[1:]):
        delta = (float(b.get("animation_phase", 0)) - float(a.get("animation_phase", 0))) % 1.0
        expected = abs(float(a.get("velocity", 0))) / 96.0 / 32.0
        if not math.isclose(delta, expected, abs_tol=1e-6):
            errors.append("animation_phase_discontinuity")
            break
    captures = trace.get("captures", [])
    required = {"start", "first_cruise", "second_loop_cruise", "stop"}
    if {c.get("label") for c in captures} != required:
        errors.append("checkpoint_set")
    if any(not c.get("non_black") for c in captures):
        errors.append("black_capture")
    moving = [c for c in captures if c.get("label") in {"first_cruise", "second_loop_cruise"}]
    if len({c.get("actor_root_x") for c in moving}) < 2:
        errors.append("checkpoint_position_static")
    return errors


def trace_guard(trace: dict) -> str | None:
    errors = verify_positive(trace)
    return errors[0] if errors else None


def negatives(trace: dict) -> dict[str, dict[str, object]]:
    baseline = copy.deepcopy(trace)
    assert not verify_positive(baseline), verify_positive(baseline)
    cases: dict[str, dict[str, object]] = {}
    for name, mutate, reason in (
        ("fixed_step_tick_drop", lambda t: t["samples"].pop(3), "semantic_tick_sequence"),
        ("fixed_step_tick_duplicate", lambda t: t["samples"].insert(3, copy.deepcopy(t["samples"][3])), "semantic_tick_sequence"),
        ("loop_recenter", lambda t: t["samples"].__setitem__(32, {**t["samples"][32], "actor_root_x": 0}), "actor_position_discontinuity"),
        ("hidden_root_reset", lambda t: t["samples"].__setitem__(32, {**t["samples"][32], "actor_root_x": 9999}), "actor_position_discontinuity"),
        ("animation_phase_reset", lambda t: t["samples"].__setitem__(33, {**t["samples"][33], "animation_phase": t["samples"][32]["animation_phase"]}), "animation_phase_discontinuity"),
        ("capture_black", lambda t: t["captures"].__setitem__(0, {**t["captures"][0], "non_black": False}), "black_capture"),
    ):
        mutated = copy.deepcopy(baseline)
        mutate(mutated)
        observed = trace_guard(mutated)
        cases[name] = {"status": "failed", "reason": observed, "expected_reason": reason, "independent": observed == reason}
    return cases


def main() -> int:
    path = Path(sys.argv[1])
    trace = json.loads(path.read_text(encoding="utf-8"))
    errors = verify_positive(trace)
    if errors:
        print(json.dumps({"status": "FAIL", "errors": errors}, indent=2))
        return 1
    result = {"status": "PASS", "positive_trace": str(path.name), "negative_category": "scheduler/trace-verifier", "negative_matrix": negatives(trace)}
    if not all(v["independent"] for v in result["negative_matrix"].values()):
        result["status"] = "FAIL"
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
