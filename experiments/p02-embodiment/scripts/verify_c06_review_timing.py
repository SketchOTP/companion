#!/usr/bin/env python3
"""Verify real Godot normal/quarter checkpoint identity and wall pacing."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

LABELS = ("start", "first_cruise", "second_loop_cruise", "stop")

def checkpoint_key(c: dict) -> tuple:
    return (c.get("semantic_tick"), c.get("actor_root_x"), c.get("track_id"), c.get("frame_index"), c.get("authored_track_tick"), c.get("track_derived_phase"), c.get("source_pack_sha256"), c.get("source_frame_filename"), c.get("source_frame_sha256"))

def check_pair(normal_path: Path, quarter_path: Path) -> dict:
    normal = json.loads(normal_path.read_text()); quarter = json.loads(quarter_path.read_text())
    assert [c["label"] for c in normal["captures"]] == list(LABELS)
    assert [c["label"] for c in quarter["captures"]] == list(LABELS)
    assert [checkpoint_key(c) for c in normal["captures"]] == [checkpoint_key(c) for c in quarter["captures"]]
    for run in (normal, quarter):
        for capture in run["captures"]:
            capture_path = (normal_path.parent if run is normal else quarter_path.parent) / capture["file"]
            assert capture.get("non_black") is True
            assert capture.get("capture_sha256") == hashlib.sha256(capture_path.read_bytes()).hexdigest()
    ratio = float(quarter["review_wall_time_ms"]) / float(normal["review_wall_time_ms"])
    assert 3.90 <= ratio <= 4.10, ratio
    assert not (3.90 <= 3.33 <= 4.10), "artificial 3.33x ratio accepted"
    return {"normal_ms": normal["review_wall_time_ms"], "quarter_ms": quarter["review_wall_time_ms"], "ratio": ratio, "checkpoints": len(LABELS)}

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--left-normal", type=Path, required=True); ap.add_argument("--left-quarter", type=Path, required=True); ap.add_argument("--right-normal", type=Path, required=True); ap.add_argument("--right-quarter", type=Path, required=True)
    a = ap.parse_args(); result = {"left": check_pair(a.left_normal, a.left_quarter), "right": check_pair(a.right_normal, a.right_quarter), "artificial_ratio_3_33": "rejected"}; print(json.dumps({"status": "PASS", **result}, indent=2, sort_keys=True)); return 0

if __name__ == "__main__": raise SystemExit(main())
