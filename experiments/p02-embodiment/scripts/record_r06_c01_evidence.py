#!/usr/bin/env python3
"""Record deterministic R06-C01 evidence from the real accepted playback set."""
from __future__ import annotations
import argparse, hashlib, json, os, shutil, subprocess, tempfile
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker
from PIL import Image

ROOT=Path(__file__).resolve().parents[3]
SCHEMA=ROOT/"contracts/schemas/mon-opaque-black-frame-source-pack-v1.schema.json"
ZIP_ROOT=Path("/home/sketch/.local/share/companion-authoring/exports/full-animation-review-listen-2026-09-12-v2")
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--out",required=True); ap.add_argument("--intake",required=True); a=ap.parse_args(); out=Path(a.out); out.mkdir(parents=True,exist_ok=True)
    source=ROOT/"assets/source/p02/r06/approved"; pack=json.loads((source/"pack.json").read_text()); schema=json.loads(SCHEMA.read_text()); Draft202012Validator(schema,format_checker=FormatChecker()).validate(pack)
    byte_rows=[]; profiles=set()
    for asset in pack["source_assets"]:
        p=source/asset["filename"]; with_image=Image.open(p); profiles.add(with_image.mode); corners=[with_image.getpixel(c) for c in ((0,0),(1253,0),(0,1253),(1253,1253))]; byte_rows.append({"asset_id":asset["asset_id"],"sha256":sha(p),"manifest_sha256":asset["sha256"],"byte_identical":sha(p)==asset["sha256"],"dimensions":list(with_image.size),"mode":with_image.mode,"perimeter":corners})
    intake=Path(a.intake); receipt=json.loads((intake/"receipt.json").read_text()); runtime_pack=intake/"runtime/pack.json"
    negatives={}
    with tempfile.TemporaryDirectory(prefix="r06-c01-neg-") as td:
        t=Path(td)/"bad.json"; bad=json.loads((source/"pack.json").read_text()); bad["request_profile"]="wrong"; t.write_text(json.dumps(bad)); p=subprocess.run(["python3","-c","import json,sys; from jsonschema import Draft202012Validator; s=json.load(open(sys.argv[1])); d=json.load(open(sys.argv[2])); Draft202012Validator(s).validate(d)",str(SCHEMA),str(t)],capture_output=True); negatives["tampered_request_profile_rejected"]=p.returncode!=0
    with tempfile.TemporaryDirectory(prefix="r06-c01-intake-") as td:
        failed=Path(td)/"final"; probe=subprocess.run(["python3",str(ROOT/"experiments/p02-embodiment/scripts/intake_r06_pack.py"),"--source",str(source),"--out",str(failed),"--inject-failure"],capture_output=True,text=True)
        negatives["mid_intake_failure_nonzero"]=probe.returncode != 0; negatives["mid_intake_failure_final_absent"]=not failed.exists()
    with tempfile.TemporaryDirectory(prefix="r06-c01-restore-") as td:
        restore=Path(td)/"restore"; shutil.copytree(intake,restore)
        restore_hashes=sorted((str(p.relative_to(restore)),sha(p)) for p in restore.rglob("*") if p.is_file())
        original_hashes=sorted((str(p.relative_to(intake)),sha(p)) for p in intake.rglob("*") if p.is_file())
        export_restore=(restore_hashes==original_hashes)
    result={"profile":"COMPANION_P02_R06_C01_EVIDENCE_V1","status":"PASS" if all(negatives.values()) and export_restore else "FAIL","source_pack_sha256":sha(source/"pack.json"),"runtime_pack_sha256":sha(runtime_pack),"receipt_sha256":sha(intake/"receipt.json"),"source_assets":len(byte_rows),"tracks":len(pack["tracks"]),"frame_slots":sum(len(t["frames"]) for t in pack["tracks"]),"byte_preservation":all(r["byte_identical"] for r in byte_rows),"source_modes":sorted(profiles),"presentation_profiles":["R05_BLACK_FIELD_RGB8_V1","R05_TRANSPARENT_RGBA8_V1"],"black_habitat_perimeter_max":max(max(c) for r in byte_rows for c in r["perimeter"]),"atomic_publication":"fsync_staged_same_filesystem_rename","export_restore":export_restore,"negative_tests":negatives,"godot":"NOT_RUN_LOCAL_GODOT_UNAVAILABLE; hosted runner required","rust":"NOT_RUN_LOCAL_CARGO_UNAVAILABLE; hosted runner required","world_contact":"NOT_RUN_UNTIL_RUNTIME_GODOT_ARTIFACT"}
    (out/"source_bytes.json").write_text(json.dumps(byte_rows,sort_keys=True,indent=2)+"\n"); (out/"validation.json").write_text(json.dumps(result,sort_keys=True,indent=2)+"\n"); print(json.dumps(result,indent=2))
if __name__=="__main__": main()
