#!/usr/bin/env python3
"""Build the bounded R05 candidate pack from operator-authorized imagegen sheets.

The image model authors the visible character pixels. This builder performs only
deterministic sheet-cell extraction, chroma-to-alpha conversion, uniform
MON_FRAME_V1 normalization, source-sidecar assembly, and review derivatives.
It never redraws anatomy or invents in-between poses.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import struct
import uuid
import zlib
from dataclasses import dataclass
from pathlib import Path
from statistics import median

from PIL import Image, ImageDraw

IDENTITY_SHA = "86ce1f9428f9a998d57e1a99c4245347d5a05e9f0bcf853c2b68065f351bdb56"
TURNAROUND_SHA = "3696c7d63594de38d408438d5b882f3207635bc63e59fb270f624715faeb09e4"
FRAME_SIZE = 1024
ROOT = (512, 896)
SAFETY = (64, 32, 961, 961)


@dataclass(frozen=True)
class SheetSpec:
    name: str
    filename: str
    columns: int
    rows: int


SHEETS = {
    "construction": SheetSpec("construction", "neutral-construction-sheet.png", 3, 1),
    "profile": SheetSpec("profile", "neutral-right-profile.png", 1, 1),
    "idle": SheetSpec("idle", "idle-breathe-sheet.png", 4, 2),
    "walk": SheetSpec("walk", "walk-sheet.png", 4, 2),
    "orient": SheetSpec("orient", "orient-front-to-front-left-sheet.png", 4, 1),
    "listen": SheetSpec("listen", "listen-acknowledge-sheet.png", 3, 2),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def add_srgb_chunk(path: Path) -> None:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise ValueError(f"not a PNG: {path}")
    length = struct.unpack(">I", data[8:12])[0]
    split = 16 + length + 4
    payload = b"\x00"
    kind = b"sRGB"
    chunk = (
        struct.pack(">I", len(payload))
        + kind
        + payload
        + struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF)
    )
    path.write_bytes(data[:split] + chunk + data[split:])


def chroma_to_alpha(image: Image.Image) -> Image.Image:
    """Remove the deliberately green imagegen background without redrawing."""
    result: list[tuple[int, int, int, int]] = []
    for red, green, blue in image.convert("RGB").getdata():
        dominance = green - max(red, blue)
        if green >= 145 and dominance >= 42:
            alpha = 0 if dominance >= 96 else round(255 * (96 - dominance) / 54)
            if alpha <= 0:
                result.append((0, 0, 0, 0))
                continue
            amount = alpha / 255.0
            clean_red = max(0, min(255, round(red / amount)))
            clean_blue = max(0, min(255, round(blue / amount)))
            clean_green = max(0, min(255, round((green - (1.0 - amount) * 255) / amount)))
            result.append((clean_red, clean_green, clean_blue, alpha))
        else:
            result.append((red, green, blue, 255))
    output = Image.new("RGBA", image.size)
    output.putdata(result)
    return output


def split_sheet(path: Path, spec: SheetSpec) -> list[Image.Image]:
    image = Image.open(path).convert("RGB")
    cells: list[Image.Image] = []
    for row in range(spec.rows):
        for column in range(spec.columns):
            x0 = round(column * image.width / spec.columns)
            x1 = round((column + 1) * image.width / spec.columns)
            y0 = round(row * image.height / spec.rows)
            y1 = round((row + 1) * image.height / spec.rows)
            cells.append(chroma_to_alpha(image.crop((x0, y0, x1, y1))))
    return cells


def normalized_cells(cells: list[Image.Image]) -> list[Image.Image]:
    boxes = [cell.getchannel("A").getbbox() for cell in cells]
    if any(box is None for box in boxes):
        raise ValueError("blank imagegen cell")
    concrete = [box for box in boxes if box is not None]
    heights = [box[3] - box[1] for box in concrete]
    scale = 800.0 / median(heights)
    for box in concrete:
        anchor_x = (box[0] + box[2]) / 2.0
        left_room = anchor_x - box[0]
        right_room = box[2] - anchor_x
        top_room = box[3] - box[1]
        scale = min(
            scale,
            (ROOT[0] - SAFETY[0]) / max(left_room, 1),
            (SAFETY[2] - 1 - ROOT[0]) / max(right_room, 1),
            (ROOT[1] - SAFETY[1]) / max(top_room, 1),
        )
    scale *= 0.985
    output: list[Image.Image] = []
    for cell, box in zip(cells, concrete, strict=True):
        resized = cell.resize(
            (round(cell.width * scale), round(cell.height * scale)),
            Image.Resampling.LANCZOS,
        )
        canvas = Image.new("RGBA", (FRAME_SIZE, FRAME_SIZE), (0, 0, 0, 0))
        # Imagegen sheet placement is not semantic motion.  Normalize the
        # rendered silhouette center to the root X and the lowest opaque row
        # to the MON_FRAME_V1 baseline without cropping or non-uniform scaling.
        x = round(ROOT[0] - ((box[0] + box[2]) / 2.0) * scale)
        y = round(ROOT[1] + 1 - box[3] * scale)
        canvas.alpha_composite(resized, (x, y))
        bbox = canvas.getchannel("A").getbbox()
        if bbox is None or bbox[0] < SAFETY[0] or bbox[1] < SAFETY[1] or bbox[2] > SAFETY[2] or bbox[3] > SAFETY[3]:
            raise ValueError(f"normalized cell outside MON_FRAME_V1 safety region: {bbox}")
        output.append(canvas)
    return output


def point(x: int, y: int, state: str = "visible") -> dict:
    return {"state": state, "point": {"x": x, "y": y} if state == "visible" else None}


def opaque_bbox(image: Image.Image) -> tuple[int, int, int, int]:
    bbox = image.getchannel("A").point(lambda value: 255 if value >= 32 else 0).getbbox()
    if bbox is None:
        raise ValueError("normalized frame is blank")
    return bbox


def lowest_point(image: Image.Image, left: bool) -> tuple[int, int]:
    alpha = image.getchannel("A")
    x0, x1 = (64, ROOT[0]) if left else (ROOT[0], 961)
    candidates: list[tuple[int, int]] = []
    for y in range(ROOT[1], 500, -1):
        row = [x for x in range(x0, x1) if alpha.getpixel((x, y)) >= 48]
        if row:
            candidates.extend((x, y) for x in row)
            if len(candidates) >= 12:
                break
    if not candidates:
        return (430 if left else 594, ROOT[1])
    y = max(item[1] for item in candidates)
    xs = sorted(item[0] for item in candidates if item[1] >= y - 2)
    return (xs[len(xs) // 2], y)


def align_planted_contact(images: list[Image.Image], *, left: bool) -> list[Image.Image]:
    """Translation-only alignment for one declared planted source contact."""
    target_x = round(median(lowest_point(image, left)[0] for image in images))
    aligned: list[Image.Image] = []
    for image in images:
        current_x, _ = lowest_point(image, left)
        canvas = Image.new("RGBA", image.size, (0, 0, 0, 0))
        canvas.alpha_composite(image, (target_x - current_x, 0))
        bbox = canvas.getchannel("A").getbbox()
        if bbox is None or bbox[0] < SAFETY[0] or bbox[2] > SAFETY[2]:
            raise ValueError(f"contact alignment outside safety region: {bbox}")
        aligned.append(canvas)
    return aligned


def landmarks(image: Image.Image, *, profile: bool = False) -> dict:
    left, top, right, bottom = opaque_bbox(image)
    width = right - left
    height = bottom - top
    center_x = (left + right) // 2
    head_y = top + round(height * 0.28)
    eye_y = top + round(height * 0.38)
    mouth_y = top + round(height * 0.47)
    hand_y = top + round(height * 0.66)
    foot_left = lowest_point(image, True)
    foot_right = lowest_point(image, False)
    return {
        "root": point(*ROOT),
        "ground_contact_left": point(*foot_left),
        "ground_contact_right": point(*foot_right),
        "head_center": point(center_x, head_y),
        "eye_midpoint": point(center_x, eye_y),
        "eye_left": point(center_x - round(width * 0.10), eye_y, "occluded" if profile else "visible"),
        "eye_right": point(center_x + round(width * 0.10), eye_y),
        "mouth_center": point(center_x, mouth_y),
        "hand_left": point(left + round(width * 0.12), hand_y, "occluded" if profile else "visible"),
        "hand_right": point(right - round(width * 0.12), hand_y),
        "foot_left": point(*foot_left),
        "foot_right": point(*foot_right),
        "attachment_back": point(0, 0, "not_applicable"),
        "attachment_front": point(0, 0, "not_applicable"),
        "interaction_focus": point(center_x, eye_y),
        "action_anchor": point(center_x, top + round(height * 0.63)),
        "object_anchor": point(0, 0, "not_applicable"),
    }


def save_frame(path: Path, image: Image.Image) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, "PNG", optimize=False, compress_level=9)
    add_srgb_chunk(path)
    return sha256(path)


def make_track(
    out: Path,
    family: str,
    selection: str,
    entry: str,
    exit_: str,
    posture: str,
    entry_posture: str,
    exit_posture: str,
    completion: str,
    images: list[Image.Image],
    facings: list[str],
    phases: list[str],
    *,
    events: list[tuple[str, str, int]],
    contacts: list[dict],
    profile: bool = False,
    duration_ticks: int = 2,
) -> dict:
    frames: list[dict] = []
    for index, (image, facing, phase) in enumerate(zip(images, facings, phases, strict=True)):
        frame_posture = posture
        if family == "listen_acknowledge" and index >= 4:
            frame_posture = "acknowledging"
        stem = f"{family}__{facing}__{frame_posture}__v01__f{index:03d}"
        frame_path = out / "frames" / f"{stem}.png"
        digest = save_frame(frame_path, image)
        frame = {
            "frame_id": f"{family}_{facing}_{frame_posture}_01_{index:03d}",
            "frame_index": index,
            "filename": frame_path.name,
            "sidecar_filename": f"{stem}.frame.json",
            "duration_ticks": duration_ticks,
            "source_asset_id": f"asset_{family}_{facing}_{frame_posture}_01_{index:03d}",
            "source_sha256": digest,
            "facing": facing,
            "posture": frame_posture,
            "action_phase": phase,
            "landmarks": landmarks(image, profile=profile),
            "provenance": {
                "authored_by": "Codex image generation under Operator Override ADR-57",
                "method": "reference-conditioned image generation; deterministic chroma-alpha and MON_FRAME_V1 normalization",
                "source_revision": "r05-author-001-v1",
            },
            "reuse_of": None,
        }
        stable(out / "sidecars" / frame["sidecar_filename"], frame)
        frames.append(frame)
    timed_events = [
        {
            "event_id": event_id,
            "name": name,
            "tick": sum(frame["duration_ticks"] for frame in frames[:frame_index]),
            "frame_index": frame_index,
        }
        for event_id, name, frame_index in events
    ]
    total = sum(frame["duration_ticks"] for frame in frames)
    track = {
        "track_id": f"candidate:{family}:{selection}:1",
        "family": family,
        "selection_facing": selection,
        "entry_facing": entry,
        "exit_facing": exit_,
        "posture": posture,
        "variant": 1,
        "entry_posture": entry_posture,
        "exit_posture": exit_posture,
        "completion": completion,
        "frames": frames,
        "contacts": contacts,
        "events": timed_events,
        "interruption_ranges": [{"start_tick": 0, "end_tick": total}],
    }
    unsigned = json.dumps(track, sort_keys=True, separators=(",", ":")).encode()
    track["track_checksum"] = hashlib.sha256(unsigned).hexdigest()
    return track


def make_review(out: Path, tracks: list[dict]) -> None:
    review = out / "review"
    review.mkdir(parents=True, exist_ok=True)
    for track in tracks:
        images = [Image.open(out / "frames" / frame["filename"]).convert("RGBA") for frame in track["frames"]]
        thumbs = []
        for image in images:
            thumb = image.copy()
            thumb.thumbnail((256, 256), Image.Resampling.LANCZOS)
            tile = Image.new("RGBA", (280, 280), (238, 238, 242, 255))
            tile.alpha_composite(thumb, ((280 - thumb.width) // 2, (280 - thumb.height) // 2))
            thumbs.append(tile.convert("RGB"))
        strip = Image.new("RGB", (280 * len(thumbs), 280), (238, 238, 242))
        for index, image in enumerate(thumbs):
            strip.paste(image, (index * 280, 0))
        strip.save(review / f"{track['family']}-{track['selection_facing']}-strip.png", "PNG", optimize=False)

        frames = [image.resize((512, 512), Image.Resampling.LANCZOS) for image in images]
        normal = [frame for frame in frames for _ in range(2)]
        quarter = [frame for frame in frames for _ in range(8)]
        normal[0].save(review / f"{track['family']}-{track['selection_facing']}-normal.gif", save_all=True, append_images=normal[1:], duration=42, loop=0, disposal=2)
        quarter[0].save(review / f"{track['family']}-{track['selection_facing']}-quarter.gif", save_all=True, append_images=quarter[1:], duration=42, loop=0, disposal=2)

        silhouettes: list[Image.Image] = []
        for image in images:
            silhouette = Image.new("RGBA", image.size, (238, 238, 242, 255))
            mask = image.getchannel("A")
            ink = Image.new("RGBA", image.size, (22, 18, 34, 255))
            silhouette.alpha_composite(Image.composite(ink, Image.new("RGBA", image.size), mask))
            silhouettes.append(silhouette.resize((512, 512), Image.Resampling.LANCZOS))
        silhouettes[0].save(review / f"{track['family']}-{track['selection_facing']}-silhouette.gif", save_all=True, append_images=silhouettes[1:], duration=84, loop=0, disposal=2)

        overlay_frames: list[Image.Image] = []
        for image, frame in zip(images, track["frames"], strict=True):
            overlay = image.copy()
            draw = ImageDraw.Draw(overlay)
            draw.line((64, ROOT[1], 960, ROOT[1]), fill=(0, 220, 255, 220), width=3)
            draw.ellipse((ROOT[0] - 7, ROOT[1] - 7, ROOT[0] + 7, ROOT[1] + 7), fill=(255, 40, 80, 255))
            for key in ("ground_contact_left", "ground_contact_right"):
                value = frame["landmarks"][key]
                if value["state"] == "visible":
                    x = value["point"]["x"]
                    y = value["point"]["y"]
                    draw.ellipse((x - 6, y - 6, x + 6, y + 6), fill=(255, 220, 0, 255))
            overlay_frames.append(overlay.resize((512, 512), Image.Resampling.LANCZOS))
        overlay_frames[0].save(review / f"{track['family']}-{track['selection_facing']}-root-contact.gif", save_all=True, append_images=overlay_frames[1:], duration=84, loop=0, disposal=2)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sheets", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--clean", action="store_true")
    args = parser.parse_args()
    source = args.sheets.resolve()
    out = args.out.resolve()
    if args.clean and out.exists():
        shutil.rmtree(out)
    if out.exists() and any(out.iterdir()):
        raise SystemExit(f"output must be absent or empty: {out}")
    (out / "frames").mkdir(parents=True, exist_ok=True)
    (out / "sidecars").mkdir(parents=True, exist_ok=True)

    prepared = {
        name: normalized_cells(split_sheet(source / spec.filename, spec))
        for name, spec in SHEETS.items()
    }
    prepared["idle"] = align_planted_contact(prepared["idle"], left=False)
    prepared["listen"] = align_planted_contact(prepared["listen"], left=False)
    planted = lambda total: [
        {"landmark": "ground_contact_left", "state": "planted", "start_tick": 0, "end_tick": total},
        {"landmark": "ground_contact_right", "state": "planted", "start_tick": 0, "end_tick": total},
    ]
    tracks = [
        make_track(out, "neutral_construction", "front", "front", "front", "neutral", "neutral", "neutral", "once", [prepared["construction"][0]], ["front"], ["rest"], events=[], contacts=planted(1), duration_ticks=1),
        make_track(out, "neutral_construction", "right", "right", "right", "neutral", "neutral", "neutral", "once", [prepared["profile"][0]], ["right"], ["rest"], events=[], contacts=planted(1), profile=True, duration_ticks=1),
        make_track(out, "neutral_construction", "front_left", "front_left", "front_left", "neutral", "neutral", "neutral", "once", [prepared["construction"][2]], ["front_left"], ["rest"], events=[], contacts=planted(1), duration_ticks=1),
        make_track(out, "idle_breathe", "front_left", "front_left", "front_left", "neutral", "neutral", "neutral", "loop", prepared["idle"], ["front_left"] * 8, ["settle", "inhale", "expand", "breath_apex", "exhale", "relax", "follow_through", "neutral"], events=[], contacts=[
            {"landmark": "ground_contact_right", "state": "planted", "start_tick": 0, "end_tick": 16},
            {"landmark": "ground_contact_left", "state": "clear", "start_tick": 0, "end_tick": 16},
        ]),
        make_track(out, "walk", "front_left", "front_left", "front_left", "walking", "walking", "walking", "loop", prepared["walk"], ["front_left"] * 8, ["left_contact", "left_down", "left_passing", "left_up", "right_contact", "right_down", "right_passing", "right_up"], events=[("walk_left_footfall", "footfall_left", 0), ("walk_right_footfall", "footfall_right", 4)], contacts=[
            {"landmark": "ground_contact_left", "state": "planted", "start_tick": 0, "end_tick": 2},
            {"landmark": "ground_contact_right", "state": "swing", "start_tick": 0, "end_tick": 8},
            {"landmark": "ground_contact_right", "state": "planted", "start_tick": 8, "end_tick": 10},
            {"landmark": "ground_contact_left", "state": "swing", "start_tick": 2, "end_tick": 16},
        ]),
        make_track(out, "orient_front_to_front_left", "front", "front", "front_left", "neutral", "neutral", "neutral", "once", prepared["orient"], ["front", "front", "front_left", "front_left"], ["anticipate", "turn_begin", "turn_follow", "settle"], events=[("orient_forward_done", "facing_changed", 3)], contacts=[]),
        make_track(out, "orient_front_left_to_front", "front_left", "front_left", "front", "neutral", "neutral", "neutral", "once", list(reversed(prepared["orient"])), ["front_left", "front_left", "front", "front"], ["anticipate", "turn_begin", "turn_follow", "settle"], events=[("orient_reverse_done", "facing_changed", 3)], contacts=[]),
        make_track(out, "listen_acknowledge", "front_left", "front_left", "front_left", "listening", "listening", "acknowledging", "once", prepared["listen"], ["front_left"] * 6, ["neutral_attention", "head_lead", "posture_response", "settle_attention", "acknowledge", "follow_through"], events=[("listen_attention", "attention_acquired", 1), ("listen_ack", "acknowledge", 4), ("listen_settled", "settled", 5)], contacts=[
            {"landmark": "ground_contact_right", "state": "planted", "start_tick": 0, "end_tick": 12},
            {"landmark": "ground_contact_left", "state": "clear", "start_tick": 0, "end_tick": 12},
        ]),
    ]
    assets = [
        {"asset_id": frame["source_asset_id"], "filename": f"frames/{frame['filename']}", "sha256": frame["source_sha256"]}
        for track in tracks
        for frame in track["frames"]
    ]
    pack = {
        "profile": "MON_AUTHORED_FRAME_SOURCE_PACK_V1",
        "schema_version": 1,
        "pack_id": str(uuid.UUID("05a17a00-0000-4000-8000-000000000001")),
        "pack_revision": "r05-author-001-bounded-v1",
        "body_revision": "mon-approved-identity-candidate-r05-v1",
        "developmental_stage": "candidate",
        "approval_state": "candidate",
        "approved_references": {"identity_sha256": IDENTITY_SHA, "turnaround_sha256": TURNAROUND_SHA},
        "provenance": {
            "art_authority": "Codex image generation under operator-authorized ADR-57",
            "generation_or_edit_method": "OpenAI reference-conditioned image generation; deterministic chroma-alpha and MON_FRAME_V1 normalization",
            "source_authority": "COMPANION-P02-EMBODIMENT-001-R05-AUTHOR-001 / Architect Review 10",
            "rights_record": "project-approved original reference assets; operator-authorized candidate derivative generation",
        },
        "timing": {"fps": 24, "tick_unit": "1/24_second"},
        "request_profile": "phase02_bounded_motion_proof_v1",
        "source_assets": assets,
        "tracks": tracks,
    }
    stable(out / "pack.json", pack)
    make_review(out, tracks)
    source_hashes = {spec.filename: sha256(source / spec.filename) for spec in SHEETS.values()}
    stable(out / "generation-inputs.json", {"profile": "R05_IMAGEGEN_INPUTS_V1", "source_sheet_sha256": source_hashes, "reference_sha256": {"identity": IDENTITY_SHA, "turnaround": TURNAROUND_SHA}})
    print(json.dumps({"status": "CANDIDATE_PACK_BUILT", "pack": str(out / "pack.json"), "tracks": len(tracks), "frames": sum(len(track["frames"]) for track in tracks), "approval_state": "candidate", "source_sheet_sha256": source_hashes}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
