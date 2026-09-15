#!/usr/bin/env python3
"""Verify checkpoint-wise pacing and identity for real Godot review captures."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path

LABELS = ("start", "first_cruise", "second_loop_cruise", "stop")
TIMED_LABELS = ("first_cruise", "second_loop_cruise", "stop")
LOWER_RATIO = 3.90
UPPER_RATIO = 4.10

def checkpoint_key(c: dict) -> tuple:
    return (c.get("semantic_tick"), c.get("actor_root_x"), c.get("track_id"), c.get("frame_index"), c.get("authored_track_tick"), c.get("authored_tick_cursor"), c.get("authored_loop_ticks"), c.get("track_derived_phase"), c.get("source_pack_sha256"), c.get("source_frame_filename"), c.get("source_frame_sha256"))

def _validate_pair(normal: dict, quarter: dict, normal_path: Path | None = None, quarter_path: Path | None = None) -> dict:
    n_caps = normal.get("captures", []); q_caps = quarter.get("captures", [])
    assert [c.get("label") for c in n_caps] == list(LABELS), "normal checkpoint labels"
    assert [c.get("label") for c in q_caps] == list(LABELS), "quarter checkpoint labels"
    assert [checkpoint_key(c) for c in n_caps] == [checkpoint_key(c) for c in q_caps], "semantic checkpoints differ"
    for run, path in ((normal, normal_path), (quarter, quarter_path)):
        elapsed = []
        for capture in run["captures"]:
            required = ("review_observed_elapsed_usec", "review_elapsed_usec", "authored_tick_cursor", "source_pack_sha256", "source_frame_sha256", "capture_sha256")
            assert all(capture.get(k) is not None for k in required), (capture.get("label"), "capture metadata")
            observed = int(capture["review_observed_elapsed_usec"]); elapsed.append(observed)
            assert observed >= 0, (capture.get("label"), observed)
            assert capture.get("non_black") is True, (capture.get("label"), "black capture")
            if path is not None:
                capture_path = path.parent / str(capture["file"])
                assert capture_path.is_file(), capture_path
                assert capture.get("capture_sha256") == hashlib.sha256(capture_path.read_bytes()).hexdigest(), capture_path
        assert elapsed == sorted(elapsed), ("non-monotonic capture observation", elapsed)
    by_label_n = {c["label"]: c for c in n_caps}; by_label_q = {c["label"]: c for c in q_caps}
    table = {}
    for label in TIMED_LABELS:
        normal_elapsed = int(by_label_n[label]["review_observed_elapsed_usec"]); quarter_elapsed = int(by_label_q[label]["review_observed_elapsed_usec"])
        assert normal_elapsed > 0 and quarter_elapsed > 0, (label, normal_elapsed, quarter_elapsed)
        ratio = quarter_elapsed / normal_elapsed
        assert LOWER_RATIO <= ratio <= UPPER_RATIO, (label, ratio, normal_elapsed, quarter_elapsed)
        table[label] = {"normal_elapsed_usec": normal_elapsed, "quarter_elapsed_usec": quarter_elapsed, "ratio": ratio}
    normal_wall = float(normal["review_wall_time_ms"]); quarter_wall = float(quarter["review_wall_time_ms"]); full_ratio = quarter_wall / normal_wall
    assert LOWER_RATIO <= full_ratio <= UPPER_RATIO, ("full", full_ratio, normal_wall, quarter_wall)
    table["full_run"] = {"normal_ms": normal_wall, "quarter_ms": quarter_wall, "ratio": full_ratio}
    return table

def check_pair(normal_path: Path, quarter_path: Path) -> dict:
    normal = json.loads(normal_path.read_text(encoding="utf-8")); quarter = json.loads(quarter_path.read_text(encoding="utf-8"))
    table = _validate_pair(normal, quarter, normal_path, quarter_path)
    bad_intermediate = copy.deepcopy(quarter)
    first = next(c for c in bad_intermediate["captures"] if c["label"] == "first_cruise")
    normal_first = next(c for c in normal["captures"] if c["label"] == "first_cruise")
    first["review_observed_elapsed_usec"] = int(normal_first["review_observed_elapsed_usec"] * 3.33)
    try:
        _validate_pair(normal, bad_intermediate)
    except AssertionError:
        intermediate_negative = "rejected"
    else:
        raise AssertionError("bad intermediate checkpoint timing accepted")
    return {"checkpoints": table, "bad_intermediate_checkpoint": intermediate_negative}

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--left-normal", type=Path, required=True); ap.add_argument("--left-quarter", type=Path, required=True); ap.add_argument("--right-normal", type=Path, required=True); ap.add_argument("--right-quarter", type=Path, required=True); a = ap.parse_args()
    result = {"left": check_pair(a.left_normal, a.left_quarter), "right": check_pair(a.right_normal, a.right_quarter), "artificial_ratio_3_33": "rejected", "checkpoint_ratio_bounds": [LOWER_RATIO, UPPER_RATIO], "timing_origin": "monotonic review epoch immediately before cruise intent", "observation_point": "post-wait RenderingServer.frame_post_draw observation before readback"}
    print(json.dumps({"status": "PASS", **result}, indent=2, sort_keys=True)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
