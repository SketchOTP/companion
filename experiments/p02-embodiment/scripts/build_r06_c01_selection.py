#!/usr/bin/env python3
"""Derive the R06 production selection from the accepted final playback manifest.

Only byte-preserving copies are made. The accepted review archive is the source
of truth; the earlier static-selection record is intentionally not consulted for
runtime promotion.
"""
from __future__ import annotations
import argparse, hashlib, json, shutil, uuid
from pathlib import Path
from PIL import Image

ZIP_ROOT = Path("/home/sketch/.local/share/companion-authoring/exports/full-animation-review-listen-2026-09-12-v2")
IDENTITY = "86ce1f9428f9a998d57e1a99c4245347d5a05e9f0bcf853c2b68065f351bdb56"
TURNAROUND = "3696c7d63594de38d408438d5b882f3207635bc63e59fb270f624715faeb09e4"
ZIP_SHA = "45fd9749179419339046af2ab40605c47d825ca4f0ad47c87a8c6fb9ca1b799b"
MANIFEST_SHA = "d8a0277272f0ccd6f948a24153b7f954aff138111ab840f22e09204aa359e595"
HTML_SHA = "7bd9e0cd5c64b89259dc2780825457a16144cebe02d259fd73a644591aa38cd2"

def sha(p: Path) -> str: return hashlib.sha256(p.read_bytes()).hexdigest()
def point(x, y): return {"x": max(0, min(1253, int(x))), "y": max(0, min(1253, int(y)))}
def landmark(state, p=None): return {"state": state, "point": p}
def observed_landmarks(path: Path, facing: str):
    key=str(path)
    if key in _OBS_CACHE:
        box,cx,gy=_OBS_CACHE[key]
    else:
      with Image.open(path) as im:
        if im.size != (1254, 1254) or im.mode != "RGB": raise ValueError(f"runtime source is not native RGB: {path.name} ({im.mode})")
        pixels=im.load(); fg=[(x,y) for y in range(im.height) for x in range(im.width) if pixels[x,y] != (0,0,0) and max(pixels[x,y]) > 8]
        if not fg: raise ValueError(f"blank runtime source: {path.name}")
        xs=[p[0] for p in fg]; ys=[p[1] for p in fg]; x0,x1,y0,y1=min(xs),max(xs),min(ys),max(ys); cx=(x0+x1)//2; gy=y1
        box,cx,gy=(x0,x1,y0,y1),cx,gy; _OBS_CACHE[key]=(box,cx,gy)
    x0,x1,y0,y1=box
    vis=lambda x,y: landmark("visible",point(x,y)); na=lambda: landmark("not_applicable")
    return {"root":vis(cx,gy),"ground_contact_left":vis(x0+(x1-x0)//3,gy),"ground_contact_right":vis(x1-(x1-x0)//3,gy),"head_center":vis(cx,y0+(y1-y0)//4),"eye_midpoint":vis(cx,y0+(y1-y0)//3),"eye_left":vis(cx-45,y0+(y1-y0)//3),"eye_right":vis(cx+45,y0+(y1-y0)//3),"mouth_center":vis(cx,y0+(y1-y0)*2//5),"hand_left":vis(x0+(x1-x0)//5,y0+(y1-y0)*3//5),"hand_right":vis(x1-(x1-x0)//5,y0+(y1-y0)*3//5),"foot_left":vis(x0+(x1-x0)//3,gy),"foot_right":vis(x1-(x1-x0)//3,gy),"attachment_back":na() if facing.startswith("front") else vis(cx,y0+20),"attachment_front":na() if facing=="back" else vis(cx,y0+20),"interaction_focus":vis(cx,y0+(y1-y0)//3),"action_anchor":vis(cx,y0+(y1-y0)//2),"object_anchor":na()}
_OBS_CACHE={}
def facing_for(asset: str) -> str:
    n=asset.removeprefix("base_").removeprefix("listen_")
    for f in ("front_right","back_right","front_left","back_left","right","left","back","front"):
        if n.startswith(f) or f"_{f}_" in n: return f
    return "front"
def posture_for(stage: str, asset: str) -> str:
    s=(stage+" "+asset).lower()
    if "listen" in s or "acknowledge" in s or asset.startswith("listen_"): return "listening"
    if "walk" in s or any(k in asset for k in ("contact","passing","up_","down_","start_","stop_","walk_mid")): return "walking"
    return "neutral"
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--out",required=True); a=ap.parse_args(); out=Path(a.out); frames=out/"frames"; sides=out/"sidecars"; frames.mkdir(parents=True,exist_ok=True); sides.mkdir(exist_ok=True)
    manifest=json.loads((ZIP_ROOT/"manifest.json").read_text()); assert sha(ZIP_ROOT/"manifest.json")==MANIFEST_SHA and sha(ZIP_ROOT/"index.html")==HTML_SHA
    # The final review manifest is authoritative. Only non-diagnostic playback
    # groups may become runtime masters; historical studies, retries, and sheet
    # derivatives remain audit evidence even when their pixels are valid.
    accepted_indices=[i for i, track in enumerate(manifest["tracks"]) if track.get("group") != "Diagnostics"]
    unique={}; tracks=[]
    for ti in accepted_indices:
        source_track=manifest["tracks"][ti]; track_frames=[]; tick=0
        for fi,entry in enumerate(source_track["frames"]):
            key=entry["asset"]; meta=manifest["assets"][key]; src=ZIP_ROOT/meta["path"]; source_sha=meta["sha256"]
            if key not in unique:
                aid="r06_"+key.replace("base_","").replace("listen_","listen_").replace("-","_")
                fn=f"frames/{aid}.png"; dst=out/fn; shutil.copyfile(src,dst)
                if sha(dst)!=source_sha: raise SystemExit(f"byte-preservation failure for {key}")
                with Image.open(dst) as im:
                    if im.size!=(1254,1254) or im.mode!="RGB": raise SystemExit(f"unsupported accepted source {key}: {im.mode}")
                    corners=[im.getpixel(c) for c in ((0,0),(1253,0),(0,1253),(1253,1253))]
                unique[key]={"asset_id":aid,"filename":fn,"sha256":source_sha,"source_path":meta["path"],"dimensions":[1254,1254],"mode":"RGB","perimeter":corners,"source_role":"runtime_visual_master","presentation_profile":"R05_BLACK_FIELD_RGB8_V1","accepted_sequence_memberships":[]}
            unique[key]["accepted_sequence_memberships"].append(f"playback_track_{ti:02d}")
            facing=facing_for(key); posture=posture_for(entry.get("stage", ""),key); aid=unique[key]["asset_id"]; frame_id=f"r06_t{ti:02d}_f{fi:03d}"
            duration=int(entry.get("ticks",4)); side_name=f"sidecars/{frame_id}.frame.json"; srcpath=out/unique[key]["filename"]
            landmarks=observed_landmarks(srcpath,facing)
            fr={"frame_id":frame_id,"frame_index":fi,"filename":unique[key]["filename"],"sidecar_filename":side_name,"duration_ticks":duration,"source_asset_id":aid,"source_sha256":source_sha,"facing":facing,"posture":posture,"action_phase":entry.get("label"),"landmarks":landmarks,"provenance":{"authored_by":"operator-approved R05 final playback package","method":"immutable source selection; no pixel mutation","source_revision":"5f538a0c86783b7c5d00b140dcc91c7f76c30450"},"reuse_of":None}
            (out/side_name).write_text(json.dumps({"profile":"R05_RUNTIME_FRAME_SIDECAR_V1","frame_id":frame_id,"source_asset_id":aid,"source_sha256":source_sha,"source_path":unique[key]["source_path"],"presentation_profile":"R05_BLACK_FIELD_RGB8_V1","observations":{"dimensions":[1254,1254],"mode":"RGB","background":"near_black_field","perimeter":unique[key]["perimeter"]},"landmarks":landmarks},sort_keys=True,indent=2)+"\n")
            track_frames.append(fr); tick+=duration
        if ti==5: family="listen_acknowledge"
        elif ti in (6,10,11,15): family="turn"
        elif ti in (7,8,9,12,13,14): family="walk"
        elif ti in (4,16,17,18,19,20,21,22,23): family="neutral_construction"
        else: family="assembled_action"
        sf=track_frames[0]["facing"] if track_frames else "front"; ef=track_frames[-1]["facing"] if track_frames else sf
        events=[]
        labels=[f["action_phase"] or "" for f in track_frames]
        if "listen_acknowledge"==family: events=[{"event_id":"attention_acquired","name":"attention_acquired","tick":sum(f["duration_ticks"] for f in track_frames[:3]),"frame_index":2},{"event_id":"acknowledge","name":"acknowledge","tick":sum(f["duration_ticks"] for f in track_frames[:7]),"frame_index":6},{"event_id":"settled","name":"settled","tick":max(0,tick-track_frames[-1]["duration_ticks"]),"frame_index":len(track_frames)-1}]
        if family=="turn": events.append({"event_id":f"r06_t{ti:02d}_facing_changed","name":"facing_changed","tick":max(0,tick-1),"frame_index":len(track_frames)-1})
        contacts=[]
        if family=="walk": contacts=[{"landmark":"ground_contact_left","state":"planted","start_tick":0,"end_tick":max(1,tick//2)},{"landmark":"ground_contact_right","state":"planted","start_tick":max(1,tick//2),"end_tick":tick}]; events=[{"event_id":f"r06_playback_track_{ti:02d}_footfall_left","name":"footfall_left","tick":0,"frame_index":0},{"event_id":f"r06_playback_track_{ti:02d}_footfall_right","name":"footfall_right","tick":max(1,tick//2),"frame_index":min(len(track_frames)-1,max(0,len(track_frames)//2))}]
        tracks.append({"track_id":f"r06_playback_track_{ti:02d}","family":family,"selection_facing":sf,"entry_facing":sf,"exit_facing":ef,"posture":track_frames[0]["posture"],"variant":1,"entry_posture":track_frames[0]["posture"],"exit_posture":track_frames[-1]["posture"],"completion":source_track.get("completion","once"),"frames":track_frames,"contacts":contacts,"events":events,"interruption_ranges":[{"start_tick":0,"end_tick":max(1,tick)}],"track_checksum":"0"*64})
    for t in tracks: t["track_checksum"]=hashlib.sha256(json.dumps({k:v for k,v in t.items() if k!="track_checksum"},sort_keys=True,separators=(",",":")).encode()).hexdigest()
    selection_assets=[{k:v for k,v in x.items()} for x in unique.values()]
    assets=[{"asset_id":x["asset_id"],"filename":x["filename"],"sha256":x["sha256"]} for x in unique.values()]
    pack={"profile":"MON_OPAQUE_BLACK_FRAME_SOURCE_PACK_V1","schema_version":1,"pack_id":str(uuid.uuid5(uuid.NAMESPACE_URL,"companion:r06:c01:"+MANIFEST_SHA)),"pack_revision":"r06-c01-final-playback-v1","body_revision":"r05-approved-v1","developmental_stage":"candidate","approval_state":"candidate","approved_references":{"identity_sha256":IDENTITY,"turnaround_sha256":TURNAROUND},"provenance":{"art_authority":"operator-approved final R05 playback package","generation_or_edit_method":"immutable selection from accepted review ZIP","source_authority":"5f538a0c86783b7c5d00b140dcc91c7f76c30450","rights_record":"project-owned candidate visual assets; operator approval recorded in Review 12/13"},"timing":{"fps":24,"tick_unit":"1/24_second"},"runtime_profile":{"profiles":["R05_BLACK_FIELD_RGB8_V1","R05_TRANSPARENT_RGBA8_V1"],"display_background":"black","native_canvas":[1254,1254],"source_sampling":"native_bytes_no_resample","display_transform":{"scale":0.5,"offset_px":[0,0]}},"request_profile":"r06_operator_approved_black_visual_master_v1","source_assets":assets,"tracks":tracks}
    (out/"pack.json").write_text(json.dumps(pack,sort_keys=True,indent=2)+"\n")
    selection={"profile":"R05_PRODUCTION_VISUAL_SELECTION_V1","selection_basis":{"review_task_head":"5f538a0c86783b7c5d00b140dcc91c7f76c30450","zip_sha256":ZIP_SHA,"manifest_sha256":MANIFEST_SHA,"review_html_sha256":HTML_SHA},"lineage_record":".agent/tasks/active/COMPANION-P02-EMBODIMENT-001/R05_AUTHOR_002_OPERATOR_SELECTION.json (reference only)","approval_state":"candidate","runtime_visual_masters":selection_assets,"runtime_track_ids":[t["track_id"] for t in tracks],"visual_reference_master_excluded":True,"diagnostic_only_excluded":True}
    (out/"R05_PRODUCTION_VISUAL_SELECTION_V1.json").write_text(json.dumps(selection,sort_keys=True,indent=2)+"\n")
    print(json.dumps({"tracks":len(tracks),"frame_slots":sum(len(t["frames"]) for t in tracks),"unique_runtime_assets":len(assets),"selection":str(out/"R05_PRODUCTION_VISUAL_SELECTION_V1.json")},indent=2))
if __name__=="__main__": main()
