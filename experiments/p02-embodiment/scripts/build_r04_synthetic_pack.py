#!/usr/bin/env python3
"""Build an unmistakably synthetic source pack for contract/intake tests.

This fixture is calibration geometry, never production character art. PNGs are
emitted with an explicit sRGB chunk so validation exercises actual wire bytes.
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

ROOT = Path(__file__).resolve().parents[3]
IDENTITY_SHA = "86ce1f9428f9a998d57e1a99c4245347d5a05e9f0bcf853c2b68065f351bdb56"
TURNAROUND_SHA = "3696c7d63594de38d408438d5b882f3207635bc63e59fb270f624715faeb09e4"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def add_srgb_chunk(path: Path) -> None:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not PNG")
    length = struct.unpack(">I", data[8:12])[0]
    if data[12:16] != b"IHDR" or length != 13:
        raise ValueError("invalid IHDR")
    split = 16 + length + 4
    payload = b"\x00"
    kind = b"sRGB"
    chunk = struct.pack(">I", len(payload)) + kind + payload
    chunk += struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF)
    path.write_bytes(data[:split] + chunk + data[split:])


def render(path: Path, index: int) -> None:
    image = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    # Calibration geometry, deliberately never a character.
    draw.rectangle((256 + index * 24, 320, 768 - index * 24, 768), fill=(0, 190, 255, 220), outline=(255, 255, 255, 255), width=8)
    draw.ellipse((448, 832, 576, 960), fill=(255, 170, 0, 255))
    draw.line((512, 320, 512, 896), fill=(255, 0, 150, 255), width=6)
    draw.text((380, 500), f"SYNTHETIC TEST {index}", fill=(0, 0, 0, 255))
    image.save(path, "PNG", optimize=False)
    add_srgb_chunk(path)


def landmark(x: int, y: int, state: str = "visible") -> dict:
    return {"state": state, "point": {"x": x, "y": y} if state == "visible" else None}


def make_frame(out: Path, index: int) -> dict:
    stem = f"test_pulse__front__neutral__v01__f{index:03d}"
    filename = f"frames/{stem}.png"
    sidecar_filename = f"sidecars/{stem}.frame.json"
    image_path = out / filename
    render(image_path, index)
    digest = sha256(image_path)
    landmarks = {
        "root": landmark(512, 896), "ground_contact_left": landmark(480, 896), "ground_contact_right": landmark(544, 896),
        "head_center": landmark(512, 320), "eye_midpoint": landmark(512, 448), "eye_left": landmark(448, 448), "eye_right": landmark(576, 448),
        "mouth_center": landmark(512, 520), "hand_left": landmark(280, 560), "hand_right": landmark(744, 560), "foot_left": landmark(480, 896), "foot_right": landmark(544, 896),
        "attachment_back": landmark(512, 640), "attachment_front": landmark(512, 600), "interaction_focus": landmark(512, 448), "action_anchor": landmark(512, 560), "object_anchor": landmark(512, 560, "not_applicable"),
    }
    frame = {
        "frame_id": f"test_pulse_front_neutral_01_{index:03d}", "frame_index": index,
        "filename": filename.removeprefix("frames/"), "sidecar_filename": sidecar_filename.removeprefix("sidecars/"),
        "duration_ticks": index + 1, "source_asset_id": f"asset_test_pulse_{index:03d}", "source_sha256": digest,
        "facing": "front", "posture": "neutral", "action_phase": "pulse" if index else "settle", "landmarks": landmarks,
        "provenance": {"authored_by": "synthetic_fixture_builder", "method": "obvious geometric calibration pattern", "source_revision": "r04-c01-v1"}, "reuse_of": None,
    }
    write_json(out / sidecar_filename, frame)
    return frame


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--clean", action="store_true")
    args = parser.parse_args()
    out = args.out.resolve()
    if args.clean and out.exists():
        shutil.rmtree(out)
    (out / "frames").mkdir(parents=True, exist_ok=True)
    (out / "sidecars").mkdir(parents=True, exist_ok=True)
    frames = [make_frame(out, index) for index in range(2)]
    track = {
        "track_id": "synthetic:test_pulse:front:neutral:1", "family": "test_pulse", "selection_facing": "front", "entry_facing": "front", "exit_facing": "front",
        "posture": "neutral", "variant": 1, "entry_posture": "neutral", "exit_posture": "neutral", "completion": "once", "frames": frames,
        "contacts": [{"landmark": "ground_contact_left", "state": "planted", "start_tick": 0, "end_tick": 3}], "events": [{"event_id": "test_marker_001", "name": "test_marker", "tick": 1, "frame_index": 1}], "interruption_ranges": [{"start_tick": 0, "end_tick": 3}],
    }
    track["track_checksum"] = hashlib.sha256(json.dumps(track, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    assets = [{"asset_id": f["source_asset_id"], "filename": f"frames/{f['filename']}", "sha256": f["source_sha256"]} for f in frames]
    pack = {
        "profile": "MON_AUTHORED_FRAME_SOURCE_PACK_V1", "schema_version": 1, "pack_id": "00000000-0000-4000-8000-000000000405", "pack_revision": "synthetic-r04-c01-v1", "body_revision": "synthetic-geometric-v1", "developmental_stage": "synthetic", "approval_state": "synthetic_test_only",
        "approved_references": {"identity_sha256": IDENTITY_SHA, "turnaround_sha256": TURNAROUND_SHA}, "provenance": {"art_authority": "synthetic_test_fixture", "generation_or_edit_method": "obvious geometric calibration pattern", "source_authority": "COMPANION-P02-EMBODIMENT-001-R04-C01", "rights_record": "project-authored synthetic test data; not production character art"}, "timing": {"fps": 24, "tick_unit": "1/24_second"}, "request_profile": "synthetic_r04_test_v1", "source_assets": assets, "tracks": [track],
    }
    write_json(out / "pack.json", pack)
    print(json.dumps({"status": "SYNTHETIC_TEST_PACK_BUILT", "frames": len(frames), "pack": str(out / "pack.json"), "profile": pack["profile"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
