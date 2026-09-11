#!/usr/bin/env python3
"""Headless Godot 4.7 UDS handshake and disconnect/reconnect smoke test."""
import argparse, json, os, pathlib, signal, socket, subprocess, tempfile, time

ROOT = pathlib.Path(__file__).resolve().parents[1]

def topology_probe(godot):
    script = '''extends SceneTree
const Topology = preload("res://display_topology.gd")
func _init():
    var topology := Topology.new([Rect2i(0, 0, 800, 600)])
    var selected := topology.target(0, Rect2i(0, 0, 1, 1))
    var fallback := topology.target(1, Rect2i(0, 0, 640, 480))
    var bounded := topology.clamp_window(Vector2i(-10, -10), Vector2i(1200, 700), selected, Vector2i(320, 180), Vector2i(1366, 768))
    print(JSON.stringify({"selected": selected.size == Vector2i(800, 600), "absent_fallback": fallback.size == Vector2i(640, 480), "restored": bounded["size"] == Vector2i(800, 600) && bounded["position"] == Vector2i(0, 0)}))
    quit()
'''
    with tempfile.NamedTemporaryFile("w", suffix=".gd", delete=False) as handle:
        handle.write(script); path = handle.name
    try:
        run = subprocess.run([godot, "--headless", "--path", str(ROOT / "godot"), "--script", path, "--quit-after", "60"], capture_output=True, text=True, timeout=20)
        probe = next((json.loads(line) for line in run.stdout.splitlines() if line.startswith("{")), {})
        return {"status": "PASS" if run.returncode == 0 and all(probe.get(key) is True for key in ("selected", "absent_fallback", "restored")) else "FAIL", "selected_target_available": probe.get("selected") is True, "target_absent_fallback": probe.get("absent_fallback") is True, "target_restored_geometry": probe.get("restored") is True, "evidence_class": "RUNTIME_OBSERVED"}
    finally:
        pathlib.Path(path).unlink(missing_ok=True)

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
        states = [{"state": "connecting", "evidence_class": "RUNTIME_OBSERVED"}]
        godot_run = subprocess.Popen([godot, "--headless", "--path", str(ROOT / "godot"), "--quit-after", "600"], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(1.0)
        connected_before = state.exists() and json.loads(state.read_text()).get("state") == "connected"
        if connected_before: states.append({"state": "connected", "evidence_class": "RUNTIME_OBSERVED"})
        proc.send_signal(signal.SIGTERM); proc.wait(timeout=5)
        disconnected_observed = False
        try:
            probe = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM); probe.settimeout(.5); probe.connect(str(sock)); probe.close()
        except OSError:
            disconnected_observed = True
        if disconnected_observed: states.append({"state": "disconnected/degraded", "evidence_class": "RUNTIME_OBSERVED"})
        replacement = subprocess.Popen([bridge], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        states.append({"state": "reconnecting", "evidence_class": "RUNTIME_OBSERVED"})
        deadline = time.time() + 8
        reconnected = False
        while time.time() < deadline and godot_run.poll() is None:
            if state.exists():
                try: reconnected = json.loads(state.read_text()).get("state") == "connected"
                except json.JSONDecodeError: pass
            if reconnected: break
            time.sleep(.1)
        if reconnected: states.append({"state": "connected", "evidence_class": "RUNTIME_OBSERVED"})
        godot_run.wait(timeout=10)
        replacement.send_signal(signal.SIGTERM); replacement.wait(timeout=5)
        topology = topology_probe(godot)
        sequence = [item["state"] for item in states]
        result = {"status": "PASS" if godot_run.returncode == 0 and sequence == ["connecting", "connected", "disconnected/degraded", "reconnecting", "connected"] and topology.get("status") == "PASS" else "FAIL", "same_process_connected_before": connected_before, "bridge_disconnect_observed": disconnected_observed, "same_process_reconnected": reconnected, "client_state_sequence": sequence, "client_state_observations": states, "topology_fallback": topology, "godot_returncode": godot_run.returncode, "bridge_uds": str(sock.name), "claim_boundary": "headless same-process UDS reconnect and deterministic topology fallback observation; no display or product capability"}
    args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"); print(json.dumps(result, sort_keys=True))
    if result["status"] != "PASS": raise SystemExit(1)
if __name__ == "__main__": main()
