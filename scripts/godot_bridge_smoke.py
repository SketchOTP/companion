#!/usr/bin/env python3
"""Headless Godot 4.7 UDS handshake and disconnect/reconnect smoke test."""
import argparse, json, os, pathlib, signal, socket, subprocess, tempfile, time

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
        godot_run = subprocess.Popen([godot, "--headless", "--path", "godot", "--quit-after", "600"], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(1.0)
        connected_before = state.exists() and json.loads(state.read_text()).get("state") == "connected"
        proc.send_signal(signal.SIGTERM); proc.wait(timeout=5)
        disconnected_observed = False
        try:
            probe = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM); probe.settimeout(.5); probe.connect(str(sock)); probe.close()
        except OSError:
            disconnected_observed = True
        replacement = subprocess.Popen([bridge], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        deadline = time.time() + 8
        reconnected = False
        while time.time() < deadline and godot_run.poll() is None:
            if state.exists():
                try: reconnected = json.loads(state.read_text()).get("state") == "connected"
                except json.JSONDecodeError: pass
            if reconnected: break
            time.sleep(.1)
        godot_run.wait(timeout=10)
        replacement.send_signal(signal.SIGTERM); replacement.wait(timeout=5)
        result = {"status": "PASS" if godot_run.returncode == 0 and connected_before and disconnected_observed and reconnected else "FAIL", "same_process_connected_before": connected_before, "bridge_disconnect_observed": disconnected_observed, "same_process_reconnected": reconnected, "godot_returncode": godot_run.returncode, "bridge_uds": str(sock.name), "claim_boundary": "headless same-process UDS reconnect observation; no display or product capability"}
    args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"); print(json.dumps(result, sort_keys=True))
    if result["status"] != "PASS": raise SystemExit(1)
if __name__ == "__main__": main()
