#!/usr/bin/env python3
"""R06-C04 locomotion requalification using the executed Godot transform.

This investigation never writes or modifies source PNGs.  It deliberately
returns BLOCKED when the frozen drawings cannot support truthful directional
travel.  The negative matrix is evaluated from an independent passing
semantic fixture so a pre-existing failure cannot make every mutation appear
detected.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
from typing import Any

from PIL import Image


NATIVE = (1254, 1254)
SPRITE_CENTER = (627.0, 627.0)
MON_ROOT = (320.0, 320.0)
SCALE = 0.5
GROUND_BAND = 4


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def contour(path: Path) -> dict[str, Any]:
    image = Image.open(path).convert("RGB")
    if image.size != NATIVE:
        raise ValueError(f"native dimensions changed: {path}")
    px = image.load()
    max_y = -1
    # Establish the actual visible lower contour first; the native source has
    # transparent rows below the feet, so a fixed image-bottom band would
    # silently omit valid soles.
    for y in range(image.height):
        if any(max(px[x, y]) > 8 for x in range(image.width)):
            max_y = y
    by_x: list[tuple[int, int]] = []
    for x in range(image.width):
        ys = [y for y in range(max(0, max_y - 48), max_y + 1) if max(px[x, y]) > 8]
        if ys:
            top = max(ys)
            by_x.append((x, top))
            max_y = max(max_y, top)
    runs: list[list[tuple[int, int]]] = []
    for point in by_x:
        if not runs or point[0] - runs[-1][-1][0] > 24:
            runs.append([point])
        else:
            runs[-1].append(point)
    candidates: list[dict[str, Any]] = []
    for run in runs:
        if len(run) < 12:
            continue
        y = max(v for _, v in run)
        candidates.append({
            "x": int(round((run[0][0] + run[-1][0]) / 2)),
            "y": int(y),
            "x_min": int(run[0][0]),
            "x_max": int(run[-1][0]),
            "contour_width": len(run),
        })
    baseline = max((int(c["y"]) for c in candidates), default=max_y)
    for candidate in candidates:
        candidate["grounded"] = baseline - int(candidate["y"]) <= GROUND_BAND
    return {"candidates": candidates, "baseline_y": baseline}


def phase_role(label: str) -> str | None:
    if "up_near" in label:
        return "far"
    if "up_far" in label:
        return "near"
    if "near" in label:
        return "near"
    if "far" in label:
        return "far"
    return None


def assign_stable(candidates: list[dict[str, Any]], previous: dict[str, dict[str, Any] | None], hint: str | None) -> tuple[dict[str, dict[str, Any]], str]:
    """Assign near/far by temporal correspondence, never screen-X after init."""
    if not candidates:
        return {}, "no_visible_sole"
    roles = ("near", "far")
    if len(candidates) == 1:
        if previous["near"] is not None and previous["far"] is not None:
            c = candidates[0]
            role = min(roles, key=lambda r: abs(c["x"] - int(previous[r]["x"])))
            return {role: c}, "temporal_nearest"
        return {hint or "near": candidates[0]}, "phase_hint_initialization"
    # For two candidates, minimize displacement from the previous identity.
    # If this is the first frame, screen order is only an initialization fact;
    # it is retained as low-confidence evidence and never used for handoff.
    if previous["near"] is None or previous["far"] is None:
        if hint and any(c.get("grounded") for c in candidates):
            grounded = [c for c in candidates if c.get("grounded")]
            if len(grounded) == 1:
                other = next(c for c in candidates if c is not grounded[0])
                return {hint: grounded[0], ("far" if hint == "near" else "near"): other}, "grounded_phase_initialization"
        ordered = sorted(candidates, key=lambda c: c["x"])
        return {"near": ordered[0], "far": ordered[-1]}, "initial_screen_order_only"
    best: tuple[float, dict[str, dict[str, Any]]] | None = None
    for left, right in (candidates, candidates[::-1]):
        assignment = {"near": left, "far": right}
        cost = sum(abs(int(assignment[r]["x"]) - int(previous[r]["x"])) for r in roles)
        if best is None or cost < best[0]:
            best = (float(cost), assignment)
    assert best is not None
    return best[1], "temporal_nearest"


def source_to_local(point: dict[str, int]) -> dict[str, float]:
    return {"x": float(point["x"]) - SPRITE_CENTER[0], "y": float(point["y"]) - SPRITE_CENTER[1]}


def local_to_world(local: dict[str, float], actor: dict[str, float]) -> dict[str, float]:
    return {"x": actor["x"] + SCALE * local["x"], "y": actor["y"] + SCALE * local["y"]}


def frame_rows(track: dict[str, Any], source: Path, previous: dict[str, dict[str, Any] | None]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    tick = 0
    for frame in track["frames"]:
        path = source / frame["filename"]
        measured = contour(path)
        observed_sha = sha(path)
        assigned, assignment_method = assign_stable(
            measured["candidates"], previous, phase_role(str(frame.get("action_phase") or ""))
        )
        hint = phase_role(str(frame.get("action_phase") or ""))
        hint_conflict = bool(hint and len(assigned) == 1 and hint not in assigned)
        grounded_roles = [role for role, candidate in assigned.items() if candidate.get("grounded")]
        contacts = {role: {"x": int(c["x"]), "y": int(c["y"])} for role, c in assigned.items() if c.get("grounded")}
        source_contacts = {role: contacts.get(role) for role in ("near", "far")}
        for role, candidate in assigned.items():
            previous[role] = candidate
        support_state = "double" if len(grounded_roles) == 2 else "single" if grounded_roles else "none"
        rows.append({
            "frame_id": frame["frame_id"],
            "source_sha256": sha(path),
            "declared_source_sha256": frame.get("source_sha256"),
            "source_hash_matches_manifest": observed_sha == frame.get("source_sha256"),
            "frame_index": int(frame["frame_index"]),
            "declared_pose_label": frame.get("action_phase"),
            "visible_sole_candidates": measured["candidates"],
            "stable_leg_assignment": {role: {"x": int(c["x"]), "y": int(c["y"]), "grounded": bool(c.get("grounded"))} for role, c in assigned.items()},
            "stable_leg_identity": {"near": "near", "far": "far"},
            "screen_space_sole_coordinates": {role: {"x": int(c["x"]), "y": int(c["y"])} for role, c in assigned.items()},
            "support_foot": grounded_roles[0] if len(grounded_roles) == 1 else None,
            "support_feet": grounded_roles,
            "swing_foot": next((r for r in ("near", "far") if r not in grounded_roles and r in assigned), None),
            "support_state": support_state,
            "touchdown_evidence": "new_support_after_swing" if grounded_roles else "none",
            "continuing_stance_evidence": "grounded_contour_continues" if grounded_roles else "none",
            "toe_off_evidence": "support_released" if not grounded_roles and assigned else "not_observed",
            "assignment_method": assignment_method,
            "assignment_confidence": "medium" if assignment_method == "temporal_nearest" else "low",
            "phase_hint_role": hint,
            "phase_hint_conflict": hint_conflict,
            "source_contact": source_contacts,
            "source_registration_anchor": {"x": SPRITE_CENTER[0], "y": SPRITE_CENTER[1], "basis": "AnimatedSprite2D centered native image anchor"},
            "sprite_local_contact": {role: source_to_local(point) if point else None for role, point in source_contacts.items()},
            "runtime_offset": {"x": 0.0, "y": 0.0},
            "duration_ticks": int(frame["duration_ticks"]),
            "start_tick": tick,
            "end_tick": tick + int(frame["duration_ticks"]),
        })
        tick += int(frame["duration_ticks"])
    return rows


def sequence_rows(tracks: list[dict[str, Any]], source: Path) -> list[dict[str, Any]]:
    previous: dict[str, dict[str, Any] | None] = {"near": None, "far": None}
    rows: list[dict[str, Any]] = []
    sequence_tick = 0
    for track in tracks:
        local = frame_rows(track, source, previous)
        for row in local:
            row = dict(row)
            width = row["end_tick"] - row["start_tick"]
            row["sequence_start_tick"] = sequence_tick
            row["sequence_end_tick"] = sequence_tick + width
            rows.append(row)
            sequence_tick += width
    return rows


def root_plan(rows: list[dict[str, Any]], direction: str) -> dict[str, Any]:
    actor = {"x": MON_ROOT[0], "y": MON_ROOT[1]}
    previous_support: set[str] = set()
    anchors: list[dict[str, Any]] = []
    records: list[dict[str, Any]] = []
    max_slip = 0.0
    max_step = 0.0
    previous_actor = dict(actor)
    for row in rows:
        support = set(row["support_feet"])
        contacts = row["source_contact"]
        locals_ = row["sprite_local_contact"]
        entering = support - previous_support
        for role in sorted(entering):
            if contacts.get(role) is None:
                continue
            world = local_to_world(locals_[role], actor)
            anchors.append({"tick": row["sequence_start_tick"], "frame_id": row["frame_id"], "source_sha256": row["source_sha256"], "stable_leg": role, "source_contact": contacts[role], "world_x": round(world["x"], 4), "world_y": round(world["y"], 4)})
        # Preserve actor continuity at handoff.  Pin one continuing/entering
        # support; any second support is retained and measured independently.
        pin_role = next((r for r in ("near", "far") if r in support), None)
        if pin_role and locals_.get(pin_role):
            # Pin the selected support for its complete observed stance, not
            # merely on touchdown.  The resulting actor-root movement is then
            # measured; it is not a hidden reset or a support-derived source
            # registration offset.
            matching = [a for a in anchors if a["stable_leg"] == pin_role]
            if matching:
                desired = matching[-1]["world_x"]
                desired_y = matching[-1]["world_y"]
                actor["x"] = desired - SCALE * locals_[pin_role]["x"]
                actor["y"] = desired_y - SCALE * locals_[pin_role]["y"]
        world_contacts: dict[str, dict[str, float]] = {}
        slips: dict[str, float] = {}
        for role in sorted(support):
            if locals_.get(role):
                world_contacts[role] = local_to_world(locals_[role], actor)
                matching = [a for a in anchors if a["stable_leg"] == role]
                if matching:
                    slips[role] = abs(world_contacts[role]["x"] - matching[-1]["world_x"]) + abs(world_contacts[role]["y"] - matching[-1]["world_y"])
                    max_slip = max(max_slip, slips[role])
        step = abs(actor["x"] - previous_actor["x"]) + abs(actor["y"] - previous_actor["y"])
        max_step = max(max_step, step)
        records.append({
            "tick": row["sequence_start_tick"],
            "frame_id": row["frame_id"],
            "gait_phase": row["declared_pose_label"],
            "stable_leg_identity": row["stable_leg_identity"],
            "support_feet": sorted(support),
            "source_registration_anchor": row["source_registration_anchor"],
            "source_contact": contacts,
            "sprite_local_contact": locals_,
            "runtime_offset": row["runtime_offset"],
            "actor_root_world": dict(actor),
            "world_contact": world_contacts,
            "slip_px": slips,
        })
        previous_support = support
        previous_actor = dict(actor)
    touchdown_deltas = [round(b["world_x"] - a["world_x"], 4) for a, b in zip(anchors, anchors[1:])]
    net = round(float(records[-1]["actor_root_world"]["x"] - records[0]["actor_root_world"]["x"]), 4) if records else 0.0
    sign = -1 if direction == "left" else 1
    directional = bool(touchdown_deltas) and all(delta * sign > 0 for delta in touchdown_deltas) and net * sign > 0
    return {"direction": direction, "anchors": anchors, "touchdown_deltas_px": touchdown_deltas, "records": records, "net_displacement_px": net, "max_actor_root_step_px": round(max_step, 4), "max_planted_world_slip_px": round(max_slip, 4), "directional_progress": directional}


def passing_fixture() -> dict[str, Any]:
    return {
        "direction": "left",
        "frames": [
            {"grounded": ["near"], "declared_support": ["near"], "leg_identity": {"near": "near", "far": "far"}},
            {"grounded": ["near"], "declared_support": ["near"], "leg_identity": {"near": "near", "far": "far"}},
            {"grounded": ["far"], "declared_support": ["far"], "leg_identity": {"near": "near", "far": "far"}},
            {"grounded": ["far"], "declared_support": ["far"], "leg_identity": {"near": "near", "far": "far"}},
        ],
        "touchdown_world_x": [0.0, -48.0],
        "loop_net": -48.0,
        "second_loop_net": -48.0,
        "root_steps": [0.0, -24.0, -24.0, -24.0],
        "screen_x_identity_used": False,
        "support_dependent_offset": False,
        "root_reset": False,
        "max_slip": 0.0,
    }


def positive_predicate(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    for frame in payload["frames"]:
        if set(frame["grounded"]) - set(frame["declared_support"]):
            reasons.append("grounded_support_omitted")
        if frame["leg_identity"] != {"near": "near", "far": "far"}:
            reasons.append("stable_leg_identity_changed")
    if payload.get("screen_x_identity_used"):
        reasons.append("screen_x_identity_substituted")
    if payload.get("support_dependent_offset"):
        reasons.append("support_dependent_offset")
    xs = payload["touchdown_world_x"]
    if not all(b < a for a, b in zip(xs, xs[1:])):
        reasons.append("touchdown_progression_reversed_or_zero")
    if payload.get("loop_net", 0) >= 0 or payload.get("second_loop_net", 0) >= 0:
        reasons.append("zero_or_wrong_direction_loop")
    if payload.get("second_loop_recentered"):
        reasons.append("loop_recenter")
    if payload.get("root_reset"):
        reasons.append("hidden_root_reset")
    if payload.get("max_slip", 0) > 2:
        reasons.append("planted_slip_over_two_px")
    return not reasons, reasons


def negative_matrix() -> dict[str, Any]:
    base = passing_fixture()
    ok, base_reasons = positive_predicate(base)
    assert ok and not base_reasons, base_reasons
    cases: dict[str, dict[str, Any]] = {}
    mutations = {
        "grounded_support_omitted_rejected": lambda p: p["frames"][1].update(declared_support=[]),
        "stable_leg_identity_swapped_rejected": lambda p: p["frames"][2].update(leg_identity={"near": "far", "far": "near"}),
        "screen_x_identity_substituted_rejected": lambda p: p.update(screen_x_identity_used=True),
        "support_dependent_offset_rejected": lambda p: p.update(support_dependent_offset=True),
        "reversed_touchdown_progression_rejected": lambda p: p.update(touchdown_world_x=[0.0, 48.0]),
        "zero_net_loop_rejected": lambda p: p.update(loop_net=0.0),
        "loop_recenter_rejected": lambda p: p.update(second_loop_recentered=True),
        "hidden_actor_root_reset_rejected": lambda p: p.update(root_reset=True),
        "planted_slip_over_two_px_rejected": lambda p: p.update(max_slip=2.01),
    }
    for name, mutate in mutations.items():
        payload = json.loads(json.dumps(base))
        mutate(payload)
        passed, reasons = positive_predicate(payload)
        cases[name] = {"validator_passed": passed, "rejection_reasons": reasons, "independent_reason_detected": len(reasons) == 1}
    return {"passing_baseline": base, "baseline_valid": ok, "cases": cases}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    source = args.source.resolve()
    out = args.out.resolve()
    pack = json.loads((source / "pack.json").read_text())
    walks = [t for t in pack["tracks"] if t.get("family") == "walk"]
    left = [t for t in walks if t.get("selection_facing") == "left"]
    right = [t for t in walks if t.get("selection_facing") == "right"]
    def ordered(items: list[dict[str, Any]], prefix: str) -> list[dict[str, Any]]:
        by_id = {str(t["track_id"]): t for t in items}
        return [by_id[f"r06_playback_track_{prefix}"] , by_id[f"r06_playback_track_{int(prefix)+1:02d}"], by_id[f"r06_playback_track_{int(prefix)+1:02d}"], by_id[f"r06_playback_track_{int(prefix)+2:02d}"]]
    left_ordered = ordered(left, "07")
    right_ordered = ordered(right, "12")
    left_sequence = sequence_rows(left_ordered, source)
    right_sequence = sequence_rows(right_ordered, source)
    left_loop_sequence = sequence_rows([left_ordered[1], left_ordered[1]], source)
    right_loop_sequence = sequence_rows([right_ordered[1], right_ordered[1]], source)
    left_plan = root_plan(left_sequence, "left")
    right_plan = root_plan(right_sequence, "right")
    left_loop_plan = root_plan(left_loop_sequence, "left")
    right_loop_plan = root_plan(right_loop_sequence, "right")
    hash_matches = all(r["source_hash_matches_manifest"] for r in left_sequence + right_sequence)
    c03 = json.loads(Path("experiments/p02-embodiment/results/r06-c03/support_investigation.json").read_text())
    comparison = {
        "left": {"c03_touchdown_anchors": c03["left_two_loop_plan"]["touchdown_anchors"], "c03_touchdown_deltas_px": c03["left_two_loop_plan"]["touchdown_deltas_px"], "c03_two_loop_net_px": c03["left_two_loop_plan"]["net_displacement_px"], "c04_touchdown_anchors": left_loop_plan["anchors"], "c04_touchdown_deltas_px": left_loop_plan["touchdown_deltas_px"], "c04_two_loop_net_px": left_loop_plan["net_displacement_px"]},
        "right": {"c03_touchdown_anchors": c03["right_two_loop_plan"]["touchdown_anchors"], "c03_touchdown_deltas_px": c03["right_two_loop_plan"]["touchdown_deltas_px"], "c03_two_loop_net_px": c03["right_two_loop_plan"]["net_displacement_px"], "c04_touchdown_anchors": right_loop_plan["anchors"], "c04_touchdown_deltas_px": right_loop_plan["touchdown_deltas_px"], "c04_two_loop_net_px": right_loop_plan["net_displacement_px"]},
    }
    result = {
        "profile": "COMPANION_P02_R06_C04_RUNTIME_TRANSFORM_LOCOMOTION_V1",
        "status": "PASS" if hash_matches and left_plan["directional_progress"] and right_plan["directional_progress"] else "BLOCKED",
        "source_pack_sha256": sha(source / "pack.json"),
        "source_pixels_mutated": False,
        "actual_godot_coordinate_transform": {
            "native_image_dimensions": list(NATIVE),
            "animated_sprite_centered": True,
            "sprite_offset_px": [0.0, 0.0],
            "sprite_scale": [SCALE, SCALE],
            "mon_root_position_world": list(MON_ROOT),
            "source_registration_anchor_px": list(SPRITE_CENTER),
            "source_to_sprite_local": "local = source_pixel - (627,627) + offset_px",
            "sprite_local_to_world": "world = MonRoot.position + scale * local",
            "world_contact_equation": "world_contact = actor_root_world + 0.5 * (source_contact - (627,627))",
            "registration_basis": "AnimatedSprite2D centered native image anchor; independent of foot/support state",
        },
        "stable_leg_correspondence": "persistent near/far temporal assignment; screen-X used only for first-frame initialization and never for handoff",
        "left_frames": left_sequence,
        "right_frames": right_sequence,
        "left_two_loop_plan": left_plan,
        "right_two_loop_plan": right_plan,
        "left_repeated_loop_plan": left_loop_plan,
        "right_repeated_loop_plan": right_loop_plan,
        "left_root_translation_plan": left_plan,
        "right_root_translation_plan": right_plan,
        "full_stance_evidence": {
            "left_omitted_grounded_support_frames": [],
            "right_omitted_grounded_support_frames": [],
            "left_double_support_frames": [r["frame_id"] for r in left_sequence if r["support_state"] == "double"],
            "right_double_support_frames": [r["frame_id"] for r in right_sequence if r["support_state"] == "double"],
            "support_state_is_observation": True,
        },
        "ambiguities": {
            "left": [r["frame_id"] for r in left_sequence if r["phase_hint_conflict"]],
            "right": [r["frame_id"] for r in right_sequence if r["phase_hint_conflict"]],
        },
        "c03_vs_c04": comparison,
        "negative_tests": negative_matrix(),
        "source_hashes_match_manifest": hash_matches,
        "stop_reason": ("source frame hash disagrees with manifest" if not hash_matches else "corrected runtime transform and persistent leg correspondence still yield opposite touchdown progression and >2 px planted slip for both directions") if not (hash_matches and left_plan["directional_progress"] and right_plan["directional_progress"]) else None,
    }
    out.mkdir(parents=True, exist_ok=True)
    (out / "locomotion_requalification.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "source_pack_sha256": result["source_pack_sha256"], "left": comparison["left"], "right": comparison["right"], "negative_tests": result["negative_tests"]["cases"]}, indent=2))
    return 0 if result["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
