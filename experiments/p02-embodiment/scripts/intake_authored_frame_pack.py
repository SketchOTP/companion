#!/usr/bin/env python3
"""Fail-closed, byte-preserving intake for Architect-authored source packs.

The input ``MON_AUTHORED_FRAME_SOURCE_PACK_V1`` is immutable authority. Intake
copies it byte-for-byte into a fresh staged tree, emits a separate
``MON_INGESTED_FRAME_PACK_V1`` plus ``MON_FRAME_INTAKE_RECEIPT_V1``, and only
then atomically publishes the destination. No repair, resize, crop, recolor,
recompression, or inferred metadata is performed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import struct
import sys
import tempfile
import zlib
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
SOURCE_SCHEMA = ROOT / "contracts/schemas/mon-authored-frame-source-pack-v1.schema.json"
INGESTED_SCHEMA = ROOT / "contracts/schemas/mon-ingested-frame-pack-v1.schema.json"
IDENTITY_SHA = "86ce1f9428f9a998d57e1a99c4245347d5a05e9f0bcf853c2b68065f351bdb56"
TURNAROUND_SHA = "3696c7d63594de38d408438d5b882f3207635bc63e59fb270f624715faeb09e4"
NAME = re.compile(r"^(?P<family>[a-z][a-z0-9_]{1,63})__(?P<facing>front|front_right|right|back_right|back|back_left|left|front_left)__(?P<posture>neutral|listening|acknowledging|walking)__v(?P<variant>[0-9]{2})__f(?P<frame>[0-9]{3})\.png$")
FACING = {"front", "front_right", "right", "back_right", "back", "back_left", "left", "front_left"}


class IntakeError(Exception):
    def __init__(self, code: str, detail: str):
        super().__init__(detail)
        self.code = code


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def tree_digest(root: Path, exclude: set[str] | None = None) -> str:
    exclude = exclude or set()
    digest = hashlib.sha256()
    for path in sorted(p for p in root.rglob("*") if p.is_file() and p.relative_to(root).as_posix() not in exclude):
        rel = path.relative_to(root).as_posix().encode()
        data = path.read_bytes()
        digest.update(len(rel).to_bytes(4, "big")); digest.update(rel)
        digest.update(len(data).to_bytes(8, "big")); digest.update(data)
    return digest.hexdigest()


def _fsync_file(path: Path) -> None:
    with path.open("rb") as handle:
        os.fsync(handle.fileno())


def _fsync_tree(root: Path) -> None:
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        _fsync_file(path)
    for path in sorted((p for p in root.rglob("*") if p.is_dir()), key=lambda p: len(p.parts), reverse=True):
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)); os.fsync(fd); os.close(fd)
    fd = os.open(root, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)); os.fsync(fd); os.close(fd)


def validate_schema(pack: dict, schema_path: Path, label: str) -> None:
    try:
        import jsonschema
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker()).validate(pack)
    except ImportError as exc:
        raise IntakeError("validator_unavailable", "jsonschema is required") from exc
    except Exception as exc:
        path = ".".join(str(item) for item in getattr(exc, "absolute_path", []))
        message = str(exc)
        if "landmarks" in path and "required property" in message:
            code = "landmark_missing"
        elif "landmarks" in path:
            code = "landmark_state_invalid"
        elif "duration_ticks" in path:
            code = "duration_invalid"
        else:
            code = "manifest_invalid"
        raise IntakeError(code, f"{label}: {exc}") from exc


def eligible(state: str, operation: str) -> bool:
    return state in {"operator_approved"} if operation == "production" else state in {"candidate", "operator_approved"} if operation == "review" else state == "synthetic_test_only"


def _png_chunks(data: bytes):
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise IntakeError("png_signature_invalid", "PNG signature missing")
    offset = 8
    chunks = []
    seen_iend = False
    while offset + 12 <= len(data):
        length = struct.unpack(">I", data[offset:offset + 4])[0]
        kind = data[offset + 4:offset + 8]
        end = offset + 12 + length
        if end > len(data):
            raise IntakeError("png_truncated", "PNG chunk exceeds file")
        payload = data[offset + 8:offset + 8 + length]
        crc = struct.unpack(">I", data[offset + 8 + length:end])[0]
        if zlib.crc32(kind + payload) & 0xFFFFFFFF != crc:
            raise IntakeError("png_crc_invalid", kind.decode("latin1"))
        chunks.append((kind, payload))
        offset = end
        if kind == b"IEND":
            seen_iend = True
            break
    if not seen_iend or offset != len(data):
        raise IntakeError("png_trailing_or_missing_iend", "PNG must end immediately after one IEND")
    kinds = [kind for kind, _ in chunks]
    if kinds.count(b"IHDR") != 1 or kinds[0] != b"IHDR" or kinds.count(b"IEND") != 1 or kinds[-1] != b"IEND":
        raise IntakeError("png_chunk_order_invalid", "exactly one IHDR first and one IEND last required")
    ihdr = chunks[0][1]
    if len(ihdr) != 13 or ihdr[10:] != b"\x00\x00\x00":
        raise IntakeError("png_encoding_invalid", "compression, filter, and interlace must all be zero")
    return chunks


def validate_image(path: Path, expected_hash: str) -> dict:
    if not path.is_file():
        raise IntakeError("source_missing", path.name)
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != expected_hash:
        raise IntakeError("source_hash_mismatch", path.name)
    chunks = _png_chunks(data)
    ihdr = next((payload for kind, payload in chunks if kind == b"IHDR"), None)
    if ihdr is None or len(ihdr) != 13:
        raise IntakeError("png_ihdr_invalid", path.name)
    width, height, bit_depth, color_type = struct.unpack(">IIBB", ihdr[:10])
    if (width, height) != (1024, 1024):
        raise IntakeError("wrong_dimensions", path.name)
    if bit_depth != 8:
        raise IntakeError("png_bit_depth_invalid", path.name)
    if color_type != 6:
        raise IntakeError("png_color_type_invalid", path.name)
    srgb = [payload for kind, payload in chunks if kind == b"sRGB"]
    icc = [payload for kind, payload in chunks if kind == b"iCCP"]
    if not srgb:
        raise IntakeError("missing_srgb", path.name)
    if len(srgb) != 1:
        raise IntakeError("srgb_duplicate", path.name)
    if len(srgb[0]) != 1 or srgb[0][0] not in range(4):
        raise IntakeError("srgb_invalid", path.name)
    if icc:
        raise IntakeError("png_profile_conflict", path.name)
    try:
        with Image.open(path) as image:
            image.load()
            if image.format != "PNG" or image.size != (1024, 1024) or image.mode != "RGBA":
                raise IntakeError("wrong_mode", path.name)
            alpha = image.getchannel("A")
            amin, amax = alpha.getextrema()
            if amax == 0:
                raise IntakeError("blank_image", path.name)
            if amin > 0:
                raise IntakeError("opaque_background", path.name)
            pixels = alpha.load()
            if any(pixels[x, 0] != 0 or pixels[x, 1023] != 0 for x in range(1024)) or any(pixels[0, y] != 0 or pixels[1023, y] != 0 for y in range(1024)):
                raise IntakeError("transparent_perimeter_required", path.name)
            bbox = alpha.getbbox()
            if bbox is None or bbox[0] < 64 or bbox[1] < 32 or bbox[2] > 961 or bbox[3] > 961:
                raise IntakeError("safety_region_violation", path.name)
    except IntakeError:
        raise
    except Exception as exc:
        raise IntakeError("source_invalid", f"{path.name}: {exc}") from exc
    return {"png_signature": True, "width": width, "height": height, "bit_depth": bit_depth, "color_type": color_type, "srgb": True, "alpha_nonempty": True, "transparent_perimeter": True, "safety_region": True}


def _point_state_valid(value: dict, name: str) -> None:
    state = value.get("state")
    point = value.get("point")
    if state == "visible" and not isinstance(point, dict):
        raise IntakeError("landmark_state_invalid", name)
    if state in {"occluded", "not_applicable"} and point is not None:
        raise IntakeError("landmark_state_invalid", name)


def validate_request_profile(pack: dict) -> None:
    if pack.get("request_profile") != "phase02_bounded_motion_proof_v1":
        return
    required = {
        ("neutral_construction", "front", "front", "front"): (1, 1, "neutral", "neutral", "once"),
        ("neutral_construction", "right", "right", "right"): (1, 1, "neutral", "neutral", "once"),
        ("neutral_construction", "front_left", "front_left", "front_left"): (1, 1, "neutral", "neutral", "once"),
        ("idle_breathe", "front_left", "front_left", "front_left"): (6, 8, "neutral", "neutral", "loop"),
        ("walk", "front_left", "front_left", "front_left"): (8, 8, "walking", "walking", "loop"),
        ("orient_front_to_front_left", "front", "front", "front_left"): (4, 4, "neutral", "neutral", "once"),
        ("orient_front_left_to_front", "front_left", "front_left", "front"): (4, 4, "neutral", "neutral", "once"),
        ("listen_acknowledge", "front_left", "front_left", "front_left"): (6, 6, "listening", "acknowledging", "once"),
    }
    key = lambda track: (track.get("family"), track.get("selection_facing"), track.get("entry_facing"), track.get("exit_facing"))
    roles = [key(track) for track in pack["tracks"]]
    if len(roles) != len(set(roles)):
        raise IntakeError("request_profile_duplicate_role", "duplicate request role")
    seen = {key(track): track for track in pack["tracks"]}
    missing = sorted(set(required) - set(seen))
    if missing:
        raise IntakeError("request_profile_incomplete", ";".join("/".join(item) for item in missing))
    if len(seen) != len(required):
        raise IntakeError("request_profile_extra_track", str(len(seen) - len(required)))
    for role, (low, high, entry_posture, exit_posture, completion) in required.items():
        track = seen[role]
        if not low <= len(track.get("frames", [])) <= high:
            raise IntakeError("request_profile_count_invalid", role[0])
        if track.get("entry_posture") != entry_posture or track.get("exit_posture") != exit_posture or track.get("completion") != completion:
            raise IntakeError("request_profile_semantics_invalid", role[0])
        frames = track.get("frames", [])
        if frames and (frames[0].get("facing") != role[2] or frames[-1].get("facing") != role[3]):
            raise IntakeError("orientation_endpoint_mismatch", role[0])
        names = [event.get("name") for event in track.get("events", [])]
        if role[0].startswith("orient_") and names != ["facing_changed"]:
            raise IntakeError("request_profile_event_missing", role[0])
        if role[0] == "walk" and names != ["footfall_left", "footfall_right"]:
            raise IntakeError("request_profile_event_missing", role[0])
        if role[0] == "listen_acknowledge" and names != ["attention_acquired", "acknowledge", "settled"]:
            raise IntakeError("request_profile_event_missing", role[0])


def validate_semantics(pack: dict, source: Path | None = None) -> None:
    if pack["approved_references"] != {"identity_sha256": IDENTITY_SHA, "turnaround_sha256": TURNAROUND_SHA}:
        raise IntakeError("approved_reference_mismatch", "approved reference hashes differ from authority")
    assets = pack["source_assets"]
    ids = [asset["asset_id"] for asset in assets]; hashes = [asset["sha256"] for asset in assets]; names = [asset["filename"] for asset in assets]
    if len(ids) != len(set(ids)) or len(names) != len(set(names)):
        raise IntakeError("duplicate_source_asset", "asset IDs, hashes, and filenames must be unique")
    track_ids: set[str] = set(); frame_ids: set[str] = set(); filenames: set[str] = set(); sidecars: set[str] = set()
    asset_by_id = {asset["asset_id"]: asset for asset in assets}
    for track in pack["tracks"]:
        if track["track_id"] in track_ids:
            raise IntakeError("duplicate_track_id", track["track_id"])
        track_ids.add(track["track_id"])
        if track["entry_facing"] not in FACING or track["exit_facing"] not in FACING:
            raise IntakeError("facing_invalid", track["track_id"])
        unsigned = {key: value for key, value in track.items() if key != "track_checksum"}
        actual = hashlib.sha256(json.dumps(unsigned, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        if actual != track["track_checksum"]:
            raise IntakeError("track_checksum_mismatch", track["track_id"])
        total_ticks = sum(frame["duration_ticks"] for frame in track["frames"])
        hashes_in_track: set[str] = set(); expected = list(range(len(track["frames"])))
        if [frame["frame_index"] for frame in track["frames"]] != expected:
            raise IntakeError("frame_index_invalid", track["track_id"])
        for frame in track["frames"]:
            if frame["frame_id"] in frame_ids or frame["filename"] in filenames or frame["sidecar_filename"] in sidecars:
                raise IntakeError("duplicate_frame_identity", frame["frame_id"])
            frame_ids.add(frame["frame_id"]); filenames.add(frame["filename"]); sidecars.add(frame["sidecar_filename"])
            match = NAME.fullmatch(frame["filename"])
            if not match or frame["sidecar_filename"] != frame["filename"].removesuffix(".png") + ".frame.json":
                raise IntakeError("filename_invalid", frame["filename"])
            sidecar_path = Path("sidecars") / frame["sidecar_filename"]
            if source is not None and not (source / sidecar_path).is_file():
                raise IntakeError("sidecar_missing", frame["sidecar_filename"])
            if source is not None:
                try:
                    sidecar = json.loads((source / sidecar_path).read_text(encoding="utf-8"))
                except Exception as exc:
                    raise IntakeError("sidecar_invalid", frame["sidecar_filename"]) from exc
                if sidecar != frame:
                    raise IntakeError("sidecar_mismatch", frame["frame_id"])
            if match["family"] != track["family"] or match["facing"] != frame["facing"] or match["posture"] != frame["posture"] or int(match["frame"]) != frame["frame_index"]:
                raise IntakeError("filename_invalid", frame["filename"])
            asset = asset_by_id.get(frame["source_asset_id"])
            if asset is None or asset["sha256"] != frame["source_sha256"] or asset["filename"] != "frames/" + frame["filename"]:
                raise IntakeError("source_asset_mismatch", frame["frame_id"])
            for name, value in frame["landmarks"].items():
                _point_state_valid(value, name)
            if frame["landmarks"]["root"] != {"state": "visible", "point": {"x": 512, "y": 896}}:
                raise IntakeError("root_mismatch", frame["frame_id"])
            if frame["source_sha256"] in hashes_in_track and not frame.get("reuse_of"):
                raise IntakeError("duplicate_source_hash", frame["frame_id"])
            if frame.get("reuse_of"):
                prior = next((candidate for candidate in track["frames"] if candidate["frame_id"] == frame["reuse_of"]), None)
                if prior is None or prior["frame_index"] >= frame["frame_index"] or prior["source_sha256"] != frame["source_sha256"]:
                    raise IntakeError("reuse_reference_invalid", frame["frame_id"])
            hashes_in_track.add(frame["source_sha256"])
        for event in track["events"]:
            if event["tick"] >= total_ticks:
                raise IntakeError("event_tick_invalid", track["track_id"])
            start = sum(item["duration_ticks"] for item in track["frames"][:event["frame_index"]])
            end = start + track["frames"][event["frame_index"]]["duration_ticks"]
            if not start <= event["tick"] < end:
                raise IntakeError("event_tick_frame_mismatch", event["event_id"])
        if len({e["event_id"] for e in track["events"]}) != len(track["events"]):
            raise IntakeError("duplicate_event_id", track["track_id"])
        for span in [*track["contacts"], *track["interruption_ranges"]]:
            if span["start_tick"] >= span["end_tick"] or span["end_tick"] > total_ticks:
                raise IntakeError("contact_invalid", track["track_id"])
    validate_request_profile(pack)


def build_ingested(pack: dict, source: Path, stage: Path) -> tuple[dict, list[dict], dict]:
    source_tree = tree_digest(source)
    relationships: list[dict] = []; observations: list[dict] = []
    asset_map = {asset["asset_id"]: asset for asset in pack["source_assets"]}
    for asset in pack["source_assets"]:
        source_path = source / asset["filename"]
        if not source_path.is_file():
            raise IntakeError("source_missing", asset["filename"])
        profile = validate_image(source_path, asset["sha256"])
        cas_rel = Path("sources/sha256") / asset["sha256"][:2] / f"{asset['sha256']}.png"
        runtime_rel = Path("runtime/frames") / Path(asset["filename"]).name
        cas_path = stage / cas_rel; runtime_path = stage / runtime_rel
        cas_path.parent.mkdir(parents=True, exist_ok=True); runtime_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, cas_path); shutil.copyfile(source_path, runtime_path)
        raw = source_path.read_bytes(); cas_bytes = cas_path.read_bytes(); runtime_bytes = runtime_path.read_bytes()
        if not (raw == cas_bytes == runtime_bytes):
            raise IntakeError("byte_preservation_failed", asset["filename"])
        if not (sha256(cas_path) == sha256(runtime_path) == asset["sha256"]):
            raise IntakeError("stored_hash_mismatch", asset["filename"])
        relationships.append({"asset_id": asset["asset_id"], "source_sha256": asset["sha256"], "source_filename": asset["filename"], "content_address": cas_rel.as_posix(), "runtime_asset": runtime_rel.as_posix(), "validation": profile})
        observations.append({"frame_id": next(frame["frame_id"] for track in pack["tracks"] for frame in track["frames"] if frame["source_asset_id"] == asset["asset_id"]), "source_asset_id": asset["asset_id"], "input_sha256": asset["sha256"], "stored_sha256": sha256(cas_path), "runtime_sha256": sha256(runtime_path), "byte_identical": True})
    ingested = {key: value for key, value in pack.items() if key not in {"profile", "schema_version", "pack_id", "source_assets", "tracks"}}
    ingested.update({"profile": "MON_INGESTED_FRAME_PACK_V1", "schema_version": 1, "source_profile": "MON_AUTHORED_FRAME_SOURCE_PACK_V1", "source_pack_id": pack["pack_id"]})
    ingested["source_assets"] = relationships; ingested["tracks"] = pack["tracks"]
    ingested["pack_digest"] = hashlib.sha256(json.dumps(ingested, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return ingested, observations, {"source_tree_sha256": source_tree, "source_pack_sha256": sha256(source / "pack.json")}


def intake(source: Path, output: Path, operation: str) -> dict:
    if output.exists() and any(output.iterdir()):
        raise IntakeError("destination_not_empty", str(output))
    manifest_path = source / "pack.json"
    if not manifest_path.is_file():
        raise IntakeError("manifest_incomplete", "pack.json missing")
    try:
        pack = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise IntakeError("manifest_invalid", str(exc)) from exc
    validate_schema(pack, SOURCE_SCHEMA, "source pack")
    validate_semantics(pack, source)
    if not eligible(pack["approval_state"], operation):
        raise IntakeError("approval_ineligible", f"{pack['approval_state']} is ineligible for {operation}")
    output.parent.mkdir(parents=True, exist_ok=True)
    if os.stat(source).st_dev != os.stat(output.parent).st_dev:
        raise IntakeError("cross_filesystem_destination", "staging and final output must share a filesystem")
    stage = Path(tempfile.mkdtemp(prefix=f".{output.name}.stage-", dir=output.parent))
    try:
        source_copy = stage / "source"; shutil.copytree(source, source_copy)
        ingested, observations, source_meta = build_ingested(pack, source, stage)
        stable(stage / "pack.json", ingested)
        validate_schema(ingested, INGESTED_SCHEMA, "ingested pack")
        ingested_hash = sha256(stage / "pack.json")
        stable(stage / "receipt.json", {"profile": "MON_FRAME_INTAKE_RECEIPT_V1", "schema_version": 1, "operation": operation, "validation_profile": pack["request_profile"], "source_pack_sha256": source_meta["source_pack_sha256"], "source_tree_sha256": source_meta["source_tree_sha256"], "ingested_pack_sha256": ingested_hash, "output_tree_sha256": "0" * 64, "publication_state": "staged", "source_bytes_mutated": False, "frames": observations, "validation": {"status": "PASSED", "errors": []}})
        receipt = json.loads((stage / "receipt.json").read_text(encoding="utf-8")); receipt["output_tree_sha256"] = tree_digest(stage, {"receipt.json"}); receipt["publication_state"] = "published"; stable(stage / "receipt.json", receipt)
        validate_schema(receipt, ROOT / "contracts/schemas/mon-frame-intake-receipt-v1.schema.json", "intake receipt")
        if os.environ.get("COMPANION_INTAKE_FAIL_AFTER_STAGE") == "1":
            raise IntakeError("injected_mid_intake_failure", "test-only failure before publish")
        _fsync_tree(stage)
        if output.exists() and any(output.iterdir()):
            raise IntakeError("destination_not_empty", str(output))
        if output.exists():
            output.rmdir()
        os.replace(stage, output)
        fd = os.open(output.parent, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)); os.fsync(fd); os.close(fd)
        return {"status": "PASSED", "profile": "MON_FRAME_INTAKE_RECEIPT_V1", "operation": operation, "approval_state": pack["approval_state"], "ingested_pack": "pack.json", "receipt": "receipt.json", "source_bytes_mutated": False, "frames": observations, "source_tree_sha256": source_meta["source_tree_sha256"], "ingested_pack_sha256": ingested_hash, "output_tree_sha256": receipt["output_tree_sha256"]}
    except Exception:
        shutil.rmtree(stage, ignore_errors=True)
        raise


def identity_smoke(source: Path, output: Path) -> dict:
    if sha256(source) != IDENTITY_SHA:
        raise IntakeError("source_hash_mismatch", "approved identity smoke fixture")
    with Image.open(source) as image:
        if image.size != (1254, 1254) or image.mode != "RGBA":
            raise IntakeError("source_invalid", "approved identity metadata mismatch")
    target = output / "smoke/identity-approved.png"; target.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(source, target)
    if target.read_bytes() != source.read_bytes():
        raise IntakeError("byte_preservation_failed", "approved identity smoke fixture")
    result = {"status": "PASSED", "fixture_role": "one_frame_import_smoke_only", "candidate_art": False, "input_sha256": IDENTITY_SHA, "stored_sha256": sha256(target), "byte_identical": True}
    stable(output / "identity-smoke-report.json", result); return result


def main() -> int:
    parser = argparse.ArgumentParser(); sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("intake"); run.add_argument("--source", type=Path, required=True); run.add_argument("--out", type=Path, required=True); run.add_argument("--operation", choices=("production", "review", "test"), required=True)
    smoke = sub.add_parser("identity-smoke"); smoke.add_argument("--source", type=Path, required=True); smoke.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = intake(args.source.resolve(), args.out.resolve(), args.operation) if args.command == "intake" else identity_smoke(args.source.resolve(), args.out.resolve())
        print(json.dumps(result, sort_keys=True)); return 0
    except IntakeError as exc:
        print(json.dumps({"status": "REJECTED", "reason": exc.code, "detail": str(exc)}, sort_keys=True), file=sys.stderr); return 1


if __name__ == "__main__":
    raise SystemExit(main())
