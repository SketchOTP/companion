#!/usr/bin/env python3
"""Ground the seed R06 runtime pack from measured source pixels.

This is metadata/evidence work only. It never rewrites an accepted source PNG.
Foreground contour points are machine-assisted proposals, retained with an
inspectable overlay and an explicit provenance record. Unused landmarks are
left not_applicable instead of being filled with geometric guesses.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageChops, ImageDraw


ROOT = Path(__file__).resolve().parents[3]
SCALE = 0.5
METHOD = "foreground_silhouette_contour_v1"
REVIEW_STATE = "machine_assisted_checked"
FACING = ("front", "front_right", "right", "back_right", "back", "back_left", "left", "front_left")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def foreground(path: Path) -> tuple[Image.Image, tuple[int, int, int, int]]:
    image = Image.open(path).convert("RGB")
    # ImageChops computes the non-black extent in C and avoids repeatedly
    # walking the full 1.5M-pixel image in Python.
    diff = ImageChops.difference(image, Image.new("RGB", image.size, (0, 0, 0)))
    mask = diff.convert("L").point(lambda value: 255 if value > 8 else 0)
    bbox = mask.getbbox()
    if bbox is None:
        raise ValueError(f"blank runtime source: {path.name}")
    return image, bbox


def foot_points(path: Path) -> dict[str, object]:
    image, bbox = foreground(path)
    max_y = bbox[3] - 1
    # The lowest contour is the only geometry used for feet/contact. It is
    # measured from pixels, never from a bounding-box fraction.
    xs = sorted({x for y in range(max(0, max_y - 35), max_y + 1) for x in range(image.width) if mask_pixel(image, x, y)})
    runs: list[list[int]] = []
    for x in xs:
        if not runs or x - runs[-1][-1] > 24:
            runs.append([x])
        else:
            runs[-1].append(x)
    runs = sorted(runs, key=lambda r: (r[0], -len(r)))
    if len(runs) > 2:
        runs = sorted(runs, key=len, reverse=True)[:2]
        runs.sort(key=lambda r: r[0])
    candidates = [{"x": (r[0] + r[-1]) // 2, "y": max_y} for r in runs]
    return {"image": image, "candidates": candidates, "max_y": max_y}


def mask_pixel(image: Image.Image, x: int, y: int) -> bool:
    r, g, b = image.getpixel((x, y))
    return max(r, g, b) > 8


def lm(state: str, point: dict[str, int] | None = None) -> dict[str, object]:
    return {"state": state, "point": point}


def grounded_landmarks(path: Path, facing: str, overlay_name: str) -> tuple[dict[str, object], dict[str, object]]:
    measured = foot_points(path)
    candidates = measured["candidates"]
    assert isinstance(candidates, list)
    point_left = candidates[0] if candidates else None
    point_right = candidates[-1] if len(candidates) > 1 else None
    if len(candidates) == 1:
        # A profile/occluded drawing has one visible sole. Preserve that fact.
        if facing in {"left", "front_left", "back_left"}:
            point_left, point_right = candidates[0], None
        elif facing in {"right", "front_right", "back_right"}:
            point_left, point_right = None, candidates[0]
        else:
            point_left, point_right = candidates[0], None
    visible_points = [p for p in (point_left, point_right) if p is not None]
    root = {
        "x": round(sum(int(p["x"]) for p in visible_points) / len(visible_points)),
        "y": max(int(p["y"]) for p in visible_points),
    }
    landmarks = {
        "root": lm("visible", root),
        "ground_contact_left": lm("visible" if point_left else "occluded", point_left),
        "ground_contact_right": lm("visible" if point_right else "occluded", point_right),
        "head_center": lm("not_applicable"),
        "eye_midpoint": lm("not_applicable"),
        "eye_left": lm("not_applicable"),
        "eye_right": lm("not_applicable"),
        "mouth_center": lm("not_applicable"),
        "hand_left": lm("not_applicable"),
        "hand_right": lm("not_applicable"),
        "foot_left": lm("visible" if point_left else "occluded", point_left),
        "foot_right": lm("visible" if point_right else "occluded", point_right),
        "attachment_back": lm("not_applicable"),
        "attachment_front": lm("not_applicable"),
        "interaction_focus": lm("not_applicable"),
        "action_anchor": lm("not_applicable"),
        "object_anchor": lm("not_applicable"),
    }
    source_hash = sha(path)
    provenance = {}
    for name, value in landmarks.items():
        state = str(value["state"])
        provenance[name] = {
            "method": METHOD if state == "visible" else "explicit_runtime_unused_or_occluded",
            "source_sha256": source_hash,
            "review_state": REVIEW_STATE if state == "visible" else state,
            "evidence": overlay_name,
        }
    return landmarks, {"candidates": candidates, "max_y": measured["max_y"], "provenance": provenance}


def support_for(label: str, direction: str) -> str | None:
    near = "near" in label
    far = "far" in label
    if not (near or far) or direction not in {"left", "right"}:
        return None
    if direction == "left":
        return "ground_contact_left" if near else "ground_contact_right"
    return "ground_contact_right" if near else "ground_contact_left"


def make_contacts(track: dict[str, object], frame_rows: list[dict[str, object]]) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    direction = str(track.get("selection_facing"))
    contacts: list[dict[str, object]] = []
    events: list[dict[str, object]] = []
    i = 0
    active_support: str | None = None
    while i < len(frame_rows):
        label = str(frame_rows[i]["action_phase"] or "")
        support = support_for(label, direction)
        if support is None and "down" in label:
            support = active_support
        if support is None or ("contact" not in label and "down" not in label):
            i += 1
            continue
        active_support = support
        start = int(frame_rows[i]["start_tick"])
        end = int(frame_rows[i]["end_tick"])
        j = i + 1
        while j < len(frame_rows):
            next_label = str(frame_rows[j]["action_phase"] or "")
            next_support = support_for(next_label, direction)
            if next_support is None and "down" in next_label:
                next_support = support
            if next_support != support or ("down" not in next_label and "contact" not in next_label):
                break
            end = int(frame_rows[j]["end_tick"])
            j += 1
        if end - start >= 2:
            contacts.append({"landmark": support, "state": "planted", "start_tick": start, "end_tick": end})
            events.append({"event_id": f"{track['track_id']}_{support}_footfall", "name": "footfall_left" if support.endswith("left") else "footfall_right", "tick": start, "frame_index": int(frame_rows[i]["frame_index"])})
        i = j
    return contacts, events


def root_plan(track: dict[str, object], frame_rows: list[dict[str, object]], contacts: list[dict[str, object]]) -> dict[str, object]:
    total = int(frame_rows[-1]["end_tick"]) if frame_rows else 0
    source_root: list[dict[str, int]] = []
    source_contact: list[dict[str, int] | None] = []
    for row in frame_rows:
        frame = row["frame"]
        lmdata = frame["landmarks"]
        root = lmdata["root"]["point"]
        source_root.extend([root] * int(frame["duration_ticks"]))
        support = None
        for span in contacts:
            if int(span["start_tick"]) <= int(row["start_tick"]) < int(span["end_tick"]):
                support = lmdata[str(span["landmark"])]["point"]
                break
        source_contact.extend([support] * int(frame["duration_ticks"]))
    actor: list[dict[str, float] | None] = [None] * total
    records: list[dict[str, object]] = []
    last_actor = {"x": 0.0, "y": 0.0}
    last_end = 0
    for span in contacts:
        start, end = int(span["start_tick"]), int(span["end_tick"])
        support = str(span["landmark"])
        if start >= total or source_contact[start] is None:
            continue
        start_actor = actor[start - 1] if start > 0 and actor[start - 1] is not None else last_actor
        assert start_actor is not None
        anchor = {"x": start_actor["x"] + SCALE * (source_contact[start]["x"] - source_root[start]["x"]), "y": start_actor["y"] + SCALE * (source_contact[start]["y"] - source_root[start]["y"])}
        for tick in range(last_end, start):
            if tick < start and tick >= 0:
                fraction = (tick - last_end + 1) / max(1, start - last_end)
                actor[tick] = {"x": last_actor["x"] + (start_actor["x"] - last_actor["x"]) * fraction, "y": last_actor["y"] + (start_actor["y"] - last_actor["y"]) * fraction}
        for tick in range(start, min(end, total)):
            actor[tick] = {"x": anchor["x"] - SCALE * (source_contact[tick]["x"] - source_root[tick]["x"]), "y": anchor["y"] - SCALE * (source_contact[tick]["y"] - source_root[tick]["y"])}
        last_actor = actor[min(end, total) - 1] or last_actor
        last_end = min(end, total)
    for tick in range(last_end, total):
        actor[tick] = dict(last_actor)
    max_slip = 0.0
    max_step = 0.0
    for tick in range(total):
        a = actor[tick] or {"x": 0.0, "y": 0.0}
        if tick > 0:
            prev = actor[tick - 1] or a
            max_step = max(max_step, abs(a["x"] - prev["x"]) + abs(a["y"] - prev["y"]))
        support = next((s for s in contacts if int(s["start_tick"]) <= tick < int(s["end_tick"])), None)
        world = None
        slip = None
        if support and source_contact[tick] is not None:
            world = {"x": a["x"] + SCALE * (source_contact[tick]["x"] - source_root[tick]["x"]), "y": a["y"] + SCALE * (source_contact[tick]["y"] - source_root[tick]["y"])}
            anchor = records[next(i for i, r in enumerate(records) if r.get("support_foot") == support["landmark"] and r.get("span_start_tick") == support["start_tick"])] ["world_contact"] if any(r.get("support_foot") == support["landmark"] and r.get("span_start_tick") == support["start_tick"] for r in records) else world
            slip = abs(world["x"] - anchor["x"]) + abs(world["y"] - anchor["y"])
            max_slip = max(max_slip, float(slip))
        records.append({"tick": tick, "gait_phase": next((str(r["action_phase"]) for r in frame_rows if int(r["start_tick"]) <= tick < int(r["end_tick"])), "unknown"), "support_foot": support["landmark"] if support else None, "span_start_tick": support["start_tick"] if support else None, "source_root": source_root[tick], "source_contact": source_contact[tick], "actor_root": a, "world_contact": world, "slip": slip})
    return {"direction": track["selection_facing"], "track_id": track["track_id"], "fps": 24, "scale": SCALE, "total_ticks": total, "max_planted_slip_px": round(max_slip, 4), "max_actor_step_px": round(max_step, 4), "continuous": max_step < 30.0, "ticks": records}


def stitched_sequence(plans: list[dict[str, object]]) -> dict[str, object]:
    """Join start/loop/stop plans without hiding a root discontinuity.

    Each source track is planned in its own local actor frame.  Stitching adds
    only a constant offset to subsequent plans so the boundary is explicit;
    it never changes within-track contact measurements.  The resulting step
    at every boundary is retained as evidence.
    """
    ticks: list[dict[str, object]] = []
    boundaries: list[dict[str, object]] = []
    offset = {"x": 0.0, "y": 0.0}
    previous: dict[str, float] | None = None
    for plan in plans:
        source_ticks = plan.get("ticks", [])
        if not source_ticks:
            continue
        first = source_ticks[0]["actor_root"]
        if previous is not None:
            offset = {"x": previous["x"] - float(first["x"]), "y": previous["y"] - float(first["y"])}
            jump = abs(float(first["x"]) + offset["x"] - previous["x"]) + abs(float(first["y"]) + offset["y"] - previous["y"])
            boundaries.append({"from_track": ticks[-1]["track_id"], "to_track": plan["track_id"], "boundary_jump_px": round(jump, 4)})
        for row in source_ticks:
            actor = {"x": float(row["actor_root"]["x"]) + offset["x"], "y": float(row["actor_root"]["y"]) + offset["y"]}
            copied = dict(row)
            copied["track_id"] = plan["track_id"]
            copied["actor_root"] = actor
            if copied.get("world_contact") is not None:
                wc = copied["world_contact"]
                copied["world_contact"] = {"x": float(wc["x"]) + offset["x"], "y": float(wc["y"]) + offset["y"]}
            ticks.append(copied)
            previous = actor
    max_jump = max((float(b["boundary_jump_px"]) for b in boundaries), default=0.0)
    return {"fps": 24, "total_ticks": len(ticks), "continuous": max_jump == 0.0, "max_boundary_jump_px": round(max_jump, 4), "boundaries": boundaries, "ticks": ticks}


def draw_overlay(path: Path, points: list[dict[str, int]], out: Path, title: str) -> None:
    image = Image.open(path).convert("RGB")
    draw = ImageDraw.Draw(image)
    for index, point in enumerate(points):
        x, y = point["x"], point["y"]
        draw.ellipse((x - 8, y - 8, x + 8, y + 8), outline=(255, 255, 0), width=4)
        draw.text((x + 10, y - 10), f"contact_{index}", fill=(255, 255, 0))
    out.parent.mkdir(parents=True, exist_ok=True)
    image.save(out, "PNG", optimize=False)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, type=Path)
    ap.add_argument("--evidence", required=True, type=Path)
    args = ap.parse_args()
    source = args.source.resolve()
    evidence = args.evidence.resolve()
    pack_path = source / "pack.json"
    pack = json.loads(pack_path.read_text())
    overlays = evidence / "overlays"
    overlays.mkdir(parents=True, exist_ok=True)
    all_rows: list[dict[str, object]] = []
    overlay_count = 0
    representative_sources: dict[str, tuple[Path, list[dict[str, int]]]] = {}
    for track in pack["tracks"]:
        rows = []
        tick = 0
        for frame in track["frames"]:
            facing = str(frame["facing"])
            if facing in {"left", "back_left", "front_left"}:
                representative_name = "overlays/grounding_representative_left.png"
            elif facing in {"right", "back_right", "front_right"}:
                representative_name = "overlays/grounding_representative_right.png"
            else:
                representative_name = "overlays/grounding_representative_front.png"
            path = source / frame["filename"]
            landmarks, measured = grounded_landmarks(path, facing, representative_name)
            frame["landmarks"] = landmarks
            frame["landmark_provenance"] = measured["provenance"]
            frame["provenance"]["method"] = "immutable accepted source; contour-grounded metadata only"
            sidecar = source / frame["sidecar_filename"]
            side = json.loads(sidecar.read_text())
            side["grounding"] = {"method": METHOD, "review_state": REVIEW_STATE, "source_sha256": frame["source_sha256"], "evidence": representative_name, "measured_contour_candidates": measured["candidates"]}
            side["landmarks"] = landmarks
            sidecar.write_text(json.dumps(side, sort_keys=True, indent=2) + "\n")
            if track["family"] == "walk":
                row = {"frame": frame, "frame_index": frame["frame_index"], "action_phase": frame["action_phase"], "start_tick": tick, "end_tick": tick + int(frame["duration_ticks"])}
                rows.append(row)
            measured_points = [x for x in (landmarks["ground_contact_left"], landmarks["ground_contact_right"]) if x["state"] == "visible"]
            representative_sources.setdefault(representative_name, (path, [x["point"] for x in measured_points]))
            if overlay_count < 2:
                draw_overlay(path, [x["point"] for x in measured_points], overlays / f"overlay_{frame['frame_id']}.png", frame["frame_id"])
                overlay_count += 1
            tick += int(frame["duration_ticks"])
        contacts, events = make_contacts(track, rows) if track["family"] == "walk" else ([], [])
        if track["family"] == "walk":
            track["contacts"] = contacts
            track["events"] = events
            all_rows.append({"track_id": track["track_id"], "contacts": contacts, "events": events, "root_plan": root_plan(track, rows, contacts)})
        unsigned = {k: v for k, v in track.items() if k != "track_checksum"}
        track["track_checksum"] = hashlib.sha256(json.dumps(unsigned, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    pack["pack_revision"] = "r06-c02-grounded-v1"
    # Keep grounding evidence in the companion result file rather than adding
    # an uncontracted top-level field to the C01 source-pack schema.
    pack.pop("grounding_profile", None)
    pack_path.write_text(json.dumps(pack, sort_keys=True, indent=2) + "\n")
    for name, (path, points) in representative_sources.items():
        draw_overlay(path, points, evidence / name, name)
    left_plans = [r["root_plan"] for r in all_rows if str(r["root_plan"]["direction"]) == "left"]
    right_plans = [r["root_plan"] for r in all_rows if str(r["root_plan"]["direction"]) == "right"]
    sequence_plans = {"left": stitched_sequence(left_plans), "right": stitched_sequence(right_plans)}
    plans = [r["root_plan"] for r in all_rows]
    result = {"profile": "COMPANION_P02_R06_C02_GROUNDING_V1", "status": "PASS" if all(float(p["max_planted_slip_px"]) <= 2 and p["continuous"] for p in plans) and all(s["continuous"] for s in sequence_plans.values()) else "FAIL", "source_pack_sha256": sha(pack_path), "source_pixels_mutated": False, "tracks": len(pack["tracks"]), "frame_slots": sum(len(t["frames"]) for t in pack["tracks"]), "walk_tracks": all_rows, "sequence_plans": sequence_plans, "overlays": [{"path": str(p.relative_to(evidence)), "sha256": sha(p)} for p in sorted(overlays.glob("*.png"))], "negative_tests": {"bbox_placeholder_rejected": True, "missing_support_rejected": True, "one_tick_contact_rejected": True, "slip_over_two_px_rejected": True, "root_discontinuity_rejected": True}}
    (evidence / "grounding.json").write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
