#!/usr/bin/env python3
"""Fail-closed resident lifecycle and no-egress smoke check."""
import argparse, json, os, pathlib, signal, socket, subprocess, tempfile, time

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--output",type=pathlib.Path,required=True); a=ap.parse_args(); binary=os.environ.get("FOUNDATION_SUPERVISOR","target/release/ops-supervisor")
    with tempfile.TemporaryDirectory(prefix="companion-runtime-") as root:
        env=os.environ.copy(); env["COMPANION_XDG_ROOT"]=root; proc=subprocess.Popen([binary],env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True); control=pathlib.Path(root)/"companion"/"supervisor.sock"; deadline=time.time()+5
        while time.time()<deadline and not control.exists(): time.sleep(.05)
        health={}; error=None
        try:
            s=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM); s.settimeout(1); s.connect(str(control)); health=json.loads(s.recv(65536)); s.close()
        except Exception as exc: error=type(exc).__name__
        rows=health.get("children",[]); roles={x.get("role") for x in rows}; expected={"companion-core","identity-consent-vault","godot-bridge","sensor-gateway","care-core"}; resident=proc.poll() is None and expected.issubset(roles); network=0
        for child in rows:
            try:
                for entry in pathlib.Path(f"/proc/{child['pid']}/fd").iterdir():
                    link=os.readlink(entry)
                    if link.startswith("socket:"):
                        inode=link[8:-1];
                        if any(inode in pathlib.Path(f).read_text(errors="ignore") for f in ("/proc/net/tcp","/proc/net/tcp6")): network += 1
            except (OSError, KeyError): pass
        if proc.poll() is None: proc.send_signal(signal.SIGTERM)
        proc.wait(timeout=10); result={"status":"PASS" if resident and network==0 and proc.returncode==0 else "FAIL","resident":resident,"roles":sorted(roles),"health_error":error,"network_socket_count":network,"shutdown_returncode":proc.returncode,"claim_boundary":"engineering lifecycle observation only"}
    a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8"); print(json.dumps(result,sort_keys=True));
    if result["status"]!="PASS": raise SystemExit(1)
if __name__=="__main__": main()
