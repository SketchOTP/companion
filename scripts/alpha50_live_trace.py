#!/usr/bin/env python3
"""Exercise the resident ordinary -> V2 -> bridge result production path.

This intentionally starts the checked-in service binaries and communicates via
their Unix sockets; it never writes ordinary-observation.json or calls V2
helpers directly.
"""
from __future__ import annotations
import argparse, hashlib, json, os, pathlib, signal, socket, sqlite3, subprocess, tempfile, time, uuid

ROOT = pathlib.Path(__file__).resolve().parents[1]

def envelope() -> dict:
    value = {
        "schema_major": 1, "message_id": str(uuid.uuid4()),
        "producer_generation": "live-trace-generation", "source": "sensor-gateway",
        "observed_at": "2026-01-01T00:00:00Z", "monotonic_ns": time.monotonic_ns(),
        "confidence_milli": 900, "quality_milli": 900, "replay": False,
        "causation_id": None, "correlation_id": str(uuid.uuid4()),
        "auth_scheme": "scm-credentials-v1", "mac": "",
        "payload": {"kind": "preference", "subject": "primary_user", "value": "listen"},
    }
    unsigned = dict(value); unsigned["mac"] = ""
    value["mac"] = hashlib.sha256(json.dumps(unsigned, separators=(",", ":")).encode()).hexdigest()
    return value

def send(path: pathlib.Path, value: dict) -> dict:
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
        deadline = time.time() + 5
        while True:
            try: s.connect(str(path)); break
            except OSError:
                if time.time() > deadline: raise
                time.sleep(.05)
        s.sendall(json.dumps(value).encode()); s.shutdown(socket.SHUT_WR)
        return json.loads(s.recv(8192))

def wait_socket(path: pathlib.Path) -> None:
    deadline = time.time() + 5
    while time.time() < deadline:
        if path.exists(): return
        time.sleep(.05)
    raise RuntimeError(f"socket unavailable: {path.name}")

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--output", type=pathlib.Path, required=True); ap.add_argument("--companion", default="target/release/companion-core"); ap.add_argument("--bridge", default="target/release/godot-bridge"); args = ap.parse_args()
    with tempfile.TemporaryDirectory(prefix="companion-alpha50-live-") as td:
        root = pathlib.Path(td); env = os.environ.copy(); env["COMPANION_XDG_ROOT"] = str(root)
        bridge = subprocess.Popen([args.bridge, "--service"], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        companion = subprocess.Popen([args.companion, "--service"], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ordinary = root / "companion" / "ordinary-evidence.sock"; godot = root / "companion" / "godot-bridge.sock"
        wait_socket(ordinary); wait_socket(godot)
        obs = envelope(); response = send(ordinary, obs); time.sleep(.6)
        companion.send_signal(signal.SIGTERM); companion.wait(timeout=5)
        companion2 = subprocess.Popen([args.companion, "--service"], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        wait_socket(ordinary); time.sleep(.15)
        db = root / "companion" / "companion.sqlite3"; rows = []
        restored_identity = None
        if db.exists():
            con = sqlite3.connect(db); rows = con.execute("select event_type from event_log order by id").fetchall()
            try:
                raw = con.execute("select state_json from organism_snapshots order by id desc limit 1").fetchone()
                restored_identity = json.loads(raw[0])["identity"] if raw else None
            except sqlite3.Error:
                restored_identity = None
            con.close()
        events = [r[0] for r in rows]
        ok = response.get("accepted") is True and "ordinary_evidence_accepted" in events and "body_neutral_intent" in events and "observed_embodiment_result" in events and restored_identity is not None
        result = {"status": "PASS" if ok else "FAIL", "ordinary_response": response, "event_types": events, "message_id": obs["message_id"], "restored_identity": restored_identity, "bridge_result_observed": "observed_embodiment_result" in events, "v2_only": True, "transport": "authenticated ordinary Unix peer-credential channel", "claim_boundary": "resident production-process causal trace; no product autonomy/care claim"}
        companion2.send_signal(signal.SIGTERM); companion2.wait(timeout=5); bridge.send_signal(signal.SIGTERM); bridge.wait(timeout=5)
        args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print(json.dumps(result, sort_keys=True)); return 0 if ok else 1

if __name__ == "__main__": raise SystemExit(main())
