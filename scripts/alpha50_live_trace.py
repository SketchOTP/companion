#!/usr/bin/env python3
"""Exercise the resident sensor-gateway -> companion V2 path."""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import signal
import socket
import sqlite3
import subprocess
import tempfile
import time


def request(path: pathlib.Path, value: dict) -> dict:
    deadline = time.time() + 10
    while True:
        try:
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
                sock.settimeout(3)
                sock.connect(str(path))
                sock.sendall((json.dumps(value, sort_keys=True) + "\n").encode())
                sock.shutdown(socket.SHUT_WR)
                return json.loads(sock.recv(128 * 1024))
        except OSError:
            if time.time() >= deadline:
                raise
            time.sleep(0.05)


def wait_health(control: pathlib.Path, predicate, timeout: float = 15.0) -> dict:
    deadline = time.time() + timeout
    latest = {}
    while time.time() < deadline:
        latest = request(control, {"command": "health"})
        try:
            health = json.loads(latest["health"])
        except (KeyError, TypeError, json.JSONDecodeError):
            health = {}
        if predicate(health):
            return health
        time.sleep(0.1)
    raise RuntimeError(f"health predicate did not converge: {latest}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=pathlib.Path, required=True)
    ap.add_argument("--supervisor", default="target/release/ops-supervisor")
    args = ap.parse_args()
    with tempfile.TemporaryDirectory(prefix="companion-alpha50-live-") as td:
        root = pathlib.Path(td)
        env = os.environ.copy()
        # Alpha live mode always uses the authenticated ordinary-evidence UDS.
        # The legacy JSON reader is disabled even when the compatibility
        # switch is absent; Phase 01 opts in explicitly in its own workflow.
        env.update({"COMPANION_XDG_ROOT": str(root), "COMPANION_CYCLES": "0", "COMPANION_ALPHA_LIFE": "1"})
        supervisor = subprocess.Popen([args.supervisor], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        control = root / "companion" / "supervisor.sock"
        try:
            health = wait_health(control, lambda h: all(
                any(c.get("role") == role and c.get("ready") for c in h.get("children", []))
                for role in ("sensor-gateway", "companion-core", "godot-bridge")
            ))
            db = root / "companion" / "companion.sqlite3"
            legacy = root / "companion" / "ordinary-observation.json"
            legacy.write_text(json.dumps({"message_id": "legacy-file-must-not-be-consumed", "kind": "preference", "payload": {"value": "acknowledge"}}))
            time.sleep(0.25)
            with sqlite3.connect(db) as con:
                legacy_events = int(con.execute("select count(*) from event_log where event_type = 'ordinary_observation'").fetchone()[0])
            ordinary = request(control, {"command": "inject", "kind": "valid_ordinary_observation", "request_id": "sensor-gateway-live-positive"})
            deadline = time.time() + 45
            rows = []
            snapshot = None
            while time.time() < deadline:
                con = sqlite3.connect(db)
                rows = con.execute("select message_id,event_type,payload from event_log order by id").fetchall()
                snapshot = con.execute("select state_json from organism_snapshots order by id desc limit 1").fetchone()
                con.close()
                if any(row[1] == "observed_embodiment_result" for row in rows):
                    break
                time.sleep(0.2)
            events = [row[1] for row in rows]
            first_identity = json.loads(snapshot[0])["identity"] if snapshot else None
            request(control, {"command": "kill", "role": "companion-core"})
            restarted = wait_health(control, lambda h: any(
                c.get("role") == "companion-core" and c.get("ready") and c.get("restarts", 0) >= 1
                for c in h.get("children", [])
            ))
            replay = request(control, {"command": "inject", "kind": "duplicate_ordinary_observation", "request_id": "sensor-gateway-live-positive"})
            time.sleep(0.3)
            con = sqlite3.connect(db)
            rows_after = con.execute("select message_id,event_type,payload from event_log order by id").fetchall()
            snapshot_after = con.execute("select state_json from organism_snapshots order by id desc limit 1").fetchone()
            con.close()
            final_identity = json.loads(snapshot_after[0])["identity"] if snapshot_after else None
            received = [row for row in rows_after if row[1] == "ordinary_evidence_received"]
            event_types = [row[1] for row in rows_after]
            bridge_result_observed = "observed_embodiment_result" in event_types
            ok = (ordinary.get("accepted") is True and legacy_events == 0 and len(received) == 1 and
                  replay.get("accepted") is True and "body_neutral_intent" in event_types and
                  bridge_result_observed and first_identity == final_identity)
            result = {"status": "PASS" if ok else "FAIL", "v2_only": True, "ordinary_transport": ordinary, "replay_control": replay, "event_types": event_types, "ordinary_received_count": len(received), "legacy_file_written": True, "legacy_file_event_count": legacy_events, "legacy_file_ignored": legacy_events == 0, "bridge_result_observed": bridge_result_observed, "identity_preserved": first_identity == final_identity, "supervisor_health_before_restart": health, "supervisor_health_after_restart": restarted, "producer": "checked-in sensor-gateway child via supervisor control", "claim_boundary": "resident authenticated ordinary ingress plus real Godot result required; this run fails closed when Godot is not provisioned"}
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
            print(json.dumps(result, sort_keys=True))
            return 0 if ok else 1
        finally:
            if supervisor.poll() is None:
                try:
                    request(control, {"command": "shutdown"})
                except OSError:
                    supervisor.send_signal(signal.SIGTERM)
                supervisor.wait(timeout=15)


if __name__ == "__main__":
    raise SystemExit(main())
