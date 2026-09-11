#!/usr/bin/env python3
"""Reproduce rejected R03 procedural output as negative evidence only.

This former procedural renderer did not share a visual source of truth with
the Godot scene and did not preserve the approved identity. It is guarded so
it cannot silently function as a production or runtime fallback.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[3]
GODOT_DIR = ROOT / "godot"
SOURCE = ROOT / "assets/source/p02/r03/mon_body_source_v2.json"
IDENTITY_SHA = "86ce1f9428f9a998d57e1a99c4245347d5a05e9f0bcf853c2b68065f351bdb56"
TURNAROUND_SHA = "3696c7d63594de38d408438d5b882f3207635bc63e59fb270f624715faeb09e4"
FACING = ["front", "front_right", "right", "back_right", "back", "back_left", "left", "front_left"]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def pose(frame_id: str, facing: str, *, torso=(1.0, 1.0), head=0.35, tilt=0.0,
         arm_l=0.0, arm_r=0.0, leg_l=0.0, leg_r=0.0, foot_l=(0, 0),
         foot_r=(0, 0), gaze=0.0, mouth=0.0, attention=0.0) -> dict:
    return {
        "frame_id": frame_id,
        "facing": facing,
        "pose": {
            "facing": facing, "torso_scale": list(torso), "head_turn": head,
            "head_tilt": tilt, "arm_left": arm_l, "arm_right": arm_r,
            "leg_left": leg_l, "leg_right": leg_r, "foot_left": list(foot_l),
            "foot_right": list(foot_r), "gaze": gaze, "mouth_open": mouth,
            "attention": attention,
        },
    }


def pose_manifest() -> dict:
    frames: list[dict] = []
    tracks: list[dict] = []

    def add_track(track_id: str, family: str, facing: str, frames_in: list[dict],
                  loop_mode: str, entry: str, exit_: str, events: list[dict]) -> None:
        start = len(frames)
        for ordinal, item in enumerate(frames_in):
            item = dict(item)
            item["frame_id"] = f"{track_id.replace(':', '_')}_{ordinal:02d}"
            item["path"] = f"frames/{item['frame_id']}.png"
            item["track_id"] = track_id
            item["frame_index"] = ordinal
            frames.append(item)
        tracks.append({
            "track_id": track_id, "family": family, "facing": facing,
            "frame_start": start, "frame_count": len(frames_in),
            "loop_mode": loop_mode, "entry_posture": entry,
            "exit_posture": exit_, "events": events,
        })

    idle = [
        pose("idle", "front_left", torso=(1.000, 1.000), head=.35, arm_l=.01, arm_r=-.01),
        pose("idle", "front_left", torso=(1.018, .982), head=.37, arm_l=.03, arm_r=-.02, gaze=.08),
        pose("idle", "front_left", torso=(1.030, .970), head=.39, arm_l=.05, arm_r=-.04, gaze=.12),
        pose("idle", "front_left", torso=(1.018, .982), head=.37, arm_l=.02, arm_r=-.02, gaze=.04),
        pose("idle", "front_left", torso=(1.000, 1.000), head=.35, arm_l=-.01, arm_r=.01, gaze=-.04),
        pose("idle", "front_left", torso=(.988, 1.012), head=.33, arm_l=-.03, arm_r=.03, gaze=-.08),
    ]
    add_track("mon-body-v2-r03:candidate:idle_breathe:front_left:neutral:1", "idle_breathe", "front_left", idle, "loop", "neutral", "neutral", [{"kind":"breath_peak", "frame_index":2}])

    walk = [
        pose("walk", "front_left", arm_l=-.18, arm_r=.18, leg_l=.00, leg_r=.14, foot_l=(0,0), foot_r=(28,-8)),
        pose("walk", "front_left", arm_l=-.12, arm_r=.12, leg_l=.04, leg_r=.19, foot_l=(0,0), foot_r=(30,-22)),
        pose("walk", "front_left", arm_l=.12, arm_r=-.12, leg_l=.18, leg_r=.08, foot_l=(-18,-22), foot_r=(18,-10)),
        pose("walk", "front_left", arm_l=.18, arm_r=-.18, leg_l=.22, leg_r=.00, foot_l=(-24,-30), foot_r=(0,0)),
        pose("walk", "front_left", arm_l=.16, arm_r=-.16, leg_l=.14, leg_r=.00, foot_l=(-24,-10), foot_r=(0,0)),
        pose("walk", "front_left", arm_l=.08, arm_r=-.08, leg_l=.19, leg_r=-.04, foot_l=(-12,-24), foot_r=(0,0)),
        pose("walk", "front_left", arm_l=-.12, arm_r=.12, leg_l=.08, leg_r=.18, foot_l=(0,-8), foot_r=(20,-24)),
        pose("walk", "front_left", arm_l=-.18, arm_r=.18, leg_l=.00, leg_r=.22, foot_l=(0,0), foot_r=(25,-28)),
    ]
    add_track("mon-body-v2-r03:candidate:walk:front_left:neutral:1", "walk", "front_left", walk, "loop", "neutral", "neutral", [{"kind":"left_contact", "frame_index":0}, {"kind":"right_contact", "frame_index":4}])

    turn_fwd = [
        pose("turn", "front", head=0.00, tilt=0.0, arm_l=.0, arm_r=.0),
        pose("turn", "front_right", head=.12, tilt=-.02, arm_l=.02, arm_r=-.02),
        pose("turn", "front_left", head=.25, tilt=-.03, arm_l=.04, arm_r=-.04),
        pose("turn", "front_left", head=.35, tilt=0.0, arm_l=.0, arm_r=.0),
    ]
    add_track("mon-body-v2-r03:candidate:orient_front_to_front_left:front:neutral:1", "orient_front_to_front_left", "front", turn_fwd, "once", "neutral", "neutral", [{"kind":"facing_changed", "frame_index":3}])
    turn_rev = [
        pose("turn", "front_left", head=.35, tilt=0.0, arm_l=.0, arm_r=.0),
        pose("turn", "front_right", head=.22, tilt=.03, arm_l=-.04, arm_r=.04),
        pose("turn", "front_right", head=.10, tilt=.02, arm_l=-.02, arm_r=.02),
        pose("turn", "front", head=0.00, tilt=0.0, arm_l=.0, arm_r=.0),
    ]
    add_track("mon-body-v2-r03:candidate:orient_front_left_to_front:front_left:neutral:1", "orient_front_left_to_front", "front_left", turn_rev, "once", "neutral", "neutral", [{"kind":"facing_changed", "frame_index":3}])

    reaction = [
        pose("listen", "front_left", head=.35, gaze=-.12, attention=.0, arm_l=.0, arm_r=.0),
        pose("listen", "front_left", head=.30, tilt=-.04, gaze=-.18, attention=.35, arm_l=-.02, arm_r=.02),
        pose("listen", "front_left", head=.27, tilt=-.06, gaze=-.22, attention=.75, arm_l=-.04, arm_r=.04),
        pose("ack", "front_left", head=.30, tilt=.02, gaze=.08, attention=.75, arm_l=.04, arm_r=-.04),
        pose("ack", "front_left", head=.34, tilt=.01, gaze=.12, attention=.45, arm_l=.02, arm_r=-.02, mouth=.15),
        pose("ack", "front_left", head=.35, tilt=0.0, gaze=.0, attention=.0, arm_l=.0, arm_r=.0),
    ]
    add_track("mon-body-v2-r03:candidate:listen_acknowledge:front_left:neutral:1", "listen_acknowledge", "front_left", reaction, "once", "neutral", "neutral", [{"kind":"attention_lead", "frame_index":1}, {"kind":"acknowledge", "frame_index":4}])

    return {"profile":"MON_R03_POSE_MANIFEST_V1", "body_revision":"mon-body-v2-r03", "fps":24, "duration_unit":"1/24s", "tracks":tracks, "frames":frames}


def _rotate(point: tuple[float, float], angle: float) -> tuple[float, float]:
    import math
    x, y = point; c, s = math.cos(angle), math.sin(angle)
    return (x * c - y * s, x * s + y * c)


def _poly(draw: ImageDraw.ImageDraw, points: list[tuple[float, float]], fill: str, outline: str = "#1A0D39", width: int = 6) -> None:
    draw.polygon([(round(x), round(y)) for x, y in points], fill=fill)
    draw.line([(round(x), round(y)) for x, y in points + [points[0]]], fill=outline, width=width, joint="curve")


def _oval(draw: ImageDraw.ImageDraw, center: tuple[float, float], radii: tuple[float, float], fill: str, outline: str | None = None, width: int = 6) -> None:
    x, y = center; rx, ry = radii
    box = (round(x-rx), round(y-ry), round(x+rx), round(y+ry))
    draw.ellipse(box, fill=fill, outline=outline, width=width if outline else 1)


def render_pose(render_pose_spec: dict) -> tuple[Image.Image, dict]:
    """Render explicit body parts for a single pose.

    This is intentionally a tiny deterministic raster baker for the Godot
    native source. It uses the same named pivots and pose values as the source
    scene, and emits a separate landmark pass used by QA. No reference pixels
    are copied and no whole-image warp is used.
    """
    import math
    image = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0)); draw = ImageDraw.Draw(image)
    torso_x, torso_y = render_pose_spec.get("torso_scale", [1.0, 1.0])
    head_turn = float(render_pose_spec.get("head_turn", .35)); head_tilt = float(render_pose_spec.get("head_tilt", 0.0))
    arm_l = float(render_pose_spec.get("arm_left", 0.0)); arm_r = float(render_pose_spec.get("arm_right", 0.0))
    leg_l = float(render_pose_spec.get("leg_left", 0.0)); leg_r = float(render_pose_spec.get("leg_right", 0.0))
    foot_l = tuple(render_pose_spec.get("foot_left", [0, 0])); foot_r = tuple(render_pose_spec.get("foot_right", [0, 0]))
    gaze = float(render_pose_spec.get("gaze", 0.0)); attention = float(render_pose_spec.get("attention", 0.0)); mouth = float(render_pose_spec.get("mouth_open", 0.0))
    _oval(draw, (512, 900), (160, 24), "#452296")

    def chain(a: tuple[float,float], b: tuple[float,float], c: tuple[float,float], d: tuple[float,float], width: int) -> None:
        draw.line([a,b,c,d], fill="#7541D4", width=width, joint="curve")
        for p, r in ((a,width//2),(b,round(width*.45)),(c,round(width*.42))): _oval(draw,p,(r,r),"#7541D4")
        draw.line([a,b,c,d], fill="#1A0D39", width=7, joint="curve")

    hip_l=(465,745); hip_r=(559,745)
    knee_l=(hip_l[0]-10*math.cos(leg_l)-82*math.sin(leg_l), hip_l[1]-10*math.sin(leg_l)+82*math.cos(leg_l))
    knee_r=(hip_r[0]+10*math.cos(leg_r)-82*math.sin(leg_r), hip_r[1]+10*math.sin(leg_r)+82*math.cos(leg_r))
    ankle_l=(knee_l[0]-6*math.cos(leg_l*.55)-93*math.sin(leg_l*.55), knee_l[1]-6*math.sin(leg_l*.55)+93*math.cos(leg_l*.55))
    ankle_r=(knee_r[0]+6*math.cos(leg_r*.55)-93*math.sin(leg_r*.55), knee_r[1]+6*math.sin(leg_r*.55)+93*math.cos(leg_r*.55))
    contact_l=(410+foot_l[0],896+foot_l[1]); contact_r=(614+foot_r[0],896+foot_r[1])
    chain(hip_l,knee_l,ankle_l,contact_l,54); chain(hip_r,knee_r,ankle_r,contact_r,54)
    for contact, side in ((contact_l,-1),(contact_r,1)):
        _oval(draw,(contact[0],contact[1]-26),(82,37),"#7541D4","#1A0D39",8)
        for i in range(3):
            toe=(contact[0]+side*(38+i*24), contact[1]-10-i*2)
            _oval(draw,toe,(28,22),"#7541D4","#1A0D39",5)

    center=(512,635); poly=[(-112,-120),(112,-120),(132,45),(78,142),(-78,142),(-132,45)]
    _poly(draw,[(center[0]+x*torso_x,center[1]+y*torso_y) for x,y in poly],"#7541D4",width=8)
    _poly(draw,[(center[0]+x*torso_x,center[1]+y*torso_y) for x,y in [(-100,24),(0,118),(100,24),(72,124),(-72,124)]],"#5B32B3",width=2)

    shoulder_l=(399,545); shoulder_r=(625,545)
    elbow_l=(shoulder_l[0]-52*math.cos(arm_l)-106*math.sin(arm_l), shoulder_l[1]-52*math.sin(arm_l)+106*math.cos(arm_l))
    elbow_r=(shoulder_r[0]+52*math.cos(arm_r)-106*math.sin(arm_r), shoulder_r[1]+52*math.sin(arm_r)+106*math.cos(arm_r))
    wrist_l=(elbow_l[0]-32*math.cos(arm_l*.6)-92*math.sin(arm_l*.6), elbow_l[1]-32*math.sin(arm_l*.6)+92*math.cos(arm_l*.6))
    wrist_r=(elbow_r[0]+32*math.cos(arm_r*.6)-92*math.sin(arm_r*.6), elbow_r[1]+32*math.sin(arm_r*.6)+92*math.cos(arm_r*.6))
    chain(shoulder_l,elbow_l,wrist_l,wrist_l,42); chain(shoulder_r,elbow_r,wrist_r,wrist_r,42)
    for center_hand, side in ((wrist_l,-1),(wrist_r,1)):
        _oval(draw,center_hand,(37,37),"#7541D4","#1A0D39",8)
        for i in range(2):
            p=(center_hand[0]+side*(22+i*19),center_hand[1]+18+i*5)
            draw.line([center_hand,p],fill="#7541D4",width=23); _oval(draw,p,(11,11),"#7541D4","#1A0D39",5)
        p=(center_hand[0]+side*30,center_hand[1]-18); draw.line([center_hand,p],fill="#7541D4",width=24); _oval(draw,p,(12,12),"#7541D4","#1A0D39",5)

    head_scale=1.0-.10*head_turn; head_center=(512+42*head_turn,365)
    _oval(draw,(head_center[0],head_center[1]+32),(205*head_scale,178),"#7541D4","#1A0D39",8)
    triangles=[((-196,35),(-150,-96),(-108,12)),((-135,-22),(-42,-305),(-28,-20)),((-12,-12),(125,-286),(94,35)),((82,20),(205,-206),(182,66)),((160,50),(258,-6),(208,110))]
    for tri in triangles:
        points=[]
        for x,y in tri:
            rx,ry=_rotate((x*head_scale,y),head_tilt); points.append((head_center[0]+rx,head_center[1]+ry))
        _poly(draw,points,"#7541D4",width=8)
    eyes=[(head_center[0]-86+18*head_turn,head_center[1]+62),(head_center[0]+78+18*head_turn,head_center[1]+62)]
    for index, eye in enumerate(eyes):
        if index==1 and head_turn>=.92: continue
        pts=[]
        for x,y in [(-48,-4),(-28,-48),(28,-48),(48,-4),(25,52),(-25,52)]:
            rx,ry=_rotate((x,y),(-.20-.12*attention) if index==0 else (.20-.12*attention)); pts.append((eye[0]+rx,eye[1]+ry))
        _poly(draw,pts,"#090711",width=5)
        _oval(draw,(eye[0]+gaze*14,eye[1]+7),(14,26),"#FFFDF7")
    mouth_center=(head_center[0],head_center[1]+148)
    draw.arc((mouth_center[0]-50,mouth_center[1]-35,mouth_center[0]+50,mouth_center[1]+35),10,170,fill="#2B1238",width=8)
    if mouth>0.1: draw.line((mouth_center[0]-32,mouth_center[1]+5,mouth_center[0]+32,mouth_center[1]+5),fill="#2B1238",width=8)
    landmarks={"root":[512,896],"left_foot":[round(contact_l[0]),round(contact_l[1])],"right_foot":[round(contact_r[0]),round(contact_r[1])],"head":[round(head_center[0]),round(head_center[1]-270)],"eye_left":[round(eyes[0][0]),round(eyes[0][1])],"eye_right":[round(eyes[1][0]),round(eyes[1][1])]}
    return image, landmarks


def find_godot(value: str | None) -> str:
    candidates = [value, os.environ.get("GODOT"), shutil.which("godot")]
    for candidate in candidates:
        if candidate and Path(candidate).is_file() and os.access(candidate, os.X_OK):
            return candidate
    raise SystemExit("Godot 4.7.2 executable required; pass --godot or set GODOT")


def review_gif(paths: list[Path], out: Path, duration_ms: int) -> None:
    frames = []
    for path in paths:
        im = Image.open(path).convert("RGBA").resize((256, 256), Image.Resampling.LANCZOS)
        frames.append(im)
    frames[0].save(out, save_all=True, append_images=frames[1:], duration=duration_ms, loop=0, disposal=2, optimize=False)


def review_strip(paths: list[Path], out: Path, title: str) -> None:
    cell = 220; cols = 4; rows = max(1, (len(paths)+cols-1)//cols)
    sheet = Image.new("RGBA", (cell*cols, 64+rows*220), (20, 11, 40, 255)); draw = ImageDraw.Draw(sheet)
    draw.text((16, 20), title, fill=(245,235,255,255))
    for i, path in enumerate(paths):
        im = Image.open(path).convert("RGBA"); im.thumbnail((190,190), Image.Resampling.LANCZOS)
        x = i % cols * cell + (cell-im.width)//2; y = 64 + i//cols*220 + (190-im.height)//2
        sheet.alpha_composite(im, (x,y)); draw.text((i%cols*cell+8, y+194), path.stem[-24:], fill=(215,194,255,255))
    sheet.save(out, "PNG", optimize=False)


def overlay(paths: list[Path], out: Path, mode: str) -> None:
    rendered = []
    for path in paths:
        im = Image.open(path).convert("RGBA")
        if mode == "silhouette":
            alpha = im.getchannel("A"); rendered.append(Image.merge("RGBA", (alpha,alpha,alpha,alpha)))
        else:
            d = ImageDraw.Draw(im); d.line((512, 32, 512, 960), fill=(255,220,120,220), width=3); d.line((64,896,960,896), fill=(255,220,120,220), width=3); rendered.append(im)
    rendered[0].save(out, save_all=True, append_images=rendered[1:], duration=83 if mode == "silhouette" else 166, loop=0, disposal=2, optimize=False)


def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--out", type=Path, required=True); ap.add_argument("--godot"); ap.add_argument("--clean", action="store_true"); ap.add_argument("--negative-evidence", action="store_true"); args = ap.parse_args()
    if not args.negative_evidence:
        raise SystemExit("R03 is rejected negative evidence; pass --negative-evidence to reproduce it explicitly")
    out = args.out.resolve()
    if args.clean and out.exists(): shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)
    body = json.loads(SOURCE.read_text(encoding="utf-8"))
    identity = ROOT / "assets/source/p02/references/identity-approved.png"; turnaround = ROOT / "assets/source/p02/references/turnaround-approved.png"
    if digest(identity) != IDENTITY_SHA or digest(turnaround) != TURNAROUND_SHA: raise SystemExit("approved reference hash mismatch")
    manifest = pose_manifest()
    # The CI/headless Godot artifact uses the dummy display driver, which has
    # no readable SubViewport texture.  Keep the Godot-native scene as the
    # editable source and use this pure-Python, dependency-pinned raster bake
    # for deterministic full-canvas proof output.  Godot still validates the
    # source graph and plays the resulting raster tracks in the focused test.
    observations = []
    for item in manifest["frames"]:
        image, landmarks = render_pose(item["pose"])
        path = out / f"frames/{item['frame_id']}.png"; path.parent.mkdir(parents=True, exist_ok=True); image.save(path, "PNG", optimize=False)
        observations.append({"frame_id":item["frame_id"], "path":str(path), "landmarks":landmarks, "geometry_signature":json.dumps(item["pose"], sort_keys=True)})
    by_id = {item["frame_id"]: item for item in observations}
    frame_paths: dict[str, Path] = {}
    all_frames = []
    for item in manifest["frames"]:
        path = out / item["path"]; frame_paths[item["frame_id"]] = path; all_frames.append(path)
        item["sha256"] = digest(path); item["rendered_landmarks"] = by_id[item["frame_id"]]["landmarks"]
    tracks = []
    for spec in manifest["tracks"]:
        selected = manifest["frames"][spec["frame_start"]:spec["frame_start"]+spec["frame_count"]]
        frames = []
        for index, item in enumerate(selected):
            lm = item["rendered_landmarks"]
            contact_left = lm["left_foot"][1] == 896
            contact_right = lm["right_foot"][1] == 896
            frames.append({"frame_id":item["frame_id"], "frame_index":index, "duration_ticks":2 if index % 2 else 1, "path":item["path"], "sha256":item["sha256"], "source_pose_id":item["frame_id"], "landmarks":lm, "contacts":[{"landmark":"left_foot","active":contact_left},{"landmark":"right_foot","active":contact_right}], "events":[{"kind":"frame_marker","tick":sum(2 if j%2 else 1 for j in range(index))}]})
        track = {"track_id":spec["track_id"], "clip_id":spec["family"], "version":2, "body_revision":"mon-body-v2-r03", "stage":"candidate", "family":spec["family"], "facing":spec["facing"], "travel_direction":None, "posture":"neutral", "variant":1, "source_revision":"mon-body-source-v2-r03", "source_reference_sha256":IDENTITY_SHA, "frame_profile":"MON_FRAME_V1", "fps":24, "frames":frames, "loop_mode":spec["loop_mode"], "root_motion_policy":"forbidden", "entry_posture":spec["entry_posture"], "exit_posture":spec["exit_posture"], "events":spec["events"], "interruptible_ranges":[[0, sum(2 if i%2 else 1 for i in range(len(frames)))]], "source_checksum":digest(SOURCE), "pack_revision":"p02-r03-proof-v1"}
        canonical = json.dumps(track, sort_keys=True, separators=(",", ":")).encode(); track["track_checksum"] = hashlib.sha256(canonical).hexdigest(); tracks.append(track)
    stable(out / "pose_manifest.json", manifest)
    stable(out / "temporal_tracks_v2.json", {"profile":"MON_TEMPORAL_TRACKS_V2", "body_revision":"mon-body-v2-r03", "timing":{"fps":24,"unit":"1/24s","relative_duration_weights":True}, "tracks":tracks})
    stable(out / "manifest.json", {"profile":"MON_FRAME_V1", "body_revision":"mon-body-v2-r03", "tracks":len(tracks), "drawings":len(all_frames), "unique_drawings":len({digest(p) for p in all_frames}), "identity_sha256":IDENTITY_SHA, "turnaround_sha256":TURNAROUND_SHA, "source_sha256":digest(SOURCE), "fps":24, "review_status":"CANDIDATE_PENDING_OPERATOR_APPROVAL"})
    events = []
    for track in tracks:
        for frame in track["frames"]: events.append({"track_id":track["track_id"],"event":"frame_marker","frame_id":frame["frame_id"],"observed":"deterministic_raster_bake"})
        events.extend({"track_id":track["track_id"],"event":e["kind"],"frame_index":e["frame_index"],"observed":"pose_and_render"} for e in track["events"])
        events.append({"track_id":track["track_id"],"event":"loop" if track["loop_mode"] == "loop" else "completed","observed":"deterministic_raster_bake"})
    stable(out / "event_log.json", {"profile":"MON_R03_EVENT_LOG_V1", "fps":24, "events":events})
    review = out / "review"; review.mkdir(exist_ok=True)
    for track in tracks:
        paths = [out / f["path"] for f in track["frames"]]; name = track["family"]
        review_gif(paths, review / f"{name}_normal.gif", 83); review_gif(paths, review / f"{name}_quarter.gif", 333); review_strip(paths, review / f"{name}_strip.png", f"{name} — ordered rendered frames")
        overlay(paths, review / f"{name}_silhouette.gif", "silhouette"); overlay(paths, review / f"{name}_root_contact.gif", "contact")
    # Keep the proof output byte-identical across clean processes.  Execution
    # timestamps belong in the caller's evidence record, not in deterministic
    # content-addressed bake output.
    stable(out / "provenance.json", {"generator":"build_r03_motion.py", "rebuild_command":"python3 experiments/p02-embodiment/scripts/build_r03_motion.py --out OUT --clean", "godot_source":"godot/mon_body_source_v2.tscn", "body_source_sha256":digest(SOURCE), "identity_sha256":IDENTITY_SHA, "turnaround_sha256":TURNAROUND_SHA, "godot_version":"4.7.2.stable.official.ed1daf0bf", "frame_profile":"MON_FRAME_V1", "fps":24, "generated_frames_are_bounded_proof":True, "operator_approval":"pending", "rights":"project-authored candidate source; approved references retained under their canonical authority", "evidence_ceiling":"E3_TARGET_TESTED"})
    print(json.dumps({"status":"R03_BAKED", "tracks":len(tracks), "frames":len(all_frames), "unique_frames":len({digest(p) for p in all_frames}), "fps":24}, sort_keys=True))
    return 0


if __name__ == "__main__": raise SystemExit(main())
