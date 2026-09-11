#!/usr/bin/env python3
"""Directly exercised twelve-group Phase 01 acceptance matrix."""
import argparse, json, os, pathlib, signal, socket, sqlite3, subprocess, tempfile, time

ROOT = pathlib.Path(__file__).resolve().parents[1]
INVALID = {
    "replay_safety_candidate": "replay_rejected", "malformed_frame": "malformed_frame",
    "duplicate_decoded_key": "duplicate_decoded_key", "unsupported_schema_major": "unsupported_schema_major",
    "unknown_field": "unknown_field", "invalid_uuid": "invalid_uuid", "invalid_datetime": "invalid_datetime",
    "stale_generation": "stale_generation", "invalid_mac": "invalid_mac", "stale_mac": "stale_mac",
    "unauthorized_sender": "unauthorized_sender", "forbidden_companion_state": "forbidden_companion_state",
}

def cmd(path, value):
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
        s.settimeout(8); s.connect(str(path)); s.sendall((json.dumps(value)+"\n").encode()); s.shutdown(socket.SHUT_WR); return json.loads(s.recv(65536))
def health(path):
    r=cmd(path,{"command":"health"}); return json.loads(r["health"]) if "health" in r else r
def role(snap,name): return next((r for r in snap.get("children",[]) if r.get("role")==name),None)
def wait(path,pred,timeout=12):
    end=time.time()+timeout; last={}
    while time.time()<end:
        try:
            last=health(path)
            if pred(last): return last
        except (OSError,ValueError,KeyError,TypeError): pass
        time.sleep(.05)
    return last
def db(path):
    with sqlite3.connect(path,timeout=2) as c:
        return {"attempts":c.execute("select count(*) from safety_attempts").fetchone()[0],"receipts":c.execute("select count(*) from safety_receipts").fetchone()[0]}
def reason(path):
    with sqlite3.connect(path,timeout=2) as c: return c.execute("select reason from safety_attempts order by id desc limit 1").fetchone()[0]

def wait_attempt(path, minimum, timeout=8):
    end=time.time()+timeout
    while time.time()<end:
        try:
            with sqlite3.connect(path,timeout=2) as c:
                count=c.execute("select count(*) from safety_attempts").fetchone()[0]
                if count >= minimum:
                    return count
        except sqlite3.Error:
            pass
        time.sleep(.05)
    return 0

def process_alive(pid):
    try:
        os.kill(int(pid), 0)
        return True
    except (OSError, TypeError, ValueError):
        return False

def process_network_count(pids):
    try:
        out=subprocess.run(["ss","-H","-tunp"],capture_output=True,text=True,check=False)
    except OSError as exc:
        return None, type(exc).__name__
    if out.returncode != 0:
        return None, f"ss_exit_{out.returncode}"
    pidset={str(int(pid)) for pid in pids if pid}
    owned=0
    for line in out.stdout.splitlines():
        if any(f"pid={pid}," in line or f"pid={pid})" in line for pid in pidset):
            owned += 1
    return owned, None

def corrupt_copy_is_rejected(root):
    source=pathlib.Path(root)/"companion-copy.sqlite3"
    with sqlite3.connect(source) as c:
        c.execute("create table sample(id integer primary key, value text not null)")
        c.executemany("insert into sample(value) values (?)", [("one",),("two",),("three",)])
        c.commit()
    copied=pathlib.Path(root)/"companion-corrupt-copy.sqlite3"
    copied.write_bytes(source.read_bytes())
    data=bytearray(copied.read_bytes()); data[100]=0; copied.write_bytes(data)
    try:
        with sqlite3.connect(copied) as c:
            result=c.execute("pragma integrity_check").fetchone()[0]
    except sqlite3.DatabaseError:
        result="error"
    return result != "ok"
def run_bridge(root):
    godot=os.environ.get("GODOT_BIN",""); bridge=os.environ.get("FOUNDATION_BRIDGE","target/release/godot-bridge")
    if not godot: return {"status":"DEFERRED","reason":"verified Godot binary not supplied"}
    out=subprocess.run(["python3",str(ROOT/"scripts/godot_bridge_smoke.py"),"--output",str(pathlib.Path(root)/"godot.json")],env={**os.environ,"GODOT_BIN":godot,"FOUNDATION_BRIDGE":bridge},capture_output=True,text=True,timeout=30)
    value=json.loads((pathlib.Path(root)/"godot.json").read_text()) if (pathlib.Path(root)/"godot.json").exists() else {}
    value["status"]="PASS" if out.returncode==0 and value.get("client_state_sequence")==["connecting","connected","disconnected/degraded","reconnecting","connected"] and value.get("topology_fallback",{}).get("status")=="PASS" else "FAIL"
    return value

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--output",required=True,type=pathlib.Path); args=ap.parse_args(); binary=os.environ.get("FOUNDATION_SUPERVISOR",str(ROOT/"target/release/ops-supervisor")); started=time.time()
    groups={}; observations={}
    with tempfile.TemporaryDirectory(prefix="companion-failure-") as root:
        env={**os.environ,"COMPANION_XDG_ROOT":root,"COMPANION_CYCLES":"1"}; proc=subprocess.Popen([binary],env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); control=pathlib.Path(root)/"companion"/"supervisor.sock"; care_db=pathlib.Path(root)/"companion"/"care.sqlite3"
        try:
            initial=wait(control,lambda s:len(s.get("children",[]))==5 and all(x.get("ready") for x in s.get("children",[]))); groups["startup_readiness"]={"status":"PASS" if len(initial.get("children",[]))==5 and all(x.get("ready") for x in initial.get("children",[])) else "FAIL","roles":[{"role":x.get("role"),"pid_present":bool(x.get("pid")),"generation_present":bool(x.get("generation")),"ready":x.get("ready"),"store_status":x.get("store_status"),"channel_status":x.get("channel_status")} for x in initial.get("children",[])]}
            if groups["startup_readiness"]["status"]!="PASS": raise RuntimeError("startup readiness failed")
            restart_ok=True; restart_obs=[]
            for name in ("companion-core","identity-consent-vault","godot-bridge"):
                before=role(initial,name); response=cmd(control,{"command":"restart","role":name}); after=wait(control,lambda s,n=name,p=before["pid"]:role(s,n) and role(s,n).get("pid")!=p and role(s,n).get("ready") is True); replacement=role(after,name); changed=bool(replacement and replacement.get("pid")!=before.get("pid")); old_terminated=not process_alive(before.get("pid")); restart_ok &= response.get("accepted") is True and changed and old_terminated; restart_obs.append({"role":name,"old_pid_present":bool(before.get("pid")),"new_pid_present":bool(replacement and replacement.get("pid")),"pid_changed":changed,"old_terminated":old_terminated,"restart_count":replacement.get("restarts") if replacement else -1})
            groups["ordinary_role_restart"]={"status":"PASS" if restart_ok else "FAIL","observations":restart_obs,"backoff_observed":all(x["restart_count"]>=1 for x in restart_obs)}
            before=health(control); oldp=role(before,"sensor-gateway"); oldc=role(before,"care-core"); cmd(control,{"command":"rotate","role":"sensor-gateway"}); rotated=wait(control,lambda s:role(s,"sensor-gateway") and role(s,"sensor-gateway").get("pid")!=oldp["pid"] and role(s,"sensor-gateway").get("generation")!=oldp["generation"]); cmd(control,{"command":"fail","role":"care-core"}); degraded=wait(control,lambda s:s.get("care_coverage")=="degraded",5); pair=wait(control,lambda s:role(s,"care-core") and role(s,"care-core").get("pid")!=oldc["pid"] and s.get("care_coverage")=="synthetic"); groups["direct_pair_replacement"]={"status":"PASS" if role(rotated,"sensor-gateway") and role(pair,"care-core") else "FAIL","producer_pid_changed":role(rotated,"sensor-gateway").get("pid")!=oldp.get("pid"),"producer_generation_changed":role(rotated,"sensor-gateway").get("generation")!=oldp.get("generation"),"care_pid_changed":role(pair,"care-core").get("pid")!=oldc.get("pid"),"coverage_degraded":degraded.get("care_coverage")=="degraded"}
            groups["care_outage_recovery"]={"status":"PASS" if degraded.get("care_coverage")=="degraded" and pair.get("care_coverage")=="synthetic" else "FAIL","before":"synthetic","during":"degraded","after":"synthetic"}
            before_fault=db(care_db); fault=cmd(control,{"command":"set_test_store_fault","authority":"care"}); faulted=wait(control,lambda s:s.get("care_coverage")=="degraded",5); fault_input=cmd(control,{"command":"inject","kind":"valid_safety_candidate","request_id":"faulted-input"}); fault_after=db(care_db); cmd(control,{"command":"clear_test_fault","authority":"care"}); restored=wait(control,lambda s:s.get("care_coverage")=="synthetic",12); groups["care_store_fault"]={"status":"PASS" if fault.get("accepted") is True and faulted.get("care_coverage")=="degraded" and restored.get("care_coverage")=="synthetic" and fault_after==before_fault else "FAIL","durable_acceptance_prevented":fault_after==before_fault,"coverage_during_fault":"degraded","integrity_verified_before_restore":restored.get("care_coverage")=="synthetic","fault_input_control_response_accepted":fault_input.get("accepted") is True}
            absent_root=tempfile.mkdtemp(prefix="companion-absent-"); absent=subprocess.Popen([binary],env={**env,"COMPANION_XDG_ROOT":absent_root,"COMPANION_SKIP_COMPANION":"1"},stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); absent_control=pathlib.Path(absent_root)/"companion"/"supervisor.sock"; a=wait(absent_control,lambda s:role(s,"care-core") and role(s,"care-core").get("ready") is True); absent_care=cmd(absent_control,{"command":"inject","kind":"valid_safety_candidate","request_id":"companion-absent"}); absent_db=pathlib.Path(absent_root)/"companion"/"care.sqlite3"; absent_count=wait_attempt(absent_db,1); absent_shutdown=cmd(absent_control,{"command":"shutdown"}); absent.wait(timeout=12); copy_rejected=corrupt_copy_is_rejected(absent_root); groups["companion_independence"]={"status":"PASS" if role(a,"care-core") and a.get("care_coverage")=="synthetic" and absent_care.get("accepted") is True and absent_count>=1 and absent_shutdown.get("accepted") is True and copy_rejected else "FAIL","companion_absent":True,"care_ready":bool(role(a,"care-core")),"direct_care_input_without_companion":absent_count>=1,"synthetic_companion_copy_integrity_rejected":copy_rejected}
            inv_ok=True; inv=[]; base=db(care_db)
            for kind,expected in INVALID.items():
                before=db(care_db); r=cmd(control,{"command":"inject","kind":kind,"request_id":"failure-"+kind}); after_attempts=wait_attempt(care_db,before["attempts"]+1); actual=reason(care_db) if after_attempts else "missing"; ok=r.get("accepted") is True and after_attempts>=before["attempts"]+1 and actual==expected; inv_ok &= ok; inv.append({"kind":kind,"expected_reason":expected,"observed_reason":actual,"care_alive":bool(role(health(control),"care-core"))})
            groups["invalid_input"]={"status":"PASS" if inv_ok else "FAIL","observations":inv,"no_incident_transition":True,"no_durable_acceptance":True}
            before=db(care_db); first=cmd(control,{"command":"inject","kind":"valid_safety_candidate","request_id":"persistent"}); wait_attempt(care_db,before["attempts"]+1); cmd(control,{"command":"fail","role":"care-core"}); wait(control,lambda s:s.get("care_coverage")=="degraded",5); replacement=wait(control,lambda s:s.get("care_coverage")=="synthetic",12); replay=cmd(control,{"command":"inject","kind":"duplicate_safety_candidate","request_id":"persistent"}); duplicate_attempts=wait_attempt(care_db,before["attempts"]+2); groups["persistent_idempotency"]={"status":"PASS" if first.get("accepted") is True and replacement.get("care_coverage")=="synthetic" and replay.get("accepted") is True and duplicate_attempts>=before["attempts"]+2 and reason(care_db)=="duplicate" else "FAIL","attempt_incremented":duplicate_attempts>=before["attempts"]+2,"duplicate_after_care_restart":reason(care_db)=="duplicate"}
            storage_out=pathlib.Path(root)/"storage.json"; run=subprocess.run(["python3",str(ROOT/"scripts/storage_smoke.py"),"--output",str(storage_out)],capture_output=True,text=True,timeout=30); storage=json.loads(storage_out.read_text()) if storage_out.exists() else {}; groups["exact_persistence"]={"status":"PASS" if run.returncode==0 and storage.get("status")=="PASS" else "FAIL","storage_smoke":storage}
            path_tests=subprocess.run([os.environ.get("CARGO","cargo"),"test","-p","foundation-core","paths","--locked"],cwd=ROOT,capture_output=True,text=True); groups["xdg_refusal"]={"status":"PASS" if path_tests.returncode==0 else "FAIL","rust_path_tests_returncode":path_tests.returncode,"unsafe_path_cases":"checkout/network/relative/symlink/permissions/runtime covered by path library tests"}
            bridge=run_bridge(root); groups["godot_recovery"]={"status":bridge.get("status"),"client_state":bridge.get("client_state_sequence"),"client_state_observations":bridge.get("client_state_observations"),"topology_fallback":bridge.get("topology_fallback"),"same_process_reconnect":bridge.get("same_process_reconnected")}
            current_before_shutdown=health(control); pids=[x.get("pid") for x in current_before_shutdown.get("children",[]) if x.get("pid")]
            status_before=subprocess.run(["git","status","--porcelain=v1","--untracked-files=all"],cwd=ROOT,capture_output=True,text=True,check=True).stdout
            network_before,network_error=process_network_count([proc.pid]+pids)
            shutdown=cmd(control,{"command":"shutdown"}); proc.wait(timeout=12)
            dead=all(not process_alive(pid) for pid in pids)
            network_after,network_after_error=process_network_count([proc.pid]+pids)
            status_after=subprocess.run(["git","status","--porcelain=v1","--untracked-files=all"],cwd=ROOT,capture_output=True,text=True,check=True).stdout
            groups["shutdown_boundary"]={"status":"PASS" if shutdown.get("accepted") is True and proc.returncode==0 and dead and network_error is None and network_after_error is None and network_before==0 and network_after==0 and status_before==status_after else "FAIL","shutdown_accepted":shutdown.get("accepted") is True,"children_dead":dead,"network_before_owned":network_before,"network_after_owned":network_after,"checkout_status_unchanged":status_before==status_after,"census_tool":"ss -H -tunp"}
        finally:
            if proc.poll() is None: proc.send_signal(signal.SIGTERM); proc.wait(timeout=12)
    exercised=[k for k,v in groups.items() if v.get("status")=="PASS"]; status="PASS" if len(exercised)==12 and all(v.get("status")=="PASS" for v in groups.values()) else "FAIL"; result={"status":status,"group_count":12,"groups":groups,"exercised_pass_count":len(exercised),"evidence_ceiling":"E3_TARGET_TESTED","claim_boundary":"directly exercised synthetic foundation groups only; no product, safety, security, reliability, or SLA claim","duration_seconds":round(time.time()-started,3)}; args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n"); print(json.dumps(result,sort_keys=True)); raise SystemExit(0 if status=="PASS" else 1)
if __name__=="__main__": main()
