#!/usr/bin/env python3
"""Fail-closed MON_FRAME_V1 and pack validation."""
from __future__ import annotations
import hashlib, json, sys, zipfile
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[3]; OUT=ROOT/"assets/generated/p02"; SIZE=1024; SAFETY=(64,32,960,960)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    manifest=json.loads((OUT/"manifest.json").read_text()); clips=json.loads((OUT/"clip_manifest.json").read_text()); errors=[]; frames=list((OUT/"frames").glob("*.png"));
    if manifest["frame_count"] != 256 or len(frames)!=256: errors.append("frame count")
    if manifest["families"] != 32 or len(clips["families"])!=32: errors.append("family count")
    hashes=set()
    for p in frames:
        try:
            im=Image.open(p); im.load()
            if im.size!=(SIZE,SIZE) or im.mode!="RGBA": errors.append(f"canvas {p.name}")
            if im.getbbox() is None: errors.append(f"empty {p.name}")
            # Bounding box of nontransparent pixels must remain in drawable safety region.
            box=im.getchannel("A").getbbox()
            if box and (box[0]<SAFETY[0] or box[1]<SAFETY[1] or box[2]>SAFETY[2] or box[3]>SAFETY[3]): errors.append(f"safety {p.name}")
            hashes.add(sha(p))
        except Exception as e: errors.append(f"decode {p.name}: {e}")
    if len(hashes)!=len(frames): errors.append("duplicate frames")
    for c in clips["families"]:
        if c["direction_coverage"] != ["N","NE","E","SE","S","SW","W","NW"]: errors.append(f"directions {c['clip_id']}")
        if c["seam"]["root_drift_px"] != 0: errors.append(f"root drift {c['clip_id']}")
        if any(f["duration_ticks"]<1 for f in c["frames"]): errors.append(f"timing {c['clip_id']}")
    if len(clips["overlays"]["eyes"])<24 or len(clips["overlays"]["mouths"])<8: errors.append("overlay floor")
    pack=OUT/"mon-embodiment-p02-v1.zip"
    if not pack.exists() or not zipfile.is_zipfile(pack): errors.append("pack")
    if errors:
        print("ASSET_VALIDATION_FAILED"); print("\n".join(errors)); return 1
    print(json.dumps({"status":"PASSED","frames":len(frames),"unique_frames":len(hashes),"families":len(clips["families"]),"eyes":len(clips["overlays"]["eyes"]),"mouths":len(clips["overlays"]["mouths"]),"pack_sha256":sha(pack)},sort_keys=True)); return 0
if __name__=="__main__": sys.exit(main())
