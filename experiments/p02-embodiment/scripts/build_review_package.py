#!/usr/bin/env python3
"""Create deterministic, publication-ready review derivatives from native refs."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[3]
IDENTITY = ROOT / "assets/source/p02/references/identity-approved.png"
TURNAROUND = ROOT / "assets/source/p02/references/turnaround-approved.png"
EXPECTED_ID = "86ce1f9428f9a998d57e1a99c4245347d5a05e9f0bcf853c2b68065f351bdb56"
EXPECTED_TURN = "3696c7d63594de38d408438d5b882f3207635bc63e59fb270f624715faeb09e4"

def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def panel(title: str, size=(1400, 900)):
    im = Image.new("RGBA", size, (20, 11, 40, 255)); d = ImageDraw.Draw(im)
    d.text((28, 24), title, fill=(245,235,255,255)); return im, d

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--out", type=Path, required=True); ap.add_argument("--core", type=Path); a = ap.parse_args(); out = a.out
    if sha(IDENTITY) != EXPECTED_ID or sha(TURNAROUND) != EXPECTED_TURN: raise SystemExit("approved reference hash mismatch")
    out.mkdir(parents=True, exist_ok=True)
    identity = Image.open(IDENTITY).convert("RGBA"); turnaround = Image.open(TURNAROUND).convert("RGB")

    # Six-view correspondence: native turnaround is shown intact beside the
    # normalized MON_FRAME_V1 identity input used by the motion builder.
    im, d = panel("MON_REFERENCE_CORRESPONDENCE_V1 — native six-view + identity source")
    t = turnaround.copy(); t.thumbnail((820, 615), Image.Resampling.LANCZOS); im.paste(t, (35, 110))
    i = identity.copy(); i.thumbnail((430, 650), Image.Resampling.LANCZOS); im.alpha_composite(i, (925, 115))
    d.text((925, 785), "native identity • 1254×1254 RGBA", fill=(215,194,255,255))
    im.convert("RGB").save(out / "six_view_correspondence_sheet.png", "PNG", optimize=False)

    # Construction grid, landmarks and shadow footprint are intentionally
    # diagrammatic review aids; they do not alter the approved source.
    im, d = panel("MON_CONSTRUCTION_GRID_V2 — source-space landmarks")
    for x in range(64, 961, 64): d.line((x,80,x,850), fill=(80,55,110,180), width=1)
    for y in range(32, 961, 64): d.line((40,y,1360,y), fill=(80,55,110,180), width=1)
    n = identity.copy(); n.thumbnail((720,720), Image.Resampling.LANCZOS); im.alpha_composite(n,(340,95))
    d.line((700,80,700,850), fill=(255,220,120,220), width=3); d.line((240,760,1160,760), fill=(255,220,120,220), width=3)
    d.text((50,815), "root=(512,896) • baseline y=896 • safety x=64..960 y=32..960 • crop/encoded translation forbidden", fill=(245,235,255,255))
    im.convert("RGB").save(out / "proportion_silhouette_root_sheet.png", "PNG", optimize=False)

    im, d = panel("MON_ANATOMY_PALETTE_V2 — operator candidate")
    colors=[("outline","#261444"),("body","#8b54d9"),("light","#b879f2"),("shadow","#5b3299"),("eye","#090711"),("pupil","#fff9ff"),("mouth","#2b1238")]
    for idx,(name,val) in enumerate(colors):
        x=45+idx*188; d.rectangle((x,150,x+130,275),fill=val); d.text((x,290),name,fill=(245,235,255,255))
    d.text((48,390),"Head spikes: edge-flame silhouette; eyes: black fields + white pupils; mouth: small/simple",fill=(245,235,255,255))
    d.text((48,430),"Hands: exactly 2 fingers + 1 thumb each; feet: exactly 3 toes each",fill=(245,235,255,255))
    d.text((48,470),"No clothes, muzzle, nose, teeth, ears, horns, symbols, extra limbs, painterly/3D/pixel treatment",fill=(245,235,255,255))
    im.convert("RGB").save(out / "anatomy_palette_sheet.png", "PNG", optimize=False)

    im, d = panel("MON_POSE_LIMITS_V1 — candidate construction rules")
    lines=["squash/stretch ±4% around root", "tilt ≤12°; no root translation", "planted contacts ≤2 px drift", "perspective follows six-view correspondence", "shadow footprint stays beneath planted feet", "diagonals front_left/front_right/back_left/back_right require operator approval"]
    for idx,line in enumerate(lines): d.text((70,150+idx*70), "• "+line, fill=(245,235,255,255))
    im.convert("RGB").save(out / "pose_limits_shadow_sheet.png", "PNG", optimize=False)

    # Diagonal candidates are selected from the generated temporal tracks, not
    # mirrored or metadata-only copies. They remain explicitly unapproved.
    if a.core:
        picks = [a.core / "frames" / f"walk_{direction}_1_00.png" for direction in ("NE", "SE", "SW", "NW")]
        if all(p.exists() for p in picks):
            im, d = panel("MON_DIAGONAL_CANDIDATES_V1 — operator approval required")
            for idx, (direction, p) in enumerate(zip(("front_left", "front_right", "back_left", "back_right"), picks)):
                sprite = Image.open(p).convert("RGBA"); sprite.thumbnail((270, 620), Image.Resampling.LANCZOS)
                im.alpha_composite(sprite, (40 + idx * 340, 120)); d.text((55 + idx * 340, 770), direction, fill=(215,194,255,255))
            im.convert("RGB").save(out / "diagonal_candidates_sheet.png", "PNG", optimize=False)

    print(json.dumps({"status":"REVIEW_DERIVATIVES_GENERATED", "identity_sha256":sha(IDENTITY), "turnaround_sha256":sha(TURNAROUND), "files":sorted(p.name for p in out.iterdir())}, sort_keys=True))
    return 0
if __name__ == "__main__": raise SystemExit(main())
