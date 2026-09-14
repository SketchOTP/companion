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

def _rebind_sample_from_cursor(sample: dict, track: dict, cursor: float) -> None:
    """Keep a mutation individually valid against the pack, but not sequentially valid."""
    frames = track.get("frames", [])
    durations = [int(f.get("duration_ticks", 0)) for f in frames]
    total = sum(durations)
    cursor = cursor % total
    authored_tick = int(math.floor(cursor)) % total
    frame_index = _frame_for_tick(durations, authored_tick)
    frame = frames[frame_index]
    sample["authored_tick_cursor"] = cursor
    sample["authored_track_tick"] = authored_tick
    sample["frame_index"] = frame_index
    sample["duration_ticks"] = durations[frame_index]
    sample["authored_loop_ticks"] = total
    sample["track_derived_phase"] = cursor / float(total)
    sample["source_frame_filename"] = frame.get("filename")
    sample["source_frame_sha256"] = frame.get("source_sha256")

def _check_authored_progression(samples: list[dict], tracks: dict[str, dict]) -> list[str]:
    """Verify adjacent cruise samples against the loaded track's duration clock."""
    errors: list[str] = []
    cruise = [s for s in samples if s.get("phase") == "cruise"]
    if not cruise:
        return ["cruise_samples_missing"]
    previous = None
    seam_count = 0
    for sample in cruise:
        track = tracks.get(str(sample.get("track_id")))
        if track is None:
            continue
        durations = [int(f.get("duration_ticks", 0)) for f in track.get("frames", [])]
        total = sum(durations)
        cursor = sample.get("authored_tick_cursor")
        rate = sample.get("playback_rate")
        if total <= 0 or not isinstance(cursor, (int, float)) or not isinstance(rate, (int, float)):
            errors.append("authored_progression")
            break
        if previous is not None:
            prev_cursor, prev_rate, prev_total = previous
            if prev_total != total or not math.isclose(float(rate), float(prev_rate), abs_tol=1e-9):
                errors.append("authored_progression")
                break
            expected = (float(prev_cursor) + float(rate)) % float(total)
            actual = float(cursor) % float(total)
            if actual == 0.0 and float(prev_cursor) > 0.0 and not math.isclose(expected, 0.0, abs_tol=1e-6):
                errors.append("authored_phase_reset")
                break
            if float(cursor) < float(prev_cursor):
                seam_count += 1
            if not math.isclose(actual, expected, abs_tol=1e-6):
                errors.append("authored_progression")
                break
        previous = (float(cursor), float(rate), total)
    if len(cruise) >= 33 and seam_count < 1:
        errors.append("authored_seam")
    return errors

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
        cursor = sample.get("authored_tick_cursor")
        expected_phase = (float(cursor) % total) / float(total) if isinstance(cursor, (int, float)) else -1.0
        if not math.isclose(float(sample.get("track_derived_phase", -1)), expected_phase, abs_tol=1e-6): errors.append("pack_phase_binding")
        if sample.get("source_frame_filename") != frame.get("filename"): errors.append("source_frame_filename")
        if sample.get("source_frame_sha256") != frame.get("source_sha256"): errors.append("source_frame_hash")
    errors.extend(_check_authored_progression(samples, tracks))
    captures = trace.get("captures", []); required = {"start", "first_cruise", "second_loop_cruise", "stop"}
    if {c.get("label") for c in captures} != required: errors.append("checkpoint_set")
    if any(not c.get("non_black") for c in captures): errors.append("black_capture")
    moving = [c for c in captures if c.get("label") in {"first_cruise", "second_loop_cruise"}]
    if len({c.get("actor_root_x") for c in moving}) < 2: errors.append("checkpoint_position_static")
    fields = {"capture_index", "semantic_tick", "actor_root_x", "track_id", "frame_index", "authored_track_tick", "authored_tick_cursor", "authored_loop_ticks", "track_derived_phase", "review_observed_elapsed_usec", "review_elapsed_usec", "source_pack_sha256", "source_frame_filename", "source_frame_sha256", "capture_sha256", "file", "non_black"}
    if any(not fields.issubset(c) for c in captures): errors.append("capture_metadata")
    if [c.get("capture_index") for c in captures] != list(range(len(captures))): errors.append("capture_index_sequence")
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
    target_sample = next(s for s in baseline["samples"] if s.get("phase") == "cruise")
    target_track = next(t for t in altered_pack.get("tracks", []) if t.get("track_id") == target_sample.get("track_id"))
    target_frame = target_track["frames"][int(target_sample.get("frame_index", 0))]
    target_frame["duration_ticks"] = int(target_frame.get("duration_ticks", 1)) + 17
    observed = trace_guard(baseline, altered_pack)
    cases["pack_source_duration_mutation"] = {"status": "failed", "reason": observed, "expected_reason": "pack_duration_binding", "independent": observed == "pack_duration_binding"}
    cruise_indices = [i for i, s in enumerate(baseline["samples"]) if s.get("phase") == "cruise"]
    if len(cruise_indices) >= 9:
        jump = copy.deepcopy(baseline)
        jump_index = cruise_indices[8]
        jump_track = next(t for t in pack.get("tracks", []) if t.get("track_id") == jump["samples"][jump_index].get("track_id"))
        previous_cursor = float(jump["samples"][cruise_indices[7]].get("authored_tick_cursor", 0.0))
        rate = float(jump["samples"][jump_index].get("playback_rate", 1.0))
        _rebind_sample_from_cursor(jump["samples"][jump_index], jump_track, previous_cursor + rate + 2.0)
        observed = trace_guard(jump, pack)
        cases["pack_valid_sequential_jump"] = {"status": "failed", "reason": observed, "expected_reason": "authored_progression", "independent": observed == "authored_progression"}
        reset = copy.deepcopy(baseline)
        reset_index = cruise_indices[8]
        reset_track = next(t for t in pack.get("tracks", []) if t.get("track_id") == reset["samples"][reset_index].get("track_id"))
        _rebind_sample_from_cursor(reset["samples"][reset_index], reset_track, 0.0)
        observed = trace_guard(reset, pack)
        cases["unexpected_phase_reset"] = {"status": "failed", "reason": observed, "expected_reason": "authored_phase_reset", "independent": observed == "authored_phase_reset"}
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
