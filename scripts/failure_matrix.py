#!/usr/bin/env python3
"""Fail-closed bounded lifecycle/recovery checks for the foundation."""
import argparse, json, os, pathlib, re, subprocess, tempfile

def run(binary, env, *args): return subprocess.run([binary,*args],env=env,capture_output=True,text=True,timeout=30)
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--output",type=pathlib.Path,required=True); a=ap.parse_args(); binary=os.environ.get("FOUNDATION_SUPERVISOR","target/release/ops-supervisor"); scenarios={}
    with tempfile.TemporaryDirectory(prefix="companion-failure-") as root:
        def environment():
            child=tempfile.mkdtemp(dir=root); e=os.environ.copy(); e["COMPANION_XDG_ROOT"]=child; e["COMPANION_CYCLES"]="2"; return e
        env=environment(); clean=run(binary,env,"--once"); scenarios["clean_start_stop"]="PASSED" if clean.returncode==0 and '"stopped"' in clean.stdout else "FAILED"
        absent=environment(); absent["COMPANION_SKIP_COMPANION"]="1"; no_comp=run(binary,absent,"--once"); scenarios["companion_store_absent"]="PASSED" if no_comp.returncode==0 and '"accepted":true' in no_comp.stdout and '"process":"companion-core","version"' not in no_comp.stdout else "FAILED"
        outage=environment(); outage["COMPANION_SKIP_CARE"]="1"; no_care=run(binary,outage,"--once"); scenarios["care_outage_degraded"]="PASSED" if no_care.returncode==0 and '"care-core"' not in no_care.stdout else "FAILED"
        bad_env=environment(); bad=subprocess.run([os.environ.get("FOUNDATION_CARE","target/release/care-core"),"--once"],env=bad_env,capture_output=True,text=True,timeout=30); scenarios["invalid_contract"]="PASSED" if bad.returncode!=0 else "FAILED"
        bridge_env=environment(); bridge=subprocess.run([os.environ.get("FOUNDATION_BRIDGE","target/release/godot-bridge"),"--once"],env=bridge_env,capture_output=True,text=True,timeout=30); scenarios["godot_disconnect_reconnect"]="PASSED" if bridge.returncode==0 and "bridge_handshake" in bridge.stdout else "FAILED"
        pids=[int(x) for x in re.findall(r'"pid":(\d+)',clean.stdout)]; scenarios["orphan_cleanup"]="PASSED" if clean.returncode==0 and all(not pathlib.Path(f"/proc/{p}").exists() for p in pids) else "FAILED"
    status="PASS" if all(v=="PASSED" for v in scenarios.values()) else "FAIL"; result={"status":status,"scenarios":scenarios,"evidence_ceiling":"E3_TARGET_TESTED","claim_boundary":"bounded synthetic lifecycle and explicit degraded-state observations; no production reliability claim"}; a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8"); print(json.dumps(result,sort_keys=True));
    if status!="PASS": raise SystemExit(1)
if __name__=="__main__": main()
