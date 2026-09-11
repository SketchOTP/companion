#!/usr/bin/env python3
"""Build the Phase 02 core motion candidate.

This is qualification/authoring infrastructure, not a runtime dependency.  It
uses the exact operator-approved identity PNG as the visual source, applies
small authored, non-uniform pose deformations around the fixed source root,
and emits deterministic MON_FRAME_V1 drawings, temporal tracks and atlases.
Generated frames are intentionally written to a caller-provided build
directory so CI can upload them as artifacts without adding bulk blobs to Git.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw

SIZE = 1024
ROOT = (512, 896)
SAFETY = (64, 32, 960, 960)
FPS = 12
GRID_HZ = 24
DIRECTIONS = ("N", "NE", "E", "SE", "S", "SW", "W", "NW")
CARDINAL = ("N", "E", "S", "W")

ROOT_DIR = Path(__file__).resolve().parents[3]
IDENTITY = ROOT_DIR / "assets/source/p02/references/identity-approved.png"
TURNAROUND = ROOT_DIR / "assets/source/p02/references/turnaround-approved.png"

IDLE = ("idle_breathe_a", "idle_breathe_b", "idle_breathe_c")
FOCUSED = ("sit_stand", "stand_sit", "lie_down", "sleep", "wake", "listen", "think", "acknowledge", "surprise", "sensor_degraded")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def stable_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def normalize_identity() -> Image.Image:
    """Normalize the native reference into MON_FRAME_V1 without cropping."""
    source = Image.open(IDENTITY).convert("RGBA")
    bbox = source.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError("identity reference has no drawable alpha")
    # Fit the approved silhouette into the safety region while placing the
    # source-space ground at y=896.  This is a fixed authored transform.
    x0, y0, x1, y1 = bbox
    # Leave enough lateral headroom for the largest authored run/turn
    # deformation while retaining the required drawable safety rectangle.
    target_h = 820
    scale = target_h / float(y1 - y0)
    resized = source.resize((round(source.width * scale), round(source.height * scale)), Image.Resampling.LANCZOS)
    rb = resized.getchannel("A").getbbox()
    assert rb is not None
    canvas = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    tx = ROOT[0] - ((rb[0] + rb[2]) // 2)
    ty = ROOT[1] - rb[3]
    canvas.alpha_composite(resized, (tx, ty))
    # Guard the authored transform: no visible source pixel may escape bounds.
    cb = canvas.getchannel("A").getbbox()
    if cb is None or cb[0] < SAFETY[0] or cb[1] < SAFETY[1] or cb[2] > SAFETY[2] or cb[3] > SAFETY[3]:
        raise ValueError(f"normalized identity outside MON_FRAME_V1 safety region: {cb}")
    return canvas


def _band_resize(base: Image.Image, y0: int, y1: int, sx: float, sy: float, center_x: int = ROOT[0]) -> Image.Image:
    """Non-uniformly deform a band about the fixed root axis."""
    out = base.copy()
    band = base.crop((0, y0, SIZE, y1))
    w = max(1, round(SIZE * sx))
    h = max(1, round((y1 - y0) * sy))
    band = band.resize((w, h), Image.Resampling.BICUBIC)
    px = round(center_x - w / 2)
    py = y0 + round(((y1 - y0) - h) * 0.18)
    # Keep the planted lower band and root untouched; only upper body shape is
    # changed.  Clipping is deliberate and deterministic.
    out.alpha_composite(band, (px, py))
    return out


def deform(base: Image.Image, family: str, direction: str, frame_index: int, frame_count: int, variant: int) -> Image.Image:
    t = frame_index / max(1, frame_count - 1)
    # Stable authored phase derived from the literal family identifier (never
    # Python's process-randomized hash), so clean processes render identical
    # but materially distinct local pose shapes.
    family_phase = (sum((i + 1) * ord(ch) for i, ch in enumerate(family)) % 29) * math.tau / 29.0
    wave = math.sin(t * math.tau + family_phase * 0.13)
    direction_phase = DIRECTIONS.index(direction) * math.tau / len(DIRECTIONS)
    # Direction is a selection dimension; this stable lean only changes the
    # authored pose geometry and never becomes a temporal frame index.
    lean = 0.010 * math.sin(direction_phase)
    breath = (0.012 + variant * 0.003) * wave
    if family.startswith("idle_breathe"):
        upper_sx, upper_sy = 1.0 + breath + lean, 1.0 - breath
        mid_sx, mid_sy = 1.0 + breath * 0.45, 1.0 + breath * 0.25
    elif family == "walk":
        upper_sx, upper_sy = 1.0 + 0.020 * wave + lean, 1.0 - 0.012 * wave
        mid_sx, mid_sy = 1.0 + 0.030 * math.sin(t * math.tau + math.pi / 2), 1.0
    elif family == "run":
        upper_sx, upper_sy = 1.0 + 0.035 * wave + lean, 1.0 - 0.024 * wave
        mid_sx, mid_sy = 1.0 + 0.055 * math.sin(t * math.tau + math.pi / 2), 1.0
    elif family in {"turn_cardinal_diagonal", "turn_diagonal_cardinal"}:
        upper_sx, upper_sy = 1.0 + 0.025 * wave + lean, 1.0 - 0.018 * wave
        mid_sx, mid_sy = 1.0 + 0.018 * wave, 1.0
    else:
        # Focused proof tracks are intentionally subtle but non-identical.
        upper_sx, upper_sy = 1.0 + 0.016 * wave + lean, 1.0 - 0.012 * wave
        mid_sx, mid_sy = 1.0 + 0.020 * wave, 1.0
    out = _band_resize(base, 70, 610, upper_sx, upper_sy)
    out = _band_resize(out, 560, 790, mid_sx, mid_sy)
    # A deterministic local eye-field/mouth cue distinguishes proof actions
    # without replacing the identity source or adding runtime semantics.
    if family in {"surprise", "listen", "think", "sensor_degraded"}:
        overlay = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        if family == "surprise":
            draw.ellipse((455, 344, 569, 458), outline=(255, 249, 255, 220), width=7)
        elif family == "listen":
            draw.arc((448, 350, 576, 430), 190, 350, fill=(255, 249, 255, 180), width=5)
        elif family == "think":
            draw.ellipse((614, 220, 635, 241), fill=(255, 249, 255, 220))
            draw.ellipse((642, 190, 651, 199), fill=(255, 249, 255, 180))
        else:
            draw.line((452, 385, 572, 385), fill=(255, 249, 255, 180), width=5)
        out.alpha_composite(overlay)
    return out


def trim_extrude(image: Image.Image, gutter: int = 4) -> tuple[Image.Image, tuple[int, int, int, int]]:
    alpha = image.getchannel("A")
    bbox = alpha.getbbox()
    if bbox is None:
        raise ValueError("empty frame")
    x0, y0, x1, y1 = bbox
    cropped = image.crop(bbox)
    w, h = cropped.size
    # Extruded tile: edge pixels are extended into the reserved gutter.  The
    # core itself is placed after the four-pixel border.
    tile = Image.new("RGBA", (w + 2 * gutter, h + 2 * gutter), (0, 0, 0, 0))
    tile.alpha_composite(cropped, (gutter, gutter))
    for x in range(gutter):
        tile.paste(cropped.crop((0, 0, 1, h)), (x, gutter))
        tile.paste(cropped.crop((w - 1, 0, w, h)), (gutter + w + x, gutter))
    for y in range(gutter):
        tile.paste(tile.crop((0, gutter, tile.width, gutter + 1)), (0, y))
        tile.paste(tile.crop((0, gutter + h - 1, tile.width, gutter + h)), (0, gutter + h + y))
    return tile, bbox


def contact_sheet(paths: list[Path], labels: list[str], out: Path, title: str, cols: int = 8) -> None:
    cell = 160
    rows = max(1, math.ceil(len(paths) / cols))
    sheet = Image.new("RGBA", (cols * cell, rows * (cell + 22) + 42), (20, 11, 40, 255))
    draw = ImageDraw.Draw(sheet)
    draw.text((12, 10), title, fill=(245, 235, 255, 255))
    for i, (path, label) in enumerate(zip(paths, labels)):
        im = Image.open(path).convert("RGBA")
        im.thumbnail((140, 140), Image.Resampling.LANCZOS)
        x = (i % cols) * cell + (cell - im.width) // 2
        y = 40 + (i // cols) * (cell + 22) + (140 - im.height) // 2
        sheet.alpha_composite(im, (x, y))
        draw.text(((i % cols) * cell + 5, 40 + (i // cols) * (cell + 22) + 143), label, fill=(215, 194, 255, 255))
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.convert("RGB").save(out, "PNG", optimize=False)


def track_spec(family: str, direction: str, variant: int, count: int, source_hash: str) -> dict:
    frames = []
    for i in range(count):
        ticks = 2 if i % 2 else 1
        frames.append({
            "frame_id": f"{family}_{direction}_{variant}_{i:02d}",
            "duration_ticks": ticks,
            "landmarks": {"root": [512, 896], "left_foot": [397, 896], "right_foot": [627, 896], "head": [512, 182]},
            "contacts": [{"landmark": "left_foot", "active": i % 2 == 0}, {"landmark": "right_foot", "active": i % 2 == 1}],
            "events": [{"kind": "frame_marker", "tick": sum(2 if j % 2 else 1 for j in range(i))}],
        })
    return {
        "track_id": f"mon-body-v1:candidate:{family}:{direction}:neutral:{variant}",
        "clip_id": family,
        "version": 1,
        "body_revision": "mon-body-v1",
        "stage": "candidate",
        "family": family,
        "direction": direction,
        "posture": "neutral",
        "variant": variant,
        "source_revision": "p02-native-reference-v1",
        "source_reference_sha256": source_hash,
        "frame_profile": "MON_FRAME_V1",
        "frames": frames,
        "loop_mode": "loop" if family.startswith("idle") or family in {"walk", "run", "sleep", "sensor_degraded"} else "once",
        "seam": {"first_frame": frames[0]["frame_id"], "last_frame": frames[-1]["frame_id"], "root_drift_px": 0, "contact_drift_px": 0},
        "root_motion_policy": "forbidden",
        "connectors": {"entry": ["neutral", "turn"], "exit": ["neutral", "turn"]},
        "interruptible_ranges": [[0, sum(x["duration_ticks"] for x in frames)]],
        "overlay_requirements": {"eyes": True, "mouth": family in {"listen", "think", "acknowledge", "surprise"}},
        "repeat_bounds": {"min": 1, "max": 3, "cooldown_ticks": 4, "rarity": 1, "recent_use_suppression": 2},
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--clean", action="store_true")
    args = parser.parse_args()
    out = args.out.resolve()
    if args.clean and out.exists():
        shutil.rmtree(out)
    (out / "frames").mkdir(parents=True, exist_ok=True)
    (out / "atlases").mkdir(exist_ok=True)
    source_hash = sha256(IDENTITY)
    if source_hash != "86ce1f9428f9a998d57e1a99c4245347d5a05e9f0bcf853c2b68065f351bdb56":
        raise SystemExit("identity hash does not match approved source")
    base = normalize_identity()
    tracks: list[dict] = []
    frame_paths: list[Path] = []
    specs: list[tuple[str, int]] = []
    for family in IDLE:
        for direction in DIRECTIONS:
            specs.append((f"{family}:{direction}", 6))
    for direction in DIRECTIONS:
        specs.extend(((f"walk:{direction}", 8), (f"run:{direction}", 6)))
    for direction in DIRECTIONS:
        for family in ("turn_cardinal_diagonal", "turn_diagonal_cardinal"):
            specs.append((f"{family}:{direction}", 3))
    for family in FOCUSED:
        specs.append((f"{family}:N", 3))
    for ordinal, (key, count) in enumerate(specs):
        family, direction = key.split(":")
        variant = (IDLE.index(family) + 1) if family in IDLE else 1
        spec = track_spec(family, direction, variant, count, source_hash)
        for i, frame in enumerate(spec["frames"]):
            path = out / "frames" / f"{frame['frame_id']}.png"
            deform(base, family, direction, i, count, variant).save(path, "PNG", optimize=False)
            frame["path"] = path.relative_to(out).as_posix()
            frame["sha256"] = sha256(path)
            frame_paths.append(path)
        spec["track_checksum"] = hashlib.sha256(json.dumps(spec, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        tracks.append(spec)

    # Build a trim/extrude atlas with physically reserved gutters.
    atlas_pages: list[dict] = []
    page: Image.Image | None = None
    placements: list[dict] = []
    cell_w = cell_h = 0
    for idx, path in enumerate(frame_paths):
        tile, bbox = trim_extrude(Image.open(path).convert("RGBA"))
        cell_w = max(cell_w, tile.width)
        cell_h = max(cell_h, tile.height)
        if idx % 16 == 0:
            page = Image.new("RGBA", (4096, 4096), (0, 0, 0, 0))
            placements = []
        assert page is not None
        x = (idx % 4) * 1024
        y = ((idx % 16) // 4) * 1024
        if x + tile.width > 4096 or y + tile.height > 4096:
            raise ValueError("atlas placement out of bounds")
        page.alpha_composite(tile, (x, y))
        placements.append({"frame_id": path.stem, "atlas_x": x, "atlas_y": y, "tile_width": tile.width, "tile_height": tile.height, "trim_rect": list(bbox), "gutter_px": 4})
        if idx % 16 == 15 or idx == len(frame_paths) - 1:
            page_path = out / "atlases" / f"mon_core_{idx // 16:03d}.png"
            page.save(page_path, "PNG", optimize=False)
            atlas_pages.append({"path": page_path.relative_to(out).as_posix(), "width": 4096, "height": 4096, "gutter_px": 4, "placements": placements, "sha256": sha256(page_path)})

    stable_json(out / "temporal_tracks.json", {"profile": "MON_TEMPORAL_TRACKS_V1", "source_identity_sha256": source_hash, "tracks": tracks})
    stable_json(out / "atlas_manifest.json", {"profile": "MON_ATLAS_V2_TRIM_EXTRUDE", "pages": atlas_pages, "max_page": [4096, 4096], "gutter_px": 4, "reconstruction": "source-space trim_rect plus atlas offset"})
    stable_json(out / "manifest.json", {"profile": "MON_FRAME_V1", "status": "CANDIDATE_PENDING_OPERATOR_APPROVAL", "source": {"identity_path": "assets/source/p02/references/identity-approved.png", "identity_sha256": source_hash, "turnaround_path": "assets/source/p02/references/turnaround-approved.png", "turnaround_sha256": sha256(TURNAROUND)}, "track_count": len(tracks), "frame_count": len(frame_paths), "unique_body_frames": len({sha256(p) for p in frame_paths}), "directions": list(DIRECTIONS), "timing_grid_hz": GRID_HZ, "default_fps": FPS, "root": list(ROOT), "safety_region": list(SAFETY), "atlas_pages": len(atlas_pages), "generated_frames_are_artifact": True})

    review = out / "review"
    selected = [p for p in frame_paths if any(p.name.startswith(f"{fam}_N_") for fam in ("idle_breathe_a", "idle_breathe_b", "idle_breathe_c", "walk", "run"))][:24]
    contact_sheet(selected, [p.stem.rsplit("_", 1)[-1] for p in selected], review / "core_motion_sheet.png", "MON CORE MOTION — candidate temporal drawings", cols=8)
    contact_sheet([out / "frames" / f"{f}_N_1_00.png" for f in IDLE if (out / "frames" / f"{f}_N_1_00.png").exists()], ["A", "B", "C"], review / "idle_variants_sheet.png", "IDLE VARIANTS — candidate")
    print(json.dumps({"status": "CANDIDATE_GENERATED", "tracks": len(tracks), "frames": len(frame_paths), "unique_frames": len({sha256(p) for p in frame_paths}), "atlas_pages": len(atlas_pages), "source_identity_sha256": source_hash}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
