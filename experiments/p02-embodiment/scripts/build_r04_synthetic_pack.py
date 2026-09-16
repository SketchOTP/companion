#!/usr/bin/env python3
"""Build the complete C02 bounded profile using calibration geometry only.

The generated images are deliberately abstract (cyan/orange calibration marks)
and are never candidate character artwork. They exercise the exact request
profile, source/sidecar relationships, event timing, contacts, and reuse rules.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import struct
import zlib
from pathlib import Path

from PIL import Image, ImageDraw

IDENTITY_SHA = "86ce1f9428f9a998d57e1a99c4245347d5a05e9f0bcf853c2b68065f351bdb56"
TURNAROUND_SHA = "3696c7d63594de38d408438d5b882f3207635bc63e59fb270f624715faeb09e4"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def add_srgb_chunk(path: Path) -> None:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise ValueError("not a canonical PNG")
    length = struct.unpack(">I", data[8:12])[0]
    split = 16 + length + 4
    payload = b"\x00"; kind = b"sRGB"
    chunk = struct.pack(">I", 1) + kind + payload + struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF)
    path.write_bytes(data[:split] + chunk + data[split:])


def render(path: Path, index: int, family: str, facing: str, posture: str) -> None:
    image = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0)); draw = ImageDraw.Draw(image)
    phase = (index * 37 + len(family) * 11 + len(facing) * 7) % 160
    left = 176 + phase // 3; right = 848 - phase // 4; top = 192 + (index % 4) * 24; bottom = 760 - (index % 3) * 16
    draw.rounded_rectangle((left, top, right, bottom), radius=36, fill=(0, 190, 255, 220), outline=(255, 255, 255, 255), width=8)
    draw.ellipse((420 + (index % 3) * 8, 820, 604 + (index % 3) * 8, 956), fill=(255, 170, 0, 255), outline=(255, 255, 255, 255), width=6)
    draw.line((512, 96 + index * 8, 512, 896), fill=(255, 0, 150, 255), width=6)
    draw.line((128, 896, 896, 896), fill=(120, 255, 120, 255), width=4)
    draw.text((250, 480), f"CAL {family} {facing} {posture} {index}", fill=(0, 0, 0, 255))
    image.save(path, "PNG", optimize=False); add_srgb_chunk(path)


def landmark(x: int, y: int, state: str = "visible") -> dict:
    return {"state": state, "point": {"x": x, "y": y} if state == "visible" else None}


def make_frame(out: Path, family: str, facing: str, posture: str, variant: int, index: int, phase: str, *, reuse_of: str | None = None, occluded: bool = False) -> dict:
    stem = f"{family}__{facing}__{posture}__v{variant:02d}__f{index:03d}"; image_rel = Path("frames") / f"{stem}.png"; sidecar_rel = Path("sidecars") / f"{stem}.frame.json"
    image_path = out / image_rel; image_path.parent.mkdir(parents=True, exist_ok=True)
    render_index = index - 1 if reuse_of else index
    render(image_path, render_index, family, facing, posture); digest = sha256(image_path)
    landmarks = {
        "root": landmark(512, 896), "ground_contact_left": landmark(420, 896), "ground_contact_right": landmark(604, 896), "head_center": landmark(512, 300),
        "eye_midpoint": landmark(512, 430), "eye_left": landmark(450, 430, "occluded" if occluded else "visible"), "eye_right": landmark(574, 430, "occluded" if occluded else "visible"), "mouth_center": landmark(512, 520),
        "hand_left": landmark(270, 620), "hand_right": landmark(754, 620), "foot_left": landmark(420, 896), "foot_right": landmark(604, 896), "attachment_back": landmark(512, 650), "attachment_front": landmark(512, 610), "interaction_focus": landmark(512, 430), "action_anchor": landmark(512, 560), "object_anchor": landmark(512, 560, "not_applicable")}
    result = {"frame_id": f"{family}_{facing}_{posture}_{variant:02d}_{index:03d}", "frame_index": index, "filename": image_rel.name, "sidecar_filename": sidecar_rel.name, "duration_ticks": 2 if reuse_of else 1, "source_asset_id": f"asset_{family}_{facing}_{posture}_{variant:02d}_{index:03d}", "source_sha256": digest, "facing": facing, "posture": posture, "action_phase": phase, "landmarks": landmarks, "provenance": {"authored_by": "synthetic_fixture_builder", "method": "obvious geometric calibration pattern", "source_revision": "r04-c02-v1"}, "reuse_of": reuse_of}
    write_json(out / sidecar_rel, result); return result


def make_track(out: Path, family: str, selection: str, entry: str, exit_: str, posture: str, variant: int, completion: str, facings: list[str], phases: list[str], *, event_specs: list[tuple[str, str, int]] = (), contacts: list[dict] | None = None, entry_posture: str | None = None, exit_posture: str | None = None, occluded_index: int | None = None, reuse_index: int | None = None) -> dict:
    frames = []
    for i, facing in enumerate(facings):
        reuse = frames[i - 1]["frame_id"] if reuse_index is not None and i == reuse_index else None
        frames.append(make_frame(out, family, facing, posture, variant, i, phases[i], reuse_of=reuse, occluded=i == occluded_index))
    events = [{"event_id": event_id, "name": name, "tick": sum(item["duration_ticks"] for item in frames[:frame_index]), "frame_index": frame_index} for event_id, name, frame_index in event_specs]
    total = sum(item["duration_ticks"] for item in frames)
    track = {"track_id": f"synthetic:{family}:{selection}:{variant}", "family": family, "selection_facing": selection, "entry_facing": entry, "exit_facing": exit_, "posture": posture, "variant": variant, "entry_posture": entry_posture or posture, "exit_posture": exit_posture or posture, "completion": completion, "frames": frames, "contacts": contacts or [], "events": events, "interruption_ranges": [{"start_tick": 0, "end_tick": total}]}
    track["track_checksum"] = hashlib.sha256(json.dumps({key: value for key, value in track.items() if key != "track_checksum"}, sort_keys=True, separators=(",", ":")).encode()).hexdigest(); return track


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--out", type=Path, required=True); parser.add_argument("--clean", action="store_true"); args = parser.parse_args(); out = args.out.resolve()
    if args.clean and out.exists(): shutil.rmtree(out)
    (out / "frames").mkdir(parents=True, exist_ok=True); (out / "sidecars").mkdir(parents=True, exist_ok=True)
    tracks = [
        make_track(out, "neutral_construction", "front", "front", "front", "neutral", 1, "once", ["front"], ["rest"]),
        make_track(out, "neutral_construction", "right", "right", "right", "neutral", 1, "once", ["right"], ["rest"], occluded_index=0),
        make_track(out, "neutral_construction", "front_left", "front_left", "front_left", "neutral", 1, "once", ["front_left"], ["rest"]),
        make_track(out, "idle_breathe", "front_left", "front_left", "front_left", "neutral", 1, "loop", ["front_left"] * 6, ["inhale", "rise", "peak", "exhale", "settle", "rest"], reuse_index=5),
        make_track(out, "walk", "front_left", "front_left", "front_left", "walking", 1, "loop", ["front_left"] * 8, ["left_contact", "left_down", "left_passing", "left_up", "right_contact", "right_down", "right_passing", "right_up"], contacts=[{"landmark": "ground_contact_left", "state": "planted", "start_tick": 0, "end_tick": 1}, {"landmark": "ground_contact_right", "state": "planted", "start_tick": 4, "end_tick": 5}], event_specs=[("walk_left_footfall", "footfall_left", 1), ("walk_right_footfall", "footfall_right", 4)]),
        make_track(out, "orient_front_to_front_left", "front", "front", "front_left", "neutral", 1, "once", ["front", "front", "front_left", "front_left"], ["anticipate", "turn", "settle", "finish"], event_specs=[("orient_forward_done", "facing_changed", 3)]),
        make_track(out, "orient_front_left_to_front", "front_left", "front_left", "front", "neutral", 1, "once", ["front_left", "front_left", "front", "front"], ["anticipate", "turn", "settle", "finish"], event_specs=[("orient_back_done", "facing_changed", 3)]),
        make_track(out, "listen_acknowledge", "front_left", "front_left", "front_left", "listening", 1, "once", ["front_left"] * 6, ["listen", "attend", "ack", "ack", "settle", "settled"], event_specs=[("listen_attention", "attention_acquired", 1), ("listen_ack", "acknowledge", 3), ("listen_settled", "settled", 5)], entry_posture="listening", exit_posture="acknowledging"),
    ]
    assets = [{"asset_id": item["source_asset_id"], "filename": f"frames/{item['filename']}", "sha256": item["source_sha256"]} for track in tracks for item in track["frames"]]
    pack = {"profile": "MON_AUTHORED_FRAME_SOURCE_PACK_V1", "schema_version": 1, "pack_id": "00000000-0000-4000-8000-00000000c002", "pack_revision": "phase02-bounded-motion-proof-v1", "body_revision": "synthetic-calibration-v1", "developmental_stage": "synthetic", "approval_state": "synthetic_test_only", "approved_references": {"identity_sha256": IDENTITY_SHA, "turnaround_sha256": TURNAROUND_SHA}, "provenance": {"art_authority": "synthetic_test_fixture", "generation_or_edit_method": "obvious geometric calibration pattern", "source_authority": "COMPANION-P02-EMBODIMENT-001-R04-C02", "rights_record": "project-authored synthetic test data; not production character art"}, "timing": {"fps": 24, "tick_unit": "1/24_second"}, "request_profile": "phase02_bounded_motion_proof_v1", "source_assets": assets, "tracks": tracks}
    write_json(out / "pack.json", pack); print(json.dumps({"status": "SYNTHETIC_TEST_PACK_BUILT", "frames": sum(len(t["frames"]) for t in tracks), "tracks": len(tracks), "pack": str(out / "pack.json"), "profile": pack["request_profile"]}, sort_keys=True)); return 0


if __name__ == "__main__":
    raise SystemExit(main())
