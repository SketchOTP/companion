#!/usr/bin/env python3
"""Fail-closed negative matrix for the authored-frame intake boundary.

All images generated here are unmistakably synthetic calibration geometry. No
production character pixels are created or repaired by this test.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import shutil
import subprocess
import struct
import tempfile
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
BUILD = ROOT / "experiments/p02-embodiment/scripts/build_r04_synthetic_pack.py"
INTAKE = ROOT / "experiments/p02-embodiment/scripts/intake_authored_frame_pack.py"
sys.path.insert(0, str(INTAKE.parent))
from intake_authored_frame_pack import IntakeError, validate_request_profile


def stable(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def invoke(source: Path, output: Path, operation: str = "test") -> tuple[int, dict]:
    result = subprocess.run(
        ["python3", str(INTAKE), "intake", "--source", str(source), "--out", str(output), "--operation", operation],
        text=True, capture_output=True,
    )
    stream = result.stdout if result.returncode == 0 else result.stderr
    try:
        return result.returncode, json.loads(stream.strip().splitlines()[-1])
    except (json.JSONDecodeError, IndexError):
        return result.returncode, {"status": "UNKNOWN", "detail": stream[-500:]}


def edit_manifest(source: Path, mutate, *, update_sidecar: bool = False) -> None:
    manifest = source / "pack.json"
    pack = json.loads(manifest.read_text(encoding="utf-8"))
    mutate(pack)
    track = pack["tracks"][0]
    if update_sidecar and track["frames"]:
        frame = track["frames"][0]
        stable(source / "sidecars" / frame["sidecar_filename"], frame)
    unsigned = {key: value for key, value in track.items() if key != "track_checksum"}
    track["track_checksum"] = hashlib.sha256(json.dumps(unsigned, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    stable(manifest, pack)


def mutate_image(source: Path, transform, *, update_manifest_hash: bool = True) -> None:
    pack = json.loads((source / "pack.json").read_text(encoding="utf-8"))
    frame = pack["tracks"][0]["frames"][0]
    path = source / "frames" / frame["filename"]
    transform(path)
    if update_manifest_hash:
        digest = sha(path)
        frame["source_sha256"] = digest
        for asset in pack["source_assets"]:
            if asset["asset_id"] == frame["source_asset_id"]:
                asset["sha256"] = digest
        stable(source / "sidecars" / frame["sidecar_filename"], frame)
        track = pack["tracks"][0]
        unsigned = {key: value for key, value in track.items() if key != "track_checksum"}
        track["track_checksum"] = hashlib.sha256(json.dumps(unsigned, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    stable(source / "pack.json", pack)


def remove_srgb(path: Path) -> None:
    data = path.read_bytes(); out = bytearray(data[:8]); offset = 8
    while offset + 12 <= len(data):
        length = struct.unpack(">I", data[offset:offset + 4])[0]
        chunk = data[offset:offset + 12 + length]
        if data[offset + 4:offset + 8] != b"sRGB":
            out.extend(chunk)
        offset += 12 + length
        if chunk[4:8] == b"IEND":
            break
    path.write_bytes(out)


def mutate_ihdr_bit_depth(path: Path, bit_depth: int) -> None:
    data = bytearray(path.read_bytes())
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise AssertionError("synthetic fixture is not a PNG with IHDR")
    data[24] = bit_depth
    data[29:33] = struct.pack(">I", __import__("zlib").crc32(data[12:29]) & 0xFFFFFFFF)
    path.write_bytes(data)


def blank_image(path: Path) -> None:
    Image.new("RGBA", (1024, 1024), (0, 0, 0, 0)).save(path, "PNG", optimize=False)
    # Exercise the blank-image rule independently of the sRGB rule.
    data = path.read_bytes(); length = struct.unpack(">I", data[8:12])[0]; split = 16 + length + 4
    payload = b"\x00"; kind = b"sRGB"; chunk = struct.pack(">I", 1) + kind + payload + struct.pack(">I", __import__("zlib").crc32(kind + payload) & 0xFFFFFFFF)
    path.write_bytes(data[:split] + chunk + data[split:])


def opaque_image(path: Path) -> None:
    Image.new("RGBA", (1024, 1024), (0, 190, 255, 255)).save(path, "PNG", optimize=False)
    data = path.read_bytes(); length = struct.unpack(">I", data[8:12])[0]; split = 16 + length + 4
    payload = b"\x00"; kind = b"sRGB"; chunk = struct.pack(">I", 1) + kind + payload + struct.pack(">I", __import__("zlib").crc32(kind + payload) & 0xFFFFFFFF)
    path.write_bytes(data[:split] + chunk + data[split:])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    evidence = args.out.resolve()
    evidence.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="companion-r04-c01-intake-") as temporary:
        temp = Path(temporary)
        source = temp / "source"
        subprocess.run(["python3", str(BUILD), "--out", str(source), "--clean"], check=True, stdout=subprocess.DEVNULL)
        code, valid = invoke(source, temp / "valid")
        if code or valid.get("status") != "PASSED" or not all(row.get("byte_identical") for row in valid.get("frames", [])):
            raise AssertionError(f"valid byte-preserving intake failed: {valid}")

        cases: dict[str, dict] = {}

        def case(name: str, expected: str, edit, operation: str = "test", *, preserve_output: bool = False) -> None:
            candidate = temp / name
            shutil.copytree(source, candidate)
            edit(candidate)
            output = temp / f"out-{name}"
            returncode, result = invoke(candidate, output, operation)
            if returncode == 0 or result.get("reason") != expected:
                raise AssertionError(f"{name}: expected {expected}, got {returncode} {result}")
            if not preserve_output and output.exists() and any(output.iterdir()):
                raise AssertionError(f"{name}: failed intake left published output")
            cases[name] = {"status": "REJECTED", "reason": result["reason"]}

        case("wrong_dimension", "wrong_dimensions", lambda p: mutate_image(p, lambda f: Image.open(f).resize((1000, 1024)).save(f, "PNG")))
        case("wrong_mode", "png_color_type_invalid", lambda p: mutate_image(p, lambda f: Image.open(f).convert("RGB").save(f, "PNG")))
        case("source_hash_tamper", "source_hash_mismatch", lambda p: mutate_image(p, lambda f: f.write_bytes(b"tampered"), update_manifest_hash=False))
        case("approval_state", "approval_ineligible", lambda p: edit_manifest(p, lambda d: d.__setitem__("approval_state", "candidate")), "production")
        case("missing_landmark", "landmark_missing", lambda p: edit_manifest(p, lambda d: d["tracks"][0]["frames"][0]["landmarks"].pop("head_center"), update_sidecar=True))
        case("contact_tamper", "contact_invalid", lambda p: edit_manifest(p, lambda d: d["tracks"][0]["contacts"][0].__setitem__("end_tick", 99)))
        case("duration_tamper", "duration_invalid", lambda p: edit_manifest(p, lambda d: d["tracks"][0]["frames"][0].__setitem__("duration_ticks", 0), update_sidecar=True))
        case("event_tick_tamper", "event_tick_frame_mismatch", lambda p: edit_manifest(p, lambda d: d["tracks"][0]["events"].__setitem__(0, {"event_id": "test_marker_001", "name": "test_marker", "tick": 0, "frame_index": 1})))
        case("duplicate_asset", "duplicate_source_asset", lambda p: edit_manifest(p, lambda d: d["source_assets"].append(copy.deepcopy(d["source_assets"][0]))) )
        case("missing_srgb", "missing_srgb", lambda p: mutate_image(p, remove_srgb))
        case("invalid_landmark_state", "landmark_state_invalid", lambda p: edit_manifest(p, lambda d: d["tracks"][0]["frames"][0]["landmarks"]["root"].__setitem__("state", "occluded"), update_sidecar=True))
        case("duplicate_frame_id", "duplicate_frame_identity", lambda p: edit_manifest(p, lambda d: d["tracks"][0]["frames"][1].__setitem__("frame_id", d["tracks"][0]["frames"][0]["frame_id"])))
        case("duplicate_track_id", "duplicate_track_id", lambda p: edit_manifest(p, lambda d: d["tracks"].append(copy.deepcopy(d["tracks"][0]))) )
        case("incomplete_profile", "request_profile_incomplete", lambda p: edit_manifest(p, lambda d: d.__setitem__("request_profile", "phase02_bounded_motion_proof_v1")))
        case("sixteen_bit_rgba", "png_bit_depth_invalid", lambda p: mutate_image(p, lambda f: mutate_ihdr_bit_depth(f, 16)))
        case("blank_image", "blank_image", lambda p: mutate_image(p, blank_image))
        case("opaque_background", "opaque_background", lambda p: mutate_image(p, opaque_image))
        case("path_traversal", "manifest_invalid", lambda p: edit_manifest(p, lambda d: d["tracks"][0]["frames"][0].__setitem__("filename", "../escape.png"), update_sidecar=True))

        profile_required = {
            "neutral_front": ("front", "front", 1), "neutral_profile": ("left", "left", 1),
            "neutral_front_left": ("front_left", "front_left", 1), "idle_breathe": ("front_left", "front_left", 6),
            "walk": ("front_left", "front_left", 8), "orient_front_to_front_left": ("front", "front_left", 4),
            "orient_front_left_to_front": ("front_left", "front", 4), "listen_acknowledge": ("front_left", "front_left", 6),
        }
        profile_tracks = [{"family": family, "entry_facing": entry, "exit_facing": exit_, "frames": [{}] * count, "events": [{}]}
                          for family, (entry, exit_, count) in profile_required.items()]
        profile_tracks[-3]["entry_facing"] = "front_left"
        try:
            validate_request_profile({"request_profile": "phase02_bounded_motion_proof_v1", "tracks": profile_tracks})
        except IntakeError as exc:
            if exc.code != "orientation_endpoint_mismatch":
                raise AssertionError(f"orientation profile expected endpoint rejection, got {exc.code}")
            cases["orientation_endpoint"] = {"status": "REJECTED", "reason": exc.code}
        else:
            raise AssertionError("orientation profile mismatch was accepted")

        stale_candidate = temp / "stale-destination-source"
        shutil.copytree(source, stale_candidate)
        stale_output = temp / "stale-destination-output"
        stale_output.mkdir(); (stale_output / "old.txt").write_text("preserve", encoding="utf-8")
        stale_code, stale_result = invoke(stale_candidate, stale_output)
        if stale_code == 0 or stale_result.get("reason") != "destination_not_empty" or (stale_output / "old.txt").read_text(encoding="utf-8") != "preserve":
            raise AssertionError(f"stale destination was not rejected/preserved: {stale_code} {stale_result}")
        cases["stale_destination"] = {"status": "REJECTED", "reason": stale_result["reason"]}

        result = {
            "status": "PASSED",
            "profile": "MON_R04_C01_INTAKE_VALIDATION_V1",
            "valid_intake": valid,
            "negative_cases": cases,
            "production_pixels_generated": False,
            "atomic_publication": True,
            "invalid_accepted": 0,
            "category_equations": {"requested_total": len(cases), "accepted": 0, "rejected": len(cases), "duplicate": 0},
        }
        stable(evidence / "intake_validation.json", result)
        print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
