#!/usr/bin/env python3
"""Fail-closed checks for the bounded R02 motion proof artifact."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image

IDENTITY_SHA = "86ce1f9428f9a998d57e1a99c4245347d5a05e9f0bcf853c2b68065f351bdb56"
TURNAROUND_SHA = "3696c7d63594de38d408438d5b882f3207635bc63e59fb270f624715faeb09e4"
REQUIRED = {
    "idle_breathe": 6,
    "walk": 8,
    "orient_front_to_front_left": 3,
    "orient_front_left_to_front": 3,
    "listen": 3,
    "acknowledge": 3,
}


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--out", type=Path, required=True); a = ap.parse_args()
    root = a.out.resolve(); errors: list[str] = []
    repo = Path(__file__).resolve().parents[3]
    identity = repo / "assets/source/p02/references/identity-approved.png"
    turnaround = repo / "assets/source/p02/references/turnaround-approved.png"
    if sha(identity) != IDENTITY_SHA: errors.append("identity hash")
    if sha(turnaround) != TURNAROUND_SHA: errors.append("turnaround hash")
    try:
        manifest = json.loads((root / "manifest.json").read_text())
        payload = json.loads((root / "temporal_tracks.json").read_text())
    except Exception as exc:
        print(json.dumps({"status": "FAILED", "errors": [f"manifest parse: {exc}"]})); return 1
    tracks = payload.get("tracks", [])
    if manifest.get("tracks") != 6 or manifest.get("drawings") != 26: errors.append("manifest counts")
    if manifest.get("facing") != "front_left": errors.append("facing is not a selection axis")
    seen: set[str] = set(); frame_count = 0
    for item in tracks:
        family = item.get("family")
        if family not in REQUIRED: errors.append(f"unexpected family {family}"); continue
        if item.get("direction") != "front_left": errors.append(f"direction {family}")
        frames = item.get("frames", [])
        track_seen: set[str] = set()
        if len(frames) != REQUIRED[family]: errors.append(f"frame count {family}")
        for frame in frames:
            frame_count += 1
            if frame.get("duration_ticks", 0) not in (1, 2): errors.append(f"duration {frame.get('frame_id')}")
            if frame.get("landmarks", {}).get("root") != [512, 896]: errors.append(f"root {frame.get('frame_id')}")
            path = root / frame.get("path", "")
            if not path.is_file(): errors.append(f"missing frame {path.name}"); continue
            with Image.open(path) as image:
                if image.size != (1024, 1024) or image.mode != "RGBA": errors.append(f"canvas {path.name}")
                bbox = image.getchannel("A").getbbox()
                if bbox is None or bbox[0] < 64 or bbox[1] < 32 or bbox[2] > 960 or bbox[3] > 960: errors.append(f"safety {path.name}")
            digest = sha(path)
            if digest in track_seen: errors.append(f"duplicate drawing within track {path.name}")
            track_seen.add(digest)
            seen.add(digest)
    if frame_count != 26: errors.append("frame total")
    if manifest.get("unique_drawings") != len(seen): errors.append("unique drawing count")
    result = {"status": "PASSED" if not errors else "FAILED", "errors": errors, "tracks": len(tracks), "drawings": frame_count, "unique_drawings": len(seen), "identity_sha256": sha(identity), "turnaround_sha256": sha(turnaround)}
    print(json.dumps(result, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
