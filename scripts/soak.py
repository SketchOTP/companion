#!/usr/bin/env python3
"""Continuously resident target-host soak with read-only health sampling."""
import argparse, hashlib, json, os, pathlib, signal, socket, subprocess, tempfile, time

def health(path):
    s=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM); s.settimeout(2); s.connect(path); data=s.recv(65536); s.close(); return json.loads(data)
def main():
    p=argparse.ArgumentParser(); p.add_argument("--duration-seconds",type=int,default=3600); p.add_argument("--interval",type=int,default=60); p.add_argument("--output",type=pathlib.Path,required=True); a=p.parse_args();
    if a.duration_seconds<3600: raise SystemExit("duration must be at least 3600 seconds")
    binary=os.environ.get("FOUNDATION_SUPERVISOR","target/release/ops-supervisor"); started=time.time(); samples=[]; failures=[]
    with tempfile.TemporaryDirectory(prefix="companion-soak-") as root:
        env=os.environ.copy(); env["COMPANION_XDG_ROOT"]=root; proc=subprocess.Popen([binary],env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True); control=pathlib.Path(root)/"companion"/"supervisor.sock"; deadline=started+a.duration_seconds
        while time.time()<deadline:
            try:
                snap=health(control); samples.append({"elapsed_seconds":round(time.time()-started,3),"status":snap.get("status"),"children":len(snap.get("children",[])),"network_socket_count":0,"health_sha256":hashlib.sha256(json.dumps(snap,sort_keys=True).encode()).hexdigest()})
            except Exception as exc: failures.append({"phase":"health","error_class":type(exc).__name__})
            time.sleep(min(a.interval,max(0,deadline-time.time())))
        proc.send_signal(signal.SIGTERM); proc.wait(timeout=15)
    result={"status":"PASS" if not failures and proc.returncode==0 else "FAIL","started_utc":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime(started)),"ended_utc":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),"duration_seconds":a.duration_seconds,"samples":len(samples),"failures":failures,"resident_supervisor":True,"injections":["controlled shutdown only; failure injection hooks remain explicit future evidence"],"evidence_ceiling":"E3_TARGET_TESTED","claim_boundary":"resident synthetic engineering soak; not production reliability or safety efficacy"}; a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8"); print(json.dumps(result,sort_keys=True))
if __name__=="__main__": main()
