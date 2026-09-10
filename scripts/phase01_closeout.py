#!/usr/bin/env python3
"""Fail-closed, resident Phase 01 closeout matrix.

This drives the real supervisor control socket and inspects only synthetic
XDG state. It is evidence infrastructure, not Companion product behavior.
"""
import argparse, json, os, pathlib, signal, socket, sqlite3, subprocess, tempfile, time, uuid

ROOT = pathlib.Path(__file__).resolve().parents[1]

def command(sock_path, payload):
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
        s.settimeout(3); s.connect(str(sock_path)); s.sendall((json.dumps(payload)+"\n").encode()); s.shutdown(socket.SHUT_WR)
        data = s.recv(65536)
    return json.loads(data)

def health(sock_path):
    r = command(sock_path, {"command":"health"})
    return json.loads(r["health"]) if "health" in r else r

def wait_for(sock_path, predicate, timeout=8):
    deadline = time.time()+timeout; last = {}
    while time.time() < deadline:
        try:
            last = health(sock_path)
            if predicate(last): return last
        except (OSError, ValueError, KeyError): pass
        time.sleep(.05)
    return last

def attempts(db):
    if not db.exists(): return 0
    try:
        with sqlite3.connect(db, timeout=1) as c:
            return c.execute("select count(*) from safety_attempts").fetchone()[0]
    except sqlite3.Error: return 0

def send(sock_path, kind, db, baseline):
    response = command(sock_path, {"command":"inject", "kind":kind})
    if response.get("accepted") is not True: raise RuntimeError(f"control injection rejected: {kind}: {response}")
    deadline=time.time()+5
    while time.time()<deadline and attempts(db) <= baseline: time.sleep(.01)
    return attempts(db) == baseline+1

def row(snapshot, role): return next((x for x in snapshot.get("children",[]) if x.get("role")==role), None)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--output", required=True, type=pathlib.Path); ap.add_argument("--cycles", type=int, default=3000); ap.add_argument("--seeds", default="17,23,41"); args=ap.parse_args()
    if args.cycles < 3000: raise SystemExit("cycles must be at least 3000")
    binary=os.environ.get("FOUNDATION_SUPERVISOR", str(ROOT/"target/release/ops-supervisor")); seeds=[int(x) for x in args.seeds.split(",") if x]
    categories=["valid","duplicate","replay","malformed","unsupported_major","unknown_field","invalid_uuid","invalid_datetime","duplicate_key","stale_generation","invalid_mac","companion_state","ordinary_observation","unauthorized_sender"]
    counts={k:0 for k in categories}; lifecycle={}; started=time.time()
    with tempfile.TemporaryDirectory(prefix="companion-closeout-") as root:
        env=os.environ.copy(); env.update(COMPANION_XDG_ROOT=root, COMPANION_CYCLES="1", COMPANION_SEEDS=','.join(map(str,seeds)))
        proc=subprocess.Popen([binary], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        runtime=pathlib.Path(root)/"companion"; sock=runtime/"supervisor.sock"; care_db=runtime/"../companion/care.sqlite3"
        # Store::open places the care DB under data/companion; override roots map all bases here.
        care_db=pathlib.Path(root)/"companion"/"care.sqlite3"
        try:
            snap=wait_for(sock, lambda x: {"companion-core","identity-consent-vault","godot-bridge","sensor-gateway","care-core"}.issubset({r.get("role") for r in x.get("children",[])}) and all(r.get("ready") for r in x.get("children",[])), 10)
            lifecycle["startup_ready"] = bool(row(snap,"care-core") and row(snap,"sensor-gateway")) and all(r.get("ready") for r in snap.get("children",[]))
            if not lifecycle["startup_ready"]: raise RuntimeError("roles did not become ready")
            before_attempts=attempts(care_db)
            # Three deterministic seed segments alter category order.
            target=args.cycles
            for i in range(target):
                seed=seeds[i % len(seeds)]
                kind="valid" if i % 13 == 0 else categories[(i + seed) % len(categories)]
                if kind=="valid" and counts["valid"]>0 and i % 29 == 0: kind="duplicate"
                if kind == "unauthorized_sender": kind = "forged_producer"
                if kind not in counts and kind != "forged_producer": kind="valid"
                count_key = "unauthorized_sender" if kind == "forged_producer" else kind
                if send(sock, kind, care_db, before_attempts): counts[count_key]+=1; before_attempts+=1
                else: raise RuntimeError(f"attempt not durably observed: {kind}")
            lifecycle["mixed_messages"] = sum(counts.values()) == target
            old_companion=row(snap,"companion-core")["pid"]
            command(sock,{"command":"restart","role":"companion-core"})
            snap=wait_for(sock, lambda x: row(x,"companion-core") and row(x,"companion-core").get("pid") != old_companion and row(x,"companion-core").get("ready") is True)
            lifecycle["companion_restart"] = bool(row(snap,"companion-core") and row(snap,"companion-core").get("restarts",0)>=1)
            old_sensor=row(snap,"sensor-gateway")["pid"]; old_generation=row(snap,"sensor-gateway")["generation"]
            command(sock,{"command":"rotate","role":"sensor-gateway"})
            snap=wait_for(sock, lambda x: row(x,"sensor-gateway") and row(x,"sensor-gateway").get("pid") != old_sensor and row(x,"sensor-gateway").get("generation") != old_generation)
            lifecycle["producer_rotation"] = bool(row(snap,"sensor-gateway") and row(snap,"sensor-gateway").get("pid") != old_sensor)
            old_care=row(snap,"care-core")["pid"]
            command(sock,{"command":"fail","role":"care-core"})
            degraded=wait_for(sock, lambda x: x.get("care_coverage")=="degraded", 3)
            recovered=wait_for(sock, lambda x: x.get("care_coverage")=="synthetic" and row(x,"care-core") and row(x,"care-core").get("pid") != old_care, 10)
            lifecycle["care_degraded_recovered"] = degraded.get("care_coverage")=="degraded" and recovered.get("care_coverage")=="synthetic"
            command(sock,{"command":"set_test_store_fault"})
            degraded_store=wait_for(sock, lambda x: x.get("care_coverage")=="degraded", 5)
            command(sock,{"command":"clear_test_fault"})
            recovered_store=wait_for(sock, lambda x: x.get("care_coverage")=="synthetic", 10)
            lifecycle["care_store_fault_recovery"] = degraded_store.get("care_coverage")=="degraded" and recovered_store.get("care_coverage")=="synthetic"
            command(sock,{"command":"disconnect","role":"godot-bridge"})
            bridge=wait_for(sock, lambda x: row(x,"godot-bridge") and row(x,"godot-bridge").get("restarts",0)>=1, 10)
            lifecycle["bridge_replacement"] = bool(row(bridge,"godot-bridge") and row(bridge,"godot-bridge").get("restarts",0)>=1)
            command(sock,{"command":"shutdown"}); proc.wait(timeout=10)
            lifecycle["clean_shutdown"] = proc.returncode==0
        finally:
            if proc.poll() is None:
                proc.send_signal(signal.SIGTERM); proc.wait(timeout=10)
        expected_rejections={k for k in categories if k not in ("valid",)}
        with sqlite3.connect(care_db) as c:
            rows=c.execute("select reason,count(*) from safety_attempts group by reason").fetchall()
        reasons=dict(rows)
        result={"status":"PASS" if lifecycle.get("mixed_messages") and all(lifecycle.values()) and attempts(care_db)>=target else "FAIL", "cycles":target,"seeds":seeds,"counts":counts,"lifecycle":lifecycle,"rejection_reasons":reasons,"attempts":attempts(care_db),"evidence_ceiling":"E3_TARGET_TESTED","claim_boundary":"resident synthetic foundation closeout only; no product, safety efficacy, security certification, reliability, or SLA claim","duration_seconds":round(time.time()-started,3)}
    args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8"); print(json.dumps(result,sort_keys=True))
    if result["status"] != "PASS": raise SystemExit(1)
if __name__=="__main__": main()
