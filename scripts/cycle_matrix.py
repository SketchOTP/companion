#!/usr/bin/env python3
"""Run actual resident foundation processes for retained deterministic seeds."""
import argparse, hashlib, json, os, pathlib, re, subprocess, tempfile, time

def main():
    p=argparse.ArgumentParser(); p.add_argument("--cycles",type=int,default=1000); p.add_argument("--seeds",default="17,23,41"); p.add_argument("--output",type=pathlib.Path); a=p.parse_args()
    seeds=[int(x) for x in a.seeds.split(",") if x]; binary=pathlib.Path(os.environ.get("FOUNDATION_SUPERVISOR","target/release/ops-supervisor"))
    if a.cycles < 1000 or not seeds: raise SystemExit("at least 1000 cycles and one retained seed required")
    started=time.time(); reports=[]
    for seed in seeds:
        with tempfile.TemporaryDirectory(prefix="companion-matrix-") as root:
            env=os.environ.copy(); env.update(HOME=os.environ.get("HOME","/home/sketch"),COMPANION_XDG_ROOT=root,COMPANION_CYCLES=str(a.cycles),COMPANION_SEED=str(seed))
            proc=subprocess.run([str(binary),"--once"],env=env,capture_output=True,text=True,timeout=max(60,a.cycles//20+30))
            accepted=len(re.findall(r'"accepted":true',proc.stdout)); rejected=len(re.findall(r'"accepted":false',proc.stdout));
            reports.append({"seed":seed,"returncode":proc.returncode,"actual_packets":accepted+rejected,"accepted":accepted,"rejected":rejected,"stdout_sha256":hashlib.sha256(proc.stdout.encode()).hexdigest()})
            if proc.returncode != 0 or accepted != a.cycles or rejected != 1: raise SystemExit(json.dumps({"status":"FAIL","seed":seed,"reports":reports},sort_keys=True))
    result={"status":"PASS","cycles_per_seed":a.cycles,"seeds":seeds,"total_cycles":a.cycles*len(seeds),"actual_packet_count":sum(x["actual_packets"] for x in reports),"reports":reports,"duration_seconds":round(time.time()-started,6),"evidence_ceiling":"E3_TARGET_TESTED","claim_boundary":"actual synthetic resident-process messages; not product capability"}
    if a.output: a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(result,sort_keys=True))
if __name__=="__main__": main()
