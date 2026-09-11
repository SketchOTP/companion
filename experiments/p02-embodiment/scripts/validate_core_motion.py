#!/usr/bin/env python3
"""Fail-closed validation for the reference-grounded temporal core pack."""
from __future__ import annotations
import argparse, hashlib, json, sys, zipfile
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
EXPECTED_ID = "86ce1f9428f9a998d57e1a99c4245347d5a05e9f0bcf853c2b68065f351bdb56"
EXPECTED_TURN = "3696c7d63594de38d408438d5b882f3207635bc63e59fb270f624715faeb09e4"
SAFETY = (64,32,960,960); ROOT_POINT = (512,896)
DIRECTIONS = {"N","NE","E","SE","S","SW","W","NW"}

def sha(p: Path) -> str: return hashlib.sha256(p.read_bytes()).hexdigest()

def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument("--out",type=Path,required=True); a=ap.parse_args(); out=a.out
    errors=[]; identity=ROOT/"assets/source/p02/references/identity-approved.png"; turnaround=ROOT/"assets/source/p02/references/turnaround-approved.png"
    if sha(identity)!=EXPECTED_ID: errors.append("identity hash")
    if sha(turnaround)!=EXPECTED_TURN: errors.append("turnaround hash")
    try: tracks=json.loads((out/"temporal_tracks.json").read_text())
    except Exception as e: errors.append(f"tracks unreadable: {e}"); tracks={}
    try: manifest=json.loads((out/"manifest.json").read_text())
    except Exception as e: errors.append(f"manifest unreadable: {e}"); manifest={}
    if manifest.get("profile")!="MON_FRAME_V1": errors.append("profile")
    if manifest.get("source",{}).get("identity_sha256")!=EXPECTED_ID: errors.append("manifest identity binding")
    rows=tracks.get("tracks",[]); seen_ids=set(); seen_bytes=set(); family_dirs={}; counts={}
    for t in rows:
        tid=t.get("track_id"); fam=t.get("family"); direction=t.get("direction"); frames=t.get("frames",[])
        if not tid or tid in seen_ids: errors.append(f"duplicate/missing track {tid}")
        seen_ids.add(tid)
        if direction not in DIRECTIONS: errors.append(f"direction {tid}")
        family_dirs.setdefault(fam,set()).add(direction); counts[fam]=len(frames)
        if t.get("frame_profile")!="MON_FRAME_V1" or t.get("root_motion_policy")!="forbidden": errors.append(f"track profile {tid}")
        if len(frames)<1: errors.append(f"empty {tid}")
        for f in frames:
            p=out/f.get("path","")
            if not p.exists(): errors.append(f"missing frame {p}"); continue
            try:
                im=Image.open(p); im.load()
                if im.size!=(1024,1024) or im.mode!="RGBA": errors.append(f"canvas {p.name}")
                box=im.getchannel("A").getbbox()
                if box is None or box[0]<SAFETY[0] or box[1]<SAFETY[1] or box[2]>SAFETY[2] or box[3]>SAFETY[3]: errors.append(f"safety {p.name}")
                digest=sha(p); seen_bytes.add(digest)
                if f.get("sha256")!=digest: errors.append(f"frame hash {p.name}")
            except Exception as e: errors.append(f"decode {p.name}: {e}")
            if int(f.get("duration_ticks",0))<1 or not isinstance(f.get("duration_ticks"),int): errors.append(f"duration {tid}")
            if f.get("landmarks",{}).get("root")!=list(ROOT_POINT): errors.append(f"root landmark {tid}")
    for fam in ("idle_breathe_a","idle_breathe_b","idle_breathe_c"):
        if family_dirs.get(fam)!=DIRECTIONS: errors.append(f"idle coverage {fam}")
        if counts.get(fam,0)<6: errors.append(f"idle count {fam}")
    for fam,n in (("walk",8),("run",6)):
        if family_dirs.get(fam)!=DIRECTIONS: errors.append(f"coverage {fam}")
        if counts.get(fam,0)<n: errors.append(f"count {fam}")
    for fam in ("turn_cardinal_diagonal","turn_diagonal_cardinal"):
        if len(family_dirs.get(fam,set()))<8: errors.append(f"connector coverage {fam}")
    for fam in ("sit_stand","stand_sit","lie_down","sleep","wake","listen","think","acknowledge","surprise","sensor_degraded"):
        if not family_dirs.get(fam): errors.append(f"focused proof {fam}")
    if manifest.get("frame_count") != sum(len(t.get("frames",[])) for t in rows): errors.append("frame count equation")
    if manifest.get("unique_body_frames") != len(seen_bytes): errors.append("unique frame equation")
    try: atlas=json.loads((out/"atlas_manifest.json").read_text())
    except Exception as e: errors.append(f"atlas unreadable: {e}"); atlas={}
    placements=[]
    for page in atlas.get("pages",[]):
        if page.get("width",0)>4096 or page.get("height",0)>4096: errors.append("atlas bounds")
        pp=out/page.get("path","")
        if not pp.exists() or sha(pp)!=page.get("sha256"): errors.append(f"atlas hash {pp}")
        for item in page.get("placements",[]):
            x,y,w,h=item.get("atlas_x",-1),item.get("atlas_y",-1),item.get("tile_width",0),item.get("tile_height",0)
            if item.get("gutter_px") != 4 or x<0 or y<0 or x+w>4096 or y+h>4096: errors.append(f"atlas placement {item.get('frame_id')}")
            placements.append((page.get("path"),x,y,w,h,item.get("frame_id")))
    # No physical overlap; reserved cells leave the declared extrusion gutter.
    for i,a1 in enumerate(placements):
        for b1 in placements[i+1:]:
            if a1[0]!=b1[0]: continue
            if a1[1]<b1[1]+b1[3] and b1[1]<a1[1]+a1[3] and a1[2]<b1[2]+b1[4] and b1[2]<a1[2]+a1[4]: errors.append(f"atlas overlap {a1[5]} {b1[5]}")
    result={"status":"PASSED" if not errors else "FAILED","tracks":len(rows),"frames":sum(len(t.get("frames",[])) for t in rows),"unique_body_frames":len(seen_bytes),"errors":errors}
    print(json.dumps(result,sort_keys=True)); return 0 if not errors else 1
if __name__=="__main__": raise SystemExit(main())
