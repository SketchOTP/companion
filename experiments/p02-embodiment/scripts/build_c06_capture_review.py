#!/usr/bin/env python3
"""Assemble review media solely from actual Godot checkpoint PNG captures."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from PIL import Image, ImageDraw

LABELS = ("start", "first_cruise", "second_loop_cruise", "stop")

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--out", type=Path, required=True); ap.add_argument("runs", nargs="+", type=Path)
    args = ap.parse_args(); args.out.mkdir(parents=True, exist_ok=True)
    manifests = []
    for run in args.runs:
        movement = json.loads((run / "movement.json").read_text())
        images = []
        for label in LABELS:
            capture = next(c for c in movement["captures"] if c["label"] == label)
            path = run / capture["file"]; image = Image.open(path).convert("RGB"); images.append(image)
        strip = Image.new("RGB", (images[0].width * len(images), images[0].height), "black")
        for index, image in enumerate(images): strip.paste(image, (index * image.width, 0))
        stem = run.name
        strip_path = args.out / f"{stem}_actual-captures.png"; strip.save(strip_path, format="PNG", optimize=False)
        gif_path = args.out / f"{stem}_actual-captures.gif"; images[0].save(gif_path, save_all=True, append_images=images[1:], duration=100, loop=0, optimize=False)
        manifests.append({"run": stem, "strip": strip_path.name, "strip_sha256": hashlib.sha256(strip_path.read_bytes()).hexdigest(), "gif": gif_path.name, "gif_sha256": hashlib.sha256(gif_path.read_bytes()).hexdigest(), "inputs": [c["file"] for c in movement["captures"]]})
    (args.out / "manifest.json").write_text(json.dumps({"source": "actual_godot_checkpoint_pngs", "runs": manifests}, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "PASS", "runs": len(manifests), "media": manifests}, indent=2, sort_keys=True)); return 0

if __name__ == "__main__": raise SystemExit(main())
