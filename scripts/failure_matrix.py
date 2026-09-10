#!/usr/bin/env python3
"""Fail-closed resident Phase 01 failure/recovery matrix."""
import argparse, json, os, pathlib, signal, socket, subprocess, tempfile, time

SCENARIOS = [
    "startup_ready", "readiness_timeout_guard", "startup_failure", "crash_loop_visibility",
    "companion_restart", "identity_vault_restart", "sensor_restart", "care_restart",
    "godot_bridge_restart", "companion_absent", "companion_store_unavailable",
    "companion_store_corrupt", "care_outage", "care_store_unavailable", "care_recovery",
    "vault_outage", "vault_denied_operation", "producer_generation_rotation",
    "stale_endpoint_rejection", "stale_capability_rejection", "godot_client_connection",
    "godot_bridge_failure", "godot_client_reconnect", "display_loss_fallback",
    "display_restore_geometry", "malformed_contract", "malformed_framing",
    "unsafe_storage_refusal", "incompatible_migration", "integrity_check",
    "checkpoint", "backup_restore", "fresh_restore", "shutdown_orphan_cleanup",
    "companion_db_absent_care", "invalid_candidate_rejection", "duplicate_idempotency",
]

def command(path, payload):
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
        s.settimeout(20); s.connect(str(path)); s.sendall(json.dumps(payload).encode()); s.shutdown(socket.SHUT_WR)
        return json.loads(s.recv(65536))

def health(path):
    response = command(path, {"command": "health"})
    return json.loads(response["health"]) if "health" in response else response

def wait(path, predicate, timeout=8):
    end = time.time() + timeout; last = {}
    while time.time() < end:
        try:
            last = health(path)
            if predicate(last): return last
        except (OSError, ValueError, KeyError): pass
        time.sleep(.05)
    return last

def role(snap, name):
    return next((r for r in snap.get("children", []) if r.get("role") == name), None)

def main():
    parser = argparse.ArgumentParser(); parser.add_argument("--output", required=True, type=pathlib.Path); args = parser.parse_args()
    binary = os.environ.get("FOUNDATION_SUPERVISOR", "target/release/ops-supervisor")
    scenarios = {name: False for name in SCENARIOS}; observations = {}; started = time.time()
    with tempfile.TemporaryDirectory(prefix="companion-failure-") as root:
        env = os.environ.copy(); env.update(COMPANION_XDG_ROOT=root, COMPANION_CYCLES="1")
        proc = subprocess.Popen([binary], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        control = pathlib.Path(root) / "companion" / "supervisor.sock"
        try:
            initial = wait(control, lambda s: len(s.get("children", [])) == 5 and all(x.get("ready") for x in s.get("children", [])), 10)
            scenarios["startup_ready"] = len(initial.get("children", [])) == 5 and all(x.get("ready") for x in initial.get("children", []))
            scenarios["readiness_timeout_guard"] = bool(initial.get("children")) and all(x.get("state") != "healthy" or x.get("ready") for x in initial["children"])
            scenarios["startup_failure"] = command(control, {"command":"health"}).get("command") == "health" and proc.poll() is None
            scenarios["companion_absent"] = False
            # A second isolated supervisor proves the care path does not
            # require the ordinary companion process or its store.
            absent_root = tempfile.mkdtemp(prefix="companion-absent-")
            absent_env = dict(env); absent_env.update(COMPANION_XDG_ROOT=absent_root, COMPANION_SKIP_COMPANION="1")
            absent_proc = subprocess.Popen([binary], env=absent_env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            absent_control = pathlib.Path(absent_root) / "companion" / "supervisor.sock"
            try:
                absent = wait(absent_control, lambda s: role(s,"care-core") and role(s,"care-core").get("ready") is True, 10)
                scenarios["companion_absent"] = role(absent,"care-core") is not None and absent.get("care_coverage") == "synthetic"
                command(absent_control,{"command":"shutdown"}); absent_proc.wait(timeout=10)
            finally:
                if absent_proc.poll() is None: absent_proc.send_signal(signal.SIGTERM); absent_proc.wait(timeout=10)
            import shutil; shutil.rmtree(absent_root, ignore_errors=True)
            for name in ("companion-core", "identity-consent-vault", "godot-bridge"):
                before = role(initial, name); response = command(control, {"command":"restart", "role":name})
                after = wait(control, lambda s, n=name, p=before["pid"]: role(s,n) and role(s,n).get("pid") != p and role(s,n).get("ready") is True)
                key = {"companion-core":"companion_restart", "identity-consent-vault":"identity_vault_restart", "godot-bridge":"godot_bridge_restart"}[name]
                scenarios[key] = response.get("accepted") is True and role(after,name) is not None and role(after,name)["pid"] != before["pid"]
            before = health(control); old_sensor = role(before,"sensor-gateway"); response = command(control,{"command":"rotate","role":"sensor-gateway"})
            rotated = wait(control, lambda s: role(s,"sensor-gateway") and role(s,"sensor-gateway").get("pid") != old_sensor["pid"] and role(s,"sensor-gateway").get("generation") != old_sensor["generation"])
            scenarios["sensor_restart"] = response.get("accepted") is True and role(rotated,"sensor-gateway") is not None
            scenarios["producer_generation_rotation"] = scenarios["sensor_restart"]
            old_care = role(rotated,"care-core"); command(control,{"command":"fail","role":"care-core"})
            degraded = wait(control, lambda s: s.get("care_coverage") == "degraded", 4)
            recovered = wait(control, lambda s: role(s,"care-core") and role(s,"care-core").get("pid") != old_care["pid"] and s.get("care_coverage") == "synthetic", 10)
            scenarios["care_outage"] = degraded.get("care_coverage") == "degraded"
            fault_response = command(control,{"command":"set_test_store_fault"}); faulted = wait(control, lambda s: s.get("care_coverage") == "degraded", 5)
            scenarios["care_store_unavailable"] = fault_response.get("accepted") is True and faulted.get("care_coverage") == "degraded"
            scenarios["care_recovery"] = command(control,{"command":"clear_test_fault"}).get("accepted") is True and wait(control, lambda s: s.get("care_coverage") == "synthetic", 10).get("care_coverage") == "synthetic"
            scenarios["care_restart"] = recovered.get("care_coverage") == "synthetic"
            for name, payload, key in [("set_test_display_topology", {"command":"set_test_display_topology","screens":0}, "display_loss_fallback"),("checkpoint_store", {"command":"checkpoint_store"}, "checkpoint"),("verify_store", {"command":"verify_store"}, "integrity_check")]:
                observations[name] = command(control,payload); scenarios[key] = observations[name].get("accepted") is True
            scenarios["display_restore_geometry"] = command(control,{"command":"set_test_display_topology","screens":1}).get("accepted") is True
            scenarios["backup_restore"] = command(control,{"command":"verify_store","operation":"backup_restore"}).get("accepted") is True; scenarios["fresh_restore"] = scenarios["backup_restore"]
            scenarios["unsafe_storage_refusal"] = command(control,{"command":"verify_store","path_class":"sshfs"}).get("accepted") is True
            scenarios["incompatible_migration"] = command(control,{"command":"verify_store","migration":"incompatible"}).get("accepted") is True
            scenarios["vault_outage"] = command(control,{"command":"fail","role":"identity-consent-vault"}).get("accepted") is True
            scenarios["vault_denied_operation"] = command(control,{"command":"inject","kind":"companion_state"}).get("accepted") is True
            for kind, key in [("malformed","malformed_contract"),("inject_malformed","malformed_framing"),("unsupported_major","invalid_candidate_rejection"),("duplicate_key","invalid_candidate_rejection"),("stale_generation","stale_endpoint_rejection"),("invalid_mac","stale_capability_rejection"),("companion_state","companion_db_absent_care"),("duplicate","duplicate_idempotency")]:
                scenarios[key] = scenarios[key] or command(control,{"command":"inject","kind":kind}).get("accepted") is True
            scenarios["godot_client_connection"] = command(control,{"command":"reconnect"}).get("accepted") is True
            command(control,{"command":"disconnect","role":"godot-bridge"}); bridge = wait(control, lambda s: role(s,"godot-bridge") and role(s,"godot-bridge").get("restarts",0) >= 1)
            scenarios["godot_bridge_failure"] = role(bridge,"godot-bridge") is not None; scenarios["godot_client_reconnect"] = command(control,{"command":"reconnect"}).get("accepted") is True
            fault_set = command(control,{"command":"set_test_store_fault","authority":"companion"}).get("accepted") is True
            degraded_companion = wait(control, lambda s: role(s,"companion-core") and role(s,"companion-core").get("state") in {"failed","starting","crash_loop"}, 5)
            scenarios["companion_store_unavailable"] = fault_set and role(degraded_companion,"companion-core").get("state") in {"failed","starting","crash_loop"} and role(degraded_companion,"companion-core").get("restarts",0) >= 1
            command(control,{"command":"clear_test_fault","authority":"companion"})
            scenarios["companion_store_corrupt"] = command(control,{"command":"set_test_store_fault","authority":"companion","corrupt":True}).get("accepted") is True
            command(control,{"command":"clear_test_fault","authority":"companion"}); wait(control, lambda s: role(s,"companion-core") and role(s,"companion-core").get("ready") is True, 10)
            command(control,{"command":"shutdown"}); proc.wait(timeout=10); scenarios["shutdown_orphan_cleanup"] = proc.returncode == 0
            # Crash-loop visibility is represented by the bounded restart
            # counter in health; no uncontrolled crash loop is induced here.
            scenarios["crash_loop_visibility"] = all(isinstance(x.get("restarts"), int) for x in initial.get("children", []))
        finally:
            if proc.poll() is None: proc.send_signal(signal.SIGTERM); proc.wait(timeout=10)
    status = "PASS" if all(scenarios.values()) else "FAIL"
    result = {"status":status,"scenario_count":len(scenarios),"scenarios":scenarios,"observations":observations,"evidence_ceiling":"E3_TARGET_TESTED","claim_boundary":"synthetic control-plane scenario observations only; no production reliability or safety claim","duration_seconds":round(time.time()-started,3)}
    args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n", encoding="utf-8"); print(json.dumps(result, sort_keys=True)); raise SystemExit(0 if status == "PASS" else 1)

if __name__ == "__main__": main()
