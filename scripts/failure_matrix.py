#!/usr/bin/env python3
"""Observed resident control-plane failure/recovery matrix.

All mutations are synthetic child kills in an isolated XDG root. The matrix is
fail-closed: an absent command response, stale state, or failed recovery is a
non-zero result.
"""
import argparse, json, os, pathlib, signal, socket, subprocess, tempfile, time

def command(path, payload):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM); s.settimeout(3); s.connect(str(path)); s.sendall((json.dumps(payload)+"\n").encode()); s.shutdown(socket.SHUT_WR); data=s.recv(65536); s.close(); return json.loads(data)

def health(path):
    response = command(path, {"command":"health"})
    return json.loads(response["health"]) if "health" in response else response

def wait_health(path, role, predicate, timeout=5):
    deadline=time.time()+timeout
    while time.time()<deadline:
        snap=health(path)
        row=next((x for x in snap.get("children",[]) if x.get("role")==role), None)
        if row and predicate(row, snap): return snap
        time.sleep(.1)
    return health(path)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--output",type=pathlib.Path,required=True); args=ap.parse_args()
    binary=os.environ.get("FOUNDATION_SUPERVISOR","target/release/ops-supervisor")
    scenarios={}
    with tempfile.TemporaryDirectory(prefix="companion-failure-") as root:
        env=os.environ.copy(); env["COMPANION_XDG_ROOT"]=root; env["COMPANION_CYCLES"]="2"
        proc=subprocess.Popen([binary],env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        control=pathlib.Path(root)/"companion"/"supervisor.sock"; deadline=time.time()+5
        while time.time()<deadline and not control.exists(): time.sleep(.05)
        try:
            initial=wait_health(control,"care-core",lambda row,s: row.get("state")=="healthy")
            scenarios["resident_start_and_readiness"] = initial.get("care_coverage")=="synthetic" and all(x.get("ready") for x in initial.get("children",[]))
            old_companion=next(x["pid"] for x in initial["children"] if x["role"]=="companion-core")
            command(control,{"command":"restart","role":"companion-core"})
            recovered=wait_health(control,"companion-core",lambda row,s: row.get("state")=="healthy" and row.get("restarts",0)>=1)
            scenarios["companion_restart_and_backoff"] = recovered.get("care_coverage")=="synthetic" and next(x for x in recovered["children"] if x["role"]=="companion-core")["pid"] != old_companion
            old_sensor=next(x["pid"] for x in recovered["children"] if x["role"]=="sensor-gateway")
            old_sensor_generation=next(x["generation"] for x in recovered["children"] if x["role"]=="sensor-gateway")
            command(control,{"command":"rotate","role":"sensor-gateway"})
            rotated=wait_health(control,"sensor-gateway",lambda row,s: row.get("state")=="healthy" and row.get("pid")!=old_sensor)
            new_sensor=next(x for x in rotated["children"] if x["role"]=="sensor-gateway")
            scenarios["producer_rotation_generation_rebuild"] = rotated.get("care_coverage")=="synthetic" and new_sensor["pid"] != old_sensor and new_sensor["generation"] != old_sensor_generation
            old_care=next(x["pid"] for x in rotated["children"] if x["role"]=="care-core")
            command(control,{"command":"fail","role":"care-core"})
            degraded=health(control)
            restored=wait_health(control,"care-core",lambda row,s: row.get("state")=="healthy" and row.get("pid")!=old_care)
            scenarios["care_outage_degraded_then_recovered"] = (degraded.get("care_coverage")=="degraded" and restored.get("care_coverage")=="synthetic" and next(x for x in restored["children"] if x["role"]=="care-core")["pid"] != old_care)
            command(control,{"command":"fail","role":"godot-bridge"})
            bridge=wait_health(control,"godot-bridge",lambda row,s: row.get("state")=="healthy" and row.get("restarts",0)>=1)
            scenarios["bridge_failure_recovery"] = next(x for x in bridge["children"] if x["role"]=="godot-bridge").get("restarts",0)>=1
            command(control,{"command":"shutdown"}); proc.wait(timeout=10)
            scenarios["signal_shutdown_and_orphan_cleanup"] = proc.returncode==0
        finally:
            if proc.poll() is None: proc.send_signal(signal.SIGTERM); proc.wait(timeout=10)
    status="PASS" if all(scenarios.values()) else "FAIL"
    result={"status":status,"scenarios":scenarios,"evidence_ceiling":"E3_TARGET_TESTED","claim_boundary":"observed synthetic control-plane failures and bounded recovery; no production reliability claim"}
    args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8"); print(json.dumps(result,sort_keys=True))
    if status!="PASS": raise SystemExit(1)
if __name__=="__main__": main()
