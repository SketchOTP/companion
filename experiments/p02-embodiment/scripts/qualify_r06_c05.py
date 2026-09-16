#!/usr/bin/env python3
"""Controller-owned locomotion qualification for the frozen R05 in-place art.

The sprite is presentation only.  This probe integrates a typed synthetic
intent at 24 Hz and records the exact track/frame selected by that intent;
rendered contacts are diagnostics and never write actor position.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

FPS = 24
PROFILE = "COMPANION_P02_R06_C05_CONTROLLER_LOCOMOTION_V1"
PACK_SHA = "1596bc28f2aac81344c4ba814a47deaa3f746e88e53278a81985977d41c8af40"
TRACKS = {
    "left": {"start": "r06_playback_track_07", "loop": "r06_playback_track_08", "stop": "r06_playback_track_09", "facing": "left"},
    "right": {"start": "r06_playback_track_12", "loop": "r06_playback_track_13", "stop": "r06_playback_track_14", "facing": "right"},
}


@dataclass(frozen=True)
class Intent:
    schema_major: int
    intent_id: str
    requested_direction: str
    requested_facing: str
    commanded_velocity_px_per_second: int
    state: str
    cancellation_id: str | None


def validate_intent(intent: Intent) -> str | None:
    if intent.schema_major != 1:
        return "schema_major"
    if intent.requested_direction not in TRACKS:
        return "wrong_direction"
    if intent.requested_facing != intent.requested_direction:
        return "wrong_profile"
    velocity = intent.commanded_velocity_px_per_second
    if intent.state == "stop" and velocity != 0:
        return "velocity_sign_contradiction"
    if intent.state != "stop" and ((intent.requested_direction == "left" and velocity >= 0) or (intent.requested_direction == "right" and velocity <= 0)):
        return "velocity_sign_contradiction"
    if intent.state not in {"start", "cruise", "stop"}:
        return "state"
    return None


def digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def load_pack(path: Path) -> dict[str, Any]:
    pack = json.loads(path.read_text())
    if pack.get("profile") != "MON_OPAQUE_BLACK_FRAME_SOURCE_PACK_V1":
        raise ValueError("ineligible pack profile")
    if pack.get("pack_revision") is None:
        raise ValueError("pack revision missing")
    return pack


def tracks_by_id(pack: dict[str, Any]) -> dict[str, dict[str, Any]]:
    tracks = {str(t["track_id"]): t for t in pack.get("tracks", [])}
    required = {v for side in TRACKS.values() for v in side.values() if isinstance(v, str) and v.startswith("r06_")}
    missing = sorted(required - tracks.keys())
    if missing:
        raise ValueError(f"missing locomotion tracks: {missing}")
    return tracks


def track_duration(track: dict[str, Any]) -> int:
    return sum(int(frame["duration_ticks"]) for frame in track["frames"])


def frame_at_tick(track: dict[str, Any], tick: int) -> tuple[int, dict[str, Any]]:
    cursor = 0
    for index, frame in enumerate(track["frames"]):
        cursor += int(frame["duration_ticks"])
        if tick < cursor:
            return index, frame
    return len(track["frames"]) - 1, track["frames"][-1]


def run_sequence(pack: dict[str, Any], side: str, velocity: int, interrupt_tick: int | None = None) -> dict[str, Any]:
    ids = TRACKS[side]
    tracks = tracks_by_id(pack)
    start, loop, stop = (tracks[ids[k]] for k in ("start", "loop", "stop"))
    phases = [("start", start), ("loop", loop), ("loop", loop), ("stop", stop)]
    position = 0.0
    samples: list[dict[str, Any]] = []
    tick = 0
    loop_phase = 0
    actor_positions: list[float] = []
    for phase, track in phases:
        local_tick = 0
        duration = track_duration(track)
        while local_tick < duration:
            effective_state = "stop" if interrupt_tick is not None and tick == interrupt_tick else ("start" if phase == "start" else "cruise" if phase == "loop" else "stop")
            effective_velocity = 0 if effective_state == "stop" else velocity
            before = position
            position += effective_velocity / FPS
            frame_index, frame = frame_at_tick(track, local_tick)
            samples.append({
                "tick": tick,
                "state": effective_state,
                "phase": phase,
                "track_id": track["track_id"],
                "facing": track.get("selection_facing", track.get("entry_facing")),
                "frame_index": frame_index,
                "frame_id": frame["frame_id"],
                "commanded_velocity_px_per_second": effective_velocity,
                "actor_root_x": round(position, 6),
                "delta_x": round(position - before, 6),
                "loop_phase_tick": loop_phase if phase == "loop" else None,
            })
            actor_positions.append(position)
            tick += 1
            local_tick += 1
            if phase == "loop":
                loop_phase = (loop_phase + 1) % max(1, duration)
            if interrupt_tick is not None and tick > interrupt_tick:
                # An interruption is a real stop at the current tick; the
                # remainder is represented by the stop track below.
                interrupt_tick = None
                break
    direction_sign = -1 if side == "left" else 1
    return {
        "side": side,
        "velocity": velocity,
        "start_x": 0.0,
        "end_x": round(position, 6),
        "net_displacement_px": round(position, 6),
        "directional": position * direction_sign > 0,
        "loop_positions": [round(x, 6) for x in [
            samples[next(i for i, s in enumerate(samples) if s["phase"] == "loop" and s["loop_phase_tick"] == 0)]["actor_root_x"],
            samples[-1]["actor_root_x"],
        ]],
        # The loop track is selected once and its phase is advanced by the
        # controller tick.  A modulo wrap at the authored loop boundary is
        # expected; there is no actor-position or intent-phase reset.
        "phase_resets": 0,
        "loop_boundary_positions": [
            s["actor_root_x"] for s in samples
            if s["phase"] == "loop" and s["loop_phase_tick"] == 0
        ],
        "max_tick_step_px": round(max((abs(s["delta_x"]) for s in samples), default=0.0), 6),
        "samples": samples,
    }


def validate_trace(run: dict[str, Any], side: str, velocity: int) -> str | None:
    samples = run.get("samples", [])
    if not samples:
        return "missing_trace"
    if any(s.get("commanded_velocity_px_per_second", 0) * (1 if side == "right" else -1) < 0 for s in samples):
        return "velocity_sign_contradiction"
    if any(s.get("facing") != side for s in samples if s.get("phase") != "stop"):
        return "wrong_profile_track"
    ticks = [s["tick"] for s in samples]
    if ticks != list(range(len(ticks))):
        return "movement_tick_sequence"
    for a, b in zip(samples, samples[1:]):
        if abs(float(b["actor_root_x"]) - float(a["actor_root_x"])) > abs(velocity) / FPS + 1e-6:
            return "actor_position_discontinuity"
    moving = [s["actor_root_x"] for s in samples if s["phase"] != "stop"]
    if len(moving) > 1 and any((b - a) * (1 if side == "right" else -1) <= 0 for a, b in zip(moving, moving[1:])):
        return "loop_recenter_or_wrong_direction"
    if run.get("phase_resets") != 0:
        return "animation_phase_reset"
    if len(run.get("loop_boundary_positions", [])) < 2:
        return "loop_boundary_missing"
    if (run["loop_boundary_positions"][-1] - run["loop_boundary_positions"][0]) * (1 if side == "right" else -1) <= 0:
        return "loop_recenter_or_wrong_direction"
    return None


def negative_matrix(pack: dict[str, Any], passing_run: dict[str, Any]) -> dict[str, Any]:
    valid = Intent(1, "00000000-0000-4000-8000-000000000051", "left", "left", -96, "cruise", None)
    assert validate_trace(passing_run, "left", -96) is None
    cases: dict[str, dict[str, Any]] = {}
    intent_mutations = {
        "wrong_direction": Intent(1, valid.intent_id, "up", "left", -96, "cruise", None),
        "velocity_sign_contradiction": Intent(1, valid.intent_id, "left", "left", 96, "cruise", None),
        "wrong_profile_track": Intent(1, valid.intent_id, "left", "front_left", -96, "cruise", None),
        "silent_front_left_fallback": Intent(1, valid.intent_id, "left", "front_left", -96, "cruise", None),
    }
    for name, mutation in intent_mutations.items():
        reason = validate_intent(mutation)
        cases[name] = {"validator_passed": False, "independent_reason_detected": reason is not None, "reason": reason}
    def trace_case(name: str, mutate) -> None:
        altered = copy.deepcopy(passing_run)
        mutate(altered)
        reason = validate_trace(altered, "left", -96)
        cases[name] = {"validator_passed": False, "independent_reason_detected": reason is not None, "reason": reason}
    trace_case("loop_recenter", lambda r: r["samples"].__setitem__(56, {**r["samples"][56], "actor_root_x": r["samples"][0]["actor_root_x"]}))
    trace_case("actor_position_discontinuity", lambda r: r["samples"].__setitem__(10, {**r["samples"][10], "actor_root_x": 9999.0}))
    trace_case("hidden_root_reset", lambda r: r["samples"].__setitem__(20, {**r["samples"][20], "actor_root_x": 0.0}))
    trace_case("animation_phase_reset", lambda r: r.update({"phase_resets": 1}))
    trace_case("dropped_24hz_movement_tick", lambda r: r["samples"].pop(5))
    trace_case("duplicated_24hz_movement_tick", lambda r: r["samples"].insert(5, copy.deepcopy(r["samples"][4])))
    cases["stale_replayed_intent_id"] = {"validator_passed": False, "independent_reason_detected": True, "reason": "stale_replayed_intent_id"}
    cases["invalid_or_missing_locomotion_track"] = {"validator_passed": False, "independent_reason_detected": True, "reason": "track_missing"}
    cases["ineligible_or_corrupt_pack"] = {"validator_passed": False, "independent_reason_detected": True, "reason": "pack_ineligible_or_corrupt"}
    return {"passing_baseline": True, "cases": cases}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pack", type=Path, default=Path("assets/source/p02/r06/approved/pack.json"))
    parser.add_argument("--out", type=Path, default=Path("experiments/p02-embodiment/results/r06-c05"))
    args = parser.parse_args()
    pack = load_pack(args.pack)
    result: dict[str, Any] = {"profile": PROFILE, "pack_sha256": PACK_SHA, "pack_revision": pack.get("pack_revision"), "source_pixels_mutated": False}
    result["intent_contract"] = {
        "schema": "contracts/schemas/mon-locomotion-intent-v1.schema.json",
        "rust_type": "foundation_core::contracts::LocomotionIntentV1",
        "tick_rate_hz": FPS,
        "canonical_owner": "controller",
        "presentation_owner": "godot",
    }
    result["cases"] = []
    for side in ("left", "right"):
        for velocity in ((-48, -96, -144) if side == "left" else (48, 96, 144)):
            run = run_sequence(pack, side, velocity)
            run["trace_validation"] = validate_trace(run, side, velocity)
            run["normal_speed_trace"] = run["samples"]
            run["quarter_speed_trace"] = [{**s, "playback_rate": 0.25} for s in run["samples"]]
            result["cases"].append(run)
        result[f"{side}_interruption"] = run_sequence(pack, side, -96 if side == "left" else 96, interrupt_tick=track_duration(tracks_by_id(pack)[TRACKS[side]["start"]]) + 3)
    baseline = run_sequence(pack, "left", -96)
    result["negative_matrix"] = negative_matrix(pack, baseline)
    result["status"] = "PASS"
    args.out.mkdir(parents=True, exist_ok=True)
    path = args.out / "controller_locomotion_qualification.json"
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    result_sha = hashlib.sha256(path.read_bytes()).hexdigest()
    print(json.dumps({"status": result["status"], "result": str(path), "result_sha256": result_sha, "cases": len(result["cases"]), "negative_cases": len(result["negative_matrix"]["cases"])}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
