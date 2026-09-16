#!/usr/bin/env python3
"""Review-only raster composition, not character authoring or source repair."""
import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw

FACINGS = ("front", "front_right", "right", "back_right", "back", "back_left", "left", "front_left")
BACKDROPS = ((255, 255, 255), (0, 0, 0), (128, 128, 128), (255, 0, 255))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cutouts", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    board = Image.new("RGB", (1600, 920), (225, 225, 230))
    draw = ImageDraw.Draw(board)
    draw.text((16, 8), "AUTHOR-002 CONSTRUCTION STUDIES - SELF-QA ONLY; NOT VISUALLY APPROVED", fill="black")
    observations = {}
    for index, facing in enumerate(FACINGS):
        path = args.cutouts / (facing + ".png")
        raw = path.read_bytes()
        image = Image.open(path)
        if image.mode != "RGBA":
            raise ValueError("expected cutout RGBA: " + facing)
        alpha = image.getchannel("A")
        perimeter = list(alpha.crop((0, 0, image.width, 1)).getdata()) + list(alpha.crop((0, image.height - 1, image.width, image.height)).getdata())
        perimeter += list(alpha.crop((0, 0, 1, image.height)).getdata()) + list(alpha.crop((image.width - 1, 0, image.width, image.height)).getdata())
        green = sum(a > 8 and g > max(r, b) + 12 for r, g, b, a in image.getdata())
        observations[facing] = {"sha256": hashlib.sha256(raw).hexdigest(), "size": list(image.size), "mode": image.mode,
            "alpha_extrema": list(alpha.getextrema()), "nonzero_alpha_bbox": alpha.getbbox(),
            "perimeter_nonzero": sum(v > 0 for v in perimeter), "perimeter_alpha_max": max(perimeter),
            "green_dominance_pixels": green, "visual_anatomy": "REQUIRES_DIRECT_INSPECTION", "intake_status": "NOT_RUN"}
        thumb = image.copy()
        thumb.thumbnail((380, 405), Image.Resampling.LANCZOS)
        x, y = (index % 4) * 400, 35 + (index // 4) * 440
        board.paste(thumb, (x + (400 - thumb.width) // 2, y), thumb)
        draw.text((x + 16, y + 410), facing, fill="black")
        edges = Image.new("RGB", (image.width * 2, image.height * 2))
        for n, color in enumerate(BACKDROPS):
            composite = Image.new("RGBA", image.size, color + (255,))
            composite.alpha_composite(image)
            edges.paste(composite.convert("RGB"), ((n % 2) * image.width, (n // 2) * image.height))
        edges.save(args.out / (facing + "-edges.png"))
        if path.read_bytes() != raw:
            raise AssertionError("source mutated")
    board.save(args.out / "construction-eight-facing.png")
    (args.out / "observations.json").write_text(json.dumps(observations, indent=2, sort_keys=True) + "\n")
    print(json.dumps(observations, sort_keys=True))


if __name__ == "__main__":
    main()
