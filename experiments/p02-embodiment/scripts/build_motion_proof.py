#!/usr/bin/env python3
"""Build the small Phase 02 canon/motion proof pack.

This is disposable authoring/qualification infrastructure.  It deliberately
does not build the rejected full library.  Each facing is a selection axis and
each proof track contains a real ordered temporal sequence.  Outputs go to a
caller-provided private directory so generated frames stay out of Git.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
from pathlib import Path

from PIL import Image, ImageDraw

SIZE = 1024
ROOT = (512, 896)
SAFETY = (64, 32, 960, 960)
GRID_HZ = 24
FPS = 12
IDENTITY_SHA = "86ce1f9428f9a998d57e1a99c4245347d5a05e9f0bcf853c2b68065f351bdb56"
TURNAROUND_SHA = "3696c7d63594de38d408438d5b882f3207635bc63e59fb270f624715faeb09e4"
ROOT_DIR = Path(__file__).resolve().parents[3]
IDENTITY = ROOT_DIR / "assets/source/p02/references/identity-approved.png"
TURNAROUND = ROOT_DIR / "assets/source/p02/references/turnaround-approved.png"
FACING = "front_left"


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def normalize() -> Image.Image:
    source = Image.open(IDENTITY).convert("RGBA")
    bbox = source.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError("approved identity is transparent")
    x0, y0, x1, y1 = bbox
    scale = 820.0 / (y1 - y0)
    resized = source.resize((round(source.width * scale), round(source.height * scale)), Image.Resampling.LANCZOS)
    rb = resized.getchannel("A").getbbox()
    assert rb is not None
    canvas = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    canvas.alpha_composite(resized, (ROOT[0] - (rb[0] + rb[2]) // 2, ROOT[1] - rb[3]))
    cb = canvas.getchannel("A").getbbox()
    if cb is None or cb[0] < SAFETY[0] or cb[1] < SAFETY[1] or cb[2] > SAFETY[2] or cb[3] > SAFETY[3]:
        raise ValueError(f"identity outside MON_FRAME_V1 safety region: {cb}")
    return canvas


def deform(base: Image.Image, family: str, index: int, count: int) -> Image.Image:
    """Apply a stable local authored pose around the fixed root.

    Lower planted feet remain from the source.  The explicit family/index
    phase is part of the source specification, never a runtime random value.
    """
    # Sample the cyclic wave at cell centres so the final drawing is not an
    # accidental byte-duplicate of the first drawing; the runtime loop seam
    # is represented by an explicit connector/event, not a repeated hold.
    t = (index + 0.5) / max(1, count)
    phase = sum((i + 1) * ord(ch) for i, ch in enumerate(family)) % 31
    wave = math.sin(t * math.tau + phase * math.tau / 31.0) + 0.22 * (index + 1) / max(1, count)
    out = base.copy()
    if family == "idle_breathe":
        sx, sy = 1.0 + 0.032 * wave, 1.0 - 0.026 * wave
    elif family == "walk":
        sx, sy = 1.0 + 0.030 * wave, 1.0 - 0.022 * wave
    elif family.startswith("orient"):
        sx, sy = 1.0 + 0.024 * wave, 1.0 - 0.016 * wave
    elif family in {"listen", "acknowledge"}:
        sx, sy = 1.0 + 0.014 * wave, 1.0 - 0.010 * wave
    else:
        sx, sy = 1.0, 1.0
    band = base.crop((0, 70, SIZE, 790)).resize((round(SIZE * sx), round(720 * sy)), Image.Resampling.BICUBIC)
    x = round(ROOT[0] - band.width / 2)
    y = 70 + round((720 - band.height) * 0.18)
    out.alpha_composite(band, (x, y))
    if family == "listen":
        draw = ImageDraw.Draw(out)
        draw.arc((428, 320, 596, 448), 205, 335, fill=(255, 249, 255, 180), width=5)
    elif family == "acknowledge":
        draw = ImageDraw.Draw(out)
        draw.arc((430, 330, 594, 450), 15, 165, fill=(43, 18, 56, 230), width=6)
    return out


def track(family: str, label: str, count: int, loop: bool, source_hash: str) -> dict:
    frames = []
    elapsed = 0
    for i in range(count):
        ticks = 2 if i % 3 == 1 else 1
        frames.append({
            "frame_id": f"proof_{label}_{i:02d}",
            "duration_ticks": ticks,
            "path": f"frames/proof_{label}_{i:02d}.png",
            "landmarks": {"root": [512, 896], "left_foot": [397, 896], "right_foot": [627, 896]},
            "contacts": [{"landmark": "left_foot", "active": family == "walk" and i in {0, 1, 4, 5}}, {"landmark": "right_foot", "active": family == "walk" and i in {2, 3, 6, 7}}],
            "events": [{"kind": "frame_marker", "tick": elapsed}],
        })
        elapsed += ticks
    return {
        "track_id": f"mon-body-v1:proof:{family}:{FACING}:neutral:1",
        "family": family,
        "direction": FACING,
        "posture": "neutral",
        "variant": 1,
        "body_revision": "mon-body-v1",
        "stage": "proof",
        "version": 1,
        "frame_profile": "MON_FRAME_V1",
        "root_motion_policy": "forbidden",
        "source_revision": "p02-native-reference-v1",
        "source_reference_sha256": source_hash,
        "frames": frames,
        "loop_mode": "loop" if loop else "once",
        "seam": {"first_frame": frames[0]["frame_id"], "last_frame": frames[-1]["frame_id"], "root_drift_px": 0},
        "contacts": {"planted_contact_drift_px": 0, "declared_contact_spans": [f["frame_id"] for f in frames if any(c["active"] for c in f["contacts"]) ]},
        "connectors": {"entry": ["neutral"], "exit": ["neutral"]},
        "interruptible_ranges": [[0, elapsed]],
    }


def strip(paths: list[Path], out: Path, title: str) -> None:
    cell, cols = 180, 4
    rows = max(1, math.ceil(len(paths) / cols))
    sheet = Image.new("RGBA", (cell * cols, 54 + rows * 200), (20, 11, 40, 255))
    d = ImageDraw.Draw(sheet)
    d.text((12, 14), title, fill=(245, 235, 255, 255))
    for i, path in enumerate(paths):
        im = Image.open(path).convert("RGBA")
        im.thumbnail((160, 160), Image.Resampling.LANCZOS)
        x = (i % cols) * cell + (cell - im.width) // 2
        y = 54 + (i // cols) * 200 + (160 - im.height) // 2
        sheet.alpha_composite(im, (x, y))
        d.text(((i % cols) * cell + 8, y + 166), path.stem, fill=(215, 194, 255, 255))
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.convert("RGB").save(out, "PNG", optimize=False)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--clean", action="store_true")
    args = ap.parse_args()
    out = args.out.resolve()
    if args.clean and out.exists():
        shutil.rmtree(out)
    if sha(IDENTITY) != IDENTITY_SHA or sha(TURNAROUND) != TURNAROUND_SHA:
        raise SystemExit("approved reference hash mismatch")
    base = normalize()
    out.joinpath("frames").mkdir(parents=True, exist_ok=True)
    source_hash = sha(IDENTITY)
    specs = [("idle_breathe", "idle_breathe", 6, True), ("walk", "walk", 8, True), ("orient_front_to_front_left", "turn_fwd", 3, False), ("orient_front_left_to_front", "turn_rev", 3, False), ("listen", "listen", 3, False), ("acknowledge", "acknowledge", 3, False)]
    tracks = []
    frame_paths = []
    for family, label, count, loop in specs:
        item = track(family, label, count, loop, source_hash)
        for i, frame in enumerate(item["frames"]):
            p = out / frame["path"]
            deform(base, family, i, count).save(p, "PNG", optimize=False)
            frame["sha256"] = sha(p)
            frame_paths.append(p)
        tracks.append(item)
    write_json(out / "temporal_tracks.json", {"profile": "MON_TEMPORAL_PROOF_V1", "source_identity_sha256": source_hash, "source_turnaround_sha256": sha(TURNAROUND), "tracks": tracks})
    write_json(out / "manifest.json", {"profile": "MON_FRAME_V1", "status": "CANDIDATE_PENDING_OPERATOR_APPROVAL", "tracks": len(tracks), "drawings": len(frame_paths), "unique_drawings": len({sha(p) for p in frame_paths}), "facing": FACING, "timing_grid_hz": GRID_HZ, "default_fps": FPS, "root": list(ROOT), "safety_region": list(SAFETY), "source_identity_sha256": source_hash, "source_turnaround_sha256": sha(TURNAROUND)})
    review = out / "review"
    strip(frame_paths[:6], review / "idle_breathe_front_left.png", "IDLE / BREATHE — FRONT LEFT — candidate")
    strip(frame_paths[6:14], review / "walk_front_left.png", "WALK — FRONT LEFT — candidate")
    strip(frame_paths[14:], review / "connectors_reactions.png", "CONNECTORS + LISTEN / ACKNOWLEDGE — candidate")
    events = []
    for item in tracks:
        events.extend({"track_id": item["track_id"], "event": "frame_marker", "frame_id": frame["frame_id"], "observed_by": "proof-builder-render"} for frame in item["frames"])
        events.append({"track_id": item["track_id"], "event": "loop_or_completion", "observed_by": "proof-builder-render", "expected_runtime_observation": True})
    write_json(out / "review" / "event_expectations.json", {"status": "RUNTIME_OBSERVATION_REQUIRED", "events": events})
    print(json.dumps({"status": "PROOF_CANDIDATE_GENERATED", "tracks": len(tracks), "drawings": len(frame_paths), "unique_drawings": len({sha(p) for p in frame_paths}), "facing": FACING}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
