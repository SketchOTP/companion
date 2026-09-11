#!/usr/bin/env python3
"""Exercise R04 source-intake positive and tamper-negative cases."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
BUILD = ROOT / "experiments/p02-embodiment/scripts/build_r04_synthetic_pack.py"
INTAKE = ROOT / "experiments/p02-embodiment/scripts/intake_authored_frame_pack.py"


def stable(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def invoke(source: Path, output: Path, operation: str = "test") -> tuple[int, dict]:
    result = subprocess.run(["python3", str(INTAKE), "intake", "--source", str(source), "--out", str(output), "--operation", operation], text=True, capture_output=True)
    stream = result.stdout if result.returncode == 0 else result.stderr
    return result.returncode, json.loads(stream.strip().splitlines()[-1])


def rewrite_frame(source: Path, mutator) -> None:
    pack_path = source / "pack.json"
    pack = json.loads(pack_path.read_text(encoding="utf-8"))
    frame = pack["tracks"][0]["frames"][0]
    image_path = source / "frames" / frame["filename"]
    mutator(image_path)
    frame["source_sha256"] = sha(image_path)
    stable(source / "sidecars" / frame["sidecar_filename"], frame)
    track = pack["tracks"][0]
    unsigned = {key: value for key, value in track.items() if key != "track_checksum"}
    track["track_checksum"] = hashlib.sha256(json.dumps(unsigned, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    stable(pack_path, pack)


def mutate_manifest(source: Path, mutator, rewrite_sidecar: bool = False) -> None:
    pack_path = source / "pack.json"
    pack = json.loads(pack_path.read_text(encoding="utf-8"))
    mutator(pack)
    if rewrite_sidecar and pack["tracks"][0]["frames"]:
        frame = pack["tracks"][0]["frames"][0]
        stable(source / "sidecars" / frame["sidecar_filename"], frame)
    track = pack["tracks"][0]
    unsigned = {key: value for key, value in track.items() if key != "track_checksum"}
    track["track_checksum"] = hashlib.sha256(json.dumps(unsigned, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    stable(pack_path, pack)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    evidence = args.out.resolve()
    evidence.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="companion-r04-intake-") as temporary:
        temp = Path(temporary)
        source = temp / "source"
        subprocess.run(["python3", str(BUILD), "--out", str(source), "--clean"], check=True, stdout=subprocess.DEVNULL)
        code, valid = invoke(source, temp / "valid")
        if code != 0 or valid.get("status") != "PASSED" or not all(frame["byte_identical"] for frame in valid["frames"]):
            raise AssertionError("valid byte-preserving intake failed")

        cases = {}
        def case(name: str, expected: str, edit, operation: str = "test") -> None:
            candidate = temp / name
            shutil.copytree(source, candidate)
            edit(candidate)
            returncode, result = invoke(candidate, temp / f"out-{name}", operation)
            if returncode == 0 or result.get("reason") != expected:
                raise AssertionError(f"{name}: expected {expected}, got {returncode} {result}")
            cases[name] = {"status": "REJECTED", "reason": result["reason"]}

        case("wrong_dimension", "wrong_dimensions", lambda p: rewrite_frame(p, lambda image: Image.open(image).resize((1000, 1024)).save(image, "PNG")))
        case("wrong_mode", "wrong_mode", lambda p: rewrite_frame(p, lambda image: Image.open(image).convert("RGB").save(image, "PNG")))
        case("source_hash_tamper", "source_hash_mismatch", lambda p: (p / "frames" / json.loads((p / "pack.json").read_text())["tracks"][0]["frames"][0]["filename"]).write_bytes(b"tampered"))
        case("approval_state", "approval_ineligible", lambda p: mutate_manifest(p, lambda d: d.__setitem__("approval_state", "candidate")), "production")
        case("missing_landmark", "landmark_missing", lambda p: mutate_manifest(p, lambda d: d["tracks"][0]["frames"][0]["landmarks"].pop("head"), True))
        case("contact_tamper", "contact_invalid", lambda p: mutate_manifest(p, lambda d: d["tracks"][0]["contacts"][0].__setitem__("end_tick", 99)))
        case("duration_tamper", "duration_invalid", lambda p: mutate_manifest(p, lambda d: d["tracks"][0]["frames"][0].__setitem__("duration_ticks", 0), True))
        case("event_order_tamper", "event_order_invalid", lambda p: mutate_manifest(p, lambda d: d["tracks"][0]["events"].extend([{"name": "late", "tick": 2, "frame_index": 1}, {"name": "early", "tick": 0, "frame_index": 0}])))

        result = {"status": "PASSED", "profile": "MON_R04_INTAKE_VALIDATION_V1", "valid_intake": valid, "negative_cases": cases, "production_pixels_generated": False}
        stable(evidence / "intake_validation.json", result)
        print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
