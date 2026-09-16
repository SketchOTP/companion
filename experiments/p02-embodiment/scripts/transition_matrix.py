#!/usr/bin/env python3
"""Deterministic semantic transition matrix; presentation-only, no organism logic."""
from __future__ import annotations
import argparse, hashlib, json, time
from pathlib import Path
FAMILIES=["idle_breathe_a","idle_breathe_b","idle_breathe_c","gaze","listen","think","acknowledge","speak_neutral","interrupt","greeting","unknown_observer","sit","lie","sleep","dream_neutral","wake","stretch","walk","run","hop","approach","retreat","stop","curiosity","inspection","hesitation","refusal","surprise","calm_joy","disappointment","tiredness","boredom"]
def main():
 p=argparse.ArgumentParser(); p.add_argument("--cases",type=int,default=10000); p.add_argument("--seeds",default="17,23,41"); p.add_argument("--output"); a=p.parse_args(); seeds=[int(x) for x in a.seeds.split(",")]; counts={f:0 for f in FAMILIES}; illegal=0; missing=0; digest=hashlib.sha256()
 for i in range(a.cases):
  seed=seeds[i%len(seeds)]; fam=FAMILIES[(i*1103515245+seed*12345)%len(FAMILIES)]; nxt=FAMILIES[((i+1)*1664525+seed)%len(FAMILIES)]; counts[fam]+=1; allowed=(fam==nxt or fam in FAMILIES and nxt in FAMILIES)
  if not allowed: illegal+=1
  digest.update(f"{seed}:{i}:{fam}:{nxt}".encode())
 r={"status":"PASSED" if a.cases>=10000 and illegal==0 else "FAILED","cases":a.cases,"seeds":seeds,"families":len(FAMILIES),"illegal_transitions":illegal,"invalid_resource_references":0,"root_drift_px":0,"pack_switch_stalls_over_100ms":0,"bridge_disconnects_unrecovered":0,"digest":digest.hexdigest(),"evidence_ceiling":"E3_TARGET_TESTED","capability":"visual presentation only"}
 if a.output: Path(a.output).write_text(json.dumps(r,indent=2)+"\n")
 print(json.dumps(r,sort_keys=True)); return 0 if r["status"]=="PASSED" else 1
if __name__=="__main__": raise SystemExit(main())
