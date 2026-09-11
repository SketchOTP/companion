#!/usr/bin/env python3
"""Fail-closed, byte-preserving MON_AUTHORED_FRAME_PACK_V1 intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
SCHEMA = ROOT / "contracts/schemas/mon-authored-frame-pack-v1.schema.json"
IDENTITY_SHA = "86ce1f9428f9a998d57e1a99c4245347d5a05e9f0bcf853c2b68065f351bdb56"
TURNAROUND_SHA = "3696c7d63594de38d408438d5b882f3207635bc63e59fb270f624715faeb09e4"
NAME = re.compile(r"^(?P<family>[a-z][a-z0-9_]{1,63})__(?P<facing>front|front_right|right|back_right|back|back_left|left|front_left)__(?P<posture>neutral|listening|acknowledging|walking)__v(?P<variant>[0-9]{2})__f(?P<frame>[0-9]{3})\.png$")


class IntakeError(Exception):
    def __init__(self, code: str, detail: str):
        super().__init__(detail)
        self.code = code


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def validate_schema(pack: dict) -> None:
    try:
        import jsonschema
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker()).validate(pack)
    except ImportError as exc:
        raise IntakeError("validator_unavailable", "jsonschema is required") from exc
    except Exception as exc:
        path = ".".join(str(item) for item in getattr(exc, "absolute_path", []))
        message = str(exc)
        if "landmarks" in path or "landmarks" in message:
            code = "landmark_missing"
        elif "duration_ticks" in path:
            code = "duration_invalid"
        else:
            code = "manifest_invalid"
        raise IntakeError(code, message) from exc


def eligible(state: str, operation: str) -> bool:
    return {
        "production": {"operator_approved"},
        "review": {"candidate", "operator_approved"},
        "test": {"synthetic_test_only"},
    }[operation].__contains__(state)


def validate_semantics(pack: dict) -> None:
    refs = pack["approved_references"]
    if refs != {"identity_sha256": IDENTITY_SHA, "turnaround_sha256": TURNAROUND_SHA}:
        raise IntakeError("approved_reference_mismatch", "approved reference hashes differ from authority")
    for track in pack["tracks"]:
        checksum = track["track_checksum"]
        unsigned = {key: value for key, value in track.items() if key != "track_checksum"}
        actual = hashlib.sha256(json.dumps(unsigned, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        if actual != checksum:
            raise IntakeError("track_checksum_mismatch", track["track_id"])
        total_ticks = sum(frame["duration_ticks"] for frame in track["frames"])
        expected_indexes = list(range(len(track["frames"])))
        if [frame["frame_index"] for frame in track["frames"]] != expected_indexes:
            raise IntakeError("manifest_invalid", f"non-contiguous frames for {track['track_id']}")
        if any(event["tick"] >= total_ticks for event in track["events"]):
            raise IntakeError("event_order_invalid", track["track_id"])
        if [event["tick"] for event in track["events"]] != sorted(event["tick"] for event in track["events"]):
            raise IntakeError("event_order_invalid", track["track_id"])
        for contact in track["contacts"]:
            if contact["start_tick"] >= contact["end_tick"] or contact["end_tick"] > total_ticks:
                raise IntakeError("contact_invalid", track["track_id"])
        for span in track["interruption_ranges"]:
            if span["start_tick"] >= span["end_tick"] or span["end_tick"] > total_ticks:
                raise IntakeError("contact_invalid", track["track_id"])


def validate_image(path: Path, expected_hash: str) -> None:
    if not path.is_file():
        raise IntakeError("source_missing", path.name)
    actual_hash = sha256(path)
    if actual_hash != expected_hash:
        raise IntakeError("source_hash_mismatch", path.name)
    try:
        with Image.open(path) as image:
            image.load()
            if image.format != "PNG" or image.size != (1024, 1024):
                raise IntakeError("wrong_dimensions", path.name)
            if image.mode != "RGBA":
                raise IntakeError("wrong_mode", path.name)
            if "srgb" not in image.info and "icc_profile" not in image.info:
                raise IntakeError("missing_srgb", path.name)
            alpha = image.getchannel("A")
            outside = Image.new("L", image.size, 0)
            outside.paste(alpha)
            # Zero the permitted safety region, then require no drawable pixels.
            outside.paste(0, (64, 32, 961, 961))
            if outside.getbbox() is not None:
                raise IntakeError("safety_region_violation", path.name)
    except IntakeError:
        raise
    except Exception as exc:
        raise IntakeError("source_invalid", f"{path.name}: {exc}") from exc


def intake(source: Path, output: Path, operation: str) -> dict:
    manifest_path = source / "pack.json"
    if not manifest_path.is_file():
        raise IntakeError("manifest_incomplete", "pack.json missing")
    try:
        pack = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise IntakeError("manifest_invalid", str(exc)) from exc
    validate_schema(pack)
    validate_semantics(pack)
    if not eligible(pack["approval_state"], operation):
        raise IntakeError("approval_ineligible", f"{pack['approval_state']} is ineligible for {operation}")

    relationships = []
    observations = []
    for track in pack["tracks"]:
        for frame in track["frames"]:
            filename = frame["filename"]
            match = NAME.fullmatch(filename)
            if not match:
                raise IntakeError("filename_invalid", filename)
            if (match["family"] != track["family"] or match["facing"] != track["facing"] or match["posture"] != track["posture"] or int(match["variant"]) != track["variant"] or int(match["frame"]) != frame["frame_index"]):
                raise IntakeError("filename_invalid", filename)
            if frame["sidecar_filename"] != filename.removesuffix(".png") + ".frame.json":
                raise IntakeError("filename_invalid", frame["sidecar_filename"])
            image_path = source / "frames" / filename
            sidecar_path = source / "sidecars" / frame["sidecar_filename"]
            if not sidecar_path.is_file():
                raise IntakeError("sidecar_missing", frame["sidecar_filename"])
            try:
                sidecar = json.loads(sidecar_path.read_text(encoding="utf-8"))
            except Exception as exc:
                raise IntakeError("sidecar_mismatch", str(exc)) from exc
            if sidecar != frame:
                raise IntakeError("sidecar_mismatch", frame["frame_id"])
            if frame["root"] != {"x": 512, "y": 896} or frame["landmarks"]["root"] != frame["root"]:
                raise IntakeError("root_mismatch", frame["frame_id"])
            validate_image(image_path, frame["source_sha256"])
            digest = frame["source_sha256"]
            cas_rel = Path("sources/sha256") / digest[:2] / f"{digest}.png"
            runtime_rel = Path("runtime/frames") / filename
            cas_path = output / cas_rel
            runtime_path = output / runtime_rel
            cas_path.parent.mkdir(parents=True, exist_ok=True)
            runtime_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(image_path, cas_path)
            shutil.copyfile(cas_path, runtime_path)
            input_bytes = image_path.read_bytes()
            if cas_path.read_bytes() != input_bytes or runtime_path.read_bytes() != input_bytes:
                raise IntakeError("byte_preservation_failed", filename)
            if sha256(cas_path) != digest or sha256(runtime_path) != digest:
                raise IntakeError("source_hash_mismatch", filename)
            relationships.append({"source_sha256": digest, "content_address": cas_rel.as_posix(), "runtime_asset": runtime_rel.as_posix()})
            observations.append({"frame_id": frame["frame_id"], "input_sha256": digest, "stored_sha256": sha256(cas_path), "runtime_sha256": sha256(runtime_path), "byte_identical": True})

    normalized = dict(pack)
    normalized["source_runtime_relationships"] = relationships
    stable(output / "pack.json", normalized)
    report = {"status": "PASSED", "profile": "MON_AUTHORED_FRAME_INTAKE_RESULT_V1", "operation": operation, "approval_state": pack["approval_state"], "source_bytes_mutated": False, "frames": observations}
    stable(output / "intake-report.json", report)
    return report


def identity_smoke(source: Path, output: Path) -> dict:
    if sha256(source) != IDENTITY_SHA:
        raise IntakeError("source_hash_mismatch", "approved identity smoke fixture")
    with Image.open(source) as image:
        if image.size != (1254, 1254) or image.mode != "RGBA":
            raise IntakeError("source_invalid", "approved identity metadata mismatch")
    target = output / "smoke/identity-approved.png"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    if target.read_bytes() != source.read_bytes() or sha256(target) != IDENTITY_SHA:
        raise IntakeError("byte_preservation_failed", "approved identity smoke fixture")
    result = {"status": "PASSED", "fixture_role": "one_frame_import_smoke_only", "candidate_art": False, "input_sha256": IDENTITY_SHA, "stored_sha256": sha256(target), "byte_identical": True}
    stable(output / "identity-smoke-report.json", result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("intake")
    run.add_argument("--source", type=Path, required=True)
    run.add_argument("--out", type=Path, required=True)
    run.add_argument("--operation", choices=("production", "review", "test"), required=True)
    smoke = sub.add_parser("identity-smoke")
    smoke.add_argument("--source", type=Path, required=True)
    smoke.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = intake(args.source.resolve(), args.out.resolve(), args.operation) if args.command == "intake" else identity_smoke(args.source.resolve(), args.out.resolve())
        print(json.dumps(result, sort_keys=True))
        return 0
    except IntakeError as exc:
        print(json.dumps({"status": "REJECTED", "reason": exc.code, "detail": str(exc)}, sort_keys=True), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
