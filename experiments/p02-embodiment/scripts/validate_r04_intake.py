#!/usr/bin/env python3
"""Fail-closed C02 intake/profile negative matrix (synthetic geometry only)."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import shutil
import struct
import subprocess
import tempfile
import zlib
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
BUILD = ROOT / "experiments/p02-embodiment/scripts/build_r04_synthetic_pack.py"
INTAKE = ROOT / "experiments/p02-embodiment/scripts/intake_authored_frame_pack.py"


def stable(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def recalc(pack: dict) -> None:
    for track in pack["tracks"]:
        track["track_checksum"] = hashlib.sha256(json.dumps({k: v for k, v in track.items() if k != "track_checksum"}, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    stable(pack["_path"], {k: v for k, v in pack.items() if k != "_path"})


def invoke(source: Path, output: Path, operation: str = "test", *, injected_failure: bool = False) -> tuple[int, dict]:
    env = os.environ.copy()
    if injected_failure:
        env["COMPANION_INTAKE_FAIL_AFTER_STAGE"] = "1"
    result = subprocess.run(["python3", str(INTAKE), "intake", "--source", str(source), "--out", str(output), "--operation", operation], text=True, capture_output=True, env=env)
    stream = result.stdout if result.returncode == 0 else result.stderr
    try:
        return result.returncode, json.loads(stream.strip().splitlines()[-1])
    except (json.JSONDecodeError, IndexError):
        return result.returncode, {"status": "UNKNOWN", "detail": stream[-500:]}


def load_pack(source: Path) -> dict:
    pack = json.loads((source / "pack.json").read_text(encoding="utf-8")); pack["_path"] = source / "pack.json"; return pack


def write_pack(source: Path, pack: dict) -> None:
    pack["_path"] = source / "pack.json"; recalc(pack)


def track(pack: dict, family: str, facing: str | None = None) -> dict:
    for item in pack["tracks"]:
        if item["family"] == family and (facing is None or item["selection_facing"] == facing): return item
    raise KeyError(family)


def mutate_image(source: Path, transform, *, update_manifest_hash: bool = True) -> None:
    pack = load_pack(source); item = pack["tracks"][0]["frames"][0]; path = source / "frames" / item["filename"]; transform(path)
    if update_manifest_hash:
        digest = sha(path); item["source_sha256"] = digest
        for asset in pack["source_assets"]:
            if asset["asset_id"] == item["source_asset_id"]: asset["sha256"] = digest
        stable(source / "sidecars" / item["sidecar_filename"], item)
    write_pack(source, pack)


def add_chunk(path: Path, kind: bytes, payload: bytes, *, before_ihdr: bool = False) -> None:
    data = path.read_bytes(); chunk = struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF)
    if before_ihdr: path.write_bytes(data[:8] + chunk + data[8:]); return
    length = struct.unpack(">I", data[8:12])[0]; split = 16 + length + 4; path.write_bytes(data[:split] + chunk + data[split:])


def remove_chunk(path: Path, kind_wanted: bytes) -> None:
    data = path.read_bytes(); out = bytearray(data[:8]); offset = 8
    while offset + 12 <= len(data):
        length = struct.unpack(">I", data[offset:offset + 4])[0]; chunk = data[offset:offset + 12 + length]; offset += len(chunk)
        if chunk[4:8] != kind_wanted: out.extend(chunk)
        if chunk[4:8] == b"IEND": break
    path.write_bytes(out)


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--out", type=Path, required=True); args = parser.parse_args(); evidence = args.out.resolve(); evidence.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="companion-r04-c02-intake-") as temporary:
        temp = Path(temporary); source = temp / "source"; subprocess.run(["python3", str(BUILD), "--out", str(source), "--clean"], check=True, stdout=subprocess.DEVNULL)
        code, valid = invoke(source, temp / "valid")
        if code or valid.get("status") != "PASSED": raise AssertionError(f"positive intake failed: {valid}")
        cases: dict[str, dict] = {}

        def case(name: str, expected: str, edit, operation: str = "test") -> None:
            candidate = temp / name; shutil.copytree(source, candidate); edit(candidate); output = temp / f"out-{name}"; rc, result = invoke(candidate, output, operation)
            if rc == 0 or result.get("reason") != expected: raise AssertionError(f"{name}: expected {expected}, got {rc} {result}")
            if output.exists() and any(output.iterdir()): raise AssertionError(f"{name}: failed intake published output")
            cases[name] = {"status": "REJECTED", "reason": result["reason"]}

        case("right_profile_mismatch", "request_profile_incomplete", lambda p: (lambda d: (d["tracks"][1].update({"entry_facing": "left", "exit_facing": "left"}), write_pack(p, d)))(load_pack(p)))
        case("missing_neutral_role", "request_profile_incomplete", lambda p: (lambda d: (d["tracks"].pop(1), write_pack(p, d)))(load_pack(p)))
        def duplicate_role(p: Path) -> None:
            d = load_pack(p); dupe = copy.deepcopy(d["tracks"][0]); source_frame = dupe["frames"][0]; old_name = source_frame["filename"]
            new_name = "neutral_construction__front__neutral__v02__f000.png"; new_sidecar = new_name.removesuffix(".png") + ".frame.json"
            shutil.copyfile(p / "frames" / old_name, p / "frames" / new_name)
            source_frame.update({"frame_id": "duplicate_neutral_front_000", "filename": new_name, "sidecar_filename": new_sidecar, "source_asset_id": "asset_duplicate_neutral_front_000"})
            digest = sha(p / "frames" / new_name); source_frame["source_sha256"] = digest
            stable(p / "sidecars" / new_sidecar, source_frame)
            d["source_assets"].append({"asset_id": "asset_duplicate_neutral_front_000", "filename": "frames/" + new_name, "sha256": digest})
            dupe["track_id"] = "synthetic:duplicate:front:2"; write_pack(p, d | {"tracks": d["tracks"] + [dupe]})
        case("duplicate_neutral_role", "request_profile_duplicate_role", duplicate_role)
        def endpoint(p: Path) -> None:
            d = load_pack(p); t = track(d, "orient_front_to_front_left"); t["frames"][-1]["facing"] = "front"; stable(p / "sidecars" / t["frames"][-1]["sidecar_filename"], t["frames"][-1]); write_pack(p, d)
        case("wrong_entry_exit_frame_facing", "filename_invalid", endpoint)
        def missing_facing_event(p: Path) -> None:
            d = load_pack(p); track(d, "orient_front_to_front_left")["events"] = []; write_pack(p, d)
        case("missing_facing_changed", "request_profile_event_missing", missing_facing_event)
        def walk_events(p: Path) -> None:
            d = load_pack(p); track(d, "walk")["events"] = [{"event_id": "wrong", "name": "other", "tick": 0, "frame_index": 0}]; write_pack(p, d)
        case("missing_walk_footfalls", "request_profile_event_missing", walk_events)
        def listen_order(p: Path) -> None:
            d = load_pack(p); t = track(d, "listen_acknowledge"); t["events"] = list(reversed(t["events"])); write_pack(p, d)
        case("listen_acknowledge_order", "request_profile_event_missing", listen_order)
        def reuse_bad(p: Path) -> None:
            d = load_pack(p); t = track(d, "idle_breathe"); t["frames"][-1]["reuse_of"] = "missing_reuse_target"; stable(p / "sidecars" / t["frames"][-1]["sidecar_filename"], t["frames"][-1]); write_pack(p, d)
        case("invalid_reuse_target_hash", "reuse_reference_invalid", reuse_bad)
        case("wrong_dimension", "wrong_dimensions", lambda p: mutate_image(p, lambda f: Image.open(f).resize((1000, 1024)).save(f, "PNG")))
        case("wrong_mode", "png_color_type_invalid", lambda p: mutate_image(p, lambda f: Image.open(f).convert("RGB").save(f, "PNG")))
        case("source_hash_tamper", "source_hash_mismatch", lambda p: mutate_image(p, lambda f: f.write_bytes(b"tampered"), update_manifest_hash=False))
        case("approval_state", "approval_ineligible", lambda p: (lambda d: (d.update({"approval_state": "candidate"}), write_pack(p, d)))(load_pack(p)), "production")
        case("missing_srgb", "missing_srgb", lambda p: mutate_image(p, lambda f: remove_chunk(f, b"sRGB")))
        case("iccp_only_false_srgb", "missing_srgb", lambda p: mutate_image(p, lambda f: (remove_chunk(f, b"sRGB"), add_chunk(f, b"iCCP", b"FakeICC\x00\x00"))))
        case("duplicate_srgb", "srgb_duplicate", lambda p: mutate_image(p, lambda f: add_chunk(f, b"sRGB", b"\x00")))
        case("trailing_bytes", "png_trailing_or_missing_iend", lambda p: mutate_image(p, lambda f: f.write_bytes(f.read_bytes() + b"tail")))
        case("malformed_chunk_order", "png_chunk_order_invalid", lambda p: mutate_image(p, lambda f: add_chunk(f, b"tEXt", b"bad", before_ihdr=True)))
        def mid_failure(p: Path) -> None:
            out = temp / "out-mid-intake"; rc, result = invoke(p, out, injected_failure=True)
            if rc == 0 or result.get("reason") != "injected_mid_intake_failure" or out.exists(): raise AssertionError(f"mid-intake failure not fail-closed: {rc} {result}")
        mid_failure(source); cases["mid_intake_failure"] = {"status": "REJECTED", "reason": "injected_mid_intake_failure"}
        stale_output = temp / "stale-output"; stale_output.mkdir(); (stale_output / "old.txt").write_text("preserve", encoding="utf-8"); rc, result = invoke(source, stale_output)
        if rc == 0 or result.get("reason") != "destination_not_empty": raise AssertionError("stale output accepted")
        cases["stale_output"] = {"status": "REJECTED", "reason": result["reason"]}
        result = {"status": "PASSED", "profile": "MON_R04_C02_INTAKE_VALIDATION_V1", "positive_pack": "phase02_bounded_motion_proof_v1", "valid_intake": valid, "negative_cases": cases, "production_pixels_generated": False, "atomic_publication": True, "mid_intake_failure_fail_closed": True, "invalid_accepted": 0, "category_equations": {"requested_total": len(cases), "accepted": 0, "rejected": len(cases), "duplicate": 0}}
        stable(evidence / "intake_validation.json", result); print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__": raise SystemExit(main())
