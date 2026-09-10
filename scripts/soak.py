#!/usr/bin/env python3
"""Resident 60-minute target-host soak driver with deterministic injections."""
import argparse, hashlib, json, os, pathlib, signal, socket, subprocess, tempfile, time

def command(path, payload):
    s=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM); s.settimeout(3); s.connect(str(path)); s.sendall((json.dumps(payload)+"\n").encode()); s.shutdown(socket.SHUT_WR); data=s.recv(65536); s.close(); response=json.loads(data); return json.loads(response["health"]) if "health" in response else response

def resource_snapshot(pids):
    rss=0; cpu_ticks=0; errors=[]
    for pid in pids:
        try:
            fields=pathlib.Path(f"/proc/{pid}/stat").read_text().split(); cpu_ticks += int(fields[13])+int(fields[14]); rss += int(pathlib.Path(f"/proc/{pid}/statm").read_text().split()[1]) * os.sysconf("SC_PAGE_SIZE")
        except (OSError,ValueError,IndexError) as exc: errors.append(type(exc).__name__)
    return {"rss_bytes":rss,"cpu_ticks":cpu_ticks,"proc_errors":errors}

def network_snapshot(pids):
    try:
        result=subprocess.run(["ss","-H","-tunp"],capture_output=True,text=True,check=False)
    except OSError as exc:
        return {"owned_count":None,"error":type(exc).__name__}
    if result.returncode != 0: return {"owned_count":None,"error":f"ss_exit_{result.returncode}"}
    pidset={int(pid) for pid in pids}; owned=0
    for line in result.stdout.splitlines():
        if pidset & {int(value) for value in __import__("re").findall(r"pid=(\d+)",line)}: owned += 1
    return {"owned_count":owned,"error":None}

def main():
    p=argparse.ArgumentParser(); p.add_argument("--duration-seconds",type=int,default=3600); p.add_argument("--interval",type=int,default=60); p.add_argument("--output",type=pathlib.Path,required=True); a=p.parse_args()
    if a.duration_seconds < 3600: raise SystemExit("duration must be at least 3600 seconds")
    binary=os.environ.get("FOUNDATION_SUPERVISOR","target/release/ops-supervisor"); started=time.time(); samples=[]; failures=[]; injections=[]
    baseline_checkout=subprocess.run(["git","status","--porcelain=v1","--",".",":!.gitignore"],capture_output=True,text=True,check=True).stdout
    with tempfile.TemporaryDirectory(prefix="companion-soak-") as root:
        env=os.environ.copy(); env["COMPANION_XDG_ROOT"]=root; proc=subprocess.Popen([binary],env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        godot_proc = None
        if env.get("GODOT_BIN"):
            godot_proc = subprocess.Popen([env["GODOT_BIN"], "--headless", "--path", str(pathlib.Path(__file__).resolve().parents[1]/"godot")], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        godot_resident_observed = bool(godot_proc and godot_proc.poll() is None)
        resident_observed=proc.poll() is None; control=pathlib.Path(root)/"companion"/"supervisor.sock"; startup_deadline=time.time()+10
        while time.time() < startup_deadline and not control.exists() and proc.poll() is None:
            time.sleep(0.05)
        if not control.exists():
            proc.terminate()
            proc.wait(timeout=15)
            if godot_proc and godot_proc.poll() is None: godot_proc.terminate(); godot_proc.wait(timeout=10)
            raise RuntimeError("supervisor control socket did not become ready")
        deadline=started+a.duration_seconds
        while time.time()<deadline:
            elapsed=time.time()-started
            try:
                snap=command(control,{"command":"health"}); pids=[x.get("pid") for x in snap.get("children",[]) if x.get("pid")]; resources=resource_snapshot(pids)
                current_checkout=subprocess.run(["git","status","--porcelain=v1","--",".",":!.gitignore"],capture_output=True,text=True,check=True).stdout
                network=network_snapshot([proc.pid]+[x.get("pid") for x in snap.get("children",[]) if x.get("pid")])
                samples.append({"elapsed_seconds":round(elapsed,3),"status":snap.get("status"),"care_coverage":snap.get("care_coverage"),"children":snap.get("children",[]),"resources":resources,"network":network,"checkout_write_detected":current_checkout != baseline_checkout,"health_sha256":hashlib.sha256(json.dumps(snap,sort_keys=True).encode()).hexdigest()})
                for offset, role, action in ((60,"companion-core","restart"),(120,"sensor-gateway","rotate"),(180,"godot-bridge","restart"),(240,"care-core","fail")):
                    if offset <= elapsed < offset + a.interval:
                        marker=f"{role}:{action}";
                        if marker not in injections:
                            before = next((x for x in snap.get("children",[]) if x.get("role")==role), {})
                            response=command(control,{"command":action,"role":role}); injections.append(marker)
                            if response.get("accepted") is not True:
                                failures.append({"phase":"injection","role":role,"response":response})
                            else:
                                deadline_recovery=time.time()+min(20, max(5, a.interval))
                                recovered=False; degraded_seen=False
                                while time.time()<deadline_recovery:
                                    current=command(control,{"command":"health"}); current=json.loads(current["health"]) if "health" in current else current
                                    if current.get("care_coverage")=="degraded": degraded_seen=True
                                    row=next((x for x in current.get("children",[]) if x.get("role")==role), {})
                                    changed = row.get("pid") != before.get("pid") or row.get("generation") != before.get("generation") or row.get("restarts",0)>before.get("restarts",0)
                                    if action=="fail": changed = degraded_seen and current.get("care_coverage")=="synthetic" and row.get("pid") != before.get("pid")
                                    if changed: recovered=True; break
                                    time.sleep(.1)
                                if not recovered: failures.append({"phase":"recovery","role":role,"action":action})
            except Exception as exc: failures.append({"phase":"health","error_class":type(exc).__name__})
            time.sleep(min(a.interval,max(0,deadline-time.time())))
        try: command(control,{"command":"shutdown"})
        except Exception as exc: failures.append({"phase":"shutdown","error_class":type(exc).__name__})
        proc.wait(timeout=15)
        if godot_proc and godot_proc.poll() is None: godot_proc.terminate(); godot_proc.wait(timeout=10)
    checkout_changed=any(sample.get("checkout_write_detected") for sample in samples)
    network_counts=[sample.get("network",{}).get("owned_count") for sample in samples]
    network_error=any(sample.get("network",{}).get("error") for sample in samples)
    result={"status":"PASS" if not failures and proc.returncode==0 and len(samples)>0 and len(injections)==4 and not checkout_changed and not network_error and all(count==0 for count in network_counts) else "FAIL","started_utc":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime(started)),"ended_utc":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),"duration_seconds":a.duration_seconds,"samples":len(samples),"failures":failures,"injections":injections,"resident_supervisor_observed":resident_observed,"godot_process_observed":godot_resident_observed,"checkout_write_detected":checkout_changed,"network_owned_counts":network_counts,"evidence_ceiling":"E3_TARGET_TESTED","claim_boundary":"resident synthetic engineering soak with controlled failures; not production reliability or safety efficacy"}; a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8"); print(json.dumps(result,sort_keys=True))
if __name__=="__main__": main()
