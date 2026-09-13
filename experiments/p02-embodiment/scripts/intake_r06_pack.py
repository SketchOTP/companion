#!/usr/bin/env python3
"""Fail-closed, byte-preserving intake for the R06 accepted playback pack."""
from __future__ import annotations
import argparse, hashlib, json, os, shutil, tempfile, uuid
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker
from PIL import Image

ROOT=Path(__file__).resolve().parents[3]
SCHEMA=ROOT/"contracts/schemas/mon-opaque-black-frame-source-pack-v1.schema.json"
def digest(p:Path)->str: return hashlib.sha256(p.read_bytes()).hexdigest()
def fsync_file(p:Path):
    with p.open("rb") as f: os.fsync(f.fileno())
def fsync_dir(p:Path):
    fd=os.open(p,os.O_RDONLY|os.O_DIRECTORY); os.fsync(fd); os.close(fd)
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--source",required=True); ap.add_argument("--out",required=True); ap.add_argument("--inject-failure",action="store_true"); a=ap.parse_args()
    src=Path(a.source); out=Path(a.out); pack=json.loads((src/"pack.json").read_text()); schema=json.loads(SCHEMA.read_text()); Draft202012Validator(schema,format_checker=FormatChecker()).validate(pack)
    stage=out.parent/(out.name+f".staging-{uuid.uuid4().hex}"); stage.mkdir(parents=True,exist_ok=False); (stage/"runtime/frames").mkdir(parents=True); (stage/"runtime/sidecars").mkdir();
    try:
        seen=[]
        for i,asset in enumerate(pack["source_assets"]):
            source=src/asset["filename"]; expected=asset["sha256"]
            if digest(source)!=expected: raise SystemExit(f"source hash mismatch: {asset['asset_id']}")
            with Image.open(source) as im:
                if im.size!=(1254,1254) or im.mode!="RGB": raise SystemExit(f"source format mismatch: {asset['asset_id']}")
                if max(max(im.getpixel(c)) for c in ((0,0),(1253,0),(0,1253),(1253,1253)))>4: raise SystemExit(f"source is not black-field eligible: {asset['asset_id']}")
            dst=stage/"runtime"/asset["filename"]; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(source,dst); fsync_file(dst)
            if digest(dst)!=expected: raise SystemExit(f"stored hash mismatch: {asset['asset_id']}")
            seen.append({"asset_id":asset["asset_id"],"source_sha256":expected,"source_filename":asset["filename"],"content_address":"sources/sha256/"+expected,"runtime_asset":"runtime/"+asset["filename"],"validation":{"dimensions":[1254,1254],"mode":"RGB","presentation_profile":"R05_BLACK_FIELD_RGB8_V1"}})
        for track in pack["tracks"]:
            for frame in track["frames"]:
                side=src/frame["sidecar_filename"]; dst=stage/"runtime"/frame["sidecar_filename"]; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(side,dst); fsync_file(dst)
        if a.inject_failure: raise RuntimeError("injected_mid_intake_failure")
        ingested=dict(pack); ingested["profile"]="MON_INGESTED_FRAME_PACK_V1"; ingested["source_profile"]=pack["profile"]; ingested["source_pack_id"]=pack["pack_id"]; ingested["source_assets"]=seen
        canonical={k:v for k,v in ingested.items() if k!="pack_digest"}; ingested["pack_digest"]=hashlib.sha256(json.dumps(canonical,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
        (stage/"runtime/pack.json").write_text(json.dumps(ingested,sort_keys=True,indent=2)+"\n")
        fsync_file(stage/"runtime/pack.json")
        receipt={"profile":"MON_OPAQUE_BLACK_FRAME_INTAKE_RECEIPT_V1","operation":"r06_c01_intake","source_pack_sha256":digest(src/"pack.json"),"runtime_pack_sha256":digest(stage/"runtime/pack.json"),"asset_count":len(seen),"source_bytes_mutated":False,"publication_state":"atomic_rename_complete","validation":"passed"}
        (stage/"receipt.json").write_text(json.dumps(receipt,sort_keys=True,indent=2)+"\n")
        fsync_file(stage/"receipt.json")
        fsync_dir(stage/"runtime")
        fsync_dir(stage)
        if out.exists(): raise SystemExit("refusing to replace existing intake output")
        os.rename(stage,out)
        fsync_dir(out.parent)
        print(json.dumps({"status":"PASSED","output":str(out),"assets":len(seen),"source_pack_sha256":digest(src/"pack.json"),"runtime_pack_sha256":digest(out/"runtime/pack.json")},indent=2))
    except BaseException:
        if stage.exists(): shutil.rmtree(stage)
        raise
if __name__=="__main__": main()
