#!/usr/bin/env python3
"""Fail-closed resident injection and authority-separation matrix."""
import argparse, json, os, pathlib, signal, socket, sqlite3, subprocess, tempfile, time

ROOT = pathlib.Path(__file__).resolve().parents[1]
KINDS = [
    ("valid_safety_candidate", "direct-care", "accepted", "accepted", 1, 1),
    ("duplicate_safety_candidate", "direct-care", "duplicate", "duplicate", 1, 0),
    ("replay_safety_candidate", "direct-care", "rejected", "replay_rejected", 1, 0),
    ("malformed_frame", "direct-care", "rejected", "malformed_frame", 1, 0),
    ("duplicate_decoded_key", "direct-care", "rejected", "duplicate_decoded_key", 1, 0),
    ("unsupported_schema_major", "direct-care", "rejected", "unsupported_schema_major", 1, 0),
    ("unknown_field", "direct-care", "rejected", "unknown_field", 1, 0),
    ("invalid_uuid", "direct-care", "rejected", "invalid_uuid", 1, 0),
    ("invalid_datetime", "direct-care", "rejected", "invalid_datetime", 1, 0),
    ("stale_generation", "direct-care", "rejected", "stale_generation", 1, 0),
    ("invalid_mac", "direct-care", "rejected", "invalid_mac", 1, 0),
    ("stale_mac", "direct-care", "rejected", "stale_mac", 1, 0),
    ("unauthorized_sender", "direct-care", "rejected", "unauthorized_sender", 1, 0),
    ("forbidden_companion_state", "direct-care", "rejected", "forbidden_companion_state", 1, 0),
    ("valid_ordinary_observation", "ordinary", "accepted", "ordinary_observation", 0, 0),
]
EXPECTATIONS = {n: {"category": n, "transport_path": p, "expected_status": s, "expected_reason": r, "care_attempt_delta": a, "care_outcome_delta": o, "companion_event_delta": int(p == "ordinary")} for n, p, s, r, a, o in KINDS}

def command(path, payload):
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
        s.settimeout(5); s.connect(str(path)); s.sendall((json.dumps(payload, separators=(",", ":")) + "\n").encode()); s.shutdown(socket.SHUT_WR); return json.loads(s.recv(65536))

def health(path):
    v = command(path, {"command": "health"}); return json.loads(v["health"]) if "health" in v else v

def wait_for(path, predicate, timeout=10):
    deadline = time.time() + timeout; last = {}
    while time.time() < deadline:
        try:
            last = health(path)
            if predicate(last): return last
        except (OSError, ValueError, KeyError, TypeError): pass
        time.sleep(.05)
    return last

def role(snap, name): return next((x for x in snap.get("children", []) if x.get("role") == name), None)

def db_counts(path):
    try:
        with sqlite3.connect(path, timeout=2) as c:
            return {"attempts": c.execute("SELECT count(*) FROM safety_attempts").fetchone()[0], "receipts": c.execute("SELECT count(*) FROM safety_receipts").fetchone()[0]}
    except sqlite3.Error: return {"attempts": 0, "receipts": 0}

def event_count(path):
    try:
        with sqlite3.connect(path, timeout=2) as c: return c.execute("SELECT count(*) FROM event_log WHERE event_type='ordinary_observation'").fetchone()[0]
    except sqlite3.Error: return 0

def wait_increase(fn, old, timeout=5):
    deadline = time.time() + timeout
    while time.time() < deadline:
        value = fn()
        if value > old: return value
        time.sleep(.02)
    return fn()

def wait_absent(path, timeout=5):
    deadline = time.time() + timeout
    while time.time() < deadline:
        if not path.exists(): return True
        time.sleep(.02)
    return not path.exists()

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--output", required=True, type=pathlib.Path); ap.add_argument("--cycles", type=int, default=3000); ap.add_argument("--seeds", default="17,23,41"); args = ap.parse_args()
    if args.cycles < 3000 or args.cycles % 3: raise SystemExit("cycles must be >=3000 and divisible by 3")
    seeds = [int(x) for x in args.seeds.split(",") if x]; binary = os.environ.get("FOUNDATION_SUPERVISOR", str(ROOT / "target/release/ops-supervisor")); started = time.time()
    categories = {k: dict(EXPECTATIONS[k], requested=0, applied=0, accepted=0, rejected=0, duplicate=0, reasons={}, care_attempt_delta=0, care_outcome_delta=0, companion_event_delta=0) for k in EXPECTATIONS}; lifecycle = {}
    with tempfile.TemporaryDirectory(prefix="companion-closeout-") as root:
        env = os.environ.copy(); env.update(COMPANION_XDG_ROOT=root, COMPANION_CYCLES="1", COMPANION_SEEDS=','.join(map(str, seeds))); proc = subprocess.Popen([binary], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        control = pathlib.Path(root) / "companion" / "supervisor.sock"; care_db = pathlib.Path(root) / "companion" / "care.sqlite3"; companion_db = pathlib.Path(root) / "companion" / "companion.sqlite3"; ordinary_marker = pathlib.Path(root) / "companion" / "ordinary-observation.json"
        try:
            snap = wait_for(control, lambda s: len(s.get("children", [])) == 5 and all(x.get("ready") for x in s.get("children", [])), 12); lifecycle["startup_ready"] = len(snap.get("children", [])) == 5 and all(x.get("ready") for x in snap.get("children", []))
            if not lifecycle["startup_ready"]: raise RuntimeError("roles not ready")
            time.sleep(.2); baseline = db_counts(care_db); event_baseline = event_count(companion_db)
            unknown = command(control, {"command":"inject", "kind":"not_a_real_injection", "request_id":"unknown"}); lifecycle["unknown_kind_rejected_before_transport"] = unknown.get("accepted") is False and unknown.get("reason") == "unknown_injection_kind"
            per_seed = args.cycles // len(seeds); order = list(EXPECTATIONS)
            for i in range(args.cycles):
                seed = seeds[i // per_seed]; kind = order[(i + seed) % len(order)]; categories[kind]["requested"] += 1; before = db_counts(care_db); before_events = event_count(companion_db)
                response = command(control, {"command":"inject", "kind":kind, "request_id":f"seed-{seed}-{i}"}); categories[kind]["applied"] += 1
                if response.get("normalized_kind") != kind or response.get("accepted") is not True: raise RuntimeError(f"typed injection mismatch {kind}: {response}")
                if kind == "valid_ordinary_observation":
                    after_events = wait_increase(lambda: event_count(companion_db), before_events); consumed = wait_absent(ordinary_marker); after = db_counts(care_db); status, reason = ("accepted", "ordinary_observation") if after_events == before_events + 1 and consumed else ("rejected", "ordinary_observation"); categories[kind]["companion_event_delta"] += after_events - before_events
                else:
                    wait_increase(lambda: db_counts(care_db)["attempts"], before["attempts"]); after = db_counts(care_db); reason = next(iter(sqlite3.connect(care_db).execute("SELECT reason FROM safety_attempts ORDER BY id DESC LIMIT 1")), (None,))[0]; status = "duplicate" if reason == "duplicate" else ("accepted" if reason == "accepted" else "rejected"); categories[kind]["care_attempt_delta"] += after["attempts"] - before["attempts"]; categories[kind]["care_outcome_delta"] += after["receipts"] - before["receipts"]
                categories[kind][status] += 1; categories[kind]["reasons"][reason] = categories[kind]["reasons"].get(reason, 0) + 1
                if status != EXPECTATIONS[kind]["expected_status"] or reason != EXPECTATIONS[kind]["expected_reason"]: raise RuntimeError(f"outcome mismatch {kind}: {status}/{reason}")
            lifecycle["mixed_messages"] = sum(v["requested"] for v in categories.values()) == args.cycles; invalid = [k for k, v in EXPECTATIONS.items() if v["expected_status"] == "rejected"]; lifecycle["invalid_accepted_zero"] = sum(categories[k]["accepted"] for k in invalid) == 0; lifecycle["ordinary_separated"] = categories["valid_ordinary_observation"]["care_attempt_delta"] == 0 and categories["valid_ordinary_observation"]["care_outcome_delta"] == 0 and event_count(companion_db) > event_baseline; lifecycle["care_alive_after_hostile"] = bool(role(health(control), "care-core") and role(health(control), "care-core").get("ready"))
            old_care = role(health(control), "care-core"); command(control, {"command":"fail", "role":"care-core"}); degraded = wait_for(control, lambda s: s.get("care_coverage") == "degraded", 5); recovered = wait_for(control, lambda s: role(s,"care-core") and role(s,"care-core").get("pid") != old_care["pid"] and s.get("care_coverage") == "synthetic", 12); lifecycle["care_degraded_recovered"] = degraded.get("care_coverage") == "degraded" and recovered.get("care_coverage") == "synthetic"
            before = db_counts(care_db); command(control, {"command":"inject", "kind":"duplicate_safety_candidate", "request_id":"restart-duplicate"}); wait_increase(lambda: db_counts(care_db)["attempts"], before["attempts"]); lifecycle["persistent_idempotency"] = db_counts(care_db)["attempts"] == before["attempts"] + 1 and next(iter(sqlite3.connect(care_db).execute("SELECT reason FROM safety_attempts ORDER BY id DESC LIMIT 1")), (None,))[0] == "duplicate"
            old_sensor = role(recovered, "sensor-gateway"); command(control, {"command":"rotate", "role":"sensor-gateway"}); rotated = wait_for(control, lambda s: role(s,"sensor-gateway") and role(s,"sensor-gateway").get("pid") != old_sensor["pid"] and role(s,"sensor-gateway").get("generation") != old_sensor["generation"], 12); lifecycle["producer_rotation"] = bool(role(rotated, "sensor-gateway"))
            fault = command(control, {"command":"set_test_store_fault", "authority":"care"}); lifecycle["care_store_fault_degraded"] = fault.get("accepted") is True and wait_for(control, lambda s: s.get("care_coverage") == "degraded", 5).get("care_coverage") == "degraded"; command(control, {"command":"clear_test_fault", "authority":"care"}); lifecycle["care_store_recovered"] = wait_for(control, lambda s: s.get("care_coverage") == "synthetic", 12).get("care_coverage") == "synthetic"; command(control, {"command":"shutdown"}); proc.wait(timeout=12); lifecycle["clean_shutdown"] = proc.returncode == 0
        finally:
            if proc.poll() is None: proc.send_signal(signal.SIGTERM); proc.wait(timeout=12)
    requested_total = sum(v["requested"] for v in categories.values())
    accepted = sum(v["accepted"] for v in categories.values())
    rejected = sum(v["rejected"] for v in categories.values())
    duplicate = sum(v["duplicate"] for v in categories.values())
    invalid_accepted = sum(v["accepted"] for name, v in categories.items() if EXPECTATIONS[name]["expected_status"] == "rejected")
    equations = {"requested_total": requested_total, "observed_total": accepted + rejected + duplicate, "accepted": accepted, "rejected": rejected, "duplicate": duplicate, "invalid_accepted": invalid_accepted, "care_attempt_rows": sum(v["care_attempt_delta"] for v in categories.values()), "care_outcome_rows": sum(v["care_outcome_delta"] for v in categories.values()), "ordinary_care_attempt_rows": categories["valid_ordinary_observation"]["care_attempt_delta"], "ordinary_care_outcome_rows": categories["valid_ordinary_observation"]["care_outcome_delta"]}
    equations["accounting_exact"] = requested_total == equations["observed_total"] == args.cycles and equations["invalid_accepted"] == 0 and equations["ordinary_care_attempt_rows"] == equations["ordinary_care_outcome_rows"] == 0
    result = {"status":"PASS" if equations["accounting_exact"] and all(lifecycle.values()) else "FAIL", "cycles":args.cycles, "seeds":seeds, "expectations":EXPECTATIONS, "categories":categories, "equations":equations, "lifecycle":lifecycle, "unknown_kind":unknown, "evidence_ceiling":"E3_TARGET_TESTED", "claim_boundary":"resident synthetic foundation evidence only; no product, safety efficacy, security certification, reliability, or SLA claim", "duration_seconds":round(time.time()-started,3)}; args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n", encoding="utf-8"); print(json.dumps(result, sort_keys=True)); raise SystemExit(0 if result["status"] == "PASS" else 1)

if __name__ == "__main__": main()
