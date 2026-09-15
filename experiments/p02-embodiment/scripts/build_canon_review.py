#!/usr/bin/env python3
"""Create deterministic, operator-accessible R02 construction review aids."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

IDENTITY = Path(__file__).resolve().parents[3] / "assets/source/p02/references/identity-approved.png"
TURNAROUND = Path(__file__).resolve().parents[3] / "assets/source/p02/references/turnaround-approved.png"
IDENTITY_SHA = "86ce1f9428f9a998d57e1a99c4245347d5a05e9f0bcf853c2b68065f351bdb56"
TURNAROUND_SHA = "3696c7d63594de38d408438d5b882f3207635bc63e59fb270f624715faeb09e4"


def check() -> None:
    if hashlib.sha256(IDENTITY.read_bytes()).hexdigest() != IDENTITY_SHA or hashlib.sha256(TURNAROUND.read_bytes()).hexdigest() != TURNAROUND_SHA:
        raise SystemExit("reference hash mismatch")


def canvas(title: str, width: int = 1400, height: int = 900) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGBA", (width, height), (20, 11, 40, 255)); draw = ImageDraw.Draw(image); draw.text((30, 24), title, fill=(245, 235, 255, 255)); return image, draw


def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--out", type=Path, required=True); ap.add_argument("--proof", type=Path, required=True); a = ap.parse_args(); check(); a.out.mkdir(parents=True, exist_ok=True)
    identity = Image.open(IDENTITY).convert("RGBA"); turnaround = Image.open(TURNAROUND).convert("RGB")

    image, draw = canvas("MON_BODY_SOURCE_V1 — front / profile correspondence / front-left candidate")
    t = turnaround.copy(); t.thumbnail((780, 700), Image.Resampling.LANCZOS); image.paste(t, (30, 110))
    n = identity.copy(); n.thumbnail((460, 700), Image.Resampling.LANCZOS); image.alpha_composite(n, (880, 110))
    draw.text((880, 820), "native identity source • exact hash-bound", fill=(215, 194, 255, 255))
    image.convert("RGB").save(a.out / "construction_front_profile_frontleft.png", "PNG", optimize=False)

    image, draw = canvas("MON_FRAME_V1 — rendered root/contact candidate overlay", 1100, 1100)
    n = identity.copy(); n.thumbnail((820, 820), Image.Resampling.LANCZOS); image.alpha_composite(n, (140, 120))
    draw.line((550, 70, 550, 1030), fill=(255, 220, 120, 240), width=3); draw.line((70, 896, 1030, 896), fill=(255, 220, 120, 240), width=3)
    draw.ellipse((430, 878, 455, 903), outline=(120, 255, 190, 255), width=4); draw.ellipse((655, 878, 680, 903), outline=(120, 255, 190, 255), width=4)
    draw.text((70, 980), "root=(512,896) • baseline y=896 • contact drift target ≤2 px • candidate", fill=(245, 235, 255, 255))
    image.convert("RGB").save(a.out / "root_contact_overlay.png", "PNG", optimize=False)

    image, draw = canvas("MON_AUTHORING_COMPARISON_V1 — two candidates, no selection")
    left = identity.copy(); left.thumbnail((500, 620), Image.Resampling.LANCZOS); image.alpha_composite(left, (80, 130)); draw.text((80, 770), "layered raster key-pose candidate", fill=(215, 194, 255, 255))
    right = Image.new("RGBA", (500, 620), (35, 20, 65, 255)); rd = ImageDraw.Draw(right)
    rd.ellipse((120, 180, 380, 500), fill="#8b54d9", outline="#261444", width=10); rd.polygon([(250, 70), (175, 190), (250, 150), (325, 190)], fill="#8b54d9", outline="#261444"); rd.ellipse((190, 270, 235, 330), fill="#090711"); rd.ellipse((265, 270, 310, 330), fill="#090711"); rd.ellipse((205, 280, 220, 310), fill="#fff9ff"); rd.ellipse((280, 280, 295, 310), fill="#fff9ff"); rd.arc((210, 340, 290, 400), 10, 170, fill="#2b1238", width=6); image.alpha_composite(right, (760, 130)); draw.text((760, 770), "layered vector/path candidate • resvg not run", fill=(215, 194, 255, 255))
    draw.text((80, 835), "Compare silhouette, face, palette, edge/shadow, hands, feet, root and contacts; operator chooses.", fill=(245, 235, 255, 255))
    image.convert("RGB").save(a.out / "authoring_comparison.png", "PNG", optimize=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
