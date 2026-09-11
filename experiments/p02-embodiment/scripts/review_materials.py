#!/usr/bin/env python3
"""Create deterministic operator-review sheets from the generated candidate."""
from pathlib import Path
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[3]; OUT=ROOT/"assets/generated/p02"; R=OUT/"review"
def canvas(title):
    im=Image.new("RGB",(1200,760),(29,16,54)); d=ImageDraw.Draw(im); d.text((30,25),title,fill="#f5ebff"); return im,d
def main():
    # Four diagonal candidates are represented by authored direction frames and
    # explicitly marked as candidates; no mirror is used.
    im,d=canvas("MON_CONSTRUCTION_V1 — diagonal candidates (operator review)")
    names=["greeting_NE_075.png","greeting_SE_077.png","retreat_SW_173.png","retreat_NW_175.png"]
    for i,n in enumerate(names):
        p=OUT/"frames"/n
        if p.exists():
            x=40+i*290; sprite=Image.open(p).convert("RGBA"); sprite.thumbnail((250,620)); im.paste(sprite,(x,80),sprite); d.text((x,710),n.split("_")[1],fill="#d7c2ff")
    im.save(R/"construction_diagonal_candidates.png","PNG",optimize=False)
    # Palette/anatomy reference board (swatches + text, no hidden state).
    im,d=canvas("MON_PALETTE_ANATOMY_V1 — candidate")
    sw=[("outline","#261444"),("body","#8b54d9"),("light","#b879f2"),("shadow","#5b3299"),("eye","#090711"),("pupil","#fff9ff"),("mouth","#2b1238")]
    for i,(name,c) in enumerate(sw):
        x=50+i*160; d.rectangle((x,100,x+120,220),fill=c); d.text((x,240),name,fill="#f5ebff")
    d.text((50,340),"Anatomy: 2 fingers + 1 thumb per hand; 3 toes per foot; 7 edge spikes;",fill="#f5ebff")
    d.text((50,380),"black eye fields + white pupils; small mouth; transparent background.",fill="#f5ebff")
    d.text((50,460),"No clothing, muzzle, nose, teeth, ears, horns, extra limbs, painterly, 3D, or pixel art.",fill="#f5ebff")
    im.save(R/"palette_anatomy_sheet.png","PNG",optimize=False)
    # Transition/debug sheet from representative frames.
    im,d=canvas("MON_TRANSITIONS_V1 — authored connector candidates")
    names=["idle_breathe_a_N_000.png","greeting_N_072.png","walk_N_136.png","run_N_144.png"]
    for i,n in enumerate(names):
        p=OUT/"frames"/n
        if p.exists():
            x=40+i*290; sprite=Image.open(p).convert("RGBA"); sprite.thumbnail((250,620)); im.paste(sprite,(x,80),sprite); d.text((x,710),n.split("_")[0],fill="#d7c2ff")
    im.save(R/"transition_sheet.png","PNG",optimize=False)
    # Viewport-only habitat still is an authored review derivative, not a
    # desktop screenshot. It documents the bounded shell and target policy.
    im=Image.new("RGB",(960,540),(18,10,36)); d=ImageDraw.Draw(im)
    d.rectangle((18,18,942,522),outline="#8c63d2",width=3)
    p=OUT/"frames"/"idle_breathe_a_N_000.png"
    if p.exists():
        sprite=Image.open(p).convert("RGBA"); sprite.thumbnail((420,420)); im.paste(sprite,(270,80),sprite)
    d.text((32,36),"MON_HABITAT_V1 • target-screen policy • viewport-only candidate",fill="#f5ebff")
    im.save(R/"habitat_viewport_still.png","PNG",optimize=False)
if __name__=="__main__": main()
