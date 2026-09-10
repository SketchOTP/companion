#!/usr/bin/env python3
"""Operator-facing read-only health query."""
import argparse, json, os, pathlib, socket, time

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--json",action="store_true"); args=ap.parse_args()
    override = os.environ.get("COMPANION_XDG_ROOT")
    root = pathlib.Path(override) / "companion" if override else pathlib.Path(os.environ.get("XDG_RUNTIME_DIR", "")) / "companion"
    sock_path = root / "supervisor.sock"
    state={"version":"companion-foundation/0.1.0","timestamp_utc":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),"network_default":"deny","privacy_class":"PUBLIC_METADATA","supervisor":"not_running","children":[]}
    try:
        s=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM); s.settimeout(1); s.connect(str(sock_path)); state.update(json.loads(s.recv(65536))); s.close()
    except OSError as exc: state.update({"supervisor":"unavailable","known_degradation":"supervisor control socket unavailable","error_class":type(exc).__name__})
    print(json.dumps(state,indent=2,sort_keys=True) if args.json else f"foundation supervisor: {state.get('status', state['supervisor'])}")
if __name__=="__main__": main()
