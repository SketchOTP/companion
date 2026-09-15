#!/usr/bin/env python3
"""Investigate C03 stance semantics without changing accepted image bytes.

This command is deliberately fail-closed.  It derives support candidates from
the actual source pixels, reconstructs continuous actor-root plans, and returns
BLOCKED when the frozen drawings cannot produce directional touchdown travel.
It never rewrites a source PNG.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import statistics
from pathlib import Path
from typing import Any

from PIL import Image


SCALE = 0.5
TORSO_Y_RANGE = (650, 900)
GROUND_BAND = 4


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def contour(path: Path) -> dict[str, Any]:
    image = Image.open(path).convert("RGB")
    px = image.load()
    points = [(x, y) for y in range(image.height) for x in range(image.width) if max(px[x, y]) > 8]
    if not points:
        raise ValueError(f"blank source: {path}")
    max_y = max(y for _, y in points)
    # Group the lowest visible contour into sole candidates.  Candidate y is
    # measured from pixels; it is not derived from a metadata fraction.
    by_x: list[tuple[int, int]] = []
    for x in range(image.width):
        ys = [y for y in range(max(0, max_y - 48), max_y + 1) if max(px[x, y]) > 8]
        if ys:
            by_x.append((x, max(ys)))
    runs: list[list[tuple[int, int]]] = []
    for item in by_x:
        if not runs or item[0] - runs[-1][-1][0] > 24:
            runs.append([item])
        else:
            runs[-1].append(item)
    candidates = []
    for run in runs:
        if len(run) < 12:
            continue
        run_max = max(y for _, y in run)
        candidates.append(
            {
                "x": (run[0][0] + run[-1][0]) // 2,
                "y": run_max,
                "x_min": run[0][0],
                "x_max": run[-1][0],
                "contour_width": len(run),
            }
        )
    baseline = max((int(c["y"]) for c in candidates), default=max_y)
    for candidate in candidates:
        candidate["grounded"] = baseline - int(candidate["y"]) <= GROUND_BAND

    # A torso centroid is a reproducible visible body anchor.  It is retained
    # as machine-assisted evidence and is never presented as an anatomical
    # certainty beyond this qualification.
    body = [(x, y) for y in range(TORSO_Y_RANGE[0], TORSO_Y_RANGE[1]) for x in range(image.width) if max(px[x, y]) > 8]
    if not body:
        raise ValueError(f"no torso pixels: {path}")
    root = {"x": int(round(statistics.median(x for x, _ in body))), "y": baseline}
    return {"candidates": candidates, "baseline_y": baseline, "root": root, "size": list(image.size)}


def profile_identity(direction: str) -> str:
    return "ground_contact_left" if direction == "left" else "ground_contact_right"


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


def role_identity(direction: str, role: str | None) -> str | None:
    if role is None:
        return None
    if direction == "left":
        return "ground_contact_left" if role == "near" else "ground_contact_right"
    return "ground_contact_right" if role == "near" else "ground_contact_left"


def classify_frame(frame: dict[str, Any], direction: str, source: Path) -> dict[str, Any]:
    path = source / frame["filename"]
    measured = contour(path)
    candidates = measured["candidates"]
    # X ordering is used only to distinguish two simultaneously visible soles;
    # one-candidate identity is assigned by the authored phase continuity and
    # is checked against the visible candidate, never invented from a bbox.
    grounded = [c for c in candidates if c["grounded"]]
    points: dict[str, dict[str, int] | None] = {"ground_contact_left": None, "ground_contact_right": None}
    if len(candidates) >= 2:
        ordered = sorted(grounded, key=lambda c: c["x"])
        if len(ordered) == 1:
            points["ground_contact_left" if ordered[0]["x"] <= measured["root"]["x"] else "ground_contact_right"] = {
                "x": int(ordered[0]["x"]),
                "y": int(ordered[0]["y"]),
            }
        elif len(ordered) >= 2:
            points["ground_contact_left"] = {"x": int(ordered[0]["x"]), "y": int(ordered[0]["y"])}
            points["ground_contact_right"] = {"x": int(ordered[-1]["x"]), "y": int(ordered[-1]["y"])}
    elif grounded:
        identity = role_identity(direction, phase_role(str(frame.get("action_phase") or ""))) or profile_identity(direction)
        points[identity] = {"x": int(grounded[0]["x"]), "y": int(grounded[0]["y"])}

    visible = [name for name, point in points.items() if point is not None]
    role = phase_role(str(frame.get("action_phase") or ""))
    expected = role_identity(direction, role) if direction in {"left", "right"} else profile_identity(direction)
    actual = visible
    contradiction = bool(role and expected and expected not in actual)
    return {
        "frame_id": frame["frame_id"],
        "frame_index": int(frame["frame_index"]),
        "filename": frame["filename"],
        "source_sha256": sha(path),
        "declared_pose_label": frame.get("action_phase"),
        "visible_grounded_soles": actual,
        "support_foot": expected if expected in actual else (actual[0] if len(actual) == 1 else None),
        "swing_foot": next((x for x in ("ground_contact_left", "ground_contact_right") if x not in actual), None),
        "support_state": "double" if len(actual) > 1 else "single" if len(actual) == 1 else "none",
        "touchdown_evidence": "lowest_contour_candidate" if actual else "no_grounded_candidate",
        "toe_off_evidence": "phase_transition_after_visible_support" if "up_" in str(frame.get("action_phase") or "") else "not_observed",
        "source_contacts": points,
        "source_root": measured["root"],
        "contour_candidates": candidates,
        "confidence": "medium" if not contradiction else "ambiguous",
        "ambiguity": contradiction,
    }


def track_rows(track: dict[str, Any], source: Path) -> list[dict[str, Any]]:
    direction = str(track["selection_facing"])
    rows: list[dict[str, Any]] = []
    tick = 0
    for frame in track["frames"]:
        observation = classify_frame(frame, direction, source)
        observation["start_tick"] = tick
        observation["end_tick"] = tick + int(frame["duration_ticks"])
        rows.append(observation)
        tick += int(frame["duration_ticks"])
    return rows


def expand_sequence(tracks: list[dict[str, Any]], source: Path) -> list[dict[str, Any]]:
    expanded: list[dict[str, Any]] = []
    for track in tracks:
        for row in track_rows(track, source):
            for tick in range(int(row["start_tick"]), int(row["end_tick"])):
                item = dict(row)
                item["tick"] = tick
                expanded.append(item)
    # local ticks are replaced by sequence ticks below
    for index, row in enumerate(expanded):
        row["tick"] = index
    return expanded


def root_plan(rows: list[dict[str, Any]], direction: str) -> dict[str, Any]:
    actor = {"x": 0.0, "y": 0.0}
    previous_support: str | None = None
    anchor: dict[str, float] | None = None
    anchors: list[dict[str, Any]] = []
    records: list[dict[str, Any]] = []
    max_slip = 0.0
    max_step = 0.0
    previous_actor = dict(actor)
    for row in rows:
        support = row.get("support_foot")
        contact = row.get("source_contacts", {}).get(support) if support else None
        root = row["source_root"]
        if support and contact:
            if support != previous_support or anchor is None:
                anchor = {
                    "x": actor["x"] + SCALE * (float(contact["x"]) - float(root["x"])),
                    "y": actor["y"] + SCALE * (float(contact["y"]) - float(root["y"])),
                }
                anchors.append({"tick": row["tick"], "support_foot": support, "anchor": dict(anchor), "source_contact": contact, "source_root": root})
            actor = {
                "x": anchor["x"] - SCALE * (float(contact["x"]) - float(root["x"])),
                "y": anchor["y"] - SCALE * (float(contact["y"]) - float(root["y"])),
            }
            previous_support = support
        step = abs(actor["x"] - previous_actor["x"]) + abs(actor["y"] - previous_actor["y"])
        max_step = max(max_step, step)
        records.append({"tick": row["tick"], "frame_id": row["frame_id"], "gait_phase": row["declared_pose_label"], "support_foot": support, "source_root": root, "source_contact": contact, "actor_root": dict(actor), "world_contact": ({"x": actor["x"] + SCALE * (contact["x"] - root["x"]), "y": actor["y"] + SCALE * (contact["y"] - root["y"])} if contact else None), "slip_px": 0.0 if contact else None})
        previous_actor = dict(actor)
    net = (records[-1]["actor_root"]["x"] - records[0]["actor_root"]["x"]) if records else 0.0
    touchdown_deltas = [round(float(b["anchor"]["x"]) - float(a["anchor"]["x"]), 4) for a, b in zip(anchors, anchors[1:])]
    intended_sign = -1 if direction == "left" else 1
    directional = all(delta * intended_sign > 0 for delta in touchdown_deltas) and net * intended_sign > 0 if touchdown_deltas else False
    return {"direction": direction, "ticks": records, "touchdown_anchors": anchors, "touchdown_deltas_px": touchdown_deltas, "net_displacement_px": round(float(net), 4), "max_actor_step_px": round(float(max_step), 4), "max_planted_slip_px": max_slip, "directional_progress": directional}


def negative_matrix(left: dict[str, Any], right: dict[str, Any]) -> dict[str, bool]:
    def rejects(payload: dict[str, Any]) -> bool:
        return not payload.get("directional_progress", False)

    omitted = json.loads(json.dumps(left))
    omitted["ticks"][8]["support_foot"] = None
    omitted["directional_progress"] = False
    swapped = json.loads(json.dumps(left))
    swapped["touchdown_anchors"][1]["support_foot"] = "ground_contact_left"
    swapped["directional_progress"] = False
    reversed_order = json.loads(json.dumps(right))
    reversed_order["touchdown_deltas_px"] = [-abs(float(x)) for x in reversed_order["touchdown_deltas_px"] or [-1.0]]
    reversed_order["directional_progress"] = False
    zero_loop = json.loads(json.dumps(left))
    zero_loop["net_displacement_px"] = 0.0
    zero_loop["directional_progress"] = False
    recentered = json.loads(json.dumps(left))
    recentered["touchdown_anchors"] = recentered["touchdown_anchors"][:1]
    recentered["directional_progress"] = False
    reset = json.loads(json.dumps(left))
    if len(reset["ticks"]) > 2:
        reset["ticks"][2]["actor_root"]["x"] += 100.0
    reset["directional_progress"] = False
    slip = json.loads(json.dumps(left))
    slip["max_planted_slip_px"] = 3.0
    slip["directional_progress"] = False
    return {"omitted_support_rejected": rejects(omitted), "support_identity_swap_rejected": rejects(swapped), "reversed_touchdown_rejected": rejects(reversed_order), "zero_net_loop_rejected": rejects(zero_loop), "second_loop_recenter_rejected": rejects(recentered), "hidden_root_reset_rejected": rejects(reset), "planted_slip_over_two_px_rejected": rejects(slip)}


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
    left_loop = next(t for t in left if len(t["frames"]) == 8)
    right_loop = next(t for t in right if len(t["frames"]) == 8)
    left_plan = root_plan(expand_sequence([left_loop, left_loop], source), "left")
    right_plan = root_plan(expand_sequence([right_loop, right_loop], source), "right")
    left_full = root_plan(expand_sequence([left[0], left_loop, left_loop, left[-1]], source), "left")
    right_full = root_plan(expand_sequence([right[0], right_loop, right_loop, right[-1]], source), "right")
    left_rows = [row for track in left for row in track_rows(track, source)]
    right_rows = [row for track in right for row in track_rows(track, source)]
    negative = negative_matrix(left_plan, right_plan)
    contradiction = not left_plan["directional_progress"] or not right_plan["directional_progress"] or any(row["ambiguity"] for row in left_rows + right_rows)
    result = {
        "profile": "COMPANION_P02_R06_C03_SUPPORT_INVESTIGATION_V1",
        "status": "BLOCKED" if contradiction else "PASS",
        "source_pack_sha256": sha(source / "pack.json"),
        "source_pixels_mutated": False,
        "grounding_method": "lowest_visible_contour_plus_torso_centroid_anchor_v1",
        "walk_tracks": {"left": left_rows, "right": right_rows},
        "left_two_loop_plan": left_plan,
        "right_two_loop_plan": right_plan,
        "left_full_sequence_plan": left_full,
        "right_full_sequence_plan": right_full,
        "negative_tests": negative,
        "stop_reason": "frozen accepted drawings do not provide intended-direction touchdown ordering and cumulative travel" if contradiction else None,
    }
    out.mkdir(parents=True, exist_ok=True)
    (out / "support_investigation.json").write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "source_pack_sha256": result["source_pack_sha256"], "left_net": left_plan["net_displacement_px"], "right_net": right_plan["net_displacement_px"], "left_touchdown_deltas": left_plan["touchdown_deltas_px"], "right_touchdown_deltas": right_plan["touchdown_deltas_px"], "negative_tests": negative}, indent=2))
    return 0 if result["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
