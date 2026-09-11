#!/usr/bin/env python3
"""Focused resident regression for the corrected Phase 01 semantics."""
import argparse, json, os, pathlib, signal, socket, sqlite3, subprocess, tempfile, time

ROOT = pathlib.Path(__file__).resolve().parents[1]

def command(path, payload):
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
        sock.settimeout(8)
        sock.connect(str(path))
        sock.sendall((json.dumps(payload, separators=(",", ":")) + "\n").encode())
        sock.shutdown(socket.SHUT_WR)
        response = json.loads(sock.recv(65536))
    return json.loads(response["health"]) if "health" in response else response

def role(snapshot, name):
    return next((item for item in snapshot.get("children", []) if item.get("role") == name), None)

def health(path):
    return command(path, {"command": "health"})

def wait_for(path, predicate, timeout=12):
    deadline = time.time() + timeout
    last = {}
    while time.time() < deadline:
        try:
            last = health(path)
            if predicate(last):
                return last
        except (OSError, ValueError, KeyError, TypeError):
            pass
        time.sleep(0.05)
    return last

def db_counts(path):
    with sqlite3.connect(path, timeout=2) as conn:
        return {
            "attempts": conn.execute("select count(*) from safety_attempts").fetchone()[0],
            "receipts": conn.execute("select count(*) from safety_receipts").fetchone()[0],
        }

def last_reason(path):
    with sqlite3.connect(path, timeout=2) as conn:
        return conn.execute("select reason from safety_attempts order by id desc limit 1").fetchone()[0]

def wait_attempt(path, minimum, timeout=8):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            if db_counts(path)["attempts"] >= minimum:
                return db_counts(path)
        except sqlite3.Error:
            pass
        time.sleep(0.05)
    return db_counts(path)

def process_alive(pid):
    try:
        os.kill(int(pid), 0)
        return True
    except (OSError, TypeError, ValueError):
        return False

def network_owned(pids):
    try:
        result = subprocess.run(["ss", "-H", "-tunp"], capture_output=True, text=True, check=False)
    except OSError as exc:
        return None, type(exc).__name__
    if result.returncode != 0:
        return None, f"ss_exit_{result.returncode}"
    pidset = {str(int(pid)) for pid in pids if pid}
    return sum(any(f"pid={pid}," in line or f"pid={pid})" in line for pid in pidset) for line in result.stdout.splitlines()), None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration-seconds", type=int, default=900)
    parser.add_argument("--output", type=pathlib.Path, required=True)
    args = parser.parse_args()
    if args.duration_seconds < 900:
        raise SystemExit("duration must be at least 900 seconds")
    binary = os.environ.get("FOUNDATION_SUPERVISOR", str(ROOT / "target/release/ops-supervisor"))
    started = time.time()
    observations = {"invalid_rejected": False, "valid_accepted": False, "duplicate_after_care_restart": False, "producer_rotated": False, "stale_rejected": False, "store_fault_degraded": False, "store_fault_blocked": False, "store_recovered": False, "bridge_restarted": False}
    failures = []
    samples = []
    baseline_status = subprocess.run(["git", "status", "--porcelain=v1", "--untracked-files=all"], cwd=ROOT, capture_output=True, text=True, check=True).stdout
    proc = None
    children_at_start = []
    try:
        with tempfile.TemporaryDirectory(prefix="companion-regression-") as root:
            env = {**os.environ, "COMPANION_XDG_ROOT": root, "COMPANION_CYCLES": "1"}
            proc = subprocess.Popen([binary], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            control = pathlib.Path(root) / "companion" / "supervisor.sock"
            care_db = pathlib.Path(root) / "companion" / "care.sqlite3"
            snap = wait_for(control, lambda value: len(value.get("children", [])) == 5 and all(item.get("ready") for item in value.get("children", [])), 15)
            if len(snap.get("children", [])) != 5:
                failures.append("startup_readiness")
            children_at_start = [item.get("pid") for item in snap.get("children", []) if item.get("pid")]
            deadline = started + args.duration_seconds
            actions = {}
            while time.time() < deadline:
                elapsed = time.time() - started
                try:
                    snap = health(control)
                    pids = [item.get("pid") for item in snap.get("children", []) if item.get("pid")]
                    owned, error = network_owned([proc.pid] + pids)
                    status = subprocess.run(["git", "status", "--porcelain=v1", "--untracked-files=all"], cwd=ROOT, capture_output=True, text=True, check=True).stdout
                    samples.append({"elapsed_seconds": round(elapsed, 2), "care_coverage": snap.get("care_coverage"), "children": len(pids), "network_owned": owned, "network_error": error, "checkout_unchanged": status == baseline_status})
                    care = db_counts(care_db)
                    if elapsed >= 30 and "invalid" not in actions:
                        before = care["attempts"]
                        response = command(control, {"command": "inject", "kind": "unknown_field", "request_id": "regression-invalid"})
                        after = wait_attempt(care_db, before + 1)
                        observations["invalid_rejected"] = response.get("accepted") is True and last_reason(care_db) == "unknown_field" and after["attempts"] == before + 1 and role(health(control), "care-core") is not None
                        actions["invalid"] = True
                    if elapsed >= 60 and "valid" not in actions:
                        before = db_counts(care_db)
                        response = command(control, {"command": "inject", "kind": "valid_safety_candidate", "request_id": "regression-valid"})
                        after = wait_attempt(care_db, before["attempts"] + 1)
                        observations["valid_accepted"] = response.get("accepted") is True and after["receipts"] == before["receipts"] + 1 and last_reason(care_db) == "accepted"
                        actions["valid"] = True
                    if elapsed >= 120 and "care_restart" not in actions:
                        old = role(snap, "care-core")
                        command(control, {"command": "fail", "role": "care-core"})
                        degraded = wait_for(control, lambda value: value.get("care_coverage") == "degraded", 5)
                        replacement = wait_for(control, lambda value: role(value, "care-core") and role(value, "care-core").get("pid") != old.get("pid") and value.get("care_coverage") == "synthetic", 15)
                        before = db_counts(care_db)
                        duplicate = command(control, {"command": "inject", "kind": "duplicate_safety_candidate", "request_id": "regression-valid"})
                        after = wait_attempt(care_db, before["attempts"] + 1)
                        observations["duplicate_after_care_restart"] = degraded.get("care_coverage") == "degraded" and replacement.get("care_coverage") == "synthetic" and duplicate.get("accepted") is True and after["attempts"] == before["attempts"] + 1 and last_reason(care_db) == "duplicate"
                        actions["care_restart"] = True
                    if elapsed >= 240 and "rotate" not in actions:
                        old = role(snap, "sensor-gateway")
                        command(control, {"command": "rotate", "role": "sensor-gateway"})
                        replacement = wait_for(control, lambda value: role(value, "sensor-gateway") and role(value, "sensor-gateway").get("pid") != old.get("pid") and role(value, "sensor-gateway").get("generation") != old.get("generation"), 15)
                        observations["producer_rotated"] = role(replacement, "sensor-gateway") is not None
                        actions["rotate"] = True
                    if elapsed >= 300 and "stale" not in actions:
                        before = db_counts(care_db)
                        command(control, {"command": "inject", "kind": "stale_generation", "request_id": "regression-stale"})
                        after = wait_attempt(care_db, before["attempts"] + 1)
                        observations["stale_rejected"] = after["attempts"] == before["attempts"] + 1 and last_reason(care_db) == "stale_generation"
                        actions["stale"] = True
                    if elapsed >= 360 and "fault" not in actions:
                        before = db_counts(care_db)
                        command(control, {"command": "set_test_store_fault", "authority": "care"})
                        degraded = wait_for(control, lambda value: value.get("care_coverage") == "degraded", 8)
                        command(control, {"command": "inject", "kind": "valid_safety_candidate", "request_id": "regression-fault"})
                        time.sleep(0.5)
                        during = db_counts(care_db)
                        command(control, {"command": "clear_test_fault", "authority": "care"})
                        restored = wait_for(control, lambda value: value.get("care_coverage") == "synthetic", 15)
                        observations["store_fault_degraded"] = degraded.get("care_coverage") == "degraded"
                        observations["store_fault_blocked"] = during == before
                        observations["store_recovered"] = restored.get("care_coverage") == "synthetic"
                        actions["fault"] = True
                    if elapsed >= 480 and "bridge" not in actions:
                        old = role(snap, "godot-bridge")
                        response = command(control, {"command": "restart", "role": "godot-bridge"})
                        replacement = wait_for(control, lambda value: role(value, "godot-bridge") and role(value, "godot-bridge").get("pid") != old.get("pid") and role(value, "godot-bridge").get("ready"), 15)
                        observations["bridge_restarted"] = response.get("accepted") is True and role(replacement, "godot-bridge") is not None
                        actions["bridge"] = True
                except Exception as exc:
                    failures.append(type(exc).__name__)
                time.sleep(min(5, max(0, deadline - time.time())))
            try:
                shutdown = command(control, {"command": "shutdown"})
                proc.wait(timeout=15)
            except Exception as exc:
                failures.append(f"shutdown:{type(exc).__name__}")
                shutdown = {}
            final_status = subprocess.run(["git", "status", "--porcelain=v1", "--untracked-files=all"], cwd=ROOT, capture_output=True, text=True, check=True).stdout
            owned_after, network_error_after = network_owned([proc.pid] + children_at_start)
            observations["clean_shutdown"] = shutdown.get("accepted") is True and proc.returncode == 0 and all(not process_alive(pid) for pid in children_at_start)
            observations["checkout_unchanged"] = final_status == baseline_status and all(sample["checkout_unchanged"] for sample in samples)
            observations["network_census_complete"] = all(sample["network_error"] is None for sample in samples) and network_error_after is None and owned_after == 0
    except Exception as exc:
        failures.append(type(exc).__name__)
    finally:
        if proc is not None and proc.poll() is None:
            proc.send_signal(signal.SIGTERM)
            proc.wait(timeout=15)
    required = ["invalid_rejected", "valid_accepted", "duplicate_after_care_restart", "producer_rotated", "stale_rejected", "store_fault_degraded", "store_fault_blocked", "store_recovered", "bridge_restarted", "clean_shutdown", "checkout_unchanged", "network_census_complete"]
    result = {"status": "PASS" if not failures and all(observations.get(key) is True for key in required) and len(samples) > 0 else "FAIL", "duration_seconds": args.duration_seconds, "samples": len(samples), "observations": observations, "failures": failures, "evidence_ceiling": "E3_TARGET_TESTED", "claim_boundary": "focused resident synthetic regression; not product reliability, safety efficacy, security certification, or SLA evidence"}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    raise SystemExit(0 if result["status"] == "PASS" else 1)

if __name__ == "__main__":
    main()
