#!/usr/bin/env python3
"""Fail-closed runtime identity check for the exact SQLite build."""
import argparse, json, os, pathlib, socket, subprocess, tempfile, time, signal

EXPECTED_VERSION = "3.53.4"
EXPECTED_SOURCE_ID = "2026-07-24 19:02:57 bf7c7f30031888f4e796e429ab3978879485813aaca6f641c7b33e4e09459bcc"

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--output",type=pathlib.Path,required=True); args=ap.parse_args()
    source=os.environ.get("COMPANION_SQLITE_SOURCE")
    if not source or not pathlib.Path(source).is_file(): raise SystemExit("COMPANION_SQLITE_SOURCE is required")
    root=tempfile.mkdtemp(prefix="companion-sqlite-identity-"); env=os.environ.copy(); env["COMPANION_XDG_ROOT"]=root
    binary=env.get("FOUNDATION_SUPERVISOR","target/release/ops-supervisor"); proc=subprocess.Popen([binary],env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); control=pathlib.Path(root)/"companion"/"supervisor.sock"; deadline=time.time()+5
    while time.time()<deadline and not control.exists(): time.sleep(.05)
    try:
        s=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM); s.settimeout(2); s.connect(str(control)); s.sendall(b'{"command":"health"}\n'); s.shutdown(socket.SHUT_WR); response=json.loads(s.recv(65536)); s.close(); health=json.loads(response["health"]); identity=health.get("sqlite",{}); status=identity.get("version")==EXPECTED_VERSION and identity.get("source_id")==EXPECTED_SOURCE_ID and bool(identity.get("compile_options"))
    finally:
        if proc.poll() is None:
            try:
                s=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM); s.connect(str(control)); s.sendall(b'{"command":"shutdown"}\n'); s.shutdown(socket.SHUT_WR); s.close()
            except OSError: proc.send_signal(signal.SIGTERM)
        proc.wait(timeout=10)
    result={"status":"PASS" if status and proc.returncode==0 else "FAIL","runtime_identity":identity,"source_sha256":__import__("hashlib").sha256(pathlib.Path(source).read_bytes()).hexdigest(),"claim_boundary":"exact SQLite runtime identity only; no release or lifetime reliability claim"}; args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8"); print(json.dumps(result,sort_keys=True))
    if result["status"]!="PASS": raise SystemExit(1)
if __name__=="__main__": main()
