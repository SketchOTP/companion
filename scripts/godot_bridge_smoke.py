#!/usr/bin/env python3
"""Headless Godot 4.7 UDS handshake and disconnect/reconnect smoke test."""
import argparse, json, os, pathlib, signal, subprocess, tempfile, time

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--output", type=pathlib.Path, required=True); args = ap.parse_args()
    bridge = os.environ.get("FOUNDATION_BRIDGE", "target/release/godot-bridge")
    godot = os.environ.get("GODOT_BIN", "")
    if not godot:
        raise SystemExit("GODOT_BIN must identify the verified official Godot 4.7.2 binary")
    with tempfile.TemporaryDirectory(prefix="companion-godot-bridge-") as root:
        env = os.environ.copy(); env["COMPANION_XDG_ROOT"] = root
        proc = subprocess.Popen([bridge], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        runtime = pathlib.Path(root) / "companion"; sock = runtime / "godot-bridge.sock"; state = runtime / "bridge-state.json"
        deadline = time.time() + 5
        while time.time() < deadline and not sock.exists(): time.sleep(.05)
        if not sock.exists():
            proc.kill(); raise SystemExit("bridge socket did not appear")
        godot_run = subprocess.run([godot, "--headless", "--path", "godot", "--quit-after", "1"], env=env, capture_output=True, text=True, timeout=10)
        connected = state.exists() and json.loads(state.read_text()).get("state") == "connected"
        proc.send_signal(signal.SIGTERM); proc.wait(timeout=5)
        disconnected_run = subprocess.run([godot, "--headless", "--path", "godot", "--quit-after", "1"], env=env, capture_output=True, text=True, timeout=10)
        result = {"status": "PASS" if godot_run.returncode == 0 and connected and disconnected_run.returncode == 0 else "FAIL", "connected_state_observed": connected, "godot_connected_returncode": godot_run.returncode, "godot_after_bridge_stop_returncode": disconnected_run.returncode, "bridge_uds": str(sock.name), "claim_boundary": "headless UDS protocol and degraded disconnect observation; no display or product capability"}
    args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"); print(json.dumps(result, sort_keys=True))
    if result["status"] != "PASS": raise SystemExit(1)
if __name__ == "__main__": main()
