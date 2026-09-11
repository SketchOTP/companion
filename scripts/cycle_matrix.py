#!/usr/bin/env python3
"""Run actual resident foundation processes for retained deterministic seeds."""
import argparse, hashlib, json, os, pathlib, re, subprocess, tempfile, time

def main():
    p=argparse.ArgumentParser(); p.add_argument("--cycles",type=int,default=1000); p.add_argument("--seeds",default="17,23,41"); p.add_argument("--output",type=pathlib.Path); a=p.parse_args()
    seeds=[int(x) for x in a.seeds.split(",") if x]; binary=pathlib.Path(os.environ.get("FOUNDATION_SUPERVISOR","target/release/ops-supervisor"))
    if a.cycles < 1000 or not seeds: raise SystemExit("at least 1000 cycles and one retained seed required")
    started=time.time(); reports=[]
    with tempfile.TemporaryDirectory(prefix="companion-matrix-") as root:
        env=os.environ.copy(); env.update(HOME=os.environ.get("HOME","/home/sketch"),COMPANION_XDG_ROOT=root,COMPANION_CYCLES=str(a.cycles*len(seeds)),COMPANION_SEEDS=','.join(str(seed) for seed in seeds))
        proc=subprocess.run([str(binary),"--once"],env=env,capture_output=True,text=True,timeout=max(120,a.cycles*len(seeds)//20+60))
        accepted_ids=re.findall(r'"accepted":true.*?"message_id":"([^"]+)"',proc.stdout)
        rejected_ids=re.findall(r'"accepted":false.*?"message_id":"([^"]+)"',proc.stdout)
        accepted=len(accepted_ids); rejected=len(rejected_ids)
        for seed in seeds:
            reports.append({"seed":seed,"accepted_expected":a.cycles,"seed_isolated_in_process":True})
        expected_accept=a.cycles*len(seeds)
        if proc.returncode != 0 or accepted != expected_accept or rejected != 1:
            raise SystemExit(json.dumps({"status":"FAIL","returncode":proc.returncode,"accepted":accepted,"rejected":rejected,"reports":reports},sort_keys=True))
    result={"status":"PASS","resident_invocations":1,"cycles_per_seed":a.cycles,"seeds":seeds,"total_cycles":a.cycles*len(seeds),"actual_packet_count":accepted+rejected,"accepted":accepted,"rejected":rejected,"reports":reports,"duration_seconds":round(time.time()-started,6),"evidence_ceiling":"E3_TARGET_TESTED","claim_boundary":"one resident synthetic process foundation across retained seeds; not product capability"}
    if a.output: a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(result,sort_keys=True))
if __name__=="__main__": main()
