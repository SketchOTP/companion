#!/usr/bin/env python3
"""Write a deterministic hash manifest for selected visual review files."""
import argparse, hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out',type=Path,required=True); a=ap.parse_args()
    refs=[ROOT/'assets/source/p02/references/identity-approved.png',ROOT/'assets/source/p02/references/turnaround-approved.png']
    files=refs+sorted((a.out).glob('*.png'))
    result={'profile':'MON_REVIEW_MANIFEST_V1','status':'CANDIDATE_PENDING_OPERATOR_VISUAL_APPROVAL','files':[{'path':str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else p.name,'sha256':digest(p),'size_bytes':p.stat().st_size} for p in files if p.exists()]}
    (a.out/'review_manifest.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps(result,sort_keys=True))
if __name__=='__main__': main()
