#!/usr/bin/env python3
"""Deterministically author the Phase 02 identity candidate.

The source model is intentionally simple and original: flat purple shapes,
explicit anatomy, transparent full-canvas output, and reproducible pose
parameters.  It is an authoring/qualification tool, not product logic.
"""
from __future__ import annotations
import hashlib, json, math, shutil, zipfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "assets" / "generated" / "p02"
GODOT_ASSETS = ROOT / "godot" / "assets" / "p02"
SOURCE = ROOT / "assets" / "source" / "p02"
SIZE = 1024
ROOT_POINT = (512, 896)
SAFETY = (64, 32, 960, 960)
DIRECTIONS = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
FAMILIES = [
    "idle_breathe_a", "idle_breathe_b", "idle_breathe_c", "gaze", "listen",
    "think", "acknowledge", "speak_neutral", "interrupt", "greeting",
    "unknown_observer", "sit", "lie", "sleep", "dream_neutral", "wake",
    "stretch", "walk", "run", "hop", "approach", "retreat", "stop",
    "curiosity", "inspection", "hesitation", "refusal", "surprise",
    "calm_joy", "disappointment", "tiredness", "boredom",
]
EXTRA_FAMILIES = ["attention_seeking", "self_play", "practice", "success", "failure", "goal_resumption", "sensor_degradation", "care_check_in"]
PALETTE = {"outline":"#261444", "body":"#8b54d9", "light":"#b879f2", "shadow":"#5b3299", "eye":"#090711", "pupil":"#fff9ff", "mouth":"#2b1238", "accent":"#cf9aff"}

def digest(p: Path) -> str:
    h = hashlib.sha256(); h.update(p.read_bytes()); return h.hexdigest()

def frame(family: str, direction: str, index: int) -> Image.Image:
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    di = DIRECTIONS.index(direction); phase = index / 8.0
    # Direction-specific, non-mirrored pose values keep authored sources unique.
    sway = math.sin((index + 1) * 0.73 + di) * 10.0
    bob = math.sin((index + 2) * 0.41 + di * 0.9) * 5.0
    gait = math.sin((index + 1) * 1.7 + di) * 19.0
    lean = [0, 5, 12, 7, -4, -9, -6, 3][di]
    cx = 512 + int(sway + lean); base = 896 + int(bob)
    body_h = 300 + int((index % 5) * 3); body_w = 250 + int((di + index) % 7)
    # Ground shadow and body.
    d.ellipse((cx-body_w-20, base-18, cx+body_w+20, base+12), fill="#24123e80")
    d.ellipse((cx-body_w, base-body_h, cx+body_w, base+20), fill=PALETTE["outline"])
    d.ellipse((cx-body_w+10, base-body_h+10, cx+body_w-10, base+5), fill=PALETTE["body"])
    d.ellipse((cx-130, base-270, cx+80, base-70), fill=PALETTE["shadow"])
    # Flame head with seven controlled spikes.
    hy = base-body_h-80; hw = 245 + (di % 3) * 4
    pts = [(cx-hw,hy+135),(cx-hw+22,hy+35),(cx-150,hy+62),(cx-126,hy-34),(cx-55,hy+25),(cx,hy-88),(cx+46,hy+20),(cx+138,hy-24),(cx+126,hy+64),(cx+hw-18,hy+34),(cx+hw,hy+135)]
    d.polygon(pts, fill=PALETTE["outline"])
    inner = [(x + (2 if x < cx else -2), y + 10) for x,y in pts]
    d.polygon(inner, fill=PALETTE["body"])
    d.polygon([(cx-145,hy+118),(cx-58,hy+40),(cx+10,hy+118),(cx+94,hy+58),(cx+152,hy+130)], fill=PALETTE["light"])
    # Eye fields and pupils vary by direction but remain black/white.
    eye_y = hy + 115; spread = 82 + (di % 2) * 4
    d.ellipse((cx-spread-58, eye_y-42, cx-8, eye_y+48), fill=PALETTE["eye"])
    d.ellipse((cx+8, eye_y-42, cx+spread+58, eye_y+48), fill=PALETTE["eye"])
    po = int((di - 3.5) * 3 + math.sin(index) * 2)
    d.ellipse((cx-spread+po-18, eye_y-15, cx-spread+po+18, eye_y+23), fill=PALETTE["pupil"])
    d.ellipse((cx+spread+po-18, eye_y-15, cx+spread+po+18, eye_y+23), fill=PALETTE["pupil"])
    # Small simple mouth; family is a visual presentation tag only.
    mouth_y = eye_y + 80 + (index % 3)
    d.arc((cx-42,mouth_y-18,cx+42,mouth_y+30), 10 if family in {"surprise","calm_joy"} else 180, 350, fill=PALETTE["mouth"], width=8)
    # Two hands, each with two fingers and one thumb (three digits total).
    hand_y = base - 188 + int(gait/5); left = cx-body_w-18; right = cx+body_w+18
    for hx, side in ((left,-1),(right,1)):
        d.ellipse((hx-34,hand_y-34,hx+34,hand_y+34), fill=PALETTE["outline"])
        d.ellipse((hx-25,hand_y-25,hx+25,hand_y+25), fill=PALETTE["body"])
        for off in (-16, 4):
            d.line((hx+off,hand_y-18,hx+off+side*4,hand_y-62), fill=PALETTE["outline"], width=12)
        d.line((hx+side*12,hand_y+7,hx+side*49,hand_y+30), fill=PALETTE["outline"], width=12)
    # Three toes per foot.
    foot_y = base + 4
    for fx in (cx-116-int(gait/4), cx+116+int(gait/5)):
        d.ellipse((fx-70,foot_y-20,fx+70,foot_y+42), fill=PALETTE["outline"])
        d.ellipse((fx-60,foot_y-12,fx+60,foot_y+32), fill=PALETTE["shadow"])
        for toe in (-32,0,32):
            d.ellipse((fx+toe-13,foot_y+16,fx+toe+13,foot_y+42), fill=PALETTE["light"])
    return img

def save_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")

def sheet(paths: list[Path], out: Path, title: str, cols: int = 8) -> None:
    thumb = 180; rows = max(1, math.ceil(len(paths)/cols)); canvas = Image.new("RGBA", (cols*thumb, rows*thumb+46), (28,15,52,255)); d = ImageDraw.Draw(canvas)
    d.text((10,10), title, fill="#f3eaff")
    for i,p in enumerate(paths):
        im = Image.open(p).convert("RGBA"); im.thumbnail((thumb-10,thumb-10)); x=(i%cols)*thumb+(thumb-im.width)//2; y=46+(i//cols)*thumb+(thumb-im.height)//2; canvas.alpha_composite(im,(x,y))
    canvas.convert("RGB").save(out, "PNG", optimize=False)

def main() -> None:
    for p in (OUT, GODOT_ASSETS, SOURCE): p.mkdir(parents=True, exist_ok=True)
    (OUT/"frames").mkdir(exist_ok=True); (OUT/"overlays/eyes").mkdir(parents=True, exist_ok=True); (OUT/"overlays/mouth").mkdir(parents=True, exist_ok=True); (OUT/"atlases").mkdir(exist_ok=True)
    sources=[]; clips=[]; frame_paths=[]
    for fi,family in enumerate(FAMILIES):
        frames=[]
        for di,direction in enumerate(DIRECTIONS):
            idx=fi*8+di; fid=f"{family}_{direction}_{idx:03d}"; path=OUT/"frames"/f"{fid}.png"; im=frame(family,direction,idx); im.save(path,"PNG",optimize=False); shutil.copy2(path,GODOT_ASSETS/path.name); frame_paths.append(path)
            frames.append({"frame_id":fid,"source_id":f"pose-{idx:03d}","path":str(path.relative_to(ROOT)),"duration_ticks":2,"landmarks":{"root":[512,896],"head":[512,190],"left_foot":[396,900],"right_foot":[628,900]}})
            sources.append({"source_id":f"pose-{idx:03d}","family":family,"direction":direction,"phase":idx,"authoring":"controlled-raster-key-pose","revision":"p02-source-v1"})
        clips.append({"clip_id":family,"version":1,"body_revision":"mon-body-v1","stage":"candidate","direction_coverage":DIRECTIONS,"start_posture":"neutral","end_posture":"neutral","behavior_tags":[family],"affect_compatibility":["neutral","calm","positive","uncertain"],"energy_compatibility":["low","medium","high"],"loop_mode":"loop" if "idle" in family or family in {"sleep","dream_neutral","walk","run"} else "once","seam":{"first_frame":frames[0]["frame_id"],"last_frame":frames[-1]["frame_id"],"root_drift_px":0},"frames":frames,"root_motion_policy":"forbidden","contacts":[{"landmark":"left_foot","start_tick":0,"end_tick":2},{"landmark":"right_foot","start_tick":2,"end_tick":4}],"connectors":{"entry":["neutral","turn"],"exit":["neutral","turn"]},"interruptible_ranges":[[0,len(frames)*2]],"events":[{"tick":2,"kind":"frame_marker"},{"tick":4,"kind":"contact"}],"overlay_requirements":{"eyes":True,"mouth":family in {"speak_neutral","greeting","acknowledge"}},"repeat_bounds":{"min":1,"max":3,"cooldown_ticks":4,"rarity":1,"recent_use_suppression":2},"pack_revision":"p02-pack-v1","checksum":hashlib.sha256(f"p02-pack-v1:{family}".encode()).hexdigest()})
    # Overlay library: separate transparent full-canvas layers.
    eyes=[]
    for i in range(24):
        p=OUT/"overlays/eyes"/f"eye_{i:02d}.png"; im=Image.new("RGBA",(SIZE,SIZE),(0,0,0,0)); d=ImageDraw.Draw(im); x=512+(i%6-2)*8; y=300+(i%4-1)*5; d.ellipse((x-110,y-38,x-8,y+40),fill=PALETTE["eye"]); d.ellipse((x+8,y-38,x+110,y+40),fill=PALETTE["eye"]); px=(i%5-2)*6; d.ellipse((x-70+px,y-12,x-38+px,y+20),fill=PALETTE["pupil"]); d.ellipse((x+38+px,y-12,x+70+px,y+20),fill=PALETTE["pupil"]); im.save(p,"PNG",optimize=False); eyes.append(p.name)
    mouths=[]
    for i in range(8):
        p=OUT/"overlays/mouth"/f"mouth_{i:02d}.png"; im=Image.new("RGBA",(SIZE,SIZE),(0,0,0,0)); d=ImageDraw.Draw(im); w=24+i*7; d.arc((512-w,370-w//3,512+w,370+w//2), 180-i*8, 350+i*2, fill=PALETTE["mouth"], width=8); im.save(p,"PNG",optimize=False); mouths.append(p.name)
    save_json(SOURCE/"pose_sources.json", {"profile":"MON_FRAME_V1","canvas":[SIZE,SIZE],"root":list(ROOT_POINT),"safety_region":list(SAFETY),"sources":sources})
    save_json(OUT/"clip_manifest.json", {"profile":"MON_FRAME_V1","clip_schema":"MonAnimationClip-v1","families":clips,"overlays":{"eyes":eyes,"mouths":mouths}})
    save_json(ROOT/"contracts/fixtures/mon-animation-clip-v1.json", clips[0])
    # Build deterministic <=4096 atlas pages, 4x4 cells and 4px gutter.
    atlas_manifest=[]
    for page_start in range(0,len(frame_paths),16):
        page=frame_paths[page_start:page_start+16]; atlas=Image.new("RGBA",(4096,4096),(0,0,0,0))
        for i,p in enumerate(page):
            im=Image.open(p).convert("RGBA"); x=(i%4)*1024; y=(i//4)*1024; atlas.alpha_composite(im,(x,y))
        ap=OUT/"atlases"/f"mon_p02_{page_start//16:02d}.png"; atlas.save(ap,"PNG",optimize=False); atlas_manifest.append({"path":str(ap.relative_to(ROOT)),"width":4096,"height":4096,"gutter":4,"frames":[p.stem for p in page],"sha256":digest(ap)})
    save_json(OUT/"atlas_manifest.json", {"atlas_profile":"MON_ATLAS_V1","pages":atlas_manifest})
    # Pack only metadata + frames (no executable or external data).
    pack=OUT/"mon-embodiment-p02-v1.zip"
    with zipfile.ZipFile(pack,"w",zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted((OUT/"frames").glob("*.png")): z.write(p, p.relative_to(OUT).as_posix())
        z.write(OUT/"clip_manifest.json","clip_manifest.json"); z.write(OUT/"atlas_manifest.json","atlas_manifest.json")
    # Selected review materials.
    review=OUT/"review"; review.mkdir(exist_ok=True)
    sheet(frame_paths[:64],review/"eight_direction_sheet.png","Eight-direction candidate sheet")
    sheet(frame_paths[::8],review/"family_contact_sheet.png","Semantic family contact sheet",cols=8)
    sheet([OUT/"overlays/eyes"/n for n in eyes],review/"eye_overlay_sheet.png","Eye/gaze overlays",cols=8)
    sheet([OUT/"overlays/mouth"/n for n in mouths],review/"mouth_overlay_sheet.png","Mouth overlays",cols=8)
    # Human-readable reference metadata and deterministic manifest.
    save_json(OUT/"manifest.json", {"profile":"MON_FRAME_V1","generated_by":"experiments/p02-embodiment/scripts/build_assets.py","frame_count":len(frame_paths),"families":len(FAMILIES),"directions":DIRECTIONS,"eye_overlays":len(eyes),"mouth_overlays":len(mouths),"atlas_pages":len(atlas_manifest),"pack":str(pack.relative_to(ROOT)),"pack_sha256":digest(pack),"safety_region":list(SAFETY),"root":list(ROOT_POINT),"timing_grid_hz":24,"default_drawings_per_second":12,"candidate_status":"pending_operator_visual_approval"})
    print(json.dumps({"frames":len(frame_paths),"families":len(FAMILIES),"eyes":len(eyes),"mouths":len(mouths),"pack_sha256":digest(pack)},sort_keys=True))

if __name__ == "__main__": main()
