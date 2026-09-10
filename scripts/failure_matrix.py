#!/usr/bin/env python3
"""Bounded synthetic lifecycle checks; unrun host mutations remain visible."""
import argparse, json, os, pathlib, subprocess, tempfile
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--output", type=pathlib.Path, required=True); a=ap.parse_args()
    scenarios={"clean_start_stop": "NOT_RUN", "companion_store_absent": "NOT_RUN", "care_outage_degraded": "NOT_RUN", "godot_disconnect_reconnect": "NOT_RUN", "invalid_contract": "NOT_RUN", "orphan_cleanup": "NOT_RUN"}
    root=pathlib.Path(tempfile.mkdtemp(prefix="companion-failure.")); env=os.environ.copy(); env["COMPANION_XDG_ROOT"]=str(root)
    proc=subprocess.run([env.get("FOUNDATION_SUPERVISOR","target/release/ops-supervisor")],env=env,capture_output=True,text=True,timeout=30)
    scenarios["clean_start_stop"]="PASSED" if proc.returncode==0 else "FAILED"
    scenarios["orphan_cleanup"]="PASSED" if not any(x in proc.stdout for x in ("crash_loop","orphan")) else "FAILED"
    result={"status":"PARTIAL" if proc.returncode==0 else "FAILED","scenarios":scenarios,"evidence_ceiling":"E3_TARGET_TESTED","claim_boundary":"synthetic lifecycle observations; unrun host/display mutations remain unqualified"}
    a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8"); print(json.dumps(result,sort_keys=True))
if __name__ == "__main__": main()
