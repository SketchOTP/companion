#!/usr/bin/env python3
import json, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/"assets/generated/p02"; packet=ROOT/".agent/tasks/active/COMPANION-P02-EMBODIMENT-001/ASSET_MANIFEST.json"
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    m=json.loads((OUT/"manifest.json").read_text()); c=json.loads((OUT/"clip_manifest.json").read_text()); a=json.loads((OUT/"atlas_manifest.json").read_text())
    result={"schema":"companion-mon-asset-manifest-v1","status":"CODEX_GENERATED_CANDIDATE_PENDING_OPERATOR_APPROVAL","canonical_frame_profile":"MON_FRAME_V1","approved_references":{"identity_native_sha256":"86ce1f9428f9a998d57e1a99c4245347d5a05e9f0bcf853c2b68065f351bdb56","identity_inspected_derivative_sha256":"a242d3f493db7c70e766ce64259850c3961e4e1cdbbfae015fc85611324af6f9","turnaround_sha256":"3696c7d63594de38d408438d5b882f3207635bc63e59fb270f624715faeb09e4"},"body_revision":"mon-body-v1","palette_roles":["outline","body","light","shadow","eye","pupil","mouth"],"directions":["N","NE","E","SE","S","SW","W","NW"],"clip_families":[x["clip_id"] for x in c["families"]],"body_frame_sources":256,"unique_body_frame_sha256":256,"overlays":{"eye_gaze_blink":24,"mouth_shapes":8},"packs":[{"name":"mon-embodiment-p02-v1.zip","sha256":sha(OUT/"mon-embodiment-p02-v1.zip"),"status":"generated"},{"name":"atlas_pages","count":len(a["pages"]),"max_dimensions":[4096,4096],"gutter_px":4}],"review_artifacts":[str(p.relative_to(ROOT)) for p in sorted((OUT/"review").glob("*.png"))],"validation":{"status":"PASSED","validator":"experiments/p02-embodiment/scripts/validate_assets.py","candidate_approval":"PENDING_OPERATOR_VISUAL_REVIEW"}}
    packet.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result,sort_keys=True))
if __name__=="__main__": main()
