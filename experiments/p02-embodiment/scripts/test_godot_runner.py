#!/usr/bin/env python3
"""Deterministic unit checks for the C03 Godot-channel classifier."""
from __future__ import annotations

from run_godot_qualification import classify_logs


def main() -> int:
    cases = {
        "stdout_error": (["ERROR: stdout failure"], [], [], True),
        "stderr_error": ([], ["ERROR: stderr failure"], [], True),
        "engine_error": ([], [], ["ERROR: engine failure"], True),
        "xvfb_warning_only": ([], [], [], False),
        "ordinary_warning": (["WARNING: ordinary warning"], [], [], False),
        "clean": ([], [], [], False),
        # This is the regression guard for the former stdout-only workflow:
        # a stderr error must not be silently classified as clean.
        "former_stdout_only_regression": ([], ["ERROR: hidden stderr failure"], [], True),
    }
    for name, (stdout, stderr, engine, should_fail) in cases.items():
        result = classify_logs(stdout, stderr, engine)
        actual = result["godot_gate"] == "FAILED"
        if actual != should_fail:
            raise SystemExit(f"{name}: expected fail={should_fail}, got {result}")
    print("{\"status\":\"PASSED\",\"cases\":7,\"wrapper_warning_is_separate\":true}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
