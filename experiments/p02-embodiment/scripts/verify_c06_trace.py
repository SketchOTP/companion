#!/usr/bin/env python3
"""Pack-backed verifier for the real Godot C06 movement trace."""
from __future__ import annotations
import copy, hashlib, json, math, sys
from pathlib import Path

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def _frame_for_tick(durations: list[int], tick: int) -> int:
    cursor = 0
    for index, duration in enumerate(durations):
        cursor += duration
        if tick < cursor: return index
    return max(0, len(durations) - 1)

def verify_positive(trace: dict, pack: dict | None = None, trace_dir: Path | None = None) -> list[str]:
    errors: list[str] = []
    samples = trace.get("samples", [])
    if not samples: return ["samples_missing"]
    if [s.get("semantic_tick") for s in samples] != list(range(len(samples))): errors.append("semantic_tick_sequence")
    for a, b in zip(samples, samples[1:]):
        if abs(float(b.get("actor_root_x", 0)) - float(a.get("actor_root_x", 0))) > 4.000001:
            errors.append("actor_position_discontinuity"); break
    tracks = {str(t.get("track_id")): t for t in (pack or {}).get("tracks", [])}
    if not tracks: errors.append("pack_missing")
    if pack is not None and trace_dir is not None and trace.get("source_pack_sha256"):
        pack_file = trace_dir / "pack.json"
        if pack_file.is_file() and trace["source_pack_sha256"] != digest(pack_file): errors.append("source_pack_hash")
    for sample in samples:
        track = tracks.get(str(sample.get("track_id")))
        if track is None: errors.append("track_missing"); continue
        frames = track.get("frames", []); durations = [int(f.get("duration_ticks", 0)) for f in frames]; total = sum(durations)
        authored_tick = int(sample.get("authored_track_tick", -1))
        if total <= 0 or authored_tick < 0 or authored_tick >= total: errors.append("authored_tick_range"); continue
        frame_index = _frame_for_tick(durations, authored_tick); frame = frames[frame_index]
        if sample.get("frame_index") != frame_index: errors.append("pack_frame_mapping")
        if sample.get("duration_ticks") != durations[frame_index]: errors.append("pack_duration_binding")
        if sample.get("authored_loop_ticks") != total: errors.append("pack_duration_total")
        if not math.isclose(float(sample.get("track_derived_phase", -1)), float(authored_tick) / total, abs_tol=1e-6): errors.append("pack_phase_binding")
        if sample.get("source_frame_filename") != frame.get("filename"): errors.append("source_frame_filename")
        if sample.get("source_frame_sha256") != frame.get("source_sha256"): errors.append("source_frame_hash")
    captures = trace.get("captures", []); required = {"start", "first_cruise", "second_loop_cruise", "stop"}
    if {c.get("label") for c in captures} != required: errors.append("checkpoint_set")
    if any(not c.get("non_black") for c in captures): errors.append("black_capture")
    moving = [c for c in captures if c.get("label") in {"first_cruise", "second_loop_cruise"}]
    if len({c.get("actor_root_x") for c in moving}) < 2: errors.append("checkpoint_position_static")
    fields = {"semantic_tick", "actor_root_x", "track_id", "frame_index", "authored_track_tick", "track_derived_phase", "review_elapsed_usec", "source_pack_sha256", "source_frame_filename", "source_frame_sha256", "capture_sha256", "file", "non_black"}
    if any(not fields.issubset(c) for c in captures): errors.append("capture_metadata")
    if any(not c.get("capture_sha256") for c in captures): errors.append("capture_hash")
    return list(dict.fromkeys(errors))

def trace_guard(trace: dict, pack: dict | None = None, trace_dir: Path | None = None) -> str | None:
    errors = verify_positive(trace, pack, trace_dir); return errors[0] if errors else None

def negatives(trace: dict, pack: dict) -> dict[str, dict[str, object]]:
    baseline = copy.deepcopy(trace); assert not verify_positive(baseline, pack), verify_positive(baseline, pack)
    cases = {}
    mutations = (
        ("fixed_step_tick_drop", lambda t: t["samples"].pop(3), "semantic_tick_sequence"),
        ("fixed_step_tick_duplicate", lambda t: t["samples"].insert(3, copy.deepcopy(t["samples"][3])), "semantic_tick_sequence"),
        ("loop_recenter", lambda t: t["samples"].__setitem__(32, {**t["samples"][32], "actor_root_x": 0}), "actor_position_discontinuity"),
        ("hidden_root_reset", lambda t: t["samples"].__setitem__(32, {**t["samples"][32], "actor_root_x": 9999}), "actor_position_discontinuity"),
        ("pack_duration_mutation", lambda t: t["samples"].__setitem__(20, {**t["samples"][20], "duration_ticks": 99}), "pack_duration_binding"),
        ("capture_black", lambda t: t["captures"].__setitem__(0, {**t["captures"][0], "non_black": False}), "black_capture"),
    )
    for name, mutate, reason in mutations:
        mutated = copy.deepcopy(baseline); mutate(mutated); observed = trace_guard(mutated, pack)
        cases[name] = {"status": "failed", "reason": observed, "expected_reason": reason, "independent": observed == reason}
    altered_pack = copy.deepcopy(pack)
    target_track = next(t for t in altered_pack.get("tracks", []) if t.get("track_id") == "r06_playback_track_08")
    target_track["frames"][0]["duration_ticks"] = int(target_track["frames"][0].get("duration_ticks", 1)) + 1
    observed = trace_guard(baseline, altered_pack)
    cases["pack_source_duration_mutation"] = {"status": "failed", "reason": observed, "expected_reason": "pack_duration_binding", "independent": observed == "pack_duration_binding"}
    return cases

def main() -> int:
    path = Path(sys.argv[1]); pack_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    trace = json.loads(path.read_text(encoding="utf-8")); pack = json.loads(pack_path.read_text(encoding="utf-8")) if pack_path else None
    errors = verify_positive(trace, pack, pack_path.parent if pack_path else None)
    if errors: print(json.dumps({"status": "FAIL", "errors": errors}, indent=2)); return 1
    result = {"status": "PASS", "positive_trace": path.name, "negative_category": "scheduler/trace-verifier", "negative_matrix": negatives(trace, pack or {})}
    if not all(v["independent"] for v in result["negative_matrix"].values()): result["status"] = "FAIL"
    print(json.dumps(result, indent=2, sort_keys=True)); return 0 if result["status"] == "PASS" else 1

if __name__ == "__main__": raise SystemExit(main())
