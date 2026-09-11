#!/usr/bin/env python3
"""Build an obviously synthetic, non-product authored-frame intake fixture."""

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
    """Insert the standard perceptual-intent sRGB chunk after IHDR."""
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not PNG")
    ihdr_len = struct.unpack(">I", data[8:12])[0]
    split = 20 + ihdr_len
    payload = b"\x00"
    chunk_type = b"sRGB"
    chunk = struct.pack(">I", len(payload)) + chunk_type + payload
    chunk += struct.pack(">I", zlib.crc32(chunk_type + payload) & 0xFFFFFFFF)
    path.write_bytes(data[:split] + chunk + data[split:])


def render(path: Path, index: int) -> None:
    image = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    # Deliberately unmistakable calibration geometry, never a character.
    draw.rectangle((256 + index * 24, 320, 768 - index * 24, 768), fill=(0, 190, 255, 220), outline=(255, 255, 255, 255), width=8)
    draw.ellipse((448, 832, 576, 960), fill=(255, 170, 0, 255))
    draw.line((512, 320, 512, 896), fill=(255, 0, 150, 255), width=6)
    draw.text((390, 500), f"SYNTHETIC TEST {index}", fill=(0, 0, 0, 255))
    image.save(path, "PNG", optimize=False)
    add_srgb_chunk(path)


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

    frames = []
    for index in range(2):
        stem = f"test_pulse__front__neutral__v01__f{index:03d}"
        filename = f"{stem}.png"
        sidecar_filename = f"{stem}.frame.json"
        image_path = out / "frames" / filename
        render(image_path, index)
        frame = {
            "frame_id": f"test_pulse_front_neutral_01_{index:03d}",
            "frame_index": index,
            "filename": filename,
            "sidecar_filename": sidecar_filename,
            "duration_ticks": index + 1,
            "source_sha256": sha256(image_path),
            "root": {"x": 512, "y": 896},
            "landmarks": {
                "root": {"x": 512, "y": 896}, "head": {"x": 512, "y": 320},
                "eye_left": {"x": 448, "y": 448}, "eye_right": {"x": 576, "y": 448},
                "hand_left": {"x": 280, "y": 560}, "hand_right": {"x": 744, "y": 560},
                "foot_left": {"x": 480, "y": 896}, "foot_right": {"x": 544, "y": 896}
            },
            "provenance": {"authored_by": "synthetic_fixture_builder", "method": "obvious geometric test pattern", "source_revision": "r04-v1"}
        }
        write_json(out / "sidecars" / sidecar_filename, frame)
        frames.append(frame)

    track = {
        "track_id": "synthetic:test_pulse:front:neutral:1", "family": "test_pulse",
        "facing": "front", "posture": "neutral", "variant": 1,
        "entry_posture": "neutral", "exit_posture": "neutral", "completion": "once",
        "frames": frames,
        "contacts": [{"landmark": "foot_left", "state": "planted", "start_tick": 0, "end_tick": 3}],
        "events": [{"name": "test_marker", "tick": 1, "frame_index": 1}],
        "interruption_ranges": [{"start_tick": 0, "end_tick": 3}]
    }
    track["track_checksum"] = hashlib.sha256(json.dumps(track, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    pack = {
        "profile": "MON_AUTHORED_FRAME_PACK_V1", "schema_version": 1,
        "pack_id": "00000000-0000-4000-8000-000000000404", "pack_revision": "synthetic-r04-v1",
        "body_revision": "synthetic-geometric-v1", "developmental_stage": "synthetic",
        "approval_state": "synthetic_test_only",
        "approved_references": {"identity_sha256": IDENTITY_SHA, "turnaround_sha256": TURNAROUND_SHA},
        "provenance": {"art_authority": "synthetic_test_fixture", "generation_or_edit_method": "obvious geometric test pattern", "source_authority": "COMPANION-P02-EMBODIMENT-001-R04", "rights_record": "project-authored synthetic test data; not production character art"},
        "timing": {"fps": 24, "tick_unit": "1/24_second"}, "tracks": [track], "source_runtime_relationships": []
    }
    write_json(out / "pack.json", pack)
    print(json.dumps({"status": "SYNTHETIC_TEST_PACK_BUILT", "frames": len(frames), "pack": str(out / "pack.json")}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
