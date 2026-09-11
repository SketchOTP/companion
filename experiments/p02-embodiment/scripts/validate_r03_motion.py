#!/usr/bin/env python3
"""Fail-closed validator for the R03 reference-grounded motion proof.

The validator consumes only a disposable, synthetic bake directory.  Every
claim is derived from the rendered PNGs, pose manifest, source hierarchy, and
temporal-track JSON; no hand-authored PASS flag is accepted.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import shutil
import sys
import tempfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
SCHEMA = ROOT / "contracts/schemas/mon-temporal-track-v2.schema.json"
BODY = ROOT / "assets/source/p02/r03/mon_body_source_v2.json"
EXPECTED_FAMILIES = {
    "idle_breathe": 6,
    "walk": 8,
    "orient_front_to_front_left": 4,
    "orient_front_left_to_front": 4,
    "listen_acknowledge": 6,
}
REQUIRED_PARTS = {
    "shadow", "pelvis_root", "torso", "head", "head_base", "spike_topology",
    "eye_field_left", "eye_field_right", "pupil_left", "pupil_right", "mouth",
    "arm_left", "arm_right", "leg_left", "leg_right",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def schema_validate(track: dict, errors: list[str]) -> None:
    try:
        import jsonschema
    except ImportError:
        fail(errors, "jsonschema package unavailable; Draft 2020-12 validation cannot be claimed")
        return
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    try:
        jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker()).validate(track)
    except Exception as exc:
        fail(errors, f"schema validation failed for {track.get('track_id')}: {exc}")


def flatten_parts(body: dict) -> set[str]:
    """Collect stable IDs from the committed explicit part table."""
    if isinstance(body.get("parts"), list):
        return {part.get("id", "") for part in body["parts"]}
    node = body.get("hierarchy", body)
    found = {node.get("id", "")}
    for child in node.get("children", []):
        found |= flatten_parts(child)
    return found


def track_checksum(track: dict) -> str:
    payload = {k: v for k, v in track.items() if k != "track_checksum"}
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def evaluate(out: Path, body_path: Path = BODY) -> tuple[dict, list[str]]:
    errors: list[str] = []
    tracks_doc = json.loads((out / "temporal_tracks_v2.json").read_text(encoding="utf-8"))
    pose_doc = json.loads((out / "pose_manifest.json").read_text(encoding="utf-8"))
    body = json.loads(body_path.read_text(encoding="utf-8"))
    parts = flatten_parts(body)
    missing = REQUIRED_PARTS - parts
    if missing:
        fail(errors, f"body hierarchy missing parts: {sorted(missing)}")
    for stem in ("upper_arm", "forearm", "hand", "finger01", "finger02", "thumb", "thigh", "lower_leg", "foot", "toe01", "toe02", "toe03"):
        if not any(part == stem + "_left" for part in parts) or not any(part == stem + "_right" for part in parts):
            fail(errors, f"body hierarchy missing bilateral component {stem}")
    tracks = tracks_doc.get("tracks", [])
    if len(tracks) != len(EXPECTED_FAMILIES):
        fail(errors, f"expected {len(EXPECTED_FAMILIES)} tracks, observed {len(tracks)}")
    pose_by_id = {f["frame_id"]: f for f in pose_doc.get("frames", [])}
    observations: dict[str, dict] = {}
    for track in tracks:
        family = track.get("family")
        expected_count = EXPECTED_FAMILIES.get(family)
        if expected_count is None:
            fail(errors, f"unexpected track family {family!r}")
            continue
        if len(track.get("frames", [])) != expected_count:
            fail(errors, f"{family}: expected {expected_count} temporal drawings")
        schema_validate(track, errors)
        if track.get("track_checksum") != track_checksum(track):
            fail(errors, f"{family}: track checksum mismatch")
        if track.get("fps") != 24:
            fail(errors, f"{family}: timing grid is not 24 FPS")
        if track.get("root_motion_policy") != "forbidden":
            fail(errors, f"{family}: root motion is not forbidden")
        frame_hashes = []
        roots = []
        feet = []
        baseline_counts = []
        for index, frame in enumerate(track.get("frames", [])):
            if frame.get("frame_index") != index:
                fail(errors, f"{family}: frame indices are not contiguous")
            if frame.get("duration_ticks", 0) < 1:
                fail(errors, f"{family}: invalid duration tick")
            path = out / frame["path"]
            if not path.is_file():
                fail(errors, f"{family}: missing rendered frame {frame['path']}")
                continue
            lm = frame.get("landmarks", {})
            with Image.open(path) as image:
                image.load()
                if image.size != (1024, 1024) or image.mode != "RGBA":
                    fail(errors, f"{family}: frame canvas/mode mismatch {frame['path']}")
                alpha = image.getchannel("A")
                bbox = alpha.getbbox()
                if bbox:
                    left, top, right, bottom = bbox
                    if left < 64 or right > 960 or top < 32 or bottom > 960:
                        fail(errors, f"{family}: rendered pixels outside MON_FRAME_V1 safety region")
                # Contact evidence must be visible in the raster, not only in
                # the JSON sidecar: inspect alpha at the declared baseline
                # around each active foot landmark.
                alpha_pixels = alpha.load()
                baseline_hits = 0
                for x in range(64, 961):
                    if alpha_pixels[x, 896] > 0:
                        baseline_hits += 1
                baseline_counts.append(baseline_hits)
                for contact in frame.get("contacts", []):
                    if not contact.get("active"):
                        continue
                    point = lm.get(contact.get("landmark"), [0, 0])
                    lo, hi = max(64, int(point[0]) - 45), min(960, int(point[0]) + 45)
                    if not any(alpha_pixels[x, 896] > 0 for x in range(lo, hi + 1)):
                        fail(errors, f"{family}: active contact has no baseline pixels in rendered raster")
                frame_hashes.append(sha256(path))
            if frame.get("sha256") != frame_hashes[-1]:
                fail(errors, f"{family}: frame hash mismatch {frame['frame_id']}")
            roots.append(tuple(lm.get("root", [])))
            feet.append((tuple(lm.get("left_foot", [])), tuple(lm.get("right_foot", []))))
            for contact in frame.get("contacts", []):
                landmark = contact.get("landmark")
                point = lm.get(landmark, [])
                if contact.get("active") and (len(point) != 2 or point[1] != 896):
                    fail(errors, f"{family}: active contact {landmark} is not on the rendered baseline")
            if frame["frame_id"] not in pose_by_id:
                fail(errors, f"{family}: source pose is not traceable")
        if roots and any(root != (512, 896) for root in roots):
            fail(errors, f"{family}: rendered root landmark moved")
        if family == "idle_breathe" and any(foot[0][1] != 896 or foot[1][1] != 896 for foot in feet):
            fail(errors, "idle_breathe: planted feet are not stable")
        observations[family] = {"frame_count": len(frame_hashes), "unique_frame_hashes": len(set(frame_hashes)), "roots": roots, "feet": feet, "baseline_alpha_pixel_counts": baseline_counts}

    walk = observations.get("walk", {})
    walk_feet = walk.get("feet", [])
    if walk_feet:
        left_x = {foot[0][0] for foot in walk_feet}; right_x = {foot[1][0] for foot in walk_feet}
        if len(left_x) < 2 or len(right_x) < 2:
            fail(errors, "walk: swing-foot displacement was not rendered")
        if not any(foot[0][1] == 896 for foot in walk_feet) or not any(foot[1][1] == 896 for foot in walk_feet):
            fail(errors, "walk: each foot lacks a rendered planted contact")
    for family in ("orient_front_to_front_left", "orient_front_left_to_front"):
        track = next((t for t in tracks if t.get("family") == family), None)
        if track and track.get("frames"):
            first, last = track["frames"][0], track["frames"][-1]
            if first.get("sha256") == last.get("sha256"):
                fail(errors, f"{family}: endpoint silhouettes are identical")
    reaction = observations.get("listen_acknowledge", {})
    if reaction and reaction.get("unique_frame_hashes", 0) < 4:
        fail(errors, "listen_acknowledge: insufficient rendered temporal change")
    summary = {"status": "PASS" if not errors else "FAIL", "tracks": observations, "errors": errors}
    return summary, errors


def tamper_negative(out: Path) -> list[str]:
    """Run deterministic mutations against the semantic checks.

    These are evidence that the gate is fail-closed, not product tests.
    """
    checks: list[str] = []
    with tempfile.TemporaryDirectory(prefix="companion-r03-negative-") as temp:
        root = Path(temp)
        shutil.copytree(out, root / "bundle")
        bundle = root / "bundle"
        cases = [
            ("root_one_pixel", lambda d, b: d["tracks"][0]["frames"][0]["landmarks"].__setitem__("root", [513, 896]), None),
            ("duration_zero", lambda d, b: d["tracks"][0]["frames"][0].__setitem__("duration_ticks", 0), None),
            ("contact_shift", lambda d, b: d["tracks"][1]["frames"][0]["landmarks"].__setitem__("left_foot", [410, 895]), None),
            ("facing_reused", lambda d, b: d["tracks"][2]["frames"][-1].__setitem__("sha256", d["tracks"][2]["frames"][0]["sha256"]), None),
            ("missing_digit", None, "finger02_left"),
        ]
        for name, mutate, remove_part in cases:
            shutil.rmtree(bundle)
            shutil.copytree(out, bundle)
            candidate_path = bundle / "temporal_tracks_v2.json"
            candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
            body_path = BODY
            if mutate:
                mutate(candidate, None)
                # Keep the envelope internally consistent so the mutation
                # exercises the semantic assertion rather than only checksum
                # verification.
                if name in {"root_one_pixel", "contact_shift"}:
                    for changed in candidate["tracks"]:
                        changed["track_checksum"] = track_checksum(changed)
                candidate_path.write_text(json.dumps(candidate, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            if remove_part:
                body_copy = bundle / "tampered_body.json"
                body_doc = json.loads(BODY.read_text(encoding="utf-8"))
                body_doc["parts"] = [p for p in body_doc["parts"] if p.get("id") != remove_part]
                body_copy.write_text(json.dumps(body_doc, indent=2, sort_keys=True) + "\n", encoding="utf-8")
                body_path = body_copy
            _, errors = evaluate(bundle, body_path=body_path)
            if not errors:
                checks.append(f"{name}: accepted unexpectedly")
            else:
                checks.append(f"{name}: rejected ({errors[0]})")
    return checks


def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--out", type=Path, required=True); ap.add_argument("--tamper-negative", action="store_true")
    args = ap.parse_args(); out = args.out.resolve()
    try:
        summary, errors = evaluate(out)
    except Exception as exc:
        print(f"ERROR validator could not evaluate bundle: {exc}", file=sys.stderr)
        return 2
    if args.tamper_negative:
        summary["tamper_negative"] = tamper_negative(out)
        negative_failed = any("accepted unexpectedly" in item for item in summary["tamper_negative"])
    else:
        negative_failed = False
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1 if errors or negative_failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
