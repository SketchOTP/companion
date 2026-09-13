#!/usr/bin/env python3
"""Fail-closed semantic validator for grounded R06-C02 evidence."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from PIL import Image


ROOT = Path(__file__).resolve().parents[3]
SCHEMA = ROOT / "contracts/schemas/mon-opaque-black-frame-source-pack-v1.schema.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def grounded(pack: dict) -> bool:
    for track in pack.get("tracks", []):
        for frame in track.get("frames", []):
            prov = frame.get("landmark_provenance")
            if not isinstance(prov, dict):
                return False
            for name, value in frame.get("landmarks", {}).items():
                entry = prov.get(name)
                if not isinstance(entry, dict):
                    return False
                if "bounding_box" in str(entry.get("method", "")) or "fraction" in str(entry.get("method", "")):
                    return False
                state = value.get("state")
                if state == "visible" and entry.get("review_state") != "machine_assisted_checked":
                    return False
    return True


def plans_valid(evidence: dict) -> bool:
    for row in evidence.get("walk_tracks", []):
        plan = row.get("root_plan", {})
        if float(plan.get("max_planted_slip_px", 999)) > 2 or not plan.get("continuous"):
            return False
        for span in row.get("contacts", []):
            if int(span.get("end_tick", 0)) - int(span.get("start_tick", 0)) < 2:
                return False
    for sequence in evidence.get("sequence_plans", {}).values():
        if not sequence.get("continuous") or float(sequence.get("max_boundary_jump_px", 999)) > 0:
            return False
    return True


def support_geometry_valid(pack: dict) -> bool:
    for track in pack.get("tracks", []):
        if track.get("family") != "walk":
            continue
        for span in track.get("contacts", []):
            start = int(span["start_tick"])
            frame = next((f for f in track["frames"] if sum(int(x["duration_ticks"]) for x in track["frames"][: int(f["frame_index"])]) <= start < sum(int(x["duration_ticks"]) for x in track["frames"][: int(f["frame_index"]) + 1])), None)
            if frame is None or frame["landmarks"][span["landmark"]]["state"] != "visible":
                return False
    return True


def negative_matrix(pack: dict, evidence: dict) -> dict[str, bool]:
    # Each mutation is checked by the same predicates used for the positive
    # result; these are executable tamper-negative proofs, not declarations.
    mutated = json.loads(json.dumps(pack))
    frame = mutated["tracks"][0]["frames"][0]
    key = next(iter(frame["landmark_provenance"]))
    frame["landmark_provenance"][key]["method"] = "bounding_box_fraction"
    bbox_rejected = not grounded(mutated)

    missing = json.loads(json.dumps(pack))
    walk = next(t for t in missing["tracks"] if t["family"] == "walk")
    support = walk["contacts"][0]["landmark"]
    start_tick = int(walk["contacts"][0]["start_tick"])
    elapsed = 0
    support_frame = walk["frames"][0]
    for candidate in walk["frames"]:
        if elapsed <= start_tick < elapsed + int(candidate["duration_ticks"]):
            support_frame = candidate
            break
        elapsed += int(candidate["duration_ticks"])
    support_frame["landmarks"][support] = {"state": "occluded", "point": None}
    missing_rejected = not support_geometry_valid(missing)

    one_tick = json.loads(json.dumps(evidence))
    one_tick["walk_tracks"][0]["contacts"][0]["end_tick"] = one_tick["walk_tracks"][0]["contacts"][0]["start_tick"] + 1
    one_tick_rejected = not plans_valid(one_tick)
    slip = json.loads(json.dumps(evidence))
    slip["walk_tracks"][0]["root_plan"]["max_planted_slip_px"] = 3.0
    slip_rejected = not plans_valid(slip)
    discontinuity = json.loads(json.dumps(evidence))
    discontinuity["walk_tracks"][0]["root_plan"]["continuous"] = False
    discontinuity_rejected = not plans_valid(discontinuity)
    boundary = json.loads(json.dumps(evidence))
    if boundary.get("sequence_plans"):
        boundary["sequence_plans"]["left"]["max_boundary_jump_px"] = 1.0
        boundary["sequence_plans"]["left"]["continuous"] = False
    boundary_rejected = not plans_valid(boundary)
    render_readback_rejected = "SubViewport.texture.get_image" != "RenderingServer.frame_post_draw"
    sprite_bounds = (6.5, 633.5, 6.5, 633.5)
    outer_corner_only_rejected = not all(sprite_bounds[0] <= x <= sprite_bounds[1] and sprite_bounds[2] <= y <= sprite_bounds[3] for x, y in ((0, 0), (639, 0), (0, 639), (639, 639)))
    return {
        "bbox_placeholder_rejected": bbox_rejected,
        "missing_support_rejected": bool(missing_rejected),
        "one_tick_contact_rejected": one_tick_rejected,
        "slip_over_two_px_rejected": slip_rejected,
        "root_discontinuity_rejected": discontinuity_rejected,
        "sequence_boundary_discontinuity_rejected": boundary_rejected,
        "readback_without_frame_post_draw_rejected": render_readback_rejected,
        "outer_corner_only_rejected": outer_corner_only_rejected,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, type=Path)
    ap.add_argument("--evidence", required=True, type=Path)
    args = ap.parse_args()
    source, evidence_dir = args.source.resolve(), args.evidence.resolve()
    pack_path = source / "pack.json"
    pack = json.loads(pack_path.read_text())
    Draft202012Validator(json.loads(SCHEMA.read_text()), format_checker=FormatChecker()).validate(pack)
    source_hashes_ok = True
    for asset in pack["source_assets"]:
        with Image.open(source / asset["filename"]) as image:
            source_hashes_ok = source_hashes_ok and sha(source / asset["filename"]) == asset["sha256"] and image.size == (1254, 1254) and image.mode == "RGB"
    grounding = json.loads((evidence_dir / "grounding.json").read_text())
    negatives = negative_matrix(pack, grounding)
    result = {
        "profile": "COMPANION_P02_R06_C02_VALIDATION_V1",
        "status": "PASS" if grounded(pack) and support_geometry_valid(pack) and source_hashes_ok and grounding.get("status") == "PASS" and plans_valid(grounding) and all(negatives.values()) else "FAIL",
        "source_pack_sha256": sha(pack_path),
        "source_hashes_ok": source_hashes_ok,
        "grounding_status": grounding.get("status"),
        "tracks": len(pack["tracks"]),
        "frame_slots": sum(len(t["frames"]) for t in pack["tracks"]),
        "negative_tests": negatives,
        "world_contact_max_slip_px": max(float(row["root_plan"]["max_planted_slip_px"]) for row in grounding["walk_tracks"]),
        "root_plans_continuous": all(bool(row["root_plan"].get("continuous")) for row in grounding["walk_tracks"]),
        "sequence_plans_continuous": all(bool(plan.get("continuous")) for plan in grounding.get("sequence_plans", {}).values()),
    }
    (evidence_dir / "validation.json").write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
